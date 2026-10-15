"""Isolated regressions: python admin/tests/runtime_audit.py (no deploy/build)."""
import concurrent.futures
import base64
import hashlib
import importlib.util
import json
import io
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("audit_server", ROOT / "admin/server.py")
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
TEMP = tempfile.TemporaryDirectory(prefix="seoimpuls-audit-")
TEST_ROOT = Path(TEMP.name)
for name, relative in {
    "PROJECT_ROOT": ".", "ADMIN_ROOT": "admin", "CONTENT_ROOT": "content",
    "STATIC_ROOT": "static", "UPLOAD_ROOT": "static/uploads", "PUBLIC_ROOT": "public",
    "BACKUP_ROOT": "admin/backups", "TRASH_ROOT": "admin/trash",
    "MEDIA_TRASH_ROOT": "admin/media_trash", "FILE_UPLOAD_ROOT": "static/files",
}.items():
    setattr(server, name, TEST_ROOT / relative)
    getattr(server, name).mkdir(parents=True, exist_ok=True)
server.UI_ROOT = ROOT / "admin/static"
server.CHROME_PATH = TEST_ROOT / "data/chrome.json"
server.HUGO_CONFIG_PATH = TEST_ROOT / "hugo.toml"
server.DEPLOY_CONFIG_PATH = TEST_ROOT / "no-deploy-config.json"
server.AUTH_ENABLED = False
shutil.copytree(ROOT / "content", server.CONTENT_ROOT, dirs_exist_ok=True)
shutil.copytree(ROOT / "data", TEST_ROOT / "data", dirs_exist_ok=True)
shutil.copy2(ROOT / "hugo.toml", server.HUGO_CONFIG_PATH)
for asset in (ROOT / "static").rglob("*"):
    if asset.is_file() and asset.suffix.lower() in server.IMAGE_SUFFIXES:
        target = server.STATIC_ROOT / asset.relative_to(ROOT / "static")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, target)


class Handler(server.AdminHandler):
    def log_message(self, *args):
        pass


HTTP = server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
BASE = f"http://127.0.0.1:{HTTP.server_port}"
threading.Thread(target=HTTP.serve_forever, daemon=True).start()


def request(path, data=None):
    req = urllib.request.Request(BASE + path, headers={"Content-Type": "application/json"},
                                 data=json.dumps(data).encode() if data is not None else None)
    try:
        response = urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError as error:
        response = error
    return response.status, json.loads(response.read())


