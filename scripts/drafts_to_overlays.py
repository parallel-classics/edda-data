"""Convert the AI draft English (auto/en_draft.json) into overlay records.

Writes one overlay file per part under overlays/en/:
  overlays/en/hattatal-ai-draft.json        (row ids h-*)
  overlays/en/skaldskaparmal-ai-draft.json  (row ids s-*)

Every record has status "draft" and author "ai:claude-2026-10"; the "[?]" markers in the text are kept.
Verse rows keep their line breaks as "\n" inside "text".

Usage (from the repository root):
  python -I scripts/drafts_to_overlays.py [auto/en_draft.json] [overlays/en]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART_FILES = {"h": "hattatal-ai-draft.json", "s": "skaldskaparmal-ai-draft.json",
              "g": "gylfaginning-ai-draft.json", "p": "formali-ai-draft.json"}
NOTE = ("AI draft English translation (status draft, author ai:claude-2026-10), one record per row. "
        "Unreviewed; '[?]' marks a rendering the draft itself was unsure of. Verse lines are separated by \\n. "
        "Generated from auto/en_draft.json by scripts/drafts_to_overlays.py; edit by adding newer records, "
        "not by changing these.")


def row_key(rid):
    """Sort key: part letter, chapter number, row number (suffix kept as a string)."""
    p, c, r = rid.split("-", 2)
    num = "".join(ch for ch in r if ch.isdigit())
    return (p, int(c[1:]), int(num) if num else 0, r)


def main(src, out_dir):
    drafts = json.load(open(src, encoding="utf-8"))["rows"]
    by_part = {}
    for rid in sorted(drafts, key=row_key):
        by_part.setdefault(rid[0], []).append({
            "row": rid,
            "cell": "en",
            "text": drafts[rid].strip(),
            "status": "draft",
            "author": "ai:claude-2026-10",
            "date": "2026-10-23",
            "reason": "no public-domain English translation exists",
            "replaces": None,
        })
    os.makedirs(out_dir, exist_ok=True)
    for p, recs in by_part.items():
        path = os.path.join(out_dir, PART_FILES[p])
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_note": NOTE, "records": recs}, f, ensure_ascii=False, indent=1)
            f.write("\n")
        unsure = sum(1 for r in recs if "[?]" in r["text"])
        print(f"{os.path.relpath(path, ROOT)}: {len(recs)} records, {unsure} with [?]")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "auto", "en_draft.json")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "overlays", "en")
    main(src, out)
