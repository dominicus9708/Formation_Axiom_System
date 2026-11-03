# Phase 9 — Minimal source-scoped editorial amendments (NOT APPLIED)

**Paper author:** Kwon Dominicus  
**Locked manuscript:** 2026-10-22, 34 pp, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## Candidate M1 — Section 2.2, after the material-record signature declaration

> The material-record signature is held fixed when comparing formation regimes within a comparison family. In the existence constructions of Section 7, the choice of such a signature is permitted as part of the existentially supplied formation data.

This preserves the actual Theorem 7.1 singleton existence argument and the parameter-free existential Corollary 7.2. The alternative of claiming existence for *every* externally fixed typed signature is stronger and requires distinct hypotheses and proof. Do not assert it implicitly.

## Candidates E1 and E2 — Data and code availability, pp.33–34

**Proposed complete paragraph, replacing only the existing availability paragraph:**

> No external empirical dataset is used. Model constructions, countermodels, and finite-witness counts used in this version are specified in Sections 4–7 and Appendix C. Executable checks of selected finite witnesses and numerical counts are publicly available at https://github.com/dominicus9708/Formation_Axiom_System. The original D2 checker verifies a lightweight stage profile, while its original Proposition 5.14 checker uses a valid alternative construction. Supplementary, source-matched checks are documented in the associated audit records. No computational output is required for the proofs in this manuscript, and the executable package is not used in place of the general set-theoretic proofs.

**Associated verification links** (ideally maintained in the public reproducibility README):
- Full source-matched D2 57/9/6: `dominicus9708/DSD_Method_Family/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/scripts/verify_n2_four_sections.py`
- Source-matched Proposition 5.14 one-material/three-role witness: `dominicus9708/Formation_Axiom_System/src/formation_semantic_boundary_audit.py`, case `S08`.

## Non-mandatory clarifications

- Definition 6.4 R4 reflects partial assignment graphs relative to the **source pointed-value image**, not every target-only assignment.
- Appendix E uses countably indexed families with possible repetitions, unconditional convergence, and bounded linear transport; the separate Channel-Indexed Static Aggregation paper uses countable sets and absolute-summability requirements.

## Change-management boundary

These are **candidates only**. Do not overwrite historical PDF, LaTeX, release assets, Zenodo entries, prior benchmark programs, or expected outputs. For actual manuscript revision, edit one LaTeX section at a time, preserve stable reference labels and author **Kwon Dominicus**, then independently rebuild and compare English and Korean PDFs.