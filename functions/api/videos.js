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

    const videos = entries.map(match => {
      const entry = match[1];

      const getTag = (tag) => {
        const m = entry.match(new RegExp(`<${tag}[^>]*>([\\\\s\\\\S]*?)<\\\\/${tag}>`));
        return m ? m[1].replace(/<!\\[CDATA\\[|\\]\\]>/g, "").trim() : "";
      };

      const videoId = getTag("yt:videoId");
      const title = getTag("title");
      const published = getTag("published");
      const updated = getTag("updated");
      const linkMatch = entry.match(/<link[^>]+rel="alternate"[^>]+href="([^"]+)"/);
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

    return Response.json({ videos }, {
      headers: {
        "Cache-Control": "public, max-age=900, s-maxage=900"
      }
    });
  } catch (error) {
    return Response.json({ error: "Unable to read YouTube feed." }, { status: 502 });
  }
}
