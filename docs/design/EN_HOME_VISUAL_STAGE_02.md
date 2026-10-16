# EN homepage design — Stage 02: Service index

Date: 2026-10-16. Branch: `white-seo-rebuild`. Scope: English homepage only.

## Before
Published EN screenshot: hero is distinctive, but the first six SEO service cards are near-identical dark rectangles with numbered badges and long equal-weight paragraphs. User asked for independent art direction and no generic generated-image look. The fixed contacts panel remains a separate UX concern.

## Visual decisions
- Retain seven approved service IDs, text, result clauses, four real detail-page links, three enquiry anchors and full-width SEO Retainer.
- Use seven bespoke schematic inline SVG glyphs (not generic emoji, Font Awesome or external images). Each glyph encodes the service meaning, uses square geometry inspired by the hero flow diagram, and has no external dependencies.
- Consistent hierarchy: small editorial kicker, service title and glyph, description, distinct result field, accessible link. Matte navy surfaces, restrained cyan, no glass/neon/gradients for ordinary cards, no fictional numbers or badges.
- Isolate code under `.seo-central--art-directed`, rendered exclusively in English Hugo template branch. RU/ES unchanged.
- Three columns wide, two at 768px, one at 390px; retainer full-width at desktop. Retain keyboard focus and reduced motion.
- Scope of this pass excludes other sections, header, sitewide CSS, internal pages, content claims, production.

## Acceptance protocol
Committed source is not proof of visual quality. Require passing strict Hugo, SEO/whitehat, EN/RU browser audit and general homepage browser + WCAG diagnostics at 390/768/1280. Inspect published EN preview in browser; reject visual awkwardness after screenshots. Log actual run IDs and outstanding findings in `CHATGPT_PROJECT_CONTEXT.md`.
