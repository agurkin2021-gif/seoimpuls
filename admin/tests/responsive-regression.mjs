import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ROOT = new URL("../../", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const ADMIN_URL = process.env.ADMIN_URL || "http://127.0.0.1:8787/";
const HUGO_URL = process.env.HUGO_URL || "http://127.0.0.1:1314/";
const SERVICE_URL = new URL("/ru/services/", HUGO_URL).toString();
const TEST_BUTTON_URL = new URL("/ru/admin-test/button-url-drag-test/", HUGO_URL).toString();
const FULL_STRESS_PATH = "content/admin-test/full-editor-stress/index.ru.md";
const FULL_STRESS_URL = new URL("/ru/admin-test/full-editor-stress/", HUGO_URL).toString();
const DEBUG_PORT = Number(process.env.CDP_PORT || 9337);

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

function rgbParts(value) {
  return (String(value).match(/\d+(?:\.\d+)?/g) || []).slice(0, 3).map(Number);
}

function relativeLuminance(rgb) {
  const convert = (value) => {
    const channel = value / 255;
    return channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
  };
  const [r, g, b] = rgb.map(convert);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(a, b) {
  const first = relativeLuminance(a);
  const second = relativeLuminance(b);
  return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
}

async function canFetch(url) {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(1500) });
    return response.ok;
  } catch {
    return false;
  }
}

async function adminApi(path, options = {}) {
  const response = await fetch(new URL(path, ADMIN_URL), {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  assert(response.ok && data.ok !== false, `Admin API failed: ${path}`, data);
  return data;
}

function findChrome() {
  const chrome = chromeCandidates.find((candidate) => existsSync(candidate));
  assert(chrome, "Chrome or Edge executable was not found. Set CHROME_PATH.");
  return chrome;
}

async function waitForHttp(url, timeoutMs = 20000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    if (await canFetch(url)) return true;
    await new Promise((resolve) => setTimeout(resolve, 300));
  }
  return false;
}

async function startHugoIfNeeded() {
  if (await canFetch(SERVICE_URL)) return null;
  const child = spawn("hugo", ["server", "--noBuildLock", "--bind", "127.0.0.1", "--port", "1314", "--disableFastRender"], {
    cwd: ROOT,
    stdio: "ignore",
    windowsHide: true,
  });
  const ready = await waitForHttp(SERVICE_URL, 30000);
  assert(ready, "Hugo server did not start on http://127.0.0.1:1314/ru/services/");
  return child;
}

async function startChrome() {
  const userDataDir = mkdtempSync(join(tmpdir(), "seoimpuls-cdp-"));
  const child = spawn(findChrome(), [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--remote-debugging-port=${DEBUG_PORT}`,
    `--user-data-dir=${userDataDir}`,
    "about:blank",
  ], { stdio: "ignore", windowsHide: true });
  const versionUrl = `http://127.0.0.1:${DEBUG_PORT}/json/version`;
  const ready = await waitForHttp(versionUrl, 15000);
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

  await send("Runtime.enable");
  await send("Page.enable");
  return {
    send,
    evaluate,
    waitFor,
    close: () => ws.close(),
  };
}

async function testPublicResponsive() {
  const viewports = [
    { name: "desktop", width: 1440, height: 1000 },
    { name: "tablet", width: 1024, height: 900 },
    { name: "mobile", width: 390, height: 900 },
  ];
  const results = [];

  for (const viewport of viewports) {
    const page = await openCdpPage(SERVICE_URL);
    await page.send("Emulation.setDeviceMetricsOverride", {
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: 1,
      mobile: viewport.width < 768,
    });
    await page.send("Page.navigate", { url: SERVICE_URL });
    await page.waitFor("document.readyState === 'complete'");
    await page.waitFor("!!document.querySelector('.seo-builder')");
    const gdprBackdrop = JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const backdrop = document.querySelector('.gdpr-consent-backdrop');
      const modal = document.querySelector('.gdpr-consent-modal');
      if (!backdrop) return { missing: true };
      const style = getComputedStyle(backdrop);
      return {
        hidden: backdrop.hidden,
        pointer: style.pointerEvents,
        modalOpen: !!modal && !modal.hidden
      };
    })())`));
    assert(gdprBackdrop.missing || gdprBackdrop.hidden || gdprBackdrop.pointer === "none" || gdprBackdrop.modalOpen, `Public ${viewport.name} GDPR backdrop intercepts page clicks while only the banner is open.`, gdprBackdrop);
    await page.evaluate(`(() => {
      localStorage.setItem('seoimpuls_cookie_consent_v2', JSON.stringify({ analytics: false, updatedAt: new Date().toISOString(), policyVersion: '2026-02-28', lang: 'ru', source: 'responsive-service-test' }));
      document.cookie = 'seoimpuls_cookie_consent_v2=' + encodeURIComponent(localStorage.getItem('seoimpuls_cookie_consent_v2')) + '; path=/; max-age=31536000; SameSite=Lax';
      return true;
    })()`);
    await page.send("Page.reload", { ignoreCache: true });
    await page.waitFor("document.readyState === 'complete'");
    await page.waitFor("!!document.querySelector('.seo-builder')");
    await page.evaluate(`(() => {
      const button = document.querySelector('.seo-builder-block--buttons.seo-builder-block--compact .seo-cta');
      button?.scrollIntoView({ block: 'center', inline: 'center' });
      if (!button) return false;
      const rect = button.getBoundingClientRect();
      window.scrollBy({ top: rect.top - (innerHeight - rect.height) / 2, left: 0, behavior: 'instant' });
      return true;
    })()`);
    await new Promise((resolve) => setTimeout(resolve, 180));
    const metrics = JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const root = document.documentElement;
      const images = Array.from(document.querySelectorAll('.seo-builder-block--image img')).map((img) => {
        const rect = img.getBoundingClientRect();
        const style = getComputedStyle(img);
        return {
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
          transform: style.transform,
        };
      });
      const compactButtons = Array.from(document.querySelectorAll('.seo-builder-block--buttons.seo-builder-block--compact')).map((block) => {
        const button = block.querySelector('.seo-cta');
        const blockRect = block.getBoundingClientRect();
        const buttonRect = button?.getBoundingClientRect();
        const style = getComputedStyle(block);
        const hit = buttonRect ? document.elementFromPoint(buttonRect.left + buttonRect.width / 2, buttonRect.top + buttonRect.height / 2) : null;
        return {
          label: button?.textContent.trim() || '',
          href: button?.href || '',
          padding: style.paddingTop,
          border: style.borderTopWidth,
          background: style.backgroundColor,
          widthDelta: buttonRect ? Math.round(Math.abs(blockRect.width - buttonRect.width)) : null,
          heightDelta: buttonRect ? Math.round(Math.abs(blockRect.height - buttonRect.height)) : null,
          hitInside: !!button && !!hit && (hit === button || button.contains(hit)),
          hit: hit ? { tag: hit.tagName, cls: String(hit.className || ''), href: hit.href || '' } : null
        };
      });
      const overflowers = Array.from(document.body.querySelectorAll('*'))
        .map((el) => ({ tag: el.tagName, cls: String(el.className || ''), right: Math.round(el.getBoundingClientRect().right) }))
        .filter((item) => item.right > root.clientWidth + 2)
        .slice(0, 8);
      return {
        clientWidth: root.clientWidth,
        scrollWidth: root.scrollWidth,
        images,
        compactButtons,
        overflowers,
      };
    })())`));
    if (viewport.name === "desktop") {
      const lightLink = JSON.parse(await page.evaluate(`JSON.stringify((() => {
        document.body.setAttribute('theme', 'light');
        const link = document.querySelector('.seo-builder-text a, .seo-hero-text a');
        if (!link) return { found: false };
        const style = getComputedStyle(link);
        return {
          found: true,
          text: link.textContent.trim(),
          color: style.color,
          filter: style.filter,
          decoration: style.textDecorationLine
        };
      })())`));
      lightLink.contrastVsWhite = Number(contrastRatio(rgbParts(lightLink.color), [255, 255, 255]).toFixed(2));
      assert(lightLink.found && lightLink.decoration.includes("underline") && lightLink.contrastVsWhite >= 4.5, "Public light theme text anchor is not visible enough.", lightLink);
    }
    results.push({ viewport, metrics });
    assert(metrics.scrollWidth <= metrics.clientWidth + 2, `Public ${viewport.name} has horizontal overflow.`, metrics);
    assert(metrics.overflowers.length === 0, `Public ${viewport.name} has clipped elements outside the viewport.`, metrics.overflowers);
    assert(metrics.compactButtons.length > 0, `Public ${viewport.name} services page has no compact button to test.`, metrics);
    assert(metrics.compactButtons.every((item) => item.padding === "0px" && item.border === "0px" && item.background === "rgba(0, 0, 0, 0)"), `Public ${viewport.name} compact service button has wrapper chrome.`, metrics.compactButtons);
    assert(metrics.compactButtons.every((item) => item.widthDelta <= 2 && item.heightDelta <= 2 && item.hitInside), `Public ${viewport.name} compact service button is blocked or wrapper-sized.`, metrics.compactButtons);
    if (viewport.width <= 1100) {
      assert(metrics.images.every((image) => image.transform === "none"), `Public ${viewport.name} still has image transforms on responsive layout.`, metrics.images);
      assert(metrics.images.every((image) => image.left >= -1 && image.right <= metrics.clientWidth + 2), `Public ${viewport.name} image escapes viewport.`, metrics.images);
    }
    page.close();
  }

  return results;
}

async function openServicesInAdmin(page) {
  await page.waitFor("!!document.querySelector('#langFilter') && document.querySelectorAll('.page-item').length > 0");
  await page.evaluate(`(() => {
    const filter = document.querySelector('#langFilter');
    filter.value = 'ru';
    filter.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  await page.evaluate(`(() => {
    const row = Array.from(document.querySelectorAll('.page-item')).find((item) => item.dataset.path === 'content/services/_index.ru.md');
    if (!row) throw new Error('services page not found');
    row.querySelector('.page-open').click();
    return true;
  })()`);
  await page.waitFor(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame && frame.contentDocument;
    return !!(doc && doc.querySelector('[data-preview-index="2"] .admin-real-image-wrap'));
  })()`);
}

async function openPageInAdmin(page, path, lang = "ru") {
  await page.waitFor("!!document.querySelector('#langFilter') && document.querySelectorAll('.page-item').length > 0");
  await page.evaluate(`(() => {
    const search = document.querySelector('#searchInput');
    if (search) {
      search.value = '';
      search.dispatchEvent(new Event('input', { bubbles: true }));
    }
    const filter = document.querySelector('#langFilter');
    filter.value = '${lang}';
    filter.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  await page.evaluate(`(() => {
    const row = Array.from(document.querySelectorAll('.page-item')).find((item) => item.dataset.path === '${path}');
    if (!row) throw new Error('admin page not found: ${path}');
    row.querySelector('.page-open').click();
    return true;
  })()`);
  await page.waitFor(`document.querySelector('#fieldFilePath')?.value === '${path}'`);
  await page.waitFor(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame && frame.contentDocument;
    return !!(doc && doc.body && doc.readyState !== 'loading');
  })()`);
}

async function keepOnlyServiceImageRow(page) {
  await page.evaluate(`(() => {
    state.builderBlocks = state.builderBlocks.slice(0, 3);
    state.selectedBlockIndex = 0;
    state.selectedButton = null;
    state.insertPoint = null;
    renderBuilder();
    updatePreview();
    return true;
  })()`);
  await page.waitFor(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame && frame.contentDocument;
    return doc && doc.querySelectorAll('[data-preview-index]').length === 3;
  })()`);
}

async function adminImageRects(page) {
  return JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    return Array.from(doc.querySelectorAll('[data-preview-index]')).map((block) => {
      const image = block.querySelector('.admin-real-image-wrap') || block;
      const rect = image.getBoundingClientRect();
      return {
        index: Number(block.dataset.previewIndex),
        cls: String(block.className),
        top: Math.round(rect.top),
        left: Math.round(rect.left),
        right: Math.round(rect.right),
        bottom: Math.round(rect.bottom),
      };
    });
  })())`));
}

function adminOrder(rects) {
  return rects.map((item) => {
    if (item.cls.includes("seo-builder-block--buttons")) return "buttons";
    if (item.cls.includes("seo-builder-block--text")) return "text";
    if (item.cls.includes("seo-builder-block--wrap")) return "wrap";
    if (item.cls.includes("seo-builder-block--image")) return "image";
    return "other";
  });
}

async function clickAdminFrameBlock(page, index) {
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const block = doc.querySelector('[data-preview-index="${index}"]');
    const rect = block.getBoundingClientRect();
    const x = rect.left + 20;
    const y = rect.top + 20;
    block.dispatchEvent(new win.PointerEvent('pointerdown', { bubbles: true, clientX: x, clientY: y, button: 0, pointerId: 1, pointerType: 'mouse' }));
    block.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: x, clientY: y, button: 0, pointerId: 1, pointerType: 'mouse' }));
    return true;
  })()`);
}

async function testExistingServiceButtonHandles(page) {
  const result = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const block = doc.querySelector('[data-preview-index="3"].seo-builder-block--buttons');
    if (!block) return { missing: true };
    block.scrollIntoView({ block: 'center', inline: 'center' });
    const byPoint = (rect) => {
      const target = doc.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
      return target ? { tag: target.tagName, className: String(target.className || ''), resize: target.dataset.buttonResize || '', move: target.dataset.buttonMove || '' } : null;
    };
    const rectInfo = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return {
        display: style.display,
        opacity: style.opacity,
        left: Math.round(rect.left),
        top: Math.round(rect.top),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        background: style.backgroundColor,
        boxShadow: style.boxShadow,
        hit: byPoint(rect)
      };
    };
    const dispatch = (target, type, x, y, pointerId, button = 0, buttons = null) => target.dispatchEvent(new win.PointerEvent(type, {
      bubbles: true,
      clientX: x,
      clientY: y,
      button,
      buttons: buttons ?? (type === 'pointerup' ? 0 : (button === 2 ? 2 : 1)),
      pointerId,
      pointerType: 'mouse'
    }));
    const buttonRect = () => doc.querySelector('[data-preview-index="3"] .seo-cta').getBoundingClientRect();
    const start = buttonRect();
    let right = block.querySelector('[data-button-resize="right"]');
    let bottom = block.querySelector('[data-button-resize="bottom"]');
    let move = block.querySelector('[data-button-move]');
    const handles = {
      right: rectInfo(right),
      bottom: rectInfo(bottom),
      move: rectInfo(move)
    };
    let r = bottom.getBoundingClientRect();
    let target = doc.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    dispatch(target, 'pointerdown', r.left + r.width / 2, r.top + r.height / 2, 41);
    dispatch(target, 'pointermove', r.left + r.width / 2, r.top + r.height / 2 + 34, 41);
    dispatch(target, 'pointerup', r.left + r.width / 2, r.top + r.height / 2 + 34, 41);
    right = doc.querySelector('[data-preview-index="3"] [data-button-resize="right"]');
    bottom = doc.querySelector('[data-preview-index="3"] [data-button-resize="bottom"]');
    r = right.getBoundingClientRect();
    target = doc.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    dispatch(target, 'pointerdown', r.left + r.width / 2, r.top + r.height / 2, 42);
    dispatch(target, 'pointermove', r.left + r.width / 2 + 96, r.top + r.height / 2, 42);
    dispatch(target, 'pointerup', r.left + r.width / 2 + 96, r.top + r.height / 2, 42);
    move = doc.querySelector('[data-preview-index="3"] [data-button-move]');
    const afterResize = buttonRect();
    r = move.getBoundingClientRect();
    target = doc.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    dispatch(target, 'pointerdown', r.left + r.width / 2, r.top + r.height / 2, 43);
    dispatch(target, 'pointermove', r.left + r.width / 2 + 140, r.top + r.height / 2 + 72, 43);
    dispatch(target, 'pointerup', r.left + r.width / 2 + 140, r.top + r.height / 2 + 72, 43);
    const afterMove = buttonRect();
    const button = doc.querySelector('[data-preview-index="3"] .seo-cta');
    r = button.getBoundingClientRect();
    dispatch(button, 'pointerdown', r.left + r.width / 2, r.top + r.height / 2, 44, 2, 2);
    dispatch(doc, 'pointermove', r.left + r.width / 2 + 88, r.top + r.height / 2 + 44, 44, 2, 2);
    dispatch(doc, 'pointerup', r.left + r.width / 2 + 88, r.top + r.height / 2 + 44, 44, 2, 0);
    doc.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: r.left + r.width / 2 + 88, clientY: r.top + r.height / 2 + 44, button: 2 }));
    const afterRightDrag = buttonRect();
    return {
      missing: false,
      handles,
      start: { width: Math.round(start.width), height: Math.round(start.height), left: Math.round(start.left), top: Math.round(start.top) },
      afterResize: { width: Math.round(afterResize.width), height: Math.round(afterResize.height), left: Math.round(afterResize.left), top: Math.round(afterResize.top) },
      afterMove: { width: Math.round(afterMove.width), height: Math.round(afterMove.height), left: Math.round(afterMove.left), top: Math.round(afterMove.top) },
      afterRightDrag: { width: Math.round(afterRightDrag.width), height: Math.round(afterRightDrag.height), left: Math.round(afterRightDrag.left), top: Math.round(afterRightDrag.top) },
      inspectorMode: document.querySelector('#builderList .builder-block[data-index="3"] select[data-field="buttonWidthMode"]')?.value || '',
      inspectorWidth: Number(document.querySelector('#builderList .builder-block[data-index="3"] input[data-field="buttonPixelWidth"]')?.value || 0),
      inspectorHeight: Number(document.querySelector('#builderList .builder-block[data-index="3"] input[data-field="buttonPixelHeight"]')?.value || 0)
    };
  })())`));
  assert(!result.missing, "Existing service button block is missing before reset.", result);
  assert(result.handles.right.hit?.resize === "right", "Existing service button right resize handle is not hit-testable.", result);
  assert(result.handles.bottom.hit?.resize === "bottom", "Existing service button bottom resize handle is not hit-testable.", result);
  assert(result.handles.move.hit?.move === "1", "Existing service button move handle is not hit-testable.", result);
  assert(
    [result.handles.right, result.handles.bottom, result.handles.move].every((handle) => handle.background === "rgba(0, 0, 0, 0)" && handle.boxShadow === "none"),
    "Button handles should keep a transparent hit area instead of covering the real button view.",
    result
  );
  assert(result.afterResize.width >= result.start.width + 70, "Existing service button right resize did not work.", result);
  assert(result.afterResize.height >= result.start.height + 20, "Existing service button bottom resize did not work.", result);
  assert(Math.abs(result.afterMove.left - result.afterResize.left) >= 70 || Math.abs(result.afterMove.top - result.afterResize.top) >= 35, "Existing service button move handle did not move the button.", result);
  assert(Math.abs(result.afterRightDrag.left - result.afterMove.left) >= 50 || Math.abs(result.afterRightDrag.top - result.afterMove.top) >= 30, "Right mouse drag on the button body did not move the button.", result);
  assert(result.inspectorMode === "custom" && result.inspectorWidth >= result.afterResize.width - 3 && result.inspectorHeight >= result.afterResize.height - 3, "Existing service button resize did not sync to inspector.", result);
  return result;
}

