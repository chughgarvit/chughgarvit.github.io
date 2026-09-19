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
MENTORSHIP = load("mentorship"); SKILLS_FULL = load("skills"); AWARDS = load("awards"); FUNDING = load("funding")
SERVICE = load("service")

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
}
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
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="static/media/favicon-32.png" sizes="32x32" type="image/png" />
  <link rel="apple-touch-icon" href="static/media/apple-touch-icon.png" />
  <link rel="preload" href="static/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin />
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
</header>
<main id="main" class="page">
{body}
</main>
<footer class="footer">Garvit Chugh &copy; {TODAY[:4]} &middot; Updated {TODAY}</footer>
<script>
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
        return f'<img src="static/media/{item["logo"]}" alt="" width="64" height="64" />'
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
    return '<ul class="entries">\n' + "".join(entry(e, level) for e in items) + "</ul>"

def pub_item(p, heading_level=3):
    badges = "".join(f' <span class="pub-badge pub-badge--{b["kind"]}" title="{esc_attr(BADGE_TITLES.get(b["kind"], b["text"]))}">{b["text"]}</span>' for b in p["badges"])
    title = f'<a href="{p["url"]}" target="_blank" rel="noopener">{p["title"]}</a>' if p.get("url") else p["title"]
    tags = "".join(f'<span class="pub-tag">{t}</span>' for t in p["tags"])
    return f"""      <li class="pub-item" data-year="{p["year"]}" data-track="{p["track"]}" data-topic="{' '.join(p["topics"])}">
        <h{heading_level} class="pub-title">{title}</h{heading_level}>
        <div class="pub-badges">{badges.strip()}</div>
        <div class="pub-authors">{p["authors"]}</div>
        <div class="pub-venue">{p["venue"]}</div>
        <div class="pub-tags">{tags}</div>
      </li>
"""

def news_item(n, with_year=True):
    year = f'<span class="news-year">{n["year"]}</span>' if with_year else ""
    return f'      <li class="news-item">{year}<p class="news-text">{n["text"]}</p></li>\n'

