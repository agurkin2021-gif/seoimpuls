# SEOImpuls EN homepage — WCAG contrast, keyboard and PageSpeed checkpoint (2026-10-15)

## Page under audit
- EN homepage only, branch `white-seo-rebuild`; production remains `https://seoimpuls.com/`.
- Lighthouse mobile URL (GitHub Pages Preview, not production): https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fagurkin2021-gif.github.io%2Fseoimpuls%2F&form_factor=mobile
- PageSpeed lab screenshot/time viewed in connected Opera on 2026-10-15 (approx. 21:15 local AR): Performance **98**, Accessibility **95**, Best Practices **100**, SEO **66**; First Contentful Paint **0.9s**, Largest Contentful Paint **0.9s**, Total Blocking Time **0ms**, CLS **0**, Speed Index **3.8s**.
- Google PageSpeed Insights returned **no CrUX field experience data** for this preview URL. These are a single lab run, not field Core Web Vitals or a guarantee of stable metrics.
- Lighthouse SEO 66 is driven by `Page isn't indexable` on **intentionally noindex GitHub Pages preview**. Do not remove noindex, modify production canonical, or interpret 66 as the SEO quality of production build.
- GSC at `search.google.com/search-console?resource_id=sc-domain:seoimpuls.com` redirected to sign-in/about in current Opera browser. Search Console performance cannot be independently retrieved in this session; query-to-URL cannibalization still `GSC_PENDING`.

## Independent axe WCAG diagnostic
GitHub Actions run: https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38828758946 — completed. `axe-core@4.10.3` tested WCAG 2.0/2.1/2.2 A/AA after dismissing optional cookie banner in Chromium at 390 and 1280 CSS px. Saved `accessibility.json` artifact.
- Both widths: **one confirmed serious `color-contrast` failure**, same element: bottom CTA link `<a class="seo-cta seo-cta--primary" ...>Discuss Your Website</a>`.
- Actual computed colors: text `#a9a9b3`, background `#1f739f`, contrast **2.24:1**, required **4.5:1** for 15px normal text. Verified root cause is CSS inheritance on final CTA, not guessed from visual appearance.
- Keyboard tab trace noted missing outline on some CTA buttons. These need a visible focus indicator separate from pointer hover.
- Other contrast checks and aria-prohibited attributes were marked `incomplete` by axe and cannot be reported as passing/failing without review. This automated run does not certify complete WCAG compliance.

## EN-home-only CSS correction committed
- Target only the English homepage scope CTA `a.seo-cta--primary` in `layouts/index.html`. Enforce white `#fff` text for normal/visited/hover/focus states and weight 700; on normal background `#1f739f` white has ~**5.24:1** expected contrast (calculated WCAG relative luminance, must confirm with rerun).
- Ensure all English homepage `a.seo-cta:focus-visible` have high visibility with 3px solid cyan outline and 3px offset plus focus halo.
- Regression gate in `scripts/audit_en_home_accessibility.cjs` now fails any serious/critical axe violation or English CTA keyboard-focus outline below 2 px. Rerun and actual results must be read before claiming accessibility PASS.
- No user content/H1/metadata/routes/footer changes; no RU/ES, main or production deployment.

## Other open checks
- Actual GSC and query overlap of / vs /services/ need authenticated Search Console or user-supplied evidence; no speculative keyword retargeting.
- Verify dark/light theme focus & contrast (automated test currently starts default dark).
- Some persistent first-screen cookie overlay height remains a P2 UX note; dismissible, not a blocking failure.
- CrUX field performance, human keyboard/screenreader audit and full reciprocal hreflang equivalence are not certified.
