# FAS v4.5 Phase 8A — source-locked proof inventory and independent Stage-7 obstruction audit

**Audited paper:** Kwon Dominicus, *DSD Formation Axiom System*, printed 2026-10-22, 34 pages.  
**Source PDF SHA256:** `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## Exact source inventory

The PDF is locked by SHA256. Poppler text extraction returned **69 distinct numbered items**:

| Kind | Count |
|---|---:|
| Theorem | 14 |
| Proposition | 16 |
| Corollary | 14 |
| Lemma | 2 |
| Countermodel | 6 |
| Definition | 12 |
| Remark | 5 |
| **Total** | **69** |

The 46 theorem/proposition/corollary/lemma statements comprise **33 explicit `Proof.` paragraphs** and **13 direct statements without a separately marked proof paragraph**. The latter are Corollary 4.11, Corollary 5.3, Proposition 5.4, Corollary 5.7, Proposition 5.9, Propositions 5.11–5.13, Corollaries 6.24–6.26, and Corollaries 7.2/7.4.

Each direct statement's prerequisite has been indexed:
- 4.11: finite induction on Lemma 4.10;
- 5.3–5.4: partial function and total-zero-padding definitions;
- 5.7, 5.9, 5.11–5.12: Closure VI, typed operational-channel identity and declared domain of T;
- 5.13: **explicit coexistence condition** for absent channel and admitted zero-valued term;
- 6.24–6.26: E5, E8 and induced channel bijectivity under strict isomorphism;
- 7.2, 7.4: Theorems 7.1/7.3.

This is not a declaration that any absent `Proof.` label constitutes an error; these are direct mathematical consequences. Extracted *explicitly named* references are not an exhaustive proof graph: unnamed axioms, core definitions, and logical inferences are not captured by reference regex.

## Independently executed Stage-7 first-branch witnesses

Build two full finite formation models with identical Stage 0–6 data (one material a, expression h, configuration p, one kind assigned value 0, two role-distinguished channels). The Stage-7 component space and terms may differ. Enumerate both role permutations and exactly test whether a rational vector-space isomorphism J can transport all terms.

For fixed equal term-space dimension d, `∃J∈GL_d(Q): JX=Y` iff `ker X=ker Y`. The latter is checked by exact rational reduced-row-echelon rowspaces, not float tolerances.

| Pair | Stage 0–6 | Stage 7 | Observed |
|---|---|---|---|
| Both full-family sums equal, but rank 2 vs 1 | nonempty | empty | b=7 both directions |
| Term-space dimensions 2 vs 1 | nonempty | empty | b=7 both directions |
| Both rank 1, but linear dependency coefficients differ | nonempty | empty | b=7 both directions |
| Invertible term transport | nonempty | nonempty | strict isomorphism |
| Role relabeling plus invertible transport | nonempty | nonempty | strict isomorphism |

These tests independently expose the distinction between Stage-6 channel data and Stage-7 vector-term compatibility. They support, but do not universally prove, Theorems 6.16, 6.17, 6.19 and Proposition 6.22. The first negative example has **equal aggregate full-family outputs** despite non-isomorphism.

## Provenance and artifact integrity

- [Source-locked 46-claim inventory program](../../src/formation_phase8_proof_obligation_inventory.py)
- [Executed 46-claim evidence index](../../results/formation_phase8_proof_inventory.json)
- [Exact rational Stage-7 witness program](../../src/formation_phase8_stage7_obstruction_audit.py)
- [Executed Stage-7 witness JSON](../../results/formation_phase8_stage7_obstructions.json)
- [Python 3.10 / 3.12 Stage-7 replay workflow](../../.github/workflows/formation_phase8_stage7_audit.yml)

Both programs and both JSON outputs were independently run locally with Python 3.13.5 and `-W error`. All four GitHub blob SHA values match the executed local bytes:
- Python inventory `6d81d484d401e16ffbd75b4988ec768e4f72714f`;
- JSON inventory `8085d997ab9b7f965108b0b804685f9c7958437a`;
- Python Stage-7 `eb7a48d072f962dd14ca096abc8671dcadabb9c1`;
- JSON Stage-7 `2a6fa3cf127c90dc048702b350a1fb73583c1bfa`.

A mistaken field in a **copied upload** of the Stage-7 JSON was corrected by immediate blob comparison and committed; the final stored blob equals the original executed JSON. No experiment outcome, algorithm, frozen manuscript, or prior audit was changed. **The source-PDF inventory cannot run on GitHub Actions until the locked original PDF is supplied**, so CI is configured only for the self-contained Stage-7 audit. No remote CI pass is claimed.

## Current logical-review decision and next checkpoint

- `PHASE8A_69_CLAIM_INVENTORY_COMPLETE`
- `33_EXPLICIT_PROOF_TEXTS_INDEXED / 13_DIRECT_DERIVATIONS_OBLIGATION_NOTED`
- `STAGE7_FINITE_OBSTRUCTION_3_OF_3 / STRICT_ISOMORPHISM_2_OF_2`
- `NO_NEW_COMPULSORY_MATHEMATICAL_ERRATUM_DEMONSTRATED`
- `WHOLE_ZFC_FORMAL_PROOF_AUDIT_OPEN`

**Next:** theorem-by-theorem premise-to-conclusion review of the 33 explicit proofs, with special attention to Theorems 3.3, 4.7, 6.5, 6.17, 6.19, 6.20, 7.3; then source-locked editorial patch proposal for the two known Data-and-code-availability statements. Appendix E's unconditional convergence and bounded-operator proof boundary remains audited separately in Phase 6. Manuscript and Zenodo remain untouched.

### Windows reproduction

```powershell
python -W error src\formation_phase8_stage7_obstruction_audit.py --output-dir results
python -W error src\formation_phase8_proof_obligation_inventory.py --pdf "D:\path\to\DSD_Formation_Axiom_System_EN.pdf" --output-dir results
```

The second command requires Poppler `pdftotext.exe` and the exact original PDF hash. Its JSON is a **proof obligation index**, not a formal proof certificate.