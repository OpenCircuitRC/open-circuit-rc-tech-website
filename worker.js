const CHANNEL_ID = "UC-fU_-yuEwnVY7F-mVAfO6w";

const YOUTUBE_BROWSE = "https://www.youtube.com/youtubei/v1/browse";

const VIDEO_PARAMS = "EgZ2aWRlb3MYASAAMAE=";

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

function findVideos(value, videos) {
  if (!value || typeof value !== "object") return;

  if (value.gridVideoRenderer) {
    const video = value.gridVideoRenderer;

    if (video.videoId && !videos.some(v => v.id === video.videoId)) {
      const title = getText(video.title);

      if (title) {
        videos.push({
          id: video.videoId,
          title,
          published: getText(video.publishedTimeText),
          updated: getText(video.publishedTimeText),
          url: `https://www.youtube.com/watch?v=${video.videoId}`,
          thumbnail:
            video.thumbnail?.thumbnails?.at(-1)?.url ||
            `https://i.ytimg.com/vi/${video.videoId}/hqdefault.jpg`
        });
      }
    }
  }

  if (value.videoRenderer) {
    const video = value.videoRenderer;

    if (video.videoId && !videos.some(v => v.id === video.videoId)) {
      const title = getText(video.title);

      if (title) {
        videos.push({
          id: video.videoId,
          title,
          published: getText(video.publishedTimeText),
          updated: getText(video.publishedTimeText),
          url: `https://www.youtube.com/watch?v=${video.videoId}`,
          thumbnail:
            video.thumbnail?.thumbnails?.at(-1)?.url ||
            `https://i.ytimg.com/vi/${video.videoId}/hqdefault.jpg`
        });
      }
    }
  }

  if (value.richItemRenderer?.content?.videoRenderer) {
    findVideos(
      value.richItemRenderer.content.videoRenderer,
      videos
    );
  }

  for (const key of Object.keys(value)) {
    findVideos(value[key], videos);
  }
}

async function getVideos() {
  const response = await fetch(YOUTUBE_BROWSE, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
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

      browseId: CHANNEL_ID,

      params: VIDEO_PARAMS
    })
  });

  if (!response.ok) {
    throw new Error(
      `YouTube browse returned HTTP ${response.status}`
    );
  }

  const data = await response.json();

  const videos = [];

  findVideos(data, videos);

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