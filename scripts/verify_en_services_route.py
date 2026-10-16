#!/usr/bin/env python3
"""Verify nine established SEO areas, the retainer and four direct detail routes."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import xml.etree.ElementTree as ET

ROOT = Path("public")
SITE = "https://seoimpuls.com"
SERVICES = {
    "/technical-seo-audit/": ("Technical SEO Audit", "seo", "/ru/seo/", "/es/seo/"),
    "/keyword-research/": ("Keyword Research", "keyword", "/ru/uslugi/semanticheskoe-yadro/", "/es/servicios/investigacion-palabras-clave/"),
    "/seo-consultation/": ("SEO Consultation", "consultation", "/ru/uslugi/seo-konsultaciya/", "/es/servicios/consultoria-seo/"),
}
RETAINER = "/seo-retainer/"
RETIRED_EN = (
    "/seo/", "/seo-services/", "/services/",
    "/services/keyword-research/", "/services/seo-consultation/",
)

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = []
        self.in_h1 = False
        self.title = []
        self.in_title = False
        self.links = []
        self.canonical = []
        self.alternate = {}
        self.schema = []
        self.in_schema = False
        self.json_text = []
        self.meta = {}
        self.ids = set()
        self.language = ""
        self.service_cards = []
        self.service_images = []
        self.service_marks = []
        self.service_region = 0
        self.service_ids = []
        self.offer_items = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.language = a.get("lang", "")
        if tag == "section" and a.get("id") == "services":
            self.service_region += 1
        if self.service_region and tag == "article" and a.get("data-home-service"):
            self.service_ids.append(a["data-home-service"])
        if self.service_region and tag == "img":
            self.service_images.append(a.get("src", ""))
        if self.service_region and tag == "span" and "seo-en-service-mark" in a.get("class", "").split():
            self.service_marks.append(a.get("class", ""))
        if tag == "li" and a.get("data-home-field", "").startswith("offerItem"):
            self.offer_items.append(a["data-home-field"])
        if tag == "h1":
            self.in_h1 = True
        if tag == "title":
            self.in_title = True
        if tag == "a":
            href = a.get("href", "")
            self.links.append(href)
            if self.service_region and a.get("data-home-service-link"):
                self.service_cards.append((a["data-home-service-link"], href))
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonical.append(a.get("href", ""))
            if a.get("rel") == "alternate" and a.get("hreflang"):
                self.alternate[a["hreflang"].lower()] = a.get("href", "")
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_schema = True
            self.json_text = []

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "title":
            self.in_title = False
        if tag == "section" and self.service_region:
            self.service_region -= 1
        if tag == "script" and self.in_schema:
            self.schema.append(json.loads("".join(self.json_text)))
            self.in_schema = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1.append(data)
        if self.in_title:
            self.title.append(data)
        if self.in_schema:
            self.json_text.append(data)

def load(path):
    f = ROOT / path
    assert f.is_file(), f"Missing generated HTML: {path}"
    obj = Markup()
    obj.feed(f.read_text(encoding="utf-8"))
    return obj

def title(p):
    return " ".join("".join(p.title).split())

def h1(p):
    return " ".join("".join(p.h1).split())

def schema_types(p):
    return [q.get("@type") for q in p.schema]

home = load("index.html")
assert h1(home) == "Professional SEO Services", h1(home)
assert len(home.canonical) == 1, home.canonical
BASE_URL = home.canonical[0].rstrip("/")
assert BASE_URL in ("https://seoimpuls.com", "https://agurkin2021-gif.github.io/seoimpuls"), home.canonical

def local_target(href):
    url = urlsplit(href)
    pathname = url.path
    if BASE_URL.endswith("/seoimpuls") and pathname.startswith("/seoimpuls/"):
        pathname = pathname[len("/seoimpuls"):]
    return pathname + ("#" + url.fragment if url.fragment else "")

assert home.canonical == [BASE_URL + "/"], home.canonical
assert "services" in home.ids, "Homepage service cards must have #services anchor"
EXPECTED_AREAS = ["seo-audit", "keyword-research", "on-page-seo", "technical-seo",
    "seo-competitor-analysis", "seo-content-optimization", "local-seo", "international-seo",
    "seo-consultation", "seo-retainer"]
assert home.service_ids == EXPECTED_AREAS, ("Ten distinct service area IDs required", home.service_ids)
assert len(home.service_cards) == 10, home.service_cards
assert len(home.service_marks) == 10, home.service_marks
assert {local_target(href) for kind, href in home.service_cards if kind == "details"} == set(SERVICES) | {RETAINER}, home.service_cards
assert sum(kind == "contact" and local_target(href) == "#contact-project" for kind, href in home.service_cards) == 6, home.service_cards
assert "contact-project" in home.ids, "Project enquiry anchor missing"
assert not home.service_images, f"Old service icon images remain visible: {home.service_images}"
assert all((Path("static")/path).is_file() for path in (
    "uploads/seo-icon-search-optimization.svg",
    "uploads/seo-icon-search-marketing.svg",
    "uploads/seo-icon-seo-marketing.svg"
)), "Preserved original service icon assets missing"
assert "/#services" in [local_target(x) for x in home.links], "Services navigation / hero must jump to homepage selector"
assert "seo-en-choose-title" not in home.ids, "Redundant lower 3-choice selector still on homepage"
assert not any(local_target(href).split("#")[0] in RETIRED_EN for href in home.links), "Homepage links to retired EN URLs"
assert set(schema_types(home)) == {"WebSite", "Organization"}, schema_types(home)
source_html = (ROOT / "index.html").read_text(encoding="utf-8")
assert not home.offer_items, ("Old EN supporting-work list must be absent", home.offer_items)
assert 'seo-icon-google.svg' not in source_html, "Old decorative SEO scope image still present"
assert all(term in source_html.lower() for term in (
  "seo services for your business", "seo competitor analysis", "seo content optimization",
  "international seo", "local seo", "on-page seo", "technical seo", "seo retainer",
  "keyword research spreadsheet", "for keyword research, no website is needed",
  "tell us about your seo project"
)), "Buyer-friendly service taxonomy or deliverable missing"
assert all(term not in source_html.lower() for term in (
  "discuss your website’s seo priorities", "share your website, target market",
  "performance & usability:"
)), "Old site-only CTA or 8-offer list remains"


for url, (name, _, ru, es) in SERVICES.items():
    page = load(url.lstrip("/") + "index.html")
    assert h1(page) == name, (url, h1(page))
    assert title(page) == f"{name} | SeoImpuls", (url, title(page))
    assert page.canonical == [BASE_URL + url], (url, page.canonical)
    assert page.language.lower() in ("en", "en-us"), (url, page.language)
    assert page.meta.get("description", [""])[0], (url, "Missing description")
    assert len(page.meta.get("robots", [])) == 1 and page.meta["robots"][0].startswith("index,follow"), (url, page.meta.get("robots"))
    for key in ("og:title", "og:description", "og:url", "twitter:card"):
        assert page.meta.get(key), (url, key)
    assert page.alternate.get("en-us") == BASE_URL + url, (url, "EN hreflang", page.alternate)
    assert page.alternate.get("ru-ru") == BASE_URL + ru, (url, "RU hreflang", page.alternate)
    assert page.alternate.get("es-es") == BASE_URL + es, (url, "ES hreflang", page.alternate)
    assert page.alternate.get("x-default") == BASE_URL + url, (url, "x-default", page.alternate)
    assert schema_types(page).count("WebPage") == 1, (url, schema_types(page))
    assert "BlogPosting" not in schema_types(page), (url, "Service falsely marked as blog post")
    assert schema_types(page).count("BreadcrumbList") == 1, (url, schema_types(page))
    for locale_path, code in ((ru, "ru-ru"), (es, "es-es")):
        local = load(locale_path.lstrip("/") + "index.html")
        assert local.alternate.get("en-us") == BASE_URL + url, (url, code, local.alternate)
    print("PASS: exact URL, Title, H1, metadata, schema, hreflang and direct links", url)

retainer = load("seo-retainer/index.html")
assert h1(retainer) == "SEO Retainer", h1(retainer)
assert title(retainer) == "SEO Retainer | SeoImpuls", title(retainer)
assert retainer.canonical == [BASE_URL + RETAINER], retainer.canonical
assert retainer.language.lower() in ("en", "en-us"), retainer.language
assert retainer.meta.get("description", [""])[0], "Retainer meta description missing"
assert len(retainer.meta.get("robots", [])) == 1 and retainer.meta["robots"][0].startswith("index,follow"), retainer.meta
for key in ("og:title", "og:description", "og:url", "twitter:card"):
    assert retainer.meta.get(key), (RETAINER, key)
assert schema_types(retainer).count("WebPage") == 1 and schema_types(retainer).count("BreadcrumbList") == 1, schema_types(retainer)
assert "BlogPosting" not in schema_types(retainer), schema_types(retainer)
assert {"overview", "included", "first-month", "monthly-cycle", "deliverables",
        "scope", "pricing", "comparison", "faq", "start"}.issubset(retainer.ids), retainer.ids
assert "ru-ru" not in retainer.alternate and "es-es" not in retainer.alternate, "Do not create fake translated alternates"
assert RETAINER in [local_target(href) for href in home.links], "Homepage SEO Retainer must be directly linked"
print("PASS: SEO Retainer direct page, unique intent, metadata, schema and real anchors")
kw = load("keyword-research/index.html")
assert {"what-is-included", "methodology", "deliverables"}.issubset(kw.ids), "Keyword research page sections missing"
technical = load("technical-seo-audit/index.html")
assert "technical-seo" in technical.ids, "Technical audit anchor missing"
consult = load("seo-consultation/index.html")
assert "who-it-is-for" in consult.ids, "Consultation anchor missing"

for old in RETIRED_EN:
    assert not (ROOT / old.lstrip("/") / "index.html").exists(), f"Old EN URL was still generated: {old}"

root_map = ET.parse(ROOT / "sitemap.xml").getroot()
maps = [((x.text or "").strip()) for x in root_map.iter() if x.tag.rsplit("}", 1)[-1] == "loc"]
assert BASE_URL + "/en/sitemap.xml" in maps, maps
en_map = ET.parse(ROOT / "en/sitemap.xml").getroot()
urls = {((x.text or "").strip()) for x in en_map.iter() if x.tag.rsplit("}", 1)[-1] == "loc"}
for new in tuple(SERVICES) + (RETAINER,):
    assert BASE_URL + new in urls, (new, "Missing indexed destination")
for old in RETIRED_EN:
    assert BASE_URL + old not in urls, (old, "Retired route appears in sitemap")

for path in ("about/index.html", "faq/index.html"):
    obj = load(path)
    assert "/#services" in [local_target(x) for x in obj.links], (path, "Services should lead to home selector")
    assert not any(local_target(x).split("#")[0] in RETIRED_EN for x in obj.links), (path, "Retired link")

print("PASS: four service landing pages use exact search phrase in URL, Title and H1")
print("PASS: homepage owns direct service selection; intermediate hub retired, RU/ES sources preserved")
