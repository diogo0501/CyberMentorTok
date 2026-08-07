from __future__ import annotations

import argparse
import os
import re
import socketserver
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)$")


class QuietThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        # Browsers frequently cancel media requests while seeking, scrolling,
        # switching videos or discarding preload work. On Windows this appears
        # as ConnectionResetError / WinError 10054 and is expected behaviour.
        return


class MediaRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range_remaining", None)
        try:
            if remaining is None:
                super().copyfile(source, outputfile)
                return

            while remaining > 0:
                chunk = source.read(min(256 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # A media element has cancelled an in-flight request. This is not a
            # server failure and should not flood the terminal with tracebacks.
            return

    def send_head(self):
        path = self.translate_path(self.path)

        if os.path.isdir(path):
            return super().send_head()

        try:
            file = open(path, "rb")
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            stat = os.fstat(file.fileno())
            size = stat.st_size
            range_header = self.headers.get("Range")

            if not range_header:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", self.guess_type(path))
                self.send_header("Content-Length", str(size))
                self.send_header("Last-Modified", self.date_time_string(stat.st_mtime))
                self._range_remaining = None
                self.end_headers()
                return file

            match = RANGE_RE.fullmatch(range_header.strip())
            if not match:
                self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                file.close()
                return None

            start_text, end_text = match.groups()
            if not start_text and not end_text:
                self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                file.close()
                return None

            if start_text:
                start = int(start_text)
                end = int(end_text) if end_text else size - 1
            else:
                suffix = int(end_text)
                suffix = min(suffix, size)
                start = size - suffix
                end = size - 1

            if start >= size or start < 0 or end < start:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                file.close()
                return None

            end = min(end, size - 1)
            length = end - start + 1
            file.seek(start)
            self._range_remaining = length

            self.send_response(HTTPStatus.PARTIAL_CONTENT)
            self.send_header("Content-type", self.guess_type(path))
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
            self.send_header("Last-Modified", self.date_time_string(stat.st_mtime))
            self.end_headers()
            return file
        except Exception:
            file.close()
            raise

    def log_message(self, fmt, *args):
        # Keep useful request logs, but avoid noisy stack traces for expected
        # browser disconnects handled above.
        super().log_message(fmt, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description="CyberMentorTok local media server")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    with QuietThreadingHTTPServer((args.bind, args.port), MediaRequestHandler) as server:
        print(f"Serving CyberMentorTok at http://{args.bind}:{args.port}/")
        print("Range requests enabled for MP4/WebM playback. Press Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
