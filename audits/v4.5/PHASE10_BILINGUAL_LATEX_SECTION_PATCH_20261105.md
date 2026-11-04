# Formation v4.5 — Phase 10 bilingual section-scoped revision candidate and regression status

**Paper author:** Kwon Dominicus  
**Date:** 2026-11-05  
**Printed source:** 2026-10-22, English PDF 34 pages, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.  
**Status:** `PATCH_SCRIPT_VERIFIED / TWO_LANGUAGE_SOURCE_ANCHORS_VERIFIED / TWO_LOCALIZED_SMOKE_PDFS_COMPILED / FULL_PAPER_REBUILD_NOT_PERFORMED`.

## Original source discovery and custody

The complete English and Korean 2026-10-22 RC1 TeX files were located **in the user's Library**:
- `DSD_Formation_Axiom_System_EN_20261022_RC1.tex`, 2,020 lines;
- `DSD_Formation_Axiom_System_KR_20261022_RC1.tex`, 2,066 lines.

The entire indexed text was read in line windows. Three patch anchors per language occur **exactly once** and in source order §2.2, §7.1, Data-and-code declarations. In-memory replacement of only those anchors preserves the number and identity of numbered LaTeX theorem environments, math environments, labels, references, citations and bibliography items.

**Constraint:** the Library returned the source text but raw-byte materialization to the working container was not authorized. Therefore, no complete revised English or Korean TeX manuscript and **no full 34/30-page revised PDF** were compiled or claimed. The existing complete original source was **not copied into this public GitHub repository**. Source original and Zenodo remain untouched.

## Exact edits

**Section 2.2:** clarify that the typed material-record signature is fixed for regimes being compared within a shared family, but the signature itself may be selected as part of the existentially supplied witness of Section 7.

**Section 7.1 (Theorem 7.1 proof):** clarify that choosing the empty signature is **part of the existence witness**, not a construction under every externally fixed signature/codomain; no mathematical statement or quantifier is strengthened.

**Data and code availability:** correct `Sections 4 and 7 and Appendix C` to `Sections 4–7 and Appendix C`; explain that the frozen D2 code uses a lightweight stage profile and its original Proposition 5.14 code uses a valid alternative structure, whereas source-matched checks are available in later audits.

The optional Appendix E infinite-family extension is **unchanged**: countably indexed families, unconditional convergence, bounded linear transport and the role of repeated channels remain governed by its original definitions.

## Exact executable patch and what was tested

- [Non-destructive bilingual section patch](../../src/apply_formation_phase10_patch.py), final Git blob `aa96d0324f28e896b5f562861a2af2f13b49d6ab`.
- [Five regression tests](../../tests/test_formation_phase10_patch.py), Git blob `999c1b3f3234e6198402c392d73cf8e3353ba49a`.
- [Python 3.10 / 3.12 CI workflow](../../.github/workflows/formation_phase10_bilingual_patch.yml); **CI completion has not been verified**.

The local Python 3.13.5 tests returned **5/5 PASS**: exact English and Korean source-anchor patching; rejection when an anchor is missing; rejection when the source anchor is duplicated; rejection of an incorrect printed source date. The patcher also rejects reworded source anchors, missing author/date, and any changes to protected math/label tokens; it writes new files rather than replacing originals.

In addition, **one-page English and Korean source-wording smoke fixtures** were independently patched, and each was compiled twice using XeLaTeX with successful visual layout inspection. A relative-output-directory compile regression was identified during testing and **corrected**; the final script was rerun successfully and GitHub's final blob exactly matches the corrected, executed local file.

This is **NOT** a full-paper layout, equation numbering, bilingual translation or publication-QA pass.

## Safe reproduction when original RC1 TeX files are available locally

From a Windows **CMD** working directory that contains those two original RC1 TeX files and the downloaded patch script:

```cmd
python -W error apply_formation_phase10_patch.py --en "DSD_Formation_Axiom_System_EN_20261022_RC1.tex" --kr "DSD_Formation_Axiom_System_KR_20261022_RC1.tex" --output-dir "PHASE10_CANDIDATES" --compile
```

Requires a usable Python and XeLaTeX environment, with the original paper's packages and Korean fonts. Output is *only* under the newly created directory; original inputs remain unchanged. The script produces sectionwise diff files and a SHA256 manifest, and compiles each PDF twice if requested.

## What remains open

1. Apply the tested section patch to the **actual original RC1 bytes** in a working environment where source files can be mounted.
2. Compile full English and Korean TeX twice and verify PDF outputs (pages, labels/refs, citations, no new compilation errors, bilingual text).
3. Compare changed regions and unaffected sections against both original PDFs, log differences and warnings; do not silently publish a new Zenodo version.
4. Reinspect Theorem 7.1/Corollary 7.2 quantifier scope and the two statements in Data and code availability in the fully compiled versions.

**Final classification:** `PHASE10_NONDESTRUCTIVE_PATCH_READY / BOTH_LANGUAGES_SOURCE_VERIFIED / FIVE_UNIT_TESTS_PASS / TWO_LOCALIZED_XELATEX_PDFS_PASS / FULL_SOURCE_COMPILATION_OPEN / FORMAL_ZFC_CERTIFICATION_OPEN`.