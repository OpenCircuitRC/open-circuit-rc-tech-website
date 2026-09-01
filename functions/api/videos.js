export async function onRequestGet() {
  const channelId = "UC-fU_-yuEwnVY7F-mVAfO6w";
  const feedUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;

  try {
    const response = await fetch(feedUrl, {
      headers: { "User-Agent": "OpenCircuit-RC-Tech-Website/1.0" }
    });

    if (!response.ok) {
      return Response.json(
        { error: `YouTube feed returned HTTP ${response.status}` },
        { status: 502 }
      );
    }

    const xml = await response.text();
    const entries = [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)];

    const decodeXml = (value) => value
      .replace(/<!\[CDATA\[/g, "")
      .replace(/\]\]>/g, "")
      .replace(/&amp;/g, "&")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .trim();

    const getTag = (entry, tag) => {
      const escapedTag = tag.replace(":", "\\:");
      const m = entry.match(new RegExp(`<${escapedTag}[^>]*>([\s\S]*?)<\/${escapedTag}>`));
      return m ? decodeXml(m[1]) : "";
    };

    const videos = entries.map(match => {
      const entry = match[1];
      const videoId = getTag(entry, "yt:videoId");
      const title = getTag(entry, "title");
      const published = getTag(entry, "published");
      const updated = getTag(entry, "updated");
      const linkMatch = entry.match(/<link[^>]+rel=["']alternate["'][^>]+href=["']([^"']+)["']/i);
      const url = linkMatch ? linkMatch[1] : `https://www.youtube.com/watch?v=${videoId}`;

      return {
        id: videoId,
        title,
        published,
        updated,
        url,
        thumbnail: videoId ? `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg` : ""
      };
    }).filter(v => v.id && v.title);

    videos.sort((a, b) => new Date(b.published || b.updated || 0) - new Date(a.published || a.updated || 0));

    return Response.json({ videos }, {
      headers: {
        "Cache-Control": "public, max-age=900, s-maxage=900"
      }
    });
  } catch (error) {
    return Response.json({ error: "Unable to read YouTube feed." }, { status: 502 });
  }
}
