# Formation Axiom System v4.5 — Phase 4 general-map and embedding-boundary audit

**Date:** 2026-10-29 KST · **Original author:** Kwon Dominicus  
**Locked manuscript:** 2026-10-22, 34-page English PDF, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

This phase adds source-based reasoning and finite counter-witnesses. It **does not** modify the manuscript, Zenodo, baseline scripts, or historical verification results.

## Source-level theorem checks — no new contradiction found

- **Theorem 6.5 (identities and compositions):** F1–F5 are preserved through successive maps; F6 follows from `J_Θ(J_Φ(T(c))) = T_N(Θ̂(Φ̂(c)))`. For embeddings, image-exactness R1 under composition uses the *injectivity of the intermediate material map* to commute images with intersections. R2–R5 and independent witness reflection compose by chaining both-direction implications.
- **Theorem 6.8 (preservation/reflection):** the source candidate channel membership `c∈C_L ⇔ Φ̂(c)∈C_M` follows on the **mapped candidate image**, using witness reflection, graph reflection, and role reflection. It does **not** require every target channel to be in the image. Injectivity ensures finite **set** sums are transported without collisions; equality is under J.
- **Proposition 6.11 (strict iso iff bijective embedding):** surjectivity of the candidate-expression and configuration maps allows a target witness to be pulled back. Conversely, surjectivity of each pointed value-space map I is needed to derive E5 from the R4 graph-reflection clause.

These are internal proof-obligation inspections. They are not a proof-assistant formalization or independent external peer review.

## Derived boundary lemma (relative assignment-domain reflection)

For a formation embedding Φ and any source material a, quantity kind λ,

`a∈Q_{L,λ} ⇔ [f_M(a)∈Q_{M,τ(λ)} AND q_{M,τ(λ)}(f_M(a))∈Im(I_λ)]`.

Proof: membership of a in a partial function's domain is existence of a graph pair; apply (R4) in both directions for all v in the **source** value space. The result is graph reflection restricted to the image of the pointed-space map I. If I is surjective, the image test vanishes and assignment-domain membership is fully reflected. If it is merely injective, **target-only assignments at new values are permitted, even on already-mapped material**.

This is an important *meaning/terminology scope limit*, not a counterexample to the manuscript's actual Theorem 6.8 or Proposition 6.11.

## Executed examples and provenance

1. Full source model with V_L={0,1}, no q(a), and target V_M={0,1,2}, q_M(a)=2: **valid formation embedding** satisfying F1–F6, R1–R5, witness reflection and all injection requirements. New target channel is outside the induced source channel image. Not a strict isomorphism.
2. If target instead uses q_M(a)=1 (in the image of I), R4 fails and the embedding is rejected.
3. A new target-only expression g can supply the sole target configuration witness even while R1–R5 on source-indexed data hold. The **separate witness-reflecting requirement** is therefore necessary.
4. A retained source assignment without any describable source configuration violates Primitive Axiom V.
5. Two composable embeddings with enlarged pointed value spaces produce an embedding; source/target-only channels are correctly distinguished.
6. A bijective example is strictly formation-isomorphic.
7. A target-only role z can introduce a target-only admitted channel without spoiling reflection **on the source role image**.
8. Enumerated all **12** partial-assignment status pairs for source values {undefined,0,1} and target values {undefined,0,1,2}: **4** satisfy R4, including exactly one differing-definedness case (undefined→2). In the surjective two-value case, **3 of 9** pairs satisfy R4, all with identical definedness status.
9. Three **hypothetical** application predicates — configuration admission, local coherence, boundary compatibility — independently change source/target describability beginning with primitive Stage III. These examples do not validate any real technical standard, law, or laboratory procedure.

Complete finite fixture: [local source-bound test](../../src/formation_embedding_r4_scope.py) and [exact generated JSON](../../results/formation_embedding_r4_scope.json). Both were executed locally under Python 3.13.5 with `-W error`, and the GitHub blob IDs were checked against the executed local bytes. Repeating under PYTHONHASHSEED 0 and 731 gave byte-identical output.

A **larger separate local Phase-4 fixture** also executed 9 groups of full-model checks (including R1–R5, F1–F6 and witness reflection with explicit model signatures). Its Python SHA256 is `240b8c9567b366bcc19f8e371e9ceb02da5ba1e8415f4d52cb7e11ff48d30969`; its JSON SHA256 is `f8d093459699363eac031eb1c204c2046bccd98ccf304743c63c77e41466e860`. These *separate larger source bytes are not yet committed to this repository*; do not confuse the smaller GitHub fixture with the larger full-model run.

## Reproduce from Formation_Axiom_System root (Windows 11)

```powershell
python -W error src\formation_embedding_r4_scope.py --output-dir results
python -W error -m py_compile src\formation_embedding_r4_scope.py
```

Output: `results/formation_embedding_r4_scope.json`.

## Decision and next work

**Finite boundary cases: PASS. Section 6 core derivation review: supported within original assumptions. Full independent Formal Proof Audit: OPEN. External applicability: NOT ESTABLISHED.**

Next: extend complete embedding validation to multiple quantity kinds, multi-arity material relations and fixed-external-codomain annotations; review other general propositions in Sections 3–7 with explicit premise maps. Consider an optional **explanatory remark** distinguishing relative graph reflection from total assignment-domain reflection; this is not currently a required correction to the formal claims.