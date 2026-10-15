# White-hat release readiness — baseline gate (2026-10-15)

This document describes the required NO-GRAY-SERVICES gate for SEOImpuls. Production must not be modified during this rebuild.

## Tool
`scripts/whitehat_content_gate.py`, standard-library-only Python.

Commands after Hugo builds to `public/`:
- Informational during work: `python3 scripts/whitehat_content_gate.py --site public`.
- **Blocking at release:** `python3 scripts/whitehat_content_gate.py --site public --strict`.

The informational step runs in the rebuild GitHub Actions workflow. It prints summary findings and up to 40 examples, but deliberately exits successfully while the rebuild is incomplete. A successful CI workflow **does not mean release-readiness** while blockers remain.

The strict command fails for any remaining:
- Old link-building product URL namespaces EN/RU/ES, strategy-builder/soft, unrelated /go/vdsina/ endpoint.
- Visible legacy promotion terms (EN/RU/ES), including backlinks, mass links, tiers, automated posting tools, artificial Domain Rating and satellite networks.
- Broken navigation pointing to old product namespaces.
- Legacy URLs still included in Hugo sitemap.

## Diagnostic scope
The audit checks *rendered HTML*, internal links and sitemap. It does NOT validate:
- Live HTTP 301/410, Search Console or Google index status.
- External links, client-side JavaScript-generated content, and unrendered source files.
- Detailed hreflang consistency, page speed, accessibility and mobile screenshot quality.
- Third-party backlink sources or business relevance of all offered services.
Those require independent checks. A passing strict gate is necessary but **not sufficient** for publication.

## Known historical source risk
- The original `content/services` contains 27 EN/ES/RU legacy commercial product pages under the three banned URL namespaces, many about link placement, Tier, DR or satellite sites.
- `content/strategy-builder` renders an algorithmic strategy builder backed by `layouts/strategy-builder/single.html`, a template with many legacy link/tier references.
- `content/soft` contains near-empty software section(s).
- `layouts/partials/services-hub.html`, global navigation in `hugo.toml` and language homepages may re-introduce old material.
- Static affiliate endpoint `static/go/vdsina/index.html` must be removed from the candidate release if unrelated to legitimate agency services.

## Migration process
1. Keep the unmodified legacy source only in main, never deploy it via GitHub Pages.
2. Replace legitimate existing offerings with their exact-intent white-hat successor.
3. For unethical offerings, retire the service pages in working branch; use 410/404 in production when approved rather than misleading blanket redirect.
4. Fix all internal links, menus, hreflang, canonicals, and sitemap, then run strict gate.
5. Compare live URL inventory, Search Console and incoming links before final migrations, conduct browser/visual QA, confirm readiness explicitly and publish only by separately authorized action.

No live routes or redirects are implemented by this document.
