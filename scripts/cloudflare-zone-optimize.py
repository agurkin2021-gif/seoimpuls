#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DOMAIN = "seoimpuls.com"
API = "https://api.cloudflare.com/client/v4"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN")

def api(method, path, payload=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            data = json.loads(raw)
        except Exception:
            data = {"success": False, "errors": [{"message": raw[:500]}]}
        return exc.code, data
    except Exception as exc:
        return 0, {"success": False, "errors": [{"message": str(exc)}]}

def message(data):
    errs = data.get("errors") or []
    if errs:
        return "; ".join(str(x.get("message", x)) for x in errs)[:500]
    return "unknown API error"

if not TOKEN:
    print("Cloudflare zone optimization: API token not exposed to custom build; skipped.")
    sys.exit(0)

status, data = api("GET", "/zones?" + urllib.parse.urlencode({"name": DOMAIN}))
if status != 200 or not data.get("success") or not data.get("result"):
    print(f"Cloudflare zone optimization: cannot resolve zone ({status}): {message(data)}")
    sys.exit(0)

zone_id = data["result"][0]["id"]
print("Cloudflare zone optimization: zone resolved.")

for setting in ("early_hints", "speed_brain"):
    status, data = api("PATCH", f"/zones/{zone_id}/settings/{setting}", {"value": "on"})
    if status == 200 and data.get("success"):
        print(f"Cloudflare zone optimization: {setting}=on")
    else:
        print(f"Cloudflare zone optimization: {setting} unchanged ({status}): {message(data)}")

rule = {
    "expression": "true",
    "description": "SEOImpuls cache everything 2h",
    "action": "set_cache_settings",
    "action_parameters": {
        "cache": True,
        "edge_ttl": {
            "mode": "override_origin",
            "default": 7200
        }
    },
    "enabled": True
}

status, data = api(
    "GET",
    f"/zones/{zone_id}/rulesets/phases/http_request_cache_settings/entrypoint"
)

if status == 200 and data.get("success") and data.get("result"):
    ruleset = data["result"]
    ruleset_id = ruleset["id"]
    existing = next(
        (r for r in ruleset.get("rules", [])
         if r.get("description") == rule["description"]),
        None
    )
    if existing:
        status, data = api(
            "PATCH",
            f"/zones/{zone_id}/rulesets/{ruleset_id}/rules/{existing['id']}",
            rule
        )
    else:
        status, data = api(
            "POST",
            f"/zones/{zone_id}/rulesets/{ruleset_id}/rules",
            rule
        )
elif status == 404:
    status, data = api(
        "POST",
        f"/zones/{zone_id}/rulesets",
        {
            "name": "SEOImpuls cache rules",
            "description": "Production cache settings for seoimpuls.com",
            "kind": "zone",
            "phase": "http_request_cache_settings",
            "rules": [rule]
        }
    )
else:
    print(f"Cloudflare zone optimization: cache rules lookup failed ({status}): {message(data)}")
    sys.exit(0)

if status in (200, 201) and data.get("success"):
    print("Cloudflare zone optimization: cache everything enabled, Edge TTL=2h")
else:
    print(f"Cloudflare zone optimization: cache rule unchanged ({status}): {message(data)}")
