const API_ROOT = "http://127.0.0.1:8000";
const OUTPUTS_URL = `${API_ROOT}/api/v1/videos/pipeline-outputs?limit=200`;

const backgroundVideo = document.getElementById("backgroundVideo");
const feed = document.getElementById("feed");
const libraryBackdrop = document.getElementById("libraryBackdrop");
const library = document.getElementById("library");
const libraryList = document.getElementById("libraryList");
const libraryCount = document.getElementById("libraryCount");
const libraryButton = document.getElementById("libraryButton");
const searchButton = document.getElementById("searchButton");
const navSearchButton = document.getElementById("navSearchButton");
const createButton = document.getElementById("createButton");
const closeLibraryButton = document.getElementById("closeLibraryButton");
const searchInput = document.getElementById("searchInput");
const clearSearchButton = document.getElementById("clearSearchButton");

let videos = [];
let visibleVideos = [];
let searchResults = [];
let renderedVideos = [];
let slideElements = [];
let slideByRawIndex = new Map();
let libraryItemsByVideoId = new Map();
let animatedRawIndices = new Set();
let activeIndex = 0;
let activeRenderIndex = 0;
let lastBackgroundResetIndex = -1;
let observer;
let scrollFrame;
let resetPending = false;
const LOOP_COPY_COUNT = 3;
const MEDIA_WINDOW = 1;
const ANIMATION_WINDOW = 2;

async function purgeOldFlutterCache() {
  if (sessionStorage.getItem("cmt-cache-purged-v2") === "1") return;

  if ("serviceWorker" in navigator) {
    const registrations = await navigator.serviceWorker.getRegistrations();
    await Promise.all(registrations.map((registration) => registration.unregister()));
  }

  if ("caches" in window) {
    const names = await caches.keys();
    await Promise.all(names.map((name) => caches.delete(name)));
  }

  sessionStorage.setItem("cmt-cache-purged-v2", "1");
}

function absoluteUrl(path) {
  if (!path) return "";
  return path.startsWith("http") ? path : `${API_ROOT}${path}`;
}

