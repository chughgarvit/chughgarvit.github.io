#!/usr/bin/env python3
"""Refresh data/openalex.json from OpenAlex. Run: python3 refresh.py && python3 build.py

Pulls every work OpenAlex attributes to the author (matched by ORCID): DOI,
open-access PDF, abstract and citation count. build.py merges this cache into
the publication list by title; anything set by hand in data/publications.json
(url, pdf, abstract) wins over the cache. Needs network; build.py does not.
"""
import json, pathlib, re, sys, urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
ORCID = "0000-0002-0354-9731"
MAILTO = "chughgarvit98@gmail.com"  # OpenAlex "polite pool"; identifies the caller, nothing else
OUT = ROOT / "data" / "openalex.json"
SCHOLAR_OUT = ROOT / "data" / "scholar.json"
SCHOLAR_ID = "15XfuxMAAAAJ"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"garvitchugh.com build ({MAILTO})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>", "", s or "").lower())

def abstract_from(inv):
    if not inv: return ""
    words = sorted((pos, w) for w, positions in inv.items() for pos in positions)
    return " ".join(w for _, w in words)

def scholar():
    """Headline metrics from the public Google Scholar profile. Scholar has no API
    and rate-limits scrapers, so a failure keeps the previous values rather than
    wiping them; the site shows the date they were last confirmed."""
    import datetime, html as _h
    url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        page = r.read().decode("utf-8", "replace")
    vals = re.findall(r'class="gsc_rsb_std">(\d+)</td>', page)
    if len(vals) < 6:
        raise RuntimeError("Scholar returned no metrics table (likely rate-limited)")
    works = [{"title": _h.unescape(t), "cited_by_count": int(c or 0), "year": y or None}
             for t, c, y in re.findall(r'class="gsc_a_t"><a[^>]*>([^<]*)</a>.*?class="gsc_a_c"><a[^>]*>(\d*)</a>.*?class="gsc_a_y">.*?>(\d*)<', page, re.S)]
    data = {"profile_url": url, "fetched": datetime.date.today().isoformat(),
            "cited_by_count": int(vals[0]), "h_index": int(vals[2]), "i10_index": int(vals[4]),
            "works_count": len(works), "works": works}
    SCHOLAR_OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"scholar: {data['cited_by_count']} citations, h-index {data['h_index']}, i10 {data['i10_index']}, {len(works)} works -> {SCHOLAR_OUT.relative_to(ROOT)}")

def main():
    author = get(f"https://api.openalex.org/authors/https://orcid.org/{ORCID}?mailto={MAILTO}")
    aid = author["id"].rsplit("/", 1)[-1]
    works, cursor = [], "*"
    while cursor:
        page = get(f"https://api.openalex.org/works?filter=author.id:{aid}&per-page=100&cursor={cursor}&mailto={MAILTO}")
        works += page["results"]; cursor = page["meta"].get("next_cursor")
    cache = {"author": {"openalex_id": author["id"], "works_count": author.get("works_count"), "cited_by_count": author.get("cited_by_count"),
                        "h_index": (author.get("summary_stats") or {}).get("h_index"), "i10_index": (author.get("summary_stats") or {}).get("i10_index")},
             "works": {}}
    for w in works:
        loc = w.get("primary_location") or {}; oa = w.get("open_access") or {}
        cache["works"][norm(w.get("title"))[:40]] = {
            "title": w.get("title"), "doi": w.get("doi"), "year": w.get("publication_year"), "cited_by_count": w.get("cited_by_count", 0),
            "oa_url": oa.get("oa_url"), "landing": loc.get("landing_page_url"), "pdf": loc.get("pdf_url"),
            "abstract": abstract_from(w.get("abstract_inverted_index")), "openalex_id": w.get("id")}
    OUT.write_text(json.dumps(cache, indent=1, ensure_ascii=False) + "\n")
    try: scholar()
    except Exception as e: print(f"scholar: kept previous values ({e})", file=sys.stderr)
    print(f"openalex: {len(works)} works, {cache['author']['cited_by_count']} citations, h-index {cache['author']['h_index']} -> {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print("refresh failed:", e, file=sys.stderr); sys.exit(1)
