# Open Circuit RC & Tech Website - v6

This version uses your supplied banner and transparent logo.

## Latest Videos

The Latest Videos section is now dynamic.

A Cloudflare Pages Function at `/api/videos` reads YouTube's public channel Atom feed server-side, then the homepage selects the newest matching video for:
- RC Reviews
- RC Boats
- Drones
- Tech

Each card displays the actual YouTube thumbnail and links directly to the actual video.

No YouTube Data API key is required.

## Important

The dynamic `/api/videos` function will NOT run when you double-click `index.html` on your Windows computer. That is normal.

Deploy the whole project to Cloudflare Pages. Once hosted, `/api/videos` will run automatically and the Latest Videos section will populate.

Until then, the page has a fallback so it remains usable locally.

## Cloudflare Pages

Upload the entire project. No build command is required.

The project root contains:
- index.html
- styles.css
- script.js
- site-config.js
- functions/api/videos.js
- assets/
