# RU link-building sales page — candidate retirement, 2026-10-15

Former URL: /uslugi-linkbildinga/linkbilding/
Source: content/services/linkbilding/index.ru.md

The former product offered tiered paid links on Web 2.0 sites, blogs and forums to manipulate organic ranking signals. It is withdrawn rather than repackaged as compliant SEO.

Change scope: draft the original page; remove the exact image and button cards leading to it from content/services/_index.ru.md; change the RU homepage newsUrl to /ru/news/ so the fallback news block no longer targets a retired commercial page.

CI blocks publication of the old URL and its inbound hyperlinks/sitemap entry using docs/retired-routes-en.txt and scripts/verify_retired_routes.py. After Hugo build ensure /ru/news/ exists if used as a fallback.

No production HTTP 301, 404 or 410 implemented. Final RETIRE_410 decision requires live crawl, GSC, canonicals and external link evidence. Other legal offerings remain in source for proper migration.

The source baseline in main, the live server, DNS, GitHub Pages and VDSina referral destination are unchanged. Complete localized SERP and responsive QA remain pending.
