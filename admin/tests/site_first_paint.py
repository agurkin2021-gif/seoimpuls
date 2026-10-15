"""Hold external CSS to detect unstyled first paints on cold navigation."""
import asyncio
import json
import sys
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from new_services_ui import ROOT

BASE='http://127.0.0.1:1314'
OUT=ROOT/'admin/test-artifacts/site-first-paint-20260909'
if '--base' in sys.argv:
    BASE=sys.argv[sys.argv.index('--base')+1].rstrip('/')
    OUT=OUT/(urlparse(BASE).hostname or 'custom')
BEFORE='--before' in sys.argv
ROUTES=['/','/ru/','/es/','/faq/','/es/faq/','/ru/faq/','/uslugi-linkbildinga/linkbilding/','/link-building-services/tier-1-2-3/']


async def inspect(browser,path,width):
    context=await browser.new_context(viewport={'width':width,'height':900},color_scheme='dark')
    page=await context.new_page()
    release=asyncio.Event();requests=[]
    async def route(r):
        u=urlparse(r.request.url)
        if u.hostname not in {'localhost','127.0.0.1',urlparse(BASE).hostname}:
            await r.abort();return
        if u.path.endswith('.css'):
            requests.append(u.path)
            await release.wait()
        await r.continue_()
    await context.route('**/*',route)
    response=await page.goto(BASE+path,wait_until='commit')
    assert response and response.status == 200, (path, response.status if response else None)
    await page.wait_for_timeout(700)
    pending=await page.evaluate('''()=>({paint:performance.getEntriesByType('paint').map(p=>p.name),header:!!document.querySelector('.custom-header'),headerDisplay:document.querySelector('.custom-header')?getComputedStyle(document.querySelector('.custom-header')).display:null,css:[...document.querySelectorAll('head link[as="style"],head link[rel="stylesheet"]')].map(e=>({href:e.getAttribute('href'),rel:e.rel,onload:e.getAttribute('onload')})),inline:!!document.querySelector('style[data-seoimpuls-inline-css="builder"],style[data-seoimpuls-inline-css="home"]')})''')
    name=(path.strip('/').replace('/','-') or 'home')+'-'+str(width)
    # With blocking CSS there is no painted frame or font readiness to capture yet.
    try:
        if 'first-contentful-paint' in pending['paint']:
            await page.screenshot(path=str(OUT/(("before-" if BEFORE else "after-")+name+'-pending.png')))
    finally:
        release.set()
    await page.wait_for_load_state('load')
    await page.wait_for_timeout(300)
    final=await page.evaluate('''()=>({paint:performance.getEntriesByType('paint').map(p=>p.name),header:!!document.querySelector('.custom-header'),headerDisplay:getComputedStyle(document.querySelector('.custom-header')).display,background:getComputedStyle(document.body).backgroundColor,overflow:document.documentElement.scrollWidth>innerWidth})''')
    await page.screenshot(path=str(OUT/(("before-" if BEFORE else "after-")+name+'-loaded.png')))
    result={'path':path,'width':width,'heldCss':requests,'pending':pending,'final':final}
    await context.close()
    if not BEFORE:
        assert final['header'] and not final['overflow'],result
        assert not any(x['rel']=='preload' for x in pending['css']),result
        if requests and not pending['inline']:
            assert 'first-contentful-paint' not in pending['paint'],result
        assert 'first-contentful-paint' in final['paint'],result
    return result


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True)
        try:
            for path in (ROUTES[:1] if BEFORE else ROUTES):
                for width in ((1600,) if BEFORE else (1600,390)):
                    result=await inspect(browser,path,width);results.append(result)
                    print(json.dumps(result),flush=True)
        finally:await browser.close()
    (OUT/('before.json' if BEFORE else 'after.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')


if __name__=='__main__':asyncio.run(main())
