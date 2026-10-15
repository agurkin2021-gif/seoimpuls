#!/usr/bin/env python3
"""Block affiliate placements outside explicitly approved, disclosed VPS contexts."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import sys

SITE=Path("public")
ORIGIN="https://seoimpuls.com"
EXPECTED={
    "ru/index.html":2,
    "es/index.html":2,
    "ru/uslugi/razrabotka-saitov/index.html":1,
    "es/servicios/desarrollo-web/index.html":1,
}
DESTINATION="https://www.vdsina.com/?partner=45s5fn4exi"

class Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active=None
        self.text=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.active=dict(attrs); self.text=[]
    def handle_data(self,data):
        if self.active is not None:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.active is not None:
            self.links.append((self.active," ".join(" ".join(self.text).split())))
            self.active=None;self.text=[]

issues=[]
endpoint=SITE/"go/vdsina/index.html"
if not endpoint.is_file():issues.append("Affiliate redirect endpoint missing")
else:
    raw=endpoint.read_text(encoding="utf-8")
    if 'content="noindex,nofollow,noarchive"' not in raw:issues.append("Referral endpoint missing noindex")
    if raw.count(DESTINATION)<2:issues.append("Referral destination changed")
counts={}
for html in sorted(SITE.rglob("*.html")):
    rel=html.relative_to(SITE).as_posix()
    if rel=="go/vdsina/index.html":continue
    p=Scanner();p.feed(html.read_text(encoding="utf-8",errors="replace"))
    for a,label in p.links:
        href=a.get("href","")
        cloaked=a.get("data-seo-cloaked-href","")
        target=urlsplit(urljoin(ORIGIN+"/"+rel,href))
        is_ref=(target.hostname in ("seoimpuls.com","www.seoimpuls.com") and target.path.rstrip("/")=="/go/vdsina") or (target.hostname in ("www.vdsina.com","vdsina.com") and "partner=" in target.query) or bool(cloaked)
        if not is_ref:continue
        counts[rel]=counts.get(rel,0)+1
        if rel not in EXPECTED:issues.append("Unapproved affiliate page: "+rel)
        if href!="/go/vdsina/":issues.append("Unexpected referral href: "+rel+" "+href)
        if cloaked!=DESTINATION:issues.append("Unexpected intercepted target: "+rel)
        tokens=set(a.get("rel","").lower().split())
        if not {"sponsored","nofollow"}.issubset(tokens):issues.append("Affiliate rel missing: "+rel)
        label=label.casefold()
        if not any(t in label for t in ("партнёрская ссылка","enlace de afiliado")):issues.append("Missing visible disclosure: "+rel)
        if not any(t in label for t in ("vps","hosting","сервер","proveedor")):issues.append("Referral not labeled as hosting: "+rel)
for page,expected in EXPECTED.items():
    if counts.get(page)!=expected:issues.append(f"Affiliate count mismatch {page}: expected {expected}, found {counts.get(page,0)}")
print("CONTEXTUAL AFFILIATE CHECK: inspected",sum(counts.values()),"links across",len(counts),"pages")
for issue in issues:print("FAIL:",issue)
if issues:sys.exit(1)
print("PASS: only six declared, labeled hosting referrals; no unrelated CTA interception")