async function testRightMouseImageDrag(page) {
  const result = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    let image = doc.querySelector('[data-preview-index="0"] [data-image-drag]');
    if (!image) return { missing: true };
    const dispatch = (target, type, x, y, pointerId, buttons = 2) => target.dispatchEvent(new win.PointerEvent(type, {
      bubbles: true,
      clientX: x,
      clientY: y,
      button: 2,
      buttons: type === 'pointerup' ? 0 : buttons,
      pointerId,
      pointerType: 'mouse'
    }));
    const rectOf = () => {
      const current = doc.querySelector('[data-preview-index="0"] [data-image-drag]');
      const rect = current.getBoundingClientRect();
      return { left: Math.round(rect.left), top: Math.round(rect.top), width: Math.round(rect.width), height: Math.round(rect.height) };
    };
    const start = rectOf();
    dispatch(image, 'pointerdown', start.left + start.width / 2, start.top + start.height / 2, 52, 2);
    dispatch(doc, 'pointermove', start.left + start.width / 2 + 74, start.top + start.height / 2 + 38, 52, 2);
    dispatch(doc, 'pointerup', start.left + start.width / 2 + 74, start.top + start.height / 2 + 38, 52, 0);
    image = doc.querySelector('[data-preview-index="0"] [data-image-drag]');
    const menuEvent = new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: start.left + 20, clientY: start.top + 20, button: 2 });
    const menuAllowed = image.dispatchEvent(menuEvent);
    const after = rectOf();
    return {
      missing: false,
      start,
      after,
      menuPrevented: !menuAllowed || menuEvent.defaultPrevented,
      stateOffset: {
        x: Number(state.builderBlocks[0]?.imageOffsetX) || 0,
        y: Number(state.builderBlocks[0]?.imageOffsetY) || 0
      }
    };
  })())`));
  assert(!result.missing, "Image for right mouse drag test is missing.", result);
  assert(Math.abs(result.after.left - result.start.left) >= 40 || Math.abs(result.after.top - result.start.top) >= 20, "Right mouse drag on image body did not move the image.", result);
  assert(result.menuPrevented, "Right mouse drag area should prevent the browser context menu.", result);
  assert(Math.abs(result.stateOffset.x) >= 40 || Math.abs(result.stateOffset.y) >= 20, "Right mouse image drag did not sync image offsets to state.", result);
  return result;
}

async function testHorizontalImageBalanceEdges(page) {
  const setup = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    if (!doc?.querySelector('[data-preview-index="0"] [data-image-drag]')) return { missing: true };
    state.builderBlocks.slice(0, 3).forEach((block, index) => {
      block.width = 'third';
      block.offsetX = 0;
      block.offsetY = 0;
      block.imageOffsetX = index * 5;
      block.imageOffsetY = [0, -19, 26][index];
      block.imagePixelWidth = [360, 372, 348][index];
      block.imagePixelHeight = [356, 392, 332][index];
    });
    setSelectedImageIndexes([0, 1, 2]);
    renderBuilder();
    applyDraftToRealFrame();
    state.selectedImageBlockIndexes = new Set();
    state.selectedImageBlockIndex = null;
    const before = Array.from(doc.querySelectorAll('[data-preview-index] .admin-real-image-wrap')).slice(0, 3).map((wrap) => {
      const rect = wrap.getBoundingClientRect();
      return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
    });
    const toolbarBalance = document.querySelector('.builder-toolbar [data-balance-images="horizontal"]');
    const hasBalanceDetails = !!document.querySelector('.builder-toolbar .balance-tools');
    toolbarBalance?.scrollIntoView({ block: 'center', inline: 'center' });
    const buttonRect = toolbarBalance?.getBoundingClientRect();
    return {
      missing: false,
      hasToolbarBalance: !!toolbarBalance,
      hasBalanceDetails,
      before,
      buttonRect: buttonRect ? {
        left: Math.round(buttonRect.left),
        top: Math.round(buttonRect.top),
        width: Math.round(buttonRect.width),
        height: Math.round(buttonRect.height)
      } : null
    };
  })())`));
  assert(!setup.missing, "Images for horizontal balance test are missing.", setup);
  assert(setup.hasToolbarBalance && !setup.hasBalanceDetails, "Balance must be a direct toolbar button, not a no-op dropdown summary.", setup);
  assert(setup.buttonRect && setup.buttonRect.width > 20 && setup.buttonRect.height > 20, "Balance toolbar button is not measurable for live click.", setup);
  const balanceX = Math.round(setup.buttonRect.left + setup.buttonRect.width / 2);
  const balanceY = Math.round(setup.buttonRect.top + setup.buttonRect.height / 2);
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: balanceX, y: balanceY, button: "none" });
  await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: balanceX, y: balanceY, button: "left", clickCount: 1 });
  await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: balanceX, y: balanceY, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 500));
  const result = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const after = Array.from(doc.querySelectorAll('[data-preview-index] .admin-real-image-wrap')).slice(0, 3).map((wrap) => {
      const rect = wrap.getBoundingClientRect();
      return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
    });
    return {
      missing: false,
      before: ${JSON.stringify(setup.before)},
      after,
      topSpread: Math.max(...after.map((item) => item.top)) - Math.min(...after.map((item) => item.top)),
      bottomSpread: Math.max(...after.map((item) => item.bottom)) - Math.min(...after.map((item) => item.bottom)),
      heights: state.builderBlocks.slice(0, 3).map((block) => Number(block.imagePixelHeight) || 0),
      offsetsY: state.builderBlocks.slice(0, 3).map((block) => Number(block.imageOffsetY) || 0),
      restoredSelection: Array.from(state.selectedImageBlockIndexes || []),
      toast: document.querySelector('#toast')?.textContent || ''
    };
  })())`));
  assert(result.before.some((item, index, list) => item.top !== list[0].top || item.bottom !== list[0].bottom), "Horizontal balance test setup did not skew image edges.", result);
  assert(result.topSpread <= 1, "Horizontal image balance did not align top edges to one line.", result);
  assert(result.bottomSpread <= 1, "Horizontal image balance did not align bottom edges to one line.", result);
  assert(result.restoredSelection.length >= 2, "Horizontal balance did not restore visible selected images from the iframe.", result);
  assert(!result.toast.includes("Выделите рамкой"), "Horizontal balance still complains about selection while selected image frames are visible.", result);
  assert(new Set(result.heights.map((height) => Math.round(height))).size === 1, "Horizontal image balance did not sync image heights in state.", result);
  return result;
}

async function testAdminImageRowInsertions() {
  const page = await openCdpPage(ADMIN_URL);
  await openServicesInAdmin(page);
  const existingServiceButton = await testExistingServiceButtonHandles(page);
  await page.send("Page.reload");
  await openServicesInAdmin(page);
  await keepOnlyServiceImageRow(page);
  const horizontalBalance = await testHorizontalImageBalanceEdges(page);
  await page.send("Page.reload");
  await openServicesInAdmin(page);
  await keepOnlyServiceImageRow(page);
  const rightMouseImageDrag = await testRightMouseImageDrag(page);
  await page.send("Page.reload");
  await openServicesInAdmin(page);
  await keepOnlyServiceImageRow(page);
  await new Promise((resolve) => setTimeout(resolve, 700));
  const before = await adminImageRects(page);
  await clickAdminFrameBlock(page, 1);
  await new Promise((resolve) => setTimeout(resolve, 200));
  await page.evaluate(`document.querySelector('[data-add-block="buttons"]').click() || true`);
  await page.waitFor(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame && frame.contentDocument;
    return !!(doc && doc.querySelector('[data-preview-index="3"].seo-builder-block--buttons'));
  })()`, 10000);
  await new Promise((resolve) => setTimeout(resolve, 250));
  const afterButton = await adminImageRects(page);
  const orderAfterButton = adminOrder(afterButton);
  assert(orderAfterButton.join(",") === "image,image,image,buttons", "Button inserted inside the image row.", { before, afterButton, orderAfterButton });
  assert(before.slice(0, 3).every((item, index) => item.top === afterButton[index].top && item.left === afterButton[index].left), "Image row moved after button insertion.", { before, afterButton });
  const buttonRect = afterButton[3];
  const imageRowBottom = Math.max(...afterButton.slice(0, 3).map((item) => item.bottom));
  assert(buttonRect.bottom - buttonRect.top <= 110, "Button block is too tall for comfortable moving.", buttonRect);
  assert(buttonRect.top <= imageRowBottom + 80, "Button block landed too far below the visible image row.", { imageRowBottom, buttonRect, afterButton });
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const block = doc.querySelector('[data-preview-index="3"].seo-builder-block--buttons');
    const rect = block.getBoundingClientRect();
    setInsertPointFromClient(doc, rect.left + rect.width / 2, rect.bottom + 32);
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 200));
  await page.evaluate(`document.querySelector('[data-add-block="text"]').click() || true`);
  await new Promise((resolve) => setTimeout(resolve, 900));
  const afterTextBelowButton = await adminImageRects(page);
  const orderAfterTextBelowButton = adminOrder(afterTextBelowButton);
  assert(orderAfterTextBelowButton.join(",") === "image,image,image,buttons,text", "Text inserted below a placed button should not jump above it.", { afterButton, afterTextBelowButton, orderAfterTextBelowButton });
  assert(afterTextBelowButton[3].top === buttonRect.top && afterTextBelowButton[3].left === buttonRect.left, "Adding text below the button moved the existing button.", { buttonRect, afterTextBelowButton });
  const insertedTextFocus = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="4"] [data-block-field="text"]');
    if (!editable) return { missing: true };
    const wasFocused = doc.activeElement === editable;
    editable.textContent = 'Text below button can be typed';
    editable.dispatchEvent(new frame.contentWindow.InputEvent('input', { bubbles: true, inputType: 'insertText', data: editable.textContent }));
    return {
      missing: false,
      wasFocused,
      isEditable: editable.isContentEditable,
      domText: editable.innerText.trim(),
      stateText: state.builderBlocks[4]?.text || ''
    };
  })())`));
  assert(!insertedTextFocus.missing && insertedTextFocus.isEditable, "Inserted text block is not editable in the real editor.", insertedTextFocus);
  assert(insertedTextFocus.wasFocused, "Inserted text block did not receive focus after insertion.", insertedTextFocus);
  assert(insertedTextFocus.stateText.includes("Text below button can be typed"), "Inserted text block does not accept typed text.", insertedTextFocus);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const button = doc.querySelector('[data-preview-index="3"] [data-button-field="label"]');
    selectPreviewButton(button);
    revealRealBlock(3, { instant: true });
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 300));
  const revealAfterInsert = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const block = doc.querySelector('[data-preview-index="3"]');
    const rect = block.getBoundingClientRect();
    const frameRect = frame.getBoundingClientRect();
    const scale = frameRect.width / frame.offsetWidth;
    const viewportTop = frameRect.top + rect.top * scale;
    const viewportBottom = frameRect.top + rect.bottom * scale;
    return {
      viewportTop: Math.round(viewportTop),
      viewportBottom: Math.round(viewportBottom),
      windowHeight: window.innerHeight,
      hasRevealButton: !!doc.querySelector('.reveal-button-block'),
      hasOpenButton: !!doc.querySelector('.open-button-url'),
      hasUrlField: !!doc.querySelector('#buttonPanelUrl')
    };
  })())`));
  assert(!revealAfterInsert.hasRevealButton, "Button panel should not show the redundant show-on-page control.", revealAfterInsert);
  assert(revealAfterInsert.hasOpenButton && revealAfterInsert.hasUrlField, "Button panel lost useful URL controls.", revealAfterInsert);
  assert(revealAfterInsert.viewportTop >= 80 && revealAfterInsert.viewportTop <= revealAfterInsert.windowHeight - 160, "Inserted button was not revealed in the visible viewport.", revealAfterInsert);
  await page.evaluate(`window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'auto' })`);
  await new Promise((resolve) => setTimeout(resolve, 200));
  await page.evaluate(`revealSelectedButtonBlock()`);
  await new Promise((resolve) => setTimeout(resolve, 700));
  const revealAfterClick = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const block = doc.querySelector('[data-preview-index="3"]');
    const rect = block.getBoundingClientRect();
    const frameRect = frame.getBoundingClientRect();
    const scale = frameRect.width / frame.offsetWidth;
    const viewportTop = frameRect.top + rect.top * scale;
    return { viewportTop: Math.round(viewportTop), windowHeight: window.innerHeight };
  })())`));
  assert(revealAfterClick.viewportTop >= 80 && revealAfterClick.viewportTop <= revealAfterClick.windowHeight - 160, "Show-on-page control did not reveal the inserted button.", revealAfterClick);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const button = doc.querySelector('[data-preview-index="3"] [data-button-field="label"]');
    const panel = doc.querySelector('#buttonLinkPanel');
    const url = panel?.querySelector('#buttonPanelUrl');
    const bg = panel?.querySelector('#buttonPanelBgColor');
    const text = panel?.querySelector('#buttonPanelTextColor');
    if (!button || !panel || !url || !bg || !text) throw new Error('button edit panel was not opened');
    button.textContent = 'Заказать аудит';
    button.dispatchEvent(new Event('input', { bubbles: true }));
    url.value = '/ru/about/';
    url.dispatchEvent(new Event('input', { bubbles: true }));
    bg.value = '#ee1244';
    bg.dispatchEvent(new Event('input', { bubbles: true }));
    bg.dispatchEvent(new Event('change', { bubbles: true }));
    text.value = '#ffffff';
    text.dispatchEvent(new Event('input', { bubbles: true }));
    text.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const buttonEdit = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const button = doc.querySelector('[data-preview-index="3"] [data-button-field="label"]');
    const style = getComputedStyle(button);
    return {
      label: button.textContent.trim(),
      href: button.getAttribute('href'),
      background: style.backgroundColor,
      color: style.color,
      builderLabel: state.builderBlocks[3]?.buttons?.[0]?.label || '',
      builderUrl: state.builderBlocks[3]?.buttons?.[0]?.url || '',
      builderBg: state.builderBlocks[3]?.buttonBgColor || '',
      builderText: state.builderBlocks[3]?.buttonTextColor || ''
    };
  })())`));
  assert(buttonEdit.label === "Заказать аудит", "Button label did not update from the edit panel.", buttonEdit);
  assert(buttonEdit.href === "/ru/about/", "Button URL did not update from the edit panel.", buttonEdit);
  assert(buttonEdit.background === "rgb(238, 18, 68)", "Button background color did not apply.", buttonEdit);
  assert(buttonEdit.color === "rgb(255, 255, 255)", "Button text color did not apply.", buttonEdit);
  assert(buttonEdit.builderLabel === "Заказать аудит" && buttonEdit.builderUrl === "/ru/about/", "Button panel did not sync back to the inspector fields.", buttonEdit);
  assert(buttonEdit.builderBg === "#ee1244" && buttonEdit.builderText === "#ffffff", "Button colors did not sync back to the inspector fields.", buttonEdit);
  const buttonResizeMove = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    let block = doc.querySelector('[data-preview-index="3"]');
    let button = block.querySelector('.seo-cta');
    const startButton = button.getBoundingClientRect();
    let right = block.querySelector('[data-button-resize="right"]');
    let bottom = block.querySelector('[data-button-resize="bottom"]');
    let move = block.querySelector('[data-button-move]');
    const dispatch = (target, type, x, y, pointerId) => target.dispatchEvent(new win.PointerEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0, pointerId, pointerType: 'mouse' }));
    let r = right.getBoundingClientRect();
    dispatch(right, 'pointerdown', r.left + 4, r.top + 10, 31);
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: r.left + 184, clientY: r.top + 10, button: 0, pointerId: 31, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: r.left + 184, clientY: r.top + 10, button: 0, pointerId: 31, pointerType: 'mouse' }));
    block = doc.querySelector('[data-preview-index="3"]');
    button = block.querySelector('.seo-cta');
    bottom = block.querySelector('[data-button-resize="bottom"]');
    r = bottom.getBoundingClientRect();
    dispatch(bottom, 'pointerdown', r.left + 10, r.top + 4, 32);
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: r.left + 10, clientY: r.top + 44, button: 0, pointerId: 32, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: r.left + 10, clientY: r.top + 44, button: 0, pointerId: 32, pointerType: 'mouse' }));
    block = doc.querySelector('[data-preview-index="3"]');
    button = block.querySelector('.seo-cta');
    move = block.querySelector('[data-button-move]');
    const afterResize = button.getBoundingClientRect();
    r = move.getBoundingClientRect();
    dispatch(move, 'pointerdown', r.left + 10, r.top + 5, 33);
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: r.left + 130, clientY: r.top - 45, button: 0, pointerId: 33, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: r.left + 130, clientY: r.top - 45, button: 0, pointerId: 33, pointerType: 'mouse' }));
    block = doc.querySelector('[data-preview-index="3"]');
    button = block.querySelector('.seo-cta');
    const afterMove = button.getBoundingClientRect();
    return {
      startWidth: Math.round(startButton.width),
      startHeight: Math.round(startButton.height),
      resizedWidth: Math.round(afterResize.width),
      resizedHeight: Math.round(afterResize.height),
      movedLeftDelta: Math.round(afterMove.left - afterResize.left),
      movedTopDelta: Math.round(afterMove.top - afterResize.top),
      inspectorMode: document.querySelector('#builderList select[data-field="buttonWidthMode"]').value,
      inspectorWidth: Number(document.querySelector('#builderList input[data-field="buttonPixelWidth"]').value),
      inspectorHeight: Number(document.querySelector('#builderList input[data-field="buttonPixelHeight"]').value),
      hasMove: !!move,
      hasRight: !!right,
      hasBottom: !!bottom
    };
  })())`));
  assert(buttonResizeMove.hasMove && buttonResizeMove.hasRight && buttonResizeMove.hasBottom, "Button move/resize handles are missing.", buttonResizeMove);
  assert(buttonResizeMove.resizedWidth >= buttonResizeMove.startWidth + 120, "Button right edge resize did not increase width.", buttonResizeMove);
  assert(buttonResizeMove.resizedHeight >= buttonResizeMove.startHeight + 28, "Button bottom edge resize did not increase height.", buttonResizeMove);
  assert(Math.abs(buttonResizeMove.movedLeftDelta) >= 80 || Math.abs(buttonResizeMove.movedTopDelta) >= 30, "Button move handle did not move the button.", buttonResizeMove);
  assert(buttonResizeMove.inspectorMode === "custom" && buttonResizeMove.inspectorWidth >= buttonResizeMove.resizedWidth - 3 && buttonResizeMove.inspectorHeight >= buttonResizeMove.resizedHeight - 3, "Button resize did not sync to inspector fields.", buttonResizeMove);
  const openedUrl = await page.evaluate(`(() => {
    window.__openedButtonUrl = '';
    window.open = (url) => { window.__openedButtonUrl = url; return null; };
    openSelectedButtonUrl();
    return window.__openedButtonUrl;
  })()`);
  assert(openedUrl === "/ru/about/", "Button URL check control did not open the configured URL.", { openedUrl });
  await page.evaluate(`(() => {
    state.builderBlocks[3].offsetX = 0;
    state.builderBlocks[3].offsetY = 0;
    renderBuilder();
    applyDraftToRealFrame();
    document.querySelector('#builderList input[data-field="buttonFontSize"]').value = '22';
    document.querySelector('#builderList input[data-field="buttonFontSize"]').dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('#builderList select[data-field="buttonWidthMode"]').value = 'custom';
    document.querySelector('#builderList select[data-field="buttonWidthMode"]').dispatchEvent(new Event('change', { bubbles: true }));
    document.querySelector('#builderList input[data-field="buttonPixelWidth"]').value = '320';
    document.querySelector('#builderList input[data-field="buttonPixelWidth"]').dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('#builderList select[data-field="buttonAlign"]').value = 'center';
    document.querySelector('#builderList select[data-field="buttonAlign"]').dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const buttonSizing = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const block = doc.querySelector('[data-preview-index="3"]');
    const container = block.querySelector('.seo-builder-buttons');
    const button = block.querySelector('.seo-cta');
    const work = doc.querySelector('.seo-hero-content__inner').getBoundingClientRect();
    const rect = button.getBoundingClientRect();
    return {
      fontSize: getComputedStyle(button).fontSize,
      width: Math.round(rect.width),
      centerX: Math.round(rect.left + rect.width / 2),
      workCenterX: Math.round(work.left + work.width / 2),
      justifySelf: getComputedStyle(block).justifySelf,
      justifyContent: getComputedStyle(container).justifyContent
    };
  })())`));
  assert(buttonSizing.fontSize === "22px", "Button font size control did not apply.", buttonSizing);
  assert(Math.abs(buttonSizing.width - 320) <= 2, "Button custom width did not apply.", buttonSizing);
  assert(buttonSizing.justifyContent === "center", "Button center alignment did not apply.", buttonSizing);
  assert(Math.abs(buttonSizing.centerX - buttonSizing.workCenterX) <= 2, "Compact button block did not move to the center.", buttonSizing);
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const block = doc.querySelector('[data-preview-index="3"]');
    const rect = block.getBoundingClientRect();
    const x = rect.left + 20;
    const y = rect.top + 20;
    block.dispatchEvent(new win.PointerEvent('pointerdown', { bubbles: true, clientX: x, clientY: y, button: 0, pointerId: 2, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointermove', { bubbles: true, clientX: x, clientY: y - 850, button: 0, pointerId: 2, pointerType: 'mouse' }));
    doc.dispatchEvent(new win.PointerEvent('pointerup', { bubbles: true, clientX: x, clientY: y - 850, button: 0, pointerId: 2, pointerType: 'mouse' }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const afterButtonDrag = await adminImageRects(page);
  const draggedButton = afterButtonDrag[3];
  const intersectsImages = afterButtonDrag.slice(0, 3).some((image) => (
    draggedButton.left <= image.right &&
    draggedButton.right >= image.left &&
    draggedButton.top <= image.bottom &&
    draggedButton.bottom >= image.top
  ));
  assert(!intersectsImages, "Button block was allowed to overlap the image row while dragging.", { buttonRect, afterButtonDrag });

  await page.send("Page.reload");
  await openServicesInAdmin(page);
  await keepOnlyServiceImageRow(page);
  await new Promise((resolve) => setTimeout(resolve, 700));
  const beforeText = await adminImageRects(page);
  await clickAdminFrameBlock(page, 0);
  await new Promise((resolve) => setTimeout(resolve, 200));
  await page.evaluate(`document.querySelector('[data-add-block="text"]').click() || true`);
  await page.waitFor(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame && frame.contentDocument;
    return !!(doc && doc.querySelector('[data-preview-index="3"].seo-builder-block--text'));
  })()`, 10000);
  await new Promise((resolve) => setTimeout(resolve, 250));
  const afterText = await adminImageRects(page);
  const orderAfterText = adminOrder(afterText);
  assert(orderAfterText.join(",") === "image,image,image,text", "Text inserted inside the image row.", { beforeText, afterText, orderAfterText });
  assert(beforeText.slice(0, 3).every((item, index) => item.top === afterText[index].top && item.left === afterText[index].left), "Image row moved after text insertion.", { beforeText, afterText });
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="3"] [data-block-field="text"]');
    editable.textContent = 'Текстовый блок с анкором для проверки.';
    editable.dispatchEvent(new frame.contentWindow.InputEvent('input', { bubbles: true, inputType: 'insertText', data: editable.textContent }));
    const textNode = editable.firstChild;
    const start = editable.textContent.indexOf('анкором');
    const range = doc.createRange();
    range.setStart(textNode, start);
    range.setEnd(textNode, start + 'анкором'.length);
    const selection = doc.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    doc.dispatchEvent(new Event('selectionchange'));
    const toolbarLink = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link]');
    if (!toolbarLink) throw new Error('Selection toolbar link button did not appear');
    toolbarLink.click();
    const input = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
    if (!input) throw new Error('Selection toolbar link input did not appear');
    input.focus();
    const paste = new ClipboardEvent('paste', { bubbles: true, cancelable: true });
    Object.defineProperty(paste, 'clipboardData', { value: { getData: () => '/ru/about/' } });
    input.dispatchEvent(paste);
    if (input.value !== '/ru/about/') throw new Error('Selection toolbar paste did not fill the link input');
    return true;
  })()`);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const ok = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-submit]');
    if (!ok) throw new Error('Selection toolbar OK button did not appear');
    ok.click();
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 600));
  const textLink = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const link = doc.querySelector('[data-preview-index="3"] .seo-builder-text a[href="/ru/about/"]');
    const textarea = document.querySelector('#builderList textarea[data-field="text"]');
    return {
      text: doc.querySelector('[data-preview-index="3"] .seo-builder-text').innerText.trim(),
      linkText: link ? link.textContent.trim() : '',
      href: link ? link.getAttribute('href') : '',
      raw: textarea ? textarea.value : ''
    };
  })())`));
  assert(textLink.text.includes("Текстовый блок"), "Text block content did not update from the real editor.", textLink);
  assert(textLink.linkText === "анкором" && textLink.href === "/ru/about/", "Selected text was not converted into a link.", textLink);
  assert(textLink.raw.includes("[анкором](/ru/about/)"), "Anchor link was not persisted as markdown in the inspector.", textLink);
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="3"] [data-block-field="text"]');
    editable.textContent = 'alpha target beta target gamma';
    editable.dispatchEvent(new frame.contentWindow.InputEvent('input', { bubbles: true, inputType: 'insertText', data: editable.textContent }));
    const textNode = editable.firstChild;
    const start = editable.textContent.lastIndexOf('target');
    const range = doc.createRange();
    range.setStart(textNode, start);
    range.setEnd(textNode, start + 'target'.length);
    const selection = doc.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    doc.dispatchEvent(new Event('selectionchange'));
    const toolbarLink = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link]');
    if (!toolbarLink) throw new Error('Repeated-word link toolbar did not appear');
    toolbarLink.click();
    const input = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
    if (!input) throw new Error('Repeated-word link input did not appear');
    input.value = '/ru/faq/';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-submit]').click();
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const repeatedLink = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const editable = doc.querySelector('[data-preview-index="3"] .seo-builder-text');
    const links = Array.from(editable.querySelectorAll('a')).map((link) => ({ text: link.textContent, href: link.getAttribute('href') }));
    const textarea = document.querySelector('#builderList textarea[data-field="text"]');
    return {
      text: editable.innerText.trim(),
      html: editable.innerHTML,
      links,
      raw: textarea ? textarea.value : ''
    };
  })())`));
  assert(repeatedLink.raw === "alpha target beta [target](/ru/faq/) gamma", "Link was applied to the wrong repeated word.", repeatedLink);
  assert(repeatedLink.links.length === 1 && repeatedLink.links[0].text === "target" && repeatedLink.links[0].href === "/ru/faq/", "Repeated-word link did not render on the selected target.", repeatedLink);
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    state.builderBlocks[3].text = '-\\n\\nЛучше масштабирование:\\n\\nфинал';
    renderBuilder();
    applyDraftToRealFrame();
    const editable = doc.querySelector('[data-preview-index="3"] [data-block-field="text"]');
    const text = editable.innerText || editable.textContent || '';
    const start = text.indexOf('Лучше');
    if (start < 0) throw new Error('word after standalone dash not rendered');
    const walker = doc.createTreeWalker(editable, NodeFilter.SHOW_TEXT);
    let node = walker.nextNode();
    let offset = start;
    while (node && offset > node.textContent.length) {
      offset -= node.textContent.length;
      node = walker.nextNode();
    }
    if (!node) throw new Error('word text node not found after dash');
    const range = doc.createRange();
    range.setStart(node, offset);
    range.setEnd(node, offset + 2);
    const selection = doc.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    doc.dispatchEvent(new Event('selectionchange'));
    const toolbarLink = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link]');
    if (!toolbarLink) throw new Error('Dash-adjacent link toolbar did not appear');
    toolbarLink.click();
    const input = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
    if (!input) throw new Error('Dash-adjacent link input did not appear');
    input.value = 'https://kwork.com/';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-submit]').click();
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const dashAdjacentLink = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const editable = doc.querySelector('[data-preview-index="3"] .seo-builder-text');
    const link = editable.querySelector('a[href="https://kwork.com/"]');
    const textarea = document.querySelector('#builderList textarea[data-field="text"]');
    return {
      text: editable.innerText.trim(),
      linkText: link ? link.textContent.trim() : '',
      raw: textarea ? textarea.value : ''
    };
  })())`));
  assert(dashAdjacentLink.raw === "-\n\n[Лучше](https://kwork.com/) масштабирование:\n\nфинал", "Dash before selected word was captured or word-prefix link was not expanded.", dashAdjacentLink);
  assert(dashAdjacentLink.linkText === "Лучше", "Dash-adjacent link did not render on the full selected word.", dashAdjacentLink);
  await page.evaluate(`(() => {
    document.querySelector('#builderList input[data-field="fontSize"]').value = '21';
    document.querySelector('#builderList input[data-field="fontSize"]').dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 400));
  const textFontSize = await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    return getComputedStyle(doc.querySelector('[data-preview-index="3"] .seo-builder-text')).fontSize;
  })()`);
  assert(textFontSize === "21px", "Text font size control did not apply.", { textFontSize });
  page.close();
  return { existingServiceButton, horizontalBalance, rightMouseImageDrag, orderAfterButton, orderAfterTextBelowButton, orderAfterText };
}

