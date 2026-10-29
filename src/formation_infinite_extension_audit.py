#!/usr/bin/env python3
"""Finite exact arithmetic sanity checks for the paper's Appendix E boundaries.

NOTE: the infinite statements in the report are proved analytically, not inferred
from finite numerical output. Author of audited paper: Kwon Dominicus.
"""
import argparse
import json
from fractions import Fraction
from math import fsum, sqrt
from pathlib import Path


def run():
    cases = {}
    # All finite orthogonal partial sums e_1/1 + ... + e_N/N in ell^2.
    # Every finite tail has norm^2 exactly sum(1/n^2).
    for N in (10, 100, 1000, 3000):
        squared = sum((Fraction(1, k*k) for k in range(1, N+1)), Fraction(0))
        scalar_abs = sum((Fraction(1, k) for k in range(1, N+1)), Fraction(0))
        # J diagonal on an orthonormal basis, J(e_n)=(1+1/(n+1)) e_n.
        # This bounded, boundedly invertible J has 1 < d_n <= 3/2.
        transported_squared = sum((Fraction((k+2)**2, ((k+1)*k)**2)
                                   for k in range(1, N+1)), Fraction(0))
        assert squared < Fraction(2)
        assert squared <= transported_squared <= Fraction(9,4)*squared
        assert scalar_abs >= 1
        cases[str(N)] = {
            'ell2_partial_norm': round(sqrt(float(squared)), 12),
            'absolute_norm_sum_harmonic': round(float(scalar_abs), 12),
            'bounded_transport_partial_norm': round(sqrt(float(transported_squared)), 12),
        }
    assert cases['3000']['absolute_norm_sum_harmonic'] > cases['10']['absolute_norm_sum_harmonic']

    # Finite witness: indexed duplication and set-identified channels differ.
    indexed = ['c', 'c']
    term = {'c': Fraction(1)}
    indexed_sum = sum((term[c] for c in indexed), Fraction(0))
    set_sum = sum((term[c] for c in set(indexed)), Fraction(0))
    assert indexed_sum == 2 and set_sum == 1

    # Large-n Cauchy tail bound ||sum e_n/n||^2 = sum 1/n^2 <= 1/N.
    # The first neglected index is N+1, and the integral bound holds.
    tail_bounds = {str(N): round(1/sqrt(N), 12) for N in (10,100,1000,10000)}

    # Diagonal J(e_n)=n e_n on a Hamel basis is an algebraic vector-space
    # automorphism, but not a bounded operator.  It maps e_n/n to e_n, whose
    # summands do not tend to zero. The existence and extension are mathematical
    # arguments supplied in the accompanying audit, NOT sampled computer proofs.
    return {
        'status':'PASS_FINITE_CONTROLS_WITH_ANALYTIC_PROOFS_SEPARATE',
        'source':'Formation v4.5 Appendix E and Static Aggregation Section 6',
        'orthogonal_series_ell2_over_n':{
            'partial_sum_samples':cases,
            'infinite_unconditional_convergence':'PROVED_BY_ORTHOGONAL_CAUCHY_TAILS',
            'infinite_failure_of_absolute_convergence':'PROVED_BY_DIVERGENCE_OF_HARMONIC_SERIES',
            'cauchy_tail_norm_bounds':tail_bounds,
            'not_a_computer_proof':True},
        'indexed_repetition_finite_control':{
            'index_count':len(indexed),'set_cardinality':len(set(indexed)),
            'indexed_sum':int(indexed_sum),'set_sum':int(set_sum)},
        'unbounded_algebraic_isomorphism':{
            'exists_in_zfc':'Hamel-basis extension of the orthonormal sequence',
            'J_on_orthonormal_vectors':'J(e_n)=n e_n',
            'unconditionally_convergent_source':'sum e_n/n',
            'divergent_transported_terms':'J(e_n/n)=e_n; terms do not tend to zero',
            'condition_tested':'boundedness is essential for the infinite covariance formula',
            'proof_not_numerical':True},
        'scope':'The executed finite calculations are illustrative controls only; all assertions about infinite families require the analytic proofs in the accompanying report.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',default='results')
    a=parser.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    report=run()
    target=out/'formation_infinite_extension_audit.json'
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf8')
    print('PASS infinite-boundary finite controls; sample_N = 10, 100, 1000, 3000; output',target)

if __name__=='__main__':main()
