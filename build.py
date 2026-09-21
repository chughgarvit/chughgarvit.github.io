#!/usr/bin/env python3
"""Build the site from data/*.json. Run: python3 build.py

Every page, count and "show all N" link is derived from the data files, so
adding a paper to data/publications.json or an item to data/news.json is the
whole edit. Keep this file and data/ in the repo.
"""
import json, datetime, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
SITE = "https://www.garvitchugh.com"
TODAY = datetime.date.today().isoformat()
import hashlib
CSS_HASH = hashlib.sha1((ROOT / "static/css/site.css").read_bytes()).hexdigest()[:8]

def load(name):
    return json.loads((DATA / f"{name}.json").read_text())

P = load("profile"); PUBS = load("publications"); NEWS = load("news"); RESEARCH = load("research")
EXPERIENCE = load("experience"); EDUCATION = load("education"); TEACHING = load("teaching"); OUTREACH = load("outreach")
MENTORSHIP = load("mentorship"); SKILLS_FULL = load("skills")
SERVICE = load("service"); SYSTEMS = load("systems"); HONOURS = load("honours"); LABS = load("labs")
try: OPENALEX = load("openalex")
except FileNotFoundError: OPENALEX = {"author": {}, "works": {}}
def _norm(t): return re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>", "", t or "").lower())[:40]
for p in PUBS:  # merge the OpenAlex cache; hand-set fields in publications.json win
    oa = OPENALEX["works"].get(_norm(p["title"]), {}); links = p.setdefault("links", {})
    if oa.get("doi") and not p.get("url"): p["url"] = oa["doi"]
    if p.get("url") and not links.get("paper"): links["paper"] = p["url"]
    if oa.get("oa_url") and not links.get("pdf"): links["pdf"] = oa["oa_url"]
    if oa.get("abstract") and not p.get("abstract"): p["abstract"] = oa["abstract"]
    p["cited"] = oa.get("cited_by_count", 0); p["openalex_id"] = oa.get("openalex_id")
CITES_TOTAL = OPENALEX["author"].get("cited_by_count") or sum(p["cited"] for p in PUBS)
H_INDEX = OPENALEX["author"].get("h_index")

# ── derived counts ────────────────────────────────────────────────
N_PEER = sum(p["track"] in ("main", "workshop", "journal") for p in PUBS)
N_PATENT = sum(p["track"] == "patent" for p in PUBS)
N_REVIEW = sum(p["track"] == "review" for p in PUBS)
N_PUBS = len(PUBS)
PUB_SUMMARY = f"{N_PUBS} publications: {N_PEER} peer-reviewed, {N_PATENT} filed patent, {N_REVIEW} under review."

