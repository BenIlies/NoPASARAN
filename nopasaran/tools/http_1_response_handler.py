from http.server import BaseHTTPRequestHandler, HTTPServer
from nopasaran.definitions.events import EventNames
import threading

class HTTP1ResponseHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    def __init__(self):
        self.routes = {}
        self.request_received = threading.Condition()
        self.timeout_event_triggered = False
        self.received_request_data = None

    def __getattr__(self, name):
        if name.startswith('do_'):
            method = name[3:]
            return lambda: self.handle_request(method)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def handle_request(self, method):
        route_key = (self.path, method)
        route_info = self.routes.get(route_key)
        
        if route_info:
            response_body = route_info.get('body')
            status_code = route_info.get('status')
            headers = route_info.get('headers')
        else:
            response_body = 'NoPASARAN HTTP/1.1 Server'
            status_code = 900
            headers = {}

        # Send response status code
        self.send_response(status_code)

        # Add headers
        for header_name, header_value in headers.items():
            self.send_header(header_name, header_value)

        # Write the response body
        self.write_response_body(response_body)

        # Store the received request data at the instance level
        self.received_request_data = {
            'path': self.path,
            'method': method,
            'headers': dict(self.headers),
            'body': self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8') if 'Content-Length' in self.headers else None
        }

        # Notify that a request has been received
        with self.request_received:
            self.request_received.notify_all()

    def write_response_body(self, response_body):
        # Encode the response body
        response_body_bytes = response_body.encode()
        
        # End headers
        self.end_headers()
        
        # Write the response body
        self.wfile.write(response_body_bytes)

    def add_route(self, path, method, response_body, status_code, headers):
        if headers is None:
            headers = {}
        route_key = (path, method.upper())
        self.routes[route_key] = {
            'body': response_body,
            'status': status_code,
            'headers': headers
        }

    def remove_route(self, path, method):
        route_key = (path, method.upper())
        if route_key in self.routes:
            del self.routes[route_key]

    def add_header(self, path, method, header_name, header_value):
        route_key = (path, method.upper())
        if route_key in self.routes:
            self.routes[route_key]['headers'][header_name] = header_value

    def remove_header(self, path, method, header_name):
        route_key = (path, method.upper())
        if route_key in self.routes:
            if header_name in self.routes[route_key]['headers']:
                del self.routes[route_key]['headers'][header_name]

    def add_content_length_header(self, path, method):
        route_key = (path, method.upper())
        if route_key in self.routes:
            response_body = self.routes[route_key]['body']
            content_length = len(response_body.encode())
            self.routes[route_key]['headers']['Content-Length'] = content_length

    def wait_for_request(self, port, timeout):
        server_instance = HTTPServer(('', port), self)
        request_received = self.request_received

        def on_timeout():
            if server_instance:
                server_instance.shutdown()
                server_instance.server_close()
                self.timeout_event_triggered = True

        def serve_forever():
            server_instance.serve_forever()

        server_thread = threading.Thread(target=serve_forever)
        server_thread.start()

        with request_received:
            if not request_received.wait(timeout):
                on_timeout()

        server_instance.shutdown()
        server_instance.server_close()
        if self.timeout_event_triggered:
            return None, EventNames.TIMEOUT.name
        return self.received_request_data, EventNames.REQUEST_RECEIVED.name
