document.addEventListener("DOMContentLoaded", () => {
  const cfg = window.SITE_CONFIG || {};
  const youtubeUrl = cfg.youtubeUrl || "https://www.youtube.com/channel/UC-fU_-yuEwnVY7F-mVAfO6w";

  ["nav-youtube", "hero-youtube", "subscribe-youtube", "footer-youtube"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.href = youtubeUrl;
      el.target = "_blank";
      el.rel = "noopener";
    }
  });

  const shortsEl = document.getElementById("shorts-youtube");
  if (shortsEl) {
    shortsEl.href = "https://www.youtube.com/@OpenCircuitRC/shorts";
    shortsEl.target = "_blank";
    shortsEl.rel = "noopener";
  }

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
});
