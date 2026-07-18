# staging/

Intermediate, per-course working area between raw PDFs (`sources/`) and the live app data (`docs/data/`). Not committed to git — treat it as scratch space you can regenerate.

```
staging/
  <course-slug>/
    course.config.json     # you write this once, by hand, before drafting cards
    week-01-intro.md       # output of scripts/slides_to_markdown.py
    week-02-topic.md
    draft-cards.json       # LLM-drafted candidate cards, for you to review/edit
```

## 1. `course.config.json`

Defines the course's identity and its own domain/topic taxonomy (there's no auto-classifier here — unlike the AWS CCP app this was forked from, each course's structure is different, so you define it once). Copy `TEMPLATE.course.config.json` from this directory to `staging/<slug>/course.config.json` and fill it in:

```json
{
  "slug": "cpen421",
  "title": "CPEN 421 — Software Engineering",
  "shortLabel": "CPEN 421",
  "domains": [
    { "domain": 1, "title": "Requirements & Design" },
    { "domain": 2, "title": "Testing & Quality" }
  ]
}
```

`domain` numbers just need to be distinct small integers (they render as Roman numerals in the UI, same as the AWS CCP app's 4 exam domains). Each drafted card's `topic` slug should map to one of these domains.

## 2. Drafting cards (agent-assisted step, not a script)

Once `staging/<slug>/*.md` exists (from `slides_to_markdown.py`) and `course.config.json` is filled in, ask an agent session to draft candidate cards from the markdown into `staging/<slug>/draft-cards.json`. Each entry matches the app's `deck.json` card schema — see `TEMPLATE.draft-cards.json` for the shape (`cloze` and `mcq` types, same as the AWS CCP app). Review and edit this file yourself before merging — the draft is a starting point, not a final answer.

## 3. Merging

`python3 scripts/merge_cards.py <slug>` reads `staging/<slug>/draft-cards.json` + `course.config.json` and writes/updates `docs/data/<slug>/deck.json`, `docs/data/<slug>/curriculum.json`, and registers the course in `docs/data/courses.json`. It also bumps `docs/sw.js`'s cache version so the PWA picks up the new content.
