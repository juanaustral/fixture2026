#!/usr/bin/env python3
"""Fixture data server — sirve /fixture.json (lee de /root/dashboard/data.json)"""
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler

DATA_FILE = "/root/dashboard/data.json"
PORT = 8590

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/fixture.json":
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                body = json.dumps(data, ensure_ascii=False).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                self.send_error(500, str(e))
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # silent

if __name__ == "__main__":
    print(f"Fixture server on :{PORT}")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
