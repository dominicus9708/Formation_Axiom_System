# Reproducibility protocol

**v4.5 / 2026-10-22:** see [actual two-version GitHub Actions rerun](audits/v4.5/REPRODUCTION_RESULT.md) and [public Actions logs](https://github.com/dominicus9708/Formation_Axiom_System/actions/runs/39655845322). This unchanged-script check covers original finite counts and stage-profile regressions. It does **not** itself construct all of the newly explicit §7.3 57 full D2 material items, 9 retained items, six blocked slots, 30 remaining transmissive slots or H→h→p inherited records; those have separate source-locked N2 verification in the DSD Method Family repository. It also uses an alternative valid finite-sum noninjectivity witness to the literal v4.5 Proposition 5.14 instance. Keep versioned software replay and exact manuscript-instance reconstruction distinct.



## Environment

- Python 3.10+
- standard library only
- no random seeds, network access, external datasets, or platform-specific numerical libraries

## Procedure

1. Run `formation_axiom_reproduction.py` to reconstruct all deterministic outputs.
2. Run `verify_formation_axiom_results.py` to compare outputs with the manuscript values.
3. Run the unit tests.
4. Confirm the final message reports:

```text
D2 first branch 3
indexed first branch 5
channel counts 768/1536
mismatches 387
vertical-only 62
coincidences 127
```

## Expected files

The generated JSON files are written with sorted keys and fixed indentation. The CSV rows are ordered by configuration index `0` through `511`, so identical Python versions produce semantically identical outputs.

## Failure policy

Any assertion failure indicates that the executable reconstruction no longer matches the finite definitions or reported values in the manuscript. The code must not silently update expected constants to fit new output.
