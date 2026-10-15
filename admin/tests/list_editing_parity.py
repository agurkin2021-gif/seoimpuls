"""Build an isolated copy through the admin UI and compare editor/public geometry."""
import hashlib
import json
import mimetypes
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlparse
from unittest.mock import patch

from playwright.sync_api import sync_playwright
from runtime_audit import ROOT, TEST_ROOT, BASE, HTTP, server


ARTIFACTS = ROOT / 'admin/test-artifacts'
ARTIFACTS.mkdir(exist_ok=True)
CASES = [('ru', 'index.ru.md', '/uslugi-linkbildinga/tier-1-2-3/'),
         ('en', 'index.md', '/link-building-services/tier-1-2-3/'),
         ('es', 'index.es.md', '/servicios-de-link-building/tier-1-2-3/')]


def content_hashes():
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (ROOT / 'content').rglob('*.md')}


before = content_hashes()
def copy_missing(source, target):
    if not Path(target).exists():
        shutil.copy2(source, target)
    return target

for name in ('layouts', 'themes', 'assets', 'i18n', 'static', 'modules'):
    shutil.copytree(ROOT / name, TEST_ROOT / name, dirs_exist_ok=True, copy_function=copy_missing)
for name in ('go.mod', 'go.sum'):
    if (ROOT / name).exists():
        shutil.copy2(ROOT / name, TEST_ROOT / name)


def guard(route):
    req, url = route.request, urlparse(route.request.url)
    if not req.url.startswith(BASE + '/'):
        return route.abort()
    if url.path.startswith('/site/'):
        relative = unquote(url.path[len('/site/'):])
        target = (server.PUBLIC_ROOT / relative).resolve()
        if not target.is_relative_to(server.PUBLIC_ROOT.resolve()):
            return route.abort()
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            return route.fulfill(status=404, body='Missing test asset')
        data = target.read_bytes()
        if target.suffix == '.html':
            data = re.sub(r'''((?:href|src)=["'])/(?!/)''', r'\1/site/', data.decode('utf-8')).encode('utf-8')
        return route.fulfill(body=data, content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
    if url.path == '/api/server/pause':
        return route.fulfill(json={'ok': True, 'pause': {'configured': False}})
    if url.path == '/api/deploy/status':
        return route.fulfill(json={'ok': True, 'deploy': {}})
    if req.method != 'GET' and url.path != '/api/build':
        raise AssertionError('Unexpected write: ' + url.path)
    route.continue_()


MEASURE = """() => {
    const root=document.querySelector('.seo-builder');
    const origin=root.getBoundingClientRect();
    const box=el=>{const r=el.getBoundingClientRect();return {x:r.x-origin.x,y:r.y-origin.y,w:r.width,h:r.height}};
    return [...root.querySelectorAll(':scope > .seo-builder-block')].map(el=>({
        box:box(el), text:[...el.querySelectorAll('.seo-builder-text')].map(t=>({box:box(t),html:t.innerHTML,value:t.textContent.replace(/\\s+/g,''),
            leaves:[...t.querySelectorAll('p,li')].map(p=>({text:p.textContent,box:box(p)}))})),
        headings:[...el.querySelectorAll('h2')].filter(h=>h.getBoundingClientRect().height).map(h=>({text:h.textContent,box:box(h)})),
        images:[...el.querySelectorAll('img')].map(box)}));
}"""

report = {'cases': [], 'errors': []}
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1600, 'height': 1000})
    context.route('**/*', guard)
    page = context.new_page()
    page.on('pageerror', lambda e: report['errors'].append(str(e)))
    page.goto(BASE)
    page.wait_for_function('state.pages.length > 0')
    page.locator('.nav-item[data-view="tools"]').click()
    # The build operates only in TEST_ROOT, with all service lifecycle operations disabled.
    with patch.object(server, 'stop_hugo_preview_for_build', return_value={'stopped': []}), \
         patch.object(server, 'start_hugo', side_effect=AssertionError('Must not start any service')):
        with page.expect_response(lambda r: urlparse(r.url).path == '/api/build', timeout=120000) as built:
            page.locator('#buildBtn').click()
        assert built.value.json()['ok'], built.value.text()
    page.locator('.nav-item[data-view="pages"]').click()
    for lang, filename, url in CASES:
        path = 'content/services/tier-1-2-3/' + filename
        page.evaluate('path => openPage(path)', path)
        page.wait_for_function("url=>realFrameDocument()?.location.pathname === '/site'+url && realFrameDocument()?.body?.dataset.adminFrameWired==='1'", arg=url)
        frame = page.locator('#realPageFrame').content_frame
        frame.locator('.seo-builder').wait_for()
        page.wait_for_function("[...realFrameDocument().querySelectorAll('.seo-builder img')].every(x=>x.complete && x.naturalWidth)")
        dims = page.evaluate('({width:realFrameDocument().defaultView.innerWidth,height:1000})')
        public = context.new_page()
        public.set_viewport_size(dims)
        public.goto(BASE + '/site' + url)
        public.wait_for_function("[...document.querySelectorAll('.seo-builder img')].every(x=>x.complete && x.naturalWidth)")
        public.evaluate('document.fonts.ready')
        admin_geometry = page.locator('#realPageFrame').element_handle().content_frame().evaluate(MEASURE)
        public_geometry = public.evaluate(MEASURE)
        delta = []
        assert len(admin_geometry) == len(public_geometry)
        for i, (a, b) in enumerate(zip(admin_geometry, public_geometry)):
            for key in ('x', 'y', 'w', 'h'):
                if abs(a['box'][key] - b['box'][key]) > 2:
                    delta.append([i, key, a['box'][key], b['box'][key]])
            for kind in ('text', 'headings', 'images'):
                assert len(a[kind]) == len(b[kind]), (lang, i, kind)
                for j, (at, bt) in enumerate(zip(a[kind], b[kind])):
                    if kind == 'text':
                        assert at['value'] == bt['value'], (lang, i, 'text changed',at['value'],bt['value'])
                    ab, bb = (at, bt) if kind == 'images' else (at['box'], bt['box'])
                    for key in ('x', 'y', 'w', 'h'):
                        if abs(ab[key] - bb[key]) > 2:
                            delta.append([i, kind, j, key, ab[key], bb[key]])
        page.screenshot(path=str(ARTIFACTS / f'list-parity-admin-{lang}.png'))
        public.screenshot(path=str(ARTIFACTS / f'list-parity-public-{lang}.png'), full_page=True)
        report['cases'].append({'lang': lang, 'width': dims['width'], 'delta': delta,
                                'admin': admin_geometry, 'public': public_geometry})
        print(json.dumps({'lang': lang, 'width': dims['width'], 'delta': delta}), flush=True)
        public.set_viewport_size({'width':390,'height':844})
        public.wait_for_timeout(350)
        assert public.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), (lang, 'mobile overflow')
        public.screenshot(path=str(ARTIFACTS / f'list-parity-mobile-{lang}.png'),full_page=True)
        public.close()
    browser.close()
HTTP.shutdown()
assert before == content_hashes(), 'Live content changed during the audit'
(ARTIFACTS / 'list-editing-parity.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
assert not report['errors'], report['errors']
assert all(not case['delta'] for case in report['cases']), 'Editor/public geometry differs; see report'
print('Isolated build and editor/public parity passed. Live content unchanged.')
