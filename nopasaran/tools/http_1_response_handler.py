from http.server import BaseHTTPRequestHandler, HTTPServer
from twisted.internet import threads

class HTTP1ResponseHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1' 
    
    routes = {}

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

def run_server_in_thread(state_machine, port=8000):
    server_address = ('', port)
    httpd_instance = HTTPServer(server_address, HTTP1ResponseHandler)

    # Running the server in a separate thread to allow Twisted to run concurrently
    def serve_forever():
        httpd_instance.serve_forever()

    state_machine.set_variable_value('httpd_instance', httpd_instance)
    return threads.deferToThread(serve_forever)

def stop_server(state_machine):
    httpd_instance = state_machine.get_variable_value('httpd_instance')
    if httpd_instance:
        httpd_instance.shutdown()
        httpd_instance.server_close()
        state_machine.set_variable_value('httpd_instance', None)