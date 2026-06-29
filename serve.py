#!/usr/bin/env python3
"""Tiny static server for the NZ:Portable web build.

Serves the ./web folder with the correct MIME types (notably application/wasm,
so the browser can stream-compile the engine). WebAssembly will not load from a
file:// double-click, so use this (or any static HTTP server) instead.

    python3 serve.py            # http://localhost:8000/
    python3 serve.py 9000       # custom port

Then open the printed URL. index.html is the normal build;
nzportable-standalone.html is the single-file engine variant.
"""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
        ".js": "text/javascript",
        ".pk3": "application/octet-stream",
        ".fmf": "text/plain",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    os.chdir(ROOT)
    with http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"  normal build : http://localhost:{PORT}/index.html")
        print(f"  single-file  : http://localhost:{PORT}/nzportable-standalone.html")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")
