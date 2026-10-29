# DSD Formation Axiom System v4.5 — 2026-10-29 internal boundary audit

Author of the audited paper: **Kwon Dominicus**. Target: 2026-10-22 English manuscript (34 pp), SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`. This is an **additional independent finite stress audit**, not a restatement of the earlier v4.5 CI verification.

## Executed and verified

- New Python: [src/formation_scope_stress.py](../../src/formation_scope_stress.py). Executed with seed `20261029`, 400 generated finite models and 400 consistently relabeled copies.
- Observed: 400/400 models passed sampled checks of primitive axioms I, II, III, V, the configuration-witness rule, channel formation, formation-trace membership, and order-independent finite set sums. All 400 renamed instances passed the same checks; channel counts and scalar sums were invariant.
- Coverage: 205 generated models with nonempty admitted channel sets, 104 with multiple channels, 97 with at least one defined zero assignment; half the trials intentionally include a valid active witness to reduce vacuity.
- Thirteen elementary boundary assertions passed. These are **not thirteen full independent model proofs**, and the sampled generator uses one common support anchor, an empty relational material signature, one quantity kind, two roles, and scalar term values.
- Result: [results/formation_scope_stress_report.json](../../results/formation_scope_stress_report.json). Code Git blob `b0495e94a82df5a75fa38c9f9bc2ce7954425d5f` matches the locally executed file byte-for-byte. Python source SHA256 `6bbefd7229335535c40f5c7a43785057d48199234f004052e37e1a2dbd22cd59`.
- Extra independent three-channel scalar enumeration: all 125 term triples from `{-2,-1,0,1,2}^3` have subset-sum collisions, including collisions among distinct nonempty subsets. This is only a restricted value-range statement; `(1,2,4)` gives eight distinct subset sums, demonstrating that injectivity **can** hold on a selected domain.
- Optional countable extension comparison: the orthogonal family `e_n/n` in `ℓ²` is unconditionally summable but not norm-absolutely summable. Formation Appendix E's optional unconditional indexed domain is broader than the static aggregation paper's optional absolute domain; this is not a contradiction of the finite core.

## Sampled source-level review, not completed universal proof audit

1. Sections 2–3 clearly mark `Desexpr`, `Adm_cfg`, `LC`, and `BC` as supplied primitive interface data; universal empirical criteria are **not derived**.
2. Theorem 6.17(ii)'s no-independent-Stage-IV-branch assertion follows from preservation and reflection of every conjunct of `Ψ`; a complete brute-force independent stage comparison enumerator remains pending.
3. A channel includes assigned value `v` in identity, but its post-Stage-VI supplied term `T(c)` is not a fixed function of that value alone. A defined zero can have a nonzero term, and an absent channel has no term in the core.
4. Global partial `q_lambda` excludes simultaneous contradictory values for one item and quantity kind within one regime. This is an intentional modeling restriction, not a physical result.
5. The finite composition is over an unordered **set** with no duplicates. Indexed families with multiplicity require an explicitly declared extension.
6. Proposition 6.22 is existential. For an independently prescribed term-space map `J`, strict equivalence need not yield Definition 6.21 coincidence; with no admitted channels, there are no nonempty family witnesses.
7. First branching is the least stage where all compatible comparison tuples are exhausted, not failure of one chosen identification and not chronological onset.
8. The earlier source-locked 3×3 results `768/1536/387/62/127` were **not independently rerun by this new script**. Its 512 cases enumerate site subsets under specified rules, not all possible 3×3 models.

## Prepared adversarial / scope experiments

| ID | Candidate | Expected verdict under current source | Current status |
| --- | --- | --- | --- |
| F01 | Admitted but not describable expression | Legal | Elementary assertion |
| F02 | Describable but not admitted expression | Illegal, Axiom I | Full negative fixture pending |
| F03 | Well-typed nontransitive restriction chain | Legal, optional transitivity is additional | Elementary assertion |
| F04 | Restriction target without admission or mismatched anchor | Illegal, Axiom II | Full negative fixture pending |
| F05 | Realization with noninherited material/anchor | Illegal, Axiom III | Full negative fixture pending |
| F06 | Conflicting local values of same `q_lambda(a)` | Cannot be one global partial function | Elementary assertion |
| F07 | Undefined, defined zero, negligible nonzero | Distinct statuses; small nonzero requires specific size and threshold | Expanded fixture pending |
| F08 | Describable and assigned but role absent | Channel absent | Generated-model coverage |
| F09 | Assigned zero, admitted role, nonzero term | Legal, term map supplied separately | Elementary assertion |
| F10 | Multiple witness histories for same five-tuple | One admitted channel, multiple formation traces | Full fixture pending |
| F11 | Two different finite families with equal sum | Legal, noninjectivity allowed | Exhaustive bounded scalar study |
| F12 | Superincreasing terms `(1,2,4)` | Injective on selected subsets | Constructive countercase |
| F13 | Duplicate elements in finite family | Set semantics collapse duplication | Elementary assertion |
| F14 | Consistent relabeling of candidate structures | Strictly equivalent under all maps | 400 paired finite checks; general transports pending |
| F15 | Alleged first branch at closure Stage IV | Impossible within the axioms | Proof review; independent comparison enumerator pending |
| F16 | D2 57/9/6 with one BC difference | Can produce first branch at Stage III | Earlier N2 source-locked audit only |
| F17 | 3×3 equal composite but assignment mismatch | Can give first branch at Stage V | Earlier source-locked CI only |
| F18 | Strict equivalence plus externally prescribed `J=-id` | Selected nonempty coincidence may fail | Elementary assertion |
| F19 | Empty admitted-channel set | Def 6.21 cannot have nonempty coincidence witness | Elementary assertion |
| F20 | Repeated indexed countable channels | Not core `P_fin(C)`, optional extension | Scope proof |
| F21 | `e_n/n` in `ℓ²` | Unconditional but non-absolute sum | Analytic case |
| F22 | Same material, different supplied boundary policy | Different outputs possible without inconsistency | D2 model relevant; new policy variants pending |
| F23 | Time-indexed variation in inherited assignment coordinate | Formation transition/lineage, not same static channel | Interface audit pending |
| F24 | Physical, legal, or normative validity of supplied predicates | Requires external domain evidence | External test pending |

## Unfinished priority audit work

**P0:** independent source-by-source proof-obligation map for every theorem, explicit finite counterinterpretations to F02/F04/F05/F10, full all-stage model-pair comparator, independent embedding/isomorphism transports, exact D2 and Proposition 5.14 source-instance regression tests.

**P1:** heterogeneous anchors; relational material signatures; multiple kinds, value carriers, and roles; non-scalar term spaces; invalid-input mutation tests; scaling benchmarks; real-case fitness and external peer review.

## Windows 11 execution

From the original `Formation_Axiom_System` repository root:

```powershell
python src\formation_scope_stress.py --output-dir results --trials 400 --seed 20261029
```

The only output is the new `results/formation_scope_stress_report.json`. The original reproduction algorithm, baseline expected constants, the manuscript, and previous historical evidence were not modified.

**Current status:** selected finite internal checks PASS; complete paper-level mathematical audit and external applicability assessment NOT YET COMPLETE.
