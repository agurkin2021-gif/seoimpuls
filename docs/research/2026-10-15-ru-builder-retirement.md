# RU SEO Strategy Builder — candidate retirement assessment

Date: 2026-10-15
Source: content/strategy-builder/index.ru.md
Original candidate route: /ru/konstruktor-seo-strategii/
Decision: DRAFT_PENDING_REVIEW for new Hugo candidate, not an implemented live HTTP 301/404/410.

The existing page advertised "линкбилдинг, инфраструктура и контролируемое выполнение", using the shared strategy-builder layout that contains backlink and automation guidance. This offering does not meet the strictly white-hat SEO scope. Rewriting only the title/description without replacing the tool would mislead visitors. The page is therefore withheld from the rebuilt output; the baseline remains on main.

Homepage link repair: content/_index.ru.md formerly sent its primary hero CTA to the retired builder. Now primary points to existing /ru/seo/ with visible label "SEO-услуги"; secondary points to existing /ru/about/ with visible label "О компании". The homepage's offerItem8 no longer claims to direct users to the builder. Layout fallback for already withdrawn RU and EN builders is pointed at existing legitimate SEO content; ES remains unchanged pending its separate localized retirement.

Why not 301 now: the old builder's intent is not equivalent to a technical SEO services page, so redirecting the historical URL to /ru/seo/ could be misleading. The updated homepage CTA is not a server redirect; the historical URL's final HTTP treatment needs GSC and live crawl data during migration.

Candidate checks: add /ru/konstruktor-seo-strategii/ to docs/retired-routes-en.txt, use scripts/verify_retired_routes.py in CI to detect generated pages or links, and parse the rendered RU hero buttons to test href and label plus destination page existence. CI and responsive/visual quality must be checked separately. Other gray RU homepage content and ES legacy builder remain outside this bounded pass.

No modifications to main, published seoimpuls.com, DNS, Cloudflare or GitHub Pages.