class StorageTests(unittest.TestCase):
    def test_fast_asset_catalog_never_scans_documents_or_authorizes_delete(self):
        with patch.object(server, "site_text_documents", side_effect=AssertionError("Unexpected scan")), \
             patch.object(server, "asset_usage_sources", side_effect=AssertionError("Unexpected scan")):
            status, data = request("/api/assets?usage=0")
        self.assertEqual(status, 200)
        self.assertTrue(data["assets"])
        self.assertTrue(all(not item["usageKnown"] and item["used"] is None and not item["deletable"]
                            for item in data["assets"]))
        self.assertTrue(all(item["size"] > 0 and item["url"] for item in data["assets"]))

    def test_full_asset_catalog_and_delete_still_check_usage(self):
        with patch.object(server, "site_text_documents", return_value=[]) as documents, \
             patch.object(server, "asset_usage_sources", return_value=["content/reference.md"]) as usage:
            status, data = request("/api/assets")
            self.assertEqual(status, 200)
            self.assertTrue(all(item["usageKnown"] and item["used"] and not item["deletable"]
                                for item in data["assets"]))
            documents.assert_called_once()
            self.assertEqual(usage.call_count, len(data["assets"]))
            usage.reset_mock()
            status, rejected = request("/api/assets/delete", {"path": data["assets"][0]["path"]})
            self.assertEqual(status, 500)
            self.assertFalse(rejected["ok"])
            usage.assert_called_once()

    def setUp(self):
        self.relative = "content/audit/index.ru.md"
        self.target = TEST_ROOT / self.relative
        self.target.parent.mkdir(exist_ok=True)
        self.target.write_text(server.dump_front_matter({"title": "Original", "builderJson": "[]"}, "body"), encoding="utf-8")

    def test_rapid_backups_preserve_each_version(self):
        with patch.object(server.time, "strftime", return_value="20260907-000000"):
            first = server.backup_file(self.target)
            self.target.write_text("second", encoding="utf-8")
            second = server.backup_file(self.target)
        self.assertNotEqual(first, second)
        self.assertIn("Original", first.read_text(encoding="utf-8"))
        self.assertEqual(second.read_text(), "second")
        restored = server.restore_backup(first.relative_to(TEST_ROOT).as_posix())
        self.assertEqual(restored["restoredTo"], self.relative)
        self.assertIn("Original", self.target.read_text(encoding="utf-8"))

    def test_stale_tab_save_is_rejected(self):
        _, loaded = request("/api/page?path=" + self.relative)
        revision = loaded["page"].get("revision", "baseline")
        payload = {"path": self.relative, "frontmatter": {"title": "First", "builderJson": "[]"},
                   "body": "first", "expectedRevision": revision}
        status, saved = request("/api/page/save", payload)
        self.assertEqual(status, 200)
        self.assertTrue(saved["build"]["skipped"])
        payload["body"] = "stale"
        status, _ = request("/api/page/save", payload)
        self.assertEqual(status, 409)
        self.assertEqual(server.read_markdown(self.target)[1], "first")

    def test_concurrent_saves_with_same_revision_only_one_wins(self):
        _, loaded = request("/api/page?path=" + self.relative)
        revision = loaded["page"].get("revision", "baseline")
        def save(index):
            return request("/api/page/save", {"path": self.relative,
                "expectedRevision": revision, "frontmatter": {"title": str(index)}, "body": str(index)})[0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            statuses = list(pool.map(save, range(6)))
        self.assertEqual(statuses.count(200), 1, statuses)
        self.assertEqual(statuses.count(409), 5, statuses)

    def test_invalid_builder_does_not_touch_file(self):
        before = self.target.read_bytes()
        for value in ['[{broken', '[null]', '["text"]']:
            status, _ = request("/api/page/save", {"path": self.relative,
                "frontmatter": {"title": "Bad", "builderJson": value}, "body": ""})
            self.assertGreaterEqual(status, 400, value)
            self.assertEqual(self.target.read_bytes(), before)

    def test_unicode_and_escaped_builder_roundtrip(self):
        blocks = [{"type": "text", "text": '\u0422\u0435\u043a\u0441\u0442 / Colocaci\u00f3n / "quoted"'}]
        for value in [json.dumps(blocks), json.dumps(json.dumps(blocks))]:
            status, data = request("/api/page/save", {"path": self.relative,
                "frontmatter": {"title": "Unicode", "builderJson": value}, "body": ""})
            self.assertEqual(status, 200, data)
            self.assertEqual(json.loads(server.read_markdown(self.target)[0]["builderJson"]), blocks)

    def test_preview_missing_resource_never_builds(self):
        with patch.object(server, "run_hugo_build", return_value={"ok": False}) as build:
            try:
                urllib.request.urlopen(BASE + "/site/audit-definitely-missing.webp", timeout=20)
            except urllib.error.HTTPError as error:
                self.assertEqual(error.code, 404)
            build.assert_not_called()

    def test_atomic_write_failure_preserves_old_file(self):
        original = self.target.read_bytes()
        with patch.object(server.os, "replace", side_effect=OSError("simulated disk error")):
            with self.assertRaises(OSError):
                server.atomic_write_markdown(self.target, "replacement")
        self.assertEqual(self.target.read_bytes(), original)
        self.assertEqual(list(self.target.parent.glob(".admin-save-*")), [])

    def test_create_move_delete_restore_languages(self):
        status, data = request("/api/page/create", {"section": "services", "slug": "audit-lifecycle",
            "title": "Audit lifecycle", "languages": ["ru", "en", "es"], "builderJson": "[]"})
        self.assertEqual(status, 200, data)
        self.assertEqual(len(data["created"]), 3)
        for relative in data["created"]:
            _, loaded = request("/api/page?path=" + relative)
            status, moved = request("/api/page/move", {"path": relative, "section": "services",
                "slug": "audit-lifecycle-moved", "frontmatter": loaded["page"]["frontmatter"], "body": ""})
            self.assertEqual(status, 200, moved)
            self.assertFalse((TEST_ROOT / relative).exists())
            status, deleted = request("/api/page/delete", {"path": moved["path"]})
            self.assertEqual(status, 200, deleted)
            self.assertFalse((TEST_ROOT / moved["path"]).exists())
            status, restored = request("/api/trash/restore", {"trashPath": deleted["trashPath"]})
            self.assertEqual(status, 200, restored)
            self.assertTrue((TEST_ROOT / moved["path"]).exists())

    def test_upload_compress_remains_draft(self):
        from PIL import Image
        buffer = io.BytesIO()
        Image.effect_noise((360, 240), 80).convert("RGB").save(buffer, format="PNG")
        status, uploaded = request("/api/assets/upload", {"filename": "audit-image.png",
            "dataUrl": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()})
        self.assertEqual(status, 200, uploaded)
        before = self.target.read_bytes()
        status, compressed = request("/api/assets/compress", {"url": uploaded["url"], "quality": 25})
        self.assertEqual(status, 200, compressed)
        self.assertTrue((server.STATIC_ROOT / compressed["url"].lstrip("/")).exists())
        self.assertEqual(self.target.read_bytes(), before)

    def test_all_current_builder_data_parse(self):
        for path in (ROOT / "content").rglob("*.md"):
            front, _, _ = server.read_markdown(path)
            if "builderJson" in front:
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    server.normalize_front_builder_json(front, strict=True)


class BrowserTests(unittest.TestCase):
    def test_text_insert_point_and_heading_on_different_detail_pages(self):
        paths = [self.a, 'content/services/website-creation/index.ru.md',
                 'content/services/sozdanie-satellitov/index.ru.md']
        for path in paths:
            with self.subTest(path=path):
                self.page.evaluate('p=>openPage(p,{discardDirty:true})',path)
                self.page.wait_for_function('realFrameDocument()?.body?.dataset.adminFrameWired === "1"')
                self.page.evaluate('''() => {
                    const image=state.builderBlocks.find(b=>b.image)?.image;
                    state.builderBlocks=normalizeBuilderBlocks([
                        {type:'image',image,width:'full',imagePixelWidth:200,imagePixelHeight:80,pixelHeight:600},
                        {type:'text',title:'Unchanged lower heading',text:'Lower content',width:'full'}]);
                    state.selectedBlockIndex=0; clearSelectedImages();
                    renderBuilder(); updatePreview();
                }''')
                self.page.wait_for_timeout(300)
                frame=self.page.frame_locator('#realPageFrame')
                host=frame.locator('.seo-builder')
                host.scroll_into_view_if_needed()
                r=host.bounding_box()
                scale=self.page.evaluate('Number(realPageFrame.dataset.adminPreviewScale)')
                self.page.mouse.click(r['x']+24*scale,r['y']+210*scale)
                point=self.page.evaluate('state.insertPoint')
                self.assertIsNotNone(point)
                self.page.locator('[data-add-block=text]').click()
                self.page.wait_for_timeout(400)
                result=self.page.evaluate('''() => {
                    const d=realFrameDocument(),b=d.querySelector(`[data-preview-index="${state.selectedBlockIndex}"]`);
                    const r=b.getBoundingClientRect(),w=realPageWorkRect();
                    return {x:r.x-w.x,y:r.y-w.y,focused:d.activeElement?.dataset.blockField};
                }''')
                self.assertAlmostEqual(result['x'],point['x'],delta=2,msg=result)
                self.assertAlmostEqual(result['y'],point['y'],delta=2)
                self.assertEqual(result['focused'],'title')
                self.assertEqual(self.page.evaluate('compactBuilderBlockForSave(state.builderBlocks[state.selectedBlockIndex]).titleSize'),28)
                self.assertEqual(self.page.evaluate('getComputedStyle(realFrameDocument().activeElement).fontSize'),'28px')
                frame.locator(f'[data-preview-index="{self.page.evaluate("state.selectedBlockIndex")}"] [data-block-field=title]').press_sequentially('Inserted heading')

    def test_real_clipboard_keeps_selection_rich_format_and_undo(self):
        original=(TEST_ROOT/self.a).read_text(encoding='utf-8')
        self.addCleanup(server.atomic_write_markdown,TEST_ROOT/self.a,original)
        clean=self.page.evaluate('''() => safeClipboardHtml(realFrameDocument(),
            '<script>alert(1)</script><img src=x onerror="alert(1)"><p onclick="alert(1)"><strong>Safe</strong><a href="javascript:alert(1)">link</a></p>')''')
        self.assertNotIn('script',clean)
        self.assertNotIn('onclick',clean)
        self.assertNotIn('<img',clean)
        self.assertIn('<strong>Safe</strong>',clean)
        self.page.context.grant_permissions(['clipboard-read','clipboard-write'])
        self.page.wait_for_function('realFrameDocument()?.querySelector("[data-block-field=text]")')
        self.page.evaluate('''() => {
            state.builderBlocks=normalizeBuilderBlocks([{type:'text',title:'Clipboard',
                text:'### Copy heading\\n\\n**Bold** [VPS](/go/vdsina/)\\n\\nLast paragraph',width:'full'}]);
            renderBuilder(); updatePreview();
        }''')
        frame=self.page.frame_locator('#realPageFrame')
        body=frame.locator('[data-block-field=text]')
        body.click(); body.press('Control+a')
        before=self.page.evaluate('realFrameDocument().getSelection().toString()')
        body.click(button='right')
        self.page.keyboard.press('Escape')
        self.assertEqual(self.page.evaluate('realFrameDocument().getSelection().toString()'),before)
        self.assertIsNone(self.page.evaluate('state.frameDrag'))
        body.press('Control+c')
        self.assertIn('Copy heading',self.page.evaluate('navigator.clipboard.readText()'))
        body.press('Control+a')
        body.press('Control+v')
        self.assertEqual(body.locator('h3').inner_text(),'Copy heading')
        self.assertEqual(self.page.evaluate('url=>cloakedAffiliateTarget(url)',
                         body.locator('a').get_attribute('data-seo-cloaked-href') or body.locator('a').get_attribute('href')),
                         self.page.evaluate('VDSINA_PARTNER_URL'))
        self.assertEqual(body.locator('strong').inner_text(),'Bold')
        body.press('Control+z')
        self.assertEqual(body.locator('h3').count(),1,'Rich paste undo must restore the original heading')
        body.press('Control+y')
        body.press('Control+a')
        self.page.evaluate("navigator.clipboard.writeText('Plain clipboard replacement')")
        body.press('Control+v')
        self.assertEqual(body.inner_text(),'Plain clipboard replacement')
        body.press('Control+z')
        self.assertIn('Copy heading',body.inner_text())
        with self.page.expect_response(lambda r:'/api/page/save' in r.url):
            self.page.locator('#adminSaveBtn').click()
        self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        self.assertEqual(body.locator('h3').count(),1,self.page.evaluate('JSON.stringify(state.builderBlocks)'))
        self.assertEqual(body.locator('h3').inner_text(),'Copy heading')
        self.assertFalse(self.errors)

    def test_current_admin_origin_links_are_portable(self):
        result = self.page.evaluate('''() => [
            builderUrlValue(location.origin + '/site/services/?q=1#details'),
            builderUrlValue('https://example.org/external/'),
            builderUrlValue('javascript:alert(1)')
        ]''')
        self.assertEqual(result, ['/services/?q=1#details', 'https://example.org/external/', ''])

    def test_open_translation_matches_sidebar_language(self):
        self.page.locator('#langFilter').select_option('ru')
        self.page.evaluate('path=>openPage(path)',self.b)
        self.assertEqual(self.page.locator('#langFilter').input_value(),'en')
        self.assertEqual(self.page.evaluate('readStoredPageLang()'),'en')
        self.page.locator('#langFilter').select_option('')
        self.page.evaluate('path=>openPage(path)',self.a)
        self.assertEqual(self.page.locator('#langFilter').input_value(),'')
        self.page.locator('#langFilter').select_option('en')
        self.page.route('**/api/page?path=*missing*',lambda r:r.fulfill(status=404,json={'error':'Missing'}))
        self.page.evaluate("openPage('missing.md').catch(()=>{})")
        self.assertEqual(self.page.locator('#langFilter').input_value(),'en')
        self.assertEqual(self.page.evaluate('state.activePath'),self.a)
        self.assertFalse(self.errors)

    def test_home_feed_checkbox_is_saved_per_language(self):
        paths=['content/services/seo-consultation/index'+suffix+'.md' for suffix in ('.ru','','.es')]
        originals={p:(TEST_ROOT/p).read_text(encoding='utf-8') for p in paths}
        for p,original in originals.items():self.addCleanup(server.atomic_write_markdown,TEST_ROOT/p,original)
        for path in paths:
            siblings={p:(TEST_ROOT/p).read_text(encoding='utf-8') for p in paths if p!=path}
            self.page.evaluate('p=>openPage(p)',path)
            checkbox=self.page.locator('#fieldShowOnHome')
            for checked in (True,False):
                checkbox.set_checked(checked)
                with self.page.expect_response(lambda r:'/api/page/save' in r.url):
                    self.page.locator('#adminSaveBtn').click()
                self.page.wait_for_function('!state.savingPage && !state.pageLoading')
                self.assertEqual(checkbox.is_checked(),checked)
                front,_,_=server.read_markdown(TEST_ROOT/path)
                self.assertEqual(front['showOnHome'],checked)
                self.assertTrue(front.get('date'))
                for sibling,original in siblings.items():self.assertEqual((TEST_ROOT/sibling).read_text(encoding='utf-8'),original)
        self.assertFalse(self.errors)

    def test_text_affiliate_target_survives_clipboard_and_save(self):
        original=(TEST_ROOT/self.a).read_text(encoding='utf-8')
        self.addCleanup(server.atomic_write_markdown,TEST_ROOT/self.a,original)
        partner='https://www.vdsina.com/?partner=ni8gzrvz75'
        self.page.context.grant_permissions(['clipboard-read','clipboard-write'])
        self.page.evaluate('''url => {
            state.builderBlocks=normalizeBuilderBlocks([{type:'text',text:'[VPS server]('+url+')'}]);
            renderBuilder();updatePreview();
        }''',partner)
        body=self.page.frame_locator('#realPageFrame').locator('[data-block-field=text]')
        body.click();body.press('Control+a');body.press('Control+c');body.press('Control+v')
        for _ in range(2):
            with self.page.expect_response(lambda r:'/api/page/save' in r.url):
                self.page.locator('#adminSaveBtn').click()
            self.page.wait_for_function('!state.savingPage && !state.pageLoading')
            self.assertIn(partner,self.page.evaluate('state.builderBlocks[0].text'))
            self.assertEqual(body.locator('a').get_attribute('data-seo-cloaked-href'),partner)
        unsafe=self.page.evaluate('''() => safeClipboardHtml(realFrameDocument(),
            '<a href="/safe/" data-seo-cloaked-href="javascript:alert(1)">Safe</a>')''')
        self.assertIn('href="/safe/"',unsafe)
        self.assertNotIn('javascript',unsafe)
        self.assertFalse(self.errors)

    def test_empty_title_can_be_edited_and_text_right_dragged(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-preview-index]')")
        self.page.evaluate('''() => {
            state.builderBlocks = normalizeBuilderBlocks([{type:'text', title:'', text:'Editable text',
                width:'full', blockBorderColor:'none', blockBgColor:'none'}]);
            renderBuilder(); updatePreview();
        }''')
        frame = self.page.frame_locator('#realPageFrame')
        body = frame.locator('[data-block-field=text]')
        body.click()
        frame.locator('[data-edit-block-title]').click()
        title = frame.locator('[data-block-field=title]')
        title.press_sequentially('New heading')
        title.press('Tab')
        self.assertIn('New heading', self.page.evaluate('state.builderBlocks[0].title'))
        self.page.wait_for_timeout(300)
        body.scroll_into_view_if_needed()
        box = body.bounding_box()
        self.page.mouse.move(box['x']+box['width']/2, box['y']+box['height']/2)
        self.page.mouse.down(button='right')
        self.assertEqual(self.page.evaluate('state.frameDrag?.index'), 0,
            self.page.evaluate('({resize:state.blockResize,panel:!!realFrameDocument().querySelector("#blockBorderPanel")})'))
        self.page.mouse.move(box['x']+box['width']/2+40, box['y']+box['height']/2+30, steps=5)
        self.page.mouse.up(button='right')
        self.assertGreater(self.page.evaluate('state.builderBlocks[0].offsetY || 0'), 0)
        self.assertFalse(self.errors)

    def test_first_image_ignores_deleted_spacer_position(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-preview-index]')")
        result = self.page.evaluate('''() => {
            state.builderBlocks = normalizeBuilderBlocks([{type:'spacer',width:'full',
                offsetX:623,offsetY:-366,pixelHeight:310,pixelWidth:619}]);
            state.selectedBlockIndex = 0; state.insertPoint = null;
            renderBuilder(); updatePreview();
            return imageInsertPointNearSelection();
        }''')
        self.assertEqual(result['x'], 0, result)
        self.assertFalse(self.errors)

    def test_website_save_preserves_heading_geometry_and_scroll(self):
        path = 'content/services/website-creation/index.ru.md'
        front, body, _ = server.read_markdown(TEST_ROOT/path)
        blocks = json.loads(front['builderJson'])
        text_block = next(b for b in blocks if b['type']=='text')
        text_block['text'] = '### Visible heading\n\nFirst paragraph.\n\nSecond paragraph.'
        text_block['offsetY'] = 32
        text_block['pixelHeight'] = 420
        front['builderJson'] = json.dumps(blocks)
        server.atomic_write_markdown(TEST_ROOT/path,server.dump_front_matter(front,body))
        self.page.evaluate('p=>openPage(p)',path)
        self.page.wait_for_function('!state.pageLoading && !!realFrameDocument()?.querySelector("[data-block-field=text] h3")')
        self.page.wait_for_timeout(400)
        measure = '''() => [...realFrameDocument().querySelectorAll('[data-preview-index]')].map(el=>{
            const r=el.getBoundingClientRect();return [r.x,r.y+realFrameScrollY(),r.width,r.height];})'''
        self.page.evaluate('window.scrollTo(0,200)')
        scroll = self.page.evaluate('window.scrollY')
        before = self.page.evaluate(measure)
        for _ in range(3):
            with self.page.expect_response(lambda r:'/api/page/save' in r.url):
                self.page.locator('#adminSaveBtn').click()
            self.page.wait_for_function('!state.savingPage && !state.pageLoading')
            self.page.wait_for_timeout(450)
            after = self.page.evaluate(measure)
            self.assertEqual(len(before),len(after))
            for a,b in zip(before,after):
                for x,y in zip(a,b): self.assertAlmostEqual(x,y,delta=2,msg=(before,after))
            self.assertEqual(self.page.frame_locator('#realPageFrame').locator('[data-block-field=text] h3').count(),1)
            self.assertAlmostEqual(self.page.evaluate('window.scrollY'),scroll,delta=2)
        self.assertFalse(self.errors)

    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={"width": 1600, "height": 1000})
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.route("**/api/server/pause", lambda route: route.fulfill(json={"ok": True, "pause": {"configured": False}}))
        self.page.route("**/api/deploy/status", lambda route: route.fulfill(json={"ok": True, "deploy": {}}))
        self.page.route("**/*", self.local_only)
        self.page.goto(BASE)
        self.page.wait_for_function("state.pages.length > 0")
        self.a = "content/services/obratnye-ssylki/index.ru.md"
        self.b = "content/services/backlinks/index.md"
        self.page.evaluate("path => openPage(path)", self.a)

    def local_only(self, route):
        if route.request.url.startswith((BASE, "http://127.0.0.1:1314")):
            route.fallback()
        else:
            route.abort()

    def tearDown(self):
        self.page.close()

    def test_feed_image_save_does_not_replace_seo_description_with_article(self):
        self.page.wait_for_function("realFrameDocument()?.body?.dataset.adminFrameWired === '1'")
        result=self.page.evaluate("""() => {
            const doc=realFrameDocument(), lookup=newsPageForArticle;
            const record={path:'content/audit.md',title:'Title',description:'Short SEO summary'};
            state.activePage={key:'home'}; state.pendingNewsPatches={};
            doc.body.innerHTML='<div class="js-news-strip-single"><article data-news-url="/audit/"><h2 data-news-field="title">Title</h2><div data-news-field="description"><p>Full article</p><p>More text</p></div></article></div>';
            newsPageForArticle=()=>record;
            try {
                wireHomeNewsFeed(doc);
                mergePendingNewsPatch(record.path,{image:'/new.webp'});
                const unchanged=syncHomeNewsEditablesFromFrame();
                const imageOnly={...state.pendingNewsPatches[record.path]};
                const field=doc.querySelector('[data-news-field=description]');
                field.textContent='Edited summary'; field.dataset.newsDirty='1';
                const edited=syncHomeNewsEditablesFromFrame();
                const repeat=syncHomeNewsEditablesFromFrame();
                return {unchanged,imageOnly,edited,repeat,description:state.pendingNewsPatches[record.path].description};
            } finally {newsPageForArticle=lookup;}
        }""")
        self.assertEqual(result,{'unchanged':0,'imageOnly':{'image':'/new.webp'},'edited':1,'repeat':0,'description':'Edited summary'})

    def test_text_width_preset_returns_only_selected_block_to_flow(self):
        self.page.wait_for_function("realFrameDocument()?.body?.dataset.adminFrameWired === '1'")
        self.page.evaluate("""() => {
            state.builderBlocks=normalizeBuilderBlocks([
                {type:'text',text:'Metric',fontFamily:'local',pixelWidth:411,pixelHeight:120,offsetX:435,offsetY:-115},
                {type:'text',text:'Unchanged',offsetX:20,offsetY:12}
            ]);
            state.selectedBlockIndex=0;
            renderBuilder();applyDraftToRealFrame();renderButtonLinkPanel();
        }""")
        before=self.page.evaluate('compactBuilderBlockForSave(state.builderBlocks[1])')
        self.page.frame_locator('#realPageFrame').locator('[data-block-width-preset]').select_option('third')
        result=self.page.evaluate('state.builderBlocks.map(compactBuilderBlockForSave)')
        self.assertEqual(result[0]['width'],'third')
        self.assertEqual(result[0]['text'],'Metric')
        self.assertEqual(result[0]['fontFamily'],'local')
        self.assertTrue(all(k not in result[0] for k in ('pixelWidth','pixelHeight','offsetX','offsetY')))
        self.assertEqual(result[1],before)
        self.assertFalse(self.errors)

    def test_button_new_tab_is_opt_in_and_survives_save_compaction(self):
        self.page.wait_for_function("realFrameDocument()?.body?.dataset.adminFrameWired === '1'")
        self.page.evaluate("""() => {
            state.builderBlocks = normalizeBuilderBlocks([
                {type:'buttons', buttons:[{label:'External profile',url:'https://example.com/profile'}]},
                {type:'buttons', buttons:[{label:'Internal',url:'/ru/about/'}]}
            ]);
            state.selectedBlockIndex=0;
            renderBuilder(); applyDraftToRealFrame();
            selectPreviewButton(realFrameDocument().querySelector('[data-preview-index="0"] [data-button-field="label"]'));
        }""")
        frame=self.page.frame_locator('#realPageFrame')
        toggle=frame.locator('#buttonPanelNewTab')
        self.assertFalse(toggle.is_checked())
        toggle.check()
        nofollow=frame.locator('#buttonPanelNofollow')
        self.assertFalse(nofollow.is_checked())
        nofollow.check()
        result=self.page.evaluate("""() => {
            syncButtonPanelFromDom(); syncBuilderFromDom();
            return normalizeBuilderBlocks(state.builderBlocks).map(compactBuilderBlockForSave);
        }""")
        self.assertTrue(result[0]['buttonNewTab'])
        self.assertTrue(result[0]['buttonNofollow'])
        self.assertNotIn('buttonNofollow',result[1])
        self.assertNotIn('buttonNewTab',result[1])
        self.page.evaluate("blocks=>{state.builderBlocks=normalizeBuilderBlocks(blocks);renderBuilder();applyDraftToRealFrame();selectPreviewButton(realFrameDocument().querySelector('[data-preview-index=\"0\"] [data-button-field=\"label\"]'))}",result)
        self.assertTrue(toggle.is_checked())
        self.assertTrue(nofollow.is_checked())
        nofollow.uncheck()
        self.assertNotIn('buttonNofollow',self.page.evaluate("() => {syncButtonPanelFromDom();return compactBuilderBlockForSave(state.builderBlocks[0])}"))
        toggle.uncheck()
        self.assertNotIn('buttonNewTab',self.page.evaluate("() => {syncButtonPanelFromDom();return compactBuilderBlockForSave(state.builderBlocks[0])}"))
        self.assertFalse(self.errors)

    def test_visible_page_cover_picker_changes_only_cover(self):
        self.page.wait_for_function("realFrameDocument()?.body?.dataset.adminFrameWired === '1'")
        before=self.page.evaluate("({description:state.front.description,feed:state.front.showOnHome,images:state.builderBlocks.map(b=>b.image||'')})")
        self.page.evaluate("state.assets=[{url:'/uploads/cover-check.webp',path:'static/uploads/cover-check.webp',name:'cover-check',used:true,usageKnown:true}]")
        self.page.locator('.more-blocks > summary').click()
        self.page.locator('#pageCoverPickBtn').click()
        self.page.locator('.asset-picker-card').click()
        result=self.page.evaluate("({image:state.front.image,images:state.front.images,description:state.front.description,feed:state.front.showOnHome,blocks:state.builderBlocks.map(b=>b.image||''),dirty:state.dirty})")
        self.assertEqual(result['image'],'/uploads/cover-check.webp')
        self.assertEqual(result['images'],['/uploads/cover-check.webp'])
        self.assertEqual(result['description'],before['description'])
        self.assertEqual(result.get('feed'),before.get('feed'))
        self.assertEqual(result['blocks'],before['images'])
        self.assertTrue(result['dirty'])
        self.assertFalse(self.errors)

    def test_media_variants_toggle_preserves_usage_protection(self):
        self.page.evaluate("""() => {
            state.assets = [
                {path:'static/uploads/old-q40-123.webp',url:'/uploads/old-q40-123.webp',name:'old',compressorVariant:true,used:false,deletable:true},
                {path:'static/uploads/used-q40-123.webp',url:'/uploads/used-q40-123.webp',name:'used',compressorVariant:true,used:true,deletable:false}
            ];
            renderAssets();
        }""")
        self.assertEqual(self.page.locator('#assetGrid .asset-card').count(), 1)
        self.page.locator('#showCompressedAssets').evaluate('el=>el.checked=true')
        self.page.locator('#showCompressedAssets').dispatch_event('change')
        self.assertEqual(self.page.locator('#assetGrid .asset-card').count(), 2)
        self.assertEqual(self.page.locator('#assetGrid .asset-delete').count(), 1)
        self.assertEqual(self.page.locator('#assetGrid .is-used .asset-delete').count(), 0)
        self.page.locator('#showCompressedAssets').evaluate('el=>el.checked=false')
        self.page.locator('#showCompressedAssets').dispatch_event('change')
        self.assertEqual(self.page.locator('#assetGrid .asset-card').count(), 1)
        self.assertFalse(self.errors)

    def test_backspace_unlists_middle_item_without_losing_text(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        self.page.evaluate("""() => {
            const doc=realFrameDocument(), el=doc.querySelector('[data-block-field=text]');
            el.innerHTML='<ul><li>First</li><li><strong>Second</strong> <a href="/go/vdsina/">VPS</a></li><li>Third</li></ul>';
            syncPreviewEditable(el); el.focus();
            const range=doc.createRange(); range.setStart(el.querySelectorAll('li')[1].querySelector('strong').firstChild,0); range.collapse(true);
            doc.getSelection().removeAllRanges(); doc.getSelection().addRange(range);
        }""")
        self.page.keyboard.press('Backspace')
        result=self.page.evaluate("""() => {
            const el=realFrameDocument().querySelector('[data-block-field=text]');
            const index=Number(el.closest('[data-preview-index]').dataset.previewIndex);
            const saved=state.builderBlocks[index].text;
            const restored=document.createElement('div'); restored.innerHTML=markdownToHtml(saved);
            return {html:el.innerHTML,saved,items:[...restored.querySelectorAll('li')].map(x=>x.textContent),
                paragraphs:[...restored.querySelectorAll('p')].map(x=>x.textContent),
                href:restored.querySelector('a')?.getAttribute('href')};
        }""")
        self.assertEqual(result['items'], ['First', 'Third'], result)
        self.assertIn('Second VPS',result['paragraphs'],result)
        self.assertEqual(result['href'],'/go/vdsina/')
        self.assertFalse(self.errors)

    def test_retarget_selected_rich_link_without_nested_anchors(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        results = self.page.evaluate("""() => {
            const doc = realFrameDocument();
            const editable = doc.querySelector('[data-block-field=text]');
            editable.innerHTML = 'Before <a href="/old/"><strong>VPS</strong> server</a> after';
            syncPreviewEditable(editable);
            const results = [];
            for (const url of ['/go/vdsina/', '/another/?q=1#details', '/go/vdsina/']) {
                const originalLink = editable.querySelector('a');
                const range = doc.createRange(); range.selectNodeContents(originalLink);
                doc.getSelection().removeAllRanges(); doc.getSelection().addRange(range);
                const selection = captureTextSelection(doc);
                const ok = applyTextSelectionDomLink(url, {selection});
                results.push({ok, links:editable.querySelectorAll('a').length,
                    nested:editable.querySelectorAll('a a').length, text:editable.textContent,
                    bold:editable.querySelectorAll('a strong').length,
                    same:editable.querySelector('a') === originalLink,
                    href:editable.querySelector('a')?.getAttribute('href')});
            }
            return results;
        }""")
        for result, url in zip(results, ['/go/vdsina/', '/another/?q=1#details', '/go/vdsina/']):
            self.assertEqual(result, {'ok': True, 'links': 1, 'nested': 0,
                'text': 'Before VPS server after', 'bold': 1, 'same': True, 'href': url})
        self.assertFalse(self.errors)

    def test_link_color_toolbar_save_reload_and_clear(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        self.page.evaluate('''() => {
            const el=realFrameDocument().querySelector('[data-block-field=text]');
            el.innerHTML='<p><a href="https://t.me/Seoimpuls">Telegram</a> or <a href="https://wa.me/5491132804658"><strong><span style="font-size:20px">WhatsApp</span></strong></a> after</p>';
            syncPreviewEditable(el);
        }''')
        def select_link():
            self.page.evaluate('''() => {
                const doc=realFrameDocument(),a=doc.querySelector('[data-block-field=text] a[href*="wa.me"]');
                a.closest('[contenteditable=true]').focus();
                const range=doc.createRange();range.selectNodeContents(a);
                doc.getSelection().removeAllRanges();doc.getSelection().addRange(range);
            }''')
            self.page.frame_locator('#realPageFrame').locator('[data-text-toolbar-color]').wait_for(state='visible')
        for color, expected in [('#00f56a','rgb(0, 245, 106)'),('#ff3366','rgb(255, 51, 102)'),('#00f56a','rgb(0, 245, 106)')]*3:
            select_link()
            self.assertEqual(self.page.evaluate('''() => {
                const doc=realFrameDocument(),s=activeTextToolbarSelection(),el=editableForTextSelection(s,doc),r=rangeFromFrozenTextSelection(s,el);
                return r.toString();
            }'''),'WhatsApp')
            self.page.frame_locator('#realPageFrame').locator('[data-text-toolbar-color]').fill(color)
            diagnostic = self.page.evaluate("({html:realFrameDocument().querySelector('[data-block-field=text]').innerHTML,text:state.builderBlocks[0].text})")
            with self.page.expect_response(lambda r:'/api/page/save' in r.url) as saved:
                self.page.locator('#adminSaveBtn').click()
            self.assertTrue(saved.value.json()['ok'])
            self.page.wait_for_function('!state.savingPage && !state.pageLoading')
            result=self.page.evaluate('''() => {
                const doc=realFrameDocument(),a=doc.querySelector('[data-block-field=text] a[href*="wa.me"]');
                return {text:a.textContent,color:doc.defaultView.getComputedStyle(a).color,
                    telegram:doc.defaultView.getComputedStyle(doc.querySelector('[data-block-field=text] a[href*="t.me"]')).color,
                    nested:a.querySelectorAll('a').length,bold:!!a.closest('strong')||!!a.querySelector('strong')};
            }''')
            self.assertEqual(result,{'text':'WhatsApp','color':expected,'telegram':'rgb(125, 211, 252)','nested':0,'bold':True}, diagnostic)
            self.assertEqual(self.page.frame_locator('#realPageFrame').locator('[data-block-field=text]').first.locator('a[href*="wa.me"]').count(),1)
        select_link()
        self.page.frame_locator('#realPageFrame').locator('[data-text-toolbar-clear-color]').click()
        with self.page.expect_response(lambda r:'/api/page/save' in r.url) as saved:
            self.page.locator('#adminSaveBtn').click()
        self.assertTrue(saved.value.json()['ok'])
        self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        self.assertEqual(self.page.evaluate("realFrameDocument().defaultView.getComputedStyle(realFrameDocument().querySelector('[data-block-field=text] a[href*=\"wa.me\"]')).color"),'rgb(125, 211, 252)')
        self.assertFalse(self.errors)

    def test_service_card_add_edit_shared_image_save_reload(self):
        for lang, suffix in [('ru', '.ru'), ('en', ''), ('es', '.es')]:
            path = f'content/services/_index{suffix}.md'
            self.page.evaluate('path => openPage(path)', path)
            self.page.wait_for_function('!state.pageLoading && !!realFrameDocument()?.querySelector(".admin-services-card-add")')
            frame = self.page.frame_locator('#realPageFrame')
            count = frame.locator('.services-hub-card:visible').count()
            existing_ids = self.page.evaluate('state.builderBlocks.map(b=>b.serviceCardId).filter(Boolean)')
            source = frame.locator('.services-hub-card img').first.get_attribute('src')
            frame.locator('.admin-services-card-add').click()
            self.page.locator('#serviceCardLabel').fill('Cancelled')
            self.page.locator('#serviceCardCancel').click()
            self.assertEqual(frame.locator('.services-hub-card:visible').count(), count)
            for index in range(2):
                frame.locator('.admin-services-card-add').click()
                self.page.locator('#serviceCardLabel').fill(f'Unknown service {index}')
                self.page.locator('#serviceCardUrl').fill(f'/{lang}/new-service-{index}/')
                self.page.locator('#serviceCardImage').fill(source)
                self.page.locator('#serviceCardOrder').fill(str(40 + index * 10))
                self.page.locator('#serviceCardApply').click()
                self.page.locator('#serviceCardDialog').wait_for(state='hidden')
            self.assertEqual(frame.locator('.services-hub-card:visible').count(), count + 2)
            for cycle in range(3):
                card = frame.locator(f'[data-services-card-url="/{lang}/new-service-1/"]')
                card.locator('.admin-services-card-edit').click()
                self.page.locator('#serviceCardLabel').fill(f'Edited {cycle}')
                self.page.locator('#serviceCardApply').click()
                with self.page.expect_response(lambda r:'/api/page/save' in r.url) as saved:
                    self.page.locator('#adminSaveBtn').click()
                self.assertTrue(saved.value.json()['ok'])
                self.page.wait_for_function('!state.savingPage && !state.pageLoading')
                self.assertEqual(frame.locator('.services-hub-card:visible').count(), count + 2)
                self.assertEqual(card.locator('.services-hub-card__label').inner_text(), f'Edited {cycle}')
                self.assertEqual(card.locator('img').get_attribute('src'), source)
            current, _, _ = server.read_markdown(TEST_ROOT/path)
            blocks = json.loads(current['builderJson'])
            managed = [b for b in blocks if b.get('serviceCardId') and b['serviceCardId'] not in existing_ids]
            self.assertEqual(len(managed), 4)
            self.assertEqual(len({b['serviceCardId'] for b in managed}), 2)
            self.assertEqual(sorted(b['type'] for b in managed), ['buttons', 'buttons', 'image', 'image'])
            card.locator('.admin-services-card-edit').click()
            self.page.locator('#serviceCardUrl').fill('https://')
            self.page.locator('#serviceCardApply').click()
            self.assertTrue(self.page.locator('#serviceCardDialog').is_visible())
            self.assertIn('корректные ссылки', self.page.locator('#serviceCardStatus').inner_text())
            self.page.locator('#serviceCardUrl').fill(f'/{lang}/new-service-0/')
            self.page.locator('#serviceCardApply').click()
            self.assertTrue(self.page.locator('#serviceCardDialog').is_visible())
            self.assertIn('уже существует', self.page.locator('#serviceCardStatus').inner_text())
            self.page.locator('#serviceCardCancel').click()
            self.page.once('dialog', lambda d: d.accept())
            card.locator('.admin-services-card-delete').click()
            self.assertEqual(frame.locator('.services-hub-card:visible').count(), count + 1)
            self.assertEqual(frame.locator(f'[data-services-card-url="/{lang}/new-service-0/"]').count(), 1)
            self.page.locator('#visualUndoBtn').click()
            self.assertEqual(frame.locator('.services-hub-card:visible').count(), count + 2)
            # Leave each temporary hub clean before opening another language.
            with self.page.expect_response(lambda r:'/api/page/save' in r.url):
                self.page.locator('#adminSaveBtn').click()
            self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        self.assertFalse(self.errors)

    def test_service_card_closed_dialog_rejects_late_asset(self):
        self.page.evaluate("openPage('content/services/_index.ru.md')")
        self.page.wait_for_function('!state.pageLoading && !!realFrameDocument()?.querySelector(".admin-services-card-add")')
        frame = self.page.frame_locator('#realPageFrame')
        before = self.page.evaluate('JSON.stringify(state.builderBlocks)')
        frame.locator('.admin-services-card-add').click()
        self.page.evaluate('window.oldServiceTarget = {draft:serviceCardDraft}')
        self.page.locator('#serviceCardCancel').click()
        frame.locator('.admin-services-card-add').click()
        self.page.evaluate("applyServiceCardAsset(window.oldServiceTarget, '/uploads/stale.webp')")
        self.assertEqual(self.page.locator('#serviceCardImage').input_value(), '')
        self.assertEqual(self.page.evaluate('JSON.stringify(state.builderBlocks)'), before)
        self.page.locator('#serviceCardCancel').click()
        self.assertFalse(self.errors)

    def test_created_page_reloads_initial_missing_preview_after_build(self):
        published = {'ready': False, 'missing': 0}
        html = self.page.request.get(BASE+'/site/uslugi-linkbildinga/obratnye-ssylki/').text()
        def preview(route):
            if published['ready']:
                route.fulfill(content_type='text/html', body=html)
            else:
                published['missing'] += 1
                route.fulfill(status=404, content_type='text/plain', body='Site page not found. Start Hugo preview or build site.')
        def build(route):
            self.page.wait_for_timeout(150)
            published['ready'] = True
            route.fulfill(json={'ok':True})
        self.page.route('**/site/uslugi-linkbildinga/new-preview-fixture/**', preview)
        self.page.route('**/api/build', build)
        self.page.locator('#newPageBtn').click()
        self.page.locator('#newTitle').fill('New preview fixture')
        self.page.locator('#newSlug').fill('new-preview-fixture')
        self.page.locator('#newSectionSelect').select_option('services')
        self.page.locator('#newLanguage').select_option('ru')
        self.page.locator('#newPageForm button.btn.primary').click()
        self.page.wait_for_function('''!state.creatingPage &&
            realFrameDocument()?.body?.dataset.adminFrameWired === '1' &&
            realFrameDocument()?.querySelector('[data-page-field=title]')?.textContent === 'New preview fixture' ''')
        self.assertGreater(published['missing'], 0)
        self.assertFalse(self.errors)

    def test_service_card_delete_cancel_undo_and_save(self):
        from bs4 import BeautifulSoup
        path = 'content/services/_index.ru.md'
        front, body, _ = server.read_markdown(TEST_ROOT/path)
        original = json.loads(front['builderJson'])
        fixtures = [(40, 'XRumer training', '/uslugi-linkbildinga/hrumer-obuchenie/'),
                    (50, 'GSA training', '/uslugi-linkbildinga/obuchenie-gsa/')]
        for rank, label, url in fixtures:
            if not any(b.get('type') == 'buttons' and any(x.get('url') == url for x in b.get('buttons', [])) for b in original):
                original.extend([{'type':'image', 'image':'/uploads/service-card-'+('xrumer' if rank==40 else 'gsa')+'-20260816.webp', 'alt':label, 'imageLink':url},
                                 {'type':'buttons','buttons':[{'label':label,'url':'/'}]}])
        front['builderJson'] = json.dumps(original)
        server.atomic_write_markdown(TEST_ROOT/path, server.dump_front_matter(front, body))
        def preview_fixture(route):
            response = route.fetch()
            soup = BeautifulSoup(response.text(), 'html.parser')
            for rank, label, url in fixtures:
                if soup.select_one(f'[data-services-card-rank="{rank}"]'):
                    continue
                card = soup.new_tag('a', attrs={'class':'services-hub-card','href':url,'data-services-card-url':url,'data-services-card-rank':str(rank)})
                image = next(b['image'] for b in original if b.get('type')=='image' and b.get('imageLink')==url)
                card.append(soup.new_tag('img', attrs={'src':image, 'width':'300','height':'160'}))
                heading = soup.new_tag('h2', attrs={'class':'services-hub-card__label'})
                heading.string = label
                card.append(heading)
                soup.select_one('.services-hub').append(card)
            route.fulfill(response=response, body=str(soup))
        self.page.route('**/site/uslugi-linkbildinga/**', preview_fixture)
        self.page.evaluate('path => openPage(path)', path)
        self.page.wait_for_function("realFrameDocument()?.location.pathname === '/site/uslugi-linkbildinga/' && realFrameDocument()?.querySelector('.admin-services-card-delete')")
        frame = self.page.frame_locator('#realPageFrame')
        card = frame.locator('[data-services-card-rank="40"]')
        original_count = frame.locator('.services-hub-card:visible').count()
        snapshot = 'JSON.stringify(state.builderBlocks.filter(b=>b.type!=="text").map(({adminId,...block})=>block))'
        before = self.page.evaluate(snapshot)
        dialogs = []
        self.page.once('dialog', lambda d: (dialogs.append(d.message), d.dismiss()))
        card.locator('.admin-services-card-delete').click()
        self.assertEqual(len(dialogs), 1)
        self.assertEqual(self.page.evaluate(snapshot), before)
        self.page.wait_for_timeout(300)
        self.page.once('dialog', lambda d: (dialogs.append(d.message), d.accept()))
        card.locator('.admin-services-card-delete').click()
        self.page.wait_for_timeout(300)
        self.assertEqual(len(dialogs), 2)
        self.assertFalse(self.errors)
        self.assertFalse(self.page.evaluate('state.builderBlocks.some(b => builderBlockServiceRank(b) === 40)'), self.page.evaluate('({dirty:state.dirty, clean:state.cleanPreview})'))
        card.wait_for(state='hidden')
        self.assertFalse(card.is_visible())
        self.assertEqual(frame.locator('.services-hub-card:visible').count(), original_count - 1)
        self.page.locator('#visualUndoBtn').click()
        card.wait_for(state='visible')
        self.assertTrue(card.is_visible())
        self.assertEqual(self.page.evaluate(snapshot), before)
        for rank in (40, 50):
            self.page.wait_for_timeout(350)
            self.page.once('dialog', lambda d: d.accept())
            frame.locator(f'[data-services-card-rank="{rank}"] .admin-services-card-delete').click()
            frame.locator(f'[data-services-card-rank="{rank}"]').wait_for(state='hidden')
        self.assertEqual(frame.locator('.services-hub-card:visible').count(), original_count - 2)
        with self.page.expect_response(lambda r: '/api/page/save' in r.url) as saved:
            self.page.locator('#adminSaveBtn').click()
        self.assertTrue(saved.value.json()['ok'])
        self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        current, current_body, _ = server.read_markdown(TEST_ROOT/path)
        blocks = json.loads(current['builderJson'])
        self.assertEqual(current_body, body)
        def text_content(items):
            return self.page.evaluate('''items => items.filter(b=>b.type==='text').map(b=>{
                const el=document.createElement('div'); el.innerHTML=markdownToHtml(b.text);
                return {text:el.textContent,links:[...el.querySelectorAll('a')].map(a=>[a.textContent,a.getAttribute('href')])};
            })''', items)
        self.assertEqual(text_content(blocks), text_content(original))
        self.assertFalse(self.page.evaluate('state.builderBlocks.some(b => [40,50].includes(builderBlockServiceRank(b)))'))
        self.assertEqual(frame.locator('.services-hub-card:visible').count(), original_count - 2)
        self.assertFalse(self.errors)

    def test_save_never_merges_independent_image_and_text(self):
        result=self.page.evaluate("""() => {
            let blocks=[{type:'image',image:'/uploads/test.webp',pixelWidth:600,pixelHeight:350},
                {type:'text',text:'Independent',pixelWidth:600,pixelHeight:350,offsetX:620,offsetY:-368}];
            for(let i=0;i<8;i++) blocks=builderBlocksForSave(blocks);
            return blocks.map(b=>({type:b.type,text:b.text||'',image:b.image||'',x:b.offsetX||0,y:b.offsetY||0}));
        }""")
        self.assertEqual(result,[{'type':'image','text':'','image':'/uploads/test.webp','x':0,'y':0},
            {'type':'text','text':'Independent','image':'','x':620,'y':-368}])

    def test_adjacent_bold_colored_runs_share_delimiters(self):
        result=self.page.evaluate("""() => {
            let text='**<span style="font-size:22px">Package </span>****<span style="font-size:22px;color:#12d933">290$</span>**';
            for(let i=0;i<8;i++) text=normalizeBuilderTextMarkup(text);
            const el=document.createElement('div');el.innerHTML=markdownToHtml(text);
            return {text:el.textContent,delimiters:(text.match(/\\*\\*/g)||[]).length,
                colored:el.querySelector('span[style*="color"]')?.textContent};
        }""")
        self.assertEqual(result,{'text':'Package 290$','delimiters':2,'colored':'290$'})

    def test_separate_composite_and_drag_text_independently(self):
        path='content/services/tier-1-2-3/index.md'
        front,body,_=server.read_markdown(TEST_ROOT/path)
        front['builderJson']=json.dumps([
            {'type':'split','title':'Independent text','text':'Intro paragraph.\n\n- First item\n\n- Second item',
             'image':'/uploads/service-card-tier-1-2-3.webp','imageSide':'left','imagePixelWidth':647,
             'blockBorderColor':'none','blockBgColor':'none','fontFamily':'server'},
            {'type':'text','text':'Following content','blockBorderColor':'none','blockBgColor':'none'}])
        server.atomic_write_markdown(TEST_ROOT/path,server.dump_front_matter(front,body))
        self.page.evaluate('path=>openPage(path)',path)
        self.page.wait_for_function("realFrameDocument()?.location.pathname==='/site/link-building-services/tier-1-2-3/' && realFrameDocument()?.body?.dataset.adminFrameWired==='1'")
        self.page.wait_for_function("[...realFrameDocument().querySelectorAll('.seo-builder img')].every(x=>x.complete && x.naturalWidth)")
        measure="""() => {
            const doc=realFrameDocument();
            const box=el=>{const r=el.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
            return {text:[...doc.querySelectorAll('.seo-builder-text')].map(box),image:box(doc.querySelector('.seo-builder img')),
                copy:state.builderBlocks.map(b=>[b.title||'',b.text||'']).filter(x=>x[0]||x[1])};
        }"""
        before=self.page.evaluate(measure)
        self.page.locator('#separateBuilderBlocksBtn').evaluate('el=>el.closest("details").open=true')
        self.page.locator('#separateBuilderBlocksBtn').click()
        self.page.wait_for_timeout(400)
        after=self.page.evaluate(measure)
        self.assertEqual(before['copy'],after['copy'])
        for a,b in zip(before['text']+[before['image']],after['text']+[after['image']]):
            for x,y in zip(a,b): self.assertAlmostEqual(x,y,delta=2)
        self.assertEqual(self.page.evaluate('state.builderBlocks.map(b=>b.type)'),['image','text','text'])
        self.page.locator('#separateBuilderBlocksBtn').evaluate('el=>el.closest("details").open=false')
        handle=self.page.frame_locator('#realPageFrame').locator('[data-preview-index="1"] [data-block-move]')
        handle.scroll_into_view_if_needed()
        handle.hover()
        rect=handle.bounding_box()
        self.page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
        self.page.mouse.down()
        self.assertEqual(self.page.evaluate('state.frameDrag?.index'),1,self.page.evaluate('({resize:state.blockResize,drag:state.frameDrag})'))
        self.page.mouse.move(rect['x']+rect['width']/2-24,rect['y']+rect['height']/2+35,steps=8)
        self.page.mouse.up()
        self.page.wait_for_timeout(350)
        dragged=self.page.evaluate(measure)
        self.assertLess(dragged['text'][0][0]-after['text'][0][0],-10)
        self.assertGreater(dragged['text'][0][1]-after['text'][0][1],30)
        self.assertEqual(dragged['image'],after['image'])
        with self.page.expect_response(lambda r:'/api/page/save' in r.url) as saved:
            self.page.locator('#adminSaveBtn').click()
        self.assertTrue(saved.value.json()['ok'])
        self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        self.assertEqual(self.page.evaluate('state.builderBlocks.map(b=>b.type)'),['image','text','text'])
        self.assertFalse(self.errors)

    def test_list_keyboard_undo_and_normal_midword_backspace(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        for index in range(3):
            with self.subTest(index=index):
                self.page.evaluate("""index => {
                    const doc=realFrameDocument(), el=doc.querySelector('[data-block-field=text]');
                    el.innerHTML='<ul><li>First</li><li>Second</li><li>Third</li></ul>';
                    syncPreviewEditable(el); el.focus();
                    const range=doc.createRange(); range.setStart(el.querySelectorAll('li')[index].firstChild,0);range.collapse(true);
                    doc.getSelection().removeAllRanges();doc.getSelection().addRange(range);
                }""", index)
                self.page.keyboard.press('Backspace')
                self.assertEqual(self.page.frame_locator('#realPageFrame').locator('[data-block-field=text]').first.locator('li').count(),2)
                self.page.keyboard.press('Control+z')
                self.assertEqual(self.page.frame_locator('#realPageFrame').locator('[data-block-field=text]').first.locator('li').count(),3)
        self.page.keyboard.press('ArrowRight')
        self.page.keyboard.press('Backspace')
        result=self.page.evaluate("""() => [...realFrameDocument().querySelector('[data-block-field=text]').querySelectorAll('li')].map(x=>x.textContent)""")
        self.assertEqual(result,['First','Second','hird'])
        self.assertFalse(self.errors)

    def test_loose_lists_and_empty_titles_do_not_accumulate_layout(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        result=self.page.evaluate("""() => {
            const doc=realFrameDocument();
            const block={...defaultBuilderBlock('text'),title:'',text:'Intro\\n\\n- **First**\\n\\n- Second [VPS](/go/vdsina/)\\n\\nEnd',pixelHeight:0};
            state.builderBlocks=[block]; applyDraftToRealFrame();
            const el=doc.querySelector('[data-block-field=text]');
            const samples=[];
            for(let i=0;i<10;i++) {
                syncPreviewEditable(el);
                const saved=block.text;
                el.innerHTML=markdownToHtml(saved,block);
                samples.push({lists:el.querySelectorAll('ul').length,items:el.querySelectorAll('li').length,
                    paragraphs:el.querySelectorAll('li>p').length, height:el.getBoundingClientRect().height,
                    titleHeight:doc.querySelector('[data-block-field=title]').getBoundingClientRect().height,
                    source:saved});
            }
            return samples;
        }""")
        self.assertTrue(all(sample==result[0] for sample in result),result)
        self.assertEqual(result[0]['lists'],1)
        self.assertEqual(result[0]['items'],2)
        self.assertEqual(result[0]['paragraphs'],2)
        self.assertEqual(result[0]['titleHeight'],0)
        self.assertFalse(self.errors)

    def test_unlist_toolbar_preserves_styles_and_survives_save_reload(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        self.page.evaluate("""() => {
            const el=realFrameDocument().querySelector('[data-block-field=text]');
            el.innerHTML='<p>Intro</p><ul><li><strong>First</strong></li><li><span style="font-size:22px !important">Second <a href="/go/vdsina/">VPS</a></span></li></ul><p>End</p>';
            syncPreviewEditable(el);
        }""")
        editable=self.page.frame_locator('#realPageFrame').locator('[data-block-field=text]').first
        editable.click()
        editable.press('Control+a')
        self.page.frame_locator('#realPageFrame').locator('[data-text-toolbar-unlist]').click()
        result=self.page.evaluate("""() => {
            const el=realFrameDocument().querySelector('[data-block-field=text]');
            return {items:el.querySelectorAll('li').length, text:el.textContent,
                bold:el.querySelector('strong,b')?.textContent, size:el.querySelector('span')?.style.fontSize};
        }""")
        self.assertEqual(result,{'items':0,'text':'IntroFirstSecond VPSEnd','bold':'First','size':'22px'})
        with self.page.expect_response(lambda response: '/api/page/save' in response.url) as saved:
            self.page.locator('#adminSaveBtn').click()
        self.assertTrue(saved.value.json()['ok'])
        self.page.wait_for_function('!state.savingPage && !state.pageLoading')
        self.page.reload()
        self.page.wait_for_function('state.pages.length > 0')
        self.page.evaluate('path => openPage(path)',self.a)
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        result=self.page.evaluate("""() => {
            const el=realFrameDocument().querySelector('[data-block-field=text]');
            return {items:el.querySelectorAll('li').length, paragraphs:[...el.querySelectorAll('p')].map(x=>x.textContent),
                href:el.querySelector('a')?.getAttribute('href')};
        }""")
        self.assertEqual(result, {'items':0,'paragraphs':['Intro','First','Second VPS','End'],'href':'/go/vdsina/'})
        self.assertFalse(self.errors)

    def test_multiblock_font_changes_preserve_lists_and_do_not_accumulate(self):
        self.page.wait_for_function("realFrameDocument()?.querySelector('[data-block-field=text]')?.isContentEditable")
        result = self.page.evaluate("""() => {
            const doc = realFrameDocument(), editable = doc.querySelector('[data-block-field=text]');
            editable.innerHTML = '<p>Intro text</p><ul><li><strong>First:</strong> item</li><li>Second <a href="/go/vdsina/">VPS</a></li></ul><p>Closing text</p>';
            syncPreviewEditable(editable);
            const text = editable.textContent;
            const structure = [...editable.querySelectorAll('p,ul,li,strong,a')];
            for (let i=0;i<6;i++) {
                for (const options of [{size: i % 2 ? 22 : 14}, {fontFamily:'server'}]) {
                    const range=doc.createRange();range.selectNodeContents(editable);
                    doc.getSelection().removeAllRanges();doc.getSelection().addRange(range);
                    if (!applyTextSelectionDomStyle({...options,selection:captureTextSelection(doc)})) throw Error('Style failed');
                }
            }
            const spans = [...editable.querySelectorAll('span')];
            const roundtrip = doc.createElement('div');
            const index = Number(editable.closest('[data-preview-index]').dataset.previewIndex);
            roundtrip.innerHTML = markdownToHtml(state.builderBlocks[index].text, state.builderBlocks[index]);
            return {sameText:text===editable.textContent, intact:structure.every(el=>editable.contains(el)),
                lists:editable.querySelectorAll('li').length, empty: [...editable.querySelectorAll('li')].some(el=>!el.textContent.trim()),
                spans:spans.length, nested:editable.querySelectorAll('span span').length,
                fonts:spans.map(el=>[doc.defaultView.getComputedStyle(el).fontSize,doc.defaultView.getComputedStyle(el).fontFamily]),
                href:editable.querySelector('a').getAttribute('href'), roundtripLists:roundtrip.querySelectorAll('li').length,
                roundtripLinks:[...roundtrip.querySelectorAll('a')].map(el=>[el.getAttribute('href'),el.textContent])};
        }""")
        self.assertTrue(result['sameText'] and result['intact'])
        self.assertEqual(result['lists'], 2)
        self.assertFalse(result['empty'])
        self.assertEqual(result['nested'], 0)
        self.assertEqual(result['spans'], 6)
        self.assertEqual(result['roundtripLists'], 2)
        self.assertEqual(result['href'], '/go/vdsina/')
        self.assertEqual(result['roundtripLinks'], [['/go/vdsina/', 'VPS']])
        self.assertTrue(all(size == '22px' and 'times new roman' in font.lower() for size,font in result['fonts']), result)
        self.assertFalse(self.errors)

    def test_latest_page_wins_reordered_responses(self):
        result = self.page.evaluate("""async ([a, b]) => {
            const original = api;
            api = async (path, options) => {
                const data = await original(path, options);
                if (path.startsWith('/api/page?') && decodeURIComponent(path).endsWith(a))
                    await new Promise(resolve => setTimeout(resolve, 250));
                return data;
            };
            try {
                await Promise.all([openPage(a), openPage(b)]);
                return {path: state.activePath, lang: document.querySelector('#fieldSection').value};
            } finally { api = original; }
        }""", [self.a, self.b])
        self.assertEqual(result["path"], self.b)

    def test_page_switch_uses_only_fast_catalog_and_one_builder_load(self):
        result = self.page.evaluate("""async ([a, b]) => {
            const original = api, originalLoad = loadBuilderFromFront;
            const calls = []; let loads = 0;
            api = async (path, options) => { calls.push(path); return original(path, options); };
            loadBuilderFromFront = (...args) => { loads++; return originalLoad(...args); };
            try {
                for (const path of [b, a, b, a, b, a]) await openPage(path);
                return {calls, loads, thumbnails: document.querySelectorAll('#assetGrid img').length,
                    assets: state.assets.length, loading: state.pageLoading};
            } finally { api = original; loadBuilderFromFront = originalLoad; }
        }""", [self.a, self.b])
        self.assertEqual(result["loads"], 6)
        self.assertEqual(result["thumbnails"], 0)
        self.assertGreater(result["assets"], 0)
        self.assertFalse(result["loading"])
        self.assertEqual([url for url in result["calls"] if url.startswith("/api/assets")],
                         ["/api/assets?usage=0"] * 6)

    def test_picker_checks_usage_once_and_media_refreshes_it(self):
        result = self.page.evaluate("""async () => {
            const original = api; const calls = [];
            api = async (path, options) => { calls.push(path); return original(path, options); };
            try {
                await openAssetPicker({kind: 'pageImage'});
                document.querySelector('#assetPickerDialog').close();
                await openAssetPicker({kind: 'pageImage'});
                document.querySelector('#assetPickerDialog').close();
                const pickerCalls = calls.slice();
                const hiddenThumbnails = document.querySelectorAll('#assetGrid img').length;
                document.body.dataset.view = 'media';
                await loadAssets({includeUsage: true});
                const images = [...document.querySelectorAll('#assetGrid img')];
                return {pickerCalls, calls, hiddenThumbnails, thumbnails: images.length,
                    lazy: images.every(img => img.loading === 'lazy'),
                    known: state.assets.every(asset => asset.usageKnown)};
            } finally { api = original; document.body.dataset.view = 'pages'; }
        }""")
        self.assertEqual(result["pickerCalls"], ["/api/assets"])
        self.assertEqual(result["calls"], ["/api/assets", "/api/assets"])
        self.assertEqual(result["hiddenThumbnails"], 0)
        self.assertGreater(result["thumbnails"], 0)
        self.assertLessEqual(result["thumbnails"], 240)
        self.assertTrue(result["lazy"] and result["known"])

    def test_late_asset_catalog_cannot_overwrite_newer_response_or_reset(self):
        result = self.page.evaluate("""async () => {
            const original = api; let release;
            api = async () => new Promise(resolve => { release = resolve; });
            try {
                const first = loadAssets({includeUsage: true});
                const finishFirst = release;
                const second = loadAssets();
                release({assets: [{url: '/new.webp'}]}); await second;
                finishFirst({assets: [{url: '/old.webp'}]}); await first;
                const afterNew = state.assets.map(a => a.url);
                const third = loadAssets();
                resetPageRuntimeState();
                release({assets: [{url: '/stale.webp'}]}); await third;
                return {afterNew, afterReset: state.assets.map(a => a.url)};
            } finally { api = original; }
        }""")
        self.assertEqual(result, {"afterNew": ["/new.webp"], "afterReset": ["/new.webp"]})

    def test_loading_feedback_releases_on_catalog_failure(self):
        result = self.page.evaluate("""async path => {
            const original = api; let release;
            api = async (url, options) => {
                if (url.startsWith('/api/page?')) await new Promise(resolve => { release = resolve; });
                if (url.startsWith('/api/assets')) throw new Error('Audit offline');
                return original(url, options);
            };
            try {
                const pending = openPage(path);
                const busy = !!document.querySelector('.page-open[aria-busy="true"]');
                release();
                try { await pending; } catch (_) {}
                return {busy, loading: state.pageLoading,
                    remaining: document.querySelectorAll('.page-open[aria-busy="true"]').length,
                    active: state.activePath};
            } finally { api = original; }
        }""", self.a)
        self.assertEqual(result, {"busy": True, "loading": False, "remaining": 0, "active": self.a})

    def test_open_preserves_history_only_when_requested(self):
        result = self.page.evaluate("""async path => {
            rememberBuilderState();
            const before = state.builderHistory.length;
            await openPage(path, {preserveBuilderHistory: true});
            const preserved = state.builderHistory.length;
            await openPage(path);
            return {before, preserved, cleared: state.builderHistory.length};
        }""", self.a)
        self.assertGreater(result["before"], 0)
        self.assertEqual(result["before"], result["preserved"])
        self.assertEqual(result["cleared"], 0)

    def test_header_navigation_on_fallback_port_all_languages(self):
        self.page.on("dialog", lambda dialog: dialog.accept())
        for source, target, url in [
            (self.a, "content/services/_index.ru.md", "/uslugi-linkbildinga/"),
            (self.b, "content/services/_index.md", "/link-building-services/"),
            ("content/services/backlinks/index.es.md", "content/services/_index.es.md", "/servicios-de-link-building/"),
        ]:
            self.page.evaluate("path => openPage(path, {discardDirty: true})", source)
            self.page.wait_for_function("""() => {
                const doc = realFrameDocument();
                const image = doc?.querySelector('.seo-builder img');
                return doc?.readyState === 'complete' && doc.body?.dataset.adminFrameWired === '1' &&
                    doc.location.pathname === '/site' + draftFrameSourceUrl() && image?.complete && image.naturalWidth > 0;
            }""")
            # Locator auto-scroll can put a scaled iframe underneath the sticky toolbar.
            # Click the visible header in screen coordinates, as a user would.
            self.page.evaluate("window.scrollTo(0, 0)")
            point = self.page.evaluate("""url => {
                const frame = document.querySelector('#realPageFrame');
                const outer = frame.getBoundingClientRect();
                const link = realFrameDocument().querySelector(`.custom-header__link[href*="${url}"]`);
                const rect = link.getBoundingClientRect();
                const scale = outer.width / frame.offsetWidth;
                const x = outer.left + (rect.x + rect.width / 2) * scale;
                const y = outer.top + (rect.y + rect.height / 2) * scale;
                return {x, y, visible: document.elementFromPoint(x, y) === frame};
            }""", url)
            self.assertTrue(point["visible"], point)
            self.page.mouse.click(point["x"], point["y"])
            try:
                self.page.wait_for_function("path => state.activePath === path && !state.pageLoading", arg=target, timeout=10000)
            except Exception as error:
                details = self.page.evaluate("""() => ({path: state.activePath, loading: state.pageLoading,
                    dirty: state.dirty, toast: document.querySelector('#toast').textContent,
                    frame: realFrameDocument()?.location.href})""")
                self.page.screenshot(path=str(ROOT / 'admin/test-artifacts/header-click-failure.png'))
                raise AssertionError({"source": source, "target": target, **details}) from error
            self.page.wait_for_function("url => realFrameDocument()?.location.pathname === '/site' + url && !!realFrameDocument().querySelector('.custom-header')", arg=url, timeout=10000)
            self.assertFalse(self.page.evaluate("isMissingSitePage(realFrameDocument())"))
        self.assertEqual(self.errors, [])

    def test_unknown_internal_link_cannot_navigate_frame(self):
        self.page.wait_for_function("realFrameDocument()?.body?.dataset.adminFrameWired === '1'")
        self.page.evaluate("""() => {
            const a = realFrameDocument().createElement('a');
            a.href = '/audit-unknown-page/'; a.id = 'audit-missing-link'; a.textContent = 'Missing';
            realFrameDocument().querySelector('.custom-header').append(a);
        }""")
        self.page.frame_locator("#realPageFrame").locator("#audit-missing-link").click()
        self.page.wait_for_timeout(150)
        self.assertEqual(self.page.evaluate("state.activePath"), self.a)
        self.assertNotIn("audit-unknown-page", self.page.evaluate("realFrameDocument().location.href"))
        self.assertEqual(self.errors, [])

    def test_missing_preview_does_not_receive_editor_blocks(self):
        self.page.route("**/site/uslugi-linkbildinga/obratnye-ssylki/**", lambda route: route.fulfill(status=404, content_type="text/plain", body="Not found"))
        self.page.evaluate("reloadRealFrame()")
        self.page.wait_for_function("realFrameDocument()?.body?.textContent.trim() === 'Not found'")
        self.page.evaluate("applyDraftToRealFrame()")
        self.assertEqual(self.page.evaluate("realFrameDocument().querySelectorAll('[data-preview-index]').length"), 0)
        self.assertEqual(self.page.evaluate("state.activePath"), self.a)

    def test_unexpected_frame_load_recovers_saved_preview(self):
        self.page.evaluate("document.querySelector('#realPageFrame').src = '/audit-unknown-page/'")
        self.page.wait_for_function("realFrameDocument()?.location.pathname === '/site/uslugi-linkbildinga/obratnye-ssylki/' && !!realFrameDocument().querySelector('.custom-header')")
        self.assertEqual(self.page.evaluate("state.activePath"), self.a)
        self.assertFalse(self.page.evaluate("isMissingSitePage(realFrameDocument())"))

    def test_reset_clears_runtime_and_does_not_request_assets(self):
        result = self.page.evaluate("""async () => {
            state.runtimeAssets = [{url: '/uploads/deleted.webp', runtimeOnly: true}];
            state.pendingCardImagePatches = {stale: {url: '/deleted.webp'}};
            state.imageCompressor.draftUrls = {stale: '/deleted.webp'};
            const calls = [];
            const original = api;
            api = async (path, options) => { calls.push([path, options?.method || 'GET']); return original(path, options); };
            try {
                await resetAdminRuntime(null, {skipConfirm: true});
                return {calls, runtime: state.runtimeAssets.length,
                    patches: Object.keys(state.pendingCardImagePatches).length,
                    drafts: Object.keys(state.imageCompressor.draftUrls).length,
                    disabled: document.querySelector('#adminRuntimeResetBtn').disabled};
            } finally { api = original; }
        }""")
        self.assertEqual(result["runtime"], 0, result)
        self.assertEqual(result["patches"], 0)
        self.assertEqual(result["drafts"], 0)
        self.assertFalse(result["disabled"])
        self.assertFalse(any(path.startswith("/api/assets") or method != "GET" for path, method in result["calls"]), result)

    def test_navigation_cannot_change_inflight_save_target(self):
        result = self.page.evaluate("""async ([a, b]) => {
            const original = api;
            const writes = [];
            api = async (path, options) => {
                if (path.startsWith('/api/assets')) await new Promise(resolve => setTimeout(resolve, 200));
                if (options?.method === 'POST') writes.push(JSON.parse(options.body).path);
                return original(path, options);
            };
            try {
                const saving = savePage();
                await openPage(b);
                await saving;
                return writes;
            } finally { api = original; }
        }""", [self.a, self.b])
        self.assertEqual(result, [self.a])

    def test_invalid_builder_open_preserves_existing_editor(self):
        result = self.page.evaluate("""async path => {
            const original = api;
            const before = state.activePath;
            api = async (url, options) => {
                const data = await original(url, options);
                if (url.startsWith('/api/page?')) data.page.frontmatter.builderJson = '[{broken';
                return data;
            };
            let rejected = false;
            try { await openPage(path); } catch (_) { rejected = true; }
            finally { api = original; }
            return {rejected, unchanged: state.activePath === before};
        }""", self.b)
        self.assertTrue(result["rejected"], result)
        self.assertTrue(result["unchanged"], result)

    def test_unsaved_close_warns(self):
        self.assertTrue(self.page.evaluate("""() => {
            setDirty(true);
            const event = new Event('beforeunload', {cancelable: true});
            window.dispatchEvent(event);
            return event.defaultPrevented;
        }"""))

    def test_failed_reset_preserves_pending_edits(self):
        result = self.page.evaluate("""async () => {
            const original = api;
            state.pendingCardImagePatches = {pending: {url: '/draft.webp'}};
            setDirty(true);
            api = async (path, options) => {
                if (path.startsWith('/api/page?')) throw new Error('Simulated offline');
                return original(path, options);
            };
            try {
                const ok = await resetAdminRuntime(null, {skipConfirm: true});
                return {ok, dirty: state.dirty, count: Object.keys(state.pendingCardImagePatches).length};
            } finally { api = original; }
        }""")
        self.assertEqual(result, {"ok": False, "dirty": True, "count": 1})

    def test_new_card_patch_survives_inflight_save(self):
        result = self.page.evaluate("""async () => {
            const original = api;
            queueCardImagePatch('basesCardImage', 'content/audit.md', '/old.webp', '/middle.webp');
            api = async () => {
                queueCardImagePatch('basesCardImage', 'content/audit.md', '/middle.webp', '/new.webp');
                return {ok: true};
            };
            try {
                await savePendingCardImagePatches();
                return pendingCardImagePatchEntries().map(([, patch]) => [patch.fromUrl, patch.toUrl]);
            } finally { api = original; }
        }""")
        self.assertEqual(result, [["/middle.webp", "/new.webp"]])

    def test_new_news_patch_survives_inflight_save(self):
        result = self.page.evaluate("""async () => {
            const original = saveNewsPostPatchWithoutBuild;
            mergePendingNewsPatch('content/audit.md', {title: 'First'});
            saveNewsPostPatchWithoutBuild = async path => mergePendingNewsPatch(path, {title: 'New'});
            try {
                await savePendingNewsPatches();
                return pendingNewsPatchEntries().map(([, patch]) => patch.title);
            } finally { saveNewsPostPatchWithoutBuild = original; }
        }""")
        self.assertEqual(result, ["New"])

    def test_edits_during_save_and_duplicate_click(self):
        result = self.page.evaluate("""async () => {
            const original = api;
            let writes = 0;
            api = async (path, options) => {
                const data = await original(path, options);
                if (path === '/api/page/save') {
                    writes++;
                    const input = document.querySelector('#fieldTitle');
                    input.value = 'Typed while saving';
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                }
                return data;
            };
            try {
                await Promise.all([savePage(), savePage()]);
                return {writes, dirty: state.dirty, title: document.querySelector('#fieldTitle').value};
            } finally { api = original; }
        }""")
        self.assertEqual(result, {"writes": 1, "dirty": True, "title": "Typed while saving"})

    def test_late_file_upload_does_not_change_other_page(self):
        result = self.page.evaluate("""async path => {
            const original = uploadDownloadFile;
            let resolveUpload;
            uploadDownloadFile = () => new Promise(resolve => {resolveUpload = resolve;});
            try {
                const input = ensureBuilderFileUploadInput();
                input.dataset.blockIndex = '0';
                const transfer = new DataTransfer();
                transfer.items.add(new File(['audit'], 'audit.txt', {type: 'text/plain'}));
                input.files = transfer.files;
                input.dispatchEvent(new Event('change', {bubbles: true}));
                await openPage(path);
                resolveUpload({url: '/files/audit.txt'});
                await new Promise(resolve => setTimeout(resolve, 50));
                return state.builderBlocks[0].fileUrl || '';
            } finally { uploadDownloadFile = original; }
        }""", self.b)
        self.assertEqual(result, "")
        self.assertEqual(self.errors, [])

    def test_late_image_upload_does_not_change_other_target(self):
        result = self.page.evaluate("""async path => {
            const original = uploadAsset;
            let resolveUpload;
            uploadAsset = () => new Promise(resolve => {resolveUpload = resolve;});
            try {
                state.assetPickerTarget = {kind: 'block', blockIndex: 0};
                const input = document.querySelector('#assetPickerUploadInput');
                const transfer = new DataTransfer();
                transfer.items.add(new File(['audit'], 'audit.png', {type: 'image/png'}));
                input.files = transfer.files;
                input.dispatchEvent(new Event('change', {bubbles: true}));
                await openPage(path);
                state.assetPickerTarget = {kind: 'block', blockIndex: 0};
                const before = state.builderBlocks[0].image;
                resolveUpload({url: '/uploads/late-audit.webp'});
                await new Promise(resolve => setTimeout(resolve, 50));
                return state.builderBlocks[0].image === before;
            } finally { uploadAsset = original; }
        }""", self.b)
        self.assertTrue(result)
        self.assertEqual(self.errors, [])

    def test_rollback_image_fallback_has_no_undefined_options(self):
        result = self.page.evaluate("""async () => {
            const original = fetch;
            window.fetch = async (url, options) => {
                if (String(url).includes('adminRollbackSnapshot'))
                    return new Response('<div class="seo-builder"><img src="/uploads/rollback.webp"></div>');
                return original(url, options);
            };
            try { return await restoreBuilderFromLocalPublicSnapshot(); }
            finally { window.fetch = original; }
        }""")
        self.assertTrue(result)

    def test_rollback_button_does_not_clear_later_edits(self):
        self.page.evaluate("restoreBuilderFromLocalPublicSnapshot = async () => false")
        self.page.locator("#reloadSavedPageBtn").click()
        self.page.wait_for_function("!state.localRollbackBusy")
        self.page.evaluate("setDirty(true)")
        self.page.wait_for_timeout(550)
        self.assertTrue(self.page.evaluate("state.dirty"))
        self.assertEqual(self.errors, [])

    def test_repeated_open_edit_save_reset(self):
        result = self.page.evaluate("""async paths => {
            for (let i = 0; i < 12; i++) {
                await openPage(paths[i % paths.length], {discardDirty: true});
                const input = document.querySelector('#fieldTitle');
                input.value = 'Audit ' + i;
                input.dispatchEvent(new Event('input', {bubbles: true}));
                if (!await savePage()) throw new Error('Save failed at ' + i);
                if (!await resetAdminRuntime(null, {skipConfirm: true})) throw new Error('Reset failed');
                if (state.front.title !== 'Audit ' + i) throw new Error('Lost edit ' + i);
                if (state.builderHistory.length || Object.keys(state.pendingCardImagePatches).length)
                    throw new Error('Stale state at ' + i);
            }
            return {dirty: state.dirty, saving: state.savingPage, publishing: state.publishing};
        }""", [self.a, self.b, "content/services/backlinks/index.es.md"])
        self.assertFalse(result["dirty"], result)
        self.assertFalse(result["publishing"], result)
        self.assertEqual(self.errors, [])
        artifacts = ROOT / "admin/test-artifacts"
        artifacts.mkdir(exist_ok=True)
        self.page.screenshot(path=str(artifacts / "runtime-audit-desktop.png"))


if __name__ == "__main__":
    # Mutating tests must stay confined to the temporary project, even on failure.
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "content").rglob("*.md")}
    try:
        result = unittest.main(exit=False, verbosity=2).result
    finally:
        HTTP.shutdown()
        HTTP.server_close()
        TEMP.cleanup()
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "content").rglob("*.md")}
        assert before == after, "Real content changed during isolated tests"
    sys.exit(not result.wasSuccessful())
