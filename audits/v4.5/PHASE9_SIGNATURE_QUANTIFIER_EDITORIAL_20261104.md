# Formation v4.5 — Phase 9: existence-signature quantifier and editorial audit

**Audited paper:** Kwon Dominicus, *DSD Formation Axiom System*, 2026-10-22, 34 pp.  
**PDF SHA256:** `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.  
**Date:** 2026-11-04. **Historical source, TeX, Zenodo and prior tests:** unchanged.

## Source-locked issue: Section 2.2 vs Theorem 7.1

Printed **Section 2.2 (p.4)** fixes a typed material-record signature `S_mat`; material-internal symbols are relational and externally valued annotations may be typed maps with fixed codomains. Printed **Theorem 7.1 (pp.24–25)** asserts existence of a full formation model given B and F and constructs its witness using **the empty material-record signature**. **Corollary 7.2 (p.25)** explicitly formalizes the resulting **parameter-free existential** set-theoretic sentence. **Theorem 7.3 (pp.25–26)** separately accepts an already supplied finite relational `S_mat`-structure.

The distinction is:

1. **Existential reading:** the signature may be chosen along with the typed formation data. The empty-signature singleton witness in Theorem 7.1 is sufficient, and Corollary 7.2 is supported.
2. **Universal fixed-signature reading:** the printed proof cannot replace an arbitrarily pre-fixed signature by the empty one. An additional interpretation construction and any needed external-codomain typing hypotheses are required.

For any *purely relational* pre-fixed signature, a one-material structure can interpret **every** relation symbol as empty (including arbitrary finite arities), then use the rest of the paper's singleton formation witness. For any **finite family** of fixed unary externally valued material maps whose codomains are all nonempty, choosing an element of each also supplies the singleton interpretation.

By contrast, if a prescribed unary external annotation is total `χ:M→∅`, a **one-material** carrier `M={a}` admits no such map. **This is an obstruction to that particular singleton typed construction, NOT a counterexample asserting the nonexistence of every formation model** (e.g. the status of an empty material carrier is not adjudicated here).

**Judgment:** `THM7_1_EXISTENTIAL_READING_SUPPORTED / S_MAT_FIXED_SCOPE_CLARIFICATION_RECOMMENDED`. No demonstrated new axiom contradiction or false mathematical theorem.

## Independently executed bounded stress test

- [Exact Phase 9 fixture source](../../src/formation_signature_scope_phase9.py), Git blob `8adb6e73b0c9aaaca6b7a40f615e1d7af8acecaa`.
- [Archived deterministic JSON](../../results/formation_signature_scope_phase9.json), Git blob `d370eb2c472ef644e4e2b4fcff2c3fedf8b554e7`.
- [Python 3.10 / 3.12 replay workflow](../../.github/workflows/formation_phase9_signature_scope.yml), configured but **its completed run is not yet verified**.

The test constructs four **valid** one-material full formation models: empty signature; fixed unary/binary/ternary relations; fixed nonempty external codomain; mixed fixed relations plus three nonempty external codomains. It rejects one deliberately impossible **nonempty-material** total-map typing attempt `{a}→∅` and explicitly does not classify global model existence. In the four positive cases, Primitive Axioms I/II/III/V and Closure Clauses IV/VI/VII pass for the concrete singleton formation witness. The JSON bytes reproduce for `PYTHONHASHSEED=0,17,731`; this is not universal proof automation.

## Three minimal manuscript amendment candidates

**M1 — mathematical scope clarity, Sections 2.2 / 7.1.** Explain that a signature is fixed *within a regime-comparison family*, while the signature can be **selected as part of the existential witness** in Theorem 7.1/Corollary 7.2. This is the narrowest reading consistent with the printed singleton proof; **do not silently strengthen to a theorem for all arbitrary pre-fixed codomains**.

**E1 — actual editorial section omission.** The pp.33–34 *Data and code availability* points to Sections 4 and 7 and Appendix C, but relevant model/countermodel constructions also appear in Section 5 (Countermodel 5.10, Proposition 5.14) and Section 6 (Proposition 6.22). Change the range to **Sections 4–7 and Appendix C**.

**E2 — reproducibility fidelity.** The original [frozen experiment package](REPRODUCTION_RESULT.md) has a lightweight D2 stage-profile fixture and a valid **alternative** (not literal) Proposition 5.14 witness. The detailed D2 57/9/6 test is in the Method Family N2 audit; the source-exact one-material/three-role Proposition 5.14 witness is already `S08` in [Phase 2](../../src/formation_semantic_boundary_audit.py). Clarify **selected finite witnesses** and **supplementary source-matched checks**, preserving the original numerical evidence and the declaration that computation does not prove general theorems.

[Exact proposed English replacement paragraphs](PHASE9_PROPOSED_TEXT_20261104.md).

Optional, non-compulsory explanatory additions: Definition 6.4's R4 is image-relative, and Appendix E permits countably indexed **unconditional** summability with repeated channels and bounded-linear transport, while the separate Static Aggregation paper's optional domain uses set-indexed **absolute** summability. These are not errors.

## Current and pending outcomes

- `PHASE9_FOUR_POSITIVE_SINGLETON_FIXTURES_PASS`
- `ONE_FIXED_EMPTY_CODOMAIN_TYPED_SINGLETON_OBSTRUCTION`
- `THM7_1_EXISTENTIAL_SCOPE_SUPPORTED_WITH_EDITORIAL_QUALIFICATION`
- `THREE_MANUSCRIPT_CLARIFICATIONS_RECOMMENDED`
- `46_OF_46_SOURCE_ARGUMENTS_HAVE_PREVIOUS_INTERNAL_FIRST_PASS`
- `FULL_FORMAL_ZFC_PROOF_CERTIFICATION_OPEN`

**No original manuscript, publication, historical script or historic result was modified.** Actual change application requires a new separately versioned candidate with section-scoped LaTeX patches and English/Korean cross-reference regression.