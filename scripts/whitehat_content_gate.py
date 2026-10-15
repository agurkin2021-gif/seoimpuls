#!/usr/bin/env python3
"""SEOImpuls white-hat release gate.

By default this is an informational audit of generated Hugo HTML. --strict
fails when legacy promotional content/paths survive. Affiliate referrals are separately verified by a context-aware, blocking check.
This is an intentionally broad gate for a white-hat agency rebuild; individual
findings require manual interpretation rather than automatic deletion.
"""
from __future__ import annotations
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

LEGACY_ROUTES = (
    "/link-building-services/",
    "/uslugi-linkbildinga/",
    "/servicios-de-link-building/",
    "/seo-strategy-builder/",
    "/soft/",
)

# Terms that promote legacy offerings, not generic best-practice advice.
VISIBLE_TERMS = {
    "backlink": re.compile(r"\bbacklinks?\b", re.IGNORECASE),
    "link building": re.compile(r"\blink[\s-]*building\b", re.IGNORECASE),
    "domain rating": re.compile(r"\bdomain rating\b|\bincrease dr\b", re.IGNORECASE),
    "tier networks": re.compile(r"\btier[\s-]*[123]\b|\btier[\s-]*1[\s-]*2[\s-]*3\b", re.IGNORECASE),
    "automated link tools": re.compile(r"\bxrumer\b|\bxevil\b|\bgsa[\s-]*ser\b", re.IGNORECASE),
    "PBN/satellites": re.compile(r"\bpbn\b|\bsatellite (?:site|network|websites?)\b|\bmicrosites? (?:for|to) (?:links|seo)\b", re.IGNORECASE),
    "RU links": re.compile(r"линкбилдинг|обратн\w*\s+ссылк\w*|сателлит\w*|поведенческ\w*\s+фактор\w*", re.IGNORECASE),
    "ES links": re.compile(r"\bconstrucci[oó]n de enlaces\b|\bcompra de enlaces\b|\benlaces de retroceso\b", re.IGNORECASE),
}

class RenderedPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden_depth = 0
        self.text: list[str] = []
        self.hrefs: list[str] = []
        self.meta: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        data = dict(attrs)
        if tag in {"script", "style", "svg"}:
            self.hidden_depth += 1
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"])
        if tag == "meta" and data.get("name", "").lower() == "description":
            self.meta.append(data.get("content", ""))

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg"}:
            self.hidden_depth = max(0, self.hidden_depth - 1)

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.text.append(data)

def contains_route(url: str) -> bool:
    low = url.lower()
    return any(route in low for route in LEGACY_ROUTES)

def audit(site: Path):
    records = []
    files = sorted(site.rglob("*.html"))
    for path in files:
        rel = "/" + path.relative_to(site).as_posix()
        parser = RenderedPage()
        try:
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            records.append({"page": rel, "kind": "read_error", "match": str(exc)[:120]})
            continue
        visible = " ".join(parser.text + parser.meta)
        if contains_route(rel):
            records.append({"page": rel, "kind": "legacy_public_route", "match": rel})
        for label, pattern in VISIBLE_TERMS.items():
            match = pattern.search(visible)
            if match:
                records.append({"page": rel, "kind": "legacy_visible_copy", "match": f"{label}: {match.group(0)}"})
        linked_routes = sorted({url for url in parser.hrefs if contains_route(url)})
        for url in linked_routes[:15]:
            records.append({"page": rel, "kind": "legacy_navigation", "match": url[:160]})
    xml = site / "sitemap.xml"
    if xml.exists():
        content = xml.read_text(encoding="utf-8", errors="replace")
        for route in LEGACY_ROUTES:
            if route in content.lower():
                records.append({"page": "/sitemap.xml", "kind": "sitemap_legacy_route", "match": route})
    return files, records

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="public")
    ap.add_argument("--strict", action="store_true", help="exit 2 on any issue; use for release approval")
    ap.add_argument("--max-details", type=int, default=30)
    args = ap.parse_args()
    site = Path(args.site)
    if not site.is_dir():
        print("ERROR: Hugo site output missing:", site, file=sys.stderr)
        return 1
    files, records = audit(site)
    by_kind = Counter(r["kind"] for r in records)
    impacted = sorted({r["page"] for r in records})
    print("WHITE-HAT RELEASE AUDIT")
    print("HTML pages:", len(files))
    print("Findings:", len(records), "Affected files:", len(impacted))
    print("Findings by category:", json.dumps(dict(sorted(by_kind.items())), ensure_ascii=False))
    for record in records[:max(args.max_details, 0)]:
        print(f"{record['page']} | {record['kind']} | {record['match']}")
    if len(records) > args.max_details:
        print("Additional findings omitted from log:", len(records) - args.max_details)
    if records:
        print("RELEASE READINESS: BLOCKED. All findings require review and resolution.")
        return 2 if args.strict else 0
    print("RELEASE READINESS: CONTENT/PATH SCAN PASSED (not a substitute for full technical/visual QA).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
