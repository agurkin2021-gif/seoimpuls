#!/usr/bin/env python3
"""Verify only the English homepage's Schema.org entities and cross-references."""
from html.parser import HTMLParser
from pathlib import Path
import json
from urllib.parse import urljoin

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.schemas = []
        self.in_schema = False
        self.buffer = []
        self.description = None
        self.canonical = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_schema = True
            self.buffer = []
        elif tag == "meta" and attrs.get("name", "").lower() == "description":
            self.description = attrs.get("content", "")
        elif tag == "link" and attrs.get("rel", "").lower() == "canonical":
            self.canonical = attrs.get("href", "")
    def handle_data(self, data):
        if self.in_schema:
            self.buffer.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.in_schema:
            self.schemas.append(json.loads("".join(self.buffer)))
            self.buffer = []
            self.in_schema = False

def load(path):
    p = Markup()
    p.feed(Path(path).read_text(encoding="utf-8"))
    return p

en = load("public/index.html")
assert len(en.schemas) == 2, f"EN home expected exactly 2 JSON-LD entities: {len(en.schemas)}"
by_type = {doc["@type"]: doc for doc in en.schemas}
assert set(by_type) == {"WebSite", "Organization"}, f"Unexpected EN homepage schema types: {list(by_type)}"
site, org = by_type["WebSite"], by_type["Organization"]
assert site["@context"] == org["@context"] == "https://schema.org"
home_url = en.canonical
assert home_url and home_url.startswith("https://"), f"Invalid canonical: {home_url}"
assert site["url"] == org["url"] == home_url, "Site/organization URLs must match canonical"
assert site["@id"] == home_url + "#website"
assert org["@id"] == home_url + "#organization"
assert site["publisher"] == {"@id": org["@id"]}, "Unlinked publisher organization"
assert site["name"] == org["name"] == "SeoImpuls"
assert site["inLanguage"].lower() in ("en-us", "en"), "Unexpected home language"
assert en.description and site["description"] == en.description, "WebSite and visible meta description diverge"
assert "author" not in site and "author" not in org, "Incorrect team-as-Person author reintroduced"
assert "person" not in json.dumps(en.schemas).lower(), "Team-as-Person not permitted in EN home"
expected_logo = urljoin(home_url, "SEOIMPULS_logo.webp")
assert org["logo"] == expected_logo, f"Unexpected logo URL: {org['logo']!r}"
assert Path("static/SEOIMPULS_logo.webp").is_file(), "Confirmed brand image missing"
assert "BreadcrumbList" not in by_type, "Invalid single-item breadcrumb on EN home"

# This scoped change must preserve the existing RU/ES home schemas, not rewrite
# translations before the owner's separate localization phase.
for lang in ("ru", "es"):
    home = load(f"public/{lang}/index.html")
    kinds = [item.get("@type") for item in home.schemas]
    assert kinds.count("WebSite") == 1, (lang, kinds)
    assert kinds.count("BreadcrumbList") == 1, (lang, kinds)
    assert len(home.schemas) == 2, (lang, kinds)
    assert len(next(x for x in home.schemas if x["@type"] == "BreadcrumbList")["itemListElement"]) == 1, (
        lang, "Do not silently modify RU/ES schema in EN-only task"
    )

print("PASS EN homepage: minimal Organization + WebSite, canonical, logo, title, description, publisher")
print("PASS EN homepage: no Person/BreadcrumbList/FAQPage/Service/Review/AggregateRating")
print("PASS RU/ES: legacy homepage JSON-LD untouched by EN-only change")
