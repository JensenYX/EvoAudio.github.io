#!/usr/bin/env python3
"""Local preview server.

`python -m http.server` handles one request at a time, which this page defeats:
it asks for the framework figure, two chart SVGs and a ~900 KB demo index at
once, and the queued connections can be dropped outright. This is the same
server with threading turned on.

    python3 tools/serve.py [port]
"""

from __future__ import annotations

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # Always re-read during a preview; the demo index changes on every export.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        status = args[1] if len(args) > 1 else ""
        if status and not str(status).startswith("2"):
            super().log_message(fmt, *args)


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8811
    handler = partial(Handler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"serving {ROOT} at http://127.0.0.1:{port}/  (ctrl-c to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
