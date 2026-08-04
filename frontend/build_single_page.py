import json
import os
import re
import sqlite3
from pathlib import Path

from pwnedlabs_roadmap_lessons import build_roadmap_lessons
from repo_architecture_lessons import build_repo_lessons


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_WEB = ROOT / "frontend" / "build" / "web"
OUTPUT_DIR = ROOT / "video_pipeline" / "output"
BACKGROUNDS_DIR = ROOT / "video_pipeline" / "backgrounds"
TARGET_HTML = ROOT / "index.html"
TARGET_JSON = ROOT / "videos.json"

CSS_PATH = FRONTEND_WEB / "tiktok.css"
JS_PATH = FRONTEND_WEB / "tiktok.js"
DB_CANDIDATES = [
    ROOT / "cybermentortok.db",
    ROOT / "backend" / "cybermentortok.db",
]
FEED_BACKGROUNDS = ("gameplay_01.webm", "gameplay_01.mp4", "minecraft.mp4", "minecraft.webm")
TITLE_RULES = [
    ("conditional access", "Conditional Access Signals, Controls & Policy Testing"),
    ("what are ports exactly", "Network Ports, Sockets & Port Scanning"),
    ("tls is just", "TLS Handshakes, Certificates & Trust"),
    ("https is just", "HTTPS, TLS & Certificate Warnings"),
    ("ip addresses are just", "IP Addressing, Subnetting & Segmentation"),
    ("osi model", "OSI Model & Security Across Layers"),
    ("layer 2", "Layer 2 Security: MAC, ARP & VLAN Risks"),
    ("monolithic and microkernel", "Operating System Architecture: Monolithic vs Microkernel"),
    ("difference between a process and a thread", "Processes, Threads & Memory Management"),
    ("so the cpu is just", "CPU Architecture & Security Implications"),
    ("ai security", "AI Security: Prompt Injection, Poisoning & Model Theft"),
    ("workload identity", "Workload Identity: Managed Identities & Federation"),
    ("microsoft purview", "Microsoft Purview: Governance, Classification & Lineage"),
    ("dlp actually know", "Data Loss Prevention: Sensitive Data Detection & Controls"),
    ("encrypts everything by default", "Data Encryption End-to-End: Keys, Scope & Tradeoffs"),
    ("key vault and managed hsm", "Azure Key Vault vs Managed HSM"),
    ("ddos basic and standard", "Azure DDoS Protection: Basic vs Standard"),
    ("need a waf", "Web Application Firewall: Coverage, Rules & Limits"),
    ("api security", "API Security: Auth, Abuse & Machine-to-Machine Risk"),
    ("what is stride", "STRIDE Threat Modeling Made Practical"),
    ("infrastructure as code", "Infrastructure as Code Security at Scale"),
    ("devsecops", "DevSecOps: Security in Every Pipeline Stage"),
    ("secure development lifecycle", "Secure Development Lifecycle Essentials"),
    ("blue team, red team, and purple team", "Blue Team, Red Team & Purple Team Operations"),
    ("sentinel called cloud-native", "Microsoft Sentinel: Cloud-Native SIEM & SOAR"),
    ("need xdr", "XDR: Correlating Endpoint, Identity, Email & Cloud Signals"),
    ("communication compliance", "Communication Compliance: Policy Detection & Review"),
    ("insider threat", "Insider Risk Detection & Behavioral Analytics"),
    ("azure policy and blueprints", "Azure Policy, Blueprints & Governance at Scale"),
    ("compliance score", "Compliance Score: What It Measures and What It Does Not"),
    ("difference between b2b and b2c", "Entra External Identities: B2B vs B2C"),
    ("entitlement management", "Entitlement Management: Access Packages & Lifecycle"),
    ("standing permission", "Just-in-Time Access & Standing Privilege Risk"),
    ("permanent access", "Privileged Identity Management: Activation, Approval & Control"),
    ("entra id protection", "Entra ID Protection: User Risk & Sign-In Risk"),
    ("passwordless", "Passwordless Authentication: FIDO2, Passkeys & Windows Hello"),
    ("entra id is just azure ad", "Microsoft Entra: Identity Platform Beyond Azure AD"),
    ("bcdr", "Business Continuity, Disaster Recovery & Resilience Planning"),
    ("defender for cloud", "Microsoft Defender for Cloud: Posture + Workload Protection"),
    ("mcra and mcsb", "Cloud Security Reference Architecture & Benchmark"),
    ("well-architected framework", "Azure Well-Architected Framework for Security"),
    ("azure landing zone", "Azure Landing Zones: Governance from Day One"),
    ("move to the cloud", "Cloud Adoption Framework: Strategy to Operations"),
    ("actual data", "Zero Trust Data Protection & Information Security"),
    ("networking work in zero trust", "Zero Trust Networking & Segmentation"),
    ("what about their device", "Zero Trust Device Compliance & Health Signals"),
    ("identity is the perimeter", "Identity as Security Perimeter in Zero Trust"),
    ("actually deploy it", "Zero Trust Deployment Roadmap"),
    ("what exactly is zero trust", "Zero Trust Principles & Verification Model"),
    ("routing and switching", "Routing, Switching & Network Flow Basics"),
    ("delete a file", "File Deletion, Recovery & Forensic Reality"),
]


