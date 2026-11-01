"""Validate the edda-data repository and print the status table.

Checks
  aligned/al_*.json   every row has a non-empty Old Norse cell; row ids are unique; chapter numbers unique per part
  aligned/poetic/al_<poem>.json  Poetic Edda: rows carry their own ids <poem>-s<N> / <poem>-p<k>, unique;
                      index.json lists every poem file; links.json: both ends of every link exist
  aligned/titles.json every chapter of Snorri's parts and every poem has a title entry
  overlays/**/*.json  {"records": [...]}; every record: row id exists in aligned/, cell in {on, is, en},
                      status in {auto, draft, reviewed, disputed}, non-empty text, author, date YYYY-MM-DD,
                      "replaces" null or string
  images/records.json every record: unique id, part known, chapter exists, scene_rows (if given) exist, core keys present,
                      "file" (if given) exists in images/pd/; the optional top-level "unfilled" map names existing slots
  images/scenes.json  every chapter key exists in the part
  entities/           (when present) seed.json, rules.json, notable.json, images.json, entities.json, mentions.json:
                      ids are unique slugs, tags are from the vocabulary, Wikidata ids look like Q123, every mention
                      names an existing entity, row and language, every used image passed the licence check

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
LANG_CODES = ("on", "is", "en", "ru", "nb", "nn", "da", "sv", "de")   # possible column languages
CELLS = ("on", "is", "en", "ru", "nb", "nn", "da", "sv", "de")
STATUSES = ("auto", "draft", "reviewed", "disputed")
ROW_ID = re.compile(r"^([pgsh]-c\d+-\d+|[a-z0-9]+-[spv]\d+)[a-z]?$")
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
                rows[rid] = {c: bool(r.get(c)) for c in LANG_CODES}
                rows[rid]["en_draft"] = bool(r.get("en_draft"))
        chapters[prefix] = nums
    # Poetic Edda
    pdir = os.path.join(ROOT, "aligned", "poetic")
    if os.path.isdir(pdir):
        idx = load(os.path.join(pdir, "index.json"))
        listed = {p["file"] for p in idx["poems"]}
        for f in sorted(glob.glob(os.path.join(pdir, "al_*.json"))):
            if os.path.basename(f) not in listed:
                err(f"aligned/poetic/{os.path.basename(f)} is not listed in index.json")
        for p in idx["poems"]:
            path = os.path.join(pdir, p["file"])
            if not os.path.exists(path):
                err(f"aligned/poetic/index.json names a missing file {p['file']}")
                continue
            d = load(path)
            pfx = d.get("poem")
            if pfx != p["prefix"]:
                err(f"{p['file']}: poem {pfx!r} but index says {p['prefix']!r}")
            for c in d["chapters"]:
                for r in c["rows"]:
                    rid = r.get("id", "")
                    if not re.fullmatch(rf"{re.escape(pfx)}-[spv]\d+b?", rid):
                        err(f"{p['file']}: bad row id {rid!r}")
                    if rid in rows:
                        err(f"{p['file']}: duplicate row id {rid}")
                    if not r.get("on"):
                        err(f"{p['file']}: row {rid} has an empty Old Norse cell")
                    rows[rid] = {c2: bool(r.get(c2)) for c2 in LANG_CODES}
                    rows[rid]["en_draft"] = False
                    rows[rid]["poem"] = True
        chapters["poetic"] = {p["prefix"] for p in idx["poems"]}
    return rows, chapters


def check_links(rows, chapters):
    n = 0
    path = os.path.join(ROOT, "aligned", "poetic", "links.json")
    if os.path.exists(path):
        for k, l in enumerate(load(path).get("links", [])):
            n += 1
            if l.get("row") not in rows:
                err(f"aligned/poetic/links.json#{k}: Snorri row {l.get('row')!r} does not exist")
            if l.get("poem_row") not in rows:
                err(f"aligned/poetic/links.json#{k}: poem row {l.get('poem_row')!r} does not exist")
    tpath = os.path.join(ROOT, "aligned", "titles.json")
    if os.path.exists(tpath):
        titles = load(tpath)["titles"]
        want = [f"{p}-ch{c}" for p in "pgsh" for c in sorted(chapters.get(p, set()))] + sorted(chapters.get("poetic", set()))
        miss = [k for k in want if k not in titles]
        if miss:
            err(f"aligned/titles.json: no title for {miss[:10]}")
        for k, t in titles.items():
            if not t.get("on") or not t.get("en"):
                warnings.append(f"titles: {k} lacks an Old Norse or English title")
    return n


def check_overlays(rows):
    """Returns {(row, cell): status} after applying overlays in file order (rule in docs/DATA_MODEL.md; the site
    build applies the same rule in edda-site/pipeline/overlays.py)."""
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
            base = re.sub(r"(?<=\d)[a-z]$", "", rid)  # a suffixed id (split row) must point at an existing base id
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
                # docs/DATA_MODEL.md: an unresolved dispute wins; else the latest reviewed record; else drafts
                key = (rid, cell)
                cur = effective.get(key)
                if status in ("disputed", "reviewed"):
                    effective[key] = status          # a later reviewed record resolves a dispute
                elif status == "draft" and cur not in ("reviewed", "disputed"):
                    effective[key] = "draft"
                elif cur is None:
                    effective[key] = status          # an "auto" record on an untouched cell
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
            for key in ("width", "height", "file_width", "file_height"):
                if key in rec and not (isinstance(rec[key], int) and rec[key] > 0):
                    err(f"{where}: {key} must be a positive integer")
            if ("file_width" in rec) != ("file_height" in rec):
                err(f"{where}: file_width and file_height go together")
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


ENTITY_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ENTITY_TAGS = ("god", "goddess", "giant", "dwarf", "elf", "valkyrie", "norn", "hero", "king", "poet", "animal", "horse",
               "monster", "object", "place_myth", "place_real", "river", "hall", "people", "poem", "event", "character")
SEED_TYPES = ("god", "goddess", "giant", "dwarf", "elf", "valkyrie", "human", "character", "skald", "animal", "monster",
              "object", "place-myth", "place-legend", "place-real", "group", "work", "event", "other")
OK_LICENCE = re.compile(r"^(public domain|pd\b|cc0|cc by(-sa)?(\s|$))", re.I)


def check_entities(rows):
    """entities/: the curated seed, the hand rules and the generated files (edda-site/pipeline/make_entities.py)."""
    d = os.path.join(ROOT, "entities")
    if not os.path.isdir(d):
        return 0, 0
    ids = set()
    seed_path = os.path.join(d, "seed.json")
    if os.path.exists(seed_path):
        seed = load(seed_path)
        for e in seed.get("entities", []):
            where = f"entities/seed.json#{e.get('id')}"
            if not isinstance(e.get("id"), str) or not ENTITY_ID.match(e["id"]):
                err(f"{where}: id must be a lowercase slug")
            elif e["id"] in ids:
                err(f"{where}: duplicate id")
            ids.add(e.get("id"))
            if e.get("type") not in SEED_TYPES:
                err(f"{where}: type {e.get('type')!r} unknown")
            if e.get("wikidata") is not None and not re.match(r"^Q\d+$", str(e["wikidata"])):
                err(f"{where}: wikidata must be null or Q<number>")
            if not isinstance(e.get("names"), dict) or not e["names"]:
                err(f"{where}: names must be a non-empty object")
            if not isinstance(e.get("forms"), dict):
                err(f"{where}: forms must be an object form -> count")
    rules_path = os.path.join(d, "rules.json")
    if os.path.exists(rules_path):
        rules = load(rules_path)
        for e in rules.get("extra", []):
            where = f"entities/rules.json extra {e.get('id')}"
            if not isinstance(e.get("id"), str) or not ENTITY_ID.match(e["id"]):
                err(f"{where}: id must be a lowercase slug")
            elif e["id"] in ids:
                err(f"{where}: id already in seed.json")
            ids.add(e.get("id"))
            if not e.get("tags") or any(t not in ENTITY_TAGS for t in e["tags"]):
                err(f"{where}: tags must be from the vocabulary")
        for eid, tags in rules.get("tags", {}).items():
            if eid not in ids:
                err(f"entities/rules.json tags: unknown entity {eid!r}")
            if not tags or any(t not in ENTITY_TAGS for t in tags):
                err(f"entities/rules.json tags {eid}: tags must be from the vocabulary")
        for eid, rule in rules.get("resolve", {}).get("entities", {}).items():
            if eid not in ids:
                err(f"entities/rules.json resolve.entities: unknown entity {eid!r}")
            for sc, v in rule.items():
                vals = list(v.values()) if isinstance(v, dict) else [v]
                for x in vals:
                    if x not in ("ok", "check") and x not in ids:
                        err(f"entities/rules.json resolve.entities {eid} [{sc}]: unknown target {x!r}")
        for form, rule in rules.get("resolve", {}).get("forms", {}).items():
            for sc, v in rule.items():
                vals = list(v.values()) if isinstance(v, dict) else [v]
                for x in vals:
                    if x not in ("ok", "check", "skip") and x not in ids:
                        err(f"entities/rules.json resolve.forms {form} [{sc}]: unknown target {x!r}")
        for eid, near in rules.get("resolve", {}).get("near", {}).items():
            if eid not in ids:
                err(f"entities/rules.json resolve.near: unknown entity {eid!r}")
            for word, x in near.items():
                if x not in ids:
                    err(f"entities/rules.json resolve.near {eid} {word}: unknown target {x!r}")
        for sc in rules.get("lists", []):
            if not (sc in rows or re.match(r"^[pgsh]-c\d+$", sc) or re.match(r"^[a-z0-9]+$", sc)):
                err(f"entities/rules.json lists: {sc!r} is not a row, chapter or poem scope")
    notable_path = os.path.join(d, "notable.json")
    if os.path.exists(notable_path):
        for eid in load(notable_path).get("ids", []):
            if eid not in ids:
                warnings.append(f"entities/notable.json: {eid!r} is not an entity (yet)")
    images = {}
    images_path = os.path.join(d, "images.json")
    if os.path.exists(images_path):
        images = load(images_path).get("images", {})
        for f, rec in images.items():
            if rec.get("ok") and not OK_LICENCE.match(rec.get("licence") or ""):
                err(f"entities/images.json {f}: marked ok but licence {rec.get('licence')!r} is not PD / CC0 / CC BY / CC BY-SA")
    n_ent = n_men = 0
    ent_path = os.path.join(d, "entities.json")
    if os.path.exists(ent_path):
        doc = load(ent_path)
        seen = set()
        for e in doc.get("entities", []):
            n_ent += 1
            where = f"entities/entities.json#{e.get('id')}"
            if e.get("id") in seen:
                err(f"{where}: duplicate id")
            seen.add(e.get("id"))
            if e.get("id") not in ids:
                err(f"{where}: not in seed.json or rules.json (regenerate)")
            if not e.get("tags") or any(t not in ENTITY_TAGS for t in e["tags"]) or e.get("type") != e["tags"][0]:
                err(f"{where}: tags must be from the vocabulary and type = tags[0]")
            if e.get("status") != "auto":
                err(f"{where}: status must be auto (entities are not reviewed yet)")
            if e.get("image") and not images.get(e["image"], {}).get("ok"):
                err(f"{where}: image {e['image']!r} has not passed the licence check in images.json")
            for book, rid in list((e.get("first") or {}).items()) + list((e.get("first_any") or {}).items()):
                if rid not in rows:
                    err(f"{where}: first mention row {rid!r} does not exist")
        ids_out = seen
    else:
        ids_out = ids
    men_path = os.path.join(d, "mentions.json")
    if os.path.exists(men_path):
        for i, m in enumerate(load(men_path).get("mentions", [])):
            n_men += 1
            if m.get("entity") not in ids_out:
                err(f"entities/mentions.json[{i}]: unknown entity {m.get('entity')!r}")
            if m.get("row") not in rows:
                err(f"entities/mentions.json[{i}]: unknown row {m.get('row')!r}")
            if m.get("lang") not in CELLS:
                err(f"entities/mentions.json[{i}]: unknown lang {m.get('lang')!r}")
            if not m.get("form") or m.get("kind") not in ("name", "heiti", "kenning") or m.get("status") != "auto":
                err(f"entities/mentions.json[{i}]: needs form, kind in name/heiti/kenning, status auto")
    return n_ent, n_men


def status_table(rows, effective):
    cols = ("source", "auto", "draft", "reviewed", "disputed", "empty")
    table = []
    groups = [(prefix, display, lambda rid, p=prefix: rid.split("-")[0] == p) for prefix, _, _, _, display in PARTS]
    groups.append(("poetic", "Poetic Edda", lambda rid: rows[rid].get("poem", False)))
    for prefix, display, member in groups:
        present = [c for c in CELLS if any(rows[r][c] for r in rows if member(r))]
        for cell in present:
            counts = dict.fromkeys(cols, 0)
            for rid, r in rows.items():
                if not member(rid):
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
    n_links = check_links(rows, chapters)
    n_ent, n_men = check_entities(rows)
    print(f"aligned rows: {len(rows)} in {len(chapters)} parts; overlay files: {n_overlay_files}, "
          f"overlay cells: {len(effective)}; image records: {n_images}; quotation links: {n_links}; "
          f"entities: {n_ent}, mentions: {n_men}\n")
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
