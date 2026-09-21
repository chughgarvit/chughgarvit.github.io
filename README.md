# garvitchugh.com

Static site for Garvit Chugh, served by GitHub Pages from the `gh-pages` branch at https://www.garvitchugh.com.

## Editing content

All content lives in `data/*.json`. The HTML pages are **generated**; do not edit them by hand.

| File | What it holds |
|---|---|
| `data/profile.json` | Name, honorific, headline, tagline, `now` (the status line in the hero), about paragraphs, affiliations, links, skills, languages |
| `data/publications.json` | One object per paper: `year`, `track` (`main` / `workshop` / `journal` / `patent` / `review`), `topics`, `title`, `url`, `authors` (HTML, "Last, F." style, `<strong>` around your name), `venue`, `badges`, `tags`, `selected` (true = shown on the homepage), `links` (`paper`, `pdf`, `code`, `video`) |
| `data/news.json` | One object per update: `id`, `year`, `text` (HTML), `kind` (`paper` / `award` / `grant` / `milestone` / `service` / `talk` / `update`, picks the icon), `featured` (true = ochre bar and Highlights). Newest first. |
| `data/systems.json` | The "Systems I built" grid: `name`, `description`, `kind` (`earable` / `wearable` / `tool`), `venue`, `links` (`paper`, `code`, `video`; empty strings are hidden) |
| `data/experience.json`, `data/education.json`, `data/labs.json` | Roles, degrees, and labs with logo file names |
| `data/facts.json` | The quantified tiles on the homepage; `"number": "auto"` is filled from the publication count |
| `data/honours.json` | One object per honour or grant: `text`, `year`, `when` (display range), `kind` (`award` / `competition` / `fellowship` / `travel` / `scholarship` / `recognition` / `exam` / `talk`), `featured`, `source` (`awards` or `funding`) |
| `data/service.json`, `data/teaching.json`, `data/outreach.json`, `data/mentorship.json`, `data/skills.json` | Plain lists of HTML strings |

Then rebuild and push (run `python3 refresh.py` first to pull DOIs, open-access PDFs, abstracts and citation counts from OpenAlex into `data/openalex.json`; the build itself needs no network):

```
python3 build.py
git add -A && git commit -m "content: ..." && git push origin gh-pages
```

`build.py` derives every count from the data, writes the six pages plus one page per paper under `papers/` (with Google Scholar `citation_*` tags), `sitemap.xml` (with today's date) and `news.xml` (RSS), and generates BibTeX for every paper and ScholarlyArticle structured data for the publications page.

Typography variant: add `data-type="editorial"` to `<html>` (via the `shell()` function in `build.py`) to switch headings to Source Serif 4.

**Adding a paper:** append an object to `data/publications.json` in the right year order. **Adding news:** prepend an object to `data/news.json` with the next `id` and the year it happened.

> If a bot (GitJar or similar) was previously configured to insert HTML into the pages, point it at the JSON files instead. The old HTML anchors no longer exist.

## Assets

- `static/css/site.css`: the only stylesheet (light and dark themes, print styles, phone tab bar).
- `static/fonts/manrope.woff2`: self-hosted variable font.
- `static/media/`: photo, logos (SVG or 128px PNG), resume PDF, social preview image, favicons.

Replace `static/media/Garvit_Resume.pdf` to update the resume link.
