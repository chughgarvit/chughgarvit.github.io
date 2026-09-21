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
    print(f"openalex: {len(works)} works, {cache['author']['cited_by_count']} citations, h-index {cache['author']['h_index']} -> {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    try: main()
    except Exception as e:
        print("refresh failed:", e, file=sys.stderr); sys.exit(1)
