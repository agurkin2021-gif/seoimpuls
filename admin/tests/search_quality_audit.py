"""Read-only public-site audit. Never saves content or calls admin endpoints."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'admin/test-artifacts/search-quality-20260909'
BASE = 'http://127.0.0.1:1314'
MARKERS = re.compile(r'xrumer|хрумер|xevil|gsa|scrapebox|\bpbn\b|money.?site|донор|donor|накрут|поведен|behavior|conductual|прогон|серая|черн.{0,3} seo|black.?hat|grey|gray|spam|спам|топ|top.?10|first page|primera p.gina|гарант|guarantee|garant|dr\s*\d|\d\s*dr|ahrefs|авторитет|authority|autoridad|рефераль|referral|referencia|footprint|футпринт|нейросет|ai.assistant', re.I)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    result = {'scope': BASE, 'pages': [], 'strategy': [], 'errors': []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1600, 'height': 1100})
        def guard(route):
            req = route.request
            if req.method not in ('GET', 'HEAD') or urlparse(req.url).hostname not in ('127.0.0.1', 'localhost'):
                route.abort()
            else:
                route.continue_()
        context.route('**/*', guard)
        queue, seen, urls = ['/sitemap.xml'], set(), set()
        while queue:
            path = queue.pop()
            if path in seen:
                continue
            seen.add(path)
            response = context.request.get(BASE + path)
            root = ET.fromstring(response.text())
            paths = [urlparse(el.text).path for el in root.findall('.//{*}loc')]
            if root.tag.endswith('sitemapindex'):
                queue.extend(paths)
            else:
                urls.update(paths)
        page = context.new_page()
        for index, path in enumerate(sorted(urls)):
            try:
                response = page.goto(BASE + path, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(100)
                data = page.evaluate('''() => {
                    const main = document.querySelector('main') || document.body;
                    return {
                        lang: document.documentElement.lang, title: document.title,
                        text: main.innerText, bodyText: document.body.innerText,
                        description: document.querySelector('meta[name="description" i]')?.content || '',
                        metas: [...document.querySelectorAll('meta')].map(n=>({name:n.name,property:n.getAttribute('property'),content:n.content})),
                        schema: [...document.querySelectorAll('script[type="application/ld+json"]')].map(n=>n.textContent),
                        canonical: document.querySelector('link[rel="canonical"]')?.href || '',
                        robots: document.querySelector('meta[name="robots"]')?.content || '',
                        headings: [...main.querySelectorAll('h1,h2,h3')].map(n=>({tag:n.tagName,text:n.innerText})),
                        images: [...document.images].map(n=>({src:n.currentSrc || n.src,alt:n.alt,width:n.naturalWidth,height:n.naturalHeight,loading:n.loading})),
                        links: [...document.querySelectorAll('a[href]')].map(n=>({text:n.innerText,href:n.href,rel:n.rel,affiliateTarget:n.dataset.seoCloakedHref || ''})),
                        paragraphs: [...main.querySelectorAll('p,li')].map(n=>n.innerText).filter(t=>t.length>70)
                    };
                }''')
                data.update(path=path, status=response.status, finalUrl=page.url)
                data['matches'] = [line for line in data['text'].splitlines() if MARKERS.search(line)]
                result['pages'].append(data)
                print(f'{index+1}/{len(urls)} {response.status} {path}', flush=True)
            except Exception as exc:
                result['errors'].append({'path': path, 'error': str(exc)})
        for lang, path in [('ru', '/ru/konstruktor-seo-strategii/'), ('en', '/seo-strategy-builder/'), ('es', '/es/constructor-estrategias-seo/')]:
            try:
                page.goto(BASE + path, wait_until='domcontentloaded')
                reject = page.locator('#gdprReject')
                if reject.count() and reject.is_visible():
                    reject.press('Enter')
                for key in ('onepage', 'high', 'gray', 'drops', 'static', 'xr_forums', 'xr_comments', 'xr_profiles', 'gsa_articles', 'gsa_web20', 'gsa_t123', 'social', 'branding'):
                    page.locator(f'.sb-btn[data-key="{key}"]').click()
                for key, amount in [('pbn', 2), ('crowd', 5)]:
                    page.locator(f'.sb-btn[data-key="{key}"]').click()
                    page.locator(f'#sbQtyWheel [data-value="{amount}"]').click()
                    page.locator('.sb-qty-backdrop').click(position={'x': 3, 'y': 3})
                page.locator('.sb-btn[data-key="referral"]').click()
                page.locator('#sbApply').click()
                page.wait_for_function("document.querySelector('#sbResponse ul') !== null")
                data = {'lang': lang, 'path': path, 'scenario': 'all-tools-high-risk-drop-static', 'text': page.locator('#sbResponse').inner_text(), 'tooltips': page.locator('.sb-btn').evaluate_all('nodes=>nodes.map(n=>({label:n.innerText,title:n.title}))')}
                result['strategy'].append(data)
                page.locator('#sbResponse').screenshot(path=str(OUT / f'strategy-{lang}.png'))
                for key in ('white', 'mid', 'multipage', 'dynamic', 'newregs'):
                    page.locator(f'.sb-btn[data-key="{key}"]').click()
                page.wait_for_timeout(100)
                result['strategy'].append({'lang': lang, 'path': path, 'scenario': 'all-tools-standard-new-dynamic', 'text': page.locator('#sbResponse').inner_text()})
            except Exception as exc:
                result['errors'].append({'path': path, 'phase': 'strategy', 'error': str(exc)})
        browser.close()
    (OUT / 'evidence.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    text = '\n\n'.join('URL: '+p['path']+'\n'+p['text'] for p in result['pages'])
    text += '\n\n'+'\n\n'.join('STRATEGY: '+p['lang']+' '+p['scenario']+'\n'+p['text'] for p in result['strategy'])
    (OUT / 'visible-text.txt').write_text(text, encoding='utf-8')
    images = {}
    for item in result['pages']:
        for img in item['images']:
            entry = images.setdefault(img['src'], dict(img, pages=[]))
            entry['pages'].append(item['path'])
    (OUT / 'images.json').write_text(json.dumps(list(images.values()), ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pages': len(result['pages']), 'images': len(images), 'scenarios': len(result['strategy']), 'errors': result['errors']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