def load_db_maps():
    db_path = next((path for path in DB_CANDIDATES if path.is_file()), None)
    if not db_path:
        return {}, {}

    by_prefix = {}
    by_slug = {}
    con = sqlite3.connect(db_path)
    try:
        rows = con.execute(
            """
            SELECT lessons.id, lessons.slug, lessons.title, lessons.hook, lessons.description,
                   lessons.problem, lessons.explanation, lessons.summary, lessons.difficulty,
                   concepts.id, concepts.name, concepts.category
            FROM lessons
            JOIN concepts ON concepts.id = lessons.concept_id
            """
        ).fetchall()
    finally:
        con.close()

    for row in rows:
        lesson_id, slug, title, hook, description, problem, explanation, summary, difficulty, concept_id, concept_name, category = row
        payload = {
            "lesson_id": lesson_id,
            "concept_id": concept_id,
            "title": title,
            "hook": hook,
            "description": description,
            "problem": problem,
            "explanation": explanation,
            "summary": summary,
            "difficulty": difficulty,
            "concept": concept_name,
            "category": category,
        }
        by_slug[slug] = payload
        by_prefix[lesson_id[:8]] = payload
    return by_prefix, by_slug


def load_metadata(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def pick_backgrounds():
    candidates = [name for name in FEED_BACKGROUNDS if (BACKGROUNDS_DIR / name).is_file()]
    preferred = [name for name in ("gameplay_01.webm", "minecraft.mp4") if name in candidates]
    if preferred:
        return [f"video_pipeline/backgrounds/{name}" for name in preferred]
    if not candidates:
        return []
    candidates.sort(key=lambda name: (BACKGROUNDS_DIR / name).stat().st_size, reverse=True)
    return [f"video_pipeline/backgrounds/{name}" for name in candidates]


def pick_background_for_video(output_id, backgrounds):
    if not backgrounds:
        return None
    numeric = int.from_bytes(output_id.encode("utf-8"), "little", signed=False)
    return backgrounds[numeric % len(backgrounds)]


def load_timing_text(path):
    if not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    timeline = payload.get("timeline") or []
    parts = [item.get("text", "").strip() for item in timeline if item.get("text")]
    return " ".join(parts)


def title_case_phrase(text):
    small = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "vs", "with"}
    words = re.split(r"(\s+)", text.strip())
    titled = []
    real_index = 0
    for token in words:
        if not token or token.isspace():
            titled.append(token)
            continue
        lower = token.lower()
        if real_index > 0 and lower in small:
            titled.append(lower)
        else:
            titled.append(lower.capitalize())
        real_index += 1
    return "".join(titled)


def infer_title(output_id, merged, transcript_text):
    title = (merged.get("title") or "").strip()
    if title and title.lower() != output_id.lower() and "output" not in title.lower():
        return title

    corpus = " ".join(
        str(merged.get(key) or "").strip()
        for key in ("title", "hook", "description", "problem", "explanation", "summary", "concept", "category")
    )
    corpus = f"{corpus} {transcript_text}".strip().lower()
    for needle, label in TITLE_RULES:
        if needle in corpus:
            return label

    if transcript_text:
        question = transcript_text.split("?")[0].strip()
        question = re.sub(r"^(so|okay|wait|right|but|and)\s+", "", question, flags=re.IGNORECASE)
        question = re.sub(r"^(what|why|how|when|where|who)\s+(is|are|does|do|did|can|could|should|would)\s+", "", question, flags=re.IGNORECASE)
        question = re.sub(r"^(what|why|how|when|where|who)\s+", "", question, flags=re.IGNORECASE)
        question = re.sub(r"[^A-Za-z0-9\s/&:+-]", "", question)
        question = re.sub(r"\s+", " ", question).strip(" -")
        if question:
            return title_case_phrase(question[:72]).strip()

    concept = (merged.get("concept") or merged.get("category") or "").replace("-", " ").strip()
    if concept:
        return f"{title_case_phrase(concept)} Lesson"
    return f"Security Lesson {output_id.upper()}"


