#!/usr/bin/env python3
"""Inventory affiliate outbound links in rendered Hugo HTML without auto-approving any."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


ORIGIN = "https://seoimpuls.com"
OWN_HOSTS = {"seoimpuls.com", "www.seoimpuls.com"}
AFFILIATE_HOSTS = {"vdsina.com", "www.vdsina.com"}


def is_affiliate(raw: str, base: str) -> bool:
    if not raw:
        return False
    parsed = urlsplit(urljoin(base, raw.strip()))
    if parsed.hostname in AFFILIATE_HOSTS:
        return "partner=" in parsed.query.lower()
    if parsed.hostname in OWN_HOSTS:
        return parsed.path.rstrip("/").lower() == "/go/vdsina"
    return False


class AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict[str, str]] = []
        self.active: dict[str, str] | None = None
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        d = dict(attrs)
        if tag == "a":
            if self.active is not None:
                self.finish_anchor()
            self.active = {k: (v or "") for k, v in d.items()}
            self.text = []
        elif self.active is not None and tag == "img":
            if d.get("alt"):
                self.text.append(d["alt"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.active is not None:
            self.finish_anchor()

    def handle_data(self, data: str) -> None:
        if self.active is not None:
            self.text.append(data)

    def finish_anchor(self) -> None:
        if self.active is not None:
            self.active["_text"] = " ".join(" ".join(self.text).split())
            self.items.append(self.active)
            self.active = None
            self.text = []


def main() -> int:
    args = argparse.ArgumentParser()
    args.add_argument("--site", type=Path, default=Path("public"))
    args.add_argument("--max-details", type=int, default=150)
    parsed = args.parse_args()
    if not parsed.site.is_dir():
        raise SystemExit("Site output missing")

    findings = []
    total_html = 0
    redirect_page = parsed.site / "go" / "vdsina" / "index.html"
    for file in sorted(parsed.site.rglob("*.html")):
        total_html += 1
        rel_path = file.relative_to(parsed.site).as_posix()
        if rel_path == "go/vdsina/index.html":
            continue
        collector = AnchorCollector()
        collector.feed(file.read_text(encoding="utf-8", errors="replace"))
        collector.finish_anchor()
        page_url = ORIGIN + "/" + rel_path.removesuffix("index.html")
        for anchor in collector.items:
            href = anchor.get("href", "")
            cloak = anchor.get("data-seo-cloaked-href", "")
            if not (is_affiliate(href, page_url) or is_affiliate(cloak, page_url)):
                continue
            label = anchor.get("_text") or anchor.get("aria-label") or anchor.get("title", "")
            rel_tokens = anchor.get("rel", "").lower().split()
            issues = []
            if "sponsored" not in rel_tokens or "nofollow" not in rel_tokens:
                issues.append("MISSING_SPONSORED_NOFOLLOW")
            if cloak:
                issues.append("JS_CLOAKED_TARGET")
            topic = label.casefold()
            if any(term in topic for term in ("software", "soft", "кейсы", "cases", "seo audit", "auditoría seo", "сео-аудит")):
                issues.append("MISLEADING_LABEL")
            if not any(term in topic for term in ("affiliate", "partner", "партнёр", "afiliad")):
                issues.append("NO_AFFILIATE_NOTICE_IN_LINK_LABEL")
            findings.append({
                "page": "/" + rel_path,
                "label": label[:130],
                "href": href[:180],
                "cloaked": bool(cloak),
                "rel": " ".join(rel_tokens),
                "issues": issues,
            })

    pages = sorted(set(entry["page"] for entry in findings))
    counts = Counter(issue for entry in findings for issue in entry["issues"])
    print("AFFILIATE INVENTORY (diagnostic only; no placements automatically approved)")
    print("HTML files:", total_html, "Affiliate-linked pages:", len(pages),
          "Affiliate anchors:", len(findings))
    print("Affiliate redirect endpoint retained:", redirect_page.is_file())
    print("Flags:", ", ".join(f"{key}={counts[key]}" for key in sorted(counts)) or "none")
    for item in findings[:max(0, parsed.max_details)]:
        print(f"{item['page']} | label={item['label']!r} | href={item['href']!r} | "
              f"rel={item['rel']!r} | flags={','.join(item['issues']) or '-'}")
    if len(findings) > parsed.max_details:
        print("Additional links omitted:", len(findings) - parsed.max_details)
    if not findings:
        print("No affiliate links in rendered pages; endpoint may exist without incoming links.")
    print("Review every referring page for intent/disclosure BEFORE allowing it at release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
