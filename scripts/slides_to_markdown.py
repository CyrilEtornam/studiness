#!/usr/bin/env python3
"""Convert a course's lecture-slide PDFs (sources/<slug>/*.pdf) to markdown
(staging/<slug>/*.md) via the `markitdown` CLI. Mechanical step only — no
card drafting happens here, see staging/README.md for that step.

Usage: scripts/slides_to_markdown.py <course-slug>
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: slides_to_markdown.py <course-slug>")

    slug = sys.argv[1]
    src_dir = ROOT / "sources" / slug
    out_dir = ROOT / "staging" / slug

    if not src_dir.is_dir():
        sys.exit(f"No such source folder: {src_dir}")

    pdfs = sorted(src_dir.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs found in {src_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    for pdf in pdfs:
        out_path = out_dir / (pdf.stem + ".md")
        print(f"{pdf.name} -> {out_path.relative_to(ROOT)}")
        result = subprocess.run(
            ["markitdown", str(pdf), "-o", str(out_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  FAILED: {result.stderr.strip()}", file=sys.stderr)

    print(f"\nDone. Converted files are in {out_dir.relative_to(ROOT)}/")
    print("Next: fill in staging/<slug>/course.config.json, then draft cards "
          "into staging/<slug>/draft-cards.json (see staging/README.md).")


if __name__ == "__main__":
    main()
