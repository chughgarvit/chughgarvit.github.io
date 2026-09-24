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
SERVICE = load("service"); SYSTEMS = load("systems"); HONOURS = load("honours"); LABS = load("labs"); COLLAB = load("collaborators"); COURSEWORK = load("coursework")
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

NEWS_LABEL = {"paper": "Paper", "award": "Award", "grant": "Grant", "milestone": "Milestone", "service": "Service", "talk": "Talk", "update": "Update"}
HON_LABEL = {"award": "Award", "competition": "Competition", "fellowship": "Fellowship", "travel": "Travel grant", "scholarship": "Scholarship", "recognition": "Recognition", "exam": "Exam", "talk": "Invited talk"}
LINK_LABEL = {"paper": "DOI", "pdf": "PDF", "code": "Code", "video": "Video"}
TRACK_LABEL = {"main": "Main track", "workshop": "Workshop", "journal": "Journal", "patent": "Patent", "review": "Under review"}
CHEV = '<span class="chev" aria-hidden="true">&rsaquo;</span>'

def nav(active):
    return "".join(f'<a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == active else ""}>{I[k]}<span>{l}</span></a>' for h, l, k in NAV)

def shell(title, desc, path, active, body, extra_head="", ogtype="website"):
    url = f"{SITE}/{path}" if path else f"{SITE}/"
    preload = '  <link rel="preload" href="static/media/profile.jpg" as="image" fetchpriority="high" />\n' if active == "index.html" and not path else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#fbfbfd" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)" />
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
{preload}  <script type="speculationrules">{{"prerender":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":"/*.pdf"}}}},{{"not":{{"href_matches":"/*.xml"}}}}]}},"eagerness":"moderate"}}],"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":"/*.pdf"}}}}]}},"eagerness":"moderate"}}]}}</script>
  <link rel="stylesheet" href="static/css/site.css?v={CSS_HASH}" />
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar__inner">
    <a href="index.html" class="topbar__home" aria-label="Garvit Chugh, home">Garvit Chugh</a>
    <nav class="nav" aria-label="Primary">{nav(active)}</nav>
    <button type="button" class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark mode"><span class="ico-sun">{I["sun"]}</span><span class="ico-moon">{I["moon"]}</span></button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <nav class="footer__links" aria-label="Footer">{"".join(f'<a href="{h}">{l}</a>' for h, l, _ in NAV)}<a href="education.html#systems">Systems</a><a href="static/media/Garvit_Resume.pdf" target="_blank" rel="noopener">CV</a><a href="news.xml">RSS</a></nav>
    <p class="footer__meta">Copyright &copy; {TODAY[:4]} Garvit Chugh. Updated {TODAY}. <a href="#main">Back to top</a></p>
  </div>
</footer>
<script>
  document.getElementById('themeToggle').addEventListener('click', () => {{ const dark = matchMedia('(prefers-color-scheme: dark)').matches; const cur = document.documentElement.dataset.theme || (dark ? 'dark' : 'light'); const next = cur === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = next; try {{ localStorage.setItem('theme', next); }} catch (e) {{}} }});
  document.querySelectorAll('.copy-bib').forEach(btn => btn.addEventListener('click', async () => {{ try {{ await navigator.clipboard.writeText(btn.dataset.bib); const t = btn.textContent; btn.textContent = 'Copied'; setTimeout(() => btn.textContent = t, 1600); }} catch (e) {{ prompt('BibTeX', btn.dataset.bib); }} }}));
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {{
    const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -10% 0px' }});
    document.querySelectorAll('.section').forEach(s => {{ if (s.getBoundingClientRect().top > innerHeight) {{ s.classList.add('reveal'); io.observe(s); }} }});
  }}
  (() => {{ let last = scrollY, ticking = false;
    addEventListener('scroll', () => {{ if (ticking) return; ticking = true; requestAnimationFrame(() => {{ const y = scrollY; document.body.classList.toggle('nav-min', innerWidth <= 734 && y > last + 4 && y > 120); if (y < last - 4 || y < 120) document.body.classList.remove('nav-min'); last = y; ticking = false; }}); }}, {{ passive: true }});
  }})();
</script>
</body>
</html>
"""

# ── components ───────────────────────────────────────────────────
def section(title, body, id_=None, alt=False, more=None, intro=None, narrow=False):
    head = ""
    if title:
        link = f'<a class="more" href="{more[0]}">{more[1]} {CHEV}</a>' if more else ""
        head = f'<div class="section__head"><h2 class="section__title">{title}</h2>{link}</div>' + (f'<p class="section__intro">{intro}</p>' if intro else "")
    return f'<section class="section{" section--alt" if alt else ""}"{f" id=\"{id_}\"" if id_ else ""}><div class="wrap{" wrap--narrow" if narrow else ""}">{head}{body}</div></section>\n'

def page_head(title, sub=None):
    return f'<div class="page-head"><h1 class="page-title">{title}</h1>{f"<p class=\"page-sub\">{sub}</p>" if sub else ""}</div>'

def textlinks(pairs):
    return "".join(f'<a href="{esc_attr(u)}" target="_blank" rel="noopener">{l} {CHEV}</a>' for l, u in pairs if u)

def bullets(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def entry(e, level=3):
    logo = f'<img src="static/media/{e["logo"]}" alt="" width="48" height="48" loading="lazy" decoding="async" />' if e.get("logo") else f'<span class="mono">{e.get("mono", "")}</span>'
    meta = " &middot; ".join(x for x in [e.get("dates", ""), e.get("place", "")] if x)
    org = e["org"] + (f' &middot; {e["kind"]}' if e.get("kind") else "")
    desc = f'<p class="row__desc">{e["desc"]}</p>' if e.get("desc") else ""
    return f'<li class="row row--entry"><span class="row__logo">{logo}</span><div class="row__body"><h{level} class="row__title">{e["title"]}</h{level}><p class="row__sub">{org}</p><p class="row__meta">{meta}</p>{desc}</div></li>'

def entries(items, level=3):
    return '<ul class="rows">' + "".join(entry(e, level) for e in items) + "</ul>"

def pub_meta(p, with_tags=False):
    parts = [p["venue"]]
    if p["track"] in TRACK_LABEL and p["track"] not in ("journal",): parts.append(TRACK_LABEL[p["track"]])
    for b in p["badges"]:
        if b["kind"] == "core": parts.append("CORE A*")
        elif b["kind"] == "award": parts.append(f'<span class="row__award">{b["text"]}</span>')
        elif b["kind"] not in ("main", "wip"): parts.append(b["text"])
        elif b["kind"] == "wip" and p["track"] != "workshop": parts.append(b["text"])
    if p.get("cited"): parts.append(f'Cited {p["cited"]}')
    if with_tags: parts.append(", ".join(p["tags"]))
    return " &middot; ".join(parts)

def pub_item(p, level=3):
    links = [(LINK_LABEL[k], u) for k, u in (p.get("links") or {}).items() if u and k in LINK_LABEL]
    return f"""<li class="row row--pub" data-year="{p["year"]}" data-track="{p["track"]}" data-topic="{' '.join(p["topics"])}">
  <div class="row__body">
    <h{level} class="row__title"><a href="papers/{p["slug"]}.html">{p["title"]}</a></h{level}>
    <p class="row__sub">{p["authors"]}</p>
    <p class="row__meta">{pub_meta(p)}</p>
    <p class="row__links">{textlinks(links)}<button type="button" class="copy-bib" data-bib="{esc_attr(bibtex(p))}">BibTeX</button></p>
  </div>
</li>
"""

def news_row(n, with_year=True):
    label = NEWS_LABEL.get(n.get("kind", "update"), "Update") + (f' &middot; {n["year"]}' if with_year else "")
    return f'<li class="row row--news{" row--featured" if n.get("featured") else ""}"><span class="row__kicker">{label}</span><p class="row__text">{n["text"]}</p></li>'

def system_tile(x):
    links = [(LINK_LABEL[k], u) for k, u in x["links"].items() if u and k in LINK_LABEL and not u.endswith(".html")]
    return f'<li class="tile"><h3 class="tile__title">{x["name"]}</h3><p class="tile__desc">{x["description"]}</p><p class="tile__meta">{x["venue"]}</p><p class="row__links">{textlinks(links)}</p></li>'

def honour_row(h, with_year=True):
    year = h["when"] or (str(h["year"]) if h["year"] else "")
    label = HON_LABEL[h["kind"]] + (f" &middot; {year}" if with_year and year else "")
    return f'<li class="row row--news{" row--featured" if h.get("featured") else ""}"><span class="row__kicker">{label}</span><p class="row__text">{h["text"]}</p></li>'

def collab_list():
    import collections
    counts = collections.Counter()
    for p in PUBS:
        plain = re.sub(r"\s*\(\*Equal Contributions?\)", "", re.sub(r"<[^>]+>", "", p["authors"])).replace("&amp;", "&").replace("*", "")
        for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&\s", plain): counts[a.strip()] += 1
    items = ""
    for c in COLLAB:
        n = counts.get(c["match"], 0); joint = f' &middot; {n} joint paper{"s" if n != 1 else ""}' if n and c["match"] != "Chakraborty, S." else ""
        name = f'<a href="{c["url"]}" target="_blank" rel="noopener">{c["name"]}</a>' if c["url"] else c["name"]
        items += f'<li><p class="row__title">{name}</p><p class="row__meta">{c["role"]} &middot; {c["org"]}{joint}</p></li>'
    return f'<ul class="grid grid--2 grid--tight">{items}</ul>'

def link_list():
    return "".join(f'<a href="{esc_attr(l["url"])}"{"" if l["url"].startswith("mailto:") else " target=\"_blank\" rel=\"noopener\""}>{l["label"]} {CHEV}</a>' for l in P["links"])

# ── index ────────────────────────────────────────────────────────
def build_index():
    docs = [(d["label"], d["file"]) for d in P.get("documents", []) if d.get("file")]
    hero = f"""<section class="hero"><div class="wrap wrap--narrow">
  <img src="static/media/profile.jpg" alt="Garvit Chugh" class="hero__photo" width="176" height="176" fetchpriority="high" />
  <h1 class="hero__name" id="name">{P.get("honorific", "")} {P["name"]}</h1>
  <p class="hero__role">{P["headline"]}</p>
  <p class="hero__tag">{P["tagline"]}</p>
  <p class="hero__now">{P["now"]}</p>
  <p class="hero__affil">{"".join(f'<a href="{a["url"]}" target="_blank" rel="noopener"><img src="static/media/{a["logo"]}" alt="" width="22" height="22" />{a["name"]}</a>' for a in P["affiliations"])}</p>
  <p class="hero__actions"><a class="btn" href="mailto:{P["email"]}">Email me</a><a class="textlink" href="static/media/Garvit_Resume.pdf" target="_blank" rel="noopener">Download CV {CHEV}</a><a class="textlink" href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar {CHEV}</a></p>
</div></section>
"""
    about = section("About", f'<div class="prose">{"".join(f"<p>{p}</p>" for p in P["about"])}</div><p class="section__note">{" &middot; ".join(P["interests"])}</p>', "about", alt=True, narrow=True)
    latest = section("Latest", '<ul class="rows">' + "".join(news_row(n) for n in NEWS[:6]) + "</ul>", "news", more=("news.html", f"All {len(NEWS)} updates"), narrow=True)
    research = section("Research", '<ul class="grid grid--4">' + "".join(f'<li class="tile"><span class="tile__glyph" aria-hidden="true">{r["icon"]}</span><h3 class="tile__title">{r["title"]}</h3><p class="tile__desc">{r["description"]}</p></li>' for r in RESEARCH) + "</ul>", "research", alt=True)
    systems = section("Systems I built", '<ul class="grid grid--2">' + "".join(system_tile(x) for x in SYSTEMS[:2]) + "</ul>", "systems", more=("education.html#systems", f"All {len(SYSTEMS)} systems"))
    pubs = section("Selected publications", '<ul class="rows">' + "".join(pub_item(p) for p in PUBS if p.get("selected")) + "</ul>", "publications", alt=True, more=("publications.html", f"All {N_PUBS} publications"), narrow=True)
    exp = (section("Experience", entries(EXPERIENCE[:3]), "experience", more=("education.html", f"All {len(EXPERIENCE)} roles"), narrow=True)
           + section("Education", entries(EDUCATION), "education", alt=True, more=("education.html#education", "Coursework &amp; teaching"), narrow=True))
    hon = section("Honours", '<ul class="rows">' + "".join(honour_row(h) for h in HONOURS if h["featured"]) + "</ul>", "honours", more=("awards.html", f"All {len(HONOURS)} honours"), narrow=True)
    work = section("Work with me", f'<div class="prose"><p>{P["work_with_me"]}</p></div><p class="hero__actions hero__actions--left"><a class="btn" href="mailto:{P["email"]}">Email me</a>{"".join(f"<a class=\"textlink\" href=\"{u}\" target=\"_blank\" rel=\"noopener\">{l} {CHEV}</a>" for l, u in docs)}</p><h3 class="subhead subhead--sm">Collaborators</h3>{collab_list()}', "work-with-me", alt=True, narrow=True)
    info = section("", f"""<div class="grid grid--4 info">
  <div><h3 class="info__title">Skills</h3><p class="info__text">{", ".join(P["skills"])}</p></div>
  <div><h3 class="info__title">Languages</h3>{bullets(P["languages"], "info__list")}</div>
  <div><h3 class="info__title">Service</h3>{bullets(P["service_short"], "info__list")}</div>
  <div><h3 class="info__title">Links</h3><p class="info__links">{link_list()}</p></div>
</div>""", "contact")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": P["name"], "honorificPrefix": P.get("honorific", ""), "url": SITE + "/",
        "image": f"{SITE}/static/media/profile.jpg", "email": f"mailto:{P['email']}", "jobTitle": "Postdoctoral Researcher",
        "worksFor": {"@type": "Organization", "name": "Singapore Management University"},
        "alumniOf": [{"@type": "Organization", "name": "Indian Institute of Technology Jodhpur"}, {"@type": "Organization", "name": "Guru Gobind Singh Indraprastha University"}],
        "sameAs": [l["url"] for l in P["links"] if not l["url"].startswith("mailto:")],
        "knowsAbout": ["Earable Computing", "Wearable Sensing", "Human-Computer Interaction", "Mobile and Pervasive Computing", "Ubiquitous Computing", "Human-Centered AI"]}, indent=1)
    return shell("Garvit Chugh", "Postdoctoral Researcher at Singapore Management University. Ph.D. from IIT Jodhpur. Research in earable and wearable sensing, human-computer interaction, and pervasive computing.",
                 "", "index.html", hero + about + latest + research + systems + pubs + exp + hon + work + info, extra_head=f'  <script type="application/ld+json">{jsonld}</script>\n', ogtype="profile")

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

TRACKS = [("main", "Main track"), ("workshop", "Workshop / WiP"), ("journal", "Journal"), ("patent", "Patent"), ("review", "Under review")]
TOPICS = [("sensing", "Sensing"), ("healthcare", "Healthcare"), ("hci", "HCI"), ("mlai", "ML / AI"), ("security", "Security"), ("systems", "Systems")]


def build_publications():
    years = []
    for p in PUBS:
        if p["year"] not in years: years.append(p["year"])
    def label_year(y): return "Under review" if y == "review" else "Patent" if y == "patent" else y
    def select(id_, label, options):
        opts = "".join(f'<option value="{v}">{t}</option>' for v, t in options)
        return f'<label class="select"><span>{label}</span><select id="{id_}" aria-label="{label}"><option value="all">All</option>{opts}</select></label>'
    toolbar = select("yearSelect", "Year", [(y, label_year(y)) for y in years]) + select("trackSelect", "Track", TRACKS) + select("topicSelect", "Topic", TOPICS) + '<button type="button" class="textlink" id="resetFilters" hidden>Reset</button>'
    stats = f"""<ul class="stats"><li><strong>{N_PUBS}</strong><span>Publications</span></li><li><strong>{N_PEER}</strong><span>Peer-reviewed</span></li><li><strong>{CITES_TOTAL}</strong><span>Citations</span></li><li><strong>{H_INDEX if H_INDEX is not None else "&ndash;"}</strong><span>h-index</span></li></ul>
<p class="section__note">Citation counts from <a href="{OPENALEX["author"].get("openalex_id", "https://openalex.org")}" target="_blank" rel="noopener">OpenAlex</a>; Google Scholar usually reads higher. CORE A* marks a top-tier venue; * marks equal contribution. Full record on <a href="https://scholar.google.com/citations?user=15XfuxMAAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar</a>, <a href="https://dblp.org/pid/302/5075" target="_blank" rel="noopener">DBLP</a> and <a href="https://orcid.org/0000-0002-0354-9731" target="_blank" rel="noopener">ORCID</a>.</p>"""
    groups = "".join(f'<h2 class="group" data-year-heading="{y}">{label_year(y)}</h2>\n<ul class="rows">\n' + "".join(pub_item(p) for p in PUBS if p["year"] == y) + "</ul>\n" for y in years)
    body = f"""<section class="section section--first"><div class="wrap wrap--narrow">
  {page_head("Publications", PUB_SUMMARY)}
  {stats}
  <div class="toolbar">{toolbar}<span class="filter-count" id="filterCount" aria-live="polite"></span></div>
  <p class="no-results" id="noResults" role="status" hidden>No publications match the selected filters.</p>
  <div id="pubContainer">
{groups}  </div>
</div></section>
<script>
  const selects = {{ year: document.getElementById('yearSelect'), track: document.getElementById('trackSelect'), topic: document.getElementById('topicSelect') }};
  const items = document.querySelectorAll('.row--pub'); const countEl = document.getElementById('filterCount'); const noResults = document.getElementById('noResults'); const reset = document.getElementById('resetFilters');
  function applyFilters() {{
    const f = {{ year: selects.year.value, track: selects.track.value, topic: selects.topic.value }}; let visible = 0;
    items.forEach(item => {{ const show = (f.year === 'all' || item.dataset.year === f.year) && (f.track === 'all' || item.dataset.track === f.track) && (f.topic === 'all' || item.dataset.topic.split(' ').includes(f.topic)); item.hidden = !show; if (show) visible++; }});
    document.querySelectorAll('[data-year-heading]').forEach(h => {{ const any = Array.from(items).some(i => i.dataset.year === h.dataset.yearHeading && !i.hidden); h.hidden = !any; h.nextElementSibling.hidden = !any; }});
    const filtered = Object.values(f).some(v => v !== 'all'); countEl.textContent = filtered ? `Showing ${{visible}} of ${{items.length}}` : ''; reset.hidden = !filtered; noResults.hidden = visible !== 0;
  }}
  Object.values(selects).forEach(sel => sel.addEventListener('change', applyFilters));
  reset.addEventListener('click', () => {{ Object.values(selects).forEach(sel => sel.value = 'all'); applyFilters(); }});
</script>"""
    def article(p):
        names = [re.sub(r"[*]", "", a.strip()) for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&amp;\s|\s&\s", re.sub(r"\s*\(\*Equal Contributions?\)", "", re.sub(r"<[^>]+>", "", p["authors"]))) if a.strip()]
        d = {"@type": "ScholarlyArticle", "headline": re.sub(r"<[^>]+>", "", p["title"]).replace("&amp;", "&"), "author": [{"@type": "Person", "name": n} for n in names],
             "isPartOf": {"@type": "Periodical" if p["track"] == "journal" else "Event", "name": p["venue"].replace("&amp;", "&")}, "url": f"{SITE}/papers/{p['slug']}.html"}
        if p["year"].isdigit(): d["datePublished"] = p["year"]
        if p.get("url"): d["sameAs"] = p["url"]
        return d
    ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Publications by Garvit Chugh", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": article(p)} for i, p in enumerate(PUBS) if p["track"] != "review"]}, ensure_ascii=False)
    return shell("Publications - Garvit Chugh", f"{PUB_SUMMARY} Research by Garvit Chugh at CHI, PerCom, SenSys, PACMHCI, CIKM, ICDM and more.", "publications.html", "publications.html", body, extra_head=f'  <script type="application/ld+json">{ld}</script>\n')

# ── news ─────────────────────────────────────────────────────────
def build_news():
    years = sorted({n["year"] for n in NEWS}, reverse=True)
    jump = " &middot; ".join(f'<a href="#y{y}">{y}</a>' for y in years)
    groups = "".join(f'<h2 class="group" id="y{y}">{y}</h2>\n<ul class="rows">' + "".join(news_row(n, with_year=False) for n in NEWS if n["year"] == y) + "</ul>\n" for y in years)
    body = f'<section class="section section--first"><div class="wrap wrap--narrow">{page_head("News", f"{len(NEWS)} updates, newest first. {jump}")}{groups}</div></section>'
    return shell("News - Garvit Chugh", "Latest news and updates from Garvit Chugh.", "news.html", "news.html", body)

# ── experience & education ───────────────────────────────────────
def build_education():
    labs = "".join(f'<li class="row row--entry"><span class="row__logo"><img src="static/media/{l["logo"]}" alt="" width="48" height="48" loading="lazy" decoding="async" /></span><div class="row__body"><h3 class="row__title"><a href="{l["url"]}" target="_blank" rel="noopener">{l["name"]}</a></h3><p class="row__sub">{l["org"]}</p><p class="row__meta">{l["role"]} &middot; {l["years"]}</p></div></li>' for l in LABS)
    body = (f'<section class="section section--first"><div class="wrap wrap--narrow">{page_head("Experience")}<h2 class="subhead">Current &amp; past roles</h2>{entries(EXPERIENCE)}</div></section>'
            + section("Education", entries(EDUCATION) + '<h3 class="subhead subhead--sm">Graduate coursework</h3><div class="grid grid--2 grid--tight">'
                      + "".join(f'<div><p class="info__title">{c["area"]}</p><p class="info__text">{", ".join(c["courses"])}</p></div>' for c in COURSEWORK) + "</div>", "education", alt=True, narrow=True)
            + section("Labs I have been a part of", f'<ul class="rows">{labs}</ul>', "labs", narrow=True)
            + section("Systems I built", '<ul class="grid grid--3">' + "".join(system_tile(x) for x in SYSTEMS) + "</ul>", "systems", alt=True, intro=f"{len(SYSTEMS)} sensing systems and tools, from prototype to user study. Each links to its paper; code and video links appear as they are released.")
            + section("Teaching", '<h3 class="subhead subhead--sm">IIT Jodhpur</h3>' + bullets(TEACHING) + '<h3 class="subhead subhead--sm">PMRF outreach &amp; external teaching</h3>' + bullets(OUTREACH), "teaching", narrow=True)
            + section("Mentorship", bullets(MENTORSHIP) + '<h3 class="subhead subhead--sm">Skills &amp; languages</h3>' + bullets(SKILLS_FULL), "mentorship", alt=True, narrow=True))
    return shell("Experience - Garvit Chugh", "Experience, education, labs, systems, teaching, and mentorship of Garvit Chugh.", "education.html", "education.html", body)

# ── honours ──────────────────────────────────────────────────────
def build_awards():
    years = sorted({h["year"] for h in HONOURS if h["year"]}, reverse=True)
    groups = "".join(f'<h2 class="group" id="h{y}">{y}</h2>\n<ul class="rows">' + "".join(honour_row(h, with_year=False) for h in HONOURS if h["year"] == y) + "</ul>\n" for y in years)
    n_awards = sum(h["source"] == "awards" for h in HONOURS); n_fund = len(HONOURS) - n_awards
    body = (f'<section class="section section--first"><div class="wrap wrap--narrow">{page_head("Honours &amp; awards", f"{len(HONOURS)} in total: {n_awards} honours and {n_fund} fellowships and grants, newest first.")}{groups}</div></section>'
            + section("Community service", bullets(SERVICE), "service", alt=True, narrow=True))
    return shell("Honours - Garvit Chugh", "Honours, awards, fellowships, grants, and professional service of Garvit Chugh.", "awards.html", "awards.html", body)

# ── one page per paper (Google Scholar indexes these) ────────────
def build_paper(p):
    plain_title = re.sub(r"<[^>]+>", "", p["title"]).replace("&amp;", "&")
    plain_authors = re.sub(r"\s*\(\*Equal Contributions?\)", "", re.sub(r"<[^>]+>", "", p["authors"])).replace("&amp;", "&").replace("*", "")
    names = [a.strip() for a in re.split(r",\s(?=[A-Z][A-Za-z'\-]+,)|\s&\s", plain_authors) if a.strip()]
    year = p["year"] if p["year"].isdigit() else ("2025" if p["year"] == "patent" else "2026")
    venue = p["venue"].replace("&amp;", "&"); links = p.get("links") or {}
    meta = [("citation_title", plain_title), ("citation_publication_date", year), ("citation_journal_title" if p["track"] == "journal" else "citation_conference_title", venue)] + [("citation_author", n) for n in names]
    if p.get("url") and "doi.org/" in p["url"]: meta.append(("citation_doi", p["url"].split("doi.org/")[1]))
    if links.get("pdf"): meta.append(("citation_pdf_url", links["pdf"]))
    meta_html = "".join(f'  <meta name="{k}" content="{esc_attr(v)}" />\n' for k, v in meta)
    actions = textlinks([(LINK_LABEL[k], u) for k, u in links.items() if u and k in LINK_LABEL]) + f'<button type="button" class="copy-bib" data-bib="{esc_attr(bibtex(p))}">Copy BibTeX</button>'
    abstract = f'<h2 class="subhead">Abstract</h2><div class="prose"><p>{p["abstract"]}</p></div>' if p.get("abstract") else ""
    related = [q for q in PUBS if q is not p and set(q["topics"]) & set(p["topics"])][:4]
    related_html = ('<h2 class="subhead">Related</h2><ul class="list">' + "".join(f'<li><a href="papers/{q["slug"]}.html">{q["title"]}</a> <span class="muted">&middot; {q["venue"]}</span></li>' for q in related) + "</ul>") if related else ""
    ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": plain_title, "author": [{"@type": "Person", "name": n} for n in names], "datePublished": year,
          "isPartOf": {"@type": "Periodical" if p["track"] == "journal" else "Event", "name": venue}, "url": f"{SITE}/papers/{p['slug']}.html"}
    if p.get("url"): ld["sameAs"] = p["url"]
    if p.get("abstract"): ld["abstract"] = p["abstract"]
    body = f"""<section class="section section--first"><div class="wrap wrap--narrow">
  <p class="crumb"><a href="publications.html">Publications</a> {CHEV} {p["venue"]}</p>
  <h1 class="page-title">{p["title"]}</h1>
  <p class="paper__authors">{p["authors"]}</p>
  <p class="row__meta">{pub_meta(p, with_tags=True)}</p>
  <p class="row__links row__links--lg">{actions}</p>
  {abstract}
  <h2 class="subhead">BibTeX</h2>
  <pre class="bibtex" tabindex="0" role="region" aria-label="BibTeX entry">{bibtex(p).replace("&", "&amp;").replace("<", "&lt;")}</pre>
  {related_html}
</div></section>"""
    desc = (p.get("abstract") or f"{plain_title}. {plain_authors}. {venue}.")[:300].rsplit(" ", 1)[0]
    return shell(f"{plain_title} - Garvit Chugh", esc_attr(desc), f"papers/{p['slug']}.html", "publications.html", body,
                 extra_head=meta_html + f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n', ogtype="article")

def build_redirect(target, note):
    """Static stub for a URL that used to exist. GitHub Pages cannot issue a 301,
    so this pairs a canonical tag (what crawlers follow) with a meta refresh and a
    scripted replace (what browsers follow)."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Redirecting to {target or "the homepage"}</title>
  <link rel="canonical" href="{SITE}/{target}" />
  <meta name="robots" content="noindex, follow" />
  <meta http-equiv="refresh" content="0; url=/{target}" />
  <script>location.replace('/{target}');</script>
</head>
<body><p>{note} This page has moved to <a href="/{target}">{SITE}/{target}</a>.</p></body>
</html>
"""

def build_404():
    return shell("Page not found - Garvit Chugh", "This page does not exist.", "404.html", "", f'<section class="section section--first"><div class="wrap wrap--narrow notfound"><h1 class="page-title">404</h1><p class="page-sub">This page doesn&rsquo;t exist.</p><p class="hero__actions"><a class="btn" href="index.html">Back to home</a></p></div></section>')

def build_rss():
    import html as _h
    items = ""
    for n in NEWS:
        text = _h.unescape(re.sub(r"<[^>]+>", "", n["text"]))
        items += f"    <item><title>{_h.escape(text[:120])}</title><link>{SITE}/news.html#y{n['year']}</link><guid isPermaLink=\"false\">news-{n['id']}</guid><pubDate>{n['year']}-01-01</pubDate><description>{_h.escape(text)}</description></item>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Garvit Chugh: news</title><link>{SITE}/news.html</link><description>Updates from Garvit Chugh</description>\n{items}</channel></rss>\n'

SOURCES = {  # which data files decide when a page last genuinely changed
 "": ["profile", "news", "research", "systems", "publications", "experience", "education", "honours", "collaborators"],
 "publications.html": ["publications", "openalex"],
 "news.html": ["news"],
 "education.html": ["experience", "education", "labs", "systems", "teaching", "outreach", "mentorship", "skills", "coursework"],
 "awards.html": ["honours", "service"],
}
def last_changed(names):
    """Newest commit date across the given data files, so lastmod reflects content,
    not the moment the build ran. Falls back to today outside a git checkout."""
    import subprocess
    dates = []
    for n in names:
        try:
            d = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--", f"data/{n}.json"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
            if d: dates.append(d)
        except Exception: pass
    return max(dates) if dates else TODAY

def build_sitemap():
    pages = [("", "1.0"), ("publications.html", "0.9"), ("news.html", "0.8"), ("education.html", "0.7"), ("awards.html", "0.7")] + [(f"papers/{p['slug']}.html", "0.6") for p in PUBS]
    cache = {k: last_changed(v) for k, v in SOURCES.items()}
    paper_date = cache["publications.html"]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{cache.get(p, paper_date)}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

if __name__ == "__main__":
    out = {"index.html": build_index(), "publications.html": build_publications(), "news.html": build_news(),
           "education.html": build_education(), "awards.html": build_awards(), "404.html": build_404(), "sitemap.xml": build_sitemap(), "news.xml": build_rss(),
           "index_orig.html": build_redirect("", "The old single-page site has been replaced."),
           "papers/index.html": build_redirect("publications.html", "Individual paper pages are listed on the publications page.")}
    (ROOT / "papers").mkdir(exist_ok=True)
    for p in PUBS: out[f"papers/{p['slug']}.html"] = build_paper(p)
    for name, html in out.items():
        if name.endswith(".html"):  # relative page/asset links -> root-relative, so /papers/* resolve the same shell
            html = re.sub(r'((?:href|src)=")(?!(?:https?:|mailto:|#|/|data:))', r'\1/', html)
        (ROOT / name).write_text(html)
    print(f"built {len(out)} files · {PUB_SUMMARY} · {len(NEWS)} news items")