function formatBytes(bytes) {
  if (!bytes) return "";
  if (bytes > 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  return `${Math.round(bytes / 1024)} KB`;
}

function formatCount(count) {
  if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
  if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
  return String(count);
}

function titleFor(video) {
  return video.title && video.title !== video.id ? video.title : `Output ${video.id}`;
}

function conceptFor(video) {
  return video.concept || video.category || "CyberMentorTok";
}

function difficultyFor(video) {
  return video.difficulty ? `Level ${video.difficulty}` : "Pipeline output";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function loopEnabled() {
  return visibleVideos.length > 1;
}

function logicalIndexForRaw(rawIndex) {
  if (!visibleVideos.length) return 0;
  return ((rawIndex % visibleVideos.length) + visibleVideos.length) % visibleVideos.length;
}

function middleRawIndexForLogical(logicalIndex) {
  return loopEnabled() ? logicalIndex + visibleVideos.length : logicalIndex;
}

function buildRenderedVideos() {
  if (!loopEnabled()) {
    return visibleVideos.map((video, index) => ({ video, rawIndex: index, logicalIndex: index }));
  }

  const items = [];
  for (let copy = 0; copy < LOOP_COPY_COUNT; copy += 1) {
    visibleVideos.forEach((video, logicalIndex) => {
      items.push({
        video,
        rawIndex: copy * visibleVideos.length + logicalIndex,
        logicalIndex,
      });
    });
  }
  return items;
}

function targetSlideForRawIndex(rawIndex) {
  return slideByRawIndex.get(rawIndex) || null;
}

function ensureMediaLoadedForSlide(slide) {
  if (!slide || slide.dataset.mediaHydrated === "1") return;

  (slide._players || []).forEach((player) => {
    const source = player.dataset.src;
    if (!source || player.src) return;
    player.src = source;
    if (player.tagName === "VIDEO") player.load();
  });
  slide.dataset.mediaHydrated = "1";
}

function primeMediaAround(rawIndex) {
  for (let offset = -MEDIA_WINDOW; offset <= MEDIA_WINDOW; offset += 1) {
    ensureMediaLoadedForSlide(targetSlideForRawIndex(rawIndex + offset));
  }
}

function renderSlide(video, rawIndex, logicalIndex) {
  const slide = document.createElement("article");
  slide.className = "slide";
  slide.dataset.index = String(logicalIndex);
  slide.dataset.rawIndex = String(rawIndex);
  slide.dataset.videoId = video.id;

  const players = [];
  const makeVideo = (src, muted, loop) => {
    const videoElement = document.createElement("video");
    videoElement.dataset.src = absoluteUrl(src);
    videoElement.playsInline = true;
    videoElement.loop = loop;
    videoElement.muted = muted;
    videoElement.preload = "metadata";
    videoElement.controls = false;
    slide.appendChild(videoElement);
    players.push(videoElement);
    return videoElement;
  };

  if (video.mask_url && video.audio_url) {
    makeVideo(video.mask_url, true, false);
    const audio = document.createElement("audio");
    audio.dataset.src = absoluteUrl(video.audio_url);
    audio.preload = "none";
    slide.appendChild(audio);
    players.push(audio);
  } else if (video.full_url) {
    makeVideo(video.full_url, false, true);
  }

  slide._players = players;

  const top = document.createElement("div");
  top.className = "scrim-top";
  slide.appendChild(top);

  const bottom = document.createElement("div");
  bottom.className = "scrim-bottom";
  slide.appendChild(bottom);

  const caption = document.createElement("section");
  caption.className = "caption";
  caption.innerHTML = `
    <strong>@${escapeHtml(conceptFor(video))}</strong>
    <p>${escapeHtml(captionFor(video))}</p>
    <small>♪ ${escapeHtml(difficultyFor(video))} - ${escapeHtml(formatBytes(video.size_bytes))}</small>
  `;
  slide.appendChild(caption);

  const rail = document.createElement("aside");
  rail.className = "rail";
  rail.innerHTML = `
    <div class="avatar">${(difficultyFor(video).match(/\d/) || ["C"])[0]}</div>
    <button class="action" type="button"><b>♥</b><span>${formatCount(video.size_bytes || 0)}</span></button>
    <button class="action" type="button"><b>☰</b><span>${video.mask_url ? "Mask" : "Full"}</span></button>
    <button class="action" type="button"><b>▣</b><span>Save</span></button>
    <button class="action" type="button"><b>↗</b><span>Share</span></button>
    <div class="disc"></div>
  `;
  slide.appendChild(rail);

  slide.addEventListener("click", () => {
    const primary = players[0];
    if (!primary) return;
    if (primary.paused) {
      players.forEach((player) => player.play().catch(() => {}));
    } else {
      players.forEach((player) => player.pause());
    }
  });

  return slide;
}

function renderLibrary() {
  const list = searchInput.value.trim() ? searchResults : videos;
  libraryCount.textContent = `${list.length}/${videos.length} videos`;
  libraryList.innerHTML = "";
  libraryItemsByVideoId = new Map();
  const fragment = document.createDocumentFragment();
  const activeVideoId = visibleVideos[activeIndex]?.id;

  list.forEach((video, index) => {
    const item = document.createElement("button");
    item.className = `library-item${activeVideoId === video.id ? " active" : ""}`;
    item.type = "button";
    item.dataset.videoId = video.id;
    item.innerHTML = `
      <span class="thumb">${index + 1}</span>
      <span>
        <span class="library-title">${escapeHtml(titleFor(video))}</span>
        <span class="library-meta">${escapeHtml(conceptFor(video))} · ${escapeHtml(difficultyFor(video))}</span>
      </span>
    `;
    item.addEventListener("click", () => {
      closeLibrary();
      const targetIndex = visibleVideos.findIndex((candidate) => candidate.id === video.id);
      const targetRawIndex = middleRawIndexForLogical(targetIndex);
      const target = targetSlideForRawIndex(targetRawIndex);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      if (targetIndex >= 0) setActive(targetIndex, targetRawIndex);
    });
    libraryItemsByVideoId.set(video.id, item);
    fragment.appendChild(item);
  });
  libraryList.appendChild(fragment);
  updateLibraryHeader();
}

function updateLibraryHeader() {
  libraryButton.textContent = visibleVideos.length ? `${activeIndex + 1}/${visibleVideos.length}` : "0/0";
}

function updateLibrarySelection() {
  const activeVideoId = visibleVideos[activeIndex]?.id;
  libraryItemsByVideoId.forEach((item, videoId) => {
    item.classList.toggle("active", videoId === activeVideoId);
  });
}

function setActive(index, rawIndex = middleRawIndexForLogical(index)) {
  activeIndex = index;
  activeRenderIndex = rawIndex;
  primeMediaAround(rawIndex);
  resetBackgroundFor(index);
  backgroundVideo.play().catch(() => {});
  slideElements.forEach((slide) => {
    const players = slide._players || [];
    if (Number(slide.dataset.rawIndex) === rawIndex) {
      players.forEach((player) => player.play().catch(() => {}));
    } else {
      players.forEach((player) => {
        player.pause();
        player.currentTime = 0;
      });
    }
  });
  updateLibraryHeader();
  updateLibrarySelection();
}

function resetBackgroundFor(index) {
  if (index === lastBackgroundResetIndex) return;
  lastBackgroundResetIndex = index;
  resetPending = true;
  seekBackgroundToStart();
}

function seekBackgroundToStart() {
  if (!resetPending) return;
  try {
    backgroundVideo.currentTime = 0;
    resetPending = false;
  } catch (_) {
    backgroundVideo.addEventListener("loadedmetadata", seekBackgroundToStart, { once: true });
  }
}

function rawIndexFromScroll() {
  const slideHeight = Math.max(1, feed.clientHeight);
  return Math.max(0, Math.min(renderedVideos.length - 1, Math.round(feed.scrollTop / slideHeight)));
}

function normalizeLoopPosition(rawIndex = rawIndexFromScroll()) {
  if (!loopEnabled()) return rawIndex;

  const slideHeight = Math.max(1, feed.clientHeight);
  if (!slideHeight) return rawIndex;

  if (rawIndex < visibleVideos.length || rawIndex >= visibleVideos.length * 2) {
    const logicalIndex = logicalIndexForRaw(rawIndex);
    const remainder = feed.scrollTop - rawIndex * slideHeight;
    const targetRawIndex = logicalIndex + visibleVideos.length;
    feed.scrollTop = targetRawIndex * slideHeight + remainder;
    return targetRawIndex;
  }

  return rawIndex;
}

function updateBackgroundScroll() {
  const slideHeight = Math.max(1, feed.clientHeight);
  const progress = (feed.scrollTop % slideHeight) / slideHeight;
  const offset = (progress - 0.5) * -18;
  backgroundVideo.style.transform = `translate3d(0, ${offset}%, 0)`;
  updateSlideAnimations();
}

function updateSlideAnimations() {
  const slideHeight = Math.max(1, feed.clientHeight);
  const nextAnimated = new Set();

  for (let rawIndex = activeRenderIndex - ANIMATION_WINDOW; rawIndex <= activeRenderIndex + ANIMATION_WINDOW; rawIndex += 1) {
    const slide = targetSlideForRawIndex(rawIndex);
    if (!slide) continue;
    nextAnimated.add(rawIndex);
    const distance = (slide.offsetTop - feed.scrollTop) / slideHeight;
    const absoluteDistance = Math.min(1, Math.abs(distance));
    slide.style.opacity = String(1 - absoluteDistance * 0.16);

    const mask = slide.querySelector("video");
    if (mask) {
      mask.style.transform = `translate3d(0, ${distance * 18}px, 0) scale(${1 + absoluteDistance * 0.035})`;
      mask.style.opacity = String(1 - absoluteDistance * 0.2);
    }

    slide.querySelectorAll(".caption, .rail").forEach((element) => {
      element.style.transform = `translate3d(0, ${distance * -26}px, 0) scale(${1 - absoluteDistance * 0.03})`;
      element.style.opacity = String(1 - absoluteDistance * 0.45);
    });
  }

  animatedRawIndices.forEach((rawIndex) => {
    if (nextAnimated.has(rawIndex)) return;
    const slide = targetSlideForRawIndex(rawIndex);
    if (!slide) return;
    slide.style.opacity = "";

    const mask = slide.querySelector("video");
    if (mask) {
      mask.style.transform = "";
      mask.style.opacity = "";
    }

    slide.querySelectorAll(".caption, .rail").forEach((element) => {
      element.style.transform = "";
      element.style.opacity = "";
    });
  });

  animatedRawIndices = nextAnimated;
}

function observeSlides() {
  observer?.disconnect();
  observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) {
      const rawIndex = normalizeLoopPosition(Number(visible.target.dataset.rawIndex));
      setActive(logicalIndexForRaw(rawIndex), rawIndex);
    }
  }, { root: feed, threshold: [0.65, 0.85] });

  slideElements.forEach((slide) => observer.observe(slide));
}

