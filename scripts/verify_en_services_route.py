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
        self.class_counts={}
        self.ids=set(); self.tags={}
        self.meta={}; self.html_lang=''
        self.workstream_links=[]
        self.in_json=False; self.jsontext=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        self.tags[tag]=self.tags.get(tag,0)+1
        if a.get('id'):self.ids.add(a['id'])
        if tag=='html':self.html_lang=a.get('lang','')
        if tag=='meta':
            field=(a.get('name') or a.get('property') or '').lower()
            if field:self.meta.setdefault(field,[]).append(a.get('content',''))
        for cls in (a.get('class') or '').split():
            self.class_counts[cls]=self.class_counts.get(cls,0)+1
        if tag=='div' and 'footer-social-icons' in a.get('class',''):self.social_nodes+=1
        if tag=='div' and 'footer-map' in a.get('class','').split():self.map_nodes+=1
        if tag=='h1':self.in_h1=True
        if tag=='title':self.in_title=True
        if tag=='a' and a.get('href'):self.links.add(a['href'])
        if tag=='a' and 'seo-catalog__detail-link' in (a.get('class') or '').split():self.workstream_links.append(a.get('href',''))
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
assert ''.join(hub.title).strip()=='SEO Audits, Keyword Research & Consulting | SeoImpuls',hub.title
assert hub.html_lang.lower() in ('en-us','en'),hub.html_lang
assert len(hub.meta.get('robots',[]))==1 and hub.meta['robots'][0].startswith('index,follow'),hub.meta.get('robots')
assert len(hub.meta.get('description',[]))==1 and 'Compare SEO audits' in hub.meta['description'][0],hub.meta.get('description')
for key in ('og:title','og:description','og:url','twitter:card'):
    assert hub.meta.get(key),(key,'SEO social metadata absent')
print('SERVICES_HEAD_REPORT',json.dumps({key:hub.meta.get(key,[]) for key in ('robots','description','og:title','og:description','og:url','twitter:card','twitter:title','twitter:description')},ensure_ascii=False))

assert hub.social_nodes==0 and hub.map_nodes==0,'EN hub still contains non-branded social links or unverified location map'
hub_markup=Path('public/seo-services/index.html').read_text(encoding='utf-8')
assert 'Choose the right starting point' in hub_markup,'EN service-choice direct answer missing'
assert hub.class_counts.get('seo-catalog__area',0)==4,'Four concise scope areas required'
assert hub.class_counts.get('seo-catalog__topic',0)==12,'Three examples per work area required'
assert hub.class_counts.get('seo-catalog__workstream',0)==0,'Old 23 workstream tiles must not render'
assert not hub.workstream_links,'Workstream-specific contact links must not render'
assert 'Start with one of the three services above' in hub_markup,'Single buyer entry path missing'
assert 'These are not separate packages' in hub_markup,'Not fixed packages caveat missing'
assert 'Specialized reviews, implementation and deliverables depend' in hub_markup,'Specialist scope must be qualified'
catalog_data=json.loads(Path('data/en_seo_catalog.json').read_text(encoding='utf-8'))
assert len(catalog_data.get('scope_areas',[]))==4,'Four work areas in source'
assert all(len(x['examples'])==3 for x in catalog_data['scope_areas']),'Keep scope concise'
assert 'groups' not in catalog_data,'Old misleading 23 workstreams must not remain as source data'
assert hub.class_counts.get('seo-catalog__choice',0) == 3,'Three direct buyer entry paths are required'
pos_selector=hub_markup.find('<section class=seo-catalog__matching')
pos_directory=hub_markup.find('SEO Work We Can Scope')
if pos_selector < 0: pos_selector=hub_markup.find('<section class="seo-catalog__matching')
assert pos_selector>=0 and pos_directory>pos_selector, 'Three-way buyer selector must appear before the concise scope overview'
assert hub_markup.count('Which SEO Service Should You Start With?')==1,'Duplicate service decision selector'

assert hub.class_counts.get('seo-catalog__toc',0)==0,'Overloaded categories navigation should be removed'
assert hub.class_counts.get('seo-catalog__back',0)==0,'No repetitive return links'
assert '#seo-catalog-example' in hub.links,'Useful sample link missing'
assert 'seo-catalog-title' in hub.ids,'Main scope heading missing'
assert hub.class_counts.get('services-hub-card__consult-visual',0)==1,'Consultation graphic should not duplicate technical artwork'
assert hub.class_counts.get('seo-catalog__example',0)==1,'Demonstrable output example missing'
assert hub.class_counts.get('seo-catalog__evidence-item',0)==4,'Four evidence-to-action fields required'
assert hub.tags.get('details',0)>=5,'SEO buyer FAQ needs at least five answers'
for target in ('seo-area-technical','seo-area-content','seo-area-specialized','seo-area-strategy','seo-catalog-example'):
    assert target in hub.ids,(target,'Missing concise work area or example')
assert 'Illustrative reporting format only' in hub_markup,'Do not present an example as an actual client case'
assert 'What a Verifiable SEO Finding Looks Like' in hub_markup,'Concrete audit output example missing'
assert hub.class_counts.get('seo-catalog__real-qa',0)==1,'One verified internal QA evidence record required'
assert '<strong>not</strong> customer results' in hub_markup,'Internal report must expressly deny customer result claims'
for marker in ('Verified Internal QA Record', '38851634798', '38851849354', 'customer results', 'section at 192px'):
    assert marker in hub_markup,('Missing or untraceable internal QA proof',marker)


for required in ('What SEO Work May Include','How Scope and Deliverables Are Defined','Questions About SEO Work'):
    assert required in hub_markup,(required,'Missing useful buyer guidance')
assert '23 standalone packages' not in hub_markup,'Old 23-card FAQ language remains'
assert 'SEO work enquiry:' not in hub_markup,'Granular mailto CTAs not removed'
for path in ('/seo/','/services/keyword-research/','/services/seo-consultation/'):
    assert contains_path(hub.links,path),(path,hub.links)
crumb=[doc for doc in hub.jsonld if doc.get('@type')=='BreadcrumbList']
assert len(crumb)==1,crumb
assert not any(doc.get('@type')=='BlogPosting' for doc in hub.jsonld),'Service catalogue must not be mislabeled as a blog post'
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