# ── icons (stroke) and brand marks (fill) ─────────────────────────
def ico(paths):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
I = {
 "home": ico('<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h5v-6h4v6h5V9.5"/>'),
 "pubs": ico('<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M9 7h7M9 11h7"/>'),
 "work": ico('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><path d="M2 13h20"/>'),
 "award": ico('<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>'),
 "news": ico('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'),
 "arrow": ico('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
 "mail": ico('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
 "file": ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h8"/>'),
 "scholar": ico('<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>'),
 "star": ico('<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>'),
 "pin": ico('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
 "ticket": ico('<path d="M2 9a3 3 0 0 1 0 6v3a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-3a3 3 0 0 1 0-6V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/><path d="M13 5v2M13 17v2M13 11v2"/>'),
 "flag": ico('<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>'),
 "users": ico('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
 "talk": ico('<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>'),
 "ear": ico('<path d="M6 8.5a6.5 6.5 0 0 1 13 0c0 6-6 6-6 10a3.5 3.5 0 1 1-7 0"/><path d="M15 8.5a2.5 2.5 0 0 0-5 0v1a2 2 0 1 1 0 4"/>'),
 "watch": ico('<circle cx="12" cy="12" r="6"/><path d="M12 9v3l1.5 1.5"/><path d="M16.5 4.2 16 2H8l-.5 2.2M16.5 19.8 16 22H8l-.5-2.2"/>'),
 "wrench": ico('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'),
 "code": ico('<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>'),
 "video": ico('<path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2"/>'),
 "quote": ico('<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>'),
 "external": ico('<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'),
 "sun": ico('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>'),
 "moon": ico('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'),
 "up": ico('<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>'),
 "trophy": ico('<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>'),
 "gift": ico('<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>'),
}
HON_KIND = {"award": ("award", "Award"), "competition": ("trophy", "Competition"), "fellowship": ("star", "Fellowship"), "travel": ("ticket", "Travel grant"),
            "scholarship": ("scholar", "Scholarship"), "recognition": ("gift", "Recognition"), "exam": ("file", "Exam"), "talk": ("talk", "Invited talk")}
NEWS_KIND = {"paper": ("file", "Paper"), "award": ("award", "Award"), "grant": ("ticket", "Grant"), "milestone": ("flag", "Milestone"),
             "service": ("users", "Service"), "talk": ("talk", "Talk"), "update": ("news", "Update")}
SYS_ICON = {"earable": "ear", "wearable": "watch", "tool": "wrench"}
LINK_ICON = {"paper": ("external", "DOI"), "pdf": ("file", "PDF"), "code": ("code", "Code"), "video": ("video", "Video")}
B = {
 "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="brand-github"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="brand-linkedin"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
 "scholar": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="brand-scholar"><path d="M5.242 13.769 0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg>',
 "orcid": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="brand-orcid"><path d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zM7.4 5.6a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8zm-.7 3h1.4v9H6.7zm3.5 0h3.9c3.7 0 5.3 2.6 5.3 4.5 0 2.3-1.8 4.5-5.3 4.5h-3.9zm1.4 1.3v6.5h2.4c3.2 0 3.9-2.4 3.9-3.3 0-1.8-1.1-3.2-4-3.2z"/></svg>',
 "dblp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="brand-dblp"><path d="M3 6l9-4 9 4v2l-9 4-9-4V6zm0 5l9 4 9-4v2l-9 4-9-4v-2zm0 5l9 4 9-4v2l-9 4-9-4v-2z"/></svg>',
}
BADGE_TITLES = {"core": "Ranked A* (top tier) in the CORE conference ranking", "main": "Full paper in the main research track",
                "wip": "Short paper: workshop, work-in-progress, poster, demo or artefact track", "journal": "Journal article",
                "award": "Paper award", "patent": "Patent application", "review": "Submitted, not yet accepted"}

NAV = [("index.html", "Home", "home"), ("publications.html", "Publications", "pubs"), ("education.html", "Experience", "work"),
       ("awards.html", "Honours", "award"), ("news.html", "News", "news")]

def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")

def nav(active):
    return "".join(f'<a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == active else ""}>{I[k]}<span>{l}</span></a>' for h, l, k in NAV)

def shell(title, desc, path, active, body, extra_head="", ogtype="website"):
    url = f"{SITE}/{path}" if path else f"{SITE}/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#2f6feb" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0e1520" media="(prefers-color-scheme: dark)" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{SITE}/static/media/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="{ogtype}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{SITE}/static/media/og-image.jpg" />
  <title>{title}</title>
  <link rel="canonical" href="{url}" />
  <link rel="alternate" type="application/rss+xml" title="Garvit Chugh: news" href="{SITE}/news.xml" />
  <script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;document.documentElement.classList.add('js');}}catch(e){{}}</script>
  <link rel="icon" href="favicon.svg?v={CSS_HASH}" type="image/svg+xml" />
  <link rel="icon" href="static/media/favicon-32.png?v={CSS_HASH}" sizes="32x32" type="image/png" />
  <link rel="apple-touch-icon" href="static/media/apple-touch-icon.png?v={CSS_HASH}" />
  <link rel="preload" href="static/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin />
{'  <link rel="preload" href="static/media/profile.jpg" as="image" fetchpriority="high" />' + chr(10) if active == "index.html" else ""}  <script type="speculationrules">{{"prerender":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":"/*.pdf"}}}},{{"not":{{"href_matches":"/*.xml"}}}}]}},"eagerness":"moderate"}}],"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":"/*.pdf"}}}}]}},"eagerness":"moderate"}}]}}</script>
  <link rel="stylesheet" href="static/css/site.css?v={CSS_HASH}" />
{extra_head}</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="lg-refract" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feImage href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3ClinearGradient id='g' x1='0' x2='1'%3E%3Cstop offset='0' stop-color='rgb(0,128,128)'/%3E%3Cstop offset='.18' stop-color='rgb(128,128,128)'/%3E%3Cstop offset='.82' stop-color='rgb(128,128,128)'/%3E%3Cstop offset='1' stop-color='rgb(255,128,128)'/%3E%3C/linearGradient%3E%3Crect width='100' height='100' fill='url(%23g)'/%3E%3C/svg%3E" preserveAspectRatio="none" result="mx" />
    <feImage href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3ClinearGradient id='g' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='rgb(128,0,128)'/%3E%3Cstop offset='.3' stop-color='rgb(128,128,128)'/%3E%3Cstop offset='.7' stop-color='rgb(128,128,128)'/%3E%3Cstop offset='1' stop-color='rgb(128,255,128)'/%3E%3C/linearGradient%3E%3Crect width='100' height='100' fill='url(%23g)'/%3E%3C/svg%3E" preserveAspectRatio="none" result="my" />
    <feComposite in="mx" in2="my" operator="arithmetic" k2="1" k3="1" k4="-0.5" result="map" />
    <feDisplacementMap in="SourceGraphic" in2="map" scale="-22" xChannelSelector="R" yChannelSelector="G" />
  </filter>
</svg>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar__inner glass">
    <nav class="nav" aria-label="Primary">{nav(active)}</nav>
  </div>
  <button type="button" class="theme-toggle glass" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark mode"><span class="ico-sun">{I["sun"]}</span><span class="ico-moon">{I["moon"]}</span></button>
</header>
<main id="main" class="page">
{body}
</main>
<footer class="footer">
  <nav class="footer__links" aria-label="Footer">{"".join(f'<a href="{h}">{l}</a>' for h, l, _ in NAV)}<a href="education.html#systems">Systems</a><a href="static/media/Garvit_Resume.pdf" target="_blank" rel="noopener">CV ({P.get("cv_updated", "PDF")})</a><a href="news.xml">RSS</a></nav>
  <p class="footer__meta">Garvit Chugh &copy; {TODAY[:4]} &middot; Updated {TODAY} &middot; <a href="#main" class="footer__top">Back to top {I["up"]}</a></p>
</footer>
<script>
  // Theme toggle (remembers the choice; otherwise follows the system).
  document.getElementById('themeToggle').addEventListener('click', () => {{ const dark = matchMedia('(prefers-color-scheme: dark)').matches; const cur = document.documentElement.dataset.theme || (dark ? 'dark' : 'light'); const next = cur === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = next; try {{ localStorage.setItem('theme', next); }} catch (e) {{}} }});
  // Copy BibTeX.
  document.querySelectorAll('.iconbtn--copy').forEach(btn => btn.addEventListener('click', async () => {{ try {{ await navigator.clipboard.writeText(btn.dataset.bib); btn.classList.add('copied'); btn.querySelector('span').textContent = 'Copied'; setTimeout(() => {{ btn.classList.remove('copied'); btn.querySelector('span').textContent = 'BibTeX'; }}, 1600); }} catch (e) {{ prompt('BibTeX', btn.dataset.bib); }} }}));
  // Reveal cards as they scroll in (skipped under reduced motion).
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {{
    const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
    document.querySelectorAll('.card').forEach(c => {{ if (c.getBoundingClientRect().top > innerHeight) {{ c.classList.add('reveal'); io.observe(c); }} }});
  }}
  // Light follows the pointer across glass surfaces.
  document.querySelectorAll('.glass, .btn--outline, .btn--ghost').forEach(el => el.addEventListener('pointermove', e => {{ const r = el.getBoundingClientRect(); el.style.setProperty('--mx', (e.clientX - r.left) + 'px'); el.style.setProperty('--my', (e.clientY - r.top) + 'px'); }}, {{ passive: true }}));
  // Tab bar minimises while scrolling down and returns on scroll up (phones only).
  (() => {{ let last = scrollY, ticking = false;
    addEventListener('scroll', () => {{ if (ticking) return; ticking = true; requestAnimationFrame(() => {{
      const y = scrollY; document.body.classList.toggle('nav-min', innerWidth <= 600 && y > last + 4 && y > 120); if (y < last - 4 || y < 120) document.body.classList.remove('nav-min'); last = y; ticking = false; }}); }}, {{ passive: true }});
  }})();
</script>
</body>
</html>
"""

def show_all(href, label):
    return f'<a class="card__footer" href="{href}">{label} {I["arrow"]}</a>'

def title_h(level, text, cls="card__title", extra=""):
    return f'<h{level} class="{cls}"{extra}>{text}</h{level}>'

# ── components ───────────────────────────────────────────────────
def logo_tile(item):
    if item.get("logo"):
        return f'<img src="static/media/{item["logo"]}" alt="" width="64" height="64" loading="lazy" decoding="async" />'
    return item.get("mono", "")

def entry(e, level=3):
    meta = " &middot; ".join(x for x in [e.get("dates", ""), e.get("place", "")] if x)
    org = e["org"] + (f' &middot; {e["kind"]}' if e.get("kind") else "")
    desc = f'<div class="entry__desc">{e["desc"]}</div>' if e.get("desc") else ""
    return f"""      <li class="entry">
        <div class="entry__logo">{logo_tile(e)}</div>
        <div class="entry__body">
          <h{level} class="entry__title">{e["title"]}</h{level}>
          <div class="entry__org">{org}</div>
          <div class="entry__meta">{meta}</div>{desc}
        </div>
      </li>
"""

def entries(items, level=3):
    return '<ul class="entries entries--timeline">\n' + "".join(entry(e, level) for e in items) + "</ul>"

def bibtex(p):
    plain = re.sub(r"<[^>]+>", "", p["authors"]).replace("&amp;", "&")
    plain = re.sub(r"\s*\(\*Equal Contributions?\)", "", plain).replace("*", "")
    authors = " and ".join(a.strip() for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&\s", plain) if a.strip())
    year = p["year"] if p["year"].isdigit() else ("2025" if p["year"] == "patent" else "2026")
    first = re.match(r"([A-Za-z\-]+)", plain).group(1).lower() if re.match(r"([A-Za-z\-]+)", plain) else "chugh"
    word = re.sub(r"[^a-z]", "", p["title"].split()[0].lower()) or "paper"
    key = f"{first}{year}{word}"
    title = re.sub(r"<[^>]+>", "", p["title"]).replace("&amp;", "&")
    venue = p["venue"].replace("&amp;", "&")
    if p["track"] == "journal": body = f"@article{{{key},\n  title={{{title}}},\n  author={{{authors}}},\n  journal={{{venue}}},\n  year={{{year}}}"
    elif p["track"] == "patent": body = f"@misc{{{key},\n  title={{{title}}},\n  author={{{authors}}},\n  howpublished={{{venue}}},\n  year={{{year}}}"
    elif p["track"] == "review": body = f"@unpublished{{{key},\n  title={{{title}}},\n  author={{{authors}}},\n  note={{Under review}},\n  year={{{year}}}"
    else: body = f"@inproceedings{{{key},\n  title={{{title}}},\n  author={{{authors}}},\n  booktitle={{{venue}}},\n  year={{{year}}}"
    if p.get("url"): body += f",\n  url={{{p['url']}}}"
    return body + "\n}"

def pub_item(p, heading_level=3):
    badges = "".join(f' <span class="pub-badge pub-badge--{b["kind"]}" title="{esc_attr(BADGE_TITLES.get(b["kind"], b["text"]))}">{b["text"]}</span>' for b in p["badges"])
    title = f'<a href="papers/{p["slug"]}.html">{p["title"]}</a>'
    tags = "".join(f'<span class="pub-tag">{t}</span>' for t in p["tags"])
    cited = f'<span class="pub-cited" title="Citations counted by OpenAlex">{I["quote"]}Cited {p["cited"]}</span>' if p.get("cited") else ""
    links = "".join(f'<a class="iconbtn" href="{esc_attr(u)}" target="_blank" rel="noopener" title="{LINK_ICON[k][1]}" aria-label="{LINK_ICON[k][1]}">{I[LINK_ICON[k][0]]}<span>{LINK_ICON[k][1]}</span></a>' for k, u in (p.get("links") or {}).items() if u and k in LINK_ICON) + cited
    links += f'<button type="button" class="iconbtn iconbtn--copy" data-bib="{esc_attr(bibtex(p))}" title="Copy BibTeX" aria-label="Copy BibTeX">{I["quote"]}<span>BibTeX</span></button>'
    return f"""      <li class="pub-item" data-year="{p["year"]}" data-track="{p["track"]}" data-topic="{' '.join(p["topics"])}">
        <h{heading_level} class="pub-title">{title}</h{heading_level}>
        <div class="pub-authors">{p["authors"]}</div>
        <div class="pub-meta"><span class="pub-venue">{p["venue"]}</span>{badges}{tags}</div>
        <div class="pub-links">{links}</div>
      </li>
"""

def news_item(n, with_year=True):
    icon, label = NEWS_KIND.get(n.get("kind", "update"), NEWS_KIND["update"])
    meta = label + (f' &middot; {n["year"]}' if with_year else "")
    cls = f'news-item news-item--{n.get("kind", "update")}' + (" news-item--featured" if n.get("featured") else "")
    return f'      <li class="{cls}"><span class="news-icon" aria-hidden="true">{I[icon]}</span><div class="news-body"><p class="news-text">{n["text"]}</p><span class="news-meta">{meta}</span></div></li>\n'

def bullets(items, cls="ach-list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def news_hero(n):
    icon, label = NEWS_KIND.get(n.get("kind", "update"), NEWS_KIND["update"])
    return f'<a class="news-hero" href="news.html#y{n["year"]}"><span class="news-hero__icon" aria-hidden="true">{I[icon]}</span><span class="news-hero__body"><span class="news-hero__label">{label} &middot; {n["year"]}</span><span class="news-hero__text">{n["text"]}</span></span></a>'

def system_tile(x):
    links = "".join(f'<a class="iconbtn" href="{esc_attr(u)}"{"" if u.endswith(".html") else " target=\"_blank\" rel=\"noopener\""} title="{LINK_ICON[k][1]}" aria-label="{x["name"]} {LINK_ICON[k][1]}">{I[LINK_ICON[k][0]]}<span>{LINK_ICON[k][1]}</span></a>' for k, u in x["links"].items() if u and k in LINK_ICON)
    return f'<li class="system system--{x["kind"]}"><span class="system__icon" aria-hidden="true">{I[SYS_ICON.get(x["kind"], "wrench")]}</span><div class="system__body"><h3 class="system__name">{x["name"]}</h3><p class="system__desc">{x["description"]}</p><div class="system__meta"><span class="system__venue">{x["venue"]}</span>{links}</div></div></li>'

def links_card():
    rows = "".join(f'<a href="{esc_attr(l["url"])}"{"" if l["url"].startswith("mailto:") else " target=\"_blank\" rel=\"noopener\""}>{B.get(l["kind"], I.get(l["kind"], ""))}<span>{l["label"]}</span></a>' for l in P["links"])
    return f'<section class="card"><h2 class="card__title">Contact &amp; links</h2><div class="links">{rows}</div></section>'

# ── index ────────────────────────────────────────────────────────
def build_index():
    affils = "".join(f'<a class="affil" href="{a["url"]}" target="_blank" rel="noopener"><img class="affil__logo" src="static/media/{a["logo"]}" alt="" width="36" height="36" /><span class="affil__long">{a["name"]}</span><span class="affil__short">{a["short"]}</span></a>' for a in P["affiliations"])
    interests = "".join(f'<span class="pill">{i}</span>' for i in P["interests"])
    research = "".join(f"""        <li class="project">
          <div class="project__icon">{r["icon"]}</div>
          <div class="project__body">
            <h3>{r["title"]}</h3>
            <p class="project__description">{r["description"]}</p>
            <div class="project__stack">{"".join(f'<span class="project__stack-item">{t}</span>' for t in r["tags"])}</div>
          </div>
        </li>
""" for r in RESEARCH)
    body = f"""<section class="card vcard" aria-labelledby="name">
  <div class="vcard__side">
    <img src="static/media/profile.jpg" alt="Garvit Chugh" class="vcard__photo" width="240" height="240" fetchpriority="high" />
  </div>
  <div class="vcard__main">
    <div class="vcard__id">
      <h1 class="vcard__name" id="name">{P.get("honorific", "")} {P["name"]}</h1>
      <p class="vcard__headline">{P["headline"]}</p>
      <p class="vcard__tagline">{P["tagline"]}</p>
      <p class="vcard__now"><span class="vcard__now-dot" aria-hidden="true"></span>{P["now"]}</p>
    </div>
    <div class="vcard__ctas">
    <p class="vcard__meta">{I["pin"]}{P["location"]}</p>
    <div class="vcard__affil">{affils}</div>
    <div class="vcard__actions">
      <a class="btn btn--primary" href="mailto:{P["email"]}">{I["mail"]}<span>Contact</span></a>
      <a class="btn btn--outline" href="static/media/Garvit_Resume.pdf" target="_blank" rel="noopener" title="Curriculum vitae, {P.get("cv_updated", "")}">{I["file"]}<span>CV</span></a>
      <a class="btn btn--ghost" href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">{I["scholar"]}<span>Scholar</span></a>
    </div>
    </div>
  </div>
</section>

<div class="grid">
  <aside class="aside aside--top" aria-label="Latest news">
    <section class="card" id="news" aria-labelledby="news-title">
      <h2 class="card__title" id="news-title">Latest</h2>
      {news_hero(next(n for n in NEWS if n.get("featured")))}
      <ol class="news-list news-list--timeline">
{"".join(news_item(n) for n in [x for x in NEWS if x is not next(y for y in NEWS if y.get("featured"))][:6])}      </ol>
      {show_all("news.html", f"Show all {len(NEWS)} updates")}
    </section>
  </aside>

  <div class="main stack">
    <section class="card" id="about" aria-labelledby="about-title">
      <h2 class="card__title" id="about-title">About</h2>
      <div class="about-text">{"".join(f"<p>{p}</p>" for p in P["about"])}</div>
      <div class="pills">{interests}</div>
    </section>

    <section class="card" id="research" aria-labelledby="research-title">
      <h2 class="card__title" id="research-title">Research</h2>
      <ul class="research">
{research}      </ul>
    </section>

    <section class="card" id="systems" aria-labelledby="systems-title">
      <h2 class="card__title" id="systems-title">Systems I built</h2>
      <p class="card__sub">{len(SYSTEMS)} sensing systems and tools, from prototype to user study.</p>
      <ul class="systems systems--top">{"".join(system_tile(x) for x in SYSTEMS[:2])}</ul>
      {show_all("education.html#systems", f"Show all {len(SYSTEMS)} systems")}
    </section>

    <section class="card" id="experience" aria-labelledby="experience-title">
      <h2 class="card__title" id="experience-title">Experience</h2>
      {entries(EXPERIENCE[:3])}
      {show_all("education.html", f"Show all {len(EXPERIENCE)} roles")}
    </section>

    <section class="card" id="education" aria-labelledby="education-title">
      <h2 class="card__title" id="education-title">Education</h2>
      {entries(EDUCATION)}
      {show_all("education.html#teaching", "Show teaching &amp; mentorship")}
    </section>

    <section class="card" id="publications" aria-labelledby="publications-title">
      <h2 class="card__title" id="publications-title">Publications</h2>
      <p class="card__sub">Selected papers. {PUB_SUMMARY}</p>
      <ul class="pub-list">
{"".join(pub_item(p) for p in PUBS if p.get("selected"))}      </ul>
      {show_all("publications.html", f"Show all {N_PUBS} publications")}
    </section>

    <section class="card" id="honours" aria-labelledby="honours-title">
      <h2 class="card__title" id="honours-title">Honours &amp; awards</h2>
      <ol class="news-list">
{"".join(honour_item(h) for h in HONOURS if h["featured"])}      </ol>
      {show_all("awards.html", f"Show all {len(HONOURS)} honours &amp; grants")}
    </section>
  </div>

  <aside class="aside aside--bottom" aria-label="Sidebar" tabindex="0">
    <section class="card"><h2 class="card__title">Skills &amp; languages</h2><div class="pills">{"".join(f'<span class="pill">{s}</span>' for s in P["skills"])}</div><div class="stack" style="gap:0;margin-top:14px">{bullets(P["languages"])}</div></section>
    <section class="card"><h2 class="card__title">Service</h2>{bullets(P["service_short"])}</section>
    {links_card()}
  </aside>
</div>"""
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": P["name"], "honorificPrefix": P.get("honorific", ""), "url": SITE + "/",
        "image": f"{SITE}/static/media/profile.jpg", "email": f"mailto:{P['email']}", "jobTitle": "Postdoctoral Researcher",
        "worksFor": {"@type": "Organization", "name": "Singapore Management University"},
        "alumniOf": [{"@type": "Organization", "name": "Indian Institute of Technology Jodhpur"}, {"@type": "Organization", "name": "Guru Gobind Singh Indraprastha University"}],
        "sameAs": [l["url"] for l in P["links"] if not l["url"].startswith("mailto:")],
        "knowsAbout": ["Earable Computing", "Wearable Sensing", "Human-Computer Interaction", "Mobile and Pervasive Computing", "Ubiquitous Computing", "Human-Centered AI"]}, indent=1)
    return shell("Garvit Chugh", "Postdoctoral Researcher at Singapore Management University. Ph.D. from IIT Jodhpur. Research in earable and wearable sensing, human-computer interaction, and pervasive computing.",
                 "", "index.html", body, extra_head=f'  <script type="application/ld+json">{jsonld}</script>\n', ogtype="profile")

# ── publications ─────────────────────────────────────────────────
TRACKS = [("main", "Main track"), ("workshop", "Workshop / WiP"), ("journal", "Journal"), ("patent", "Patent"), ("review", "Under review")]
TOPICS = [("sensing", "Sensing"), ("healthcare", "Healthcare"), ("hci", "HCI"), ("mlai", "ML / AI"), ("security", "Security"), ("systems", "Systems")]

def build_publications():
    years = []
    for p in PUBS:
        if p["year"] not in years: years.append(p["year"])
    def label_year(y): return "Under review" if y == "review" else "Patent" if y == "patent" else y
    def select(id_, label, options):
        opts = "".join(f'<option value="{v}">{t}</option>' for v, t in options)
        return f'<label class="select"><span class="select__label">{label}</span><select id="{id_}" aria-label="{label}"><option value="all">All</option>{opts}</select></label>'
    toolbar = select("yearSelect", "Year", [(y, label_year(y)) for y in years]) + select("trackSelect", "Track", TRACKS) + select("topicSelect", "Topic", TOPICS) + '<button type="button" class="btn btn--ghost btn--sm" id="resetFilters" hidden>Reset</button>'
    groups = ""
    for y in years:
        groups += f'      <h2 class="pub-year" data-year-heading="{y}">{label_year(y)}</h2>\n      <ul class="pub-list">\n' + "".join(pub_item(p) for p in PUBS if p["year"] == y) + "      </ul>\n"
    topic_counts = {k: sum(k in p["topics"] for p in PUBS) for k, _ in TOPICS}
    track_counts = {k: sum(p["track"] == k for p in PUBS) for k, _ in TRACKS}
    overview = f"""<section class="card" aria-labelledby="ov-title">
      <h2 class="card__title" id="ov-title">Overview</h2>
      <dl class="stats-list">
        <div><dt>Total</dt><dd>{N_PUBS}</dd></div>
        <div><dt>Peer-reviewed</dt><dd>{N_PEER}</dd></div>
        <div><dt>Patent filed</dt><dd>{N_PATENT}</dd></div>
        <div><dt>Under review</dt><dd>{N_REVIEW}</dd></div>
        <div><dt>Citations</dt><dd>{CITES_TOTAL}</dd></div>
        <div><dt>h-index</dt><dd>{H_INDEX if H_INDEX is not None else "&ndash;"}</dd></div>
      </dl>
      <p class="muted" style="font-size:var(--t-xs);margin-top:6px">Citation counts from <a class="link" href="{OPENALEX["author"].get("openalex_id", "https://openalex.org")}" target="_blank" rel="noopener">OpenAlex</a>; Google Scholar usually reads higher.</p>
      <h3 class="card__sub-title">By track</h3>
      <div class="pills">{"".join(f'<button type="button" class="pill pill--btn" data-filter="track" data-value="{k}">{t} <b>{track_counts[k]}</b></button>' for k, t in TRACKS)}</div>
      <h3 class="card__sub-title">By topic</h3>
      <div class="pills">{"".join(f'<button type="button" class="pill pill--btn" data-filter="topic" data-value="{k}">{t} <b>{topic_counts[k]}</b></button>' for k, t in TOPICS)}</div>
      <h3 class="card__sub-title">Legend</h3>
      <p class="legend"><span class="pub-badge pub-badge--core">Core A*</span> top-tier venue in the CORE ranking &middot; <span class="pub-badge pub-badge--wip">WiP</span> work-in-progress, poster, demo or artefact track &middot; <strong>*</strong> equal contribution</p>
      <h3 class="card__sub-title">Full record</h3>
      <div class="links"><a href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">{B["scholar"]}<span>Google Scholar</span></a><a href="https://dblp.org/pid/302/5075" target="_blank" rel="noopener">{B["dblp"]}<span>DBLP</span></a><a href="https://orcid.org/0000-0002-0354-9731" target="_blank" rel="noopener">{B["orcid"]}<span>ORCID</span></a></div>
    </section>"""
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <section class="card">
      <div class="toolbar">
        <div>
          <h1 class="page-title">Publications</h1>
          <p class="page-subtitle" style="margin-bottom:0">{PUB_SUMMARY} <span class="filter-count" id="filterCount" aria-live="polite"></span></p>
        </div>
        <div class="toolbar__controls">{toolbar}</div>
      </div>
      <div class="no-results" id="noResults" role="status">No publications match the selected filters.</div>
      <div id="pubContainer">
{groups}      </div>
    </section>
  </div>
  <aside class="aside aside--bottom" aria-label="Sidebar" tabindex="0">
    {overview}
  </aside>
</div>
<script>
  const selects = {{ year: document.getElementById('yearSelect'), track: document.getElementById('trackSelect'), topic: document.getElementById('topicSelect') }};
  const items = document.querySelectorAll('.pub-item');
  const countEl = document.getElementById('filterCount');
  const noResults = document.getElementById('noResults');
  const reset = document.getElementById('resetFilters');
  function applyFilters() {{
    const f = {{ year: selects.year.value, track: selects.track.value, topic: selects.topic.value }};
    let visible = 0;
    items.forEach(item => {{
      const show = (f.year === 'all' || item.dataset.year === f.year)
        && (f.track === 'all' || item.dataset.track === f.track)
        && (f.topic === 'all' || item.dataset.topic.split(' ').includes(f.topic));
      item.classList.toggle('hidden', !show);
      if (show) visible++;
    }});
    document.querySelectorAll('[data-year-heading]').forEach(h => {{
      const any = Array.from(items).some(i => i.dataset.year === h.dataset.yearHeading && !i.classList.contains('hidden'));
      h.hidden = !any; h.nextElementSibling.hidden = !any;
    }});
    const filtered = Object.values(f).some(v => v !== 'all');
    countEl.textContent = filtered ? `Showing ${{visible}} of ${{items.length}}.` : '';
    reset.hidden = !filtered;
    noResults.style.display = visible === 0 ? 'block' : 'none';
    document.querySelectorAll('.pill--btn').forEach(p => p.classList.toggle('active', f[p.dataset.filter] === p.dataset.value));
  }}
  Object.values(selects).forEach(sel => sel.addEventListener('change', applyFilters));
  reset.addEventListener('click', () => {{ Object.values(selects).forEach(sel => sel.value = 'all'); applyFilters(); }});
  document.querySelectorAll('.pill--btn').forEach(p => p.addEventListener('click', () => {{
    const sel = selects[p.dataset.filter]; sel.value = sel.value === p.dataset.value ? 'all' : p.dataset.value; applyFilters();
    document.getElementById('pubContainer').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}));
</script>"""
    def article(p):
        names = [re.sub(r"[*]", "", a.strip()) for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&amp;\s|\s&\s", re.sub(r"\s*\(\*Equal Contributions?\)", "", re.sub(r"<[^>]+>", "", p["authors"]))) if a.strip()]
        d = {"@type": "ScholarlyArticle", "headline": re.sub(r"<[^>]+>", "", p["title"]).replace("&amp;", "&"), "author": [{"@type": "Person", "name": n} for n in names],
             "isPartOf": {"@type": "Periodical" if p["track"] == "journal" else "Event", "name": p["venue"].replace("&amp;", "&")}}
        if p["year"].isdigit(): d["datePublished"] = p["year"]
        if p.get("url"): d["url"] = p["url"]
        return d
    ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Publications by Garvit Chugh", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": article(p)} for i, p in enumerate(PUBS) if p["track"] != "review"]}, ensure_ascii=False)
    return shell("Publications - Garvit Chugh", f"{PUB_SUMMARY} Research by Garvit Chugh at CHI, PerCom, SenSys, PACMHCI, CIKM, ICDM and more.", "publications.html", "publications.html", body, extra_head=f'  <script type="application/ld+json">{ld}</script>\n')

# ── news ─────────────────────────────────────────────────────────
def build_news():
    years = sorted({n["year"] for n in NEWS}, reverse=True)
    groups = "".join(f'      <h2 class="pub-year" id="y{y}">{y} <span class="muted">&middot; {sum(n["year"] == y for n in NEWS)}</span></h2>\n      <ol class="news-grid">\n' + "".join(f'        <li class="news-tile news-tile--{n.get("kind","update")}{" news-tile--featured" if n.get("featured") else ""}"><span class="news-icon" aria-hidden="true">{I[NEWS_KIND.get(n.get("kind","update"), NEWS_KIND["update"])[0]]}</span><div class="news-body"><p class="news-text">{n["text"]}</p><span class="news-meta">{NEWS_KIND.get(n.get("kind","update"), NEWS_KIND["update"])[1]}</span></div></li>\n' for n in NEWS if n["year"] == y) + "      </ol>\n" for y in years)
    jump = "".join(f'<a class="pill pill--btn" href="#y{y}">{y} <b>{sum(n["year"] == y for n in NEWS)}</b></a>' for y in years)
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <section class="card">
      <h1 class="page-title">News</h1>
      <p class="page-subtitle">{len(NEWS)} updates, newest first.</p>
{groups}    </section>
  </div>
  <aside class="aside aside--bottom" aria-label="Sidebar" tabindex="0">
    <section class="card"><h2 class="card__title">Jump to year</h2><div class="pills">{jump}</div></section>
    <section class="card"><h2 class="card__title">Highlights</h2><ol class="news-list">{"".join(news_item(n) for n in NEWS if n.get("featured"))}</ol></section>
  </aside>
</div>"""
    return shell("News - Garvit Chugh", "Latest news and updates from Garvit Chugh.", "news.html", "news.html", body)

# ── experience & education ───────────────────────────────────────
def build_education():
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <section class="card">
      <h1 class="page-title">Experience</h1>
      {entries(EXPERIENCE, level=2)}
    </section>
    <section class="card">
      <h2 class="card__title">Education</h2>
      {entries(EDUCATION)}
    </section>
    <section class="card" id="systems">
      <h2 class="card__title">Systems I built</h2>
      <p class="card__sub">{len(SYSTEMS)} sensing systems and tools, from prototype to user study. Each links to its paper; code and video links appear as they are released.</p>
      <ul class="systems systems--2">{"".join(system_tile(x) for x in SYSTEMS)}</ul>
    </section>
    <section class="card" id="teaching">
      <h2 class="card__title">Teaching (IIT Jodhpur)</h2>
      {bullets(TEACHING)}
    </section>
    <section class="card">
      <h2 class="card__title">PMRF outreach &amp; external teaching</h2>
      {bullets(OUTREACH)}
    </section>
  </div>
  <aside class="aside aside--bottom" aria-label="Sidebar" tabindex="0">
    <section class="card"><h2 class="card__title">Labs I have been a part of</h2><ul class="labs">{"".join(f'<li class="lab"><a class="lab__link" href="{l["url"]}" target="_blank" rel="noopener"><span class="entry__logo lab__logo"><img src="static/media/{l["logo"]}" alt="" width="64" height="64" loading="lazy" decoding="async" /></span><span class="lab__body"><span class="lab__name">{l["name"]}</span><span class="lab__org">{l["org"]}</span><span class="entry__meta">{l["role"]} &middot; {l["years"]}</span></span></a></li>' for l in LABS)}</ul></section>
    <section class="card"><h2 class="card__title">Supervision &amp; mentorship</h2>{bullets(MENTORSHIP)}</section>
    <section class="card"><h2 class="card__title">Skills &amp; languages</h2>{bullets(SKILLS_FULL)}</section>
  </aside>
</div>"""
    return shell("Experience - Garvit Chugh", "Experience, education, teaching, and mentorship of Garvit Chugh.", "education.html", "education.html", body)

# ── honours ──────────────────────────────────────────────────────
def honour_tile(h, with_year=False):
    icon, label = HON_KIND[h["kind"]]
    meta = label + (f' &middot; {h["when"] or h["year"] or ""}' if with_year else (f' &middot; {h["when"]}' if h["when"] and not re.fullmatch(r"\d{4}", h["when"]) else ""))
    cls = f'news-tile news-tile--{h["kind"]}' + (" news-tile--featured" if h["featured"] else "")
    return f'        <li class="{cls}"><span class="news-icon" aria-hidden="true">{I[icon]}</span><div class="news-body"><p class="news-text">{h["text"]}</p><span class="news-meta">{meta}</span></div></li>\n'

def honour_item(h):
    icon, label = HON_KIND[h["kind"]]
    cls = f'news-item news-item--{h["kind"]}' + (" news-item--featured" if h["featured"] else "")
    return f'      <li class="{cls}"><span class="news-icon" aria-hidden="true">{I[icon]}</span><div class="news-body"><p class="news-text">{h["text"]}</p><span class="news-meta">{label} &middot; {h["when"] or h["year"] or ""}</span></div></li>\n'

def build_awards():
    years = sorted({h["year"] for h in HONOURS if h["year"]}, reverse=True)
    groups = ""
    for y in years:
        hs = [h for h in HONOURS if h["year"] == y]
        groups += f'      <h2 class="pub-year" id="h{y}">{y} <span class="muted">&middot; {len(hs)}</span></h2>\n      <ul class="news-grid">\n' + "".join(honour_tile(h) for h in hs) + "      </ul>\n"
    undated = [h for h in HONOURS if not h["year"]]
    if undated: groups += '      <h2 class="pub-year">Other</h2>\n      <ul class="news-grid">\n' + "".join(honour_tile(h) for h in undated) + "      </ul>\n"
    counts = {k: sum(h["kind"] == k for h in HONOURS) for k in HON_KIND if any(h["kind"] == k for h in HONOURS)}
    n_awards = sum(h["source"] == "awards" for h in HONOURS); n_fund = len(HONOURS) - n_awards
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <section class="card">
      <h1 class="page-title">Honours &amp; awards</h1>
      <p class="page-subtitle">{len(HONOURS)} in total: {n_awards} honours and {n_fund} fellowships and grants, newest first.</p>
{groups}    </section>
  </div>
  <aside class="aside aside--bottom" aria-label="Sidebar" tabindex="0">
    <section class="card"><h2 class="card__title">Highlights</h2><ol class="news-list">{"".join(honour_item(h) for h in HONOURS if h["featured"])}</ol></section>
    <section class="card"><h2 class="card__title">By kind</h2><div class="pills">{"".join(f'<span class="pill">{I[HON_KIND[k][0]]} {HON_KIND[k][1]} <b>{v}</b></span>' for k, v in counts.items())}</div></section>
    <section class="card"><h2 class="card__title">Community service</h2>{bullets(SERVICE)}</section>
  </aside>
</div>"""
    return shell("Honours - Garvit Chugh", "Honours, awards, fellowships, grants, and professional service of Garvit Chugh.", "awards.html", "awards.html", body)

# ── one page per paper (Google Scholar indexes these) ────────────
def build_paper(p):
    plain_title = re.sub(r"<[^>]+>", "", p["title"]).replace("&amp;", "&")
    plain_authors = re.sub(r"\s*\(\*Equal Contributions?\)", "", re.sub(r"<[^>]+>", "", p["authors"])).replace("&amp;", "&").replace("*", "")
    names = [a.strip() for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&\s", plain_authors) if a.strip()]
    year = p["year"] if p["year"].isdigit() else ("2025" if p["year"] == "patent" else "2026")
    venue = p["venue"].replace("&amp;", "&")
    links = p.get("links") or {}
    meta = [("citation_title", plain_title), ("citation_publication_date", year), ("citation_journal_title" if p["track"] == "journal" else "citation_conference_title", venue)]
    meta += [("citation_author", n) for n in names]
    if p.get("url") and "doi.org/" in p["url"]: meta.append(("citation_doi", p["url"].split("doi.org/")[1]))
    if links.get("pdf"): meta.append(("citation_pdf_url", links["pdf"]))
    meta_html = "".join(f'  <meta name="{k}" content="{esc_attr(v)}" />\n' for k, v in meta)
    badges = "".join(f' <span class="pub-badge pub-badge--{b["kind"]}" title="{esc_attr(BADGE_TITLES.get(b["kind"], b["text"]))}">{b["text"]}</span>' for b in p["badges"])
    btns = "".join(f'<a class="btn btn--outline" href="{esc_attr(u)}" target="_blank" rel="noopener">{I[LINK_ICON[k][0]]}<span>{LINK_ICON[k][1]}</span></a>' for k, u in links.items() if u and k in LINK_ICON)
    abstract = f'<h2 class="card__title">Abstract</h2><p class="paper__abstract">{p["abstract"]}</p>' if p.get("abstract") else ""
    cited = f'<div><dt>Citations</dt><dd>{p["cited"]}</dd></div>' if p.get("cited") else ""
    related = [q for q in PUBS if q is not p and set(q["topics"]) & set(p["topics"])][:4]
    related_html = "".join(f'<li><a class="link" href="papers/{q["slug"]}.html">{q["title"]}</a> <span class="muted">&middot; {q["venue"]}</span></li>' for q in related)
    ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": plain_title, "author": [{"@type": "Person", "name": n} for n in names],
          "datePublished": year, "isPartOf": {"@type": "Periodical" if p["track"] == "journal" else "Event", "name": venue}, "url": f"{SITE}/papers/{p['slug']}.html"}
    if p.get("url"): ld["sameAs"] = p["url"]
    if p.get("abstract"): ld["abstract"] = p["abstract"]
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <article class="card paper">
      <p class="paper__kicker"><a class="link" href="publications.html">Publications</a> &rsaquo; {p["venue"]}</p>
      <h1 class="page-title paper__title">{p["title"]}</h1>
      <p class="paper__authors">{p["authors"]}</p>
      <p class="pub-meta"><span class="pub-venue">{p["venue"]}</span>{badges}{"".join(f'<span class="pub-tag">{t}</span>' for t in p["tags"])}</p>
      <div class="paper__actions">{btns}<button type="button" class="btn btn--ghost iconbtn--copy" data-bib="{esc_attr(bibtex(p))}">{I["quote"]}<span>BibTeX</span></button></div>
      {abstract}
      <h2 class="card__title">BibTeX</h2>
      <pre class="bibtex">{bibtex(p).replace("&", "&amp;").replace("<", "&lt;")}</pre>
    </article>
  </div>
  <aside class="aside aside--bottom" aria-label="Paper details" tabindex="0">
    <section class="card"><h2 class="card__title">At a glance</h2>
      <dl class="stats-list"><div><dt>Year</dt><dd>{year}</dd></div><div><dt>Track</dt><dd>{dict(TRACKS).get(p["track"], p["track"]).split(" /")[0]}</dd></div>{cited}</dl>
      {'<h3 class="card__sub-title">Related</h3><ul class="ach-list">' + related_html + '</ul>' if related_html else ''}
    </section>
  </aside>
</div>"""
    desc = (p.get("abstract") or f"{plain_title}. {plain_authors}. {venue}.")[:300].rsplit(" ", 1)[0]
    return shell(f"{plain_title} - Garvit Chugh", esc_attr(desc), f"papers/{p['slug']}.html", "publications.html", body,
                 extra_head=meta_html + f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n', ogtype="article")

def build_404():
    return shell("Page not found - Garvit Chugh", "This page does not exist.", "404.html", "", """<section class="card notfound">
  <h1 class="page-title">404</h1>
  <p class="muted">This page doesn&rsquo;t exist.</p>
  <a class="btn btn--primary" href="index.html">Back to home</a>
</section>""")

def build_rss():
    import html as _h
    items = ""
    for n in NEWS:
        text = _h.unescape(re.sub(r"<[^>]+>", "", n["text"]))
        items += f"    <item><title>{_h.escape(text[:120])}</title><link>{SITE}/news.html#y{n['year']}</link><guid isPermaLink=\"false\">news-{n['id']}</guid><pubDate>{n['year']}-01-01</pubDate><description>{_h.escape(text)}</description></item>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Garvit Chugh: news</title><link>{SITE}/news.html</link><description>Updates from Garvit Chugh</description>\n{items}</channel></rss>\n'

def build_sitemap():
    pages = [("", "1.0"), ("publications.html", "0.9"), ("news.html", "0.8"), ("education.html", "0.7"), ("awards.html", "0.7")] + [(f"papers/{p['slug']}.html", "0.6") for p in PUBS]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

if __name__ == "__main__":
    out = {"index.html": build_index(), "publications.html": build_publications(), "news.html": build_news(),
           "education.html": build_education(), "awards.html": build_awards(), "404.html": build_404(), "sitemap.xml": build_sitemap(), "news.xml": build_rss()}
    (ROOT / "papers").mkdir(exist_ok=True)
    for p in PUBS: out[f"papers/{p['slug']}.html"] = build_paper(p)
    for name, html in out.items():
        if name.endswith(".html"):  # relative page/asset links -> root-relative, so /papers/* resolve the same shell
            html = re.sub(r'((?:href|src)=")(?!(?:https?:|mailto:|#|/|data:))', r'\1/', html)
        (ROOT / name).write_text(html)
    print(f"built {len(out)} files · {PUB_SUMMARY} · {len(NEWS)} news items")