def bullets(items, cls="ach-list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

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
      <h1 class="vcard__name" id="name">{P["name"]}</h1>
      <p class="vcard__headline">{P["headline"]}</p>
      <p class="vcard__tagline">{P["tagline"]}</p>
    </div>
    <div class="vcard__ctas">
    <p class="vcard__meta">{I["pin"]}{P["location"]}</p>
    <div class="vcard__affil">{affils}</div>
    <div class="vcard__actions">
      <a class="btn btn--primary" href="mailto:{P["email"]}">{I["mail"]}<span>Contact</span></a>
      <a class="btn btn--outline" href="static/media/Garvit_Resume.pdf" target="_blank" rel="noopener">{I["file"]}<span>Resume</span></a>
      <a class="btn btn--ghost" href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">{I["scholar"]}<span>Scholar</span></a>
    </div>
    </div>
  </div>
</section>

<div class="grid">
  <aside class="aside aside--top">
    <section class="card" id="news" aria-labelledby="news-title">
      <h2 class="card__title" id="news-title">Latest</h2>
      <ol class="news-list">
{"".join(news_item(n) for n in NEWS[:6])}      </ol>
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
      <p class="card__sub">Selected recent work. {PUB_SUMMARY}</p>
      <ul class="pub-list">
{"".join(pub_item(p) for p in PUBS[:5])}      </ul>
      {show_all("publications.html", f"Show all {N_PUBS} publications")}
    </section>

    <section class="card" id="honours" aria-labelledby="honours-title">
      <h2 class="card__title" id="honours-title">Honours &amp; awards</h2>
      {bullets(AWARDS[:6])}
      {show_all("awards.html", f"Show all {len(AWARDS) + len(FUNDING)} honours &amp; grants")}
    </section>
  </div>

  <aside class="aside aside--bottom">
    <section class="card"><h2 class="card__title">Skills &amp; languages</h2><div class="pills">{"".join(f'<span class="pill">{s}</span>' for s in P["skills"])}</div><div class="stack" style="gap:0;margin-top:14px">{bullets(P["languages"])}</div></section>
    <section class="card"><h2 class="card__title">Service</h2>{bullets(P["service_short"])}</section>
    {links_card()}
  </aside>
</div>"""
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": P["name"], "url": SITE + "/",
        "image": f"{SITE}/static/media/profile.jpg", "email": f"mailto:{P['email']}", "jobTitle": "Postdoctoral Researcher",
        "worksFor": {"@type": "Organization", "name": "Singapore Management University"},
        "alumniOf": [{"@type": "Organization", "name": "Indian Institute of Technology Jodhpur"}, {"@type": "Organization", "name": "Guru Gobind Singh Indraprastha University"}],
        "sameAs": [l["url"] for l in P["links"] if not l["url"].startswith("mailto:")],
        "knowsAbout": ["Earable Computing", "Wearable Sensing", "Human-Computer Interaction", "Mobile and Pervasive Computing", "Ubiquitous Computing", "Human-Centered AI"]}, indent=1)
    return shell("Garvit Chugh", "Postdoctoral Researcher at Singapore Management University. Ph.D. from IIT Jodhpur. Research in earable and wearable sensing, human-computer interaction, and pervasive computing.",
                 "", "index.html", body, extra_head=f'  <script type="application/ld+json">{jsonld}</script>\n', ogtype="profile")

# ── publications ─────────────────────────────────────────────────
def build_publications():
    years = []
    for p in PUBS:
        if p["year"] not in years: years.append(p["year"])
    def fgroup(label, id_, options):
        btns = "".join(f'<button type="button" class="filter-btn{" active" if v == "all" else ""}" data-value="{v}" aria-pressed="{"true" if v == "all" else "false"}">{t}</button>' for v, t in options)
        return f'<div class="filter-group" role="group" aria-label="{label}"><span class="filter-label">{label}</span><div class="filter-btns" id="{id_}">{btns}</div></div>'
    year_opts = [("all", "All")] + [(y, "Under Review" if y == "review" else y.capitalize() if y == "patent" else y) for y in years]
    filters = fgroup("Year", "yearFilter", year_opts) + fgroup("Track", "trackFilter", [("all", "All"), ("main", "Main Track"), ("workshop", "Workshop / WiP"), ("journal", "Journal"), ("patent", "Patent"), ("review", "Under Review")]) + fgroup("Topic", "topicFilter", [("all", "All"), ("sensing", "Sensing"), ("healthcare", "Healthcare"), ("hci", "HCI"), ("mlai", "ML / AI"), ("security", "Security"), ("systems", "Systems")])
    groups = ""
    for y in years:
        label = "Under Review" if y == "review" else "Patent" if y == "patent" else y
        groups += f'      <h2 class="pub-year" data-year-heading="{y}">{label}</h2>\n      <ul class="pub-list">\n' + "".join(pub_item(p) for p in PUBS if p["year"] == y) + "      </ul>\n"
    body = f"""<div class="stack">
  <section class="card">
    <h1 class="page-title">Publications</h1>
    <p class="page-subtitle">{PUB_SUMMARY} <span class="filter-count" id="filterCount" aria-live="polite"></span></p>
    <div class="filters">{filters}</div>
    <p class="legend"><span class="pub-badge pub-badge--core">Core A*</span> top-tier venue in the CORE ranking &middot; <span class="pub-badge pub-badge--wip">WiP</span> work-in-progress, poster, demo or artefact track &middot; <strong>*</strong> equal contribution</p>
  </section>
  <section class="card">
    <div class="no-results" id="noResults" role="status">No publications match the selected filters.</div>
    <div id="pubContainer">
{groups}    </div>
    <p class="pub-note">Full record on <a class="link" href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar</a> and <a class="link" href="https://dblp.org/pid/302/5075" target="_blank" rel="noopener">DBLP</a>.</p>
  </section>
</div>
<script>
  const filters = {{ year: 'all', track: 'all', topic: 'all' }};
  const items = document.querySelectorAll('.pub-item');
  const countEl = document.getElementById('filterCount');
  const noResults = document.getElementById('noResults');
  function applyFilters() {{
    let visible = 0;
    items.forEach(item => {{
      const show = (filters.year === 'all' || item.dataset.year === filters.year)
        && (filters.track === 'all' || item.dataset.track === filters.track)
        && (filters.topic === 'all' || item.dataset.topic.split(' ').includes(filters.topic));
      item.classList.toggle('hidden', !show);
      if (show) visible++;
    }});
    document.querySelectorAll('[data-year-heading]').forEach(h => {{
      const any = Array.from(items).some(i => i.dataset.year === h.dataset.yearHeading && !i.classList.contains('hidden'));
      h.hidden = !any; h.nextElementSibling.hidden = !any;
    }});
    const filtered = Object.values(filters).some(v => v !== 'all');
    countEl.textContent = filtered ? `Showing ${{visible}} of ${{items.length}}.` : '';
    noResults.style.display = visible === 0 ? 'block' : 'none';
  }}
  document.querySelectorAll('.filter-btns').forEach(group => {{
    group.addEventListener('click', e => {{
      const btn = e.target.closest('.filter-btn'); if (!btn) return;
      group.querySelectorAll('.filter-btn').forEach(b => {{ b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); }});
      btn.classList.add('active'); btn.setAttribute('aria-pressed', 'true');
      filters[group.id.replace('Filter', '')] = btn.dataset.value;
      applyFilters();
    }});
  }});
