const CHANNEL_ID = "UC-fU_-yuEwnVY7F-mVAfO6w";

function readTag(entry, tag) {
  const match = entry.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
  return match ? match[1].replace(/<!\[CDATA\[|\]\]>/g, "").trim() : "";
}

async function getVideos() {
  const feedUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;
  const response = await fetch(feedUrl, {
    headers: { "User-Agent": "OpenCircuit-RC-Tech-Website/1.0" },
    cf: { cacheTtl: 300, cacheEverything: true }
  });

  if (!response.ok) {
    throw new Error(`YouTube feed returned HTTP ${response.status}`);
  }

  const xml = await response.text();
  const entries = [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)];

  const videos = entries.map(([, entry]) => {
    const id = readTag(entry, "yt:videoId");
    const title = readTag(entry, "title");
    const published = readTag(entry, "published");
    const updated = readTag(entry, "updated");
    const linkMatch = entry.match(/<link[^>]+rel="alternate"[^>]+href="([^"]+)"/);

    return {
      id,
      title,
      published,
      updated,
      url: linkMatch?.[1] || `https://www.youtube.com/watch?v=${id}`,
      thumbnail: id ? `https://i.ytimg.com/vi/${id}/hqdefault.jpg` : ""
    };
  }).filter(v => v.id && v.title);

  videos.sort((a, b) => new Date(b.published || b.updated || 0) - new Date(a.published || a.updated || 0));
  return videos;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Canonicalize the site to the root domain.
    // Keep the path and query string intact.
    if (url.hostname === "www.opencircuitrc.com") {
      url.hostname = "opencircuitrc.com";
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === "/api/videos") {
      try {
        const videos = await getVideos();
        return Response.json(
          { videos },
          { headers: { "Cache-Control": "public, max-age=300" } }
        );
      } catch (error) {
        return Response.json(
          { error: "Unable to read YouTube feed.", details: String(error?.message || error) },
          { status: 502 }
        );
      }
    }

    return env.ASSETS.fetch(request);
  }
};
