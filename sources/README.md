# sources/

Drop each course's raw lecture-slide PDFs here, one subfolder per course:

```
sources/
  <course-slug>/
    week-01-intro.pdf
    week-02-topic.pdf
    ...
```

`<course-slug>` should be a short lowercase identifier for the course (e.g. `cpen421`, `discrete-math`) — it becomes the course's slug throughout the app (`docs/data/<course-slug>/`, localStorage keys, `staging/<course-slug>/`).

PDFs themselves are not committed to git (see `.gitignore`) — only this folder structure and its `.gitkeep` markers are tracked, so the convention survives even before a course's PDFs are added.

## Pipeline

1. Drop PDFs into `sources/<course-slug>/`.
2. Run `python3 scripts/slides_to_markdown.py <course-slug>` — converts each PDF to markdown in `staging/<course-slug>/` via `markitdown`.
3. Draft cards from that markdown (LLM-assisted, reviewed by you) into `staging/<course-slug>/draft-cards.json` — see `staging/README.md`.
4. Run `python3 scripts/merge_cards.py <course-slug>` — folds reviewed cards into `docs/data/<course-slug>/deck.json`, updates `curriculum.json` and `docs/data/courses.json`, and bumps the service worker cache version.
