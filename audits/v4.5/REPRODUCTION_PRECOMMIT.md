# Formation Axiom System v4.5 — preregistered reproducibility audit

Audit date: 2026-10-22 KST. Paper author: **Kwon Dominicus**.
Manuscript: Formation Axiom System, revised print date 2026.10.22.
Release PDF source: `DSD_Formation_Axiom_System_EN(7).pdf` (34 pages), SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`. The various numbered filename suffixes are file collision suffixes, NOT manuscript version numbers.
Zenodo edition label as supplied by author: **v4.5**. This audit does not claim Zenodo publishing was executed here.

## Frozen source code (do not change source algorithms merely to fit expected results)

- `src/formation_axiom_reproduction.py` Git blob `9417dc54978d5f2cf797507fede4ebfda5076dd9`;
- `src/verify_formation_axiom_results.py` Git blob `18722f8b883b0457cef9e7f27ab0b00277d32173`;
- `tests/test_formation_axiom_reproduction.py` Git blob `21739d5db1f9c0fd7dbf46e7e44bac31dbb91289`.
- CI workflow `.github/workflows/reproducibility.yml` runs `python src/formation_axiom_reproduction.py --output-dir results`, `python src/verify_formation_axiom_results.py --results-dir results`, and `python -m unittest discover -s tests -v` on both Python 3.10 and 3.12 upon push.

## Prespecified acceptance checks

1. For **both** Python versions, observe GitHub Actions run status, final conclusion, step-level results, and actual output logs; do not label an unobserved run as complete.
2. Indexed 3×3 witness: 512 configurations; admitted channels L_H=768, L_G=1536; distinct per-configuration channel structure 387; vertical only 62; index-aligned mismatched composite coincidences 127. Indexed first branch b=5 derived from 768 vs 1536 assignment-domain cardinality under supplied Stage-4 identity comparison, rather than hard-coded.
3. D2 first branch b=3 and one-point model and non-injective composition checks pass, but distinguish **what existing code actually constructs**:
   - `construct_d2_witness()` only encodes selected sites, primitive blocked-boundary permissions and Stage comparison truth profile. It does NOT enumerate the revised v4.5 D2 material carrier of 57 items, 9 retained, 6 blocked exposure slots, or inheritance maps.
   - The **new-edition** source-bound explicit 57/9/6 D2 check is independently archived at `dominicus9708/DSD_Method_Family/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/scripts/verify_n2_four_sections.py` with its executed JSON. This is related evidence, not a rerun of this repository's D2 function.
4. Check existing `noninjective_composition_witness()` against v4.5 p14 Proposition 5.14. It gives a valid abstract unequal-family zero-sum instance using THREE material identifiers and assigned values (+1,-1,0). The printed v4.5 source instead specifies ONE material item with three role-distinguished admitted channels, each with assigned value 0 and component terms (+1,-1,0). Preserve this **source-identity difference** without silently claiming a verbatim reconstruction.
5. Source/expected-data code SHA comparison before and after. Check output JSON and CSV actual generation; note committed `results/` status separately from CI run-generated files (which GitHub Actions may discard when not uploaded as artifacts).
6. Treat finite numerical reproducibility, exact model instance reconstruction, paper-level mathematical proof, and external independent validation as four **different** verdicts. No auto-update of expected constants.
7. Publish source-bound results in `audits/v4.5/`, append README/REPRODUCIBILITY/PROOF_MAP only with accurate provenance after measured evidence; do NOT silently overwrite existing release tags or Zenodo.
8. If CI cannot be triggered or results unavailable, mark `NOT_EXECUTED` and provide Windows 11 commands. Avoid fabricated success.

```text
AUDIT_CASE: FORMATION_V4_5_REPRODUCTION_20261022
SOURCE_ALGORITHMS_CHANGED: no
CI_EXECUTION: PENDING_NEW_RUN
NUMERIC_VERDICT: NOT_REVIEWED
EXACT_D2_V4_5_CARRIER_CHECK_IN_THIS_REPO: NOT_IMPLEMENTED
EXTERNAL_INDEPENDENT_VALIDATION: not_established
```
