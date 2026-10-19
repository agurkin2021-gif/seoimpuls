#!/usr/bin/env bash
set -euo pipefail

HUGO_VERSION="0.154.5"
case "$(uname -m)" in
  x86_64|amd64) HUGO_ARCH="amd64" ;;
  aarch64|arm64) HUGO_ARCH="arm64" ;;
  *) echo "Unsupported architecture: $(uname -m)" >&2; exit 1 ;;
esac

HUGO_TGZ="/tmp/hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz"
HUGO_BIN="/tmp/hugo"

curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz" -o "$HUGO_TGZ"
tar -xzf "$HUGO_TGZ" -C /tmp hugo
chmod +x "$HUGO_BIN"

rm -rf public
"$HUGO_BIN" --minify --noBuildLock --baseURL "https://seoimpuls.com/"

python3 scripts/verify_en_home_schema.py
python3 scripts/verify_en_services_route.py
python3 scripts/verify_en_footer_popup.py
python3 scripts/verify_retired_routes.py --site public --routes docs/retired-routes-en.txt
python3 scripts/whitehat_content_gate.py --site public --strict

test -f public/index.html
test -f public/robots.txt
test -f public/sitemap.xml

echo "Cloudflare production build ready: $(find public -type f | wc -l) files"

# Keep Cloudflare zone performance settings aligned with production.
# This is non-fatal: a restricted build token must never block site deployment.
python3 scripts/cloudflare-zone-optimize.py || echo "Cloudflare zone optimization skipped; continuing production deploy."
