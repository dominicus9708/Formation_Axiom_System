#!/usr/bin/env python3
"""Finite exact-arithmetic controls for Formation Axiom System Appendix E.

Audited paper author: Kwon Dominicus. The infinite claims are established by
analytic arguments in the companion report, never extrapolated from the tests.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def replicate(series: dict[str, Fraction], multiplicity: int) -> list[tuple[str, Fraction]]:
    assert multiplicity >= 0
    return [(key, term) for key, term in series.items() for _ in range(multiplicity)]


def finite_controls() -> dict:
    e_indices = (1, 2, 3, 4, 5, 10, 20)
    tests = {}
    for n in e_indices:
        # Orthogonal x_k = e_k/k; net (finite-subset) norm squared is an exact sum.
        norm_sq = sum((Fraction(1, k*k) for k in range(1,n+1)), Fraction(0))
        twice_norm_sq = 4*norm_sq
        harm = sum((Fraction(1,k) for k in range(1,n+1)),Fraction(0))
        assert twice_norm_sq == sum((Fraction(4,k*k) for k in range(1,n+1)),Fraction(0))
        # J e_k=(1+1/(k+1))e_k is boundedly invertible, 1 < d_k <= 3/2.
        Jnorm_sq = sum((Fraction((k+2)**2, k*k*(k+1)*(k+1)) for k in range(1,n+1)),Fraction(0))
        assert norm_sq <= Jnorm_sq <= Fraction(9,4)*norm_sq
        tests[str(n)] = {
            'orthogonal_sum_squared_norm': str(norm_sq),
            'each_nonzero_channel_duplicated_sum_squared_norm': str(twice_norm_sq),
            'absolute_norm_partial_sum': str(harm),
            'bounded_transport_squared_norm': str(Jnorm_sq),
        }
    # One admitted channel repeated N times: same vector v=1 in R.
    repeated_nonzero = {str(n): str(sum((Fraction(1) for _ in range(n)),Fraction(0))) for n in (1,2,5,10,20)}
    assert repeated_nonzero['20']=='20'
    repeated_zero = {str(n): str(sum((Fraction(0) for _ in range(n)),Fraction(0))) for n in (1,2,5,10,20)}
    assert set(repeated_zero.values()) == {'0'}
    # Alternating harmonic sum converges only in the chosen order; an
    # unconditionally summable one-dimensional family cannot have a divergent
    # positive-subseries. This is a finite control of an ANALYTIC argument.
    alternating_order = {}
    positive_odd_subfamily = {}
    for n in e_indices:
        alternating_order[str(n)] = str(sum((Fraction(1 if k%2 else -1, k)
                                              for k in range(1, n+1)), Fraction(0)))
        positive_odd_subfamily[str(n)] = str(sum((Fraction(1, 2*k-1)
                                                 for k in range(1,n+1)), Fraction(0)))
    fixture = replicate({'c':Fraction(1), 'z':Fraction(0)}, 2)
    source_family_sum = sum((v for _,v in fixture),Fraction(0))
    source_distinct_set_sum = sum({k:v for k,v in fixture}.values(),Fraction(0))
    assert source_family_sum == 2 and source_distinct_set_sum == 1
    return {
        'status':'PASS_FINITE_CONTROLS_WITH_INFINITE_ANALYTIC_BOUNDARY',
        'original_source':'Formation v4.5 Appendix E, 2026-10-22, 34pp, SHA256 af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe',
        'orthogonal_partial_sum_samples':tests,
        'alternating_harmonic_ordered_partial_sums':alternating_order,
        'alternating_harmonic_positive_odd_subfamily':positive_odd_subfamily,
        'one_nonzero_channel_repeated_finitely':repeated_nonzero,
        'one_zero_channel_repeated_finitely':repeated_zero,
        'two_repeated_indices_same_channel_family_sum':str(source_family_sum),
        'two_repeated_indices_collapsed_to_set_sum':str(source_distinct_set_sum),
        'mathematical_deductions_not_from_numeric_tests':{
            'infinite_nonzero_repetition_diverges':'any convergent series must have terms tending to zero',
            'infinite_zero_repetition_converges':'all zero terms give a net of zero finite subsums',
            'alternating_harmonic_not_unconditional':'positive-index subseries has divergent harmonic sum even though the alternating enumeration converges',
            'twice_each_orthogonal_e_n_over_n_unconditional':'Hilbert finite-subset orthogonality / bounded multiplicities',
            'twice_each_orthogonal_e_n_over_n_not_absolute':'2*harmonic series diverges',
            'bounded_linear_transport_preserves_unconditional':'bounded linear maps commute with finite-subset-sum net limit',
            'unbounded_linear_transport_may_fail':'Hamel extension mapping e_n to n e_n takes e_n/n into e_n',
        },
        'scope':'Tests alone are finite demonstrations, not formal proofs of infinite assertions.',
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='results')
    args=parser.parse_args()
    result=finite_controls()
    out=Path(args.output_dir)
    out.mkdir(parents=True,exist_ok=True)
    target=out/'formation_phase11_infinite_multiplicity.json'
    target.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS 7 orthogonal partial sums; zero vs nonzero repetitions; bounded diagonal transport')
    print(target)

if __name__ == '__main__':
    main()
