document.addEventListener("DOMContentLoaded", () => {
  const cfg = window.SITE_CONFIG || {};
  const youtubeUrl = cfg.youtubeUrl || "https://www.youtube.com/channel/UC-fU_-yuEwnVY7F-mVAfO6w";

  [
    "nav-youtube",
    "hero-youtube",
    "all-videos",
    "shorts-youtube",
    "subscribe-youtube",
    "footer-youtube"
  ].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.href = youtubeUrl;
      el.target = "_blank";
      el.rel = "noopener";
    }
  });

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    nav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  loadLatestVideos();
});

const FALLBACK_VIDEOS = {
  rc: {
    title: "Best Budget Backyard Basher? | UDIRC UD1611 RC Truck",
    id: "NtOCB3a6SRo",
    url: "https://www.youtube.com/watch?v=NtOCB3a6SRo"
  },
  boats: {
    title: "RC Boat Reviews",
    url: "https://www.youtube.com/channel/UC-fU_-yuEwnVY7F-mVAfO6w"
  },
  drones: {
    title: "Drone Reviews",
    url: "https://www.youtube.com/channel/UC-fU_-yuEwnVY7F-mVAfO6w"
  },
  tech: {
    title: "Tech Reviews",
    url: "https://www.youtube.com/channel/UC-fU_-yuEwnVY7F-mVAfO6w"
  }
};

function matchesCategory(video, category) {
  const t = video.title.toLowerCase();

  const rules = {
    rc: [
      /\brc\b/, /remote control/, /truck/, /buggy/, /crawler/, /basher/,
      /monster truck/, /short course/, /off.?road/, /car review/, /r\/c/
    ],
    boats: [
      /\brc boat\b/, /\bboat\b/, /speed boat/, /jet boat/, /watercraft/
    ],
    drones: [
      /\bdrone\b/, /\bquadcopter\b/, /\bfimi\b/, /\bdji\b/, /\bmavic\b/,
      /\bair\b/
    ],
    tech: [
      /\btech\b/, /\bgadget\b/, /\bcamera\b/, /\bprinter\b/, /\bphone\b/,
      /\bcomputer\b/, /\baccessory\b/, /\bdevice\b/
    ]
  };

  return rules[category].some(rx => rx.test(t));
}

function chooseVideo(videos, category, used) {
  const candidates = videos.filter(v => matchesCategory(v, category) && !used.has(v.id));
  return candidates[0] || null;
}

async function loadLatestVideos() {
  const cards = [...document.querySelectorAll(".live-video-card")];
  if (!cards.length) return;

  try {
    const response = await fetch("/api/videos", { headers: { "Accept": "application/json" } });
    if (!response.ok) throw new Error("Feed unavailable");

    const data = await response.json();
    const videos = Array.isArray(data.videos) ? data.videos : [];
    const used = new Set();

    cards.forEach(card => {
      const category = card.dataset.category;
      const video = chooseVideo(videos, category, used);
      if (video) {
        used.add(video.id);
        renderVideoCard(card, video);
      } else {
        renderFallbackCard(card, FALLBACK_VIDEOS[category]);
      }
    });
  } catch (error) {
    cards.forEach(card => {
      const category = card.dataset.category;
      renderFallbackCard(card, FALLBACK_VIDEOS[category]);
    });
  }
}

function renderVideoCard(card, video) {
  const link = card.querySelector(".dynamic-thumb");
  const img = card.querySelector("img");
  const title = card.querySelector(".video-title");
  const date = card.querySelector(".video-date");
  const watch = card.querySelector(".video-watch");

  const url = video.url || `https://www.youtube.com/watch?v=${video.id}`;
  link.href = url;
  watch.href = url;
  title.textContent = video.title;

  if (video.published) {
    const d = new Date(video.published);
    date.textContent = isNaN(d) ? "Latest upload" : `Published ${d.toLocaleDateString(undefined, {year:"numeric", month:"short", day:"numeric"})}`;
  } else {
    date.textContent = "Latest upload";
  }

  if (video.thumbnail) {
    img.src = video.thumbnail;
    img.alt = video.title;
    img.style.display = "block";
  }
}

function renderFallbackCard(card, video) {
  if (!video) return;
  const link = card.querySelector(".dynamic-thumb");
  const img = card.querySelector("img");
  const title = card.querySelector(".video-title");
  const date = card.querySelector(".video-date");
  const watch = card.querySelector(".video-watch");

  link.href = video.url;
  watch.href = video.url;
  title.textContent = video.title;
  date.textContent = video.id ? "Open Circuit RC & Tech" : "Browse the channel";

  if (video.id) {
    img.src = `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`;
    img.alt = video.title;
    img.style.display = "block";
  }
}
