#!/usr/bin/env python3
"""Fail the Hugo candidate build if a retired URL is published or still referenced."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ORIGIN = "https://seoimpuls.com"
HOSTS = {"seoimpuls.com", "www.seoimpuls.com"}
URL_ATTRS = {"href", "action", "data-services-card-url", "data-home-link-value"}


def normalize(path: str) -> str:
    path = unquote(path or "/")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return "/" + path.strip("/") + "/" if path.strip("/") else "/"


def page_url(file: Path, site: Path) -> str:
    path = "/" + file.relative_to(site).as_posix()
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return ORIGIN + path


class PageLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in URL_ATTRS and value and tag not in {"script", "style"}:
                self.links.append((key, value))
            if tag == "meta" and key == "content" and value and re.search(
                r"\burl\s*=", value, flags=re.I
            ):
                match = re.search(r"\burl\s*=\s*['\"]?([^;'\"]+)", value, flags=re.I)
                if match:
                    self.links.append(("meta-refresh", match.group(1).strip()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("public"))
    parser.add_argument("--routes", type=Path, required=True)
    args = parser.parse_args()

    if not args.site.is_dir() or not args.routes.is_file():
        raise SystemExit("Missing generated Hugo output or retired routes manifest")

    targets = set()
    for row in args.routes.read_text(encoding="utf-8").splitlines():
        raw = row.strip()
        if raw and not raw.startswith("#"):
            if not raw.startswith("/") or "?" in raw or "#" in raw:
                raise SystemExit(f"Invalid retired URL: {raw}")
            targets.add(normalize(raw))
    if not targets:
        raise SystemExit("The retired URL manifest is empty")

    findings: list[str] = []
    for route in sorted(targets):
        local = args.site / route.lstrip("/") / "index.html"
        if local.is_file():
            findings.append(f"Still generated: {route}")
    scanned = 0
    for file in args.site.rglob("*.html"):
        scanned += 1
        page = PageLinks()
        try:
            page.feed(file.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            findings.append(f"Could not parse {file}: {exc}")
            continue
        base = page_url(file, args.site)
        for attr, raw in page.links:
            url = urlsplit(urljoin(base, raw.strip()))
            if url.hostname in HOSTS and normalize(url.path) in targets:
                findings.append(f"{file.relative_to(args.site)}: {attr} -> {raw}")
    sitemap = args.site / "sitemap.xml"
    if not sitemap.is_file():
        findings.append("Missing sitemap.xml")
    else:
        try:
            for node in ET.parse(sitemap).getroot().iter():
                if node.tag.rsplit("}", 1)[-1] == "loc" and node.text:
                    u = urlsplit(node.text.strip())
                    if u.hostname in HOSTS and normalize(u.path) in targets:
                        findings.append(f"sitemap.xml: {node.text.strip()}")
        except ET.ParseError as exc:
            findings.append(f"Could not parse sitemap.xml: {exc}")
    print(f"Retired route check: {len(targets)} routes, {scanned} HTML files.")
    for issue in findings[:50]:
        print("FAIL:", issue)
    if findings:
        print(f"FAIL: {len(findings)} references or published URLs remain.")
        return 1
    print("PASS: retired URLs are neither generated nor linked from the candidate build.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
