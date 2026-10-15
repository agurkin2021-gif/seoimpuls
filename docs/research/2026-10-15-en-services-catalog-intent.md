# Clean EN services catalog — 2026-10-15

## Architecture and intent ownership
- `/` general SEO value proposition for business audiences.
- `/services/` navigational catalog for choosing scope and deliverables. Avoid competing with primary technical SEO informational-commercial page; directory should only summarize offerings.
- `/seo/` detailed technical SEO audit and optimization services.
- `/services/keyword-research/` dedicated query research, clustering and mapping.
- `/services/seo-consultation/` planned; link only after completed and verified.
- Old `/link-building-services/` does **not** automatically become a 301 to `/services/` because user intent is materially different; pending GSC and live URL migration review.

## Specific legacy errors addressed
- Old catalog was named Link Building Services, including backlink, DR, tier, microsite/pyramid services.
- Its builder included positional offsets and fallback generation of tier cards, inappropriate for legitimate SEO.
- New EN catalog contains ONLY technical audits and keyword research in concise individual cards plus true deliverables and contact information.
- Associated EN navigation now points to /services/ and /seo/. The keyword research page's breadcrumb should now use the clean section parent.

## Remaining issues
- Other EN old service pages still exist in working branch until deliberate 410/301 migrations.
- RU and ES sections retain original taxonomy and are not production-ready.
- Canonical, sitemap and SEO output are validated via GitHub Actions, but not via full browser screenshots or Search Console.
