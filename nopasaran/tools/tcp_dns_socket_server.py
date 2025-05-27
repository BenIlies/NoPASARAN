import socket
import struct
import select
import time
from dnslib import DNSRecord, RR, QTYPE, A, CNAME, MX, TXT, NS, SOA, PTR, AAAA, SRV, DS, RRSIG, NSEC, DNSKEY
from nopasaran.definitions.events import EventNames
import logging

class TCPDNSSocketServer:
    def __init__(self):
        self.sock = None

    def start(self, listening_ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((listening_ip, port))
        self.sock.listen(5)
        logging.info(f"TCP DNS server started on {listening_ip}:{port}")
        return EventNames.SERVER_STARTED.name, f"TCP DNS server started on {listening_ip}:{port}"

    def wait_for_query(self, timeout, response_spec=None):
        timeout = float(timeout)
        start_time = time.time()
        self.sock.setblocking(False)

        logging.info(f"Waiting for connections on port {self.sock.getsockname()[1]} with timeout {timeout} seconds")

        while True:
            remaining_time = timeout - (time.time() - start_time)
            logging.debug(f"Remaining time: {remaining_time:.2f} seconds")
            if remaining_time <= 0:
                logging.warning("Timeout reached with no connection.")
                return {"received": None}, EventNames.TIMEOUT.name

            ready, _, _ = select.select([self.sock], [], [], remaining_time)
            if ready:
                client_sock, client_addr = self.sock.accept()
                logging.info(f"Accepted connection from {client_addr}")

                try:
                    client_sock.settimeout(5)
                    length_data = client_sock.recv(2)
                    logging.debug(f"Received length_data: {length_data}")

                    if len(length_data) < 2:
                        logging.error("Incomplete length_data")
                        return {"received": None}, EventNames.ERROR.name

                    expected_length = struct.unpack("!H", length_data)[0]
                    logging.debug(f"Expecting {expected_length} bytes of query data")

                    request_data = b""
                    receive_start_time = time.time()
                    receive_timeout = 5  # seconds

                    while len(request_data) < expected_length:
                        if time.time() - receive_start_time > receive_timeout:
                            logging.warning("Timeout while receiving DNS query data")
                            return {"received": None}, EventNames.TIMEOUT.name

                        try:
                            chunk = client_sock.recv(expected_length - len(request_data))
                            if not chunk:
                                logging.error("Connection closed before full query received")
                                return {"received": None}, EventNames.ERROR.name
                            request_data += chunk
                            logging.debug(f"Received {len(request_data)}/{expected_length} bytes")
                        except socket.timeout:
                            logging.warning("Socket recv() timed out")
                            return {"received": None}, EventNames.TIMEOUT.name

                    if not request_data:
                        logging.error("No request data received")
                        return {"received": None}, EventNames.ERROR.name

                    logging.debug("Parsing DNS query...")
                    parsed_query = DNSRecord.parse(request_data)
                    logging.info(f"Parsed query:\n{parsed_query.toZone()}")

                    logging.debug("Building DNS response...")
                    response = self.build_response(parsed_query, response_spec)

                    logging.debug("Sending DNS response...")
                    self.send_dns_response(client_sock, response)
                    logging.info("DNS response sent successfully.")

                    return {
                        "received": str(parsed_query.q)
                    }, EventNames.REQUEST_RECEIVED.name

                finally:
                    logging.debug("Closing client socket")
                    client_sock.close()

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

    def send_dns_response(self, client_sock, dns_record):
        response_bytes = dns_record.pack()
        length_prefix = struct.pack("!H", len(response_bytes))
        try:
            client_sock.sendall(length_prefix + response_bytes)
            return EventNames.RESPONSE_SENT.name
        except Exception as e:
            logging.error(f"Failed to send DNS response: {e}", exc_info=True)
            return EventNames.ERROR.name

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        logging.info("TCP socket closed")
        return EventNames.CONNECTION_ENDING.name