function renderFeed() {
  feed.innerHTML = "";

  if (!visibleVideos.length) {
    feed.innerHTML = `
      <section class="empty">
        <div>
          <h1>No videos found</h1>
          <p>Clear search or render videos into video_pipeline/output.</p>
        </div>
      </section>
    `;
    renderLibrary();
    return;
  }

  renderedVideos = buildRenderedVideos();
  slideElements = [];
  slideByRawIndex = new Map();
  animatedRawIndices = new Set();
  const fragment = document.createDocumentFragment();
  renderedVideos.forEach(({ video, rawIndex, logicalIndex }) => {
    const slide = renderSlide(video, rawIndex, logicalIndex);
    slideElements.push(slide);
    slideByRawIndex.set(rawIndex, slide);
    fragment.appendChild(slide);
  });
  feed.appendChild(fragment);
  setBackgroundVideo();
  renderLibrary();
  lastBackgroundResetIndex = -1;
  requestAnimationFrame(() => {
    const initialRawIndex = middleRawIndexForLogical(0);
    feed.scrollTop = initialRawIndex * Math.max(1, feed.clientHeight);
    primeMediaAround(initialRawIndex);
    observeSlides();
    setActive(0, initialRawIndex);
    updateBackgroundScroll();
  });
}

function setBackgroundVideo() {
  const source = visibleVideos.find((video) => video.background_url)?.background_url;
  if (!source) return;
  const url = absoluteUrl(source);
  if (backgroundVideo.src !== url) {
    backgroundVideo.src = url;
    backgroundVideo.preload = "auto";
    backgroundVideo.load();
  }
}

