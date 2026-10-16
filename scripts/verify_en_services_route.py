#!/usr/bin/env python3
"""Verify the English SEO hub uses one distinct canonical and retains child URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1=[]; self.in_h1=False
        self.title=[]; self.in_title=False
        self.links=set(); self.canonical=[]
        self.alternate={}; self.refresh=[]; self.jsonld=[]
        self.social_nodes=0; self.map_nodes=0
        self.in_json=False; self.jsontext=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='div' and 'footer-social-icons' in a.get('class',''):self.social_nodes+=1
        if tag=='div' and 'footer-map' in a.get('class','').split():self.map_nodes+=1
        if tag=='h1':self.in_h1=True
        if tag=='title':self.in_title=True
        if tag=='a' and a.get('href'):self.links.add(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href',''))
        if tag=='link' and a.get('rel')=='alternate':self.alternate[a.get('hreflang')]=a.get('href','')
        if tag=='meta' and a.get('http-equiv','').lower()=='refresh':self.refresh.append(a.get('content',''))
        if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.jsontext=[]
    def handle_endtag(self,tag):
        if tag=='h1':self.in_h1=False
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_json:
            self.jsonld.append(json.loads(''.join(self.jsontext)))
            self.in_json=False
    def handle_data(self,s):
        if self.in_h1:self.h1.append(s)
        if self.in_title:self.title.append(s)
        if self.in_json:self.jsontext.append(s)

def parse(path):
    f=Path('public')/path
    assert f.is_file(),f
    obj=Page();obj.feed(f.read_text(encoding='utf-8'));return obj

def contains_path(links,path):
    return any(urlsplit(link).path.endswith(path) for link in links)

hub=parse('seo-services/index.html')
assert ''.join(hub.h1).strip()=='Choose the Right SEO Work for Your Website',hub.h1
assert len(hub.canonical)==1 and hub.canonical[0].endswith('/seo-services/'),hub.canonical
assert 'Choose the Right SEO Work for Your Website' in ''.join(hub.title),hub.title
assert hub.social_nodes==0 and hub.map_nodes==0,'EN hub still contains non-branded social links or unverified location map'
hub_markup=Path('public/seo-services/index.html').read_text(encoding='utf-8')
assert 'Choose the right starting point' in hub_markup,'EN service-choice direct answer missing'
assert hub_markup.count('class="seo-catalog__group"') == 4,'Four workstream groups are required'
assert hub_markup.count('class="seo-catalog__workstream"') == 23,'All 23 scoped SEO workstreams must render'
assert hub_markup.count('class="seo-catalog__choice"') == 3,'Three direct buyer entry paths are required'
for label in ('E-commerce SEO','Local SEO & Business Profile Review','AI Search Content Readiness','International & Multilingual SEO','Earned Editorial Visibility Planning'):
    assert label in hub_markup,(label,'catalogued scope missing')
for required in ('23 standalone packages','How Scope and Deliverables Are Defined','Questions About SEO Work'):
    assert required in hub_markup,(required,'missing scope guidance')

for path in ('/seo/','/services/keyword-research/','/services/seo-consultation/'):
    assert contains_path(hub.links,path),(path,hub.links)
crumb=[doc for doc in hub.jsonld if doc.get('@type')=='BreadcrumbList']
assert len(crumb)==1,crumb
assert len(crumb[0]['itemListElement'])>=2,crumb
assert crumb[0]['itemListElement'][-1]['item'].endswith('/seo-services/'),crumb
for lang,path in [('ru','ru/uslugi/index.html'),('es','es/servicios/index.html')]:
    page=parse(path)
    assert page.alternate.get('en-us','').endswith('/seo-services/'),(lang,page.alternate)
    assert hub.alternate.get({'ru':'ru-ru','es':'es-es'}[lang],'').endswith('/'+{'ru':'ru/uslugi','es':'es/servicios'}[lang]+'/'),(lang,hub.alternate)
for path in ('index.html','about/index.html','faq/index.html'):
    pg=parse(path)
    assert contains_path(pg.links,'/seo-services/'),(path,pg.links)
for child in ('keyword-research','seo-consultation'):
    pg=parse(f'services/{child}/index.html')
    assert len(pg.canonical)==1 and pg.canonical[0].endswith('/services/'+child+'/'),(child,pg.canonical)
old=parse('services/index.html')
oldtext=(Path('public')/'services/index.html').read_text(encoding='utf-8')
assert old.refresh or re.search(r'window\.location|location\.href',oldtext,re.I),'Old URL must redirect'
assert 'seo-services/' in oldtext,'Old alias misses new hub'
assert 'Choose the Right SEO Work for Your Website' not in ''.join(old.h1),'Duplicate old catalog'
# Multilingual Hugo outputs a root sitemapindex and language-specific sitemaps.
import xml.etree.ElementTree as ET
root_sitemap=ET.parse('public/sitemap.xml').getroot()
root_locations=[(el.text or '').strip() for el in root_sitemap.iter() if el.tag.endswith('}loc') or el.tag=='loc']
assert any(x.endswith('/en/sitemap.xml') for x in root_locations),root_locations
english=ET.parse('public/en/sitemap.xml').getroot()
english_locations=[(el.text or '').strip() for el in english.iter() if el.tag.endswith('}loc') or el.tag=='loc']
assert any(urlsplit(loc).path.endswith('/seo-services/') for loc in english_locations),'Canonical hub absent from English sitemap'
assert not any(urlsplit(loc).path.endswith('/services/') for loc in english_locations),'Old alias listed in English sitemap'
print('PASS: EN SEO services hub canonical, H1, 3 services, breadcrumb and sitemap')
print('PASS: old alias redirects, EN links, hreflang reciprocal, child URLs unchanged')
