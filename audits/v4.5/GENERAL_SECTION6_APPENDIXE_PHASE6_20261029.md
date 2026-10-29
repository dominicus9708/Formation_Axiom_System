# Formation v4.5 — Phase 6: General Section 6 proof obligations and Appendix E infinite aggregation

**Audit date:** 2026-10-29 KST  
**Audited paper author:** Kwon Dominicus  
**Source lock:** `DSD_Formation_Axiom_System_EN.pdf`, 34 pp, 2026-10-22, SHA256 `af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe`.

## A. Core Section 6 obligations, source-conditional

| Source claim | Independent audit obligation | Verdict |
|---|---|---|
| Theorem 6.5 | Compose F1–F6, R1–R5, witness reflection, and injective material relation embeddings | internally supported under stated definitions |
| Corollaries 6.6–6.7 | Associativity and identity for the large category and inclusion-submodel preorder | internally supported |
| Theorem 6.8 | Reflect Ψ and channel membership **only on candidate images** and transport finite **sets** under channel injection | internally supported |
| Proposition 6.11 | Equate bijective embeddings and strict descriptor isomorphisms, using *surjectivity of each pointed-value map* to infer E5 from R4 | internally supported |
| Theorem 6.14 | Identities, inverses and composites of strict isomorphisms | internally supported |
| Theorems 6.16–6.17 | Nested full-comparison sets, I3=I4, closure determined by prior data | internally supported |
| Theorem 6.19 | Symmetry and invariance of first branch; for k≤6 J can be **any** map, while k=7 demands invertible linear J | internally supported |
| Theorem 6.20 | Dependency-based static-closure summary | supported **conditional on the preceding theorems** |

These verdicts are targeted source-based independent mathematical argument checks, **not** a complete ZFC proof-assistant certification or external referee report.

### A1. Proof detail for Theorem 6.5

For L→M material map f and M→N material map g, apply exact membership:

`f[mat_L(x)] = mat_M(f_E(x)) ∩ f[M_L]`,  
`g[mat_M(y)] = mat_N(g_E(y)) ∩ g[M_M]`.

Because g is injective, `g[A∩B]=g[A]∩g[B]`, yielding exact image membership for g◦f. The same argument holds for active material. Each R2–R5 and witness-reflection biconditional/implication chains through the intermediate model. F6 follows by composition of J maps and the induced channel maps. No invalid inference from forward homomorphism to reflection was found here.

### A2. Proof detail for Theorem 6.8 and Proposition 6.11

For source candidates, `c∈C_L ↔ Φ̂(c)∈C_M` follows from witness reflection, the reflected assignment graph and reflected role relation. This **does not** claim every target-only channel lies in the image. The exact relative assignment domain lemma is

`a∈Q_L,λ ↔ [ f(a)∈Q_M,τ(λ) AND q_M,τ(λ)(f(a))∈Im(I_λ) ]`.

In Proposition 6.11, I_λ is bijective, so the image condition disappears, explaining the E5 conclusion. The relative-domain phenomenon was separately observed in Phase 4/5 finite instances.

### A3. Proof detail for Theorems 6.17 and 6.19

Stage 3 comparison preserves and reflects each primitive conjunct of Ψ, so its existential closure is also preserved and reflected. Thus `I3=I4` and first branch 4 is impossible. Stage VI channel closure additionally needs the roles and Stage V graph; Stage VII composites additionally need W and T. Before Stage 7, the term-map component in a *full comparison tuple* is entirely unconstrained, so reversing a Stage 0–6 comparison can take the zero map; Stage 7 uses J inverse. This distinction makes first-branch symmetry valid without asserting that arbitrary vector spaces possess a linear isomorphism.

## B. Appendix E versus Static Aggregation Section 6

The **finite core** uses finite **sets** of admitted channels. Formation Appendix E optionally permits **countably indexed families with repetitions**, assumes F is R or C, W is Banach, and an **unconditionally convergent** term series. Preservation along strict comparisons adds an **indexed-family-preserving** induced map and a **bounded linear isomorphism** J.

The *Channel-Indexed Static Aggregation* paper, Section 6 (Definition 6.1, Theorem 6.2), Section 10.2 (Proposition 10.3), and Appendix C, instead use **finite or countable subsets** of admitted channels without repetition and require **absolute summability of norms**. Bounded transport preserves that narrower domain. These optional domains are **different but not inconsistent**.

