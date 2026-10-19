#!/usr/bin/env python3
"""Loopback-only static server. Started and stopped by manage.py."""
import argparse
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--token', required=True)
args = parser.parse_args()

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def do_GET(self):
        if self.path == '/__health':
            data = json.dumps({'app': 'ai-weekly', 'pid': os.getpid(), 'token': args.token}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT/'site')))
print(f'AI Weekly: http://127.0.0.1:{args.port}/', flush=True)
server.serve_forever()
