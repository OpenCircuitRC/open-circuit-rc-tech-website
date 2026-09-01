# Open Circuit RC & Tech Website - Worker deployment

This version uses a Cloudflare Worker with Static Assets.

- `worker.js` handles `/api/videos` directly.
- `public/` contains the website files.
- No Cloudflare Pages `functions/` directory is required.
- No YouTube Data API key is required.

Deploy with `npx wrangler deploy`.
