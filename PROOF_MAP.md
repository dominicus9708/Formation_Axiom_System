# Computational proof map

This map states what each executable check supports and what remains a manuscript proof.

| Manuscript result or construction | Executable support | Scope |
|---|---|---|
| Primitive-interface status | none | Expression describability, configuration admission, local coherence, and boundary compatibility are regime-supplied primitive interface data; their domain-specific content is not derived computationally |
| Primitive restriction-relation status | finite witness constructors | The code instantiates restrictions satisfying the displayed finite soundness conditions; the general fact that `Res` is primitive and that target admission is imposed by Primitive Axiom II remains a manuscript-level logical distinction |
| Stage-0 comparison status | stage-profile bookkeeping only | Index `0` denotes the inherited background / ambient comparison level, not an eighth formation stage |
| One-point model and ZFC realizability witness | `construct_one_point_model()` | Checks the displayed finite instance, not the metatheoretic ZFC statement |
| Formation-trace/channel closure in the finite witness | one-point and witness constructors | Checks the instantiated closure data |
| Non-injectivity of finite-sum composition | `noninjective_composition_witness()` | Constructs two distinct finite channel families with equal composite `0` |
| D2 early boundary obstruction | `construct_d2_witness()` | Reproduces Stage-3 first branching for the displayed pair |
| Synthetic `3 x 3` indexed witness | `enumerate_indexed_witness()` | Exhaustively checks all `512` index-aligned pairs |
| Indexed assignment domains | `assignment_domain_lh()` and `assignment_domain_lg()` | Constructs the displayed finite domains with cardinalities `768` and `1536` |
| Indexed Stage-5 obstruction and first branch | `derive_indexed_first_branch()` | Uses the supplied Stage-4 identity comparison plus unequal finite assignment-domain cardinalities to rule out Stage-5 comparison and derive first branch `5` |
| E5 assignment-domain visibility | assignment-domain constructors in the indexed witness | The finite witness exposes assignment-domain membership explicitly; the general derivability of E5 from full E6 graph preservation under the stated bijectivity assumptions is a manuscript proof-level observation |
| Channel counts | deterministic enumeration | Reproduces `768` and `1536` |
| Channel-structure mismatches | deterministic enumeration | Reproduces `387` |
| Vertical without horizontal | deterministic enumeration | Reproduces `62` |
| Full-family composite coincidences | deterministic enumeration | Reproduces `127` among mismatched pairs |
| Primitive-axiom independence | none | General countermodel proofs remain in the manuscript |
| Unique relative closure | none | General extensional set-theoretic proof remains in the manuscript |
| Identity/composition closure of maps and embeddings | none | General proofs remain in the manuscript |
| Symmetry and strict-isomorphism invariance of first branching | finite profiles only | General theorem remains in the manuscript |

The executable package is therefore a reproducibility and proof-audit companion, not an automated formalization of the entire axiom system.
