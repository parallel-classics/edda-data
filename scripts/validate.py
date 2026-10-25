"""Validate the edda-data repository and print the status table.

Checks
  aligned/al_*.json   every row has a non-empty Old Norse cell; row ids are unique; chapter numbers unique per part
  overlays/**/*.json  {"records": [...]}; every record: row id exists in aligned/, cell in {on, is, en},
                      status in {auto, draft, reviewed, disputed}, non-empty text, author, date YYYY-MM-DD,
                      "replaces" null or string
  images/records.json every record: unique id, part known, chapter exists, scene_rows (if given) exist, core keys present,
                      "file" (if given) exists in images/pd/; the optional top-level "unfilled" map names existing slots
  images/scenes.json  every chapter key exists in the part

Then prints, per part and column, how many cells are source / auto / draft / reviewed / disputed / empty after
overlays are applied (latest record per row+cell wins; a disputed record marks the cell disputed).

Usage: python -I scripts/validate.py [repo root]      exit code 1 on any error
Standard library only.
"""
import glob
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARTS = [  # row-id prefix, aligned file, "part" value inside the file, scenes.json key, display name
    ("p", "al_prol.json", "prologue", "prologue", "Formáli"),
    ("g", "al_gylf.json", "gylfaginning", "gylfaginning", "Gylfaginning"),
    ("s", "al_skald.json", "skaldskaparmal", "skaldskaparmal", "Skáldskaparmál"),
    ("h", "al_hatt.json", "hattatal", "hattatal", "Háttatal"),
]
CELLS = ("on", "is", "en")
STATUSES = ("auto", "draft", "reviewed", "disputed")
ROW_ID = re.compile(r"^[pgsh]-c\d+-\d+[a-z]?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# images/records.json: these keys must be present; the others in images/README.md are optional
IMAGE_KEYS = ("id", "part", "chapter", "title", "artist", "date", "source_url", "file_url", "width", "height",
              "license_basis", "checked_by", "checked_on", "caption")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def block_text(b):
    return b.get("s", "") if b.get("t") == "p" else " ".join(b.get("l", []))


def check_aligned():
    """Returns {row_id: {"on": bool, "is": bool, "en": bool, "en_draft": bool}} and {prefix: set(chapter nums)}."""
    rows, chapters = {}, {}
    for prefix, fname, part_name, _, _ in PARTS:
        path = os.path.join(ROOT, "aligned", fname)
        if not os.path.exists(path):
            err(f"missing {path}")
            continue
        al = load(path)
        if al.get("part") != part_name:
            err(f"{fname}: part is {al.get('part')!r}, expected {part_name!r}")
        nums = set()
        for c in al.get("chapters", []):
            num = c.get("num")
            if num in nums:
                err(f"{fname}: duplicate chapter number {num}")
            nums.add(num)
            for i, r in enumerate(c.get("rows", []), start=1):
                rid = f"{prefix}-c{num}-{i}"
                if rid in rows:
                    err(f"{fname}: duplicate row id {rid}")
                on = r.get("on") or []
                if not on or not any(block_text(b).strip() for b in on):
                    err(f"{fname}: row {rid} has an empty Old Norse cell")
                rows[rid] = {
                    "on": bool(on),
                    "is": bool(r.get("is")),
                    "en": bool(r.get("en")),
                    "en_draft": bool(r.get("en_draft")),
                }
        chapters[prefix] = nums
    return rows, chapters


def check_overlays(rows):
    """Returns {(row, cell): status} after applying overlays in file order (later records win)."""
    effective = {}
    files = sorted(glob.glob(os.path.join(ROOT, "overlays", "**", "*.json"), recursive=True))
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            doc = load(path)
        except ValueError as e:
            err(f"{rel}: invalid JSON ({e})")
            continue
        recs = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(recs, list):
            err(f"{rel}: expected an object with a \"records\" list")
            continue
        folder_cell = os.path.basename(os.path.dirname(path))
        for k, rec in enumerate(recs):
            where = f"{rel}#{k}"
            rid, cell, status = rec.get("row"), rec.get("cell"), rec.get("status")
            if not isinstance(rid, str) or not ROW_ID.match(rid):
                err(f"{where}: bad row id {rid!r}")
                continue
            base = re.sub(r"[a-z]$", "", rid)  # a suffixed id (split row) must point at an existing base id
            if rid not in rows and base not in rows:
                err(f"{where}: row {rid} does not exist in aligned/")
            if cell not in CELLS:
                err(f"{where}: cell {cell!r} not in {CELLS}")
            elif folder_cell in CELLS and cell != folder_cell:
                err(f"{where}: cell {cell!r} but the file is under overlays/{folder_cell}/")
            if status not in STATUSES:
                err(f"{where}: status {status!r} not in {STATUSES}")
            if not isinstance(rec.get("text"), str) or not rec["text"].strip():
                err(f"{where}: empty text")
            if not isinstance(rec.get("author"), str) or not rec["author"]:
                err(f"{where}: missing author")
            if not isinstance(rec.get("date"), str) or not DATE.match(rec["date"]):
                err(f"{where}: date {rec.get('date')!r} is not YYYY-MM-DD")
            if "replaces" in rec and rec["replaces"] is not None and not isinstance(rec["replaces"], str):
                err(f"{where}: replaces must be null or a string")
            if "reason" in rec and not isinstance(rec["reason"], str):
                err(f"{where}: reason must be a string")
            if rid in rows and cell in CELLS and status in STATUSES:
                key = (rid, cell)
                if status == "disputed" or effective.get(key) == "disputed":
                    effective[key] = "disputed"
                else:
                    effective[key] = status
    return effective, len(files)


def check_images(rows, chapters):
    part_by_name = {name: prefix for prefix, _, name, _, _ in PARTS}
    path = os.path.join(ROOT, "images", "records.json")
    n = 0
    if os.path.exists(path):
        doc = load(path)
        recs = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(recs, list):
            err("images/records.json: expected an object with a \"records\" list")
            recs = []
        ids = set()
        for k, rec in enumerate(recs):
            where = f"images/records.json#{k}"
            missing = [key for key in IMAGE_KEYS if key not in rec]
            if missing:
                err(f"{where}: missing keys {missing}")
            if rec.get("id") in ids:
                err(f"{where}: duplicate id {rec.get('id')!r}")
            ids.add(rec.get("id"))
            prefix = part_by_name.get(rec.get("part"))
            if prefix is None:
                err(f"{where}: unknown part {rec.get('part')!r} (use {sorted(part_by_name)})")
            elif rec.get("chapter") not in chapters.get(prefix, set()):
                err(f"{where}: chapter {rec.get('chapter')!r} does not exist in {rec.get('part')}")
            for rid in rec.get("scene_rows") or []:
                if rid not in rows:
                    err(f"{where}: scene row {rid} does not exist")
            if rec.get("file") and not os.path.exists(os.path.join(ROOT, "images", "pd", rec["file"])):
                err(f"{where}: file images/pd/{rec['file']} not found")
        n = len(recs)
        # density rule (images/README.md): one depiction slot per chapter, at most three documentary images per
        # chapter, about one placed image per twenty rows per part. Warnings only.
        per_ch, per_part = {}, {}
        for rec in recs:
            if not rec.get("placed", True):
                continue
            key = (rec.get("part"), rec.get("chapter"), rec.get("kind", "depiction") == "depiction")
            per_ch[key] = per_ch.get(key, 0) + 1
            per_part[rec.get("part")] = per_part.get(rec.get("part"), 0) + 1
        for (part, ch, is_dep), c in sorted(per_ch.items(), key=str):
            if (is_dep and c > 1) or (not is_dep and c > 3):
                warnings.append(f"images: {part} chapter {ch} has {c} {'depictions' if is_dep else 'documentary images'}")
        for prefix, _, part_name, _, _ in PARTS:
            nrows = sum(1 for r in rows if r.startswith(prefix + "-"))
            if nrows and per_part.get(part_name, 0) > max(3, round(nrows / 20 * 2)):
                warnings.append(f"images: {part_name} has {per_part[part_name]} images for {nrows} rows (at most {round(nrows / 10)})")
        total_rows, total_imgs = len(rows), sum(per_part.values())
        if total_rows and total_imgs > round(total_rows / 20 * 1.1):
            warnings.append(f"images: {total_imgs} placed images for {total_rows} rows (guide: about {round(total_rows / 20)})")
        unfilled = doc.get("unfilled") or {}
        if not isinstance(unfilled, dict):
            err("images/records.json: \"unfilled\" must be an object {slot id: reason}")
        else:
            for slot in unfilled:
                m = re.fullmatch(r"([pgsh])-c(\d+)", slot)
                if not m or int(m.group(2)) not in chapters.get(m.group(1), set()):
                    err(f"images/records.json: unfilled slot {slot!r} is not an existing chapter")
    scenes_path = os.path.join(ROOT, "images", "scenes.json")
    if os.path.exists(scenes_path):
        scenes = load(scenes_path)
        name_to_prefix = {sname: prefix for prefix, _, _, sname, _ in PARTS}
        for sname, chs in scenes.items():
            if sname.startswith("_"):
                continue
            prefix = name_to_prefix.get(sname)
            if prefix is None:
                err(f"images/scenes.json: unknown part key {sname!r}")
                continue
            for ch in chs:
                if int(ch) not in chapters.get(prefix, set()):
                    err(f"images/scenes.json: {sname} chapter {ch} does not exist")
    return n


def status_table(rows, effective):
    cols = ("source", "auto", "draft", "reviewed", "disputed", "empty")
    table = []
    for prefix, _, _, _, display in PARTS:
        for cell in CELLS:
            counts = dict.fromkeys(cols, 0)
            for rid, r in rows.items():
                if rid[0] != prefix:
                    continue
                st = effective.get((rid, cell))
                if st is None:
                    if not r[cell]:
                        st = "empty"
                    elif cell == "on":
                        st = "source"
                    elif cell == "en" and r["en_draft"]:
                        st = "draft"
                    else:
                        st = "auto"
                counts[st] += 1
            table.append((display, cell, counts))
    w = max(len(d) for d, _, _ in table)
    head = f"{'part':<{w}}  col  " + "".join(f"{c:>9}" for c in cols) + "    total"
    print(head)
    print("-" * len(head))
    for display, cell, counts in table:
        total = sum(counts.values())
        print(f"{display:<{w}}  {cell:<4} " + "".join(f"{counts[c]:>9}" for c in cols) + f"  {total:>7}")
    return table


def main():
    rows, chapters = check_aligned()
    effective, n_overlay_files = check_overlays(rows)
    n_images = check_images(rows, chapters)
    print(f"aligned rows: {len(rows)} in {len(chapters)} parts; overlay files: {n_overlay_files}, "
          f"overlay cells: {len(effective)}; image records: {n_images}\n")
    status_table(rows, effective)
    print()
    print("source = base edition text (Old Norse), auto = automatic alignment or modernisation, "
          "draft = unreviewed human or AI text, empty = no text in this cell")
    for w in warnings:
        print("warning: " + w)
    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors[:200]:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    print("\nOK")


if __name__ == "__main__":
    main()
