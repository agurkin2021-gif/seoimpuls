# EN retirement: tiered link-building sales page — 2026-10-15

Source: `content/services/link-building/index.md`.
Former published URL: `/link-building-services/link-building/`.
State in candidate `white-seo-rebuild`: `draft: true`, `showOnHome: false`.
Business reason: The page advertises backlinks from forums/blogs and tiered link-placement packages to manipulate ranking signals. There is no ethically equivalent replacement with the same transactional search intent. Merely renaming this service “outreach”, “mentions” or “digital PR” would be misleading.

Decision: `RETIRE_410` is **provisional for the final live deployment**. This commit does not return 410 or 301 on the existing live server. Do not redirect to `/services/` or `/seo/`: these services do not fulfil the former ranking-link purchase intent.

Related content: `/link-building-services/backlinks/` has also been retired from the candidate. The new English homepage and services catalog do not directly link to this old URL; a shared Hugo services-hub template formerly guessed URLs, and that behaviour was eliminated in the preceding commit.

Automated guard: `docs/retired-routes-en.txt` contains this URL. `scripts/verify_retired_routes.py` rejects generated HTML, hyperlinks, declared card URLs, and sitemap entries for it.

Known limitations: Detailed GSC clicks/impressions/canonicals, offsite backlinks, live HTTP and deployment status have not been checked; exact Google organic SERP top-10 was not obtained and is not required to justify withdrawal of a discontinued manipulative service. Full RU/ES remediation remains separate.

Acceptance criteria: candidate Hugo build PASS; retired-route check PASS; context guard PASS; later a full live migration audit before production release. Release readiness remains blocked by other legacy services.
