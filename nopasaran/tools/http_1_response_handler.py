from nopasaran.definitions.events import EventNames
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class HTTP1ResponseHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    routes = {}
    state_machine = None
    request_received = None
    timeout_event_triggered = False
    received_request_data = None

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

        # Store the received request data
        self.received_request_data = {
            'path': self.path,
            'method': method,
            'headers': self.headers,
            'body': self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8') if 'Content-Length' in self.headers else None
        }

        # Notify that a request has been received
        if self.request_received:
            with self.request_received:
                self.request_received.notify_all()

    def write_response_body(self, response_body):
        # Encode the response body
        response_body_bytes = response_body.encode()
        
        # End headers
        self.end_headers()
        
        # Write the response body
        self.wfile.write(response_body_bytes)

    @classmethod
    def add_route(cls, path, method, response_body, status_code, headers):
        if headers is None:
            headers = {}
        route_key = (path, method.upper())
        cls.routes[route_key] = {
            'body': response_body,
            'status': status_code,
            'headers': headers
        }

    @classmethod
    def remove_route(cls, path, method):
        route_key = (path, method.upper())
        if route_key in cls.routes:
            del cls.routes[route_key]

    @classmethod
    def add_header(cls, path, method, header_name, header_value):
        route_key = (path, method.upper())
        if route_key in cls.routes:
            cls.routes[route_key]['headers'][header_name] = header_value

    @classmethod
    def remove_header(cls, path, method, header_name):
        route_key = (path, method.upper())
        if route_key in cls.routes:
            if header_name in cls.routes[route_key]['headers']:
                del cls.routes[route_key]['headers'][header_name]

    @classmethod
    def add_content_length_header(cls, path, method):
        route_key = (path, method.upper())
        if route_key in cls.routes:
            response_body = cls.routes[route_key]['body']
            content_length = len(response_body.encode())
            cls.routes[route_key]['headers']['Content-Length'] = content_length

    @classmethod
    def wait_for_request(cls, state_machine, port, timeout):
        server_address = ('', port)
        request_received = threading.Condition()
        cls.state_machine = state_machine
        cls.request_received = request_received
        cls.timeout_event_triggered = False
        cls.received_request_data = None

        httpd_instance = HTTPServer(server_address, cls)

        # Function to stop the server
        def on_timeout():
            if httpd_instance:
                httpd_instance.shutdown()
                httpd_instance.server_close()
                cls.timeout_event_triggered = True

        # Run the server in the current thread
        def serve_forever():
            httpd_instance.serve_forever()

        server_thread = threading.Thread(target=serve_forever)
        server_thread.start()

        # Block until a request is received or the timeout occurs
        with request_received:
            if not request_received.wait(timeout):
                on_timeout()

        # Cleanup and return the appropriate response
        httpd_instance.shutdown()
        httpd_instance.server_close()
        if cls.timeout_event_triggered:
            return None, EventNames.TIMEOUT.name
        return cls.received_request_data, EventNames.REQUEST_RECEIVED.name