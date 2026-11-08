# Formation Axiom System — Zenodo release-date preparation (2026-11-09)

**Author:** Kwon Dominicus. **Distribution status:** files prepared for **user-operated** Zenodo publication; **not** deposited or published by the assistant.

## Change from the approved full Phase 12 editorial candidate

Exactly one LaTeX date line per language was modified:

- English: `\\date{2026.10.22...}` → `\\date{2026.11.09...}`.
- Korean: `\\date{2026.10.22...}` → `\\date{2026.11.09...}`.

The Phase12 clarifications in §2.2, Theorem 7.1 and Data/code availability are unchanged. The original full source, original published Zenodo record, existing DOI, original historical files, original math proofs and references are unmodified.

## Full regression, not a one-page smoke test

Both **complete** candidates were rebuilt with XeLaTeX twice, against a separately rebuilt prior Phase12 baseline. The PDF extracted first-page printed date is **2026.11.09** in both. The only page with differing extracted text compared with Phase12 is **page 1** in each language. Pages 2–34 (English) and 2–30 (Korean) are text-identical to Phase12.

| Measure | English | Korean |
|---|---:|---:|
| Full page count | 34 | 30 |
| Reference labels | 13 unchanged | 13 unchanged |
| XeLaTeX builds | 2 passes successful | 2 passes successful |
| Warning counts against previous build | identical | identical |
| New undefined reference warnings | 0 | 0 |

The front-page PDF render was checked visually for both languages and displayed the correct date without clipping. All PDF and TeX output bytes have independent SHA256 checksums. The six-file ZIP (4 paper files, release README, SHA256SUMS) passed ZIP integrity and internal checksum validation.

## Release file hashes (SHA256)

| Filename | SHA256 |
|---|---|
| `DSD_Formation_Axiom_System_EN_20261109.tex` | `b5b741f96453da9296bd96de81d35ba825dea726253998e38451f75a10e5ae5a` |
| `DSD_Formation_Axiom_System_EN_20261109.pdf` | `40f322e5da7f7d93739a034042947890e54c2c0ebc7ee1bd351d24863486ba2d` |
| `DSD_Formation_Axiom_System_KR_20261109.tex` | `f2e1843918182b9593c4f0505e0b62d5fb61e9149c9ab94ba56d8111be0f2df3` |
| `DSD_Formation_Axiom_System_KR_20261109.pdf` | `61d7c6520dd4b0c14e5ac66390367653e93db3d9ac2987bf10d2a1cd5478e732` |

## Zenodo upload boundary

User will personally upload the files. Where updating an existing Zenodo record, consider **New version** to preserve version history rather than making a separate unrelated record. Actual Zenodo publication date must be recorded truthfully and need not equal the date printed in the paper. DOI, license, affiliations and other repository metadata must be selected from the actual existing record and author instructions; none were invented or silently changed here.

The **complete release ZIP** and individual full paper PDFs/TeX are conversation download artifacts, not published repository assets. This GitHub report is a process and integrity record only.

**Verdict:** `ZENODO_RELEASE_DATE_SET_TO_2026_11_09 / BILINGUAL_COMPLETE_PDFS_COMPILED_AND_VERIFIED / DATE_ONLY_CHANGE_FROM_PHASE12 / CHECKSUMS_PASS / ZENODO_UPLOAD_NOT_PERFORMED`.
