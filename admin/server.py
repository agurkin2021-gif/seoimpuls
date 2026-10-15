from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import posixpath
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import unicodedata
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def admin_root_from_runtime() -> Path:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        return exe_dir.parent if exe_dir.name.lower() == "exe" else exe_dir
    return Path(__file__).resolve().parent


ADMIN_ROOT = admin_root_from_runtime()
PROJECT_ROOT = ADMIN_ROOT.parent


def ensure_runtime_streams() -> None:
    if sys.stdout is not None and sys.stderr is not None:
        return
    log_path = ADMIN_ROOT / "server_runtime.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    stream = open(log_path, "a", encoding="utf-8", buffering=1)
    if sys.stdout is None:
        sys.stdout = stream
    if sys.stderr is None:
        sys.stderr = stream


ensure_runtime_streams()

CONTENT_ROOT = PROJECT_ROOT / "content"
STATIC_ROOT = PROJECT_ROOT / "static"
PUBLIC_ROOT = PROJECT_ROOT / "public"
UPLOAD_ROOT = STATIC_ROOT / "uploads"
FILE_UPLOAD_ROOT = STATIC_ROOT / "files"
BACKUP_ROOT = ADMIN_ROOT / "backups"
TRASH_ROOT = ADMIN_ROOT / "trash"
TRASH_DELETE_UNDO_ROOT = ADMIN_ROOT / "trash_delete_undo"
MEDIA_TRASH_ROOT = ADMIN_ROOT / "media_trash"
DEPLOY_TMP_ROOT = ADMIN_ROOT / "deploy_tmp"
DEPLOY_CONFIG_PATH = ADMIN_ROOT / "deploy_config.local.json"
UI_ROOT = ADMIN_ROOT / "static"
CHROME_PATH = PROJECT_ROOT / "data" / "chrome.json"
HUGO_CONFIG_PATH = PROJECT_ROOT / "hugo.toml"
ADMIN_BUILDER_SCROLL_FIX_MARKER = "data-seoimpuls-admin-builder-scrollfix"
ADMIN_BUILDER_SCROLL_FIX_STYLE = (
    f'<style {ADMIN_BUILDER_SCROLL_FIX_MARKER}>'
    ".seo-builder{scrollbar-width:none!important;-ms-overflow-style:none!important;overscroll-behavior:none!important}"
    ".seo-builder::-webkit-scrollbar{display:none!important;width:0!important;height:0!important}"
    "</style>"
)
ADMIN_BUILDER_SCROLL_FIX_SCRIPT = (
    f'<script {ADMIN_BUILDER_SCROLL_FIX_MARKER}>'
    "(function(){"
    "function f(){document.querySelectorAll('.seo-builder').forEach(function(b){"
    "b.style.setProperty('overflow-x','clip','important');"
    "b.style.setProperty('overflow-y','hidden','important');"
    "b.style.setProperty('scrollbar-width','none','important');"
    "b.style.setProperty('overscroll-behavior','none','important');"
    "b.scrollTop=0;b.scrollLeft=0;"
    "});}"
    "function r(){f();setTimeout(f,60);setTimeout(f,240);}"
    "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',r,{once:true});else r();"
    "window.addEventListener('load',r,{passive:true});"
    "window.addEventListener('resize',r,{passive:true});"
    "})();"
    "</script>"
)

LANGS = ("en", "ru", "es")
SECTION_ALIASES = {
    "услуги": "services",
    "сервис": "services",
    "сервисы": "services",
    "link-building-services": "services",
    "uslugi-linkbildinga": "services",
    "servicios-de-link-building": "services",
    "bases": "bases",
    "bazy": "bases",
    "базы": "bases",
    "база": "bases",
    "новости": "news",
    "новость": "news",
    "блог": "blog",
    "статьи": "blog",
    "статья": "blog",
    "ресурсы": "resources",
    "частые-вопросы": "faq",
    "вопросы": "faq",
    "о-нас": "about",
}

DEFAULT_LEGAL_LINKS = {
    "en": [
        {"key": "privacy", "label": "Privacy Policy", "url": "/privacy-policy/", "enabled": True},
        {"key": "cookie", "label": "Cookie Policy", "url": "/cookie-policy/", "enabled": True},
        {"key": "terms", "label": "Terms of Service", "url": "/terms-of-service/", "enabled": True},
        {"key": "cookie-settings", "label": "Cookie Settings", "url": "/cookie-policy/", "enabled": True, "cookieSettings": True},
    ],
    "ru": [
        {"key": "privacy", "label": "Политика конфиденциальности", "url": "/privacy-policy/", "enabled": True},
        {"key": "cookie", "label": "Политика cookie", "url": "/cookie-policy/", "enabled": True},
        {"key": "terms", "label": "Условия сервиса", "url": "/terms-of-service/", "enabled": True},
        {"key": "cookie-settings", "label": "Настройки cookie", "url": "/cookie-policy/", "enabled": True, "cookieSettings": True},
    ],
    "es": [
        {"key": "privacy", "label": "Política de Privacidad", "url": "/privacy-policy/", "enabled": True},
        {"key": "cookie", "label": "Política de Cookies", "url": "/cookie-policy/", "enabled": True},
        {"key": "terms", "label": "Términos del Servicio", "url": "/terms-of-service/", "enabled": True},
        {"key": "cookie-settings", "label": "Configuración de Cookies", "url": "/cookie-policy/", "enabled": True, "cookieSettings": True},
    ],
}
LEGAL_PAGE_KEYS = {"privacy-policy", "cookie-policy", "terms-of-service"}
PROTECTED_PAGE_KEYS = {"strategy-builder"}
HOME_FEED_SECTIONS = {"services", "news", "blog"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".bmp", ".tif", ".tiff", ".svg", ".gif", ".ico"}
DOWNLOAD_FILE_SUFFIXES = {".txt", ".csv", ".json", ".xml", ".zip", ".rar", ".7z", ".tar", ".gz"}
SITE_TEXT_SUFFIXES = {".md", ".html", ".htm", ".json", ".toml", ".yaml", ".yml", ".css", ".js", ".ts", ".scss", ".txt", ".xml", ".svg"}
AUTO_IMAGE_SKIP_SUFFIXES = {".svg", ".gif", ".ico", ".avif"}
AUTO_IMAGE_MAX_BYTES = 220 * 1024
AUTO_IMAGE_MAX_SIDE = 1200
AUTO_IMAGE_QUALITY = 72
IDEAL_PAGE_TOTAL_BYTES = 180 * 1024
IDEAL_PAGE_IMAGE_BYTES = 120 * 1024
IDEAL_SINGLE_IMAGE_BYTES = 80 * 1024
IDEAL_SINGLE_ASSET_BYTES = 120 * 1024
IDEAL_RESOURCE_COUNT = 20
LOCAL_IMAGE_URL_RE = re.compile(
    r"(?P<url>(?:https?://(?:localhost|127(?:\.\d{1,3}){3}|seoimpuls\.com|www\.seoimpuls\.com))?/"
    r"[^\\\s\"'<>)]*?\.(?:png|jpe?g|webp|bmp|tiff?))(?:\?[^\\\s\"'<>)]*)?",
    re.IGNORECASE,
)
HUGO_PROCESS: subprocess.Popen | None = None
HUGO_PORT: int | None = None
HUGO_PREVIEW_PORTS = set(range(1314, 1330))
ADMIN_PASSWORD = os.environ.get("SEOIMPULS_ADMIN_PASSWORD", "").strip()
AUTH_ENABLED = bool(ADMIN_PASSWORD)
SESSION_COOKIE_NAME = "seoimpuls_admin_session"
PAGE_SAVE_LOCK = threading.RLock()

DEFAULT_DEPLOY_CONFIG = {
    "host": "87.199.197.223",
    "port": 22,
    "username": "root",
    "password": "",
    "remoteBase": "/var/www/fastuser/data/www/seoimpuls.com",
    "domain": "https://seoimpuls.com/",
    "keepReleases": 5,
}


def json_response(handler: BaseHTTPRequestHandler, payload: object, status: int = 200) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:1314")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def text_response(handler: BaseHTTPRequestHandler, text: str, status: int = 200, content_type: str = "text/plain") -> None:
    data = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", f"{content_type}; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:1314")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def error_response(handler: BaseHTTPRequestHandler, message: str, status: int = 400) -> None:
    json_response(handler, {"ok": False, "error": message}, status)


def read_body(handler: BaseHTTPRequestHandler) -> bytes:
    length = int(handler.headers.get("Content-Length", "0") or "0")
    return handler.rfile.read(length) if length else b""


def read_json(handler: BaseHTTPRequestHandler) -> dict:
    raw = read_body(handler)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8-sig"))


def read_post_payload(handler: BaseHTTPRequestHandler) -> dict:
    raw = read_body(handler)
    if not raw:
        return {}
    content_type = handler.headers.get("Content-Type", "")
    text = raw.decode("utf-8-sig")
    if "application/x-www-form-urlencoded" in content_type:
        parsed = urllib.parse.parse_qs(text, keep_blank_values=True)
        return {key: values[-1] if values else "" for key, values in parsed.items()}
    if "application/json" in content_type:
        return json.loads(text)
    return {}


def auth_session_token() -> str:
    return hashlib.sha256(f"seoimpuls-admin:{ADMIN_PASSWORD}".encode("utf-8")).hexdigest()


