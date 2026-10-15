# RU /soft/ — unintended affiliate redirect removal

Date: 2026-10-15
Source file: `static/ru/soft/index.html`. Candidate URL: `/ru/soft/`.
Original file: an immediate HTML meta refresh and JavaScript `window.location.replace('/go/vdsina/')` with a "Continue" anchor. This is not a software resource and misleadingly sends visitors from a software URL to an unrelated referral.

Decision: delete ONLY `static/ru/soft/index.html` from `white-seo-rebuild` and register `/ru/soft/` as a retired candidate route. Original remains in `main`. No 301/410 decision has been applied to the live server; no replacement page or redirect is asserted.

The provider-specific affiliate endpoint `/go/vdsina/` remains intact, including the original partner destination and `noindex` setting. Relevant links to it can be retained after per-page intent, notice, and rel review.

Evidence: generated build audit #38783627099 found 14 affiliate anchors on 9 pages, 13 with JavaScript-intercepted targets, one with a misleading label. This old /ru/soft/ page was one of them. Its removal should be verified through the blocking retired-route test and affiliate inventory in the next GitHub Actions run.

Risk: any internal link pointing to /ru/soft/ will fail the retired-route check and must be corrected at its source. ES /es/soft/ and other gray pages remain for separate passes; no blanket exemption is granted to affiliate redirects.