async function testAdminWrapBlock() {
  const page = await openCdpPage(ADMIN_URL);
  await openServicesInAdmin(page);
  await new Promise((resolve) => setTimeout(resolve, 700));
  await page.evaluate(`document.querySelector('[data-add-block="wrap"]').click() || true`);
  await new Promise((resolve) => setTimeout(resolve, 400));
  await page.evaluate(`(() => {
    const image = document.querySelector('#builderList input[data-field="image"]');
    const imageLink = document.querySelector('#builderList input[data-field="imageLink"]');
    const text = document.querySelector('#builderList textarea[data-field="text"]');
    const side = document.querySelector('#builderList select[data-field="imageSide"]');
    image.value = '/uploads/301-redirect-pagerank-1780874044.png';
    image.dispatchEvent(new Event('input', { bubbles: true }));
    imageLink.value = '/services/';
    imageLink.dispatchEvent(new Event('input', { bubbles: true }));
    text.value = 'Long wrap text. '.repeat(60);
    text.dispatchEvent(new Event('input', { bubbles: true }));
    side.value = 'left';
    side.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 600));
  const left = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const block = doc.querySelector('.seo-builder-block--wrap');
    const media = block && block.querySelector('.seo-builder-wrap-media');
    const link = block && block.querySelector('.seo-builder-image-link');
    return {
      exists: !!block,
      media: !!media,
      href: link ? link.getAttribute('href') : '',
      float: media ? getComputedStyle(media).float : ''
    };
  })())`));
  await page.evaluate(`(() => {
    const side = document.querySelector('#builderList select[data-field="imageSide"]');
    side.value = 'right';
    side.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 600));
  const right = await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const block = doc.querySelector('.seo-builder-block--wrap');
    const media = block && block.querySelector('.seo-builder-wrap-media');
    return media ? getComputedStyle(media).float : '';
  })()`);
  assert(left.exists && left.media && left.float === "left", "Wrap block left mode is not floating left.", { left });
  assert(right === "right", "Wrap block right mode is not floating right.", { right });
  page.close();
  return { left, right };
}

