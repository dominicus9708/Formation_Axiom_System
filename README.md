# Formation Axiom System reproducibility package

This repository is the standard-library Python companion to:

> Kwon Dominicus, *Formation Axiom System: Dimensional-Structural Describability*.

It reproduces the manuscript's explicit finite constructions and numerical witness claims. It does **not** replace the manuscript's general set-theoretic proofs of primitive-axiom independence, unique relative closure, formation-trace characterization, morphism closure, strict-equivalence properties, or first-branching invariance.

## Reproduced claims

The package deterministically verifies:

- the one-point full-model satisfiability witness;
- the D2 early boundary obstruction with first branching index `3`;
- the synthetic indexed witness with first branching index `5`;
- `768` admitted channels in `L_H`;
- `1536` admitted channels in `L_G`;
- assignment-domain cardinalities `768` in `L_H` and `1536` in `L_G`;
- the resulting Stage-5 assignment-domain bijection obstruction;
- the indexed first branch `5`, derived from the supplied Stage-4 identity comparison and that Stage-5 cardinality obstruction;
- `387` index-aligned channel-structure mismatches;
- `62` vertical-without-horizontal cases in `L_H`;
- `127` full-family composite coincidences among the mismatched pairs;
- a fully constructed finite witness that finite-sum composition need not be injective.

The regression constant `indexed_first_branch = 5` remains in `EXPECTED` only as a check on the derived result. The executable path that produces the indexed first branch no longer assigns `5` directly.

## Requirements

- Python 3.10 or later
- No third-party dependencies

## Run on Windows

From the repository root:

```powershell
python src\formation_axiom_reproduction.py --output-dir results
python src\verify_formation_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
```

## Run on Linux or macOS

```bash
python3 src/formation_axiom_reproduction.py --output-dir results
python3 src/verify_formation_axiom_results.py --results-dir results
python3 -m unittest discover -s tests -v
```

## Deterministic outputs

- `results/formation_witness_summary.json`
- `results/proof_obligation_audit.json`
- `results/indexed_witness_cases.csv`

## Interpretation boundary

The D2 and indexed constructions are formation-finite formal witnesses. The `3 x 3` index partition is part of the model definition and is not claimed to be a geometric invariant. For the indexed witness, the manuscript supplies identity agreement through Stage 4; the executable package independently constructs the displayed Stage-5 assignment domains, checks their unequal finite cardinalities, and derives the resulting first branch. The computational audit checks these explicitly finite consequences; it does not establish the manuscript's general first-branching theorem, syntactic completeness, categoricity, decidability, or empirical validity.

## Primitive-interface and Stage-0 boundary

The executable package assumes the manuscript's regime-supplied primitive interface data; it does not derive the domain-specific content of expression describability, configuration admission, local coherence, or boundary compatibility. Likewise, `Res` is treated as a primitive restriction relation whose soundness and target admission are imposed by the manuscript's Primitive Axiom II rather than pre-encoded by the relation name.

Stage `0` is bookkeeping for the inherited background and ambient comparison level, not an eighth formation stage. In stage profiles, failure at index `0` therefore means that the background or anchored-carrier comparison already fails before the Stage-I--VII formation comparison. The executable finite witnesses do not turn this interpretation boundary into a new computational theorem.
