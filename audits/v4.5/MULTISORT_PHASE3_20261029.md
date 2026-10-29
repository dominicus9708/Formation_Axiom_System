# Formation Axiom System v4.5 — Phase 3 multisort and morphism-boundary audit

**Audit:** 2026-10-29 KST · Paper author: Kwon Dominicus  
**Manuscript:** 2026-10-22, 34 pages, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

This is an additive independent finite internal audit. It does not alter the manuscript or historical v4.5 reproducibility scripts.

## Expanded finite signature
- Two material items, two candidate expressions, two candidate configurations, two quantity kinds, two roles.
- Pointed value carriers `{0,1,2}`; selected negligible value kinds with thresholds and size functions.
- A finite directed material relation and fixed external support anchors.
- Component terms in the two-dimensional **rational vector space** `Q^2`.
- All finite candidate bijections for material, expression, configuration, quantity kinds, roles, and zero-preserving pointed-value maps are enumerated.
- At Stage 7, existence of an invertible `Q`-linear map `J:Q²→Q²` is determined by exact rational row reduction. Equality of the rowspaces of the two channel-term matrices is equivalent to equality of their kernels, and hence to extendability to an invertible linear transport.

## Reproducible finite result
Base seed `20261029`, 24 independently generated valid source models and their 24 renamed/transported strict isomorphs: **48 pairwise distinct full models**, including **32 with at least one admitted channel**.

All unordered pairs including the diagonal were considered: `48*49/2 = 1176`. The exact first-branch distribution was:

| First branch | Pairs |
| --- | ---: |
| 0 | 896 |
| 1 | 140 |
| 2 | 44 |
| 3 | 16 |
| 4 | **0** |
| 5 | 8 |
| 6 | 0 |
| 7 | 0 |
| No branch (strictly isomorphic) | 72 |
| **Total** | **1176** |

All stage-set nesting checks, reverse-direction first-branch comparisons, and Stage 3/4 equality checks passed in the tested family. Twenty-four expected relabeling isomorphisms using `J=[[1,1],[1,2]]` (determinant `1`) were verified.

**Designed cases separate from these 1176 pairs:**
- First branch `0` from incompatible fixed support anchors;
- First branch `5` from incompatible negligible-status data;
- First branch `6` from the role relation;
- First branch `7` from a change in the linear-dependence relations among corresponding terms, despite identical whole-support aggregate `(1,1)`.

## Implications of adversarial cases
1. Source terms `(1,0),(0,1)` and target terms `(1,1),(0,0)` have the same total `(1,1)`, but ranks 2 and 1 respectively. No linear isomorphism can carry all corresponding source terms to target terms. This establishes a concrete aggregate-equality / strict-Stage-7-inequality witness.
2. A forward map may identify two distinct role-labelled source channels with the same image channel, satisfying F1–F6 and individual term compatibility. With both source terms and the image term equal to 1, the finite source set composite is 2 and the image-set composite is 1. The channel-injectivity hypothesis in Proposition 6.3 is substantive, not decorative.
3. Twelve strictly isomorphic model triples were checked under double relabeling and invertible `Q²`-linear transport, with A→B, B→C, A→C, and reverse comparisons all passing.

## Limits / unfinished
This is exhaustive only **within the selected finite model and candidate-map families**, not a proof for all models. Material structure has just one binary relation, not arbitrary full multi-arity signatures. Term spaces are Q², not arbitrary vector spaces. Source-level theorem-by-theorem proof verification of the general embedding, isomorphism and submodel results remains open. The existence or empirical validity of supplied predicates `Desexpr`, `Admcfg`, `LC`, and `BC` is not derived from Formation.

**Status:** PASS selected multisort finite checks; universal mathematical review and external empirical assessment NOT COMPLETE.

## Local execution source and outputs
The two independently executed scripts and generated results are in the user's Phase-3 audit bundle, with SHA256 entries. The original baseline Python source and v4.5 published data remain unchanged.

- `formation_multisort_stage_audit.py`: SHA256 `97d657adcc74a5a159dfa439482ce8d101817aa4542f7e3645ff2d83f01c5853`
- `formation_map_boundary_audit.py`: SHA256 `76a327d4f56a44c66d533a7e428eb9f2b723daca63f575963435a9372b771a47`
- `formation_multisort_stage_audit.json`: SHA256 `895034e903f2f14f554ce8d87c9f891a4a0fc905f0180d09cf52bc6ae762b8c8`
- `formation_map_boundary_audit.json`: SHA256 `e712fedf6a528674b51ded0eacc77573df53fefdbf716076af1430f46c383e7a`

The complete executable code is not embedded in this report: it is identified by the SHA256 manifest in the locally provided reproducibility bundle.
