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

    const readTag = (entry, tag) => {
      const match = entry.match(
        new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`)
      );
      return match ? match[1].trim() : "";
    };

    const videos = entries
      .map(([_, entry]) => {
        const videoId = readTag(entry, "yt:videoId");
        const title = readTag(entry, "title");
        const published = readTag(entry, "published");
        const updated = readTag(entry, "updated");

        const linkMatch = entry.match(
          /<link[^>]+rel="alternate"[^>]+href="([^"]+)"/
        );

        return {
          id: videoId,
          title,
          published,
          updated,
          url:
            linkMatch?.[1] ||
            `https://www.youtube.com/watch?v=${videoId}`,
          thumbnail: videoId
            ? `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`
            : ""
        };
      })
      .filter(video => video.id && video.title)
      .sort((a, b) => {
        const dateA = new Date(
          a.published || a.updated || 0
        ).getTime();

        const dateB = new Date(
          b.published || b.updated || 0
        ).getTime();

        return dateB - dateA;
      });

    return Response.json(
      { videos },
      {
        headers: {
          "Cache-Control": "no-store"
        }
      }
    );
  } catch (error) {
    return Response.json(
      { error: "Unable to read YouTube feed." },
      { status: 502 }
    );
  }
}