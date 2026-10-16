#!/usr/bin/env python3
"""RU homepage must mirror the current seven-card EN homepage for copy review."""
from html.parser import HTMLParser
from pathlib import Path
import json

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_h1=False
        self.h1=[]
        self.text=[]
        self.services=[]
        self.links=[]
        self.anchors=set()
        self.canonical=[]
        self.hero={}
        self.language=""
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html":self.language=a.get("lang","")
        if tag=="h1":self.in_h1=True
        if a.get("id"):self.anchors.add(a["id"])
        if tag=="article" and a.get("data-home-service"):self.services.append(a["data-home-service"])
        if tag=="a":
            href=a.get("href","")
            self.links.append(href)
            if a.get("data-home-link-field"):self.hero[a["data-home-link-field"]]=href
        if tag=="link" and a.get("rel")=="canonical":self.canonical.append(a.get("href",""))
    def handle_endtag(self,tag):
        if tag=="h1":self.in_h1=False
    def handle_data(self,s):
        self.text.append(s)
        if self.in_h1:self.h1.append(s)

def norm(s):return " ".join(s.split())
root=Path("public")
p=Page();p.feed((root/"ru/index.html").read_text(encoding="utf-8"))
ru=json.loads(Path("data/ru_home_services.json").read_text(encoding="utf-8"))
en=json.loads(Path("data/en_home_services.json").read_text(encoding="utf-8"))
copy=json.loads(Path("data/ru_home_copy.json").read_text(encoding="utf-8"))
txt=norm(" ".join(p.text))
assert p.language.lower().startswith("ru"),p.language
assert norm("".join(p.h1))=="Профессиональные SEO-услуги",p.h1
assert len(p.canonical)==1 and p.canonical[0].endswith("/ru/"),p.canonical
assert len(ru)==len(en)==7 and [x["id"] for x in ru]==[x["id"] for x in en]
assert [x["id"] for x in ru]==["seo-audit","keyword-research","on-page-seo",
                               "local-seo","international-seo","seo-consultation","seo-retainer"]
assert p.services==[x["id"] for x in ru],p.services
assert {"services","how-it-works","contact-project"}<=p.anchors
assert p.hero=={"heroBuilderUrl":"/ru/#services","heroCasesUrl":"/ru/#contact-project"},p.hero
assert len([x for x in ru if x.get("route")])==3
assert len([x for x in ru if x.get("featured")])==1
merged={x["id"]:(x["summary"]+" "+x["outcome"]).lower() for x in ru}
for term in ("индексац","скорост","перенаправлен"):
    assert term in merged["seo-audit"],("SEO-аудит без технической диагностики",term)
for term in ("запрос","конкурент","тем"):
    assert term in merged["keyword-research"],("Семантика без конкурентов",term)
for term in ("заголовк","текст","ссылк"):
    assert term in merged["on-page-seo"],("Оптимизация без работы над контентом",term)
for x in ru:
    for k in ("title","summary","outcome"):
        assert x[k] in txt,(x["id"],k)
    if x.get("route"):assert x["route"] in p.links,x
for key in ("servicesHeading","servicesLead","scopeNote","processHeading","processLead",
            "definitionHeading","definitionText","deliverablesHeading","deliverablesLead",
            "faqHeading","contactHeading","contactText"):
    assert copy[key] in txt,key
for section in ("processSteps","deliverables","faq"):
    assert len(copy[section])==3,section
for section in ("deliverables","faq"):
    for item in copy[section]:
        for val in item.values():assert val in txt,(section,val)
for href in ("/ru/seo/","/ru/uslugi/semanticheskoe-yadro/","/ru/uslugi/seo-konsultaciya/",
             "/ru/faq/","/ru/about/","/ru/#contact-project"):
    assert href in p.links,href
for bad in ("линкбилдинг","обратные ссылки","поведенческие факторы",
            "vps для размещения сайта","seo services for your business"):
    assert bad not in txt.lower(),bad
assert not (root/"ru/konstruktor-seo-strategii/index.html").exists()
print("PASS: RU seven consolidated cards, merged coverage, three local details, scoped claims, FAQ/process, canonical, anchors")