function fullStressBlocks() {
  return [
    {
      type: "text",
      width: "full",
      enabled: true,
      title: "Stress Text",
      text: "Первый блок: слово жирное и слово анкор должны форматироваться выделением.",
      fontSize: 0,
      textAlign: "left",
    },
    {
      type: "image",
      width: "full",
      enabled: true,
      image: "/uploads/301-redirect-pagerank-1780874044.png",
      imageLink: "/ru/faq/",
      alt: "Stress linked image",
      caption: "Кликабельная картинка",
      imagePixelWidth: 360,
      imagePixelHeight: 220,
      imageOffsetX: 0,
      imageOffsetY: 0,
    },
    {
      type: "buttons",
      width: "full",
      enabled: true,
      title: "",
      text: "",
      buttons: [{ label: "Small CTA", url: "https://kwork.com/" }],
      buttonWidthMode: "custom",
      buttonPixelWidth: 190,
      buttonPixelHeight: 48,
      buttonFontSize: 15,
      buttonRadius: 6,
      buttonAlign: "left",
      buttonBgColor: "#1f86b8",
      buttonTextColor: "#ffffff",
      offsetX: 0,
      offsetY: 0,
    },
    {
      type: "buttons",
      width: "full",
      enabled: true,
      title: "",
      text: "",
      buttons: [{ label: "Wide CTA", url: "/about/" }],
      buttonWidthMode: "custom",
      buttonPixelWidth: 520,
      buttonPixelHeight: 72,
      buttonFontSize: 22,
      buttonRadius: 18,
      buttonAlign: "center",
      buttonBgColor: "#ee1244",
      buttonTextColor: "#ffffff",
      offsetX: 0,
      offsetY: 0,
    },
    {
      type: "banner",
      width: "full",
      enabled: true,
      title: "Stress Banner",
      text: "Баннер с картинкой, текстом и кнопкой.",
      image: "/uploads/link-building-strategy-1780874114.png",
      imageLink: "https://example.com/banner",
      alt: "Stress banner image",
      caption: "",
      buttons: [{ label: "Banner CTA", url: "https://example.com/banner-button" }],
      buttonWidthMode: "custom",
      buttonPixelWidth: 260,
      buttonPixelHeight: 56,
      buttonFontSize: 18,
      buttonRadius: 10,
      buttonAlign: "left",
      buttonBgColor: "#2a80ad",
      buttonTextColor: "#ffffff",
    },
    {
      type: "wrap",
      width: "full",
      enabled: true,
      title: "Stress Wrap",
      text: "Текст обтекает картинку слева. ".repeat(18),
      image: "/uploads/доступ-1780874177.png",
      imageLink: "/ru/services/",
      alt: "Stress wrap image",
      caption: "",
      imageSide: "left",
      fontSize: 17,
      textAlign: "left",
    },
    {
      type: "buttons",
      width: "full",
      enabled: true,
      title: "",
      text: "",
      buttons: [{ label: "Square Huge CTA", url: "#square" }],
      buttonWidthMode: "custom",
      buttonPixelWidth: 900,
      buttonPixelHeight: 60,
      buttonFontSize: 20,
      buttonRadius: 0,
      buttonAlign: "right",
      buttonBgColor: "#135f5b",
      buttonTextColor: "#ffffff",
      offsetX: 0,
      offsetY: 0,
    },
    {
      type: "text",
      width: "full",
      enabled: true,
      title: "Right Align Stress",
      text: "Правое выравнивание должно сохраняться и не ломать адаптив.",
      fontSize: 18,
      textAlign: "right",
    },
    {
      type: "buttons",
      width: "full",
      enabled: true,
      title: "",
      text: "",
      buttons: [{ label: "Default Radius CTA", url: "#default-radius" }],
      buttonWidthMode: "custom",
      buttonPixelWidth: 240,
      buttonPixelHeight: 50,
      buttonFontSize: 16,
      buttonRadius: "",
      buttonAlign: "left",
      buttonBgColor: "#2a80ad",
      buttonTextColor: "#ffffff",
      offsetX: 0,
      offsetY: 0,
    },
    {
      type: "grid",
      width: "full",
      enabled: true,
      title: "Grid Align Stress",
      text: "Общий текст сетки.",
      fontSize: 19,
      textAlign: "center",
      items: [
        {
          title: "Long Grid Title WithoutSpacesToStressWrapping",
          text: "Текст карточки с выравниванием по центру.",
          image: "/uploads/301-redirect-pagerank-1780874044.png",
        },
      ],
    },
  ];
}

async function ensureFullStressPage() {
  const exists = await adminApi(`/api/page?path=${encodeURIComponent(FULL_STRESS_PATH)}`).then(() => true).catch(() => false);
  if (!exists) {
    await adminApi("/api/page/create", {
      method: "POST",
      body: JSON.stringify({
        section: "admin-test",
        slug: "full-editor-stress",
        title: "Full Editor Stress",
        languages: ["ru"],
        translationKey: "admin-test-full-editor-stress",
      }),
    });
  }
  await adminApi("/api/page/save", {
    method: "POST",
    body: JSON.stringify({
      path: FULL_STRESS_PATH,
      frontmatter: {
        title: "Full Editor Stress",
        description: "Temporary full editor regression page.",
        slug: "full-editor-stress",
        translationKey: "admin-test-full-editor-stress",
        draft: false,
        visibility: "site",
        builderJson: JSON.stringify(fullStressBlocks()),
      },
      body: "Полигон для проверки админского визуального редактора.",
    }),
  });
}

async function selectFrameText(page, blockIndex, needle) {
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="${blockIndex}"] [data-block-field="text"]');
    if (!editable) throw new Error('editable text not found: ${blockIndex}');
    const text = editable.innerText || editable.textContent || '';
    const start = text.indexOf('${needle}');
    if (start < 0) throw new Error('selection text not found: ${needle}');
    const walker = doc.createTreeWalker(editable, NodeFilter.SHOW_TEXT);
    let node = walker.nextNode();
    let offset = start;
    while (node && offset > node.textContent.length) {
      offset -= node.textContent.length;
      node = walker.nextNode();
    }
    if (!node) throw new Error('selection node not found');
    const startNode = node;
    const startOffset = offset;
    let endNode = node;
    let endOffset = offset + '${needle}'.length;
    while (endNode && endOffset > endNode.textContent.length) {
      endOffset -= endNode.textContent.length;
      endNode = walker.nextNode();
    }
    if (!endNode) throw new Error('selection end node not found');
    const range = doc.createRange();
    range.setStart(startNode, startOffset);
    range.setEnd(endNode, endOffset);
    const selection = doc.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    doc.dispatchEvent(new Event('selectionchange'));
    window.captureTextSelection(doc);
    editable.focus();
    return true;
  })()`);
}

async function selectFrameTextAt(page, blockIndex, needle, options = {}) {
  const occurrence = options.occurrence || "first";
  const length = options.length || needle.length;
  await page.evaluate(`(() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="${blockIndex}"] [data-block-field="text"]');
    if (!editable) throw new Error('editable text not found: ${blockIndex}');
    const text = editable.innerText || editable.textContent || '';
    const needle = ${JSON.stringify(needle)};
    const occurrence = ${JSON.stringify(occurrence)};
    const start = occurrence === 'last' ? text.lastIndexOf(needle) : text.indexOf(needle);
    if (start < 0) throw new Error('selection text not found: ' + needle);
    const walker = doc.createTreeWalker(editable, NodeFilter.SHOW_TEXT);
    let node = walker.nextNode();
    let offset = start;
    while (node && offset > node.textContent.length) {
      offset -= node.textContent.length;
      node = walker.nextNode();
    }
    if (!node) throw new Error('selection node not found');
    const range = doc.createRange();
    range.setStart(node, offset);
    let endNode = node;
    let endOffset = offset + ${Number(length)};
    while (endNode && endOffset > endNode.textContent.length) {
      endOffset -= endNode.textContent.length;
      endNode = walker.nextNode();
    }
    if (!endNode) throw new Error('selection end node not found');
    range.setEnd(endNode, endOffset);
    const selection = doc.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    doc.dispatchEvent(new Event('selectionchange'));
    window.captureTextSelection(doc);
    editable.focus();
    return true;
  })()`);
}

async function clickFrameElement(page, selector) {
  if (selector.includes("#textSelectionToolbar")) {
    return JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const doc = document.querySelector('#realPageFrame').contentDocument;
      const el = doc.querySelector(${JSON.stringify(selector)});
      if (!el) throw new Error('frame toolbar element not found: ${selector}');
      state.lastTextToolbarAction = null;
      for (const type of ['pointerdown', 'mousedown', 'mouseup', 'click']) {
        const Ctor = type === 'pointerdown' && doc.defaultView.PointerEvent ? doc.defaultView.PointerEvent : doc.defaultView.MouseEvent;
        el.dispatchEvent(new Ctor(type, { bubbles: true, cancelable: true, button: 0, buttons: type.endsWith('down') ? 1 : 0, clientX: 1, clientY: 1 }));
      }
      state.lastTextToolbarAction = null;
      el.click();
      return { mode: 'iframe-dispatch-direct', selector: ${JSON.stringify(selector)} };
    })())`));
  }
  const point = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    frame.scrollIntoView({ block: 'start', inline: 'center' });
    const doc = frame.contentDocument;
    const el = doc.querySelector(${JSON.stringify(selector)});
    if (!el) throw new Error('frame element not found: ${selector}');
    const frameRect = frame.getBoundingClientRect();
    const rect = el.getBoundingClientRect();
    const x = Math.round(frameRect.left + rect.left + rect.width / 2);
    const y = Math.round(frameRect.top + rect.top + rect.height / 2);
    const hit = doc.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
    const parentHit = document.elementFromPoint(x, y);
    return {
      x,
      y,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      hitInside: !!hit && (hit === el || el.contains(hit)),
      parentHitInsideFrame: parentHit === frame,
      parentHit: parentHit ? { tag: parentHit.tagName, id: parentHit.id || '', className: String(parentHit.className || '') } : null,
      hit: hit ? { tag: hit.tagName, className: String(hit.className || '') } : null
    };
  })())`));
  assert(point.hitInside, `Frame click target is intercepted: ${selector}`, point);
  assert(point.parentHitInsideFrame, `Parent page intercepts frame click target: ${selector}`, point);
  assert(point.x >= 0 && point.x <= point.viewport.width && point.y >= 0 && point.y <= point.viewport.height, `Frame click target is outside the viewport: ${selector}`, point);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    doc.defaultView.__lastFramePointer = null;
    doc.addEventListener('pointerdown', (event) => {
      doc.defaultView.__lastFramePointer = {
        tag: event.target?.tagName || '',
        className: String(event.target?.className || ''),
        id: event.target?.id || '',
        text: event.target?.textContent || '',
        inToolbar: !!event.target?.closest?.('#textSelectionToolbar')
      };
    }, { once: true, capture: true });
    return true;
  })()`);
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: point.x, y: point.y, button: "none" });
  await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: point.x, y: point.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 80));
  await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: point.x, y: point.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 220));
  let eventDebug = JSON.parse(await page.evaluate(`JSON.stringify(document.querySelector('#realPageFrame').contentDocument.defaultView.__lastFramePointer || null)`));
  let mode = "cdp";
  if (!eventDebug?.inToolbar) {
    const stillExists = await page.evaluate(`!!document.querySelector('#realPageFrame').contentDocument.querySelector(${JSON.stringify(selector)})`);
    if (!stillExists) return { ...point, mode: "cdp-removed" };
    mode = "iframe-dispatch";
    eventDebug = JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const doc = document.querySelector('#realPageFrame').contentDocument;
      const el = doc.querySelector(${JSON.stringify(selector)});
      if (!el) throw new Error('frame element not found for dispatch: ${selector}');
      doc.defaultView.__lastFramePointer = null;
      for (const type of ['pointerdown', 'mousedown', 'mouseup', 'click']) {
        const Ctor = type === 'pointerdown' && doc.defaultView.PointerEvent ? doc.defaultView.PointerEvent : doc.defaultView.MouseEvent;
        el.dispatchEvent(new Ctor(type, { bubbles: true, cancelable: true, button: 0, buttons: type.endsWith('down') ? 1 : 0, clientX: 1, clientY: 1 }));
      }
      return doc.defaultView.__lastFramePointer || { inToolbar: true, fallback: true };
    })())`));
  }
  assert(eventDebug?.inToolbar, `Frame pointerdown did not reach toolbar: ${selector}`, { point, eventDebug });
  return { ...point, mode };
}

async function setPhysicalFormatText(page, text) {
  await page.evaluate(`(() => {
    state.builderBlocks = [{
      type: 'text',
      width: 'full',
      enabled: true,
      title: 'Physical Format Matrix',
      text: ${JSON.stringify(text)},
      fontSize: 0,
      textAlign: 'left',
      image: '',
      imageLink: '',
      alt: '',
      caption: '',
      imageSide: 'right',
      offsetX: 0,
      offsetY: 0,
      pixelWidth: 0,
      buttonFontSize: 0,
      buttonPixelWidth: 0,
      buttonPixelHeight: 0,
      buttonRadius: '',
      buttonWidthMode: 'auto',
      buttonAlign: 'left',
      buttonBgColor: '',
      buttonTextColor: '',
      imageOffsetX: 0,
      imageOffsetY: 0,
      imagePixelWidth: 0,
      imagePixelHeight: 0,
      buttons: [],
      items: []
    }];
    state.selectedBlockIndex = 0;
    renderBuilder();
    applyDraftToRealFrame();
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 250));
}

async function textFormatMetrics(page) {
  return JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const editable = doc.querySelector('[data-preview-index="0"] [data-block-field="text"]');
    return {
      raw: state.builderBlocks[0]?.text || '',
      innerText: editable ? editable.innerText : '',
      html: editable ? editable.innerHTML : '',
      strongTexts: Array.from(editable?.querySelectorAll('strong') || []).map((el) => el.textContent.trim()),
      emTexts: Array.from(editable?.querySelectorAll('em') || []).map((el) => el.textContent.trim()),
      links: Array.from(editable?.querySelectorAll('a') || []).map((el) => ({ text: el.textContent.trim(), href: el.getAttribute('href') })),
    };
  })())`));
}

async function physicalBold(page, needle, options = {}) {
  await selectFrameTextAt(page, 0, needle, options);
  const beforeRaw = await page.evaluate(`state.builderBlocks[0]?.text || ''`);
  await clickFrameElement(page, "#textSelectionToolbar [data-text-toolbar-bold]");
  const debug = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const doc = document.querySelector('#realPageFrame')?.contentDocument;
    return {
      beforeRaw: ${JSON.stringify("")},
      afterRaw: state.builderBlocks[0]?.text || '',
      saved: state.savedTextSelection,
      hasToolbar: !!doc?.querySelector('#textSelectionToolbar'),
      selection: doc?.getSelection?.()?.toString?.() || ''
    };
  })())`));
  debug.beforeRaw = beforeRaw;
  assert(debug.afterRaw !== beforeRaw, "Physical bold click did not change the text block.", debug);
}

async function physicalLink(page, needle, url, options = {}) {
  await selectFrameTextAt(page, 0, needle, options);
  await clickFrameElement(page, "#textSelectionToolbar [data-text-toolbar-link]");
  await page.waitFor(`(() => {
    const doc = document.querySelector('#realPageFrame')?.contentDocument;
    return !!doc?.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
  })()`, 5000);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const input = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
    input.value = ${JSON.stringify(url)};
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await clickFrameElement(page, "#textSelectionToolbar [data-text-toolbar-link-submit]");
}

async function physicalSize(page, needle, size, options = {}) {
  await selectFrameTextAt(page, 0, needle, options);
  const beforeRaw = await page.evaluate(`state.builderBlocks[0]?.text || ''`);
  await clickFrameElement(page, `#textSelectionToolbar [data-text-toolbar-size="${size}"]`);
  const afterRaw = await page.evaluate(`state.builderBlocks[0]?.text || ''`);
  assert(options.allowNoChange || afterRaw !== beforeRaw, "Physical size click did not change the text block.", { beforeRaw, afterRaw, size });
}

