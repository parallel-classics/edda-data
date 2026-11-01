# sources/is/netutgafan/ — Eddic poems in modern spelling (Netútgáfan, 1996–1997)

Fetched 2026-11-01 by the cloud session through a browser from https://netutgafan.snerpa.is/kvaedi/<file> (the site
answers scripts with 403); raw bytes, not edited. Of the ten poem pages there, five are in modern spelling (og, eg,
það, -ur) and fit the Icelandic column:

| File | Poem | Our prefix | Parsed |
| --- | --- | --- | --- |
| `havamal.htm` | Hávamál (six section headings) | hav | `nu_havamal.json` |
| `volospa.htm` | Völuspá (67 stanzas; one of Guðni Jónsson's is split) | vsp | `nu_volospa.json` |
| `tryms2.htm` | Þrymskviða | thrk | `nu_tryms2.json` |
| `volund.htm` | Völundarkviða (with the prose; a different stanza division in places) | vkv | `nu_volund.json` |
| `helg2.htm` | Helgakviða Hundingsbana II | hh2 | `nu_helg2.json` |

Not stored: `grimnir.htm` is Jón Helgason's normalised Old Norse edition (in copyright, not usable at all);
`harbard.htm`, `lokasenn.htm`, `skirnir.htm`, `vafthrud.htm` are an older normalised Old Norse of unstated source
(no use for the Icelandic column). The Netútgáfan pages say "Völuspá er frá Runeberg samtökunum" (the text came via
Project Runeberg).

Terms (netutgafan.snerpa.is/netutgaf.htm): private copying free; whoever puts the material on a website or publishes
it is asked to tell Netútgáfan (netut@snerpa.is). Status 🟡 (edda-internal/SOURCES.md); under the sources policy of
2026-11-01 the text may be shown, labelled "Netútgáfan 1997 · placed automatically", after the notification email.

Pipeline: `edda-site/pipeline/parse_netutgafan.py <htm> <json>` makes the units; `fill_netutgafan.py` places them
on Guðni Jónsson's rows by similarity with the automatic Icelandic (`REPORT.md`: the rows without a counterpart and
the weak pairs, mostly Völundarkviða's different stanza division). Prepared form: row key `is_nu` (+ `is_nu_sim`), not
read by the page. `fill_netutgafan.py --switch` makes it the column (`is` -> `is_auto`, `is_nu` -> `is`,
`is_netutgafan: true`); `--unswitch` reverses it (the takedown switch).
