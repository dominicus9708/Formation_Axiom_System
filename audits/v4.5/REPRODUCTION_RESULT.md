# Formation Axiom System v4.5 — unchanged-script reproducibility verification

**Audit date:** 2026-10-22 KST (GitHub Actions UTC `2026-10-21T18:47:11Z`).
**Paper author:** Kwon Dominicus.
**Manuscript source:** `DSD_Formation_Axiom_System_EN(7).pdf`, **34 pages**, printed date `2026.10.22`, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.
**Author-supplied Zenodo version label:** **4.5**, not a GitHub software semantic-version upgrade.

## Preregistered baseline and original source custody

[Before-execution requirements](REPRODUCTION_PRECOMMIT.md) committed as `2b0d55984d22157cc543a84418a1c35dff2053df`. That commit **did not modify**:
- `src/formation_axiom_reproduction.py` (Git blob `9417dc54978d5f2cf797507fede4ebfda5076dd9`);
- `src/verify_formation_axiom_results.py` (Git blob `18722f8b883b0457cef9e7f27ab0b00277d32173`);
- `tests/test_formation_axiom_reproduction.py` (Git blob `21739d5db1f9c0fd7dbf46e7e44bac31dbb91289`).

No expected constant has been adjusted to make a failing result pass. The GitHub Actions `.github/workflows/reproducibility.yml` job itself performed the actual **original-script run**, not an independently rewritten imitation.

## New CI execution, complete and observed