async function testPhysicalTextFormattingMatrix() {
  await ensureFullStressPage();
  const page = await openCdpPage(ADMIN_URL);
  await openPageInAdmin(page, FULL_STRESS_PATH, "ru");
  await new Promise((resolve) => setTimeout(resolve, 700));
  const results = [];
  const record = async (name, assertFn) => {
    const metrics = await textFormatMetrics(page);
    assertFn(metrics);
    results.push({ name, raw: metrics.raw, strongTexts: metrics.strongTexts, links: metrics.links, innerText: metrics.innerText });
  };

  await setPhysicalFormatText(page, "Проверка что работает.");
  await physicalBold(page, "что");
  await record("bold plain word", (m) => {
    assert(m.raw === "Проверка **что** работает.", "Physical bold did not save markdown.", m);
    assert(m.strongTexts.includes("что") && !m.innerText.includes("**что**"), "Physical bold did not render as strong.", m);
  });

  await setPhysicalFormatText(page, "Проверка что работает.");
  await physicalLink(page, "что", "https://kwork.com/");
  await record("link plain word", (m) => {
    assert(m.raw === "Проверка [что](https://kwork.com/) работает.", "Physical link did not save markdown.", m);
    assert(m.links.some((link) => link.text === "что" && link.href === "https://kwork.com/"), "Physical link did not render.", m);
  });

  await setPhysicalFormatText(page, "Проверка что работает.");
  await physicalLink(page, "что", "https://kwork.com/");
  await physicalBold(page, "что");
  await record("link then bold", (m) => {
    assert(m.raw === "Проверка **[что](https://kwork.com/)** работает.", "Bold over existing link corrupted markdown.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что"), "Bold link did not render.", m);
  });

  await setPhysicalFormatText(page, "Проверка что работает.");
  await physicalBold(page, "что");
  await physicalLink(page, "что", "https://kwork.com/");
  await record("bold then link", (m) => {
    assert(m.raw === "Проверка **[что](https://kwork.com/)** работает.", "Link over bold word corrupted markdown.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что"), "Linked bold did not render.", m);
  });

  await setPhysicalFormatText(page, "alpha target beta target gamma");
  await physicalLink(page, "target", "/ru/faq/", { occurrence: "last" });
  await record("repeated last word link", (m) => {
    assert(m.raw === "alpha target beta [target](/ru/faq/) gamma", "Link applied to wrong repeated word.", m);
    assert(m.links.length === 1 && m.links[0].text === "target", "Repeated word link did not render once.", m);
  });

  await setPhysicalFormatText(page, "-\n\nЛучше масштабирование:\n\nфинал");
  await physicalLink(page, "Лучше", "https://kwork.com/", { length: 2 });
  await record("partial word link after dash", (m) => {
    assert(m.raw === "-\n\n[Лучше](https://kwork.com/) масштабирование:\n\nфинал", "Dash or partial word link broke markdown.", m);
    assert(m.links.some((link) => link.text === "Лучше"), "Dash-adjacent partial link did not render.", m);
  });

  await setPhysicalFormatText(page, "Проверка чтобы слово стало жирным.");
  await physicalBold(page, "чтобы", { length: 2 });
  await record("partial word bold expands", (m) => {
    assert(m.raw === "Проверка **чтобы** слово стало жирным.", "Partial word bold did not expand to the full word.", m);
    assert(m.strongTexts.includes("чтобы") && !m.innerText.includes("**чтобы**"), "Expanded bold did not render.", m);
  });

  await setPhysicalFormatText(page, "важна максимально короткая ссылка.");
  await physicalLink(page, "максимально короткая", "/ru/about/");
  await record("phrase link keeps phrase", (m) => {
    assert(m.raw === "важна [максимально короткая](/ru/about/) ссылка.", "Phrase link changed selection boundaries.", m);
    assert(m.links.some((link) => link.text === "максимально короткая"), "Phrase link did not render.", m);
  });

  await setPhysicalFormatText(page, "если продаётся именно линкбилдинг, а не объяснение, что такое PBN.");
  await physicalBold(page, "что");
  await record("cyrillic near punctuation bold", (m) => {
    assert(m.raw === "если продаётся именно линкбилдинг, а не объяснение, **что** такое PBN.", "Cyrillic word near punctuation did not bold.", m);
    assert(m.strongTexts.includes("что") && !m.innerText.includes("**что**"), "Cyrillic bold near punctuation did not render.", m);
  });

  await setPhysicalFormatText(page, "одно [что](https://kwork.com/) рядом");
  await physicalBold(page, "что");
  await record("existing anchor bold", (m) => {
    assert(m.raw === "одно **[что](https://kwork.com/)** рядом", "Existing anchor bold was corrupted.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что"), "Existing anchor bold did not render.", m);
  });

  await setPhysicalFormatText(page, "если объяснение, что такое PBN.");
  await physicalSize(page, "что", "22");
  await physicalBold(page, "что");
  await physicalLink(page, "что", "https://kwork.com/");
  await record("size then bold then link", (m) => {
    assert(m.raw === 'если объяснение, <span style="font-size: 22px;">**[что](https://kwork.com/)**</span> такое PBN.', "Size/bold/link order corrupted markdown.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что") && !m.innerText.includes("**что**"), "Size/bold/link did not render.", m);
  });

  await setPhysicalFormatText(page, "если объяснение, что такое PBN.");
  await physicalSize(page, "что", "22");
  await physicalLink(page, "что", "https://kwork.com/");
  await physicalBold(page, "что");
  await record("size then link then bold", (m) => {
    assert(m.raw === 'если объяснение, <span style="font-size: 22px;">**[что](https://kwork.com/)**</span> такое PBN.', "Size/link/bold order corrupted markdown.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что") && !m.innerText.includes("**что**"), "Size/link/bold did not render.", m);
  });

  await setPhysicalFormatText(page, 'если объяснение, <span style="font-size: 22px;">**[что](https://kwork.com/)**</span> такое PBN.');
  await physicalSize(page, "что", "14");
  await record("existing sized bold anchor reset", (m) => {
    assert(m.raw === 'если объяснение, **[что](https://kwork.com/)** такое PBN.', "Resetting existing sized bold anchor corrupted markdown.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что") && !m.raw.includes("font-size: 14px") && !m.innerText.includes("**что**"), "Reset sized bold anchor did not render normally.", m);
  });

  await setPhysicalFormatText(page, "если объяснение, **[что](https://kwork.com/)** такое PBN.");
  await physicalSize(page, "что", "14", { allowNoChange: true });
  await record("existing bold anchor normal size stays normal", (m) => {
    assert(m.raw === 'если объяснение, **[что](https://kwork.com/)** такое PBN.', "Normal-size button should not add a smaller span to bold anchor.", m);
    assert(m.strongTexts.includes("что") && m.links.some((link) => link.text === "что") && !m.raw.includes("font-size: 14px") && !m.innerText.includes("**что**"), "Normal-size bold anchor did not render.", m);
  });

  await setPhysicalFormatText(page, "важна максимально короткая ссылка.");
  await physicalSize(page, "максимально", "22");
  await physicalSize(page, "максимально", "14");
  await record("big then normal does not create small span", (m) => {
    assert(m.raw === "важна максимально короткая ссылка.", "Normal-size button should remove inline size instead of creating 14px text.", m);
    assert(!m.html.includes("font-size: 14px") && !m.html.includes("font-size: 22px"), "Normal-size text still has inline font-size.", m);
  });

  page.close();
  return { cases: results.length, results };
}

