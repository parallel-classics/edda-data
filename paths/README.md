# paths/

Reading paths for the website's "Start here" page (task 19a, `edda-site/docs/specs/START_HERE.md`).

`paths.json`: `{"status": {"en": "editor", "is": "draft"}, "paths": [ {id, title, time, steps} ]}`. A step is
`{"ref": <id>, "to": <id>?, "note": {en, is}}` where the ids are chapters (`g-ch1`), poems (`vsp-poem`) or rows
(`g-c12-4`); `to` closes a range of chapters of the same part. Titles come from `aligned/titles.json` at build time;
only the notes live here. The validator checks that every id exists. The Icelandic notes are a draft until a
native reader has checked them (`status.is`); the page says so.
