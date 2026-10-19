# Cloudflare production deployment

Production source is the repository default branch after the approved rebuild is promoted to `main`.

Cloudflare Workers build settings:

- Build command: leave empty
- Deploy command: `npx wrangler deploy`
- Root directory: `/`
- Preview builds: disabled

`wrangler.jsonc` runs `bash cloudflare-build.sh`. The build downloads the same pinned Hugo Extended version used by repository QA (0.154.5), builds production URLs for seoimpuls.com, runs core release gates, and publishes only `public/`.

Source files, Git metadata, scripts, docs, vendored Hugo source and repository maintenance files are never part of the static asset directory.

Custom-domain routes are intentionally added only after the workers.dev build is verified and the conflicting legacy apex DNS record is removed.
