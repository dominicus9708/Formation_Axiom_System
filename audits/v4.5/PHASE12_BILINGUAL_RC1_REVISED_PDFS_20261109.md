# Formation Axiom System v4.5 — Phase 12: first bilingual manuscript revision

**Date:** 2026-11-09. **Author:** Kwon Dominicus.  
**Status:** `BILINGUAL_CANDIDATE_TEX_AND_PDF_COMPILED / PUBLISHED_ORIGINALS_UNMODIFIED / EDITORIAL_FINAL_APPROVAL_OPEN`.

## Basis and source custody

Unlike the earlier Phase 10 smoke tests, this pass operated directly on **the actual user-supplied complete original RC1 source files**, not a re-created PDF-derived TeX source:

- English supplied `DSD_Formation_Axiom_System_EN(10).tex`, 107845 bytes, 2020 source lines, SHA256 `4da4441242d1ade8161ec91e3fca1cb9c8a12270dc8c690af3c73a856c10a1b1`.
- Korean supplied `DSD_Formation_Axiom_System_KR(8).tex`, 111762 bytes, 2066 source lines, SHA256 `e0c06cd74286e03bd38b14e0f300fa73a1627bc0732ae75c452b8cb4cba051b3`.

Their exact content and dimensions match the previously identified 2026-10-22 RC1 manuscript. Originals were copied unchanged for local side-by-side comparison; **Zenodo and previously issued PDFs/TeX were not modified**.

## Exactly three source regions changed per language

1. **Section 2.2:** a compared regime family's material-record signature is held fixed, whereas Section 7's existential construction may select its signature among the witness data.
2. **Section 7.1 proof:** selecting the empty material-record signature is explicitly identified as part of the existential witness; no assertion for every externally fixed annotation codomain has been added.
3. **Data and code availability:** correct Section 4 and 7 references to **Sections 4–7**, qualify the original D2 stage-profile checker and original Proposition 5.14 alternative witness, and point to supplementary source-matched audit records.

Each language's exact unified diff contains **three hunks**. LaTeX theorem/proposition/definition environment delimiters, equation environment delimiters, `label/ref/eqref/cite/bibitem` tokens, and author `Kwon Dominicus` are unchanged. The complete patch instructions and original/candidate SHA256 values are in the local downloadable audit bundle, not added as an unapproved manuscript replacement in the public repository.

## Full original-to-candidate XeLaTeX / PDF regression (performed)

**All four full papers were compiled successfully, twice each with XeLaTeX**: English and Korean originals and their revised candidate files.

| Check | English | Korean |
|---|---|---|
| Original and candidate page counts | 34 → 34 | 30 → 30 |
| Auxiliary reference labels | 13 identical | 13 identical |
| Pages with differences in extracted text | 4,5,25,33,34 | 4,5,23,30 |
| Remaining pages with identical text | 29 | 26 |
| New compile errors/warnings | 0 | 0 |

All warnings seen in the candidate were already present in the corresponding original: English `Underfull hbox` warnings and Korean `UnBatang` italic font-substitution warning. The full PDFs were rendered on their key revised pages and examined for visible text clipping or broken equations. No new page overflow was detected by PDF word-position bounds validation.

### Final candidate integrity

- English candidate TeX SHA256 `98b722ecac8f10ddefd81445100b766a0ae3a1248266fd2dc67422618f7bd7f2`.
- English candidate PDF SHA256 `ff1238ca4426fa5b88128dd479fe216866837fcb336f176d9ab4ee9a688f8fe5`.
- Korean candidate TeX SHA256 `917522a2e3eaed89f74bf3b7762e25de86d14eeaa318d50f3c3938c0085dcddb`.
- Korean candidate PDF SHA256 `88dc29c31e2348415d730ffa91774c7eb56ee59a527ba4f4e59904a8f56de37e`.

The **user-facing downloaded bundle** contains complete *candidate* English/Korean TeX+PDF, language-specific diffs, a SHA-256 source/candidate manifest, full comparison QA, Korean report, and the local deterministic section patch script. The bundle passed a ZIP integrity check.

## Status boundary

**This resolves Phase 10's previously open whole-manuscript compile and line/label regression.** It does not constitute a mathematical formal-proof certificate or publication approval. Phase 11's conditional internal mathematics-audit disposition remains separate. Before republishing, final editorial judgment about the existential quantifier phrasing and code-provenance wording is recommended. Existing public Zenodo records and historical code remain unmodified.

The canonical general non-destructive section patcher and its tests already exist at [`src/apply_formation_phase10_patch.py`](../../src/apply_formation_phase10_patch.py) and [`tests/test_formation_phase10_patch.py`](../../tests/test_formation_phase10_patch.py). The Phase 12 local reproduction bundle also includes a source-anchored variant, with a full source/PDF evidence log, for the exact files uploaded on this date.
