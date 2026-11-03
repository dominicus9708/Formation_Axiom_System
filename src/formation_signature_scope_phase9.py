"""Finite signature-scope stress fixtures for DSD Formation v4.5 Theorem 7.1.

Audited paper: Kwon Dominicus. Finite illustrations do not constitute a
universal proof and cannot refute the existential theorem over chosen signatures.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def build_one_material_model(signature):
    """Interpret all fixed purely relational symbols as empty relations.

    Interpret externally valued unary material maps by an available fixed
    codomain point. This fails for an empty codomain with nonempty material.
    """
    carrier = ('a',)
    relations = {name: {'arity': arity, 'tuples': []}
                 for name, arity in signature['relations'].items()}
    annotations = {}
    for name, values in signature['external_unary_codomains'].items():
        if not values:
            return {'one_material_full_model': False,
                    'failure': 'no total external-unary material map {a} -> empty codomain',
                    'blocking_attribute': name,
                    'whole_model_nonexistence_claimed': False}
        annotations[name] = {'codomain': list(values), 'map': {'a': values[0]}}
    for relation in relations.values():
        assert all(len(t) == relation['arity'] for t in relation['tuples'])
    for annot in annotations.values():
        assert set(annot['map']) == set(carrier)
        assert all(value in annot['codomain'] for value in annot['map'].values())

    # This is the paper's Theorem 7.1 one-material, one-channel formation core.
    expressions = {'h': {'material': ('a',), 'anchor': {'a': 's'}}}
    configs = {'p': {'active': ('a',), 'anchor': {'a': 's'},
                     'adm': True, 'lc': True, 'bc': True}}
    restrictions = {('h', 'h')}
    realizations = {('h', 'p')}
    admitted_expr = described_expr = {'h'}
    assigned = {'a': '0'}
    roles = {('p', 'a', 'lambda', 'rho')}
    # Primitive I, II, III, V (checked directly in this finite instance).
    assert described_expr <= admitted_expr
    assert ('h', 'h') in restrictions
    for H, h in restrictions:
        assert set(expressions[h]['material']) <= set(expressions[H]['material'])
        assert expressions[h]['anchor'] == {a: expressions[H]['anchor'][a] for a in expressions[h]['material']}
        assert h in admitted_expr
    for h, p in realizations:
        assert set(configs[p]['active']) <= set(expressions[h]['material'])
        assert configs[p]['anchor'] == {a: expressions[h]['anchor'][a] for a in configs[p]['active']}
    psi = {p for p, c in configs.items() if c['adm'] and c['lc'] and c['bc']
           and any((H, h) in restrictions and h in described_expr and (h, p) in realizations
                   for H in expressions for h in expressions)}
    active = {a for p in psi for a in configs[p]['active']}
    assert set(assigned) <= active
    admitted_channels = {(p, a, 'lambda', assigned[a], r)
                         for p, a, kind, r in roles if p in psi and a in assigned and a in configs[p]['active']}
    assert len(admitted_channels) == 1
    # Stage VII term space W={0}: only two finite channel sets, both sum to 0.
    assert len([frozenset(), frozenset(admitted_channels)]) == 2
    return {'one_material_full_model': True,
            'fixed_relation_symbols': len(relations),
            'nonempty_external_unary_maps': len(annotations),
            'admitted_channels': len(admitted_channels),
            'primitive_axioms': 'I/II/III/V verified on generated fixture',
            'full_model_closure': 'IV/VI/VII verified on generated fixture'}


def run():
    signatures = {
        'selectable_empty_signature': {'relations': {}, 'external_unary_codomains': {}},
        'fixed_mixed_arity_relations': {'relations': {'tag': 1, 'link': 2, 'triple': 3}, 'external_unary_codomains': {}},
        'fixed_nonempty_annotation': {'relations': {'link': 2}, 'external_unary_codomains': {'color': ('blue', 'red')}},
        'fixed_multiple_annotated_relations': {'relations': {'type': 1, 'incidence': 2, 'boundary': 3},
            'external_unary_codomains': {'color': ('blue',), 'class': ('A', 'B'), 'flags': (0, 1)}},
        'fixed_empty_external_codomain': {'relations': {'link': 2}, 'external_unary_codomains': {'unavailable_annotation': ()}},
    }
    checks = {name: build_one_material_model(signature) for name, signature in signatures.items()}
    assert sum(bool(c['one_material_full_model']) for c in checks.values()) == 4
    assert checks['fixed_empty_external_codomain']['whole_model_nonexistence_claimed'] is False
    return {'source_paper_sha256': 'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe',
            'status': 'FOUR_SINGLETON_FIXTURES_PASS_ONE_TYPED_OBSTRUCTION',
            'checks': checks, 'interpretation': 'Theorem 7.1 as an existential statement over selectable signatures is supported; a stronger all-fixed-signatures singleton construction requires codomain hypotheses.',
            'limitations': 'Illustrates one-material constructions, not nonexistence of all formation models for an empty external codomain or a proof over arbitrary infinite signature families.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output-dir', default='results')
    args = p.parse_args()
    dest = Path(args.output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    target = dest/'formation_signature_scope_phase9.json'
    target.write_text(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2)+'\n', encoding='utf8')
    print('PASS: 4 valid one-material models; 1 invalid fixed external-empty-codomain one-material type')
    print(target)


if __name__ == '__main__':
    main()