def parse_cookies(header: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for chunk in header.split(";"):
        if "=" not in chunk:
            continue
        key, value = chunk.split("=", 1)
        result[key.strip()] = urllib.parse.unquote(value.strip())
    return result


def is_authenticated(handler: BaseHTTPRequestHandler) -> bool:
    if not AUTH_ENABLED:
        return True
    cookies = parse_cookies(handler.headers.get("Cookie", ""))
    return hmac.compare_digest(cookies.get(SESSION_COOKIE_NAME, ""), auth_session_token())


def login_html(error: str = "") -> str:
    error_block = f"<p class='error'>{error}</p>" if error else ""
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SeoImpuls Backup Admin</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background:
        radial-gradient(circle at 35% 18%, rgba(47, 166, 214, .25), transparent 34%),
        linear-gradient(145deg, #040812 0%, #071221 52%, #090b16 100%);
      color: #e8f2ff;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .card {{
      width: min(390px, calc(100vw - 32px));
      box-sizing: border-box;
      padding: 28px;
      border: 1px solid rgba(122, 211, 255, .35);
      border-radius: 14px;
      background: rgba(6, 14, 30, .84);
      box-shadow: 0 24px 70px rgba(0, 0, 0, .42), inset 0 0 0 1px rgba(255, 255, 255, .04);
    }}
    .mark {{
      width: 72px;
      height: 72px;
      margin-bottom: 18px;
      display: grid;
      place-items: center;
      border-radius: 18px;
      background: linear-gradient(135deg, #163b8f, #16a8c7 58%, #a6f2ff);
      box-shadow: 0 0 30px rgba(74, 200, 255, .35);
      color: #04111f;
      font-weight: 900;
      font-size: 28px;
      letter-spacing: -2px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 25px; line-height: 1.15; }}
    p {{ margin: 0 0 20px; color: rgba(222, 236, 255, .74); line-height: 1.45; }}
    label {{ display: grid; gap: 7px; margin-bottom: 16px; color: rgba(230, 241, 255, .86); font-weight: 700; }}
    input {{
      min-height: 46px;
      box-sizing: border-box;
      border: 1px solid rgba(127, 180, 224, .45);
      border-radius: 9px;
      padding: 0 13px;
      background: rgba(3, 9, 20, .8);
      color: #fff;
      font: inherit;
      outline: none;
    }}
    input:focus {{ border-color: #75d4ff; box-shadow: 0 0 0 3px rgba(117, 212, 255, .18); }}
    button {{
      width: 100%;
      min-height: 48px;
      border: 0;
      border-radius: 9px;
      background: linear-gradient(135deg, #1d78b6, #24b8c6);
      color: white;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
    }}
    .error {{
      margin: 0 0 14px;
      padding: 10px 12px;
      border: 1px solid rgba(255, 99, 132, .55);
      border-radius: 8px;
      background: rgba(141, 16, 52, .28);
      color: #ffd8e1;
    }}
  </style>
</head>
<body>
  <form class="card" method="post" action="/login">
    <div class="mark">S↯</div>
    <h1>SeoImpuls Backup Admin</h1>
    <p>Локальный защищённый запуск админки из exe.</p>
    {error_block}
    <label>Пароль
      <input name="password" type="password" autocomplete="current-password" autofocus>
    </label>
    <button type="submit">Войти</button>
  </form>
</body>
</html>"""


def local_port_is_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.2)
        return probe.connect_ex(("127.0.0.1", port)) == 0


def safe_join(base: Path, rel: str) -> Path:
    rel = rel.replace("\\", "/").lstrip("/")
    target = (base / rel).resolve()
    base_resolved = base.resolve()
    if target != base_resolved and base_resolved not in target.parents:
        raise ValueError("Path is outside allowed directory")
    return target


def content_path(rel: str) -> Path:
    return safe_join(PROJECT_ROOT, rel)


def guess_language(path: Path) -> str:
    name = path.name.lower()
    if name.endswith(".ru.md"):
        return "ru"
    if name.endswith(".es.md"):
        return "es"
    return "en"


def page_key(path: Path) -> str:
    rel = path.relative_to(CONTENT_ROOT).as_posix()
    rel = re.sub(r"/?_index(\.[a-z]{2})?\.md$", "", rel)
    rel = re.sub(r"/?index(\.[a-z]{2})?\.md$", "", rel)
    return rel or "home"


def page_section(path: Path) -> str:
    rel_parts = path.relative_to(CONTENT_ROOT).parts
    if len(rel_parts) == 1:
        return "home"
    return rel_parts[0]


def is_section_index(path: Path) -> bool:
    return path.name.lower().startswith("_index")


def normalize_public_url(value: str) -> str:
    clean = "/" + str(value or "").strip().strip("/")
    return "/" if clean == "/" else clean + "/"


def menu_keys_for_lang(lang: str) -> set[str]:
    try:
        menu = load_menu()
    except Exception:
        return set()
    keys: set[str] = set()
    for item in menu.get(lang, []):
        url = normalize_public_url(str(item.get("url") or ""))
        keys.add("home" if url == "/" else url.strip("/").split("/", 1)[0])
    return keys


def page_visibility(path: Path, front: dict, menu_keys: set[str]) -> str:
    if bool(front.get("draft", False)):
        return "draft"
    key = page_key(path)
    root_key = "home" if key == "home" else key.split("/", 1)[0]
    if root_key in menu_keys:
        return "menu"
    if root_key in LEGAL_PAGE_KEYS:
        return "footer"
    return "site"


def page_public_path(key: str, lang: str) -> str:
    lang_prefix = "/" if lang == "en" else f"/{lang}/"
    if key == "home":
        return lang_prefix
    return f"{lang_prefix}{key.strip('/')}/"


def page_front_public_url(front: dict, key: str, lang: str) -> str:
    raw_url = str(front.get("url") or "").strip()
    if raw_url:
        return normalize_public_url(raw_url)
    return page_public_path(key, lang)


def normalize_internal_public_path(value: str) -> str:
    raw = str(value or "").strip().strip('"\'')
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:")):
        return ""
    if raw.startswith("//"):
        return ""
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme:
        host = (parsed.netloc or "").lower()
        if parsed.scheme not in {"http", "https"}:
            return ""
        if host and not (host.startswith("127.0.0.1") or host.startswith("localhost") or "seoimpuls" in host):
            return ""
        path = parsed.path or "/"
    elif raw.startswith("/"):
        path = raw.split("?", 1)[0].split("#", 1)[0]
    else:
        return ""
    path = urllib.parse.unquote(path).replace("\\", "/")
    path = re.sub(r"/+", "/", path)
    if not path.startswith("/"):
        path = "/" + path
    if "." in Path(path).name:
        return ""
    return normalize_public_url(path)


def internal_public_links(front: dict, body: str) -> set[str]:
    source = json.dumps(front, ensure_ascii=False) + "\n" + str(body or "")
    candidates = re.findall(r"https?://[^\s\"'<>)]+|/[^\s\"'<>)]+", source)
    links: set[str] = set()
    for candidate in candidates:
        clean = candidate.rstrip(".,;:")
        path = normalize_internal_public_path(clean)
        if path:
            links.add(path)
    return links


def page_delete_block_reason(path: Path) -> str:
    target_key = page_key(path)
    target_lang = guess_language(path)
    if target_key == "home":
        return "Главная защищена от удаления"
    if target_key in PROTECTED_PAGE_KEYS:
        return "Страница защищена от удаления"
    page_records: list[dict] = []
    for other in sorted(CONTENT_ROOT.rglob("*.md")):
        try:
            front, body, _ = read_markdown(other)
        except Exception:
            front, body = {}, ""
        key = page_key(other)
        lang = guess_language(other)
        page_records.append(
            {
                "path": other,
                "key": key,
                "language": lang,
                "url": page_front_public_url(front, key, lang),
                "front": front,
                "body": body,
            }
        )
    for record in page_records:
        if record["path"] == path:
            continue
        if record["language"] == target_lang and str(record["key"]).startswith(f"{target_key}/"):
            return "У страницы есть дочерние страницы"
    return ""


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        return [parse_scalar(part.strip()) for part in body.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        if value.startswith('"'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def parse_builder_json_blocks(value):
    if isinstance(value, list):
        return value
    raw = str(value or "").strip()
    if not raw:
        return []
    candidates: list[str] = []

    def add_candidate(candidate) -> None:
        text = str(candidate or "").strip()
        if text and text not in candidates:
            candidates.append(text)

    add_candidate(raw)
    current = raw
    for _index in range(3):
        try:
            parsed = json.loads(current)
        except Exception:
            break
        if isinstance(parsed, list):
            return parsed
        if not isinstance(parsed, str):
            break
        add_candidate(parsed)
        current = parsed
    for candidate in list(candidates):
        if '\\"' in candidate:
            add_candidate(candidate.replace('\\"', '"'))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except Exception:
            continue
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, str):
            try:
                nested = json.loads(parsed)
            except Exception:
                continue
            if isinstance(nested, list):
                return nested
    return None


def normalize_builder_json_value(value, strict: bool = False) -> str:
    raw = str(value or "").strip() if not isinstance(value, list) else ""
    blocks = parse_builder_json_blocks(value)
    if blocks is None or any(not isinstance(block, dict) for block in blocks):
        if strict:
            raise ValueError("builderJson is not valid JSON")
        return raw
    return json.dumps(blocks, ensure_ascii=False, separators=(",", ":"))


def normalize_front_builder_json(front: dict, strict: bool = False) -> dict:
    if isinstance(front, dict) and "builderJson" in front:
        front["builderJson"] = normalize_builder_json_value(front.get("builderJson"), strict=strict)
    return front


def dump_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(dump_scalar(item) for item in value) + "]"
    text = "" if value is None else str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def dump_block_scalar(value) -> list[str]:
    text = "" if value is None else str(value)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return ["  " + line for line in normalized.split("\n")]


def parse_front_matter(text: str) -> tuple[dict, str]:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    data: dict = {}
    current_key = ""
    current_list: list[str] | None = None
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.strip().startswith("#"):
            continue
        if current_key and line.startswith("  - "):
            if current_list is not None:
                current_list.append(parse_scalar(line[4:]))
            continue
        current_key = ""
        current_list = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_key = key
            current_list = data[key]
        elif value in (">", ">-", "|", "|-"):
            block_lines: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if next_line.startswith((" ", "\t")):
                    block_lines.append(next_line.lstrip())
                    index += 1
                    continue
                break
            data[key] = "\n".join(block_lines) if value.startswith("|") else " ".join(block_lines)
        else:
            data[key] = parse_scalar(value)
    return data, body


def dump_front_matter(front: dict, body: str) -> str:
    lines = ["---"]
    preferred = [
        "title",
        "description",
        "slug",
        "translationKey",
        "date",
        "lastmod",
        "draft",
        "showOnHome",
        "tags",
        "image",
        "images",
        "author",
    ]
    keys = [key for key in preferred if key in front]
    keys.extend([key for key in front.keys() if key not in keys])
    for key in keys:
        value = front.get(key)
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {dump_scalar(item)}")
        elif isinstance(value, str) and ("\n" in value or "\r" in value):
            lines.append(f"{key}: |-")
            lines.extend(dump_block_scalar(value))
        else:
            lines.append(f"{key}: {dump_scalar(value)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + body.lstrip("\n")


def read_markdown(path: Path) -> tuple[dict, str, str]:
    text = path.read_text(encoding="utf-8-sig")
    front, body = parse_front_matter(text)
    return front, body, text


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = time.strftime("%Y%m%d-%H%M%S")
    rel = path.relative_to(PROJECT_ROOT)
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    target = Path(tempfile.mkdtemp(prefix=stamp + "-", dir=BACKUP_ROOT)) / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    return target


def markdown_revision(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write_markdown(path: Path, text: str) -> None:
    # A reader must see either the previous file or the complete replacement.
    fd, name = tempfile.mkstemp(prefix=".admin-save-", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def clean_empty_dirs(path: Path, stop_at: Path) -> None:
    stop = stop_at.resolve()
    current = path.resolve()
    while current != stop and stop in current.parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def ensure_content_file(path: Path) -> None:
    content_root = CONTENT_ROOT.resolve()
    resolved = path.resolve()
    if content_root != resolved and content_root not in resolved.parents:
        raise ValueError("Page path is outside content")
    if path.suffix.lower() != ".md":
        raise ValueError("Only markdown pages can be changed")


def is_home_page(path: Path) -> bool:
    try:
        return page_key(path) == "home"
    except ValueError:
        return False


def home_feed_eligible(path: Path, front: dict) -> bool:
    key = page_key(path)
    if key == "home":
        return False
    return front.get("showOnHome") is True


def ensure_home_feed_date(path: Path, front: dict) -> None:
    if home_feed_eligible(path, front) and not str(front.get("date") or "").strip():
        front["date"] = time.strftime("%Y-%m-%d")


def list_pages() -> list[dict]:
    pages: list[dict] = []
    if not CONTENT_ROOT.exists():
        return pages
    menu_keys = {lang: menu_keys_for_lang(lang) for lang in LANGS}
    records: list[dict] = []
    for path in sorted(CONTENT_ROOT.rglob("*.md")):
        try:
            front, body, _ = read_markdown(path)
        except UnicodeDecodeError:
            front, body = {}, ""
        key = page_key(path)
        lang = guess_language(path)
        records.append(
            {
                "path_obj": path,
                "path": path.relative_to(PROJECT_ROOT).as_posix(),
                "key": key,
                "section": page_section(path),
                "language": lang,
                "front": front,
                "body": body,
                "url": page_front_public_url(front, key, lang),
            }
        )
    for record in records:
        path = record["path_obj"]
        front = record["front"]
        body = record["body"]
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        title = str(front.get("title") or path.stem)
        description = str(front.get("description") or "")
        lang = record["language"]
        key = record["key"]
        has_child_pages = any(
            other["path_obj"] != path
            and other["language"] == lang
            and str(other["key"]).startswith(f"{key}/")
            for other in records
        )
        delete_block_reason = ""
        if is_home_page(path):
            delete_block_reason = "Главная защищена от удаления"
        elif key in PROTECTED_PAGE_KEYS:
            delete_block_reason = "Страница защищена от удаления"
        elif has_child_pages:
            delete_block_reason = "У страницы есть дочерние страницы"
        pages.append(
            {
                "path": rel,
                "key": key,
                "section": record["section"],
                "language": lang,
                "title": title,
                "description": description,
                "url": record["url"],
                "translationKey": front.get("translationKey", ""),
                "slug": front.get("slug", ""),
                "draft": bool(front.get("draft", False)),
                "showOnHome": front.get("showOnHome") is True,
                "date": front.get("date", ""),
                "visibility": page_visibility(path, front, menu_keys.get(lang, set())),
                "deletable": not delete_block_reason,
                "deleteBlockReason": delete_block_reason,
                "words": len(re.findall(r"\w+", body, flags=re.UNICODE)),
                "modified": path.stat().st_mtime,
            }
        )
    return pages


def site_text_documents(exclude: Path | None = None, include_public: bool = True) -> list[tuple[str, str]]:
    documents: list[tuple[str, str]] = []
    roots = [
        CONTENT_ROOT,
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "layouts",
        STATIC_ROOT,
        PROJECT_ROOT / "assets",
    ]
    if include_public:
        roots.append(PUBLIC_ROOT)
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in SITE_TEXT_SUFFIXES)
    if HUGO_CONFIG_PATH.exists():
        files.append(HUGO_CONFIG_PATH)
    excluded = exclude.resolve() if exclude else None
    for path in sorted(set(files)):
        try:
            if excluded and path.resolve() == excluded:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        documents.append((path.relative_to(PROJECT_ROOT).as_posix(), text))
    return documents


def asset_public_url(path: Path) -> str:
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    if rel.startswith("static/"):
        return "/" + rel.removeprefix("static/")
    return ""


def asset_reference_tokens(path: Path, public_url: str) -> set[str]:
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    tokens = {rel, rel.replace("/", "\\")}
    if rel.startswith("static/"):
        tokens.add(rel.removeprefix("static/"))
    if rel.startswith("assets/"):
        tokens.add(rel.removeprefix("assets/"))
    if public_url:
        tokens.update(
            {
                public_url,
                public_url.lstrip("/"),
                urllib.parse.quote(public_url, safe="/:-_.?=&%"),
                urllib.parse.quote(public_url.lstrip("/"), safe="/:-_.?=&%"),
            }
        )
    return {token for token in tokens if token}


def asset_usage_sources(path: Path, public_url: str, documents: list[tuple[str, str]] | None = None) -> list[str]:
    docs = documents if documents is not None else site_text_documents(exclude=path)
    tokens = asset_reference_tokens(path, public_url)
    sources: list[str] = []
    for source, text in docs:
        if any(token in text for token in tokens):
            sources.append(source)
    return sources


def asset_file_from_rel(asset_rel: str) -> Path:
    target = safe_join(PROJECT_ROOT, asset_rel)
    static_root = STATIC_ROOT.resolve()
    assets_root = (PROJECT_ROOT / "assets").resolve()
    resolved = target.resolve()
    if not (
        static_root == resolved
        or static_root in resolved.parents
        or assets_root == resolved
        or assets_root in resolved.parents
    ):
        raise ValueError("Asset path is outside static/assets")
    if target.suffix.lower() not in IMAGE_SUFFIXES:
        raise ValueError("Only image assets can be deleted")
    return target


def asset_file_from_url_or_rel(value: str) -> Path:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("Image path is empty")
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme in {"http", "https"}:
        host = (parsed.hostname or "").lower()
        local_hosts = {"localhost", "seoimpuls.com", "www.seoimpuls.com"}
        if host not in local_hosts and not host.startswith("127."):
            raise ValueError("Можно сжимать только локальные картинки сайта")
    elif parsed.scheme and parsed.scheme != "file":
        raise ValueError("Можно сжимать только локальные картинки сайта")
    path_value = urllib.parse.unquote(parsed.path or raw).replace("\\", "/").lstrip("/")
    if path_value.startswith("public/"):
        path_value = path_value.removeprefix("public/")
    if not path_value.startswith(("static/", "assets/")):
        static_candidate = STATIC_ROOT / path_value
        assets_candidate = PROJECT_ROOT / "assets" / path_value
        if static_candidate.exists():
            path_value = "static/" + path_value
        elif assets_candidate.exists():
            path_value = "assets/" + path_value
        else:
            path_value = "static/" + path_value
    return asset_file_from_rel(path_value)


def unique_upload_target(stem: str, suffix: str) -> Path:
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    base = slugify(stem) or "image"
    stamp = int(time.time())
    target = UPLOAD_ROOT / f"{base}-{stamp}{suffix}"
    if not target.exists():
        return target
    for index in range(2, 1000):
        candidate = UPLOAD_ROOT / f"{base}-{stamp}-{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise ValueError("Cannot create unique image filename")


def unique_file_upload_target(stem: str, suffix: str) -> Path:
    FILE_UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    base = slugify(stem) or "file"
    stamp = int(time.time())
    target = FILE_UPLOAD_ROOT / f"{base}-{stamp}{suffix}"
    if not target.exists():
        return target
    for index in range(2, 1000):
        candidate = FILE_UPLOAD_ROOT / f"{base}-{stamp}-{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise ValueError("Cannot create unique file name")


def upload_download_file(payload: dict) -> dict:
    source_name = str(payload.get("filename") or "file").strip()
    suffix = Path(source_name).suffix.lower()
    if suffix not in DOWNLOAD_FILE_SUFFIXES:
        raise ValueError("Можно загрузить только архив или текстовый файл")
    data_url = str(payload.get("dataUrl") or "")
    match = re.match(r"^data:[^;]+;base64,(.+)$", data_url)
    if not match:
        raise ValueError("Expected base64 dataUrl")
    target = unique_file_upload_target(Path(source_name).stem, suffix)
    target.write_bytes(base64.b64decode(match.group(1)))
    rel = target.relative_to(PROJECT_ROOT).as_posix()
    updated_at = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(target.stat().st_mtime))
    if len(updated_at) > 2:
        updated_at = f"{updated_at[:-2]}:{updated_at[-2:]}"
    return {
        "path": rel,
        "url": "/" + rel.removeprefix("static/"),
        "name": target.name,
        "size": target.stat().st_size,
        "updatedAt": updated_at,
    }


def upload_download_file_stream(handler: BaseHTTPRequestHandler, source_name: str) -> dict:
    source_name = str(source_name or "file").strip() or "file"
    suffix = Path(source_name).suffix.lower()
    if suffix not in DOWNLOAD_FILE_SUFFIXES:
        raise ValueError("Можно загрузить только архив или текстовый файл")
    try:
        remaining = int(handler.headers.get("Content-Length", "0") or "0")
    except ValueError:
        remaining = 0
    if remaining <= 0:
        raise ValueError("Файл пустой или не передан")
    target = unique_file_upload_target(Path(source_name).stem, suffix)
    with target.open("wb") as handle:
        while remaining > 0:
            chunk = handler.rfile.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            handle.write(chunk)
            remaining -= len(chunk)
    if remaining > 0:
        try:
            target.unlink()
        except OSError:
            pass
        raise ValueError("Загрузка файла оборвалась")
    rel = target.relative_to(PROJECT_ROOT).as_posix()
    updated_at = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(target.stat().st_mtime))
    if len(updated_at) > 2:
        updated_at = f"{updated_at[:-2]}:{updated_at[-2:]}"
    return {
        "path": rel,
        "url": "/" + rel.removeprefix("static/"),
        "name": target.name,
        "size": target.stat().st_size,
        "updatedAt": updated_at,
    }


COMPRESSOR_VARIANT_RE = re.compile(r"(?:-q\d+-\d{9,})+$")


def compressor_canonical_stem(stem: str) -> str:
    return COMPRESSOR_VARIANT_RE.sub("", stem)


def is_compressor_variant(path: Path) -> bool:
    return compressor_canonical_stem(path.stem) != path.stem


def repair_missing_asset_url(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return raw
    try:
        target = asset_file_from_url_or_rel(raw)
    except Exception:
        return raw
    if target.exists() and target.is_file():
        return raw
    if target.suffix.lower() not in IMAGE_SUFFIXES:
        return raw
    parent = target.parent
    if not parent.exists() or not parent.is_dir():
        return raw
    canonical = compressor_canonical_stem(target.stem)
    candidates: list[Path] = []
    for candidate in parent.glob(f"{canonical}*"):
        if (
            candidate.is_file()
            and candidate.suffix.lower() in IMAGE_SUFFIXES
            and not candidate.name.startswith(".")
            and compressor_canonical_stem(candidate.stem) == canonical
        ):
            candidates.append(candidate)
    if not candidates:
        return raw
    target_suffix = target.suffix.lower()
    candidates.sort(
        key=lambda path: (
            0 if path.suffix.lower() == target_suffix else 1,
            0 if path.suffix.lower() == ".webp" else 1,
            -path.stat().st_mtime,
        )
    )
    repaired = asset_public_url(candidates[0])
    return repaired or raw


def repair_missing_builder_image_urls(front: dict) -> dict:
    report = {"count": 0, "items": []}

    def repair_value(value: object) -> object:
        if not isinstance(value, str) or not value.strip():
            return value
        repaired = repair_missing_asset_url(value)
        if repaired != value:
            report["count"] += 1
            report["items"].append({"from": value, "to": repaired})
        return repaired

    def walk(value: object) -> object:
        if isinstance(value, dict):
            next_value = {}
            for key, item in value.items():
                if key in {"image", "images"}:
                    next_value[key] = walk(repair_value(item) if isinstance(item, str) else item)
                elif key in {"imageLink", "url", "href"}:
                    next_value[key] = item
                else:
                    next_value[key] = walk(item)
            return next_value
        if isinstance(value, list):
            return [walk(item) for item in value]
        return value

    builder_json = str(front.get("builderJson") or "").strip()
    if builder_json:
        blocks = parse_builder_json_blocks(builder_json)
        if isinstance(blocks, list):
            repaired_blocks = walk(blocks)
            if repaired_blocks != blocks:
                front["builderJson"] = json.dumps(repaired_blocks, ensure_ascii=False, separators=(",", ":"))
    if isinstance(front.get("image"), str):
        front["image"] = repair_value(front["image"])
    if isinstance(front.get("images"), list):
        front["images"] = [repair_value(item) for item in front["images"]]
    return report


def cleanup_unused_compressor_variants() -> dict:
    documents = site_text_documents(include_public=False)
    removed: list[str] = []
    kept: list[str] = []
    bytes_removed = 0
    for root in [STATIC_ROOT, PROJECT_ROOT / "assets"]:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            if not is_compressor_variant(path):
                continue
            public_url = asset_public_url(path)
            if asset_usage_sources(path, public_url, documents):
                kept.append(path.relative_to(PROJECT_ROOT).as_posix())
                continue
            try:
                size = path.stat().st_size
                path.unlink()
                bytes_removed += size
                removed.append(path.relative_to(PROJECT_ROOT).as_posix())
            except OSError:
                continue
    return {
        "removed": len(removed),
        "bytesRemoved": bytes_removed,
        "removedPaths": removed[:50],
        "kept": len(kept),
    }


def compressor_target_for(source: Path, quality: int) -> Path:
    canonical_stem = compressor_canonical_stem(source.stem)
    stamp = int(time.time() * 1000)
    for index in range(0, 1000):
        suffix = f"-{index}" if index else ""
        candidate = source.with_name(f"{canonical_stem}-q{quality}-{stamp}{suffix}.webp")
        if candidate.resolve() != source.resolve() and not candidate.exists():
            return candidate
    raise ValueError("Не удалось создать имя для сжатой копии")


def cleanup_previous_compressor_variant(payload: dict, source: Path, target: Path) -> str:
    previous_value = str(payload.get("previousUrl") or payload.get("previousPath") or "").strip()
    if not previous_value:
        return ""
    try:
        previous = asset_file_from_url_or_rel(previous_value)
    except Exception:
        return ""
    try:
        previous_resolved = previous.resolve()
        if previous_resolved in {source.resolve(), target.resolve()}:
            return ""
        if not previous.exists() or not previous.is_file() or not is_compressor_variant(previous):
            return ""
        protected_values = payload.get("protectedUrls") or payload.get("protectedPaths") or []
        if isinstance(protected_values, str):
            protected_values = [protected_values]
        for protected_value in protected_values:
            try:
                if asset_file_from_url_or_rel(str(protected_value or "")).resolve() == previous_resolved:
                    return ""
            except Exception:
                continue
        public_url = asset_public_url(previous)
        if asset_usage_sources(previous, public_url):
            return ""
        previous.unlink(missing_ok=True)
        return previous.relative_to(PROJECT_ROOT).as_posix()
    except Exception:
        return ""


def compress_asset(payload: dict) -> dict:
    source = asset_file_from_url_or_rel(str(payload.get("url") or payload.get("path") or ""))
    if not source.exists() or not source.is_file():
        raise ValueError("Image asset not found")
    if source.suffix.lower() in {".svg", ".gif", ".ico"}:
        raise ValueError("SVG/GIF/ICO не пережимаем, чтобы не сломать вектор или анимацию")
    quality = max(1, min(90, int(payload.get("quality") or 76)))
    require_smaller = bool(payload.get("requireSmaller"))
    shrink_factor = max(0.05, min(1.0, float(payload.get("shrinkFactor") or 1)))
    max_side = max(80, min(2400, int(payload.get("maxSide") or 1600)))
    try:
        from PIL import Image, ImageOps
    except Exception as exc:
        raise ValueError("Pillow не установлен, компрессор картинок недоступен") from exc

    original_size = source.stat().st_size
    before_size = original_size
    previous_value = str(payload.get("previousUrl") or payload.get("previousPath") or "").strip()
    if previous_value:
        try:
            previous_for_size = asset_file_from_url_or_rel(previous_value)
            if previous_for_size.exists() and previous_for_size.is_file():
                before_size = previous_for_size.stat().st_size
        except Exception:
            before_size = original_size
    public_source_url = asset_public_url(source)

    def write_attempt(attempt_quality: int, attempt_shrink: float) -> tuple[Path, Path, int, int, float]:
        attempt_target = compressor_target_for(source, attempt_quality)
        attempt_target.parent.mkdir(parents=True, exist_ok=True)
        attempt_temp = attempt_target.with_name(f".{attempt_target.stem}.compress-{int(time.time() * 1000)}.webp")
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened)
            attempt_max_side = max_side
            if attempt_shrink < 1:
                attempt_max_side = max(80, min(attempt_max_side, int(max(image.size) * attempt_shrink)))
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            if max(image.size) > attempt_max_side:
                image.thumbnail((attempt_max_side, attempt_max_side), Image.Resampling.LANCZOS)
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, (7, 11, 20))
                background.paste(image, mask=image.getchannel("A"))
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")
            image.save(attempt_temp, "WEBP", quality=attempt_quality, method=6, optimize=True)
        return attempt_target, attempt_temp, attempt_temp.stat().st_size, attempt_quality, attempt_shrink

    attempts: list[tuple[int, float]] = [(quality, shrink_factor)]
    if require_smaller:
        q = quality
        shrink = shrink_factor
        for _ in range(18):
            if q > 1:
                q = max(1, q - 5)
            else:
                shrink = max(0.05, round(shrink * 0.88, 4))
            candidate = (q, shrink)
            if candidate not in attempts:
                attempts.append(candidate)

    target = temp_target = None
    new_size = before_size
    final_quality = quality
    final_shrink = shrink_factor
    for attempt_quality, attempt_shrink in attempts:
        attempt_target, attempt_temp, attempt_size, used_quality, used_shrink = write_attempt(attempt_quality, attempt_shrink)
        if not require_smaller or attempt_size < before_size:
            target, temp_target = attempt_target, attempt_temp
            new_size = attempt_size
            final_quality = used_quality
            final_shrink = used_shrink
            break
        attempt_temp.unlink(missing_ok=True)

    if target is None or temp_target is None:
        return {
            "path": source.relative_to(PROJECT_ROOT).as_posix(),
            "url": public_source_url,
            "quality": quality,
            "originalPath": source.relative_to(PROJECT_ROOT).as_posix(),
            "originalSize": before_size,
            "size": before_size,
            "keptOriginal": True,
        }
    os.replace(temp_target, target)
    removed_previous = cleanup_previous_compressor_variant(payload, source, target)
    rel = target.relative_to(PROJECT_ROOT).as_posix()
    return {
        "path": rel,
        "url": "/" + rel.removeprefix("static/"),
        "quality": final_quality,
        "shrinkFactor": final_shrink,
        "originalPath": source.relative_to(PROJECT_ROOT).as_posix(),
        "originalSize": before_size,
        "size": new_size,
        "keptOriginal": False,
        "removedPrevious": removed_previous,
    }


def template_image_url(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("Image URL is empty")
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme or parsed.netloc:
        host = (parsed.hostname or "").lower()
        if host not in {"localhost", "seoimpuls.com", "www.seoimpuls.com"} and not host.startswith("127."):
            raise ValueError("Only local site images can be saved")
    path_value = urllib.parse.unquote(parsed.path or raw).replace("\\", "/")
    if path_value.startswith("/site/"):
        path_value = path_value.removeprefix("/site")
    if not path_value.startswith("/"):
        path_value = "/" + path_value
    if not path_value.startswith(("/uploads/", "/assets/")):
        raise ValueError("Only uploads/assets images can be saved")
    suffix = Path(path_value).suffix.lower()
    if suffix not in IMAGE_SUFFIXES or suffix in {".svg", ".gif", ".ico"}:
        raise ValueError("Only raster site images can be saved")
    asset_file_from_url_or_rel(path_value)
    return path_value


def update_services_hub_image(payload: dict) -> dict:
    from_url = template_image_url(str(payload.get("fromUrl") or payload.get("from") or ""))
    to_url = template_image_url(str(payload.get("toUrl") or payload.get("to") or ""))
    if from_url == to_url:
        return {"changed": 0, "fromUrl": from_url, "toUrl": to_url, "backup": "", "updated": []}
    card_url = str(payload.get("cardUrl") or payload.get("url") or "").strip()
    if card_url:
        parsed_card_url = urllib.parse.urlparse(card_url)
        card_url = urllib.parse.unquote(parsed_card_url.path or card_url).replace("\\", "/")
        if card_url.startswith("/site/"):
            card_url = card_url.removeprefix("/site")
        if not card_url.startswith("/"):
            card_url = "/" + card_url
    card_rank = str(payload.get("cardRank") or payload.get("rank") or "").strip()
    page_lang = str(payload.get("lang") or "").strip().lower()

    def replace_in_value(value):
        if isinstance(value, str):
            count = value.count(from_url)
            return value.replace(from_url, to_url), count
        if isinstance(value, list):
            total = 0
            next_items = []
            for item in value:
                next_item, count = replace_in_value(item)
                next_items.append(next_item)
                total += count
            return next_items, total
        if isinstance(value, dict):
            total = 0
            next_items = {}
            for key, item in value.items():
                next_item, count = replace_in_value(item)
                next_items[key] = next_item
                total += count
            return next_items, total
        return value, 0

    candidates: list[Path] = []
    page_path = str(payload.get("pagePath") or payload.get("path") or "").strip()
    if page_path:
        page_target = content_path(page_path)
        if page_target.exists() and page_target.suffix.lower() == ".md":
            try:
                page_target.resolve().relative_to((CONTENT_ROOT / "services").resolve())
            except ValueError as exc:
                raise ValueError("Only services pages can be updated by this endpoint") from exc
            candidates.append(page_target)
    else:
        candidates.extend(sorted((CONTENT_ROOT / "services").glob("_index*.md")))

    updated: list[dict] = []
    total_changed = 0
    for target in candidates:
        front, body, _raw = read_markdown(target)
        next_front, front_changed = replace_in_value(front)
        next_body, body_changed = replace_in_value(body)
        changed = front_changed + body_changed
        if not changed and card_url:
            builder_json = str(next_front.get("builderJson") or "").strip()
            if builder_json:
                blocks = parse_builder_json_blocks(builder_json)
                if isinstance(blocks, list):
                    for block in blocks:
                        if not isinstance(block, dict):
                            continue
                        if str(block.get("type") or "") != "image":
                            continue
                        block_link = str(block.get("imageLink") or "").strip()
                        parsed_block_link = urllib.parse.urlparse(block_link)
                        block_link = urllib.parse.unquote(parsed_block_link.path or block_link).replace("\\", "/")
                        if block_link.startswith("/site/"):
                            block_link = block_link.removeprefix("/site")
                        if not block_link.startswith("/"):
                            block_link = "/" + block_link
                        if block_link == card_url and block.get("image") != to_url:
                            block["image"] = to_url
                            next_front["builderJson"] = json.dumps(blocks, ensure_ascii=False, separators=(",", ":"))
                            changed += 1
                            break
        if not changed:
            continue
        backup = backup_file(target)
        target.write_text(dump_front_matter(next_front, next_body), encoding="utf-8")
        total_changed += changed
        updated.append(
            {
                "path": target.relative_to(PROJECT_ROOT).as_posix(),
                "changed": changed,
                "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
            }
        )

    template = PROJECT_ROOT / "layouts" / "partials" / "services-hub.html"
    text = template.read_text(encoding="utf-8")
    template_changed = text.count(from_url)
    if template_changed:
        backup = backup_file(template)
        template.write_text(text.replace(from_url, to_url), encoding="utf-8")
        total_changed += template_changed
        updated.append(
            {
                "path": template.relative_to(PROJECT_ROOT).as_posix(),
                "changed": template_changed,
                "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
            }
        )
    elif card_rank:
        rank_pattern = re.compile(
            rf'(\{{\{{- if eq \$buttonRankGroup {re.escape(card_rank)} -\}}\}}.*?\{{\{{- end -\}}\}})',
            re.DOTALL,
        )
        rank_match = rank_pattern.search(text)
        if rank_match:
            rank_block = rank_match.group(1)
            if not page_lang and page_path:
                if ".ru." in page_path or page_path.endswith(".ru.md"):
                    page_lang = "ru"
                elif ".es." in page_path or page_path.endswith(".es.md"):
                    page_lang = "es"
                else:
                    page_lang = "en"
            next_block = rank_block
            if page_lang == "ru":
                next_block = re.sub(r'(cond \(eq \$lang "ru"\) )"[^"]*"', rf'\1"{to_url}"', next_block, count=1)
            elif page_lang == "es":
                next_block = re.sub(r'(cond \(eq \$lang "es"\) )"[^"]*"', rf'\1"{to_url}"', next_block, count=1)
            else:
                next_block = re.sub(
                    r'(" /uploads/[^"]*"\) -\}\}\{\{- end -\}\})$',
                    lambda match: match.group(0).replace(match.group(1), f'"{to_url}") -}}}}{{{{- end -}}}}'),
                    next_block,
                    count=1,
                )
            if next_block != rank_block:
                backup = backup_file(template)
                template.write_text(text[: rank_match.start(1)] + next_block + text[rank_match.end(1) :], encoding="utf-8")
                total_changed += 1
                updated.append(
                    {
                        "path": template.relative_to(PROJECT_ROOT).as_posix(),
                        "changed": 1,
                        "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
                    }
                )

    public_changed = 0
    if PUBLIC_ROOT.exists():
        for built_page in PUBLIC_ROOT.rglob("*.html"):
            try:
                built_text = built_page.read_text(encoding="utf-8")
            except Exception:
                continue
            count = built_text.count(from_url)
            if not count:
                continue
            built_page.write_text(built_text.replace(from_url, to_url), encoding="utf-8")
            public_changed += count
    if public_changed:
        total_changed += public_changed
        updated.append({"path": PUBLIC_ROOT.relative_to(PROJECT_ROOT).as_posix(), "changed": public_changed, "backup": ""})

    if total_changed <= 0:
        raise ValueError("Image URL was not found in services hub content or template")

    return {
        "changed": total_changed,
        "fromUrl": from_url,
        "toUrl": to_url,
        "updated": updated,
        "path": updated[0]["path"] if updated else "",
        "backup": updated[0]["backup"] if updated else "",
    }


def update_bases_card_image(payload: dict) -> dict:
    page_path = str(payload.get("pagePath") or payload.get("path") or "").strip()
    if not page_path:
        raise ValueError("Bases page path is empty")
    target = content_path(page_path)
    if target.suffix.lower() != ".md" or not target.exists():
        raise ValueError("Bases page was not found")
    try:
        target.resolve().relative_to((CONTENT_ROOT / "bases").resolve())
    except ValueError as exc:
        raise ValueError("Only bases pages can be updated by this endpoint") from exc

    from_url = template_image_url(str(payload.get("fromUrl") or payload.get("from") or ""))
    to_url = template_image_url(str(payload.get("toUrl") or payload.get("to") or ""))
    if from_url == to_url:
        return {"changed": 0, "fromUrl": from_url, "toUrl": to_url, "backup": ""}

    front, body, _raw = read_markdown(target)
    changed = 0
    if str(front.get("image") or "").strip() == from_url:
        front["image"] = to_url
        changed += 1

    images = front.get("images")
    if isinstance(images, list):
        next_images = []
        for item in images:
            if str(item or "").strip() == from_url:
                next_images.append(to_url)
                changed += 1
            else:
                next_images.append(item)
        if changed:
            front["images"] = next_images
    elif not front.get("image"):
        front["image"] = to_url
        front["images"] = [to_url]
        changed += 1

    if not changed:
        raise ValueError("Image URL was not found in bases page front matter")

    backup = backup_file(target)
    target.write_text(dump_front_matter(front, body), encoding="utf-8")
    return {
        "changed": changed,
        "fromUrl": from_url,
        "toUrl": to_url,
        "path": target.relative_to(PROJECT_ROOT).as_posix(),
        "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
    }


def image_pixel_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image, ImageOps

        with Image.open(path) as opened:
            image = ImageOps.exif_transpose(opened)
            return int(image.width), int(image.height)
    except Exception:
        return 0, 0


def should_auto_optimize_image(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in AUTO_IMAGE_SKIP_SUFFIXES:
        return False
    if suffix == ".webp" and is_compressor_variant(path):
        return False
    try:
        size = path.stat().st_size
    except OSError:
        return False
    width, height = image_pixel_size(path)
    longest_side = max(width, height)
    if size > AUTO_IMAGE_MAX_BYTES:
        return True
    if longest_side > AUTO_IMAGE_MAX_SIDE and size > (120 * 1024):
        return True
    if suffix in {".bmp", ".tif", ".tiff"}:
        return True
    return False


def auto_optimize_image_url(value: str, cache: dict[str, str] | None = None, report: dict | None = None) -> str:
    url = str(value or "").strip()
    if not url:
        return value
    cache = cache if cache is not None else {}
    if url in cache:
        return cache[url]
    try:
        source = asset_file_from_url_or_rel(url)
    except Exception:
        cache[url] = value
        return value
    if not source.exists() or not source.is_file() or not should_auto_optimize_image(source):
        cache[url] = value
        return value
    try:
        before_size = source.stat().st_size
        result = compress_asset(
            {
                "url": asset_public_url(source),
                "quality": AUTO_IMAGE_QUALITY,
                "maxSide": AUTO_IMAGE_MAX_SIDE,
                "requireSmaller": True,
                "shrinkFactor": 1,
            }
        )
    except Exception:
        cache[url] = value
        return value
    next_url = str(result.get("url") or value)
    if not next_url or result.get("keptOriginal"):
        cache[url] = value
        return value
    cache[url] = next_url
    if report is not None:
        replacements = report.setdefault("replacements", [])
        replacements.append(
            {
                "from": asset_public_url(source),
                "to": next_url,
                "before": before_size,
                "after": int(result.get("size") or 0),
            }
        )
    return next_url


def auto_optimize_image_references_in_text(text: str, cache: dict[str, str], report: dict) -> str:
    if not text:
        return text

    def replace_match(match: re.Match) -> str:
        original = match.group("url")
        optimized = auto_optimize_image_url(original, cache, report)
        if optimized != original and original.endswith("\\"):
            return optimized + "\\"
        return optimized

    return LOCAL_IMAGE_URL_RE.sub(replace_match, text)


def auto_optimize_builder_json(value: str, cache: dict[str, str], report: dict) -> str:
    blocks = parse_builder_json_blocks(value)
    if blocks is None:
        return auto_optimize_image_references_in_text(value, cache, report)
    if not isinstance(blocks, list):
        return auto_optimize_image_references_in_text(value, cache, report)
    optimized_blocks = []
    for block in blocks:
        if not isinstance(block, dict):
            optimized_blocks.append(block)
            continue
        skip_image = block.get("noAutoOptimize") is True
        next_block = {}
        for key, item in block.items():
            if skip_image and key == "image" and isinstance(item, str):
                next_block[key] = item
            else:
                next_block[key] = auto_optimize_frontmatter_images(item, cache, report)
        optimized_blocks.append(next_block)
    return json.dumps(optimized_blocks, ensure_ascii=False, separators=(",", ":"))


def auto_optimize_frontmatter_images(value, cache: dict[str, str], report: dict):
    if isinstance(value, dict):
        optimized = {}
        for key, item in value.items():
            if key == "builderJson" and isinstance(item, str):
                optimized[key] = auto_optimize_builder_json(item, cache, report)
            else:
                optimized[key] = auto_optimize_frontmatter_images(item, cache, report)
        return optimized
    if isinstance(value, list):
        return [auto_optimize_frontmatter_images(item, cache, report) for item in value]
    if isinstance(value, str):
        if LOCAL_IMAGE_URL_RE.search(value):
            return auto_optimize_image_references_in_text(value, cache, report)
        return value
    return value


def auto_optimize_page_payload(front: dict, body: str = "") -> tuple[dict, str, dict]:
    cache: dict[str, str] = {}
    report: dict = {"replacements": []}
    optimized_front = auto_optimize_frontmatter_images(front, cache, report)
    optimized_body = auto_optimize_image_references_in_text(body, cache, report)
    image_url = str(optimized_front.get("image") or "").strip() if isinstance(optimized_front, dict) else ""
    if image_url and not optimized_front.get("imageWidth"):
        try:
            source = asset_file_from_url_or_rel(image_url)
            width, height = image_pixel_size(source)
            if width > 0 and height > 0:
                optimized_front["imageWidth"] = width
                optimized_front["imageHeight"] = height
        except Exception:
            pass
    report["count"] = len(report.get("replacements") or [])
    return optimized_front, optimized_body, report


def list_assets(include_usage: bool = True) -> list[dict]:
    assets: list[dict] = []
    # Page editing needs file metadata, not a project-wide reference audit.
    documents = site_text_documents() if include_usage else []
    for root in [STATIC_ROOT, PROJECT_ROOT / "assets"]:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            compressor_variant = is_compressor_variant(path)
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            public_url = asset_public_url(path)
            usage_sources = asset_usage_sources(path, public_url, documents) if include_usage else []
            stat = path.stat()
            assets.append(
                {
                    "path": rel,
                    "url": public_url,
                    "name": path.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "usageKnown": include_usage,
                    "used": bool(usage_sources) if include_usage else None,
                    "deletable": include_usage and not usage_sources,
                    "usageCount": len(usage_sources),
                    "usageSources": usage_sources[:8],
                    "compressorVariant": compressor_variant,
                }
            )
    return sorted(assets, key=lambda item: item["modified"], reverse=True)


def delete_asset(payload: dict) -> dict:
    rel = str(payload.get("path") or "")
    target = asset_file_from_rel(rel)
    if not target.exists() or not target.is_file():
        raise ValueError("Asset not found")
    public_url = asset_public_url(target)
    usage_sources = asset_usage_sources(target, public_url)
    if usage_sources:
        raise ValueError("Картинка используется на сайте и не может быть удалена")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    trash_target = MEDIA_TRASH_ROOT / stamp / target.relative_to(PROJECT_ROOT)
    if trash_target.exists():
        for index in range(2, 100):
            candidate = MEDIA_TRASH_ROOT / f"{stamp}-{index}" / target.relative_to(PROJECT_ROOT)
            if not candidate.exists():
                trash_target = candidate
                break
    trash_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(target), str(trash_target))
    clean_empty_dirs(target.parent, STATIC_ROOT if STATIC_ROOT in target.resolve().parents else PROJECT_ROOT / "assets")
    return {
        "deletedFrom": rel,
        "trashPath": trash_target.relative_to(PROJECT_ROOT).as_posix(),
    }


def list_backups() -> list[dict]:
    backups: list[dict] = []
    if not BACKUP_ROOT.exists():
        return backups
    for path in BACKUP_ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel_under_backup = path.relative_to(BACKUP_ROOT)
        except ValueError:
            continue
        parts = rel_under_backup.parts
        if len(parts) < 2:
            continue
        stamp = parts[0]
        original_rel = Path(*parts[1:]).as_posix()
        backups.append(
            {
                "backupPath": path.relative_to(PROJECT_ROOT).as_posix(),
                "originalPath": original_rel,
                "stamp": stamp,
                "size": path.stat().st_size,
                "modified": path.stat().st_mtime,
            }
        )
    return sorted(backups, key=lambda item: item["modified"], reverse=True)


def restore_backup(backup_rel: str) -> dict:
    backup = content_path(backup_rel)
    backup_root = BACKUP_ROOT.resolve()
    if not backup.exists() or not backup.is_file():
        raise ValueError("Backup file not found")
    if backup_root != backup.resolve() and backup_root not in backup.resolve().parents:
        raise ValueError("Backup path is outside admin/backups")
    rel_under_backup = backup.relative_to(BACKUP_ROOT)
    parts = rel_under_backup.parts
    if len(parts) < 2:
        raise ValueError("Backup path does not contain original file path")
    original_rel = Path(*parts[1:]).as_posix()
    target = safe_join(PROJECT_ROOT, original_rel)
    if target.exists():
        backup_file(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup, target)
    return {
        "restoredFrom": backup.relative_to(PROJECT_ROOT).as_posix(),
        "restoredTo": target.relative_to(PROJECT_ROOT).as_posix(),
    }


def list_trash() -> list[dict]:
    deleted: list[dict] = []
    if not TRASH_ROOT.exists():
        return deleted
    for path in TRASH_ROOT.rglob("*.md"):
        if not path.is_file():
            continue
        try:
            rel_under_trash = path.relative_to(TRASH_ROOT)
        except ValueError:
            continue
        parts = rel_under_trash.parts
        if len(parts) < 2:
            continue
        stamp = parts[0]
        original_rel = Path(*parts[1:]).as_posix()
        try:
            front, body, _ = read_markdown(path)
        except Exception:
            front, body = {}, ""
        deleted.append(
            {
                "trashPath": path.relative_to(PROJECT_ROOT).as_posix(),
                "originalPath": original_rel,
                "stamp": stamp,
                "title": str(front.get("title") or Path(original_rel).stem),
                "language": guess_language(path),
                "words": len(re.findall(r"\w+", body, flags=re.UNICODE)),
                "size": path.stat().st_size,
                "modified": path.stat().st_mtime,
            }
        )
    latest_by_original: dict[str, dict] = {}
    for item in deleted:
        original = str(item["originalPath"])
        current = latest_by_original.get(original)
        if current is None or (str(item["stamp"]), float(item["modified"])) > (str(current["stamp"]), float(current["modified"])):
            latest_by_original[original] = item
    for item in deleted:
        latest = latest_by_original.get(str(item["originalPath"]))
        item["canDeletePermanently"] = bool(latest and latest["trashPath"] == item["trashPath"])
    return sorted(deleted, key=lambda item: item["modified"], reverse=True)


def trash_file_from_rel(trash_rel: str) -> Path:
    trash_file = content_path(trash_rel)
    trash_root = TRASH_ROOT.resolve()
    if not trash_file.exists() or not trash_file.is_file():
        raise ValueError("Deleted page not found")
    resolved = trash_file.resolve()
    if trash_root != resolved and trash_root not in resolved.parents:
        raise ValueError("Trash path is outside admin/trash")
    return trash_file


def original_path_from_trash_file(trash_file: Path) -> str:
    rel_under_trash = trash_file.relative_to(TRASH_ROOT)
    parts = rel_under_trash.parts
    if len(parts) < 2:
        raise ValueError("Trash path does not contain original file path")
    return Path(*parts[1:]).as_posix()


def preview_trash(trash_rel: str) -> dict:
    trash_file = trash_file_from_rel(trash_rel)
    original_rel = original_path_from_trash_file(trash_file)
    front, body, raw = read_markdown(trash_file)
    return {
        "trashPath": trash_file.relative_to(PROJECT_ROOT).as_posix(),
        "originalPath": original_rel,
        "title": str(front.get("title") or Path(original_rel).stem),
        "language": guess_language(trash_file),
        "frontmatter": front,
        "body": body,
        "raw": raw,
        "words": len(re.findall(r"\w+", body, flags=re.UNICODE)),
        "size": trash_file.stat().st_size,
    }


def delete_trash_item(trash_rel: str) -> dict:
    trash_file = trash_file_from_rel(trash_rel)
    trash_path = trash_file.relative_to(PROJECT_ROOT).as_posix()
    original_rel = original_path_from_trash_file(trash_file)
    latest = next((item for item in list_trash() if item["originalPath"] == original_rel and item.get("canDeletePermanently")), None)
    if not latest or latest["trashPath"] != trash_path:
        raise ValueError("Можно удалить только последний удаленный вариант этой страницы")
    token_base = time.strftime("%Y%m%d-%H%M%S")
    token_hash = hashlib.sha1(trash_path.encode("utf-8")).hexdigest()[:8]
    token = f"{token_base}-{token_hash}"
    undo_file = TRASH_DELETE_UNDO_ROOT / token / trash_path
    for index in range(2, 100):
        if not undo_file.exists():
            break
        token = f"{token_base}-{token_hash}-{index}"
        undo_file = TRASH_DELETE_UNDO_ROOT / token / trash_path
    undo_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(trash_file), str(undo_file))
    clean_empty_dirs(trash_file.parent, TRASH_ROOT)
    return {
        "deletedFrom": trash_path,
        "originalPath": original_rel,
        "undoToken": token,
    }


def undo_delete_trash_item(token: str) -> dict:
    token = str(token or "").strip()
    if not re.fullmatch(r"\d{8}-\d{6}-[0-9a-f]{8}(?:-\d{1,2})?", token):
        raise ValueError("Invalid undo token")
    undo_root = (TRASH_DELETE_UNDO_ROOT / token).resolve()
    allowed_root = TRASH_DELETE_UNDO_ROOT.resolve()
    if allowed_root != undo_root and allowed_root not in undo_root.parents:
        raise ValueError("Undo path is outside trash undo storage")
    if not undo_root.exists():
        raise ValueError("Undo data not found")
    files = [path for path in undo_root.rglob("*.md") if path.is_file()]
    if len(files) != 1:
        raise ValueError("Undo data is corrupted")
    undo_file = files[0]
    trash_rel = undo_file.relative_to(undo_root).as_posix()
    if not trash_rel.startswith("admin/trash/"):
        raise ValueError("Undo target is not a trash item")
    target = safe_join(PROJECT_ROOT, trash_rel)
    trash_root = TRASH_ROOT.resolve()
    resolved_target = target.resolve()
    if trash_root != resolved_target and trash_root not in resolved_target.parents:
        raise ValueError("Undo target is outside admin/trash")
    if target.exists():
        raise ValueError("Cannot undo: trash item already exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(undo_file), str(target))
    clean_empty_dirs(undo_file.parent, TRASH_DELETE_UNDO_ROOT)
    return {
        "restoredToTrash": target.relative_to(PROJECT_ROOT).as_posix(),
    }


def delete_page(payload: dict) -> dict:
    rel = str(payload.get("path") or "")
    target = content_path(rel)
    ensure_content_file(target)
    if not target.exists():
        raise ValueError("Page not found")
    delete_block_reason = page_delete_block_reason(target)
    if delete_block_reason:
        raise ValueError(f"Страница защищена от удаления: {delete_block_reason}")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    original_rel = target.relative_to(PROJECT_ROOT)
    trash_target = TRASH_ROOT / stamp / original_rel
    if trash_target.exists():
        for index in range(2, 100):
            candidate = TRASH_ROOT / f"{stamp}-{index}" / original_rel
            if not candidate.exists():
                trash_target = candidate
                stamp = f"{stamp}-{index}"
                break
    trash_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(target), str(trash_target))
    clean_empty_dirs(target.parent, CONTENT_ROOT)
    return {
        "deletedFrom": rel,
        "trashPath": trash_target.relative_to(PROJECT_ROOT).as_posix(),
    }


def restore_trash(trash_rel: str) -> dict:
    trash_file = trash_file_from_rel(trash_rel)
    original_rel = original_path_from_trash_file(trash_file)
    target = safe_join(PROJECT_ROOT, original_rel)
    ensure_content_file(target)
    if target.exists():
        raise ValueError("Cannot restore: a page already exists at this path")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(trash_file), str(target))
    clean_empty_dirs(trash_file.parent, TRASH_ROOT)
    return {
        "restoredFrom": trash_rel,
        "restoredTo": target.relative_to(PROJECT_ROOT).as_posix(),
    }


def load_chrome() -> dict:
    if not CHROME_PATH.exists():
        return {
            "header": {"extraLinks": {"en": [], "ru": [], "es": []}},
            "footer": {
                "contacts": {
                    "email": "support@seoimpuls.com",
                    "whatsapp": "https://wa.me/5491132804658",
                    "telegram": "https://t.me/Seoimpuls",
                },
                "textLinks": {"en": [], "ru": [], "es": []},
                "legalLinks": DEFAULT_LEGAL_LINKS,
                "socialLinks": [],
                "map": {"src": ""},
            },
        }
    return json.loads(CHROME_PATH.read_text(encoding="utf-8-sig"))


def normalize_link_list(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    items: list[dict] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        label = str(item.get("label") or "").strip()
        url = str(item.get("url") or "").strip()
        if not label and not url:
            continue
        items.append(
            {
                "label": label,
                "url": url or "#",
                "enabled": bool(item.get("enabled", True)),
            }
        )
    return items


def normalize_legal_link_list(value, lang: str) -> list[dict]:
    source = value if isinstance(value, list) and value else DEFAULT_LEGAL_LINKS.get(lang, [])
    items: list[dict] = []
    for index, item in enumerate(source):
        if not isinstance(item, dict):
            continue
        default = DEFAULT_LEGAL_LINKS.get(lang, [])
        fallback = default[index] if index < len(default) else {}
        label = str(item.get("label") or fallback.get("label") or "").strip()
        url = str(item.get("url") or fallback.get("url") or "#").strip()
        if not label and not url:
            continue
        clean = {
            "key": str(item.get("key") or fallback.get("key") or f"footer-link-{index + 1}").strip(),
            "label": label,
            "url": url or "#",
            "enabled": bool(item.get("enabled", fallback.get("enabled", True))),
        }
        if bool(item.get("cookieSettings", fallback.get("cookieSettings", False))):
            clean["cookieSettings"] = True
        items.append(clean)
    return items


def normalize_chrome(payload: dict) -> dict:
    chrome = payload if isinstance(payload, dict) else {}
    header = chrome.get("header") if isinstance(chrome.get("header"), dict) else {}
    footer = chrome.get("footer") if isinstance(chrome.get("footer"), dict) else {}
    extra = header.get("extraLinks") if isinstance(header.get("extraLinks"), dict) else {}
    text_links = footer.get("textLinks") if isinstance(footer.get("textLinks"), dict) else {}
    legal_links = footer.get("legalLinks") if isinstance(footer.get("legalLinks"), dict) else {}
    contacts = footer.get("contacts") if isinstance(footer.get("contacts"), dict) else {}
    social_links = footer.get("socialLinks") if isinstance(footer.get("socialLinks"), list) else []
    clean_social = []
    for item in social_links:
        if not isinstance(item, dict):
            continue
        clean_social.append(
            {
                "key": str(item.get("key") or "").strip(),
                "label": str(item.get("label") or "").strip(),
                "url": str(item.get("url") or "").strip(),
                "iconClass": str(item.get("iconClass") or "").strip(),
                "enabled": bool(item.get("enabled", True)),
            }
        )
    return {
        "header": {
            "extraLinks": {lang: normalize_link_list(extra.get(lang)) for lang in LANGS}
        },
        "footer": {
            "contacts": {
                "email": str(contacts.get("email") or "support@seoimpuls.com").strip(),
                "whatsapp": str(contacts.get("whatsapp") or "https://wa.me/5491132804658").strip(),
                "telegram": str(contacts.get("telegram") or "https://t.me/Seoimpuls").strip(),
            },
            "textLinks": {lang: normalize_link_list(text_links.get(lang)) for lang in LANGS},
            "legalLinks": {lang: normalize_legal_link_list(legal_links.get(lang), lang) for lang in LANGS},
            "socialLinks": clean_social,
            "map": {
                "src": str((footer.get("map") if isinstance(footer.get("map"), dict) else {}).get("src") or "").strip()
            },
        },
    }


def decode_toml_string(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return json.loads(value)
    return value


def toml_string(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=True)


def load_menu() -> dict:
    text = HUGO_CONFIG_PATH.read_text(encoding="utf-8-sig")
    menu: dict[str, list[dict]] = {lang: [] for lang in LANGS}
    for lang in LANGS:
        pattern = re.compile(rf"^\s*\[\[languages\.{lang}\.menu\.main\]\]\s*$", re.MULTILINE)
        starts = [match.start() for match in pattern.finditer(text)]
        for index, start in enumerate(starts):
            end = starts[index + 1] if index + 1 < len(starts) else len(text)
            next_lang = re.search(r"^\s*\[languages\.[a-z]{2}\]\s*$", text[start + 1 :], re.MULTILINE)
            if next_lang:
                end = min(end, start + 1 + next_lang.start())
            block = text[start:end]
            item = {"name": "", "url": "", "weight": 0, "enabled": True}
            for line in block.splitlines():
                stripped = line.strip()
                if stripped.startswith("name"):
                    item["name"] = decode_toml_string(stripped.split("=", 1)[1])
                elif stripped.startswith("url"):
                    item["url"] = decode_toml_string(stripped.split("=", 1)[1])
                elif stripped.startswith("weight"):
                    try:
                        item["weight"] = int(stripped.split("=", 1)[1].strip())
                    except ValueError:
                        item["weight"] = 0
            if item["name"] or item["url"]:
                menu[lang].append(item)
        menu[lang].sort(key=lambda item: int(item.get("weight") or 0))
    return menu


def normalize_menu(payload) -> dict:
    source = payload if isinstance(payload, dict) else {}
    menu: dict[str, list[dict]] = {}
    for lang in LANGS:
        rows = source.get(lang) if isinstance(source.get(lang), list) else []
        clean = []
        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            name = str(row.get("name") or "").strip()
            url = str(row.get("url") or "").strip()
            if not name and not url:
                continue
            try:
                weight = int(row.get("weight"))
            except (TypeError, ValueError):
                weight = (idx + 1) * 10
            clean.append({"name": name, "url": url or "#", "weight": weight, "enabled": bool(row.get("enabled", True))})
        menu[lang] = clean
    return menu


def render_menu_block(lang: str, items: list[dict]) -> str:
    lines: list[str] = []
    for item in items:
        if item.get("enabled") is False:
            continue
        lines.extend(
            [
                f"    [[languages.{lang}.menu.main]]",
                f"      name = {toml_string(item.get('name', ''))}",
                f"      url = {toml_string(item.get('url', '#'))}",
                f"      weight = {int(item.get('weight') or 0)}",
                "",
            ]
        )
    if not lines:
        return ""
    return "\n".join(lines).rstrip() + "\n"


def replace_menu_for_lang(text: str, lang: str, items: list[dict]) -> str:
    lang_header = re.search(rf"^\s*\[languages\.{lang}\]\s*$", text, re.MULTILINE)
    if not lang_header:
        raise ValueError(f"Language block not found: {lang}")

    next_lang = re.search(r"^\s*\[languages\.[a-z]{2}\]\s*$", text[lang_header.end() :], re.MULTILINE)
    block_start = lang_header.start()
    block_end = lang_header.end() + next_lang.start() if next_lang else len(text)
    block = text[block_start:block_end]

    menu_re = re.compile(rf"^\s*\[\[languages\.{lang}\.menu\.main\]\]\s*\n.*?(?=^\s*\[|\Z)", re.MULTILINE | re.DOTALL)
    cleaned_block = menu_re.sub("", block).rstrip()
    new_block = render_menu_block(lang, items)

    replacement = cleaned_block
    if new_block:
        replacement += "\n\n" + new_block.rstrip()
    return text[:block_start].rstrip() + "\n\n" + replacement.rstrip() + "\n\n" + text[block_end:].lstrip("\n")


def save_menu(payload) -> dict:
    menu = normalize_menu(payload)
    text = HUGO_CONFIG_PATH.read_text(encoding="utf-8-sig")
    backup = backup_file(HUGO_CONFIG_PATH)
    for lang in LANGS:
        text = replace_menu_for_lang(text, lang, menu[lang])
    HUGO_CONFIG_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")
    return {"menu": menu, "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else ""}


CYRILLIC_SLUG_MAP = str.maketrans(
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)


def slugify(value: str) -> str:
    value = value.strip().lower().translate(CYRILLIC_SLUG_MAP)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9_-]+", "-", value, flags=re.IGNORECASE)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "new-page"


def slugify_path(value: str, fallback: str = "pages") -> str:
    raw = str(value or fallback).strip().replace("\\", "/")
    raw = re.sub(r"^https?://[^/]+", "", raw, flags=re.IGNORECASE)
    parts: list[str] = []
    for part in raw.split("/"):
        clean = part.strip()
        if not clean or clean in {".", "..", "content"}:
            continue
        if clean in LANGS:
            continue
        clean = SECTION_ALIASES.get(clean.lower(), clean)
        parts.append(slugify(clean))
    return "/".join(parts) or fallback


def section_public_url(section: str, lang: str) -> str:
    clean_section = slugify_path(section, "pages").split("/", 1)[0]
    filename = "_index.md" if lang == "en" else f"_index.{lang}.md"
    section_index = CONTENT_ROOT / clean_section / filename
    if not section_index.exists():
        return ""
    try:
        front, _, _ = read_markdown(section_index)
    except Exception:
        return ""
    return page_front_public_url(front, clean_section, lang)


def create_page(payload: dict) -> dict:
    section = slugify_path(str(payload.get("section") or "pages"))
    base_slug = slugify(str(payload.get("slug") or payload.get("title") or "new-page"))
    slug = base_slug
    root_section = section.split("/", 1)[0]
    languages = payload.get("languages") or ["en", "ru", "es"]
    if not isinstance(languages, list):
        languages = ["en"]
    languages = [lang for lang in languages if lang in LANGS]
    if not languages:
        raise ValueError("Choose page language")
    def page_path_for(candidate_slug: str, lang: str) -> Path:
        filename = "index.md" if lang == "en" else f"index.{lang}.md"
        return CONTENT_ROOT.joinpath(*section.split("/")) / candidate_slug / filename
    suffix = 2
    while any(page_path_for(slug, lang).exists() for lang in languages):
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    page_dir = CONTENT_ROOT.joinpath(*section.split("/")) / slug
    page_dir.mkdir(parents=True, exist_ok=True)
    created = []
    titles = payload.get("titles") if isinstance(payload.get("titles"), dict) else {}
    descriptions = payload.get("descriptions") if isinstance(payload.get("descriptions"), dict) else {}
    translation_key = str(payload.get("translationKey") or f"{section.replace('/', '-')}-{slug}")
    for lang in languages:
        filename = "index.md" if lang == "en" else f"index.{lang}.md"
        path = page_dir / filename
        if path.exists():
            continue
        title = titles.get(lang) or payload.get("title") or slug.replace("-", " ").title()
        front = {
            "title": title,
            "description": descriptions.get(lang) or "",
            "slug": slug,
            "translationKey": translation_key,
            "draft": bool(payload.get("draft", False)),
        }
        if root_section in {"news", "blog"} or bool(payload.get("feedPost", False)):
            front["showOnHome"] = True
            front["date"] = time.strftime("%Y-%m-%d")
            front["tags"] = ["news"]
        elif bool(payload.get("showOnHome", False)):
            front["showOnHome"] = True
        ensure_home_feed_date(path, front)
        image = str(payload.get("image") or "").strip()
        if image:
            front["image"] = image
            front["images"] = [image]
            try:
                image_width = int(float(payload.get("imageWidth") or 0))
            except (TypeError, ValueError):
                image_width = 0
            if image_width > 0:
                front["imageWidth"] = image_width
        target_url = str(payload.get("targetUrl") or "").strip()
        if target_url:
            front["targetUrl"] = target_url
        button_label = str(payload.get("buttonLabel") or "").strip()
        button_url = str(payload.get("buttonUrl") or "").strip()
        if button_label and button_url:
            front["buttonLabel"] = button_label
            front["buttonUrl"] = button_url
        builder_json = str(payload.get("builderJson") or "").strip()
        front["builderJson"] = normalize_builder_json_value(builder_json or "[]", strict=True)
        parent_url = section_public_url(section, lang)
        if parent_url and not front.get("url"):
            front["url"] = normalize_public_url(f"{parent_url}{slug}/")
        body = str(payload.get("body") or "")
        front, body, _auto_image_report = auto_optimize_page_payload(front, body)
        path.write_text(dump_front_matter(front, body), encoding="utf-8")
        created.append(path.relative_to(PROJECT_ROOT).as_posix())
    return {"created": created, "section": section, "slug": slug}


def cleanup_empty_content_dirs(path: Path) -> None:
    current = path.parent
    content_root = CONTENT_ROOT.resolve()
    while current.resolve() != content_root and content_root in current.resolve().parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def move_page(payload: dict) -> dict:
    rel = str(payload.get("path") or "")
    source = content_path(rel)
    if source.suffix.lower() != ".md":
        raise ValueError("Only markdown pages can be moved")
    if not source.exists():
        raise ValueError("Page not found")
    front = payload.get("frontmatter")
    body = payload.get("body")
    if not isinstance(front, dict) or not isinstance(body, str):
        raise ValueError("Expected frontmatter object and body string")

    section_page = is_section_index(source)
    section = slugify_path(str(payload.get("section") or page_section(source)))
    slug = section if section_page else slugify(str(payload.get("slug") or front.get("slug") or source.parent.name))
    lang = guess_language(source)
    filename = "_index.md" if lang == "en" else f"_index.{lang}.md"
    if not section_page:
        filename = "index.md" if lang == "en" else f"index.{lang}.md"
    target = ((CONTENT_ROOT / section / filename) if section_page else (CONTENT_ROOT / section / slug / filename)).resolve()
    content_root = CONTENT_ROOT.resolve()
    if content_root != target and content_root not in target.parents:
        raise ValueError("Target path is outside content")
    if target.exists() and target != source.resolve():
        raise ValueError(f"Target page already exists: {target.relative_to(PROJECT_ROOT).as_posix()}")

    front["slug"] = slug
    if not front.get("translationKey"):
        front["translationKey"] = f"{section}-{slug}"
    normalize_front_builder_json(front, strict=True)
    ensure_home_feed_date(target, front)
    front, body, auto_image_report = auto_optimize_page_payload(front, body)
    backup = backup_file(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_front_matter(front, body), encoding="utf-8")
    if target != source.resolve():
        source.unlink()
        cleanup_empty_content_dirs(source)
    return {
        "path": target.relative_to(PROJECT_ROOT).as_posix(),
        "section": section,
        "slug": slug,
        "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
        "autoImageOptimization": auto_image_report,
    }



def find_free_port(start: int) -> int:
    import socket

    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    raise RuntimeError("No free local port found")


def start_hugo() -> dict:
    global HUGO_PROCESS, HUGO_PORT
    if HUGO_PROCESS and HUGO_PROCESS.poll() is None and HUGO_PORT:
        return {"url": f"http://127.0.0.1:{HUGO_PORT}/", "pid": HUGO_PROCESS.pid, "alreadyRunning": True}
    stop_hugo_preview_for_build()
    port = find_free_port(1314)
    args = [
        sys.executable,
        str(ADMIN_ROOT / "prod_preview_server.py"),
        "--root",
        str(PUBLIC_ROOT),
        "--port",
        str(port),
    ]
    HUGO_PROCESS = subprocess.Popen(
        args,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    HUGO_PORT = port
    return {"url": f"http://127.0.0.1:{port}/", "pid": HUGO_PROCESS.pid, "alreadyRunning": False}


def _command_has_hugo_port(command_line: str, ports: set[int]) -> bool:
    if not ports:
        return True
    matches = re.findall(r"--port(?:=|\s+)(\d+)", command_line, flags=re.IGNORECASE)
    return any(int(match) in ports for match in matches if match.isdigit())


def _windows_hugo_server_pids(ports: set[int]) -> list[int]:
    if os.name != "nt":
        return []
    script = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -in @('hugo.exe','python.exe') } | "
        "Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
    )
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            return []
        data = json.loads(proc.stdout)
    except Exception:
        return []
    rows = data if isinstance(data, list) else [data]
    result: list[int] = []
    for row in rows:
        command_line = str(row.get("CommandLine") or "")
        pid = int(row.get("ProcessId") or 0)
        if not pid or pid == os.getpid():
            continue
        lower = command_line.lower()
        if "hugo" in lower and "server" in lower and _command_has_hugo_port(command_line, ports):
            result.append(pid)
            continue
        if "prod_preview_server.py" in lower and _command_has_hugo_port(command_line, ports):
            result.append(pid)
    return result


def stop_hugo_preview_for_build() -> dict:
    global HUGO_PROCESS, HUGO_PORT
    ports = set(HUGO_PREVIEW_PORTS)
    if HUGO_PORT:
        ports.add(HUGO_PORT)
    stopped: list[int] = []
    errors: list[str] = []

    if HUGO_PROCESS and HUGO_PROCESS.poll() is None:
        pid = HUGO_PROCESS.pid
        try:
            HUGO_PROCESS.terminate()
            HUGO_PROCESS.wait(timeout=5)
        except Exception:
            try:
                HUGO_PROCESS.kill()
                HUGO_PROCESS.wait(timeout=5)
            except Exception as exc:
                errors.append(f"Failed to stop tracked Hugo preview {pid}: {exc}")
        else:
            stopped.append(pid)
    HUGO_PROCESS = None
    HUGO_PORT = None

    for pid in _windows_hugo_server_pids(ports):
        if pid in stopped:
            continue
        try:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True, timeout=10)
            stopped.append(pid)
        except Exception as exc:
            errors.append(f"Failed to stop Hugo preview {pid}: {exc}")

    return {"stopped": stopped, "errors": errors}


def load_deploy_config() -> dict:
    config = dict(DEFAULT_DEPLOY_CONFIG)
    if DEPLOY_CONFIG_PATH.exists():
        raw = json.loads(DEPLOY_CONFIG_PATH.read_text(encoding="utf-8-sig"))
        if isinstance(raw, dict):
            config.update(raw)
    env_password = os.environ.get("SEOIMPULS_DEPLOY_PASSWORD", "").strip()
    if env_password:
        config["password"] = env_password
    return config


def deploy_config_status() -> dict:
    config = load_deploy_config()
    return {
        "configured": bool(config.get("host") and config.get("username") and config.get("password") and config.get("remoteBase")),
        "host": str(config.get("host") or ""),
        "port": int(config.get("port") or 22),
        "username": str(config.get("username") or ""),
        "remoteBase": str(config.get("remoteBase") or ""),
        "domain": str(config.get("domain") or ""),
        "configPath": str(DEPLOY_CONFIG_PATH),
    }


def remote_exec(client, command: str, timeout: int = 60) -> dict:
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    code = stdout.channel.recv_exit_status()
    return {"command": command, "code": code, "stdout": out[-4000:], "stderr": err[-4000:]}


def server_pause_status() -> dict:
    config = load_deploy_config()
    missing = [key for key in ("host", "username", "password", "remoteBase") if not str(config.get(key) or "").strip()]
    if missing:
        return {"configured": False, "paused": False, "error": f"Не заполнен deploy_config.local.json: {', '.join(missing)}"}

    try:
        import paramiko
    except Exception as exc:
        raise RuntimeError("Для управления серверной паузой нужен Python-пакет paramiko.") from exc

    remote_base = str(config["remoteBase"]).rstrip("/")
    pause_file = f"{remote_base}/.paused"
    nginx_conf = "/etc/nginx/sites-available/seoimpuls.com.conf"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=str(config["host"]),
            port=int(config.get("port") or 22),
            username=str(config["username"]),
            password=str(config["password"]),
            timeout=20,
            auth_timeout=20,
            banner_timeout=20,
        )
        paused_check = remote_exec(client, f"test -f {shlex.quote(pause_file)}", timeout=30)
        hook_check = remote_exec(client, f"grep -q 'SEOIMPULS_ADMIN_PAUSE' {shlex.quote(nginx_conf)}", timeout=30)
        return {
            "configured": True,
            "paused": paused_check["code"] == 0,
            "hookConfigured": hook_check["code"] == 0,
            "pauseFile": pause_file,
            "domain": str(config.get("domain") or ""),
            "commands": [paused_check, hook_check],
        }
    finally:
        client.close()


def set_server_pause(paused: bool) -> dict:
    config = load_deploy_config()
    missing = [key for key in ("host", "username", "password", "remoteBase") if not str(config.get(key) or "").strip()]
    if missing:
        raise RuntimeError(f"Не заполнен deploy_config.local.json: {', '.join(missing)}")

    try:
        import paramiko
    except Exception as exc:
        raise RuntimeError("Для управления серверной паузой нужен Python-пакет paramiko.") from exc

    remote_base = str(config["remoteBase"]).rstrip("/")
    pause_file = f"{remote_base}/.paused"
    nginx_conf = "/etc/nginx/sites-available/seoimpuls.com.conf"
    action = f"touch {shlex.quote(pause_file)}" if paused else f"rm -f {shlex.quote(pause_file)}"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    commands: list[dict] = []
    try:
        client.connect(
            hostname=str(config["host"]),
            port=int(config.get("port") or 22),
            username=str(config["username"]),
            password=str(config["password"]),
            timeout=20,
            auth_timeout=20,
            banner_timeout=20,
        )
        hook_check = remote_exec(client, f"grep -q 'SEOIMPULS_ADMIN_PAUSE' {shlex.quote(nginx_conf)}", timeout=30)
        commands.append(hook_check)
        if hook_check["code"] != 0:
            raise RuntimeError("На сервере не найден nginx-блок SEOIMPULS_ADMIN_PAUSE. Сначала нужно поставить аварийный hook в nginx.")
        change = remote_exec(client, action, timeout=30)
        commands.append(change)
        if change["code"] != 0:
            return {"ok": False, "paused": not paused, "pauseFile": pause_file, "commands": commands}
        status = remote_exec(client, f"test -f {shlex.quote(pause_file)}", timeout=30)
        commands.append(status)
        current_paused = status["code"] == 0
        return {
            "ok": current_paused == paused,
            "paused": current_paused,
            "hookConfigured": True,
            "pauseFile": pause_file,
            "domain": str(config.get("domain") or ""),
            "commands": commands,
        }
    finally:
        client.close()


def postprocess_public_builder_scroll_fix() -> dict:
    if not PUBLIC_ROOT.exists():
        return {"changed": 0, "checked": 0}
    checked = 0
    changed = 0
    for html_path in PUBLIC_ROOT.rglob("*.html"):
        checked += 1
        try:
            html = html_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "seo-builder" not in html or ADMIN_BUILDER_SCROLL_FIX_MARKER in html:
            continue
        next_html = html
        if "</head>" in next_html:
            next_html = next_html.replace("</head>", f"{ADMIN_BUILDER_SCROLL_FIX_STYLE}</head>", 1)
        else:
            next_html = ADMIN_BUILDER_SCROLL_FIX_STYLE + next_html
        if "</body>" in next_html:
            next_html = next_html.replace("</body>", f"{ADMIN_BUILDER_SCROLL_FIX_SCRIPT}</body>", 1)
        else:
            next_html += ADMIN_BUILDER_SCROLL_FIX_SCRIPT
        if next_html != html:
            html_path.write_text(next_html, encoding="utf-8", newline="")
            changed += 1
    return {"changed": changed, "checked": checked}


def run_hugo_build() -> dict:
    preview_stop = stop_hugo_preview_for_build()
    proc = subprocess.run(
        ["hugo", "--minify", "--noBuildLock", "--cleanDestinationDir"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    postprocess = postprocess_public_builder_scroll_fix() if proc.returncode == 0 else {"changed": 0, "checked": 0}
    preview_start = start_hugo() if preview_stop["stopped"] else None
    return {
        "ok": proc.returncode == 0,
        "code": proc.returncode,
        "stdout": proc.stdout[-12000:],
        "stderr": proc.stderr[-12000:],
        "postprocess": postprocess,
        "previewStop": preview_stop,
        "previewStart": preview_start,
    }


def create_public_archive(stamp: str) -> Path:
    if not PUBLIC_ROOT.exists() or not (PUBLIC_ROOT / "index.html").exists():
        raise RuntimeError("Папка public не собрана. Сначала запустите сборку Hugo.")
    DEPLOY_TMP_ROOT.mkdir(parents=True, exist_ok=True)
    archive = DEPLOY_TMP_ROOT / f"seoimpuls-public-{stamp}.tar.gz"
    if archive.exists():
        archive.unlink()
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(PUBLIC_ROOT, arcname="public")
    return archive


def public_file_for_url(url: str) -> Path:
    parsed = urllib.parse.urlparse(str(url or ""))
    clean = urllib.parse.unquote(parsed.path or "/")
    clean = "/" + clean.lstrip("/")
    normalized = posixpath.normpath(clean)
    if normalized in ("", "."):
        normalized = "/"
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    if clean.endswith("/") or Path(normalized).suffix == "":
        rel = "index.html" if normalized == "/" else f"{normalized.strip('/')}/index.html"
    else:
        rel = normalized.strip("/")
    return safe_join(PUBLIC_ROOT, rel)


def public_rel(path: Path) -> str:
    return path.resolve().relative_to(PUBLIC_ROOT.resolve()).as_posix()


def referenced_public_assets(files: list[Path]) -> list[Path]:
    refs: set[Path] = set()
    attr_re = re.compile(r"""(?:src|href)=(?:"([^"]+)"|'([^']+)'|([^\s>]+))""", re.IGNORECASE)
    css_re = re.compile(r"""url\((['"]?)([^'")]+)\1\)""", re.IGNORECASE)
    for file in files:
        if file.suffix.lower() not in SITE_TEXT_SUFFIXES:
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        values = [next((group for group in match.groups() if group), "") for match in attr_re.finditer(text)]
        values.extend(match.group(2) for match in css_re.finditer(text))
        for value in values:
            parsed = urllib.parse.urlparse(value)
            if parsed.scheme or parsed.netloc:
                continue
            asset_path = urllib.parse.unquote(parsed.path or "")
            if not asset_path.startswith("/") or asset_path == "/":
                continue
            try:
                target = safe_join(PUBLIC_ROOT, asset_path.lstrip("/"))
            except ValueError:
                continue
            if target.exists() and target.is_file():
                refs.add(target)
    return sorted(refs, key=lambda item: item.as_posix())


def public_homepage_files() -> list[Path]:
    candidates = [
        PUBLIC_ROOT / "index.html",
        PUBLIC_ROOT / "ru" / "index.html",
        PUBLIC_ROOT / "es" / "index.html",
    ]
    return [path for path in candidates if path.exists() and path.is_file()]


def public_files_for_page_url(url: str) -> list[Path]:
    target = public_file_for_url(url)
    if target.is_dir():
        target = target / "index.html"
    if not target.exists() or not target.is_file():
        raise RuntimeError(f"После сборки не найден файл страницы: {target.relative_to(PROJECT_ROOT).as_posix()}")
    files = [target]
    if target.name.lower() == "index.html" and target.parent.resolve() != PUBLIC_ROOT.resolve():
        try:
            files.extend(
                child
                for child in target.parent.iterdir()
                if child.is_file() and child.resolve() != target.resolve()
            )
        except OSError:
            pass
    files.extend(public_homepage_files())
    files.extend(referenced_public_assets(files))
    unique: dict[str, Path] = {}
    for file in files:
        unique[public_rel(file)] = file
    return [unique[key] for key in sorted(unique)]


def public_asset_path_from_url(value: str) -> Path | None:
    parsed = urllib.parse.urlparse(str(value or "").strip())
    if parsed.scheme or parsed.netloc:
        host = (parsed.hostname or "").lower()
        if host and host not in {"localhost", "seoimpuls.com", "www.seoimpuls.com"} and not host.startswith("127."):
            return None
    asset_path = urllib.parse.unquote(parsed.path or "")
    if not asset_path.startswith("/") or asset_path == "/":
        return None
    try:
        target = safe_join(PUBLIC_ROOT, asset_path.lstrip("/"))
    except ValueError:
        return None
    return target if target.exists() and target.is_file() else None


def page_weight_audit(payload: dict) -> dict:
    url = str(payload.get("url") or "/").strip() or "/"
    target = public_file_for_url(url)
    if not target.exists() or not target.is_file():
        build = run_hugo_build()
        if not build.get("ok"):
            raise RuntimeError("Hugo build failed before page weight audit")
    target = public_file_for_url(url)
    if not target.exists() or not target.is_file():
        raise RuntimeError(f"Built page not found: {target.relative_to(PROJECT_ROOT).as_posix()}")

    html = target.read_text(encoding="utf-8", errors="ignore")
    attr_re = re.compile(r"""(?:src|href)=(?:"([^"]+)"|'([^']+)'|([^\s>]+))""", re.IGNORECASE)
    srcset_re = re.compile(r"""srcset=(?:"([^"]+)"|'([^']+)')""", re.IGNORECASE)
    img_re = re.compile(r"""<img\b[^>]*>""", re.IGNORECASE)
    src_re = re.compile(r"""src=(?:"([^"]+)"|'([^']+)'|([^\s>]+))""", re.IGNORECASE)
    width_re = re.compile(r"""\bwidth=(?:"[^"]+"|'[^']+'|[^\s>]+)""", re.IGNORECASE)
    height_re = re.compile(r"""\bheight=(?:"[^"]+"|'[^']+'|[^\s>]+)""", re.IGNORECASE)
    loading_re = re.compile(r"""\bloading=(?:"[^"]+"|'[^']+'|[^\s>]+)""", re.IGNORECASE)

    values: list[str] = []
    values.extend(next((group for group in match.groups() if group), "") for match in attr_re.finditer(html))
    for match in srcset_re.finditer(html):
        raw_srcset = next((group for group in match.groups() if group), "")
        for part in raw_srcset.split(","):
            url_part = part.strip().split(" ", 1)[0]
            if url_part:
                values.append(url_part)

    resources: dict[str, dict] = {}
    for value in values:
        file = public_asset_path_from_url(value)
        if not file:
            continue
        rel = "/" + public_rel(file)
        suffix = file.suffix.lower()
        kind = "other"
        if suffix in IMAGE_SUFFIXES:
            kind = "image"
        elif suffix == ".css":
            kind = "css"
        elif suffix == ".js":
            kind = "js"
        elif suffix in {".woff", ".woff2", ".ttf", ".otf"}:
            kind = "font"
        resources[rel] = {"url": rel, "path": public_rel(file), "kind": kind, "bytes": file.stat().st_size}

    missing_image_dimensions: list[str] = []
    eager_images: list[str] = []
    for match in img_re.finditer(html):
        tag = match.group(0)
        src_match = src_re.search(tag)
        src = next((group for group in src_match.groups() if group), "") if src_match else ""
        if not src:
            continue
        if not width_re.search(tag) or not height_re.search(tag):
            missing_image_dimensions.append(src)
        loading_match = loading_re.search(tag)
        loading_value = loading_match.group(0).lower() if loading_match else ""
        if "lazy" not in loading_value:
            eager_images.append(src)

    sorted_resources = sorted(resources.values(), key=lambda item: int(item["bytes"]), reverse=True)
    total_bytes = sum(int(item["bytes"]) for item in sorted_resources)
    image_bytes = sum(int(item["bytes"]) for item in sorted_resources if item["kind"] == "image")
    issues: list[dict] = []
    for item in sorted_resources:
        size = int(item["bytes"])
        if item["kind"] == "image" and size > 80 * 1024:
            issues.append({"level": "warning", "message": "image over 80 KB", "url": item["url"], "bytes": size})
        if item["kind"] in {"css", "js", "font"} and size > 120 * 1024:
            issues.append({"level": "warning", "message": f"{item['kind']} over 120 KB", "url": item["url"], "bytes": size})
    if total_bytes > 700 * 1024:
        issues.append({"level": "warning", "message": "page resources over 700 KB", "bytes": total_bytes})
    for src in missing_image_dimensions[:20]:
        issues.append({"level": "notice", "message": "image has no width/height in HTML", "url": src})

    failures: list[dict] = []
    if total_bytes > IDEAL_PAGE_TOTAL_BYTES:
        failures.append({"message": "page is heavier than ideal homepage budget", "bytes": total_bytes, "limit": IDEAL_PAGE_TOTAL_BYTES})
    if image_bytes > IDEAL_PAGE_IMAGE_BYTES:
        failures.append({"message": "images are heavier than ideal budget", "bytes": image_bytes, "limit": IDEAL_PAGE_IMAGE_BYTES})
    if len(sorted_resources) > IDEAL_RESOURCE_COUNT:
        failures.append({"message": "too many page resources", "count": len(sorted_resources), "limit": IDEAL_RESOURCE_COUNT})
    for item in sorted_resources:
        size = int(item["bytes"])
        if item["kind"] == "image" and size > IDEAL_SINGLE_IMAGE_BYTES:
            failures.append({"message": "single image is too heavy", "url": item["url"], "bytes": size, "limit": IDEAL_SINGLE_IMAGE_BYTES})
        if item["kind"] in {"css", "js", "font"} and size > IDEAL_SINGLE_ASSET_BYTES:
            failures.append({"message": f"{item['kind']} file is too heavy", "url": item["url"], "bytes": size, "limit": IDEAL_SINGLE_ASSET_BYTES})
    for src in missing_image_dimensions[:20]:
        failures.append({"message": "image has no width/height in HTML", "url": src})

    return {
        "url": url,
        "page": target.relative_to(PROJECT_ROOT).as_posix(),
        "profile": "seoimpuls-homepage-ideal",
        "passed": not failures,
        "budget": {
            "totalBytes": IDEAL_PAGE_TOTAL_BYTES,
            "imageBytes": IDEAL_PAGE_IMAGE_BYTES,
            "singleImageBytes": IDEAL_SINGLE_IMAGE_BYTES,
            "singleAssetBytes": IDEAL_SINGLE_ASSET_BYTES,
            "resourceCount": IDEAL_RESOURCE_COUNT,
        },
        "totalBytes": total_bytes,
        "imageBytes": image_bytes,
        "resourceCount": len(sorted_resources),
        "resources": sorted_resources[:80],
        "issues": issues[:80],
        "failures": failures[:80],
        "missingImageDimensions": missing_image_dimensions[:80],
        "eagerImages": eager_images[:80],
    }


def public_html_url(path: Path) -> str:
    rel = path.relative_to(PUBLIC_ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def site_weight_audit() -> dict:
    pages: list[dict] = []
    failures: list[dict] = []
    for html_path in sorted(PUBLIC_ROOT.rglob("*.html")):
        audit = page_weight_audit({"url": public_html_url(html_path)})
        page_result = {
            "url": audit.get("url"),
            "passed": bool(audit.get("passed")),
            "totalBytes": audit.get("totalBytes"),
            "imageBytes": audit.get("imageBytes"),
            "resourceCount": audit.get("resourceCount"),
            "failures": audit.get("failures", []),
            "issues": audit.get("issues", []),
        }
        pages.append(page_result)
        if not audit.get("passed"):
            failures.append(page_result)
    return {
        "ok": True,
        "profile": "seoimpuls-homepage-ideal",
        "passed": not failures,
        "pageCount": len(pages),
        "failureCount": len(failures),
        "failures": failures[:80],
        "pages": pages,
    }


def remote_join(*parts: str) -> str:
    clean_parts = [str(part).strip("/") for part in parts if str(part or "").strip("/")]
    prefix = "/" if parts and str(parts[0]).startswith("/") else ""
    return prefix + "/".join(clean_parts)


def deploy_page_to_server(page_url: str) -> dict:
    config = load_deploy_config()
    missing = [key for key in ("host", "username", "password", "remoteBase") if not str(config.get(key) or "").strip()]
    if missing:
        raise RuntimeError(f"Не заполнен deploy_config.local.json: {', '.join(missing)}")

    try:
        import paramiko
    except Exception as exc:
        raise RuntimeError("Для публикации нужен Python-пакет paramiko.") from exc

    compressor_cleanup = cleanup_unused_compressor_variants()
    build = run_hugo_build()
    if not build["ok"]:
        return {"ok": False, "stage": "build", "build": build}

    quality = page_weight_audit({"url": page_url})

    files = public_files_for_page_url(page_url)
    remote_base = str(config["remoteBase"]).rstrip("/")
    remote_public = f"{remote_base}/current/public"
    uploaded: list[dict] = []
    commands: list[dict] = []

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=str(config["host"]),
            port=int(config.get("port") or 22),
            username=str(config["username"]),
            password=str(config["password"]),
            timeout=20,
            auth_timeout=20,
            banner_timeout=20,
        )
        check_command = f"test -d {shlex.quote(remote_public)}"
        stdin, stdout, stderr = client.exec_command(check_command, timeout=30)
        out = stdout.read().decode("utf-8", "replace")
        err = stderr.read().decode("utf-8", "replace")
        code = stdout.channel.recv_exit_status()
        commands.append({"command": check_command, "code": code, "stdout": out[-4000:], "stderr": err[-4000:]})
        if code != 0:
            return {"ok": False, "stage": "remote-current", "build": build, "quality": quality, "compressorCleanup": compressor_cleanup, "commands": commands}

        sftp = client.open_sftp()
        try:
            made_dirs: set[str] = set()
            for file in files:
                rel = public_rel(file)
                remote_file = remote_join(remote_public, rel)
                remote_dir = posixpath.dirname(remote_file)
                if remote_dir not in made_dirs:
                    mkdir_command = f"mkdir -p {shlex.quote(remote_dir)}"
                    stdin, stdout, stderr = client.exec_command(mkdir_command, timeout=30)
                    out = stdout.read().decode("utf-8", "replace")
                    err = stderr.read().decode("utf-8", "replace")
                    code = stdout.channel.recv_exit_status()
                    commands.append({"command": mkdir_command, "code": code, "stdout": out[-4000:], "stderr": err[-4000:]})
                    if code != 0:
                        return {"ok": False, "stage": "remote-mkdir", "build": build, "compressorCleanup": compressor_cleanup, "commands": commands, "uploaded": uploaded}
                    made_dirs.add(remote_dir)
                sftp.put(str(file), remote_file)
                uploaded.append({"path": rel, "bytes": file.stat().st_size})
        finally:
            sftp.close()

        touched_roots = sorted({posixpath.dirname(remote_join(remote_public, public_rel(file))) for file in files})
        if touched_roots:
            chown_command = "chown -R fastuser:fastuser " + " ".join(shlex.quote(path) for path in touched_roots)
            stdin, stdout, stderr = client.exec_command(chown_command, timeout=120)
            out = stdout.read().decode("utf-8", "replace")
            err = stderr.read().decode("utf-8", "replace")
            code = stdout.channel.recv_exit_status()
            commands.append({"command": chown_command, "code": code, "stdout": out[-4000:], "stderr": err[-4000:]})
            if code != 0:
                return {"ok": False, "stage": "remote-chown", "build": build, "compressorCleanup": compressor_cleanup, "commands": commands, "uploaded": uploaded}
    finally:
        client.close()

    return {
        "ok": True,
        "pageUrl": str(page_url or ""),
        "domain": str(config.get("domain") or ""),
        "build": build,
        "quality": quality,
        "compressorCleanup": compressor_cleanup,
        "uploaded": uploaded,
        "commands": commands,
    }


def deploy_public_to_server() -> dict:
    config = load_deploy_config()
    missing = [key for key in ("host", "username", "password", "remoteBase") if not str(config.get(key) or "").strip()]
    if missing:
        raise RuntimeError(f"Не заполнен deploy_config.local.json: {', '.join(missing)}")

    try:
        import paramiko
    except Exception as exc:
        raise RuntimeError("Для публикации нужен Python-пакет paramiko.") from exc

    compressor_cleanup = cleanup_unused_compressor_variants()
    build = run_hugo_build()
    if not build["ok"]:
        return {"ok": False, "stage": "build", "build": build}

    quality = site_weight_audit()

    stamp = time.strftime("%Y%m%d-%H%M%S")
    archive = create_public_archive(stamp)
    remote_base = str(config["remoteBase"]).rstrip("/")
    release_dir = f"{remote_base}/releases/{stamp}"
    remote_archive = f"/tmp/seoimpuls-public-{stamp}.tar.gz"
    keep_releases = max(1, int(config.get("keepReleases") or 5))
    commands = [
        f"mkdir -p {remote_base}/releases {release_dir}",
        f"tar -xzf {remote_archive} -C {release_dir}",
        f"chown -R fastuser:fastuser {remote_base}",
        f"ln -sfn {release_dir} {remote_base}/current",
        f"rm -f {remote_archive}",
        f"cd {remote_base}/releases && ls -1dt 20* 2>/dev/null | tail -n +{keep_releases + 1} | xargs -r rm -rf",
    ]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    executed: list[dict] = []
    try:
        client.connect(
            hostname=str(config["host"]),
            port=int(config.get("port") or 22),
            username=str(config["username"]),
            password=str(config["password"]),
            timeout=20,
            auth_timeout=20,
            banner_timeout=20,
        )
        sftp = client.open_sftp()
        try:
            sftp.put(str(archive), remote_archive)
        finally:
            sftp.close()

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command, timeout=180)
            out = stdout.read().decode("utf-8", "replace")
            err = stderr.read().decode("utf-8", "replace")
            code = stdout.channel.recv_exit_status()
            executed.append({"command": command, "code": code, "stdout": out[-4000:], "stderr": err[-4000:]})
            if code != 0:
                return {"ok": False, "stage": "remote", "stamp": stamp, "build": build, "quality": quality, "compressorCleanup": compressor_cleanup, "commands": executed}
    finally:
        client.close()
        try:
            archive.unlink()
        except OSError:
            pass

    return {
        "ok": True,
        "stamp": stamp,
        "release": release_dir,
        "domain": str(config.get("domain") or ""),
        "build": build,
        "quality": quality,
        "compressorCleanup": compressor_cleanup,
        "commands": executed,
    }


class AdminHandler(BaseHTTPRequestHandler):
    server_version = "SeoimpulsAdmin/0.1"

    def log_message(self, fmt: str, *args) -> None:
        try:
            sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))
        except Exception:
            pass

    def redirect_to_login(self) -> None:
        target = urllib.parse.quote(self.path or "/", safe="")
        self.send_response(302)
        self.send_header("Location", f"/login?next={target}")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def serve_login(self, error: str = "") -> None:
        text_response(self, login_html(error), 200, "text/html")

    def require_auth(self, path: str) -> bool:
        if is_authenticated(self):
            return True
        if path.startswith("/api/"):
            return json_response(self, {"ok": False, "error": "Unauthorized"}, 401) or False
        self.redirect_to_login()
        return False

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:1314")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if path == "/login":
                return self.serve_login()
            if not self.require_auth(path):
                return
            if path.startswith("/site/"):
                return self.serve_site_proxy(path, parsed.query)
            if path == "/api/health":
                return json_response(
                    self,
                    {
                        "ok": True,
                        "projectRoot": str(PROJECT_ROOT),
                        "contentRoot": str(CONTENT_ROOT),
                        "hugo": "available",
                    },
                )
            if path == "/api/deploy/status":
                return json_response(self, {"ok": True, "deploy": deploy_config_status()})
            if path == "/api/server/pause":
                return json_response(self, {"ok": True, "pause": server_pause_status()})
            if path == "/api/pages":
                return json_response(self, {"ok": True, "pages": list_pages()})
            if path == "/api/page":
                rel = query.get("path", [""])[0]
                target = content_path(rel)
                if not target.exists() or target.suffix.lower() != ".md":
                    return error_response(self, "Page not found", 404)
                front, body, raw = read_markdown(target)
                normalize_front_builder_json(front)
                image_repair_report = repair_missing_builder_image_urls(front)
                return json_response(
                    self,
                    {
                        "ok": True,
                        "page": {
                            "path": target.relative_to(PROJECT_ROOT).as_posix(),
                            "frontmatter": front,
                            "body": body,
                            "raw": raw,
                            "revision": markdown_revision(raw),
                            "language": guess_language(target),
                            "section": page_section(target),
                            "key": page_key(target),
                        },
                        "imageRepair": image_repair_report,
                    },
                )
            if path == "/api/assets":
                include_usage = query.get("usage", ["1"])[0] != "0"
                return json_response(self, {"ok": True, "assets": list_assets(include_usage=include_usage)})
            if path == "/api/chrome":
                return json_response(self, {"ok": True, "chrome": normalize_chrome(load_chrome())})
            if path == "/api/menu":
                return json_response(self, {"ok": True, "menu": load_menu()})
            if path == "/api/backups":
                return json_response(self, {"ok": True, "backups": list_backups()})
            if path == "/api/trash":
                return json_response(self, {"ok": True, "trash": list_trash()})
            return self.serve_static(path)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            return
        except Exception as exc:
            return error_response(self, str(exc), 500)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if path == "/login":
                payload = read_post_payload(self)
                password = str(payload.get("password") or "")
                if AUTH_ENABLED and hmac.compare_digest(password, ADMIN_PASSWORD):
                    next_url = urllib.parse.parse_qs(parsed.query).get("next", ["/"])[0] or "/"
                    if not next_url.startswith("/"):
                        next_url = "/"
                    self.send_response(302)
                    self.send_header("Location", next_url)
                    self.send_header(
                        "Set-Cookie",
                        f"{SESSION_COOKIE_NAME}={auth_session_token()}; Path=/; HttpOnly; SameSite=Lax",
                    )
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    return
                return self.serve_login("Неверный пароль.")
            if not self.require_auth(path):
                return
            if path == "/api/files/upload" and "application/json" not in self.headers.get("Content-Type", ""):
                filename = query.get("filename", [""])[0] or self.headers.get("X-Upload-Filename", "")
                result = upload_download_file_stream(self, urllib.parse.unquote(filename))
                return json_response(self, {"ok": True, **result})
            payload = read_json(self)
            if path == "/api/page/save":
                rel = str(payload.get("path") or "")
                target = content_path(rel)
                ensure_content_file(target)
                if target.suffix.lower() != ".md":
                    return error_response(self, "Only markdown pages can be saved")
                allow_create = bool(payload.get("allowCreate", False))
                if not target.exists() and not allow_create:
                    return error_response(self, "Page not found", 404)
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                front = payload.get("frontmatter")
                body = payload.get("body")
                if not isinstance(front, dict) or not isinstance(body, str):
                    return error_response(self, "Expected frontmatter object and body string")
                normalize_front_builder_json(front, strict=True)
                with PAGE_SAVE_LOCK:
                    expected_revision = payload.get("expectedRevision")
                    current_raw = read_markdown(target)[2] if target.exists() else ""
                    if expected_revision is not None and expected_revision != markdown_revision(current_raw):
                        return error_response(self, "Страница уже изменена в другой вкладке или на диске. Ваши правки остались в редакторе. Сравните версии перед повторным сохранением.", 409)
                    ensure_home_feed_date(target, front)
                    backup = backup_file(target) if target.exists() else None
                    saved_text = dump_front_matter(front, body)
                    atomic_write_markdown(target, saved_text)
                return json_response(
                    self,
                    {
                        "ok": True,
                        "error": "",
                        "path": target.relative_to(PROJECT_ROOT).as_posix(),
                        "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
                        "frontmatter": front,
                        "body": body,
                        "revision": markdown_revision(saved_text),
                        "autoImageOptimization": {"count": 0, "replacements": []},
                        "imageRepair": {"changed": 0, "replacements": []},
                        "compressorCleanup": {"removed": [], "kept": []},
                        "build": {"ok": None, "skipped": True, "reason": "admin-save-only"},
                    },
                )
            if path == "/api/page/create":
                result = create_page(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/page/move":
                result = move_page(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/page/weight-audit":
                result = page_weight_audit(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/page/delete":
                result = delete_page(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/assets/delete":
                result = delete_asset(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/assets/compress":
                result = compress_asset(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/services-hub/image":
                result = update_services_hub_image(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/bases-card/image":
                result = update_bases_card_image(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/assets/upload":
                filename = slugify(Path(str(payload.get("filename") or "upload")).stem)
                suffix = Path(str(payload.get("filename") or "")).suffix.lower() or ".bin"
                data_url = str(payload.get("dataUrl") or "")
                match = re.match(r"^data:[^;]+;base64,(.+)$", data_url)
                if not match:
                    return error_response(self, "Expected base64 dataUrl")
                UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
                target = unique_upload_target(filename, suffix)
                target.write_bytes(base64.b64decode(match.group(1)))
                rel = target.relative_to(PROJECT_ROOT).as_posix()
                original_url = "/" + rel.removeprefix("static/")
                auto_report: dict = {"replacements": []}
                optimized_url = auto_optimize_image_url(original_url, {}, auto_report)
                optimized_path = rel
                if optimized_url != original_url:
                    try:
                        optimized_path = asset_file_from_url_or_rel(optimized_url).relative_to(PROJECT_ROOT).as_posix()
                    except Exception:
                        optimized_path = rel
                return json_response(
                    self,
                    {
                        "ok": True,
                        "path": optimized_path,
                        "url": optimized_url,
                        "originalPath": rel,
                        "originalUrl": original_url,
                        "autoImageOptimization": {"count": len(auto_report.get("replacements") or []), **auto_report},
                    },
                )
            if path == "/api/files/upload":
                result = upload_download_file(payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/chrome/save":
                chrome = normalize_chrome(payload.get("chrome") if isinstance(payload.get("chrome"), dict) else payload)
                CHROME_PATH.parent.mkdir(parents=True, exist_ok=True)
                backup = backup_file(CHROME_PATH) if CHROME_PATH.exists() else None
                CHROME_PATH.write_text(json.dumps(chrome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                return json_response(
                    self,
                    {
                        "ok": True,
                        "path": CHROME_PATH.relative_to(PROJECT_ROOT).as_posix(),
                        "backup": backup.relative_to(PROJECT_ROOT).as_posix() if backup else "",
                    },
                )
            if path == "/api/menu/save":
                result = save_menu(payload.get("menu") if isinstance(payload.get("menu"), dict) else payload)
                return json_response(self, {"ok": True, **result})
            if path == "/api/backups/restore":
                backup_path = str(payload.get("backupPath") or "")
                result = restore_backup(backup_path)
                return json_response(self, {"ok": True, **result})
            if path == "/api/trash/restore":
                trash_path = str(payload.get("trashPath") or "")
                result = restore_trash(trash_path)
                return json_response(self, {"ok": True, **result})
            if path == "/api/trash/preview":
                trash_path = str(payload.get("trashPath") or "")
                result = preview_trash(trash_path)
                return json_response(self, {"ok": True, **result})
            if path == "/api/trash/delete":
                trash_path = str(payload.get("trashPath") or "")
                result = delete_trash_item(trash_path)
                return json_response(self, {"ok": True, **result})
            if path == "/api/trash/delete/undo":
                token = str(payload.get("undoToken") or "")
                result = undo_delete_trash_item(token)
                return json_response(self, {"ok": True, **result})
            if path == "/api/build":
                result = run_hugo_build()
                return json_response(self, result, 200 if result["ok"] else 500)
            if path == "/api/deploy":
                result = deploy_public_to_server()
                return json_response(self, result, 200 if result["ok"] else 500)
            if path == "/api/deploy/page":
                page_url = str(payload.get("url") or "")
                result = deploy_page_to_server(page_url)
                return json_response(self, result, 200 if result["ok"] else 500)
            if path == "/api/server/pause":
                action = str(payload.get("action") or "toggle").strip().lower()
                current = server_pause_status()
                if action == "toggle":
                    paused = not bool(current.get("paused"))
                elif action in {"pause", "off", "disable"}:
                    paused = True
                elif action in {"resume", "on", "enable"}:
                    paused = False
                else:
                    return error_response(self, "Unknown pause action", 400)
                result = set_server_pause(paused)
                return json_response(self, result, 200 if result["ok"] else 500)
            if path == "/api/preview/start":
                result = start_hugo()
                return json_response(self, {"ok": True, **result})
            if path == "/api/open":
                target = str(payload.get("target") or "")
                if target == "project":
                    os.startfile(PROJECT_ROOT)  # type: ignore[attr-defined]
                elif target == "public":
                    os.startfile(PROJECT_ROOT / "public")  # type: ignore[attr-defined]
                return json_response(self, {"ok": True})
            return error_response(self, "Unknown endpoint", 404)
        except subprocess.TimeoutExpired:
            return error_response(self, "Command timed out", 500)
        except Exception as exc:
            return error_response(self, str(exc), 500)

    def serve_static(self, request_path: str) -> None:
        if request_path == "/":
            request_path = "/index.html"
        rel = urllib.parse.unquote(request_path).lstrip("/")
        target = safe_join(UI_ROOT, rel)
        if not target.exists() or not target.is_file():
            target = safe_join(STATIC_ROOT, rel)
        if not target.exists() or not target.is_file():
            target = safe_join(PUBLIC_ROOT, rel)
        if not target.exists() or not target.is_file():
            return text_response(self, "Not found", 404)
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def serve_site_proxy(self, request_path: str, query: str = "") -> None:
        site_path = "/" + request_path.removeprefix("/site/").lstrip("/")
        target_url = f"http://127.0.0.1:1314{site_path}"
        if query:
            target_url += "?" + query
        try:
            with urllib.request.urlopen(target_url, timeout=10) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "application/octet-stream")
        except Exception:
            public_target = public_file_for_url(site_path)
            if not public_target.exists() or not public_target.is_file():
                return text_response(self, "Site page not found. Start Hugo preview or build site.", 404)
            data = public_target.read_bytes()
            content_type = mimetypes.guess_type(public_target.name)[0] or "text/html; charset=utf-8"

        if "text/html" in content_type.lower():
            html = data.decode("utf-8", errors="replace")
            html = re.sub(r'((?:href|src)=["\'])/(?!/)', r'\1/site/', html)
            html = re.sub(r'(srcset=["\'])(/[^"\']+)(["\'])', lambda match: match.group(1) + match.group(2).replace("/ ", "/site/ ").replace("/", "/site/", 1) + match.group(3), html)
            data = html.encode("utf-8")
            content_type = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        if "text/html" in content_type.lower():
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run() -> None:
    port = int(os.environ.get("SEOIMPULS_ADMIN_PORT", "8787"))
    allow_port_fallback = os.environ.get("SEOIMPULS_ADMIN_PORT_FALLBACK") == "1"
    for candidate_port in range(port, port + 50):
        if local_port_is_open(candidate_port):
            if not allow_port_fallback:
                raise OSError(f"Local admin port {candidate_port} is already in use")
            continue
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate_port), AdminHandler)
            port = candidate_port
            break
        except OSError:
            if not allow_port_fallback:
                raise
    else:
        raise OSError(f"No free local admin port found from {port} to {port + 49}")
    url = f"http://127.0.0.1:{port}/"
    print(f"Seoimpuls admin: {url}")
    print(f"Project: {PROJECT_ROOT}")
    threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if HUGO_PROCESS and HUGO_PROCESS.poll() is None:
            HUGO_PROCESS.terminate()
        server.server_close()


if __name__ == "__main__":
    run()