def build_manifest():
    by_prefix, by_slug = load_db_maps()
    background_urls = pick_backgrounds()
    items = []

    if not OUTPUT_DIR.is_dir():
        return items

    for output_id in sorted(os.listdir(OUTPUT_DIR)):
        output_dir = OUTPUT_DIR / output_id
        if not output_dir.is_dir():
            continue

        mask_path = output_dir / "mask.webm"
        audio_path = output_dir / "audio.mp3"
        full_path = output_dir / "full.mp4"
        timing_path = output_dir / "timing.json"
        metadata_path = output_dir / "metadata.json"

        has_mask = mask_path.is_file() and mask_path.stat().st_size > 0
        has_audio = audio_path.is_file() and audio_path.stat().st_size > 0
        has_full = full_path.is_file() and full_path.stat().st_size > 0

        if not has_full and not (has_mask and has_audio):
            continue

        merged = {}
        merged.update(load_metadata(metadata_path))
        if merged.get("slug") and merged["slug"] in by_slug:
            merged = {**by_slug[merged["slug"]], **merged}
        if output_id in by_prefix:
            merged = {**by_prefix[output_id], **merged}
        transcript_text = load_timing_text(timing_path)
        background_url = pick_background_for_video(output_id, background_urls)

        touched = [path.stat().st_mtime for path in (mask_path, audio_path, full_path, timing_path, metadata_path) if path.exists()]
        size_bytes = sum(path.stat().st_size for path in output_dir.iterdir() if path.is_file())

        items.append(
            {
                "id": output_id,
                "title": infer_title(output_id, merged, transcript_text),
                "hook": merged.get("hook"),
                "description": merged.get("description"),
                "problem": merged.get("problem"),
                "explanation": merged.get("explanation"),
                "summary": merged.get("summary"),
                "lesson_id": merged.get("lesson_id"),
                "concept_id": merged.get("concept_id"),
                "concept": merged.get("concept"),
                "category": merged.get("category"),
                "difficulty": merged.get("difficulty"),
                "mask_url": f"video_pipeline/output/{output_id}/mask.webm" if has_mask else None,
                "audio_url": f"video_pipeline/output/{output_id}/audio.mp3" if has_audio else None,
                "full_url": f"video_pipeline/output/{output_id}/full.mp4" if has_full else None,
                "timing_url": f"video_pipeline/output/{output_id}/timing.json" if timing_path.is_file() else None,
                "background_url": background_url,
                "background_options": background_urls,
                "updated_at": max(touched) if touched else 0,
                "size_bytes": size_bytes,
            }
        )

    items.sort(key=lambda item: item["updated_at"], reverse=True)
    items = build_roadmap_lessons(items) + build_repo_lessons(items) + items
    items.sort(key=lambda item: item["updated_at"], reverse=True)
    return items


