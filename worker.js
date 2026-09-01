const CHANNEL_ID = "UC-fU_-yuEwnVY7F-mVAfO6w";

const YOUTUBE_API = "https://www.youtube.com/youtubei/v1/browse";

async function getVideos() {
  const response = await fetch(YOUTUBE_API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Origin": "https://www.youtube.com",
      "User-Agent": "Mozilla/5.0"
    },
    body: JSON.stringify({
      context: {
        client: {
          clientName: "WEB",
          clientVersion: "2.20260831.01.00",
          hl: "en",
          gl: "US"
        }
      },
      browseId: CHANNEL_ID
    })
  });

  if (!response.ok) {
    throw new Error(`YouTube browse returned HTTP ${response.status}`);
  }

  const data = await response.json();
  const videos = [];

  function walk(value) {
    if (!value || typeof value !== "object") return;

    if (value.videoRenderer) {
      addVideo(value.videoRenderer);
    }

    if (value.gridVideoRenderer) {
      addVideo(value.gridVideoRenderer);
    }

    if (value.richItemRenderer?.content?.videoRenderer) {
      addVideo(value.richItemRenderer.content.videoRenderer);
    }

    for (const key of Object.keys(value)) {
      walk(value[key]);
    }
  }

  function getText(value) {
    if (!value) return "";

    if (typeof value.simpleText === "string") {
      return value.simpleText;
    }

    if (Array.isArray(value.runs)) {
      return value.runs.map(run => run.text || "").join("");
    }

    return "";
  }

  function addVideo(video) {
    if (!video?.videoId) return;

    if (videos.some(v => v.id === video.videoId)) {
      return;
    }

    const title = getText(video.title);

    if (!title) return;

    const publishedText =
      getText(video.publishedTimeText) ||
      getText(video.publishedTime);

    videos.push({
      id: video.videoId,
      title,
      published: publishedText,
      updated: publishedText,
      url: `https://www.youtube.com/watch?v=${video.videoId}`,
      thumbnail:
        video.thumbnail?.thumbnails?.at(-1)?.url ||
        `https://i.ytimg.com/vi/${video.videoId}/hqdefault.jpg`
    });
  }

  walk(data);

  return videos.slice(0, 30);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/videos") {
      try {
        const videos = await getVideos();

        return Response.json(
          { videos },
          {
            headers: {
              "Cache-Control": "public, max-age=300"
            }
          }
        );
      } catch (error) {
        return Response.json(
          {
            error: "Unable to read YouTube videos.",
            details: String(error?.message || error)
          },
          { status: 502 }
        );
      }
    }

    return env.ASSETS.fetch(request);
  }
};