async function testEditorControlsRepair() {
  await ensureFullStressPage();
  const page = await openCdpPage(ADMIN_URL);
  await openPageInAdmin(page, FULL_STRESS_PATH, "ru");
  await new Promise((resolve) => setTimeout(resolve, 700));

  const apiPageList = (await adminApi("/api/pages")).pages || [];
  const navigation = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const filter = document.querySelector('#langFilter');
    filter.value = '';
    filter.dispatchEvent(new Event('change', { bubbles: true }));
    const paths = Array.from(document.querySelectorAll('.page-item')).map((item) => item.dataset.path);
    const buttons = Array.from(document.querySelectorAll('.nav-item')).map((item) => ({ view: item.dataset.view, text: item.textContent.trim() }));
    return { paths, buttons, filterValue: filter.value, pageCountText: document.querySelector('#pageCount')?.textContent || '' };
  })())`));
  const apiPaths = apiPageList.map((item) => item.path).sort();
  const visiblePaths = navigation.paths.slice().sort();
  assert(navigation.filterValue === "" && visiblePaths.length === apiPaths.length && apiPaths.every((path, index) => visiblePaths[index] === path), "Admin page list does not show every markdown page from API when language filter is set to all.", { navigation, apiPaths, visiblePaths });
  assert(navigation.paths.includes("content/privacy-policy/index.ru.md"), "Privacy policy page is not available in admin list.", navigation);
  assert(navigation.paths.includes("content/cookie-policy/index.ru.md"), "Cookie policy page is not available in admin list.", navigation);
  assert(navigation.paths.includes("content/services/_index.ru.md"), "Services page is not available in admin list.", navigation);
  assert(navigation.buttons.some((item) => item.view === "header") && navigation.buttons.some((item) => item.view === "footer"), "Header/Footer views are not available.", navigation);

  const allApiPagesOpen = [];
  for (const item of apiPageList) {
    await openPageInAdmin(page, item.path, item.language || "");
    const result = JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const frame = document.querySelector('#realPageFrame');
      const doc = frame?.contentDocument;
      const bodyValue = document.querySelector('#bodyEditor')?.value || '';
      const heroText = doc?.querySelector('.seo-hero-text');
      return {
        path: state.activePath,
        titleFieldExists: !!document.querySelector('#fieldTitle'),
        titleEditable: !!doc?.querySelector('.seo-hero-title[contenteditable="true"], h1[contenteditable="true"]'),
        bodyEditorExists: !!document.querySelector('#bodyEditor'),
        frontEditorExists: !!document.querySelector('#frontEditor'),
        bodyLength: bodyValue.length,
        hasBuilderJson: !!state.front.builderJson,
        builderSource: state.builderSource,
        heroEditable: !!heroText?.isContentEditable,
        frameLoaded: !!doc?.body,
        frameTextLength: (doc?.body?.innerText || '').length,
        draftUrl: draftPageUrl()
      };
    })())`));
    allApiPagesOpen.push(result);
    assert(result.path === item.path && result.frameLoaded && result.titleFieldExists && result.bodyEditorExists && result.frontEditorExists, "Markdown page from API is not open/editable in admin.", result);
    if (result.builderSource === "body" && result.bodyLength > 0 && item.section !== "strategy-builder") {
      assert(result.heroEditable || result.frameTextLength > 0, "Markdown body page has no editable/visible content in admin frame.", result);
    }
  }

  const existingPagesEditable = [];
  for (const item of [
    { path: "content/about/index.ru.md", expectedSource: "body", expectedDraft: "/ru/about/", expectedText: "SeoImpuls" },
    { path: "content/privacy-policy/index.ru.md", expectedSource: "body", expectedDraft: "/ru/privacy-policy/" },
    { path: "content/cookie-policy/index.ru.md", expectedSource: "body", expectedDraft: "/ru/cookie-policy/" },
    { path: "content/services/_index.ru.md", expectedSource: "front" },
  ]) {
    await openPageInAdmin(page, item.path, "ru");
    existingPagesEditable.push(JSON.parse(await page.evaluate(`JSON.stringify((() => {
      const frame = document.querySelector('#realPageFrame');
      const doc = frame?.contentDocument;
      const beforeHadBuilderJson = !!state.front.builderJson;
      const beforeBodyLength = (state.body || '').length;
      const beforeBlockCount = state.builderBlocks.length;
      const draftUrlValue = draftPageUrl();
      const fieldPageUrl = document.querySelector('#fieldPageUrl')?.value || '';
      const frameSrc = frame?.getAttribute('src') || '';
      const frameText = doc?.body?.innerText || '';
      const heroText = doc?.querySelector('.seo-hero-text');
      let heroEdit = null;
      if (${JSON.stringify(item.path)} === "content/about/index.ru.md" && heroText) {
        const marker = ' admin-live-edit';
        const beforeHero = heroText.innerText.trim();
        heroText.focus();
        heroText.textContent = beforeHero + marker;
        heroText.dispatchEvent(new doc.defaultView.InputEvent('input', { bubbles: true, inputType: 'insertText', data: marker }));
        heroEdit = {
          isEditable: heroText.isContentEditable,
          stateBodyHasMarker: state.body.includes(marker),
          bodyEditorHasMarker: (document.querySelector('#bodyEditor')?.value || '').includes(marker),
          blockTextHasMarker: (state.builderBlocks[0]?.text || '').includes(marker),
          previewBlockCount: doc.querySelectorAll('[data-preview-index]').length,
          heroText: heroText.innerText.trim()
        };
      }
      syncFieldsToFront();
      if (heroEdit) setDirty(false);
      return {
        path: state.activePath,
        builderSource: state.builderSource,
        draftUrlValue,
        fieldPageUrl,
        frameSrc,
        frameText,
        heroEdit,
        beforeHadBuilderJson,
        afterHadBuilderJson: !!state.front.builderJson,
        beforeBodyLength,
        afterBodyLength: (state.body || '').length,
        beforeBlockCount,
        editorBodyLength: (document.querySelector('#bodyEditor')?.value || '').length
      };
    })())`)));
    const checked = existingPagesEditable[existingPagesEditable.length - 1];
    assert(checked.path === item.path, "Existing page did not open in admin.", checked);
    assert(checked.beforeBodyLength > 20 && checked.editorBodyLength > 20 && checked.beforeBlockCount > 0, "Existing page opened without editable content.", checked);
    if (item.expectedDraft) {
      assert(checked.draftUrlValue === item.expectedDraft && checked.fieldPageUrl.endsWith(item.expectedDraft) && checked.frameSrc.includes(`/site${item.expectedDraft}`), "Existing index page preview URL is wrong.", checked);
    }
    if (item.expectedText) {
      assert(checked.frameText.includes(item.expectedText), "Existing page content is not visible in the admin iframe.", checked);
      assert(checked.heroEdit?.isEditable && checked.heroEdit.stateBodyHasMarker && checked.heroEdit.bodyEditorHasMarker && checked.heroEdit.blockTextHasMarker && checked.heroEdit.previewBlockCount === 0, "Existing body text is not editable in-place without a duplicate block.", checked);
    }
    if (item.expectedSource === "body") {
      assert(checked.builderSource === "body" && !checked.beforeHadBuilderJson && !checked.afterHadBuilderJson, "Markdown page would be converted to builderJson on save.", checked);
    } else {
      assert(checked.builderSource === "front" && checked.beforeHadBuilderJson && checked.afterHadBuilderJson, "Builder page lost builderJson editing mode.", checked);
    }
  }
  await openPageInAdmin(page, FULL_STRESS_PATH, "ru");

  await setPhysicalFormatText(page, "Клик по пустому месту закрывает окно ссылки.");
  await selectFrameTextAt(page, 0, "пустому");
  await clickFrameElement(page, "#textSelectionToolbar [data-text-toolbar-link]");
  await page.waitFor(`(() => {
    const doc = document.querySelector('#realPageFrame')?.contentDocument;
    return !!doc?.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
  })()`, 5000);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const main = doc.querySelector('main.main');
    main.dispatchEvent(new doc.defaultView.MouseEvent('click', { bubbles: true, cancelable: true, clientX: 20, clientY: 20 }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 250));
  const linkPopupClosed = await page.evaluate(`!document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar')`);
  assert(linkPopupClosed, "Link input popup did not close after clicking an empty page area.");

  await page.evaluate(`(() => {
    state.builderBlocks = [];
    state.selectedBlockIndex = null;
    clearSelectedImages();
    renderBuilder();
    applyDraftToRealFrame();
    return true;
  })()`);
  await page.evaluate(`document.querySelector('[data-add-block="image"]').click()`);
  await page.waitFor(`!!document.querySelector('#builderList input[data-field="image"]')`, 5000);
  await page.waitFor(`!!document.querySelector('#realPageFrame')?.contentDocument?.querySelector('[data-image-url-input]')`, 5000);
  const imageAdd = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const input = document.querySelector('#builderList input[data-field="image"]');
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const inlineInput = doc.querySelector('[data-image-url-input]');
    inlineInput.value = '/uploads/301-redirect-pagerank-1780874044.png';
    inlineInput.dispatchEvent(new doc.defaultView.Event('input', { bubbles: true }));
    doc.querySelector('[data-image-url-apply]').click();
    return {
      length: state.builderBlocks.length,
      type: state.builderBlocks[0]?.type,
      selected: state.selectedBlockIndex,
      hasImageInput: !!input,
      hasInlineImageInput: !!inlineInput,
      image: state.builderBlocks[0]?.image || '',
      renderedImage: !!doc.querySelector('[data-preview-index="0"] img')
    };
  })())`));
  assert(imageAdd.length === 1 && imageAdd.type === "image" && imageAdd.selected === 0 && imageAdd.hasImageInput && imageAdd.hasInlineImageInput && imageAdd.image.includes("/uploads/") && imageAdd.renderedImage, "Adding image did not expose/apply an inline image URL field.", imageAdd);

  const imageResize = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    state.selectedBlockIndex = 0;
    setSelectedImageIndexes([0]);
    renderBuilder();
    applyDraftToRealFrame();
    const before = Number(state.builderBlocks[0].imagePixelWidth) || 0;
    document.activeElement?.blur?.();
    document.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, cancelable: true, key: '+', ctrlKey: true }));
    const after = Number(state.builderBlocks[0].imagePixelWidth) || 0;
    return { before, after, selectedImage: state.selectedImageBlockIndex };
  })())`));
  assert(imageResize.after > imageResize.before && imageResize.selectedImage === 0, "Ctrl+plus did not resize the selected image.", imageResize);

  await page.evaluate(`(() => {
    document.activeElement?.blur?.();
    state.selectedBlockIndex = 0;
    setSelectedImageIndexes([0]);
    return true;
  })()`);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    doc.dispatchEvent(new doc.defaultView.KeyboardEvent('keydown', { bubbles: true, cancelable: true, key: 'Delete' }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 250));
  const deleteAndUndo = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const afterDelete = state.builderBlocks.length;
    const afterDeleteType = state.builderBlocks[0]?.type || '';
    document.querySelector('#visualUndoBtn').click();
    return {
      afterDelete,
      afterDeleteType,
      afterUndo: state.builderBlocks.length,
      restoredType: state.builderBlocks[0]?.type || '',
      undoDisabled: document.querySelector('#visualUndoBtn').disabled
    };
  })())`));
  assert(deleteAndUndo.afterDelete === 1 && deleteAndUndo.afterDeleteType === "spacer" && deleteAndUndo.afterUndo === 1 && deleteAndUndo.restoredType === "image", "Delete or visual undo for selected image failed.", deleteAndUndo);

  const deleteButtonTypes = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    state.builderBlocks = [
      { type: 'text', width: 'full', enabled: true, title: 'Delete text', text: 'Text block' },
      { type: 'buttons', width: 'full', enabled: true, buttons: [{ label: 'Button block', url: '#' }] },
      { type: 'image', width: 'full', enabled: true, image: '/uploads/301-redirect-pagerank-1780874044.png', alt: '' }
    ];
    state.selectedBlockIndex = null;
    clearSelectedImages();
    renderBuilder();
    applyDraftToRealFrame();
    const deleteAt = (index) => {
      const doc = document.querySelector('#realPageFrame').contentDocument;
      const block = doc.querySelector('[data-preview-index="' + index + '"]');
      const button = block?.querySelector('[data-block-delete]');
      state.selectedBlockIndex = index;
      if (state.builderBlocks[index]?.image) setSelectedImageIndexes([index]);
      else clearSelectedImages();
      refreshPreviewSelection();
      const before = state.builderBlocks.length;
      button?.click();
      const afterDelete = state.builderBlocks.length;
      const targetTypeAfterDelete = state.builderBlocks[index]?.type || '';
      document.querySelector('#visualUndoBtn').click();
      return {
        button: !!button,
        before,
        afterDelete,
        afterUndo: state.builderBlocks.length,
        restoredType: state.builderBlocks[index]?.type || '',
        targetTypeAfterDelete
      };
    };
    return { text: deleteAt(0), buttons: deleteAt(1), image: deleteAt(2) };
  })())`));
  assert(Object.values(deleteButtonTypes).every((item) => item.button && item.before === 3 && item.afterDelete === 3 && item.targetTypeAfterDelete === "spacer" && item.afterUndo === 3), "Visual delete button did not replace and undo all block types.", deleteButtonTypes);

  await page.evaluate(`(() => {
    state.builderBlocks = [
      { type: 'text', width: 'full', enabled: true, title: 'Physical delete target', text: 'Remove me with mouse' },
      { type: 'text', width: 'full', enabled: true, title: 'Physical delete survivor', text: 'Stay here' }
    ];
    state.selectedBlockIndex = 0;
    clearSelectedImages();
    renderBuilder();
    applyDraftToRealFrame();
    refreshPreviewSelection();
    return true;
  })()`);
  const physicalDeletePoint = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    frame.scrollIntoView({ block: 'start', inline: 'center' });
    const doc = frame.contentDocument;
    const button = doc.querySelector('[data-preview-index="0"] [data-block-delete]');
    const frameRect = frame.getBoundingClientRect();
    const rect = button?.getBoundingClientRect();
    const scaleX = frame.offsetWidth ? frameRect.width / frame.offsetWidth : 1;
    const scaleY = frame.offsetHeight ? frameRect.height / frame.offsetHeight : scaleX;
    const x = Math.round(frameRect.left + (rect.left + rect.width / 2) * scaleX);
    const y = Math.round(frameRect.top + (rect.top + rect.height / 2) * scaleY);
    const hit = rect ? doc.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2) : null;
    const parentHit = document.elementFromPoint(x, y);
    return {
      exists: !!button,
      x,
      y,
      hitDelete: !!hit?.closest?.('[data-block-delete]'),
      parentHitFrame: parentHit === frame,
      beforeCount: state.builderBlocks.length,
      viewport: { width: window.innerWidth, height: window.innerHeight }
    };
  })())`));
  assert(physicalDeletePoint.exists && physicalDeletePoint.hitDelete && physicalDeletePoint.parentHitFrame && physicalDeletePoint.x >= 0 && physicalDeletePoint.x <= physicalDeletePoint.viewport.width && physicalDeletePoint.y >= 0 && physicalDeletePoint.y <= physicalDeletePoint.viewport.height, "Physical delete button click target is not reachable.", physicalDeletePoint);
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: physicalDeletePoint.x, y: physicalDeletePoint.y, button: "none" });
  await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: physicalDeletePoint.x, y: physicalDeletePoint.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 80));
  await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: physicalDeletePoint.x, y: physicalDeletePoint.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 250));
  const physicalDelete = JSON.parse(await page.evaluate(`JSON.stringify({
    beforeCount: ${physicalDeletePoint.beforeCount},
    afterCount: state.builderBlocks.length,
    titles: state.builderBlocks.map((block) => block.title || ''),
    types: state.builderBlocks.map((block) => block.type || ''),
    selected: state.selectedBlockIndex
  })`));
  assert(physicalDelete.afterCount === 2 && physicalDelete.types[0] === "spacer" && !physicalDelete.titles.includes("Physical delete target") && physicalDelete.titles.includes("Physical delete survivor"), "Physical mouse click on delete button did not replace the block with a spacer.", physicalDelete);

  const deleteKeepsPreviewSlot = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const tallText = Array.from({ length: 34 }, (_, index) => 'Высокая строка блока ' + (index + 1)).join('\\n\\n');
    state.builderBlocks = [
      { type: 'text', width: 'full', enabled: true, title: 'Top block', text: 'Top text' },
      { type: 'text', width: 'full', enabled: true, title: 'Tall remove block', text: tallText },
      { type: 'text', width: 'full', enabled: true, title: 'Bottom block', text: 'Bottom text' }
    ];
    state.selectedBlockIndex = 1;
    clearSelectedImages();
    renderBuilder();
    applyDraftToRealFrame();
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const beforeHeight = Math.round(parseFloat(frame.style.height) || frame.getBoundingClientRect().height || 0);
    const button = doc.querySelector('[data-preview-index="1"] [data-block-delete]');
    button?.click();
    const afterHeight = Math.round(parseFloat(frame.style.height) || frame.getBoundingClientRect().height || 0);
    return {
      button: !!button,
      beforeHeight,
      afterHeight,
      heightDelta: afterHeight - beforeHeight,
      count: state.builderBlocks.length,
      types: state.builderBlocks.map((block) => block.type || ''),
      titles: state.builderBlocks.map((block) => block.title || '')
    };
  })())`));
  assert(deleteKeepsPreviewSlot.button && deleteKeepsPreviewSlot.count === 3 && deleteKeepsPreviewSlot.types[1] === "spacer" && !deleteKeepsPreviewSlot.titles.includes("Tall remove block") && Math.abs(deleteKeepsPreviewSlot.heightDelta) <= 40, "Deleting a block did not keep an empty slot in the real editor frame.", deleteKeepsPreviewSlot);

  const rightEdgeDeleteButton = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    state.builderBlocks = [
      { type: 'image', width: 'third', enabled: true, image: '/uploads/301-redirect-pagerank-1780874044.png', alt: '' },
      { type: 'image', width: 'third', enabled: true, image: '/uploads/301-redirect-pagerank-1780874044.png', alt: '' },
      { type: 'image', width: 'third', enabled: true, image: '/uploads/301-redirect-pagerank-1780874044.png', alt: '' }
    ];
    state.selectedBlockIndex = 2;
    setSelectedImageIndexes([2]);
    renderBuilder();
    applyDraftToRealFrame();
    refreshPreviewSelection();
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const block = doc.querySelector('[data-preview-index="2"]');
    const button = block?.querySelector('[data-block-delete]');
    const blockRect = block?.getBoundingClientRect();
    const buttonRect = button?.getBoundingClientRect();
    const viewportRight = doc.documentElement.clientWidth;
    return {
      exists: !!button,
      opacity: button ? getComputedStyle(button).opacity : '',
      blockRight: Math.round(blockRect?.right || 0),
      buttonLeft: Math.round(buttonRect?.left || 0),
      buttonRight: Math.round(buttonRect?.right || 0),
      viewportRight: Math.round(viewportRight),
      insideBlockRight: !!buttonRect && !!blockRect && buttonRect.right <= blockRect.right + 1,
      insideViewport: !!buttonRect && buttonRect.right <= viewportRight + 1
    };
  })())`));
  assert(rightEdgeDeleteButton.exists && rightEdgeDeleteButton.opacity === "1" && rightEdgeDeleteButton.insideBlockRight && rightEdgeDeleteButton.insideViewport, "Right-edge delete button is clipped or hidden.", rightEdgeDeleteButton);

  const deleteKeepsButtonGridSlot = JSON.parse(await page.evaluate(`(async () => JSON.stringify(await (async () => {
    const image = '/uploads/301-redirect-pagerank-1780874044.png';
    state.builderBlocks = [
      { type: 'image', width: 'third', enabled: true, image, alt: '' },
      { type: 'image', width: 'third', enabled: true, image, alt: '' },
      { type: 'image', width: 'third', enabled: true, image, alt: '' },
      { type: 'buttons', width: 'third', enabled: true, title: '', text: '', buttonWidthMode: 'full', buttons: [{ label: 'Left', url: '#' }] },
      { type: 'buttons', width: 'third', enabled: true, title: '', text: '', buttonWidthMode: 'full', buttons: [{ label: 'Middle', url: '#' }] },
      { type: 'buttons', width: 'third', enabled: true, title: '', text: '', buttonWidthMode: 'full', buttons: [{ label: 'Right', url: '#' }] }
    ];
    state.selectedBlockIndex = 4;
    clearSelectedImages();
    renderBuilder();
    applyDraftToRealFrame();
    refreshPreviewSelection();
    const doc = document.querySelector('#realPageFrame').contentDocument;
    await Promise.all(Array.from(doc.images).map((img) => img.complete ? true : new Promise((resolve) => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    })));
    await new Promise((resolve) => setTimeout(resolve, 120));
    const rectOf = (index) => {
      const rect = doc.querySelector('[data-preview-index="' + index + '"]')?.getBoundingClientRect();
      return rect ? { left: Math.round(rect.left), top: Math.round(rect.top), width: Math.round(rect.width), height: Math.round(rect.height) } : null;
    };
    const before = { left: rectOf(3), middle: rectOf(4), right: rectOf(5) };
    const button = doc.querySelector('[data-preview-index="4"] [data-block-delete]');
    button?.click();
    await Promise.all(Array.from(doc.images).map((img) => img.complete ? true : new Promise((resolve) => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    })));
    await new Promise((resolve) => setTimeout(resolve, 120));
    const after = { left: rectOf(3), middle: rectOf(4), right: rectOf(5) };
    return {
      button: !!button,
      targetType: state.builderBlocks[4]?.type || '',
      count: state.builderBlocks.length,
      before,
      after,
      leftDelta: before.left && after.left ? { x: after.left.left - before.left.left, y: after.left.top - before.left.top } : null,
      rightDelta: before.right && after.right ? { x: after.right.left - before.right.left, y: after.right.top - before.right.top } : null,
      middleHeightDelta: before.middle && after.middle ? after.middle.height - before.middle.height : null
    };
  })()))()`));
  assert(
    deleteKeepsButtonGridSlot.button &&
    deleteKeepsButtonGridSlot.count === 6 &&
    deleteKeepsButtonGridSlot.targetType === "spacer" &&
    Math.abs(deleteKeepsButtonGridSlot.leftDelta?.x || 0) <= 2 &&
    Math.abs(deleteKeepsButtonGridSlot.leftDelta?.y || 0) <= 2 &&
    Math.abs(deleteKeepsButtonGridSlot.rightDelta?.x || 0) <= 2 &&
    Math.abs(deleteKeepsButtonGridSlot.rightDelta?.y || 0) <= 2 &&
    Math.abs(deleteKeepsButtonGridSlot.middleHeightDelta || 0) <= 2,
    "Deleting the middle button did not keep the grid slot stable.",
    deleteKeepsButtonGridSlot
  );

  const undoAfterSave = JSON.parse(await page.evaluate(`(async () => JSON.stringify(await (async () => {
    state.builderBlocks = [{ type: 'text', width: 'full', enabled: true, title: 'Undo Save A', text: 'before save', titleAlign: 'left', textAlign: 'left' }];
    state.selectedBlockIndex = 0;
    clearBuilderHistory();
    renderBuilder();
    applyDraftToRealFrame();
    rememberBuilderState();
    state.builderBlocks[0].text = 'after save change';
    setDirty(true);
    syncFieldsToFront();
    await fetch('/api/page/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: state.activePath, frontmatter: state.front, body: state.body })
    });
    setDirty(false);
    const beforeUndoHistory = state.builderHistory.length;
    document.querySelector('#visualUndoBtn').click();
    return {
      beforeUndoHistory,
      textAfterUndo: state.builderBlocks[0]?.text || '',
      historyAfterUndo: state.builderHistory.length
    };
  })()))()`));
  assert(undoAfterSave.beforeUndoHistory >= 1 && undoAfterSave.textAfterUndo === "before save", "Undo after save did not restore the previous visual state.", undoAfterSave);

  const unlimitedBackUndo = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    state.builderBlocks = [{ type: 'text', width: 'full', enabled: true, title: 'Unlimited Back', text: 'step 0', titleAlign: 'left', textAlign: 'left' }];
    state.selectedBlockIndex = 0;
    clearBuilderHistory();
    renderBuilder();
    applyDraftToRealFrame();
    for (let index = 1; index <= 12; index += 1) {
      rememberBuilderState();
      state.builderBlocks[0].text = 'step ' + index;
      renderBuilder();
      applyDraftToRealFrame();
    }
    const beforeClicks = {
      history: state.builderHistory.length,
      text: state.builderBlocks[0]?.text || '',
      backDisabled: document.querySelector('#visualUndoBtn')?.disabled ?? null,
      cancelExists: !!document.querySelector('#builderUndoBtn'),
      stepsExists: !!document.querySelector('#builderUndoSteps')
    };
    for (let index = 0; index < 12; index += 1) {
      document.querySelector('#visualUndoBtn').click();
    }
    return {
      beforeClicks,
      afterText: state.builderBlocks[0]?.text || '',
      afterHistory: state.builderHistory.length,
      backDisabled: document.querySelector('#visualUndoBtn')?.disabled ?? null
    };
  })())`));
  assert(unlimitedBackUndo.beforeClicks.history === 12 && unlimitedBackUndo.beforeClicks.text === "step 12" && unlimitedBackUndo.afterText === "step 0" && unlimitedBackUndo.afterHistory === 0 && unlimitedBackUndo.backDisabled === true && !unlimitedBackUndo.beforeClicks.cancelExists && !unlimitedBackUndo.beforeClicks.stepsExists, "Back button did not undo more than 10 steps or old Cancel controls remain.", unlimitedBackUndo);

  const titleAlign = JSON.parse(await page.evaluate(`(async () => JSON.stringify(await (async () => {
    state.builderBlocks = [{ type: 'text', width: 'full', enabled: true, title: 'Centered Title', titleAlign: 'center', text: 'body', textAlign: 'left' }];
    state.selectedBlockIndex = 0;
    renderBuilder();
    applyDraftToRealFrame();
    syncFieldsToFront();
    await fetch('/api/page/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: state.activePath, frontmatter: state.front, body: state.body })
    });
    setDirty(false);
    const saved = await (await fetch('/api/page?path=' + encodeURIComponent(state.activePath))).json();
    await openPage(state.activePath);
    await new Promise((resolve) => setTimeout(resolve, 400));
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const title = doc.querySelector('[data-preview-index="0"] h2');
    return {
      stateAlign: state.builderBlocks[0].titleAlign,
      savedAlign: JSON.parse(saved.page?.frontmatter?.builderJson || '[]')[0]?.titleAlign || '',
      adminAlign: title ? getComputedStyle(title).textAlign : ''
    };
  })()))()`));
  assert(titleAlign.stateAlign === "center" && titleAlign.savedAlign === "center" && titleAlign.adminAlign === "center", "Title center alignment is not saved and restored in admin preview.", titleAlign);

  const toolbarLayout = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const toolbar = document.querySelector('.builder-toolbar');
    const firstGroup = toolbar?.querySelector('.builder-actions:first-child');
    const secondGroup = toolbar?.querySelector('.builder-actions:nth-child(2)');
    return {
      inFirst: !!firstGroup?.querySelector('#visualUndoBtn'),
      inSecond: !!secondGroup?.querySelector('#visualUndoBtn'),
      cancelExists: !!toolbar?.querySelector('#builderUndoBtn'),
      stepsExists: !!toolbar?.querySelector('#builderUndoSteps')
    };
  })())`));
  assert(!toolbarLayout.inFirst && toolbarLayout.inSecond && !toolbarLayout.cancelExists && !toolbarLayout.stepsExists, "Visual Back button layout or removed undo controls are wrong.", toolbarLayout);

  page.close();
  return { navigation, allApiPagesOpen, existingPagesEditable, imageAdd, imageResize, deleteAndUndo, deleteButtonTypes, physicalDelete, deleteKeepsPreviewSlot, rightEdgeDeleteButton, deleteKeepsButtonGridSlot, undoAfterSave, unlimitedBackUndo, titleAlign, toolbarLayout };
}

async function pressPublicElement(page, selector) {
  await page.evaluate(`(() => {
    const el = document.querySelector(${JSON.stringify(selector)});
    if (!el) throw new Error('press target not found: ${selector}');
    el.scrollIntoView({ block: 'center', inline: 'center' });
    el.addEventListener('click', (event) => event.preventDefault(), { once: true });
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 180));
  const before = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const el = document.querySelector(${JSON.stringify(selector)});
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
    return {
      x: Math.round(rect.left + rect.width / 2),
      y: Math.round(rect.top + rect.height / 2),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      href: el.href || '',
      transform: style.transform,
      filter: style.filter,
      hitInside: !!hit && (hit === el || el.contains(hit)),
      hit: hit ? { tag: hit.tagName, className: String(hit.className || ''), href: hit.href || '' } : null
    };
  })())`));
  assert(before.hitInside, `Press target center is intercepted: ${selector}`, before);
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: before.x, y: before.y, button: "none" });
  await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: before.x, y: before.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 140));
  const active = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const el = document.querySelector(${JSON.stringify(selector)});
    const style = getComputedStyle(el);
    return {
      pressed: el.classList.contains('is-pressed'),
      transform: style.transform,
      filter: style.filter
    };
  })())`));
  await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: before.x, y: before.y, button: "left", clickCount: 1 });
  return { before, active };
}

