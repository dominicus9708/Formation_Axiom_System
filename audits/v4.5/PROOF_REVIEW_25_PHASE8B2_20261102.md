# Formation Axiom System v4.5 — Phase 8B.2: remaining 25 printed proof paragraphs

**Paper author:** Kwon Dominicus. Source: printed 2026-10-22, 34-page English paper, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`. Audit date: 2026-11-02.

## Outcome

This pass **independently inspected all 25 previously outstanding, explicitly marked `Proof.` paragraphs** against their source premises and conclusions. These are distinct from the eight high-dependency claims separately audited in Phase 8B.1 and the thirteen short direct implications indexed in Phase 8A.

- **24/25:** no invalid inference identified under the declared source assumptions and definitions.
- **1/25 (Theorem 7.1):** formal-signature scope requires clarification. This is an ambiguity / possible proof-scope gap, **not an established contradiction**.
- **Complete proof-assistant ZFC certification:** OPEN; no machine-verification claim is made.

## Claim-by-claim premise-to-conclusion review

| Claim | Check performed | Verdict |
|---|---|---|
| Proposition 2.5 | Coordinate erasures, identity and composition | Supported |
| Theorem 3.6 | Existence of structural witness iff admitted channel; T domain | Supported |
| Theorem 4.5 | Four source Countermodels 4.1–4.4 satisfy the other axioms | Supported within displayed witnesses |
| Proposition 4.6 | Equality of anchor-function domains; induced relations; one partial q | Supported |
| Corollary 4.8 | Contrapositive of Axiom I | Supported |
| Lemma 4.10 | Sequential restriction and anchoring inheritance | Supported |
| Proposition 4.12 | Explicit absence of transitivity in Axiom II | Supported |
| Lemma 4.13 | Axioms II and III compose material/anchor restrictions | Supported |
| Corollary 4.14 | Negation of necessary conjuncts of Ψ | Supported |
| Proposition 5.2 | Assignment-status disjointness, `λ∈Λδ` scope | Supported under declared scope |
| Proposition 5.5 | Describable configuration with empty quantity assignment domain | Supported |
| Proposition 5.6 | Formation-channel inheritance through IV, VI, II, III | Supported |
| Proposition 5.8 | Defined assignment without any admitted role | Supported |
| Proposition 5.14 | Single material, assigned zero, three distinct role channels, terms 1,−1,0 | Supported |
| Proposition 6.3 | Forward preservation plus **channel injectivity** for finite-set covariance | Supported |
| Corollary 6.6 | Identity, associativity, composition of maps form a possibly large category | Supported |
| Corollary 6.7 | Identity and composition of inclusion embeddings form a preorder | Supported |
| Theorem 6.8 | Witness and channel reflection **on source candidate images only** | Supported |
| Corollary 6.12 | Induced channel bijection, termwise linear transport, finite sums | Supported |
| Theorem 6.14 | Inverses and compositions of all E1–E9 bijections | Supported |
| Theorem 6.16 | Nested staged comparison sets and first-empty-stage rule | Supported |
| Corollary 6.18 | Stage 4 cannot first branch because I3=I4 | Supported |
| Proposition 6.22 | One-channel zero versus two-channel cancelling sum, unequal cardinalities | Supported |
| Theorem 6.23 | Negation of existence of a candidate satisfying all E1–E9 | Supported |
| **Theorem 7.1** | Empty material-record signature chosen despite §2.2 ‘fix S_mat’ | **Scope clarification recommended** |

## Theorem 7.1: fixed versus selectable material signature

**Exact source tension:** Section 2.2 first says to fix a typed material-record signature `S_mat` and defines each material structure as an `S_mat`-structure. Theorem 7.1 states existence of a full model given B and F, and its proof **chooses the empty material-record signature**.

Two interpretations lead to different proof obligations:

1. If Theorem 7.1 asserts *existence for at least one selectable signature*, choosing the empty signature is legitimate and proves model-class nonemptiness.
2. If the theorem asserts existence **for each arbitrary, already fixed signature**, one cannot replace the fixed signature with the empty one in the proof. One must exhibit an interpretation of that fixed signature, subject to its typed external-codomain constraints, or weaken/qualify the quantification.

**Assessment:** This is a scope-of-quantification/exposition issue. The current evidence **does not establish falsehood of the existence theorem**, but the printed proof does not by itself justify the stronger reading. Clarifying whether `S_mat` is fixed *within a comparison family* or *globally before existence quantification* is recommended before an external review.

This is a new mathematical-exposition candidate **separate** from the two Data-and-code-availability editorial recommendations in Phase 7. Do not silently modify the original manuscript or enlarge the theorem's claims.

## Source-linked executable and review records

- [Locked source-PDF proof review script](../../src/formation_phase8b2_proof_review.py) — checks the SHA256 and exactly the 25 listed `Proof.` paragraphs; does **not** prove their statements.
- [Review JSON with one line of premise/conclusion reasoning per proof](../../results/formation_phase8b2_25_proof_review.json).
- [Prior eight detailed proof-chain reviews](PROOF_CHAIN_EIGHT_PHASE8B_20261102.md).
- [69-item and 13-direct-inference inventory](PROOF_OBLIGATION_STAGE7_PHASE8_20261102.md).
- [Appendix E infinite-series boundary audit](GENERAL_SECTION6_APPENDIXE_PHASE6_20261029.md).

**Reproduction from repository root**, on Windows with Poppler utilities `pdftotext` available on PATH:

```powershell
python -W error src\formation_phase8b2_proof_review.py --pdf "D:\path\to\DSD_Formation_Axiom_System_EN.pdf" --output-dir results
```

The script rejects a different PDF SHA, produces a 25-entry review register, and asserts one source-scope qualifier. It **does not computationally check the mathematics**, which is reviewed separately in this report.

## Status and following work

`P8B2_ALL_25_REMAINING_EXPLICIT_PROOFS_REVIEWED / 24_SUPPORTED_WITH_SOURCE_ASSUMPTIONS / THEOREM7_1_SIGNATURE_SCOPE_CAVEAT / ALL_33_EXPLICIT_PROOF_PARAGRAPHS_HAVE_RECEIVED_A_SOURCE_BASED_FIRST_PASS / 13_DIRECT_IMPLICATIONS_INDEXED / FULL_MACHINE_FORMALIZATION_OPEN`.

Next: re-review the 13 direct implications in detail, reconcile the material-signature quantification between Sections 2 and 7, then run a final full-reference/English-Korean editorial revision audit only when a separate manuscript change candidate is ready. The finite core and Appendix E's unconditional convergence/bounded transport must continue to be distinguished. Original PDF, TeX, and Zenodo remain unmodified.