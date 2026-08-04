"""Lightweight static server for the Flutter web build.

Serves frontend/build/web with:
- gzip Content-Encoding for compressible assets (js, wasm, html, css, json...)
  using pre-compressed copies in .gz_cache (built at startup + kept fresh).
- Cache-Control headers so repeated loads hit the browser cache.

Usage:
    python serve_web.py [port]   (default 3000)
"""
import gzip
import http.server
import os
import socketserver
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gz_cache")
MIN_SIZE = 1024  # skip tiny files
COMPRESSIBLE = {".js", ".css", ".html", ".json", ".wasm", ".svg", ".txt", ".map", ".dart"}


def compress_all():
    os.makedirs(CACHE, exist_ok=True)
    for dirpath, _, files in os.walk(ROOT):
        for name in files:
            src = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            if ext not in COMPRESSIBLE:
                continue
            if os.path.getsize(src) < MIN_SIZE:
                continue
            rel = os.path.relpath(src, ROOT)
            dst = os.path.join(CACHE, rel + ".gz")
            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(src, "rb") as f:
                data = f.read()
            gz = gzip.compress(data, compresslevel=6)
            with open(dst, "wb") as f:
                f.write(gz)
            print("gzip %s: %d -> %d (%.1f%%)" % (rel, len(data), len(gz), 100 * len(gz) / max(1, len(data))))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path) and "gzip" in self.headers.get("Accept-Encoding", ""):
            rel = os.path.relpath(path, ROOT)
            gz_path = os.path.join(CACHE, rel + ".gz")
            if os.path.isfile(gz_path):
                try:
                    f = open(gz_path, "rb")
                except OSError:
                    return super().send_head()
                self.send_response(200)
                self.send_header("Content-type", self.guess_type(path))
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Vary", "Accept-Encoding")
                self.send_header("Content-Length", str(os.fstat(f.fileno()).st_size))
                self.end_headers()
                return f
        return super().send_head()

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    compress_all()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), Handler) as httpd:
        print("Serving %s with gzip on port %d" % (ROOT, PORT))
        httpd.serve_forever()
