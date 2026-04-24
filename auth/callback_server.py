from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse


class SpotifyCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        
        print("PATH:", self.path)

        if parsed_path.path == "/callback":
            query = urlparse.parse_qs(parsed_path.query)
            code = query.get("code", [None])[0]

            print("Kod autoryzacyjny:", code)

            self.server.auth_code = code

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(b"Zalogowano! Mozesz zamknac okno.")
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SpotifyCallbackHandler)

    httpd.auth_code = None

    print(f"Server is listening http://localhost:{port}")

    httpd.handle_request()

    return httpd.auth_code