def transform_js(js_source):
    api_block = 'const API_ROOT = "http://127.0.0.1:8000";\nconst OUTPUTS_URL = `${API_ROOT}/api/v1/videos/pipeline-outputs?limit=200`;\n'
    js_source = js_source.replace(
        api_block,
        'const STATIC_VIDEOS = Array.isArray(window.__STATIC_VIDEO_DATA__) ? window.__STATIC_VIDEO_DATA__ : null;\n'
        'const STATIC_MANIFEST_URL = typeof window.__STATIC_MANIFEST_URL__ === "string" ? window.__STATIC_MANIFEST_URL__ : "";\n'
        'const ASSET_BASE = typeof window.__ASSET_BASE__ === "string" ? window.__ASSET_BASE__ : "http://127.0.0.1:8000";\n'
        'const API_ROOT = ASSET_BASE || "http://127.0.0.1:8000";\n'
        'const OUTPUTS_URL = `${API_ROOT}/api/v1/videos/pipeline-outputs?limit=200`;\n',
    )
    js_source = js_source.replace(
        '  return path.startsWith("http") ? path : `${API_ROOT}${path}`;',
        '  if (path.startsWith("http") || path.startsWith("data:") || path.startsWith("blob:")) return path;\n'
        '  if (!ASSET_BASE) return path.replace(/^\\//, "");\n'
        '  return `${ASSET_BASE}${path}`;',
    )
    js_source = js_source.replace(
        '  const response = await fetch(`${OUTPUTS_URL}&t=${Date.now()}`, { cache: "no-store" });',
        '  if (STATIC_MANIFEST_URL) {\n'
        '    try {\n'
        '      if (location.protocol !== "file:") {\n'
        '        const staticResponse = await fetch(`${STATIC_MANIFEST_URL}?t=${Date.now()}`, { cache: "no-store" });\n'
        '        if (!staticResponse.ok) throw new Error(`HTTP ${staticResponse.status}`);\n'
        '        videos = await staticResponse.json();\n'
        '        visibleVideos = [...videos];\n'
        '        searchResults = [...videos];\n'
        '        renderFeed();\n'
        '        return;\n'
        '      }\n'
        '    } catch (_) {}\n'
        '  }\n'
        '  if (STATIC_VIDEOS) {\n'
        '    videos = [...STATIC_VIDEOS];\n'
        '    visibleVideos = [...videos];\n'
        '    searchResults = [...videos];\n'
        '    renderFeed();\n'
        '    return;\n'
        '  }\n'
        '  const response = await fetch(`${OUTPUTS_URL}&t=${Date.now()}`, { cache: "no-store" });',
    )

    replacements = {
        "â™ª": "&#9835;",
        "â™¥": "&hearts;",
        "â˜°": "&#9776;",
        "â–£": "&#9723;",
        "â†—": "&#8599;",
    }
    for old, new in replacements.items():
        js_source = js_source.replace(old, new)
    return js_source


def build_html(videos, css_source, js_source):
    manifest_json = json.dumps(videos, ensure_ascii=False).replace("</script>", "<\\/script>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#000000">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>CyberMentorTok</title>
  <style>
{css_source}
  </style>
</head>
<body>
  <main class="phone" aria-label="CyberMentorTok feed">
    <video id="backgroundVideo" class="background-video" playsinline muted loop preload="auto"></video>
    <section id="feed" class="feed"></section>
    <button id="libraryBackdrop" class="library-backdrop" type="button" aria-label="Close search"></button>

    <header class="top-bar">
      <button id="libraryButton" class="plain-button counter" type="button">0</button>
      <nav class="tabs" aria-label="Feed mode">
        <button class="tab muted" type="button">Following</button>
        <button class="tab active" type="button">For You</button>
      </nav>
      <button id="searchButton" class="plain-button search" type="button" aria-label="Search videos">&#8981;</button>
    </header>

    <footer class="bottom-nav" aria-label="Main navigation">
      <button class="nav-item active" type="button"><span>&#8962;</span><small>Home</small></button>
      <button id="navSearchButton" class="nav-item" type="button"><span>&#8981;</span><small>Search</small></button>
      <button id="createButton" class="create-button" type="button" aria-label="Open video library">+</button>
      <button class="nav-item" type="button"><span>&#9649;</span><small>Progress</small></button>
      <button class="nav-item" type="button"><span>&#9711;</span><small>Profile</small></button>
    </footer>

    <aside id="library" class="library" aria-label="Lesson library">
      <div class="sheet-handle" aria-hidden="true"></div>
      <div class="library-header">
        <div>
          <strong>Lessons</strong>
          <span id="libraryCount">0 videos</span>
        </div>
        <button id="closeLibraryButton" type="button" aria-label="Close">&times;</button>
      </div>
      <label class="search-box">
        <span>&#8981;</span>
        <input id="searchInput" type="search" placeholder="Search lessons or topics" autocomplete="off">
        <button id="clearSearchButton" type="button" aria-label="Clear search">&times;</button>
      </label>
      <div id="libraryList" class="library-list"></div>
    </aside>
  </main>

  <script>
    window.__ASSET_BASE__ = "";
    window.__STATIC_MANIFEST_URL__ = "videos.json";
    window.__STATIC_VIDEO_DATA__ = {manifest_json};
  </script>
  <script>
{js_source}
  </script>
</body>
</html>
"""


def main():
    css_source = CSS_PATH.read_text(encoding="utf-8")
    js_source = transform_js(JS_PATH.read_text(encoding="utf-8"))
    videos = build_manifest()
    TARGET_JSON.write_text(json.dumps(videos, indent=2, ensure_ascii=False), encoding="utf-8")
    TARGET_HTML.write_text(build_html(videos, css_source, js_source), encoding="utf-8")
    print(f"Built {TARGET_HTML} and {TARGET_JSON} with {len(videos)} videos")


if __name__ == "__main__":
    main()