async function testFullEditorStressPage() {
  await ensureFullStressPage();
  const page = await openCdpPage(ADMIN_URL);
  await openPageInAdmin(page, FULL_STRESS_PATH, "ru");
  await new Promise((resolve) => setTimeout(resolve, 700));

  await page.evaluate(`(() => {
    state.selectedBlockIndex = 0;
    renderBuilder();
    applyDraftToRealFrame();
    const input = document.querySelector('#builderList input[data-field="fontSize"]');
    input.value = '23';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    const align = document.querySelector('#builderList select[data-field="textAlign"]');
    align.value = 'center';
    align.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 300));
  await selectFrameText(page, 0, "жирное");
  const boldSelectionDebug = JSON.parse(await page.evaluate(`JSON.stringify({
    saved: state.savedTextSelection,
    hasBoldButton: !!document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar [data-text-toolbar-bold]'),
    beforeText: state.builderBlocks[0].text
  })`));
  assert(boldSelectionDebug.saved?.text?.includes("жирное"), "Bold selection was not captured before clicking toolbar.", boldSelectionDebug);
  await page.evaluate(`document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar [data-text-toolbar-bold]').click()`);
  await new Promise((resolve) => setTimeout(resolve, 350));
  const boldApplyDebug = JSON.parse(await page.evaluate(`JSON.stringify({
    afterText: state.builderBlocks[0].text,
    saved: state.savedTextSelection
  })`));
  assert(boldApplyDebug.afterText.includes("**жирное**"), "Bold toolbar click did not apply markdown.", { before: boldSelectionDebug, after: boldApplyDebug });
  await selectFrameText(page, 0, "Первый");
  await page.evaluate(`document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar [data-text-toolbar-italic]').click()`);
  await new Promise((resolve) => setTimeout(resolve, 350));
  const italicApplyDebug = JSON.parse(await page.evaluate(`JSON.stringify({
    afterText: state.builderBlocks[0].text,
    html: document.querySelector('#realPageFrame').contentDocument.querySelector('[data-preview-index="0"] [data-block-field="text"]').innerHTML
  })`));
  assert(italicApplyDebug.afterText.includes("*Первый*") && italicApplyDebug.html.includes("<em>Первый</em>"), "Italic toolbar click did not apply markdown/rendering.", italicApplyDebug);
  await selectFrameText(page, 0, "блок");
  await page.evaluate(`document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar [data-text-toolbar-size="22"]').click()`);
  await new Promise((resolve) => setTimeout(resolve, 350));
  const sizeApplyDebug = JSON.parse(await page.evaluate(`JSON.stringify({
    afterText: state.builderBlocks[0].text,
    html: document.querySelector('#realPageFrame').contentDocument.querySelector('[data-preview-index="0"] [data-block-field="text"]').innerHTML
  })`));
  assert(sizeApplyDebug.afterText.includes('<span style="font-size: 22px;">блок</span>') && sizeApplyDebug.html.includes('font-size: 22px'), "Size toolbar click did not apply inline size.", sizeApplyDebug);
  await selectFrameText(page, 0, "анкор");
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    doc.querySelector('#textSelectionToolbar [data-text-toolbar-link]').click();
    const input = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-input]');
    input.focus();
    const paste = new ClipboardEvent('paste', { bubbles: true, cancelable: true });
    Object.defineProperty(paste, 'clipboardData', { value: { getData: () => '/ru/about/' } });
    input.dispatchEvent(paste);
    if (input.value !== '/ru/about/') throw new Error('Selection toolbar paste did not fill the link input');
    return true;
  })()`);
  await page.evaluate(`(() => {
    const doc = document.querySelector('#realPageFrame').contentDocument;
    const ok = doc.querySelector('#textSelectionToolbar [data-text-toolbar-link-submit]');
    if (!ok) throw new Error('Selection toolbar OK button did not appear');
    ok.click();
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 450));
  await selectFrameText(page, 0, "анкор");
  await page.evaluate(`document.querySelector('#realPageFrame').contentDocument.querySelector('#textSelectionToolbar [data-text-toolbar-bold]').click()`);
  await new Promise((resolve) => setTimeout(resolve, 450));
  const boldAnchorDebug = JSON.parse(await page.evaluate(`JSON.stringify({
    afterText: state.builderBlocks[0].text,
    html: document.querySelector('#realPageFrame').contentDocument.querySelector('[data-preview-index="0"] [data-block-field="text"]').innerHTML
  })`));
  assert(
    boldAnchorDebug.afterText.includes("**[анкор](/ru/about/)**")
      && !boldAnchorDebug.afterText.includes("[анк**")
      && !boldAnchorDebug.afterText.includes("**ан["),
    "Bold applied to an anchor corrupted markdown syntax.",
    boldAnchorDebug
  );
  const manualEditDebug = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const editable = doc.querySelector('[data-preview-index="0"] [data-block-field="text"]');
    editable.appendChild(doc.createTextNode(' manual-edit'));
    editable.dispatchEvent(new Event('input', { bubbles: true }));
    return { text: state.builderBlocks[0].text };
  })())`));
  assert(
    manualEditDebug.text.includes("**")
      && manualEditDebug.text.includes("](/ru/about/)")
      && manualEditDebug.text.includes("manual-edit"),
    "Manual iframe text edit erased markdown formatting.",
    manualEditDebug
  );

  await page.evaluate(`(() => {
    state.selectedBlockIndex = 1;
    renderBuilder();
    const link = document.querySelector('#builderList input[data-field="imageLink"]');
    link.value = ' javascript:alert(1) ';
    link.dispatchEvent(new Event('input', { bubbles: true }));
    if (state.builderBlocks[1].imageLink !== '') throw new Error('Unsafe image link was not cleared');
    link.value = '/ru/faq/';
    link.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 300));

  const directButtonEdit = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const button = doc.querySelector('[data-preview-index="2"] .seo-cta');
    button.click();
    const panel = doc.querySelector('#buttonLinkPanel');
    if (!panel) return { missingPanel: true };
    button.textContent = 'Small CTA Live';
    button.dispatchEvent(new Event('input', { bubbles: true }));
    const url = panel.querySelector('#buttonPanelUrl');
    url.value = ' https://kwork.com/ ';
    url.dispatchEvent(new Event('input', { bubbles: true }));
    const buttonRect = button.getBoundingClientRect();
    const panelRect = panel.getBoundingClientRect();
    return {
      parentPanel: !!document.querySelector('#buttonLinkPanel'),
      stateButton: state.builderBlocks[2].buttons[0],
      buttonText: button.textContent.trim(),
      panelRect: { left: Math.round(panelRect.left), top: Math.round(panelRect.top), bottom: Math.round(panelRect.bottom) },
      buttonRect: { left: Math.round(buttonRect.left), top: Math.round(buttonRect.top), bottom: Math.round(buttonRect.bottom) }
    };
  })())`));
  assert(!directButtonEdit.missingPanel, "Button inline panel did not appear in the iframe.", directButtonEdit);
  assert(!directButtonEdit.parentPanel, "Button panel should not be rendered outside the iframe.", directButtonEdit);
  assert(directButtonEdit.stateButton.label === "Small CTA Live" && directButtonEdit.stateButton.url === "https://kwork.com/", "Direct button label/url editing did not sync.", directButtonEdit);
  assert(Math.abs(directButtonEdit.panelRect.top - directButtonEdit.buttonRect.bottom) < 80 || directButtonEdit.panelRect.bottom <= directButtonEdit.buttonRect.top, "Button panel is not positioned near the selected button.", directButtonEdit);

  const adminMetrics = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const frame = document.querySelector('#realPageFrame');
    const doc = frame.contentDocument;
    const textBlock = doc.querySelector('[data-preview-index="0"]');
    const imageLink = doc.querySelector('[data-preview-index="1"] .seo-builder-image-link');
    const smallBlock = doc.querySelector('[data-preview-index="2"].seo-builder-block--compact');
    const smallButton = doc.querySelector('[data-preview-index="2"] .seo-cta');
    const wideButton = doc.querySelector('[data-preview-index="3"] .seo-cta');
    const banner = doc.querySelector('[data-preview-index="4"].seo-builder-block--banner');
    const squareButton = doc.querySelector('[data-preview-index="6"] .seo-cta');
    const rightText = doc.querySelector('[data-preview-index="7"] .seo-builder-text');
    const defaultRadiusButton = doc.querySelector('[data-preview-index="8"] .seo-cta');
    const gridText = doc.querySelector('[data-preview-index="9"] .seo-builder-card .seo-builder-text');
    return {
      textHtml: textBlock.querySelector('.seo-builder-text').innerHTML,
      textFont: getComputedStyle(textBlock.querySelector('.seo-builder-text')).fontSize,
      textAlign: getComputedStyle(textBlock.querySelector('.seo-builder-text')).textAlign,
      imageHref: imageLink ? imageLink.getAttribute('href') : '',
      small: (() => {
        const rect = smallButton.getBoundingClientRect();
        const style = getComputedStyle(smallButton);
        return { href: smallButton.getAttribute('href'), width: Math.round(rect.width), height: Math.round(rect.height), font: style.fontSize, radius: style.borderRadius, style: smallButton.getAttribute('style'), state: state.builderBlocks[2] };
      })(),
      smallBlock: (() => {
        const blockRect = smallBlock.getBoundingClientRect();
        const buttonRect = smallButton.getBoundingClientRect();
        const style = getComputedStyle(smallBlock);
        const hit = doc.elementFromPoint(buttonRect.left + buttonRect.width / 2, buttonRect.top + buttonRect.height / 2);
        return {
          padding: style.paddingTop,
          border: style.borderTopWidth,
          background: style.backgroundColor,
          widthDelta: Math.round(Math.abs(blockRect.width - buttonRect.width)),
          heightDelta: Math.round(Math.abs(blockRect.height - buttonRect.height)),
          hitInside: !!hit && (hit === smallButton || smallButton.contains(hit)),
          hit: hit ? { tag: hit.tagName, className: String(hit.className || ''), href: hit.href || '' } : null
        };
      })(),
      wide: (() => {
        const rect = wideButton.getBoundingClientRect();
        const style = getComputedStyle(wideButton);
        return { href: wideButton.getAttribute('href'), width: Math.round(rect.width), height: Math.round(rect.height), font: style.fontSize, radius: style.borderRadius, style: wideButton.getAttribute('style'), state: state.builderBlocks[3] };
      })(),
      square: (() => {
        const rect = squareButton.getBoundingClientRect();
        const style = getComputedStyle(squareButton);
        return { href: squareButton.getAttribute('href'), width: Math.round(rect.width), height: Math.round(rect.height), font: style.fontSize, radius: style.borderRadius, style: squareButton.getAttribute('style'), state: state.builderBlocks[6] };
      })(),
      rightTextAlign: rightText ? getComputedStyle(rightText).textAlign : '',
      defaultRadius: (() => {
        const rect = defaultRadiusButton.getBoundingClientRect();
        const style = getComputedStyle(defaultRadiusButton);
        return { href: defaultRadiusButton.getAttribute('href'), width: Math.round(rect.width), height: Math.round(rect.height), font: style.fontSize, radius: style.borderRadius, style: defaultRadiusButton.getAttribute('style'), state: state.builderBlocks[8] };
      })(),
      gridTextAlign: gridText ? getComputedStyle(gridText).textAlign : '',
      gridTextFont: gridText ? getComputedStyle(gridText).fontSize : '',
      banner: {
        exists: !!banner,
        imageHref: banner?.querySelector('.seo-builder-image-link')?.getAttribute('href') || '',
        buttonHref: banner?.querySelector('.seo-cta')?.getAttribute('href') || ''
      },
      rawText: state.builderBlocks[0].text
    };
  })())`));
  assert(adminMetrics.rawText.includes("**жирное**"), "Bold selection did not persist as markdown in admin state.", adminMetrics);
  assert(adminMetrics.rawText.includes("*Первый*"), "Italic selection did not persist as markdown in admin state.", adminMetrics);
  assert(adminMetrics.rawText.includes('<span style="font-size: 22px;">блок</span>'), "Inline selected text size did not persist in admin state.", adminMetrics);
  assert(adminMetrics.rawText.includes("**[анкор](/ru/about/)**"), "Bold anchor selection did not persist as safe markdown in admin state.", adminMetrics);
  assert(adminMetrics.textHtml.includes("<strong>жирное</strong>"), "Bold selection did not render in admin frame.", adminMetrics);
  assert(adminMetrics.textHtml.includes("<em>Первый</em>"), "Italic selection did not render in admin frame.", adminMetrics);
  assert(adminMetrics.textHtml.includes('font-size: 22px'), "Inline selected text size did not render in admin frame.", adminMetrics);
  assert(adminMetrics.textHtml.includes('href="/ru/about/"'), "Anchor selection did not render in admin frame.", adminMetrics);
  assert(adminMetrics.textFont === "23px", "Text font size did not apply in admin frame.", adminMetrics);
  assert(adminMetrics.textAlign === "center", "Text alignment did not apply in admin frame.", adminMetrics);
  assert(adminMetrics.imageHref === "/ru/faq/", "Image link did not apply in admin frame.", adminMetrics);
  assert(adminMetrics.small.width === 190 && adminMetrics.small.height === 48 && adminMetrics.small.font === "15px" && adminMetrics.small.radius === "6px", "Small button sizing is wrong in admin frame.", adminMetrics);
  assert(adminMetrics.smallBlock.padding === "0px" && adminMetrics.smallBlock.border === "0px" && adminMetrics.smallBlock.background === "rgba(0, 0, 0, 0)", "Compact button block still has visible admin wrapper chrome.", adminMetrics);
  assert(adminMetrics.smallBlock.widthDelta <= 2 && adminMetrics.smallBlock.heightDelta <= 2 && adminMetrics.smallBlock.hitInside, "Compact admin button wrapper is larger than the button or intercepts clicks.", adminMetrics);
  assert(adminMetrics.wide.width === 520 && adminMetrics.wide.height === 72 && adminMetrics.wide.font === "22px" && adminMetrics.wide.radius === "18px", "Wide button sizing is wrong in admin frame.", adminMetrics);
  assert(adminMetrics.banner.exists && adminMetrics.banner.imageHref === "https://example.com/banner" && adminMetrics.banner.buttonHref === "https://example.com/banner-button", "Banner links did not render in admin frame.", adminMetrics);
  assert(adminMetrics.square.width === 900 && adminMetrics.square.height === 60 && adminMetrics.square.font === "20px" && adminMetrics.square.radius === "0px", "Square huge button settings are wrong in admin frame.", adminMetrics);
  assert(adminMetrics.rightTextAlign === "right", "Right text alignment did not apply in admin frame.", adminMetrics);
  assert(adminMetrics.defaultRadius.width === 240 && adminMetrics.defaultRadius.height === 50 && adminMetrics.defaultRadius.font === "16px" && adminMetrics.defaultRadius.radius === "8px", "Empty button radius should keep theme default in admin frame.", adminMetrics);
  assert(adminMetrics.gridTextAlign === "center" && adminMetrics.gridTextFont === "19px", "Grid card text style does not match admin frame settings.", adminMetrics);

  await page.evaluate(`document.querySelector('#editorForm').requestSubmit()`);
  await page.waitFor(`document.querySelector('#saveState')?.textContent.includes('Не изменено')`, 45000);
  page.close();
  const savedPage = await adminApi(`/api/page?path=${encodeURIComponent(FULL_STRESS_PATH)}`);
  const savedBlocks = JSON.parse(savedPage.page?.frontmatter?.builderJson || "[]");
  assert(savedBlocks[0]?.text?.includes("**") && savedBlocks[0]?.text?.includes("](/ru/about/)") && savedBlocks[0]?.text?.includes("manual-edit"), "Saved builderJson lost formatted text after manual edit.", savedBlocks[0]);
  assert(savedBlocks[1]?.imageLink === "/ru/faq/", "Saved builderJson image link round-trip is wrong.", savedBlocks[1]);
  assert(savedBlocks[6]?.buttonRadius === 0, "Saved builderJson lost explicit zero button radius.", savedBlocks[6]);
  assert(savedBlocks[8]?.buttonRadius === "", "Saved builderJson should preserve empty default button radius.", savedBlocks[8]);
  assert(savedBlocks[9]?.type === "grid" && savedBlocks[9]?.textAlign === "center", "Saved builderJson grid text alignment is wrong.", savedBlocks[9]);
  assert(await waitForHttp(FULL_STRESS_URL, 30000), "Full stress public URL did not become available after saving.");

  const publicPage = await openCdpPage(FULL_STRESS_URL);
  await publicPage.send("Page.bringToFront");
  await publicPage.send("Emulation.setDeviceMetricsOverride", {
    width: 1440,
    height: 1000,
    deviceScaleFactor: 1,
    mobile: false,
  });
  await publicPage.evaluate(`(() => {
    localStorage.setItem('seoimpuls_cookie_consent_v2', JSON.stringify({ analytics: false, updatedAt: new Date().toISOString(), policyVersion: '2026-02-28', lang: 'ru', source: 'stress-test' }));
    return true;
  })()`);
  await publicPage.send("Page.navigate", { url: FULL_STRESS_URL });
  await publicPage.waitFor("document.readyState === 'complete'");
  const hasBuilder = await publicPage.waitFor("!!document.querySelector('.seo-builder')", 30000).catch(() => false);
  if (!hasBuilder) {
    const debug = JSON.parse(await publicPage.evaluate(`JSON.stringify({
      href: location.href,
      title: document.title,
      bodyClass: document.body.className,
      htmlStart: document.documentElement.innerHTML.slice(0, 1200)
    })`));
    assert(false, "Full stress public page did not render builder.", debug);
  }
  const publicCssReady = await publicPage.waitFor(`(() => {
    const text = document.querySelector('.seo-builder-block--text .seo-builder-text');
    const small = document.querySelector('.seo-cta[href="https://kwork.com/"]');
    const wide = document.querySelector('.seo-cta[href="/ru/about/"], .seo-cta[href="/about/"]');
    const square = document.querySelector('.seo-cta[href="#square"]');
    const rightText = document.querySelector('[data-admin-block-index="7"] .seo-builder-text');
    const defaultRadius = document.querySelector('.seo-cta[href="#default-radius"]');
    const gridText = document.querySelector('[data-admin-block-index="9"] .seo-builder-card .seo-builder-text');
    if (!text || !small || !wide || !square || !rightText || !defaultRadius || !gridText) return false;
    return getComputedStyle(text).textAlign === 'center'
      && getComputedStyle(small).borderRadius === '6px'
      && getComputedStyle(wide).borderRadius === '18px'
      && getComputedStyle(square).borderRadius === '0px'
      && getComputedStyle(rightText).textAlign === 'right'
      && getComputedStyle(defaultRadius).borderRadius === '8px'
      && getComputedStyle(gridText).textAlign === 'center';
  })()`, 30000).catch(() => false);
  if (!publicCssReady) {
    await publicPage.send("Page.reload", { ignoreCache: true });
    await publicPage.waitFor("document.readyState === 'complete'");
  }
  const publicMetrics = JSON.parse(await publicPage.evaluate(`JSON.stringify((() => {
    const root = document.documentElement;
    const text = document.querySelector('.seo-builder-block--text .seo-builder-text');
    const small = document.querySelector('.seo-cta[href="https://kwork.com/"]');
    const wide = document.querySelector('.seo-cta[href="/ru/about/"], .seo-cta[href="/about/"]');
    const image = document.querySelector('.seo-builder-block--image .seo-builder-image-link');
    const banner = document.querySelector('.seo-builder-block--banner');
    const square = document.querySelector('.seo-cta[href="#square"]');
    const rightText = document.querySelector('[data-admin-block-index="7"] .seo-builder-text');
    const defaultRadius = document.querySelector('.seo-cta[href="#default-radius"]');
    const gridText = document.querySelector('[data-admin-block-index="9"] .seo-builder-card .seo-builder-text');
    const overflowers = Array.from(document.body.querySelectorAll('*'))
      .map((el) => ({ tag: el.tagName, cls: String(el.className || ''), right: Math.round(el.getBoundingClientRect().right) }))
      .filter((item) => item.right > root.clientWidth + 2)
      .slice(0, 8);
    const rectOf = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return { width: Math.round(rect.width), height: Math.round(rect.height), font: style.fontSize, radius: style.borderRadius };
    };
    const compactBlockOf = (button) => {
      const block = button?.closest('.seo-builder-block--compact');
      if (!button || !block) return null;
      const blockRect = block.getBoundingClientRect();
      const buttonRect = button.getBoundingClientRect();
      const style = getComputedStyle(block);
      const hit = document.elementFromPoint(buttonRect.left + buttonRect.width / 2, buttonRect.top + buttonRect.height / 2);
      return {
        padding: style.paddingTop,
        border: style.borderTopWidth,
        background: style.backgroundColor,
        widthDelta: Math.round(Math.abs(blockRect.width - buttonRect.width)),
        heightDelta: Math.round(Math.abs(blockRect.height - buttonRect.height)),
        hitInside: !!hit && (hit === button || button.contains(hit)),
        hit: hit ? { tag: hit.tagName, className: String(hit.className || ''), href: hit.href || '' } : null
      };
    };
    return {
      clientWidth: root.clientWidth,
      scrollWidth: root.scrollWidth,
      overflowers,
      strong: text?.querySelector('strong')?.textContent || '',
      anchorText: text?.querySelector('a[href="/ru/about/"]')?.textContent || '',
      inlineFont: text?.querySelector('span[style*="font-size"]') ? getComputedStyle(text.querySelector('span[style*="font-size"]')).fontSize : '',
      textFont: text ? getComputedStyle(text).fontSize : '',
      textAlign: text ? getComputedStyle(text).textAlign : '',
      imageHref: image ? image.getAttribute('href') : '',
      small: small ? rectOf(small) : null,
      smallBlock: compactBlockOf(small),
      wide: wide ? rectOf(wide) : null,
      square: square ? rectOf(square) : null,
      rightTextAlign: rightText ? getComputedStyle(rightText).textAlign : '',
      defaultRadius: defaultRadius ? rectOf(defaultRadius) : null,
      gridTextAlign: gridText ? getComputedStyle(gridText).textAlign : '',
      gridTextFont: gridText ? getComputedStyle(gridText).fontSize : '',
      bannerImageHref: banner?.querySelector('.seo-builder-image-link')?.getAttribute('href') || '',
      bannerButtonHref: banner?.querySelector('.seo-cta')?.getAttribute('href') || ''
    };
  })())`));
  assert(publicMetrics.scrollWidth <= publicMetrics.clientWidth + 2 && publicMetrics.overflowers.length === 0, "Full stress public page has desktop overflow.", publicMetrics);
  assert(publicMetrics.strong === "жирное", "Public bold text is missing.", publicMetrics);
  assert(publicMetrics.anchorText === "анкор", "Public anchor text is missing.", publicMetrics);
  assert(publicMetrics.inlineFont === "22px", "Public inline selected font size is missing.", publicMetrics);
  assert(publicMetrics.textFont === "23px", "Public text font size is wrong.", publicMetrics);
  assert(publicMetrics.textAlign === "center", "Public text alignment is wrong.", publicMetrics);
  assert(publicMetrics.imageHref === "/ru/faq/", "Public image link is wrong.", publicMetrics);
  assert(publicMetrics.small?.width === 190 && publicMetrics.small?.height === 48 && publicMetrics.small?.font === "15px" && publicMetrics.small?.radius === "6px", "Public small button sizing is wrong.", publicMetrics);
  assert(publicMetrics.smallBlock?.padding === "0px" && publicMetrics.smallBlock?.border === "0px" && publicMetrics.smallBlock?.background === "rgba(0, 0, 0, 0)", "Compact button block still has visible public wrapper chrome.", publicMetrics);
  assert(publicMetrics.smallBlock?.widthDelta <= 2 && publicMetrics.smallBlock?.heightDelta <= 2 && publicMetrics.smallBlock?.hitInside, "Compact public button wrapper is larger than the button or intercepts clicks.", publicMetrics);
  assert(publicMetrics.wide?.width === 520 && publicMetrics.wide?.height === 72 && publicMetrics.wide?.font === "22px" && publicMetrics.wide?.radius === "18px", "Public wide button sizing is wrong.", publicMetrics);
  assert(publicMetrics.square?.width === 900 && publicMetrics.square?.height === 60 && publicMetrics.square?.font === "20px" && publicMetrics.square?.radius === "0px", "Public square huge button settings are wrong.", publicMetrics);
  assert(publicMetrics.rightTextAlign === "right", "Public right text alignment is wrong.", publicMetrics);
  assert(publicMetrics.defaultRadius?.width === 240 && publicMetrics.defaultRadius?.height === 50 && publicMetrics.defaultRadius?.font === "16px" && publicMetrics.defaultRadius?.radius === "8px", "Public empty button radius should keep theme default.", publicMetrics);
  assert(publicMetrics.gridTextAlign === "center" && publicMetrics.gridTextFont === "19px", "Public grid card text style is wrong.", publicMetrics);
  assert(publicMetrics.bannerImageHref === "https://example.com/banner" && publicMetrics.bannerButtonHref === "https://example.com/banner-button", "Public banner links are wrong.", publicMetrics);

  const smallPress = await pressPublicElement(publicPage, '.seo-cta[href="https://kwork.com/"]');
  const imagePress = await pressPublicElement(publicPage, '.seo-builder-block--image .seo-builder-image-link');
  assert(smallPress.active.pressed && smallPress.active.transform !== smallPress.before.transform, "Public stress button did not visually press.", smallPress);
  assert(imagePress.active.pressed && imagePress.active.transform !== imagePress.before.transform, "Public stress image link did not visually press.", imagePress);

  const responsive = [];
  for (const viewport of [
    { name: "wide-boundary", width: 1280, height: 900 },
    { name: "desktop-before-reset", width: 1101, height: 900 },
    { name: "desktop-reset", width: 1100, height: 900 },
    { name: "tablet", width: 1024, height: 900 },
    { name: "mobile-before", width: 768, height: 900 },
    { name: "mobile-boundary", width: 767, height: 900 },
    { name: "mobile", width: 390, height: 900 },
    { name: "small-mobile", width: 360, height: 900 },
    { name: "tiny-mobile", width: 320, height: 900 },
  ]) {
    await publicPage.send("Emulation.setDeviceMetricsOverride", {
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: 1,
      mobile: viewport.width < 768,
    });
    await publicPage.send("Page.navigate", { url: FULL_STRESS_URL });
    await publicPage.waitFor("document.readyState === 'complete'");
    const metrics = JSON.parse(await publicPage.evaluate(`JSON.stringify((() => {
      const root = document.documentElement;
      const overflowers = Array.from(document.body.querySelectorAll('*'))
        .map((el) => ({ tag: el.tagName, cls: String(el.className || ''), right: Math.round(el.getBoundingClientRect().right) }))
        .filter((item) => item.right > root.clientWidth + 2)
        .slice(0, 8);
      const square = document.querySelector('.seo-cta[href="#square"]');
      const squareRect = square?.getBoundingClientRect();
      return {
        clientWidth: root.clientWidth,
        scrollWidth: root.scrollWidth,
        overflowers,
        square: squareRect ? { width: Math.round(squareRect.width), right: Math.round(squareRect.right) } : null
      };
    })())`));
    responsive.push({ viewport, metrics });
    assert(metrics.scrollWidth <= metrics.clientWidth + 2 && metrics.overflowers.length === 0, `Full stress ${viewport.name} has overflow.`, metrics);
    assert(!metrics.square || metrics.square.width <= metrics.clientWidth, `Full stress ${viewport.name} square button exceeds viewport.`, metrics);
  }
  publicPage.close();
  return { adminMetrics, publicMetrics, smallPress, imagePress, responsive };
}

