import http.server
import re
import functools


class Website:
    def __init__(self):
        self._routes = {}

    def route(self, path):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kargs):
                return f(*args, **kwargs)
            self._routes[path] = f
            return wrapper
        return decorator

    @staticmethod
    def _create_http_handler(routes):
        class WebsiteHTTPHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                for path, handler in routes.items():
                    match = re.fullmatch(path, self.path)
                    if not match:
                        continue
                    code, body = handler(*match.groups())
                    self.send_response(code)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(body))
                    self.end_headers()
                    self.wfile.write(body.encode())
                self.send_response(404)
                self.end_headers()
        return WebsiteHTTPHandler

    def run(self, address):
        website_http_handler = self._create_http_handler(self._routes)
        http_server = http.server.HTTPServer(address, website_http_handler)
        http_server.serve_forever()