- **Actual GitHub Actions new run** [Reproducibility checks #39655845322](https://github.com/dominicus9708/Formation_Axiom_System/actions/runs/39655845322).
- Trigger: push `2b0d55984d22157cc543a84418a1c35dff2053df`; event `push`; `status=completed`; `conclusion=success`; attempt `1`.
- Started at UTC `2026-10-21T18:47:11Z`, completed approximately `18:47:25Z` (2026-10-22 KST). Source SHA fixed by commit.
- **Python 3.10 job** id `119415740864`: `Reproduce finite witnesses=success`, `Run unit tests=success`; observed **8 tests / 8 passed**.
- **Python 3.12 job** id `119415740740`: same two successful steps, observed **8 tests / 8 passed**.
- The job logs show the exact expected verifier statement in both jobs:
  `Verification passed: D2 first branch 3; indexed first branch 5 derived from Stage-4 identity comparison plus the 768/1536 Stage-5 assignment-domain cardinality obstruction; mismatches 387; vertical-only 62; coincidences 127.`
- GitHub Actions outputs are created in each isolated runner's `results/`. The CI workflow **does not upload those generated files as new GitHub Actions artifacts or commit back updated result files**. The observed logs verify the actual execution; existing committed JSON outputs are historical fixtures, not files produced by this new run.

### Reproduced v4.5 finite checks (under original code)

| Quantity or witness | Verified value | Scope |
| --- | ---: | --- |
| Indexed configuration pairs | 512 | All index pairs enumerated |
| Admitted channels in `L_H` | 768 | 3×3 indexed finite example |
| Admitted channels in `L_G` | 1536 | Same |
| Stage-5 assignment domains | 768 vs 1536 | Explicit cardinality obstruction |
| Indexed first branch | `b=5` | Derived using manuscript-supplied Stage-4 identity agreement and cardinality obstruction |
| Indexed channel-structure mismatch pairs | 387 | All 512 enumerated |
| Vertical-without-horizontal in `L_H` | 62 | 512 enumerated |
| Full-family composite coincidences among mismatches | 127 | 512 enumerated |
| D2 first branch | `b=3` | **Existing lightweight stage-profile fixture only** |
| Original unit tests | 8/8 on Python 3.10, 8/8 on 3.12 | Full existing `tests/` suite |

## Critical model-fidelity boundary: source v4.5 D2 and Proposition 5.14

**D2 source §7.3 (new printed pp26–27):** the updated manuscript specifies a **57-item** 3×3 typed grid carrier (9 vertex, 12 undirected nearest-neighbor edge, 36 directional boundary-slot items), **9 retained active items** (two vertices, one edge, six exposed slots), six blocked versus thirty transmissive annotations, and inherited boundary/anchor records.
Current `src/formation_axiom_reproduction.py::construct_d2_witness()` records `support_size=9` **representing the number of grid sites**, selected sites `((0,0),(1,0))`, primitive blocked-boundary policies and prescribed stage-profile flags. It **does not construct or test the full 57/9/6 annotated material-record object or the map H→h→p**. Therefore the new CI `D2 b=3` result verifies its **abstract stage-obstruction fixture**, not complete identity with §7.3 source material record. It would be wrong to describe the function as the full v4.5 D2 reconstruction.

An already executed, separately source-locked, full-grid finite checker supplies the **complementary** material-slot/anchor/annotation checks, without changing this repo's algorithms:
- [DSD Method Family new-edition N2 script](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/scripts/verify_n2_four_sections.py), Git blob `562cad9ae7399c8c81b64c793f0afea43c7a726d`;
- [N2 recorded finite output](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/results/n2_four_sections.json), Git blob `844113c067a9c487607663dd7d39b738264a2b8d`;
- [N2 source audit result](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/formation_axiom_system/versions/2026-10-22/SECTION_AUDITS/FAS-F2-20261022-N2-FOUR-SECTION-REAUDIT-001_RESULT.md).

**Proposition 5.14:** current `noninjective_composition_witness()` produces distinct admitted families with terms `+1,-1,0` for three material-item identifiers and assigned values `+1,-1,0`. Original v4.5 Proposition 5.14 printed p14 instead constructs **one material item with assigned value 0**, three distinct roles, and independent **component terms** `+1,-1,0`. The existing code's unequal-family zero-sum result is mathematically valid as an *alternative finite witness*, but the exact manuscript's material/role/value arrangement is not reproduced. This is a fidelity/documentation issue, not a failure of the underlying noninjectivity claim.

**Recommended follow-up status:** no change is required to the original **3×3 indexed numerical computation or verifier algorithms**. If the software's description is to claim **literal reconstruction of every amended v4.5 finite witness**, add a new explicit D2 material/annotation constructor and a source-exact noninjective-composition test (separate scoped tests, preserving existing code and historical results). The already-executed N2 D2 verifier is acceptable as clearly identified complementary evidence, not as an unrecorded successful test in this repository.

## Independent conclusions

```text
AUDIT_CASE: FORMATION_V4_5_REPRODUCTION_20261022
SOURCE_PAPER: Formation Axiom System v4.5 / 2026.10.22 EN PDF
GITHUB_ACTIONS_RUN: 39655845322 / completed-success
PYTHON_3_10: PASS / 8 of 8 tests
PYTHON_3_12: PASS / 8 of 8 tests
INDEXED_3X3_NUMERIC_CLAIMS: PASS, original algorithms unchanged
D2_LIGHTWEIGHT_STAGE_PROFILE: PASS, b=3
D2_FULL_57_9_6_IN_THIS_EXPERIMENT_REPO: NOT_IMPLEMENTED
D2_DETAILED_COMPLEMENTARY_N2_EVIDENCE: PRESENT, separate GitHub source-locked check
P5_14_SOURCE_EXACT_INSTANCE_IN_THIS_REPO: NOT_IMPLEMENTED (alternative valid finite witness)
ORIGINAL_PYTHON_ALGORITHMS_MODIFIED: no
NEW_GITHUB_ACTIONS_OUTPUT_ARTIFACTS: none (CI job logs only)
MATHEMATICAL_THEOREM_PROOF_BY_THIS_RUN: not_established
INDEPENDENT_EXTERNAL_VALIDATION: not_established
ZENODO_PUBLISH_ACTION: none
```

## Existing Windows 11 reproduction commands (unchanged)

From the root of the cloned **`Formation_Axiom_System`** repository:
```powershell
python src\formation_axiom_reproduction.py --output-dir results
python src\verify_formation_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
```

Outputs saved consistently at the repository's existing `results/formation_witness_summary.json`, `results/proof_obligation_audit.json` and `results/indexed_witness_cases.csv`. No new default input/output directory was invented.

**Operational note:** the GitHub Actions log emits a non-failing warning that `actions/checkout@v4` and `actions/setup-python@v5` target deprecated Node.js 20 and are forced to Node.js 24. This is CI workflow maintenance to consider separately; it does not affect the Python witness mathematical outcome and is not a reason to silently change original Python algorithms.
