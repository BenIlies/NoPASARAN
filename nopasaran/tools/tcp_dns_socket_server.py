import socket
import struct
import select
import time
from dnslib import DNSRecord, RR, QTYPE, A, CNAME, MX, TXT, NS, SOA, PTR, AAAA, SRV, DS, RRSIG, NSEC, DNSKEY
from nopasaran.definitions.events import EventNames

class TCPDNSSocketServer:
    def __init__(self):
        self.sock = None

    def start(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen(5)
        return EventNames.SERVER_STARTED.name, f"TCP DNS server started on port {port}"

    def wait_for_query(self, timeout, response_spec=None):
        start_time = time.time()
        self.sock.setblocking(False)

        while True:
            remaining_time = timeout - (time.time() - start_time)
            if remaining_time <= 0:
                return {"received": None}, EventNames.TIMEOUT.name

            ready, _, _ = select.select([self.sock], [], [], remaining_time)
            if ready:
                client_sock, client_addr = self.sock.accept()
                try:
                    length_data = client_sock.recv(2)
                    if len(length_data) < 2:
                        return {"received": None}, EventNames.ERROR.name

                    expected_length = struct.unpack("!H", length_data)[0]
                    request_data = b""
                    while len(request_data) < expected_length:
                        chunk = client_sock.recv(expected_length - len(request_data))
                        if not chunk:
                            break
                        request_data += chunk

                    if not request_data:
                        return {"received": None}, EventNames.ERROR.name

                    parsed_query = DNSRecord.parse(request_data)
                    response = self.build_response(parsed_query, response_spec)
                    self.send_dns_response(client_sock, response)

                    return {
                        "received": parsed_query.to_dict(),
                        "client_address": client_addr
                    }, EventNames.REQUEST_RECEIVED.name

                finally:
                    client_sock.close()

    def build_response(self, query_record, response_spec=None):
        # Use provided values or fallback to client query details
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
        if handler:
            reverse_qtype = {v: k for k, v in QTYPE.items()}
            rtype = reverse_qtype.get(response_type)

            if rtype is None:
                print(f"[Server Error] Unsupported response_type: {response_type}")
                return query_record.reply()  # Return an empty response if type is not supported

            response.add_answer(RR(rname=response_qname, rtype=rtype, rclass=1, ttl=60, rdata=handler()))
        else:
            print(f"[Server Error] No handler for response_type: {response_type}")
            return query_record.reply()  # Return an empty response if handler is missing

        return response


    def _parse_srv(self, value):
        try:
            target, port, priority, weight = value.split(",")
            return SRV(int(priority), int(weight), int(port), target)
        except Exception:
            return SRV(0, 0, 80, "service.example.com")

    def send_dns_response(self, client_sock, dns_record):
        response_bytes = dns_record.pack()
        length_prefix = struct.pack("!H", len(response_bytes))
        try:
            client_sock.sendall(length_prefix + response_bytes)
            return EventNames.RESPONSE_SENT.name
        except Exception as e:
            print(f"Failed to send DNS response: {e}")
            return EventNames.ERROR.name

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        return EventNames.CONNECTION_CLOSED.name
