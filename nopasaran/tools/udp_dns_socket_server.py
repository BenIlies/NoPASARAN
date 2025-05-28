import socket
from dnslib import DNSRecord, RR, QTYPE, A, CNAME, MX, TXT, NS, SOA, PTR, AAAA, SRV, DS, RRSIG, NSEC, DNSKEY
from nopasaran.definitions.events import EventNames
import logging
import time

class UDPDNSSocketServer:
    def __init__(self):
        self.sock = None

    def start(self, listening_ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((listening_ip, port))
        logging.info(f"UDP DNS server started on {listening_ip}:{port}")
        return EventNames.SERVER_STARTED.name, f"UDP DNS server started on {listening_ip}:{port}"

    def wait_for_query(self, timeout, response_spec=None):
        self.sock.settimeout(timeout)
        logging.info(f"Waiting for UDP packets on port {self.sock.getsockname()[1]} with timeout {timeout} seconds")

        start_time = time.time()

        while True:
            try:
                remaining_time = timeout - (time.time() - start_time)
                if remaining_time <= 0:
                    logging.warning("Timeout reached while waiting for a valid DNS query.")
                    return {"received": None}, EventNames.TIMEOUT.name

                self.sock.settimeout(remaining_time)
                data, client_addr = self.sock.recvfrom(512)  # max size of a DNS UDP packet
                logging.debug(f"Received {len(data)} bytes from {client_addr}")

                logging.debug("Parsing DNS query...")
                parsed_query = DNSRecord.parse(data)

                # Check if query section is empty
                if not parsed_query.questions:
                    logging.debug("Received DNS packet with no query section. Continuing to wait...")
                    continue

                logging.info(f"Parsed query:\n{parsed_query.toZone()}")

                logging.debug("Building DNS response...")
                response = self.build_response(parsed_query, response_spec)

                logging.debug("Sending DNS response...")
                self.send_dns_response(client_addr, response)
                logging.info("DNS response sent successfully.")

                return {
                    "received": str(parsed_query.q)
                }, EventNames.REQUEST_RECEIVED.name

            except socket.timeout:
                logging.warning("Timeout reached while waiting for a valid DNS query.")
                return {"received": None}, EventNames.TIMEOUT.name
            except Exception as e:
                logging.error(f"Error while handling DNS query: {e}", exc_info=True)
                return {"received": None}, EventNames.ERROR.name

    def build_response(self, query_record, response_spec=None):
        qname = str(query_record.q.qname)
        qtype = query_record.q.qtype
        response_qname = response_spec.get("qname") if response_spec and response_spec.get("qname") else qname
        response_type = response_spec.get("type").upper() if response_spec and response_spec.get("type") else QTYPE[qtype].name
        response_value = response_spec.get("value") if response_spec else None

        response = query_record.reply()

        handlers = {
            "A": lambda: A(response_value or "127.0.0.1"),
            "CNAME": lambda: CNAME(response_value or response_qname),
            "MX": lambda: MX(response_value or f"mail.{response_qname}", preference=10),
            "TXT": lambda: TXT(response_value or f"dummy record for {response_qname}"),
            "NS": lambda: NS(response_value or f"ns1.{response_qname}"),
            "SOA": lambda: SOA(response_value or f"ns1.{response_qname}", f"admin.{response_qname}", (2024051801, 3600, 3600, 3600, 3600)),
            "PTR": lambda: PTR(response_value or f"ptr.{response_qname}"),
            "AAAA": lambda: AAAA(response_value or "::1"),
            "SRV": lambda: self._parse_srv(response_value or f"service.{response_qname},80,0,0"),
            "DS": lambda: DS(12345, 1, 1, bytes(response_value or f"abcdef{response_qname}", 'utf-8')),
            "RRSIG": lambda: RRSIG(1, 1, 0, 3600, 0, 0, 0, response_value or f"signer.{response_qname}", b"signature"),
            "NSEC": lambda: NSEC(response_value or f"next.{response_qname}", []),
            "DNSKEY": lambda: DNSKEY(256, 3, 8, bytes(response_value or f"publickey{response_qname}", 'utf-8')),
            "ANY": lambda: A(response_value or "127.0.0.1")
        }

        handler = handlers.get(response_type)
        if not handler:
            logging.warning(f"No handler for response_type: {response_type}")
            return query_record.reply()

        try:
            # Get the numeric type directly from the string using QTYPE
            rtype = QTYPE.reverse.get(response_type)
            if rtype is None:
                logging.warning(f"Unsupported response_type: {response_type}")
                return query_record.reply()

            logging.debug(f"Calling handler for type {response_type}")
            rdata = handler()
            logging.debug(f"Handler produced rdata: {rdata}")
        except Exception as e:
            logging.error(f"Handler for {response_type} failed: {e}", exc_info=True)
            return query_record.reply()

        response.add_answer(RR(rname=response_qname, rtype=rtype, rclass=1, ttl=60, rdata=rdata))
        return response

    def _parse_srv(self, value):
        try:
            target, port, priority, weight = value.split(",")
            return SRV(int(priority), int(weight), int(port), target)
        except Exception:
            logging.warning(f"Failed to parse SRV value: '{value}', using default fallback")
            return SRV(0, 0, 80, "service.example.com")

    def send_dns_response(self, client_addr, dns_record):
        try:
            self.sock.sendto(dns_record.pack(), client_addr)
            return EventNames.RESPONSE_SENT.name
        except Exception as e:
            logging.error(f"Failed to send DNS response to {client_addr}: {e}", exc_info=True)
            return EventNames.ERROR.name

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        logging.info("UDP socket closed")
        return EventNames.CONNECTION_ENDING.name