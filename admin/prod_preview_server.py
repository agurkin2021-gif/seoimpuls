from __future__ import annotations

import argparse
import gzip
import mimetypes
import posixpath
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


COMPRESSIBLE_PREFIXES = (
    "text/",
    "application/javascript",
    "application/json",
    "application/xml",
    "image/svg+xml",
)


def is_compressible(content_type: str) -> bool:
    clean = content_type.split(";", 1)[0].strip().lower()
    return any(clean.startswith(prefix) for prefix in COMPRESSIBLE_PREFIXES)


def cache_control_for(path: Path, content_type: str) -> str:
    if path.name == "index.html" or content_type.startswith("text/html"):
        return "no-store, no-cache, must-revalidate, max-age=0"
    return "public, max-age=2592000, immutable"


class PreviewHandler(BaseHTTPRequestHandler):
    server_version = "SeoimpulsPreview/1.0"

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        self.serve_file()

    def do_HEAD(self) -> None:
        self.serve_file(head_only=True)

    def serve_file(self, head_only: bool = False) -> None:
        public_root: Path = self.server.public_root  # type: ignore[attr-defined]
        parsed = urllib.parse.urlparse(self.path)
        raw_path = urllib.parse.unquote(parsed.path or "/")
        clean_path = posixpath.normpath("/" + raw_path.lstrip("/")).lstrip("/")
        target = (public_root / clean_path).resolve()

        try:
            target.relative_to(public_root)
        except ValueError:
            self.send_error(403)
            return

        if target.is_dir():
            target = target / "index.html"
        if not target.exists() or not target.is_file():
            fallback = target / "index.html"
            if fallback.exists() and fallback.is_file():
                target = fallback
            else:
                self.send_error(404)
                return

        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        data = target.read_bytes()
        accepts_gzip = "gzip" in (self.headers.get("Accept-Encoding") or "").lower()
        use_gzip = accepts_gzip and is_compressible(content_type)
        if use_gzip:
            data = gzip.compress(data, compresslevel=9)

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", cache_control_for(target, content_type))
        if target.name == "index.html" or content_type.startswith("text/html"):
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        self.send_header("Vary", "Accept-Encoding")
        if use_gzip:
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args()

    public_root = Path(args.root).resolve()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), PreviewHandler)
    server.public_root = public_root  # type: ignore[attr-defined]
    server.serve_forever()


if __name__ == "__main__":
    main()
