# Release notes — 1.1.1

Release date: 2026-08-09

## Stage-5 branching derivation patch

This patch strengthens the executable support for the synthetic indexed witness without changing any manuscript claim or reported finite count.

### Changed

- constructs the displayed assignment domains `Q_{L_H,lambda_E}` and `Q_{L_G,lambda_E}` explicitly;
- verifies their cardinalities as `768` and `1536`;
- records the resulting finite-cardinality obstruction to a Stage-5 assignment-domain bijection;
- derives the indexed first branching index `5` from the manuscript-supplied Stage-4 identity comparison plus the Stage-5 obstruction, instead of assigning `5` directly in the witness summary;
- adds dedicated unit tests and proof-audit fields for that derivation;
- updates the reproducibility documentation and proof map.

### Unchanged

- indexed configuration count `512`;
- admitted-channel totals `768` and `1536`;
- `387` channel-structure mismatches;
- `62` vertical-without-horizontal cases;
- `127` full-family composite coincidences among mismatched pairs;
- D2 first branching index `3`;
- the interpretation boundary that general set-theoretic theorems remain manuscript proofs.

The existing `1.1` release remains a preserved historical release. This patch is intended for a new `1.1.1` release rather than replacement of the `1.1` tag.

---

# Previous package note — v2.2.0

Release date: 2026-08-06

## Formation Axiom System reproducibility package

This release adds an executable companion to:

> Kwon Dominicus, *Formation Axiom System: Dimensional-Structural Describability*.

### Included checks

- one-point full-model satisfiability witness;
- D2 boundary-obstruction witness with first branching index `3`;
- synthetic indexed witness with first branching index `5`;
- admitted-channel totals `768` and `1536`;
- `387` channel-structure mismatches;
- `62` vertical-without-horizontal cases;
- `127` full-family composite coincidences among mismatched pairs;
- explicit non-injectivity witness for finite-sum composition.

### Reproducibility

The package uses Python 3.10 or later and has no third-party dependencies. GitHub Actions runs the package under Python 3.10 and 3.12.

### Scope

The software reproduces finite constructions and numerical claims. It does not replace the manuscript's general proofs of independence, closure, embedding, strict equivalence, or first-branching invariance.