async function testPublicButtonPress() {
  if (!(await canFetch(TEST_BUTTON_URL))) return { skipped: true };
  const page = await openCdpPage(TEST_BUTTON_URL);
  await page.send("Page.bringToFront");
  await page.evaluate(`(() => {
    localStorage.setItem('seoimpuls_cookie_consent_v2', JSON.stringify({
      analytics: false,
      updatedAt: new Date().toISOString(),
      policyVersion: '2026-02-28',
      lang: 'ru',
      source: 'responsive-test'
    }));
    return true;
  })()`);
  await page.send("Page.reload", { ignoreCache: true });
  await page.waitFor("document.readyState === 'complete'");
  await page.waitFor(`!!document.querySelector('.seo-cta[href="https://kwork.com/"]')`);
  await page.evaluate(`document.querySelector('.seo-cta[href="https://kwork.com/"]').scrollIntoView({ block: 'center', inline: 'center' })`);
  await new Promise((resolve) => setTimeout(resolve, 300));
  const before = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const button = document.querySelector('.seo-cta[href="https://kwork.com/"]');
    const rect = button.getBoundingClientRect();
    const style = getComputedStyle(button);
    return {
      label: button.textContent.trim(),
      href: button.href,
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      x: Math.round(rect.left + rect.width / 2),
      y: Math.round(rect.top + rect.height / 2),
      transform: style.transform,
      filter: style.filter,
      pressed: button.classList.contains('is-pressed'),
      hit: (() => {
        const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
        return hit ? { tag: hit.tagName, className: String(hit.className || ''), text: hit.textContent.trim().slice(0, 80), href: hit.href || '' } : null;
      })()
    };
  })())`));
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: before.x, y: before.y, button: "none" });
  await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: before.x, y: before.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 160));
  const active = JSON.parse(await page.evaluate(`JSON.stringify((() => {
    const button = document.querySelector('.seo-cta[href="https://kwork.com/"]');
    const style = getComputedStyle(button);
    return {
      transform: style.transform,
      filter: style.filter,
      pressed: button.classList.contains('is-pressed')
    };
  })())`));
  await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: before.x, y: before.y, button: "left", clickCount: 1 });
  assert(before.label === "Test Kwork Button", "Public test button label is wrong.", { before, active });
  assert(before.href === "https://kwork.com/", "Public test button URL is wrong.", { before, active });
  assert(before.width >= 450 && before.height >= 90, "Public test button size did not persist.", { before, active });
  assert(active.pressed, "Public test button did not receive press class.", { before, active });
  assert(active.transform !== before.transform || active.filter !== before.filter, "Public test button did not visually press.", { before, active });
  page.close();
  return { before, active };
}

async function main() {
  assert(await canFetch(ADMIN_URL), `Admin is not available at ${ADMIN_URL}. Start admin/server.py first.`);
  const hugo = await startHugoIfNeeded();
  const chrome = await startChrome();
  try {
    const publicResponsive = await testPublicResponsive();
    const adminInsertions = await testAdminImageRowInsertions();
    const adminWrap = await testAdminWrapBlock();
    const fullEditorStress = await testFullEditorStressPage();
    const physicalTextFormatting = await testPhysicalTextFormattingMatrix();
    const editorControlsRepair = await testEditorControlsRepair();
    const publicButtonPress = await testPublicButtonPress();
    console.log(JSON.stringify({ ok: true, publicResponsive, adminInsertions, adminWrap, fullEditorStress, physicalTextFormatting, editorControlsRepair, publicButtonPress }, null, 2));
  } finally {
    await ensureFullStressPage().catch(() => {});
    await chrome.close();
    if (hugo) hugo.kill();
  }
}

main().catch((error) => {
  console.error(error.message);
  if (error.details) console.error(JSON.stringify(error.details, null, 2));
  process.exit(1);
});
