#!/usr/bin/env python3
"""Merge staging/<slug>/draft-cards.json into the live app data:
docs/data/<slug>/deck.json, curriculum.json, and docs/data/courses.json.
Also bumps docs/sw.js's cache version so the PWA picks up the change.

Usage: scripts/merge_cards.py <course-slug>
"""
import json
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def titleize(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def build_curriculum(cards, domain_titles):
    by_domain = {}
    for c in cards:
        d = by_domain.setdefault(c["domain"], {})
        d.setdefault(c["topic"], 0)
        d[c["topic"]] += 1

    curriculum = []
    for domain_num in sorted(by_domain):
        topics = by_domain[domain_num]
        curriculum.append({
            "domain": domain_num,
            "title": domain_titles.get(domain_num, f"Domain {domain_num}"),
            "count": sum(topics.values()),
            "topics": [
                {"slug": slug, "title": titleize(slug), "count": count}
                for slug, count in sorted(topics.items())
            ]
        })
    return curriculum


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: merge_cards.py <course-slug>")

    slug = sys.argv[1]
    staging_dir = ROOT / "staging" / slug
    config_path = staging_dir / "course.config.json"
    drafts_path = staging_dir / "draft-cards.json"

    if not config_path.exists():
        sys.exit(f"Missing {config_path} — copy staging/TEMPLATE.course.config.json there first.")
    if not drafts_path.exists():
        sys.exit(f"Missing {drafts_path} — draft cards first (see staging/README.md).")

    config = load_json(config_path, {})
    drafts = load_json(drafts_path, [])
    if not drafts:
        sys.exit(f"{drafts_path} is empty — nothing to merge.")

    course_data_dir = ROOT / "docs" / "data" / slug
    deck_path = course_data_dir / "deck.json"
    curriculum_path = course_data_dir / "curriculum.json"
    ref_index_path = course_data_dir / "reference-index.json"
    courses_path = ROOT / "docs" / "data" / "courses.json"

    deck = load_json(deck_path, [])
    existing_ids = {c["id"] for c in deck}

    added = 0
    for card in drafts:
        if "id" not in card or not card["id"]:
            card["id"] = uuid.uuid4().hex[:12]
        if card["id"] in existing_ids:
            continue
        deck.append(card)
        existing_ids.add(card["id"])
        added += 1

    save_json(deck_path, deck)

    domain_titles = {d["domain"]: d["title"] for d in config.get("domains", [])}
    save_json(curriculum_path, build_curriculum(deck, domain_titles))

    if not ref_index_path.exists():
        save_json(ref_index_path, [])

    courses = load_json(courses_path, [])
    entry = {
        "slug": slug,
        "title": config.get("title", slug),
        "shortLabel": config.get("shortLabel", config.get("title", slug))
    }
    existing = next((c for c in courses if c["slug"] == slug), None)
    if existing:
        existing.update(entry)
    else:
        courses.append(entry)
    save_json(courses_path, courses)

    sw_path = ROOT / "docs" / "sw.js"
    sw_text = sw_path.read_text(encoding="utf-8")

    def bump(match):
        return f"CACHE_VERSION = 'studiness-v{int(match.group(1)) + 1}'"

    new_sw_text, n = re.subn(r"CACHE_VERSION = 'studiness-v(\d+)'", bump, sw_text)
    if n:
        sw_path.write_text(new_sw_text, encoding="utf-8")

    print(f"Merged {added} new card(s) into {deck_path.relative_to(ROOT)} ({len(deck)} total).")
    print(f"Updated {curriculum_path.relative_to(ROOT)} and {courses_path.relative_to(ROOT)}.")
    if n:
        print("Bumped docs/sw.js cache version.")


if __name__ == "__main__":
    main()
