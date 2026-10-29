# Formation v4.5 — Phase 6 appendix A–D and publication-text inspection

**Audited paper author:** Kwon Dominicus. PDF 34 pp, 2026-10-22; SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## Appendix checks

- **Appendix A (Typing and Notation):** partial q and T on admitted channels are consistently typed, matching Section 2 and Stages VI–VII; candidate-channel absence is distinct from a component term equal to zero. No new mathematical contradiction detected.
- **Appendix B (stage/result summary):** descriptions of the six residual independent constraints and the stage 4 nonbranching closure track the revised Section 4 Theorem 4.7 and Section 6 Theorem 6.17. Full FPA remains open.
- **Appendix C (reconstruction):** 3×3 counts 768/1536, mismatches 387, vertical-only 62, index-aligned composite coincidences 127 independently re-executed against the exact 512 source partition. D2 Section 7.3 57/9/6 checked independently as combinatorics; N2 remains the distinct source-faithful typed material/anchor record audit.
- **Appendix D (optional transitivity):** `Res(H,h) ∧ Res(h,g) ⇒ Res(H,g)` is explicitly optional. With required identity restrictions this makes Res a preorder **on admitted expressions**; core Primitive Axiom II does not force transitivity. No accidental implication of the optional axiom by the core was found.

## Proposition 5.14 source fidelity: corrected remaining-work scope

The **original frozen** `src/formation_axiom_reproduction.py` uses an alternative three-material-item finite noninjectivity witness. However, the **independent Phase 2 audit** `src/formation_semantic_boundary_audit.py` already has `S08_noninjective_composition_exact_source_structure`: **one material item, one assigned value 0, three distinct roles, and supplied terms +1,-1,0**, reproducing the **exact source configuration of printed Proposition 5.14**. This source-specific check was locally rerun and PASS. It remains to **connect the newer audit fixture to the baseline reproducibility navigation**, not to invent another model or modify historic baseline source.

## Actual manuscript/editorial review issues

1. The printed p.33–34 **Data and code availability** says model constructions, countermodels and finite witness counts appear in “Sections 4 and 7 and Appendix C.” Countermodels and a finite example are also in **Sections 5 and 6** (e.g. 5.10, 5.14, 6.22). Recommend a small section-range correction.
2. The same statement references a separate public reproducibility package without distinguishing the original D2 **lightweight profile** from the 57/9/6 N2 source-faithful checker and the frozen package's **alternative** Proposition 5.14 example. Recommend an explicit source-fidelity caveat or index link to the newer tests.
3. A single optional remark after Definition 6.4 could clarify that R4 reflects graph membership **on the image of the pointed value space**, not all target-only assignment definedness.
4. Appendix E, already audited separately, correctly adds **bounded** linear transport and **indexed-family** preservation for unconditional infinite summation; Static Aggregation uses **set-indexed** absolute summability. A cross-paper scope note would help readers but is not a required correction of mathematical claims.

**Verdict:** no newly identified axiom/theorem correction obligation from appendices A–E. Two editorial/citation-fidelity repairs and optional explanatory remarks are recommended, and overall proof-assistant level formal verification remains OPEN. Manuscript PDF, LaTeX and Zenodo have **not** been altered by this audit.