</script>"""
    return shell("Publications - Garvit Chugh", f"{PUB_SUMMARY} Research by Garvit Chugh at CHI, PerCom, SenSys, PACMHCI, CIKM, ICDM and more.", "publications.html", "publications.html", body)

# ── news ─────────────────────────────────────────────────────────
def build_news():
    groups = ""
    for y in sorted({n["year"] for n in NEWS}, reverse=True):
        groups += f'  <h2 class="news-year-heading">{y}</h2>\n  <ol class="news-list">\n' + "".join(news_item(n, with_year=False) for n in NEWS if n["year"] == y) + "  </ol>\n"
    body = f"""<section class="card">
  <h1 class="page-title">News</h1>
  <p class="page-subtitle">{len(NEWS)} updates, newest first.</p>
{groups}</section>"""
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
    <section class="card" id="teaching">
      <h2 class="card__title">Teaching (IIT Jodhpur)</h2>
      {bullets(TEACHING)}
    </section>
    <section class="card">
      <h2 class="card__title">PMRF outreach &amp; external teaching</h2>
      {bullets(OUTREACH)}
    </section>
  </div>
  <aside class="aside aside--bottom">
    <section class="card"><h2 class="card__title">Supervision &amp; mentorship</h2>{bullets(MENTORSHIP)}</section>
    <section class="card"><h2 class="card__title">Skills &amp; languages</h2>{bullets(SKILLS_FULL)}</section>
  </aside>
</div>"""
    return shell("Experience - Garvit Chugh", "Experience, education, teaching, and mentorship of Garvit Chugh.", "education.html", "education.html", body)

# ── honours ──────────────────────────────────────────────────────
def build_awards():
    body = f"""<div class="grid grid--2">
  <div class="main stack">
    <section class="card">
      <h1 class="page-title">Honours &amp; awards</h1>
      {bullets(AWARDS)}
    </section>
    <section class="card">
      <h2 class="card__title">Research funding &amp; fellowships</h2>
      {bullets(FUNDING)}
    </section>
  </div>
  <aside class="aside aside--bottom">
    <section class="card"><h2 class="card__title">Community service</h2>{bullets(SERVICE)}</section>
  </aside>
</div>"""
    return shell("Honours - Garvit Chugh", "Honours, awards, fellowships, grants, and professional service of Garvit Chugh.", "awards.html", "awards.html", body)

def build_404():
    return shell("Page not found - Garvit Chugh", "This page does not exist.", "404.html", "", """<section class="card notfound">
  <h1 class="page-title">404</h1>
  <p class="muted">This page doesn&rsquo;t exist.</p>
  <a class="btn btn--primary" href="index.html">Back to home</a>
</section>""")

def build_sitemap():
    pages = [("", "1.0"), ("publications.html", "0.9"), ("news.html", "0.8"), ("education.html", "0.7"), ("awards.html", "0.7")]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

if __name__ == "__main__":
    out = {"index.html": build_index(), "publications.html": build_publications(), "news.html": build_news(),
           "education.html": build_education(), "awards.html": build_awards(), "404.html": build_404(), "sitemap.xml": build_sitemap()}
    for name, html in out.items():
        (ROOT / name).write_text(html)
    print(f"built {len(out)} files · {PUB_SUMMARY} · {len(NEWS)} news items")
