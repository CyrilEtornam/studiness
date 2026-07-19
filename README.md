# Studiness

Offline-first flashcards, scored quizzes, and reference notes for your own courses. A vanilla-JS PWA — no build step, no framework, no backend.

**App URL (once Pages is enabled — see [Deployment](#deployment-github-pages)):** https://cyriletornam.github.io/studiness/

## What it does

- **Library** — spaced-repetition flashcards (cloze + MCQ) organized by domain/topic, scheduled with the SM-2 algorithm and tracked per-device in `localStorage`.
- **Quiz** — scored, un-timed MCQ runs by domain or a random mix, with score history.
- **Notes** — the original lecture markdown, rendered in-app for offline reference.
- Installable as a PWA; a service worker caches everything for offline use after the first visit.

## Repo layout

```
sources/<course-slug>/     raw lecture-slide PDFs (gitignored — not committed)
staging/<course-slug>/     working area: course.config.json, converted markdown, draft-cards.json (gitignored)
docs/                      the deployed app (GitHub Pages root) + docs/data/<course-slug>/ content
scripts/                   the PDF → markdown → cards pipeline
```

`docs/` is served as-is by GitHub Pages — there's no build/bundle step, so what's in `docs/` is exactly what ships.

## Adding a course

See [`sources/README.md`](sources/README.md) and [`staging/README.md`](staging/README.md) for the full pipeline:

1. Drop PDFs into `sources/<course-slug>/`.
2. `python3 scripts/slides_to_markdown.py <course-slug>` — PDFs → markdown via `markitdown`.
3. Fill in `staging/<course-slug>/course.config.json` (domain/topic taxonomy), then draft `staging/<course-slug>/draft-cards.json` (agent-assisted, human-reviewed).
4. `python3 scripts/merge_cards.py <course-slug>` — merges drafts into `docs/data/<course-slug>/`, registers the course in `docs/data/courses.json`, and bumps the service worker's cache version.

## Deployment (GitHub Pages)

The site is published straight from this repo, no CI build required:

1. **Settings → Pages** on the GitHub repo.
2. **Source:** Deploy from a branch.
3. **Branch:** `master` (or `main`), folder **`/docs`**.
4. Save — GitHub serves `docs/index.html` at the Pages URL above.

To ship a content or code change, just commit and push to the deploy branch — Pages redeploys automatically. Because the service worker caches aggressively, **`scripts/merge_cards.py` bumping `CACHE_VERSION` in `docs/sw.js`** is what makes returning visitors pick up new/changed course data instead of serving a stale cache; bump it manually too if you hand-edit anything under `docs/` without going through the script.

## License

MIT — see [`LICENSE`](LICENSE).
