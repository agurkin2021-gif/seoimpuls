# SEOImpuls — EN homepage visual system, Stage 01 (2026-10-16)

## Scope
Owner's explicit instruction: DESIGN ONLY the English homepage. Never proceed to commercial detail pages, About, FAQ, news, or RU/ES page designs unless separately authorized. Build only in `white-seo-rebuild`; preview GitHub Pages is allowed, production is not. Existing seven-card EN/RU content and navigation, EN Title/H1/canonical, and all detail URLs must remain intact.

## Diagnosis (from current preview and source)
The EN first viewport presented a large headline, explanatory paragraph and two CTAs above an unrelieved three-column grid. No editorial counterweight or page-specific composition distinguished the homepage from an inner page. Shared `.seo-central--en` styling also affects RU by inheritance, so new visual design must use an EN-exclusive root class and render condition.

## Style direction
**Editorial technical minimalism, not generic AI effects.**
- Keep existing brand mark and dark navy theme. Pale slate text with restrained matte-cyan accent; no photos, orbs, glass cards, fabricated dashboards, metrics or client results.
- Typography: use existing system stack; expressive but readable H1 and small tracked category kicker. No external font request.
- Diagram: one source-controlled, inline, accessible SVG schematic containing three visually connected phases: Search Intent, Website Pages, Technical Checks. Conceptual process only, no fake traffic or ranking.
- Layout: asymmetric two-column hero on wide screens, stack on narrower screens; preserve established 120px tablet/desktop gutter for floating contact controls. Hero CTAs retain existing valid anchors and exact text.
- Performance: CSS + SVG only, no JS/dependencies or external artwork. Respect reduced motion. No new crawled content or misleading SEO outcomes.
- EN-only isolation: class `.seo-central--art-directed` and conditional `en-home-hero-diagram.html`; explicit `{{ if eq $lang "en" }}` stylesheet. RU/ES output must not contain the design class or diagram.

## Iterative acceptance
1. Baseline read of EN hero markup and existing home layout.
2. Stage-01 hero composition and original inline vector schematic.
3. Run strict Hugo/SEO/whitehat/context guard and EN/RU 390/768/1280 visual browser gates. Assert EN figure present, no external media or clipping, no copy/figure collision, and RU figure absent.
4. Open actual published noindex EN preview and inspect full first fold at desktop; inspect mobile artifacts. Repair until checks pass.
5. Record exact tested commit, completed limitations and next visual step in `CHATGPT_PROJECT_CONTEXT.md`.

Later stages, within EN homepage only: improve card iconography and section rhythm after hero acceptance. No automatic modification of other pages.
