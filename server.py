import http.server
import os

PORT = int(os.environ.get("PORT", 8080))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence logs

print(f"Dashboard running on port {PORT}")
http.server.HTTPServer(("", PORT), Handler).serve_forever()
