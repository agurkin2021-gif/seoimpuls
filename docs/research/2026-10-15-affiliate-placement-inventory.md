# Affiliate placement inventory — candidate-build review

Date: 2026-10-15. Branch: white-seo-rebuild. Status: UNVERIFIED until the GitHub Actions report is reviewed.

Owner decision: preserve genuine, relevant, transparent affiliate redirects. Do not delete the /go/vdsina/ endpoint just because the site offers SEO services. Do not substitute unrelated /soft/, SEO audit, cases, menu or generic service links.

Source-level candidates discovered so far:
- RU homepage (content/_index.ru.md): VPS-specific card2 and an infrastructure paragraph reference the VDSina partner URL. Context may be relevant, but the rendered link label, affiliate disclosure and ranking claims need a separate review.
- ES homepage (content/_index.es.md): same kind of VPS card2 and infrastructure paragraph; not automatically approved.
- RU strategy builder (content/strategy-builder/index.ru.md): VPS banner in a legacy SEO-strategy tool. The legacy tool itself remains a gray-content release blocker.
- ES strategy builder (content/strategy-builder/index.es.md + shared layout): fallback VPS banner in a legacy SEO-strategy tool; gray-content blocker.
- RU soft page: the candidate still appears in the rendered affiliate link diagnostic even though English /soft/ is a draft. Recheck page content and placement.
- The /go/vdsina/ static redirect endpoint is retained. This is not an organic SEO landing page.

Report source: Run python3 scripts/audit_affiliate_links.py --site public after a Hugo build; the GitHub Actions rebuild workflow reports every rendered link and its visible anchor text, rel attributes, and client-side intercepted target. The output is an INVENTORY, not an allowlist or a release approval.

Approval conditions per referring page: accurate destination/CTA; genuinely relevant intent; visible and truthful referral disclosure on-page; rel="sponsored nofollow" for monetary links; no hidden substitution and no gray service copy. Preserve useful referral functions only on pages meeting these conditions. An unchanged vendor endpoint alone is insufficient evidence.

The existing whitehat_content_gate.py deliberately remains conservative until the inspected references are resolved; the final strict gate must not pass by simply suppressing /go/vdsina/ diagnostics.
