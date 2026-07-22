#!/usr/bin/env python3
"""Dev server with HTTP Range support (needed for <video> playback).
Usage: python3 tools/serve.py [port]   (default 8742, serves repo root)
"""
import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class RangeHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        range_header = self.headers.get("Range")
        if not range_header:
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None
        size = os.fstat(f.fileno()).st_size
        m = re.match(r"bytes=(\d*)-(\d*)", range_header)
        if not m:
            f.close()
            return super().send_head()
        if m.group(1):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else size - 1
        elif m.group(2):
            # Suffix range: last N bytes (how Chrome fetches the trailing moov atom)
            start = max(0, size - int(m.group(2)))
            end = size - 1
        else:
            f.close()
            return super().send_head()
        end = min(end, size - 1)
        if start > end or start >= size:
            f.close()
            self.send_error(416, "Requested Range Not Satisfiable")
            return None
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        f.seek(start)
        self._range_remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)
        self._range_remaining = None


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8742
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    handler = partial(RangeHandler, directory=root)
    print(f"Serving {os.path.abspath(root)} on http://localhost:{port} (with Range support)")
    ThreadingHTTPServer(("", port), handler).serve_forever()
