# Formation Axiom System v4.5 — Phase 2 internal falsification and stage-comparison audit

**Audit date:** 2026-10-29 KST  
**Paper author:** Kwon Dominicus  
**Version lock:** 2026-10-22 English PDF, 34 pages; SHA256
`af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

This audit is additive. It does **not** alter the main manuscript, the original
reproducibility scripts, expected 3×3 constants, or prior evidence records.

## 1. Source-locked artifacts

- [Finite negative fixtures and staged comparator](../../src/formation_negative_stage_audit.py)
  — locally executed, Git blob `b141fddd50cbe6008b5d395c50c888080bd95153`.
- [Positive finite scope countermodels](../../src/formation_semantic_boundary_audit.py)
  — locally executed, Git blob `592b54f2784d3a1facffc134a8bd81d24aafdb53`.
- [Negative/stage JSON](../../results/formation_negative_stage_audit.json)
  — locally produced, Git blob `1e88da83e7b8b765fcc39e764d64cbcf787cd5b5`.
- [Semantic countermodel JSON](../../results/formation_semantic_boundary_cases.json)
  — locally produced, Git blob `4c6d9418b615a8cf93ed0b419a0b1f95b850015d`.
- [Dedicated two-version GitHub Actions workflow](../../.github/workflows/formation_scope_audit.yml).
  The workflow was **configured** to regenerate both JSON files on Python 3.10/3.12
  and compare exact bytes. A completed remote run has **not been independently
  observed** in this record.

All four source/output blob IDs were compared with GitHub's fetched files,
and the values matched the locally executed files. Local runs used
`python -W error` and `python -W error -m py_compile`.

## 2. Negative-model falsification tests

**7/7 independent primitive-axiom violations were detected with exactly
the expected violation code**, each retaining a nonempty valid formation
kernel: one describable configuration, one defined assignment, and one admitted
channel.

| Test | Expected unique detection | Result |
|---|---|---|
| F02 | expression describable without admission (I) | PASS |
| F04 | restriction breaks anchor inheritance (II) | PASS |
| F04 | restriction target not admitted (II) | PASS |
| F04 | admitted expression lacks identity restriction (II) | PASS |
| F05 | realization breaks anchor inheritance (III) | PASS |
| F05 | realization uses unretained material (III) | PASS |
| F06 | assignment outside union of describable active material (V) | PASS |

Separately, **3/3 corrupted definitional closure outputs** were detected:
incorrect Stage IV derived describability, missing Stage VI channel,
and incorrect Stage VII finite sum.

These are construction-specific negative witnesses. They are not a general
mechanized completeness proof for all ill-typed inputs or all forms of axiom
violation.

## 3. Exhaustive comparisons in a restricted finite family

An initial 72-parameter experiment included duplicate descriptors when no
admitted channel existed. That exploratory count is **superseded**.

The corrected generator varies the Stage I expression predicate, Stage II
restriction relation, three independent Stage III configuration predicates,
Stage V assignment status, Stage VI role, and Stage VII supplied term values,
while omitting vacuous term variations. It produced **80 pairwise distinct
valid descriptors**, confirmed by explicit equality checks.

Every unordered model pair including the diagonal was compared
(`80*81/2 = 3240`). Every bijection of the finite candidate material,
expression, configuration, role, and fixed pointed-value carriers was
enumerated. Stage VII existence of an invertible one-dimensional real
linear transport was checked exactly with rational ratios.

| First branch | Number of unordered pairs |
|---|---:|
| 0 | 0 within the equal-carrier 80-model family |
| 1 | 1600 |
| 2 | 800 |
| 3 | 672 |
| 4 | 0 |
| 5 | 32 |
| 6 | 44 |
| 7 | 8 |
| None (strictly isomorphic) | 84 |
| **Total** | **3240** |

- No Stage IV first-branch discrepancy: **0**.
- No disagreement between `b(L,M)` and `b(M,L)`: **0**.
- No comparison-set nesting failure: **0**.
- Additional explicitly constructed cases each realize first branches
  `b=0,1,2,3,5,6,7`, plus strict identity and a nontrivial scalar
  `J(x)=7x` strict isomorphism.

**Important computational limit:** this is exhaustive only *inside the
declared finite parameter family*, not over all DSD models. One quantity
kind, fixed pointed-value set `{0,1}`, empty relational material record,
one-dimensional real term space, and a common support anchor are imposed.
The scalar `J` check is not a general solver for arbitrary vector spaces.
Some of the 84 pairs represent two different labelled descriptors that
are strictly isomorphic under the available transformations.

## 4. Fourteen positive scope / non-implication witnesses

14 selected finite tests passed: admitted-but-not-describable expression,
nontransitive restriction chain, two witnesses for one five-coordinate
channel, assigned zero with nonzero supplied term, describable configuration
with no channels, assigned configuration with no role, absent-channel term
undefined, source-exact one-material/three-role noninjective composition,
injective powers-of-two composition, undefined/zero/negligible status with
explicit size and threshold, strict relabeling and scalar-map composition,
unused candidate's effect on strict full comparison, heterogeneous anchors,
and the same regime-global assignment inherited across two configurations.

The `(1,-1,0)` term witness gives equal nonempty subset sums for distinct
channel families, while `(1,2,4)` gives all eight different subset sums.
Therefore composition **need not be injective**; noninjectivity is not a
universal necessity.

An additional positive witness has **two different restriction-realization
histories for the same channel**, correctly yielding one channel identity
and a two-element witness family.

## 5. Audit status and remaining obligations

**PASS within the recorded finite signature. Not a full universal
mathematical proof audit, not independent external review, and not empirical
validity.**

Remaining P0/P1:
1. Prove/review each general manuscript proposition independently, with
   source line/assumption mapping, especially Section 6 embeddings,
   isomorphisms, and first-branch invariance.
2. Extend the comparator beyond one kind, one-dimensional scalar terms,
   empty material relation, and fixed pointed-value sorts.
3. Introduce malformed type and map-domain cases, including a nontrivial
   relational material signature and all anchoring-side inheritance.
4. Implement exact literal D2 source reconstruction and independent
   Proposition 5.14 checks in the original reproducibility package
   without changing older historical outputs.
5. Test cross-time changes only as a later dynamical interface, not as
   a primitive temporal Formation axiom.
6. Separate applicability/policy choices from physical, legal, empirical
   and normative validation. An externally supplied `BC` or
   `Desexpr` predicate is not derived by Formation itself.

## 6. Windows 11 reproduction

From the existing `Formation_Axiom_System` repository root:

```powershell
python -W error src\formation_negative_stage_audit.py --output-dir results
python -W error src\formation_semantic_boundary_audit.py --output-dir results
python -W error -m py_compile src\formation_negative_stage_audit.py src\formation_semantic_boundary_audit.py
```

Outputs use the existing `results/` folder:
`formation_negative_stage_audit.json` and
`formation_semantic_boundary_cases.json`.

**Verdict:** no counterexample to the examined Formation axioms or staged
comparison results was found within this finite scope. The incomplete
general theorem audit must remain explicitly open.
