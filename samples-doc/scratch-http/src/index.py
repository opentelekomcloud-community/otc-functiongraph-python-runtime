from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        name = query.get("name", ["World"])[0]
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": f"Hello, {name}!"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

        return

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            content_len = int(self.headers.get("Content-Length"))
            post_body = self.rfile.read(content_len)
            self.send_response(200)
            self.end_headers()

            self.wfile.write(post_body)
        else:
            self.send_response(404)
            self.end_headers()
            response = {"message": "Not found!"}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        return


def run(
    server_class=HTTPServer, handler_class=RequestHandler, host="0.0.0.0", port=8000
):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on {host}:{port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8000
    print(f"Starting server at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), RequestHandler)
    server.serve_forever()
