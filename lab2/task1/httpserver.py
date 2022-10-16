#run one command in cli: python -m http.server 9999 -b 192.168.0.105 --cgi

from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("127.0.0.1", 8000)

print('=== Start local webserver ===')

httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
