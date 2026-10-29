# FAS v4.5 — Phase 7 source-locked manuscript integrity and editorial review

**Date:** 2026-10-29 KST  
**Paper author:** Kwon Dominicus  
**Locked source:** `DSD_Formation_Axiom_System_EN.pdf`, 34 pp, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## Independent performed checks

1. Read the actual supplied 34-page PDF, validated its SHA256 and its metadata page count.
2. Re-extracted all explicitly numbered objects from `pdftotext -layout`: 14 Theorems, 16 Propositions, 14 Corollaries, 2 Lemmas, 6 Countermodels, 12 Definitions, 5 Remarks, **69 total**. No duplicate number per category.
3. Validated exact source anchors: Theorem 4.7, Propositions 5.13–5.14, Theorems 6.5, 6.8, 6.17, 6.19, 6.20, Proposition 6.11, Proposition 6.22, and Theorem 7.3.
4. Validated the source of printed Proposition 5.14: one material item and three roles, with individual terms `+1,-1,0`. The existing Phase-2 `formation_semantic_boundary_audit.py` check S08 already reproduces that exact witness. The **full 14-case Phase-2 source** was locally rerun under `-W error`, and its output JSON exactly matched the archived Phase-2 output bytes.
5. Verified the printed Appendix E retains **unconditional convergence** and **bounded linear isomorphism**. This verifies textual presence of its conditions; it does not prove the underlying mathematics.
6. Inspected the page 34 actual rendering, because the data-availability statement starts on page 33 and continues across the page break. Normalized inserted PDF footer page numbers only in extraction, leaving the source PDF unchanged.

## Two editorial clarification candidates, not new mathematical contradictions

**E1: provenance section location.** The printed Data and code availability describes all model constructions, countermodels and finite witness counts as located in “Sections 4 and 7 and Appendix C.” Section 5 also has Countermodel 5.10 and Proposition 5.14; Section 6 has the finite counterexample in Proposition 6.22.

**Proposed minimal replacement:**

> Model constructions, countermodels, and finite-witness counts used in this version are specified in Sections 4–7 and Appendix C.

**E2: executable package fidelity.** The baseline package's D2 fixture is a lightweight stage profile, not a literal 57/9/6 material-and-boundary reconstruction; the detailed source-locked N2 is separately recorded in the Method Family repository. Its original Proposition 5.14 code uses a valid **three-material** alternative example; the exact source's **one-material, three-role** witness is already in the repository's later Phase-2 check S08. These are provenance/coverage differences, not refutations of the paper's mathematical conclusions.

**Proposed minimal replacement of the package claim:**

> Executable checks of selected finite witnesses and numerical counts are publicly available at https://github.com/dominicus9708/Formation_Axiom_System. The original D2 checker uses a lightweight stage profile, and the original Proposition 5.14 checker uses an alternative valid construction; source-matched supplementary checks are separately documented in the associated audit materials.

The existing statement that computer output is **not needed as proof of the general theorems** should be retained.

## Optional explanatory improvement, not compulsory

Definition 6.4 R4 reflects partial assignment graphs **only relative to the image** of the source pointed value map. Appendix E's indexed-family unconditional-summability convention differs from the Static Aggregation paper's set-based absolute-summability convention. Either can be clarified without changing any mathematical premise.

## Public reproducibility items and custody

- [Executed phase7 source-locked checker](../../src/formation_manuscript_integrity_audit.py), Git blob `2ceae2cefdc1c3edc129b9709c80acf7dda5dcb9`.
- [Executed manuscript inventory JSON](../../results/formation_manuscript_integrity_audit.json), Git blob `0485129b123fa69fab7ae5f229223ec352b40476`.
- [Exact Phase-2 source-matched P5.14 check](../../src/formation_semantic_boundary_audit.py), S08; Phase-2 14-case local re-run exactly matches the archived JSON.
- [Frozen baseline reproducibility boundary](REPRODUCTION_RESULT.md).
- [Detailed source-locked D2 paper audit](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/SECTION_AUDITS/FAS-F2-20261022-N2-FOUR-SECTION-REAUDIT-001_RESULT.md).

**Windows command from repository root** (requires Poppler's `pdftotext.exe` and `pdfinfo.exe` installed and on PATH):

```powershell
python -W error src\formation_manuscript_integrity_audit.py --pdf "<actual_original_pdf_path>\DSD_Formation_Axiom_System_EN.pdf" --output-dir results
```

The script fails intentionally for a different PDF hash. Its checks **count printed headings and confirm selected strings; they do not certify that all 69 proofs are correct**. Never count this as full FPA closure.

## Decision

`SOURCE_LOCKED_PDF_INVENTORY_PASS / 69_PRINTED_ITEMS / PHASE2_P5_14_SOURCE_EXACT_REPLAY_PASS / EDITORIAL_CANDIDATES_2 / NO_NEW_MATH_ERROR_DEMONSTRATED / FULL_FORMAL_PROOF_AUDIT_OPEN`.

The original PDF, LaTeX and Zenodo publication were **not edited**. Recommended next step is theorem-by-theorem full premise-to-conclusion auditing and then applying the minimal editorial changes to a separately versioned manuscript candidate if authorized.