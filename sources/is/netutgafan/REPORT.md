# Netútgáfan poems on Guðni Jónsson's rows

## hav — Hávamál: 164 of 164 rows take Netútgáfan text, 0 units left out


## vsp — Völuspá: 66 of 66 rows take Netútgáfan text, 0 units left out


## thrk — Þrymskviða: 32 of 32 rows take Netútgáfan text, 0 units left out


## vkv — Völundarkviða: 41 of 44 rows take Netútgáfan text, 0 units left out

- vkv-p1: no Netútgáfan unit (keeps the automatic text)
- vkv-s14: no Netútgáfan unit (keeps the automatic text)
- vkv-s19: no Netútgáfan unit (keeps the automatic text)

## hh2 — Völsungakviða in forna (Helgakviða Hundingsbana II): 62 of 63 rows take Netútgáfan text, 0 units left out

- hh2-p12: no Netútgáfan unit (keeps the automatic text)


## Rows kept on the automatic text after the switch (2026-11-16, task 25)

Völundarkviða: Netútgáfan divides some stanzas differently from Guðni Jónsson, so lines move to the neighbouring
row and, in s13–s15, repeat on two rows. On these rows Netútgáfan's text would not line up with the Old Norse and
the English, so the cell keeps the automatic modernisation (labelled as such); Netútgáfan's text stays on the row as
`is_nu` for a reader to place by hand:

- vkv-s8, vkv-s9: the line "Kom þar af veiði veðureygur skyti, Völundur líðandi um langan veg" is s8's in Guðni Jónsson, s9's in Netútgáfan
- vkv-s13, vkv-s14, vkv-s15: "Gull var þar eigi á Grana leiðu …" and "man eg að vér meiri mæti áttum …" fall on two rows each
- vkv-s35, vkv-s36: "en úr tönnum tveggja þeirra sló eg brjóstkringlur, senda eg Böðvildi" is s36's in Guðni Jónsson, s35's in Netútgáfan

Kept on Netútgáfan's text although the wording differs from the automatic text: vsp-s11 (Netútgáfan's own reading of
the dwarf names), vkv-s17 (the same lines in a different order). Without any Netútgáfan counterpart (automatic text):
vkv-p1, vkv-s14 (see above), vkv-s19, hh2-p12.

Revert all five poems (the takedown switch): `python -I edda-site/pipeline/fill_netutgafan.py <edda-data> --unswitch
hav=… vsp=… thrk=… vkv=… hh2=…` (the same files as for `--switch`), then rebuild.
