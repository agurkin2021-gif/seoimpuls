import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ADMIN_URL = process.env.ADMIN_URL || "http://127.0.0.1:8787/";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "";
const PUBLIC_URL = process.env.PUBLIC_URL || "http://127.0.0.1:1314/ru/services/";
const DEBUG_PORT = Number(process.env.CDP_PORT || 9349);
const SNAP_AND_SAVE = process.env.SNAP_AND_SAVE === "1";

const chromeCandidates = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  join(process.env.LOCALAPPDATA || "", "Google\\Chrome\\Application\\chrome.exe"),
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
].filter(Boolean);

function assert(condition, message, details = null) {
  if (!condition) {
    const error = new Error(message);
    error.details = details;
    throw error;
  }
}

async function canFetch(url) {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(1500) });
    return response.status < 500;
  } catch {
    return false;
  }
}

async function waitForHttp(url, timeoutMs = 15000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    if (await canFetch(url)) return true;
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  return false;
}

function findChrome() {
  const chrome = chromeCandidates.find((candidate) => existsSync(candidate));
  assert(chrome, "Chrome or Edge executable was not found. Set CHROME_PATH.");
  return chrome;
}

async function startChrome() {
  const userDataDir = mkdtempSync(join(tmpdir(), "seoimpuls-parity-"));
  const child = spawn(findChrome(), [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--window-size=1700,1000",
    `--remote-debugging-port=${DEBUG_PORT}`,
    `--user-data-dir=${userDataDir}`,
    "about:blank",
  ], { stdio: "ignore", windowsHide: true });
  const ready = await waitForHttp(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
  assert(ready, `Chrome DevTools did not start on port ${DEBUG_PORT}.`);
  return {
    child,
    userDataDir,
    async close() {
      child.kill();
      await new Promise((resolve) => setTimeout(resolve, 400));
      rmSync(userDataDir, { recursive: true, force: true });
    },
  };
}

async function openCdpPage(url) {
  const target = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/new?${encodeURIComponent(url)}`, { method: "PUT" }).then((response) => response.json());
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  ws.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  });
  await new Promise((resolve) => ws.addEventListener("open", resolve, { once: true }));
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const callId = ++id;
    pending.set(callId, { resolve, reject });
    ws.send(JSON.stringify({ id: callId, method, params }));
  });
  await send("Page.enable");
  await send("Runtime.enable");
  const evaluate = async (expression) => {
    const result = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true, userGesture: true });
    if (result.exceptionDetails) {
      const details = result.exceptionDetails;
      const message = details.exception?.description || details.exception?.value || details.text || JSON.stringify(details);
      throw new Error(message);
    }
    return result.result.value;
  };
  const waitFor = async (expression, timeoutMs = 15000) => {
    const started = Date.now();
    while (Date.now() - started < timeoutMs) {
      if (await evaluate(expression)) return true;
      await new Promise((resolve) => setTimeout(resolve, 150));
    }
    throw new Error(`Timed out waiting for: ${expression}`);
  };
  return { evaluate, waitFor, close: async () => ws.close() };
}

async function openAdminServices(page) {
  await page.waitFor("document.readyState === 'complete'");
  const needsLogin = await page.evaluate("!!document.querySelector('input[name=\"password\"]')");
  if (needsLogin) {
    assert(ADMIN_PASSWORD, "ADMIN_PASSWORD is required for this admin URL");
    await page.evaluate(`(() => {
      document.querySelector('input[name="password"]').value = ${JSON.stringify(ADMIN_PASSWORD)};
      document.querySelector('form').requestSubmit();
      return true;
    })()`);
  }
  await page.waitFor("!!document.querySelector('#pageList .page-item')", 25000);
  await page.evaluate(`(() => {
    const search = document.querySelector('#searchInput');
    if (search) {
      search.value = '';
      search.dispatchEvent(new Event('input', { bubbles: true }));
    }
    const filter = document.querySelector('#langFilter');
    filter.value = 'ru';
    filter.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 600));
  await page.evaluate(`(() => {
    const row = Array.from(document.querySelectorAll('.page-item')).find((item) => item.dataset.path === 'content/services/_index.ru.md');
    if (!row) throw new Error('RU services row not found');
    row.querySelector('.page-open').click();
    return true;
  })()`);
  await page.waitFor("document.querySelector('#fieldFilePath')?.value === 'content/services/_index.ru.md'", 15000);
  await page.waitFor(`(() => {
    const doc = document.querySelector('#realPageFrame')?.contentDocument;
    return !!(doc && doc.querySelectorAll('.admin-real-image-wrap').length >= 3 && doc.querySelectorAll('.seo-builder-block--buttons .seo-cta').length >= 3);
  })()`, 25000);
}

function measureScript(rootExpression) {
  return `JSON.stringify((() => {
    const root = ${rootExpression};
    const builder = root.querySelector('.seo-builder');
    const base = builder.getBoundingClientRect();
    const rectOf = (node) => {
      const rect = node.getBoundingClientRect();
      return {
        x: Math.round(rect.left - base.left),
        y: Math.round(rect.top - base.top),
        w: Math.round(rect.width),
        h: Math.round(rect.height),
        bottom: Math.round(rect.bottom - base.top)
      };
    };
    return {
      builder: rectOf(builder),
      images: Array.from(root.querySelectorAll('.seo-builder-block--image')).slice(0, 3).map(rectOf),
      buttonBlocks: Array.from(root.querySelectorAll('.seo-builder-block--buttons')).slice(0, 3).map(rectOf),
      buttons: Array.from(root.querySelectorAll('.seo-builder-block--buttons .seo-cta')).slice(0, 3).map(rectOf),
      styles: Array.from(root.querySelectorAll('.seo-builder-block--buttons')).slice(0, 3).map((block) => ({
        style: block.getAttribute('style') || '',
        cls: block.className,
        buttonStyle: block.querySelector('.seo-cta')?.getAttribute('style') || ''
      }))
    };
  })())`;
}

function alignmentScript(rootExpression) {
  return `JSON.stringify((() => {
    const root = ${rootExpression};
    const builder = root.querySelector('.seo-builder');
    const base = builder.getBoundingClientRect();
    const rectOf = (node) => {
      const rect = node.getBoundingClientRect();
      return {
        x: Math.round(rect.left - base.left),
        y: Math.round(rect.top - base.top),
        w: Math.round(rect.width),
        h: Math.round(rect.height),
        bottom: Math.round(rect.bottom - base.top)
      };
    };
    const images = Array.from(root.querySelectorAll('.seo-builder-block--image')).slice(0, 3)
      .map((block) => block.querySelector('.admin-real-image-wrap') || block.querySelector('img') || block)
      .map(rectOf)
      .sort((a, b) => a.x - b.x);
    const buttons = Array.from(root.querySelectorAll('.seo-builder-block--buttons .seo-cta')).slice(0, 3)
      .map(rectOf)
      .sort((a, b) => a.x - b.x);
    const pairs = images.map((image, index) => {
      const button = buttons[index];
      return {
        index,
        image,
        button,
        leftDelta: button ? button.x - image.x : null,
        widthDelta: button ? button.w - image.w : null,
        gap: button ? button.y - image.bottom : null
      };
    });
    const maxEdgeDelta = Math.max(...pairs.flatMap((pair) => [
      Math.abs(pair.leftDelta || 0),
      Math.abs(pair.widthDelta || 0),
      Math.abs((pair.gap || 0) - 8)
    ]));
    return { images, buttons, pairs, maxEdgeDelta };
  })())`;
}

const chrome = await startChrome();
let adminPage;
let publicPage;
try {
  adminPage = await openCdpPage(ADMIN_URL);
  await openAdminServices(adminPage);
  let snapSave = null;
  if (SNAP_AND_SAVE) {
    snapSave = await adminPage.evaluate(`(async () => {
      const changed = snapCompactButtonsToImageRow();
      renderBuilder();
      applyDraftToRealFrame();
      await new Promise((resolve) => requestAnimationFrame(resolve));
      syncFieldsToFront();
      const save = await api("/api/page/save", {
        method: "POST",
        body: JSON.stringify({
          path: state.activePath,
          frontmatter: state.front,
          body: state.body
        })
      });
      const build = await api("/api/build", { method: "POST", body: "{}" });
      return { changed, save, buildOk: !!build };
    })()`);
  }
  const admin = JSON.parse(await adminPage.evaluate(measureScript("document.querySelector('#realPageFrame').contentDocument")));
  const adminAlignment = JSON.parse(await adminPage.evaluate(alignmentScript("document.querySelector('#realPageFrame').contentDocument")));

  publicPage = await openCdpPage(SNAP_AND_SAVE ? `${PUBLIC_URL}?snap=${Date.now()}` : PUBLIC_URL);
  await publicPage.waitFor("document.readyState === 'complete'");
  await publicPage.waitFor("document.querySelectorAll('.seo-builder-block--buttons .seo-cta').length >= 3", 25000);
  const pub = JSON.parse(await publicPage.evaluate(measureScript("document")));
  const publicAlignment = JSON.parse(await publicPage.evaluate(alignmentScript("document")));

  const deltas = admin.buttons.map((button, index) => ({
    index,
    x: pub.buttons[index]?.x - button.x,
    y: pub.buttons[index]?.y - button.y,
    w: pub.buttons[index]?.w - button.w,
    h: pub.buttons[index]?.h - button.h,
  }));
  const maxButtonDelta = Math.max(...deltas.flatMap((delta) => [delta.x, delta.y, delta.w, delta.h].map((value) => Math.abs(value || 0))));
  assert(maxButtonDelta <= 1, "Admin preview and public page button positions differ", { maxButtonDelta, deltas, admin, public: pub });
  if (SNAP_AND_SAVE) {
    assert(adminAlignment.maxEdgeDelta <= 1, "Admin buttons are not aligned under images after snap/save", { snapSave, adminAlignment });
    assert(publicAlignment.maxEdgeDelta <= 1, "Public buttons are not aligned under images after snap/save", { snapSave, publicAlignment });
  }
  const boundaryStress = JSON.parse(await adminPage.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const box = () => {
      const builder = doc.querySelector('.seo-builder').getBoundingClientRect();
      const rect = (node) => {
        const item = node.getBoundingClientRect();
        return {
          left: Math.round(item.left - builder.left),
          right: Math.round(item.right - builder.left),
          width: Math.round(item.width)
        };
      };
      return {
        builder: { left: 0, right: Math.round(builder.width), width: Math.round(builder.width) },
        firstImage: rect(doc.querySelector('[data-preview-index="0"] .admin-real-image-wrap')),
        thirdImage: rect(doc.querySelector('[data-preview-index="2"] .admin-real-image-wrap')),
        thirdButton: rect(doc.querySelector('[data-preview-index="5"] .seo-cta'))
      };
    };
    const dispatch = (target, type, x, y, pointerId) => target.dispatchEvent(new win.PointerEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0, pointerId, pointerType: 'mouse' }));
    const thirdRight = doc.querySelector('[data-preview-index="2"] [data-image-resize="right"]');
    let r = thirdRight.getBoundingClientRect();
    dispatch(thirdRight, 'pointerdown', r.left + 4, r.top + 20, 81);
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: r.left + 1200, clientY: r.top + 20, button: 0, pointerId: 81, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: r.left + 1200, clientY: r.top + 20, button: 0, pointerId: 81, pointerType: 'mouse' }));

    const firstImage = doc.querySelector('[data-preview-index="0"] [data-image-drag]');
    r = firstImage.getBoundingClientRect();
    dispatch(firstImage, 'pointerdown', r.left + 40, r.top + 40, 82);
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: r.left - 900, clientY: r.top + 40, button: 0, pointerId: 82, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: r.left - 900, clientY: r.top + 40, button: 0, pointerId: 82, pointerType: 'mouse' }));

    state.selectedBlockIndex = 5;
    renderBuilder();
    const input = document.querySelector('#builderList .builder-block[data-index="5"] input[data-field="buttonPixelWidth"]');
    input.value = '2400';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return box();
  })())`));
  const inside = [boundaryStress.firstImage, boundaryStress.thirdImage, boundaryStress.thirdButton].every((item) => (
    item.left >= -1 && item.right <= boundaryStress.builder.right + 1
  ));
  assert(inside, "Admin boundary clamp failed for image/button stress", boundaryStress);

  console.log(JSON.stringify({ ok: true, adminUrl: ADMIN_URL, publicUrl: PUBLIC_URL, snapSave, maxButtonDelta, adminAlignment, publicAlignment, admin, public: pub, deltas, boundaryStress }, null, 2));
} finally {
  if (adminPage) await adminPage.close();
  if (publicPage) await publicPage.close();
  await chrome.close();
}
