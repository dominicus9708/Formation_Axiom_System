"""Independent three-channel and optional-infinite-domain scope illustrations.
Research manuscript author: Kwon Dominicus. Python 3.10+ standard library.
"""
import argparse
import itertools
import json
import math
from pathlib import Path


def subset_sums(terms):
    return {mask: sum(terms[i] for i in range(len(terms)) if mask & (1 << i))
            for mask in range(1 << len(terms))}


def run():
    counts = {'total_term_triples': 0, 'injective_subset_sum_triples': 0,
              'colliding_subset_sum_triples': 0, 'colliding_nonempty_triples': 0}
    for terms in itertools.product((-2, -1, 0, 1, 2), repeat=3):
        sums = subset_sums(terms)
        counts['total_term_triples'] += 1
        distinct = len(set(sums.values())) == 8
        counts['injective_subset_sum_triples'] += int(distinct)
        counts['colliding_subset_sum_triples'] += int(not distinct)
        nonempty = [sums[i] for i in range(1, 8)]
        counts['colliding_nonempty_triples'] += int(len(set(nonempty)) < len(nonempty))
    assert counts == {'total_term_triples': 125, 'injective_subset_sum_triples': 0,
                      'colliding_subset_sum_triples': 125, 'colliding_nonempty_triples': 125}
    assert len(set(subset_sums((1, 2, 4)).values())) == 8
    assert subset_sums((1, -1, 0))[3] == subset_sums((1, -1, 0))[4] == 0
    l2 = [{'N': n,
           'l2_partial_norm': math.sqrt(sum(1 / k**2 for k in range(1, n + 1))),
           'sum_of_term_norms': sum(1 / k for k in range(1, n + 1))}
          for n in (10, 100, 1000, 10000)]
    return {
        'subset_sum_exhaustive': counts,
        'examples': {
            'noninjective': {'terms': [1, -1, 0], 'two_families': [[0, 1], [2]], 'same_sum': 0},
            'injective': {'terms': [1, 2, 4], 'distinct_outputs': list(range(8))}
        },
        'l2_unconditional_not_absolute': l2,
        'interpretation': ('finite 3-channel scalar term-map enumeration; optional '
                           'infinite-dimensional extension illustrates difference between '
                           'unconditional and absolute convergence')
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='results')
    args = parser.parse_args()
    result = run()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'formation_scope_analytic_cases.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
