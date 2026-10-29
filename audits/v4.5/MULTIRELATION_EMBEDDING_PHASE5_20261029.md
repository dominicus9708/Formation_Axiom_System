# DSD Formation Axiom System v4.5 — Phase 5: Multi-relation, multi-kind formation embedding audit

**Audit date:** 2026-10-29 (Asia/Seoul)  
**Manuscript author:** Kwon Dominicus  
**Locked manuscript:** 2026-10-22 English PDF, 34 pages, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## Scope and evidence separation

This work extends prior Phase 4 partial-assignment R4 and witness-reflection checks to **a nonempty ternary material relation, fixed external annotation codomains, support anchors, two source quantity kinds, two-dimensional rational component terms, and a chain of two non-surjective formation embeddings**. It is a finite source-linked test of Definition 6.2 F1–F6, Definition 6.4 R1–R5 and witness reflection, and selected consequences of Theorems 6.5 and 6.8.

No manuscript revision, new axiom, claim of full universal formal verification, or empirical interpretation is licensed by these tests. The scalar field used in the finite implementation is `Q`. Its finite arithmetic remains exact; it is a special instance, not an assertion concerning arbitrary fields/vector spaces.

### Frozen source and output artifacts

- [Full finite multi-relation embedding checker](../../src/formation_multirelation_embedding_audit.py)
- [Three-model composable-embedding checker](../../src/formation_embedding_composition_audit.py)
- [Executed mutation result JSON](../../results/formation_multirelation_embedding_audit.json)
- [Executed composition result JSON](../../results/formation_embedding_composition_audit.json)
- [CI Python 3.10/3.12 replay definition](../../.github/workflows/formation_phase5_embedding_audit.yml)

The two Python and two JSON files were **executed locally** and uploaded byte-identically to GitHub. Python source Git blob IDs:
- `e65c9bf6f097f0aa1a6fdfc3d9fa2b5f30f0b22f`
- `3f03e8de0dff1ddc24391b3794ca49bf32cca127`.

Result Git blob IDs:
- `8f471f83a130bb2710ec6993900aee0ee080a744`
- `b045cb59e21fb8944f036025c78b2529a7cc7909`.

Results were byte-identical under three different `PYTHONHASHSEED` settings (0,17,731). The GitHub Actions replay is configured, but no completed GitHub Actions run has yet been independently observed here.

## Source-matched positive embedding

The source L has four material items, candidate expressions `H,h`, candidate configurations `p,p_bad`, two quantity kinds `energy,phase`, two roles, and a **nonempty ternary material relation** with induced material/active substructures. Material items carry explicit fixed external color annotations and support anchors. The model has two admitted channels with 2D vector terms.

The target M adds one new material item, two mixed ternary relation tuples involving that new item, an extra expression `g` and configuration `p_extra`, an extra quantity kind and role, and new values outside the source pointed-value images. Its five admitted channels include two inherited channels and three target-only channels. The source-to-target term map is a non-singular rational 2x2 matrix.

**Observed:** F1–F6 PASS; material relation reflection on the material image PASS; R1–R5 PASS; independent witness-reflection PASS; term-space and carrier maps injective PASS. A full formation embedding exists; source and target are **not strictly formation-isomorphic**, as their carrier cardinalities differ.

The Phase 4 relative graph reflection boundary survives simultaneously for two quantity kinds: the source has undefined `energy(c)` while the target assigns `energy(c)=2`, outside the image of the source value carrier `{0,1}`. The other kind retains a valid source defined-zero assignment.

## Nine targeted invalid embedding mutations

All **nine target variants remain valid standalone Formation full models**, preserving the nonempty original formation kernel. The selected candidate source→target map is rejected for a precise reason:

| Mutation | Expected failure | Observation |
|---|---|---|
| Target adds a ternary relation tuple using only original material items | material-record **embedding** reflection (not F1 homomorphism) | PASS |
| Target changes a fixed-codomain annotation on a mapped item | F1 | PASS |
| Target changes a mapped item's fixed support anchor | F1 | PASS |
| Target includes an additional *mapped* material item in an existing expression | R1 | PASS |
| Target replaces a new outside-image assignment value with an inside-image value | R4 | PASS |
| Target adds a role tuple on entirely source-indexed data | R5 | PASS |
| Target adds a realization relation on source-indexed data | R3 | PASS |
| Target breaks the term correspondence under the supplied J | F6 | PASS |
| Target changes a previously false primitive configuration gate to a different false pattern | R2, and also F2 | PASS |

**Caveat:** the last mutation changes one primitive gate from true to false as well as its reflected status, so it fails F2 and R2; it is not an isolated R2-only counterexample. Every standalone mutated target model was checked for the core I/II/III/V rules and term-domain closure before being counted as a negative *embedding* fixture. When the assignment changes, its new channel 5-tuple forces an updated target term-map domain; an initial invalid fixture was corrected before the final PASS.

## Two successive formation embeddings

A third valid model N adds another material item, mixed ternary relation, an extra quantity kind and role, and new assignments without changing the inherited source-image primitive graph. Both embeddings L→M and M→N, and the composite embedding L→N, satisfy all checked F1–F6/R1–R5 and witness reflection clauses. The number of admitted channels is **2 → 5 → 7**.

The selected rational term maps are:
- `J_LM = [[2,1],[1,1]]`
- `J_MN = [[1,1],[0,1]]`
- `J_LN = [[3,2],[1,1]] = J_MN J_LM`.

All **4** subsets of the two admitted L-channels satisfy `J_LN Comp_L(F) = Comp_N(Φ[F])`; no multiplicity or noninjective collapse is introduced. This confirms a finite illustrative instance of Theorem 6.5 and the admitted-channel set-sum covariance of Proposition 6.3/Theorem 6.8.

## Remaining scope gaps

1. Full general proofs for all fields, infinite carriers, arbitrary multi-arity relation signatures, and arbitrary term spaces are not mechanically verified by these instances.
2. The material-record signature tested has **one ternary relation and two fixed external unary maps**, not arbitrary multi-arity combinations; the latter needs fresh adversarial audit.
3. The meaning and correctness of externally supplied `Desexpr`, `Adm_cfg`, `LC`, and `BC` remain application-specific and are not derived or empirically validated by Formation.
4. No claim is made that all possible invalid embeddings are rejected by the finite mutation bank; these are *nine selected* examples.

**Phase 5 judgment:** `FINITE_MULTIRELATION_PASS / NEGATIVE_EMBEDDING_MUTATIONS_9_OF_9 / THREE_MODEL_COMPOSITION_PASS / UNIVERSAL_FPA_OPEN / EXTERNAL_APPLICABILITY_OPEN`.

### Windows 11 execution (repository root)

```powershell
python -W error src\formation_multirelation_embedding_audit.py --output-dir results
python -W error src\formation_embedding_composition_audit.py --output-dir results
```

Outputs are written into the repository's existing `results/` directory as two new, separately named JSON files.
