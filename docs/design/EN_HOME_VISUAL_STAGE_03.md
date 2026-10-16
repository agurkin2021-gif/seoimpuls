# English homepage design — Stage 03: Section rhythm

2026-10-16. Branch `white-seo-rebuild`. Only the English homepage.

## Visual audit
Source and published-browser screenshot show too many adjacent dark card grids after the service index. These visually flatten distinct concepts: decision process, SEO explanation, examples of deliverables, practical objections, and project contact. Repeating the same rectangular panels gives everything equal importance. There is no value in adding more icons to every row.

## Differentiation
1. Process: one disciplined panel with a connected 01–03 step track; vertical on phones; headings and accepted copy unchanged.
2. Definition: side-by-side editorial heading and readable paragraph on large screens; full-width stacked on compact devices.
3. Outputs: replace three generic cards with a three-row, document-style ledger; names and descriptions unchanged. Not fixed packages.
4. Buyer FAQ: text-led question columns with single vertical keyline; no nested panels; FAQ links intact.
5. Final enquiry: a concluding visual panel with distinct matte background, cyan top rule and existing approved Telegram/consultation CTAs.

No external fonts, images, SVG, JS, fabricated metrics or new SEO claims. All selectors use `.seo-central--art-directed`; the existing RU home is rendered through a separate conditional partial and ES lacks the art-directed class.

## Verification
Must run strict Hugo/SEO, context, preview, browser on 390/768/1280, accessibility and manual screenshot examination. Footer overlay and full real-device WCAG/performance remain separate concerns.