### B1. Rigorous conditional-vs-absolute gap

Let W=ℓ²(R), let e_n be orthonormal basis vectors, x_n=e_n/n. For every finite E⊆{N+1,…},

`||Σ_(n∈E) x_n||²=Σ_(n∈E) 1/n² ≤ Σ_(n>N)1/n²→0`.

Therefore the family is unconditionally summable. However,

`Σ||x_n||=Σ 1/n=∞`,

so it is **not absolutely summable**. Hence it qualifies under Formation's Appendix E condition but not the Static Aggregation optional absolute domain. This observation requires the **infinite analytic argument**, not merely finite numerical samples.

### B2. A real counterexample if boundedness of J is dropped

Extend the independent vectors {e_n} in ℓ² to a Hamel basis using ZFC. Define an algebraic vector-space automorphism J by `J(e_n)=n e_n` and identity on all other Hamel basis elements. It is linear and bijective but unbounded. The unconditionally convergent source series `Σ e_n/n` is transported termwise to `Σ e_n`, which diverges because its summands do not converge to zero. Thus **finite strict isomorphism alone does not imply infinite-family covariance**.

This counterexample can be realized *within full Formation models*: use one material item a, admitted expression h, configuration p, a defined assigned value q(a)=0, and countably many distinct roles ρ_n. Then there are admitted channels c_n=(p,a,λ,0,ρ_n). Assign L terms e_n/n, M terms e_n, with all Stage I–VI data identical and algebraic J as above. The two **finite-core descriptors are strictly isomorphic** via E1–E9, but their infinite indexed families do not have matching convergent composites. Formation Appendix E **does not make the invalid claim**: it explicitly requires J bounded, which excludes this witness.

### B3. Indexed repeats cannot be silently reduced to sets

For `T(c)=1`, the indexed family (c,c) has sum 2, whereas the set {c} has sum 1. This is already witnessed at a finite level. Formation's Appendix E permits indexed repetition; the Static Aggregation optional extension is set-indexed. These are not automatically equivalent data types.

### B4. Covariance proof under actual Appendix E hypotheses

For an unconditionally convergent family (x_i), its net of finite-subset sums converges. Bounded linear J is continuous and commutes with this net's limit:

`J(Σ_i x_i)=Σ_i J(x_i)=Σ_i T_M(Φ̂(c_i))`.

The last equality uses **termwise** strict comparison and preservation of the indexing structure. Bounded invertibility also permits the reverse direction.

## C. Executed finite numerical controls, with limitations

- [Executable Python](../../src/formation_infinite_extension_audit.py).
- [Exact generated JSON](../../results/formation_infinite_extension_audit.json).
- Finite samples N=10,100,1000,3000 use rational arithmetic for harmonic partial sums and ℓ² squared norms; a bounded invertible diagonal map `J(e_n)=(1+1/(n+1))e_n` passes finite norm bounds.
- Indexed duplicate (c,c) versus set {c} gives 2 versus 1.
- **The infinite convergence/divergence and Hamel-basis claims are proven in B, not by the finite Python output.**

## D. Current conclusion and next serial checkpoints

**Phase 6:** `SECTION6_KEY_OBLIGATIONS_SUPPORTED_WITH_BOUNDARY / APPENDIX_E_ANALYTIC_CHECK_PASS / INFINITE_TYPE_MISMATCH_DOCUMENTED / FULL_MANUSCRIPT_FPA_OPEN`.

No new necessity to revise the mathematical statements was found at this stage. A cross-paper explanatory sentence distinguishing set-indexed absolute aggregation and indexed unconditional Formation extension would improve clarity but is not essential for validity.

Next in the user's requested sequence:
1. Source-locked Section 2–5 primitive, closure, independence, residual-minimality dependency audit.
2. Exact Section 7 D2 57/9/6, 3×3 512-index witness, Proposition 5.14 source-exact replay.
3. Appendix D and A–C consistency, text/source citations, manuscript and Zenodo publication provenance.
4. External application validation separately from the theorem-proof requirements.

Do not equate this partial, scoped mathematical inspection with all 69 numbered claims being formally proven in ZFC.