function captionFor(video) {
  return [
    video.hook,
    video.summary,
    video.description,
    video.explanation,
    titleFor(video),
  ].filter(Boolean)[0];
}

function searchableText(video) {
  return [
    video.id,
    video.title,
    video.hook,
    video.concept,
    video.category,
    video.concept_id,
    difficultyFor(video),
  ].filter(Boolean).join(" ").toLowerCase();
}

function applySearch() {
  const query = searchInput.value.trim().toLowerCase();
  searchResults = query
    ? videos.filter((video) => searchableText(video).includes(query))
    : [...videos];
  renderLibrary();
}

async function loadVideos() {
  feed.innerHTML = `<section class="empty"><div><h1>Loading videos</h1><p>Reading video_pipeline/output.</p></div></section>`;
  const response = await fetch(`${OUTPUTS_URL}&t=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  videos = await response.json();
  visibleVideos = [...videos];
  searchResults = [...videos];
  renderFeed();
}

function openLibrary() {
  library.classList.add("open");
  libraryBackdrop.classList.add("open");
}

function closeLibrary() {
  library.classList.remove("open");
  libraryBackdrop.classList.remove("open");
}

function openSearch() {
  openLibrary();
  requestAnimationFrame(() => searchInput.focus());
}

libraryButton.addEventListener("click", openLibrary);
createButton.addEventListener("click", openLibrary);
libraryBackdrop.addEventListener("click", closeLibrary);
closeLibraryButton.addEventListener("click", closeLibrary);
searchButton.addEventListener("click", openSearch);
navSearchButton.addEventListener("click", openSearch);
searchInput.addEventListener("input", applySearch);
searchInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && searchResults.length) {
    const targetIndex = visibleVideos.findIndex((video) => video.id === searchResults[0].id);
    const targetRawIndex = middleRawIndexForLogical(targetIndex);
    const target = targetSlideForRawIndex(targetRawIndex);
    closeLibrary();
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    if (targetIndex >= 0) setActive(targetIndex, targetRawIndex);
  }
});
clearSearchButton.addEventListener("click", () => {
  searchInput.value = "";
  applySearch();
  searchInput.focus();
});
feed.addEventListener("scroll", () => {
  if (scrollFrame) cancelAnimationFrame(scrollFrame);
  scrollFrame = requestAnimationFrame(() => {
    const rawIndex = normalizeLoopPosition(rawIndexFromScroll());
    updateBackgroundScroll();
    const logicalIndex = logicalIndexForRaw(rawIndex);
    if (logicalIndex !== activeIndex || rawIndex !== activeRenderIndex) setActive(logicalIndex, rawIndex);
  });
}, { passive: true });

backgroundVideo.addEventListener("seeked", () => {
  if (backgroundVideo.currentTime < 0.15) return;
  if (activeIndex === lastBackgroundResetIndex) backgroundVideo.currentTime = 0;
});

function showError(error) {
  feed.innerHTML = `
    <section class="empty">
      <div>
        <h1>Could not load videos</h1>
        <p>${error.message}</p>
      </div>
    </section>
  `;
}

purgeOldFlutterCache()
  .catch(() => {})
  .finally(() => loadVideos().catch(showError));
