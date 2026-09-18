# garvitchugh.com

Static site for Garvit Chugh, served by GitHub Pages from the `gh-pages` branch at https://www.garvitchugh.com.

## Editing content

All content lives in `data/*.json`. The HTML pages are **generated**; do not edit them by hand.

| File | What it holds |
|---|---|
| `data/profile.json` | Name, headline, tagline, highlights, affiliations, links, skills, languages |
| `data/publications.json` | One object per paper: `year`, `track` (`main` / `workshop` / `journal` / `patent` / `review`), `topics`, `title`, `url`, `authors` (HTML, "Last, F." style, `<strong>` around your name), `venue`, `badges`, `tags` |
| `data/news.json` | One object per update: `id`, `year`, `text` (HTML). Newest first. |
| `data/experience.json`, `data/education.json` | Roles and degrees with logo file names |
| `data/facts.json` | The quantified tiles on the homepage; `"number": "auto"` is filled from the publication count |
| `data/awards.json`, `data/funding.json`, `data/service.json`, `data/teaching.json`, `data/outreach.json`, `data/mentorship.json`, `data/skills.json` | Plain lists of HTML strings |

Then rebuild and push:

```
python3 build.py
git add -A && git commit -m "content: ..." && git push origin gh-pages
```

`build.py` derives every count (publication totals, "Show all N" links, the hero stats) from the data, writes the six pages, and refreshes `sitemap.xml` with today's date.

**Adding a paper:** append an object to `data/publications.json` in the right year order. **Adding news:** prepend an object to `data/news.json` with the next `id` and the year it happened.

> If a bot (GitJar or similar) was previously configured to insert HTML into the pages, point it at the JSON files instead. The old HTML anchors no longer exist.

## Assets

- `static/css/site.css`: the only stylesheet (light and dark themes, print styles, phone tab bar).
- `static/fonts/manrope.woff2`: self-hosted variable font.
- `static/media/`: photo, logos (SVG or 128px PNG), resume PDF, social preview image, favicons.

Replace `static/media/Garvit_Resume.pdf` to update the resume link.
