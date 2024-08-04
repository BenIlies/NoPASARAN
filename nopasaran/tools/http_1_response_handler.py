from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Condition
from nopasaran.definitions.events import EventNames
import threading

class HTTP1ResponseHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def __init__(self, *args, **kwargs):
        # Do not override __init__; it is handled by BaseHTTPRequestHandler
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        route_key = (self.path, method)
        route_info = getattr(self.server, 'routes', {}).get(route_key)

        if route_info:
            response_body = route_info.get('body', '')
            status_code = route_info.get('status', 200)
            headers = route_info.get('headers', {})
        else:
            response_body = 'NoPASARAN HTTP/1.1 Server'
            status_code = 900
            headers = {}

        # Send response status code
        self.send_response(status_code)

        # Add headers
        for header_name, header_value in headers.items():
            self.send_header(header_name, header_value)

        # End headers and write the response body
        self.end_headers()
        self.wfile.write(response_body.encode())

        # Store the received request data at the instance level
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else None
        self.server.received_request_data = {
            'path': self.path,
            'method': method,
            'headers': dict(self.headers),
            'body': body
        }

        # Notify that a request has been received
        with self.server.request_received:
            self.server.request_received.notify_all()

    def add_route(self, path, method, response_body, status_code, headers):
        route_key = (path, method.upper())
        self.server.routes[route_key] = {
            'body': response_body,
            'status': status_code,
            'headers': headers or {}
        }

    def remove_route(self, path, method):
        route_key = (path, method.upper())
        if route_key in self.server.routes:
            del self.server.routes[route_key]

    def add_header(self, path, method, header_name, header_value):
        route_key = (path, method.upper())
        if route_key in self.server.routes:
            self.server.routes[route_key]['headers'][header_name] = header_value

    def remove_header(self, path, method, header_name):
        route_key = (path, method.upper())
        if route_key in self.server.routes:
            headers = self.server.routes[route_key]['headers']
            if header_name in headers:
                del headers[header_name]

    def add_content_length_header(self, path, method):
        route_key = (path, method.upper())
        if route_key in self.server.routes:
            response_body = self.server.routes[route_key]['body']
            content_length = len(response_body.encode())
            self.server.routes[route_key]['headers']['Content-Length'] = content_length

    @staticmethod
    def create_server(port, handler_class):
        server_instance = HTTPServer(('', port), handler_class)
        server_instance.routes = {}
        server_instance.request_received = Condition()
        server_instance.received_request_data = None
        return server_instance

    def wait_for_request(self, port, timeout):
        server_instance = self.create_server(port, self.__class__)

        def on_timeout():
            if server_instance:
                server_instance.shutdown()
                server_instance.server_close()
                server_instance.timeout_event_triggered = True

        def serve_forever():
            server_instance.serve_forever()

        server_thread = threading.Thread(target=serve_forever)
        server_thread.start()

        with server_instance.request_received:
            if not server_instance.request_received.wait(timeout):
                on_timeout()

        server_instance.shutdown()
        server_instance.server_close()
        if getattr(server_instance, 'timeout_event_triggered', False):
            return None, EventNames.TIMEOUT.name
        return server_instance.received_request_data, EventNames.REQUEST_RECEIVED.name
