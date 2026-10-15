#!/usr/bin/env python
"""
E2E smoke checks for the multilingual SEO strategy builder.

Usage:
  python scripts/e2e_strategy_builder.py

Optional:
  python scripts/e2e_strategy_builder.py --no-server --base-url http://127.0.0.1:1313
  python scripts/e2e_strategy_builder.py --json-output e2e-report.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception as exc:  # pragma: no cover
    print("Failed to import Playwright. Install with: pip install playwright")
    print("Then install browser: playwright install chromium")
    print(f"Import error: {exc}")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


HOME_CASES = [
    ("ru", "/ru/", "\u0421\u0435\u043e \u043f\u0440\u043e\u0434\u0432\u0438\u0436\u0435\u043d\u0438\u0435 \u0441\u0430\u0439\u0442\u043e\u0432"),
    ("es", "/es/", "Servicio de Link Building"),
    ("en", "/en/", "SEO Backlink Service"),
]


BUILDER_CASES = [
    {
        "lang": "ru",
        "path": "/ru/konstruktor-seo-strategii/",
        "response_marker": "\u0422\u0435\u043a\u0443\u0449\u0430\u044f \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f:",
        "qty_crowd": "\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u0440\u0430\u0443\u0434-\u0441\u0441\u044b\u043b\u043e\u043a",
        "qty_r301": "\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e 301 \u0440\u0435\u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0432",
    },
    {
        "lang": "es",
        "path": "/es/constructor-estrategias-seo/",
        "response_marker": "Configuracion actual:",
        "qty_crowd": "Indica la cantidad de enlaces crowd",
        "qty_r301": "Indica la cantidad de redirecciones 301",
    },
    {
        "lang": "en",
        "path": "/en/seo-strategy-builder/",
        "response_marker": "Current setup:",
        "qty_crowd": "Enter number of crowd links",
        "qty_r301": "Enter number of 301 redirects",
    },
]


def wait_for_server(url: str, timeout_sec: float = 40.0) -> bool:
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.4)
    return False


def compact_text(text: str) -> str:
    return " ".join((text or "").split())


def safe_detail(text: str, max_len: int = 220) -> str:
    clipped = text[:max_len]
    return clipped.encode("unicode_escape", errors="ignore").decode("ascii")


def has_class(page, selector: str, cls_name: str) -> bool:
    cls = page.locator(selector).get_attribute("class") or ""
    return cls_name in cls.split()


def click_by_mouse_center(page, selector: str) -> None:
    box = page.locator(selector).bounding_box()
    if not box:
        raise RuntimeError(f"No bounding box for selector: {selector}")
    x = box["x"] + (box["width"] / 2)
    y = box["y"] + (box["height"] / 2)
    page.mouse.click(x, y)


def select_base_configuration(page) -> None:
    page.locator('.sb-btn[data-key="onepage"]').click()
    page.locator('.sb-btn[data-type="single"][data-group="freq"][data-key="low"]').click()
    page.locator('.sb-btn[data-type="single"][data-group="theme"][data-key="white"]').click()
    page.locator('.sb-btn[data-key="newregs"]').click()
    page.locator('.sb-btn[data-key="static"]').click()
    page.wait_for_timeout(120)


def open_qty_picker(page, key: str) -> None:
    page.locator(f'.sb-btn[data-type="multi"][data-key="{key}"]').click()
    page.wait_for_selector("#sbQtyPicker.is-open", timeout=3000)


def pick_qty_value(page, value: int) -> None:
    page.locator(f'.sb-qty-item[data-value="{value}"]').click()
    page.wait_for_timeout(120)


def run_checks(base_url: str, headless: bool = True) -> list[CheckResult]:
    results: list[CheckResult] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()

        for lang, path, expected in HOME_CASES:
            try:
                page.goto(base_url + path, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(120)
                title = page.title()
                results.append(CheckResult(f"home_{lang}_title", expected in title, safe_detail(title)))
            except Exception as exc:
                results.append(CheckResult(f"home_{lang}_title", False, safe_detail(str(exc))))

        for cfg in BUILDER_CASES:
            lang = cfg["lang"]
            url = base_url + cfg["path"]
            satellite_sel = '.sb-btn[data-type="multi"][data-key="satellite"]'
            crowd_sel = '.sb-btn[data-type="multi"][data-key="crowd"]'
            r301_sel = '.sb-btn[data-type="multi"][data-key="r301"]'
            fp_sel = '.sb-qty-item[data-special="satellite_footprints"]'

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_selector("#sbApply", timeout=8000)

                # 1) Apply -> localized full response marker
                select_base_configuration(page)
                open_qty_picker(page, "satellite")
                pick_qty_value(page, 3)
                page.locator("#sbQtyPicker .sb-qty-backdrop").click()
                page.wait_for_timeout(120)
                page.locator("#sbApply").click()
                page.wait_for_timeout(240)
                resp = compact_text(page.locator("#sbResponse").inner_text() or "")
                ok_resp = cfg["response_marker"] in resp
                results.append(CheckResult(f"{lang}_apply_localized", ok_resp, safe_detail(resp)))

                # Reset for interaction checks
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_selector("#sbApply", timeout=8000)
                select_base_configuration(page)

                # 2) First click on active PBN should cancel immediately
                open_qty_picker(page, "satellite")
                pick_qty_value(page, 3)
                before = has_class(page, satellite_sel, "is-active")
                click_by_mouse_center(page, satellite_sel)
                page.wait_for_timeout(200)
                after = has_class(page, satellite_sel, "is-active")
                results.append(
                    CheckResult(
                        f"{lang}_satellite_first_click_cancel",
                        bool(before and (not after)),
                        f"before={before}, after={after}",
                    )
                )

                # 3) Popup handoff: PBN -> Crowd in one click
                open_qty_picker(page, "satellite")
                click_by_mouse_center(page, crowd_sel)
                page.wait_for_timeout(220)
                qty_title_crowd = compact_text(page.locator("#sbQtyTitle").inner_text() or "")
                ok_crowd = cfg["qty_crowd"] in qty_title_crowd
                results.append(CheckResult(f"{lang}_popup_handoff_crowd", ok_crowd, safe_detail(qty_title_crowd)))

                # 4) Popup handoff: Crowd -> R301 in one click
                click_by_mouse_center(page, r301_sel)
                page.wait_for_timeout(220)
                qty_title_r301 = compact_text(page.locator("#sbQtyTitle").inner_text() or "")
                ok_r301 = cfg["qty_r301"] in qty_title_r301
                results.append(CheckResult(f"{lang}_popup_handoff_r301", ok_r301, safe_detail(qty_title_r301)))

                # 5) Footprints gate: disabled at qty=2, enabled at qty=3
                click_by_mouse_center(page, satellite_sel)
                page.wait_for_timeout(220)
                pick_qty_value(page, 2)
                disabled_2 = has_class(page, fp_sel, "is-disabled")
                pick_qty_value(page, 3)
                disabled_3 = has_class(page, fp_sel, "is-disabled")
                results.append(
                    CheckResult(
                        f"{lang}_footprints_gate",
                        bool(disabled_2 and (not disabled_3)),
                        f"disabled@2={disabled_2}, disabled@3={disabled_3}",
                    )
                )

            except PlaywrightTimeoutError as exc:
                results.append(CheckResult(f"{lang}_fatal", False, safe_detail(f"timeout: {exc}")))
            except Exception as exc:
                results.append(CheckResult(f"{lang}_fatal", False, safe_detail(str(exc))))

        browser.close()

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="E2E smoke for strategy builder (ru/es/en).")
    parser.add_argument("--base-url", default="http://127.0.0.1:1313", help="Base URL for the site.")
    parser.add_argument("--no-server", action="store_true", help="Do not start hugo server automatically.")
    parser.add_argument("--hugo-bin", default="hugo", help="Hugo binary to run when auto-starting server.")
    parser.add_argument("--json-output", default="", help="Optional path to write JSON report.")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    server_proc: Optional[subprocess.Popen] = None
    all_results: list[CheckResult] = []

    try:
        if not args.no_server:
            server_proc = subprocess.Popen(
                [
                    args.hugo_bin,
                    "server",
                    "--bind",
                    "127.0.0.1",
                    "--port",
                    "1313",
                    "--disableFastRender",
                ],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            if not wait_for_server(args.base_url.rstrip("/") + "/en/"):
                print("[FAIL] server_start :: hugo server did not become ready")
                return 2
            print("[PASS] server_start")

        all_results = run_checks(args.base_url.rstrip("/"), headless=not args.headed)

    finally:
        if server_proc is not None:
            try:
                server_proc.terminate()
            except Exception:
                pass
            try:
                server_proc.wait(timeout=8)
            except Exception:
                pass

    passed = 0
    failed = 0
    for item in all_results:
        if item.ok:
            passed += 1
            print(f"[PASS] {item.name}")
        else:
            failed += 1
            detail = f" :: {item.detail}" if item.detail else ""
            print(f"[FAIL] {item.name}{detail}")

    summary = {
        "passed": passed,
        "failed": failed,
        "results": [item.__dict__ for item in all_results],
    }
    print(f"Summary: passed={passed}, failed={failed}")

    if args.json_output:
        out_path = Path(args.json_output).resolve()
        out_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
        print(f"JSON report: {out_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

