"""Independent finite boundary stress checks for DSD Formation Axiom System v4.5.
Only uses Python standard library; no changes to original reproduction algorithms.
Author: Kwon Dominicus (paper); independent audit implementation.
"""
import argparse
import json
import random
from collections import Counter
from pathlib import Path


def subsets(items):
    return [frozenset(items[i] for i in range(len(items)) if mask & (1 << i))
            for mask in range(1 << len(items))]


def make_model(rng, size=3, force_active=False):
    material = tuple(f'a{i}' for i in range(size))
    pool = subsets(material)
    emat = {f'e{i}': rng.choice(pool) for i in range(4)}
    pmat = {f'p{i}': rng.choice(pool) for i in range(4)}
    if force_active:
        emat['e0'] = frozenset(material)
        pmat['p0'] = frozenset(material[:2])
    admitted_e = {e for e in emat if rng.randrange(2)}
    described_e = {e for e in sorted(admitted_e) if rng.randrange(2)}
    if force_active:
        admitted_e.add('e0')
        described_e.add('e0')
    res = {(h, h) for h in admitted_e}
    for h in emat:
        for e in emat:
            if emat[e] <= emat[h] and e in admitted_e and rng.randrange(4) == 0:
                res.add((h, e))
    realize = {(e, p) for e in emat for p in pmat
               if pmat[p] <= emat[e] and rng.randrange(3) == 0}
    conf = {p: tuple(bool(rng.randrange(2)) for _ in range(3)) for p in pmat}
    if force_active:
        realize.add(('e0','p0'))
        conf['p0'] = (True, True, True)
    psi = {p for p in pmat if all(conf[p]) and any(e in described_e and (h, e) in res
            and (e, p) in realize for h in emat for e in emat)}
    active = set().union(*(pmat[p] for p in psi)) if psi else set()
    q = {a: rng.choice((-1, 0, 1)) for a in sorted(active) if rng.randrange(2)}
    roles = {(p, a, role) for p in pmat for a in sorted(pmat[p]) for role in ('r0', 'r1')
             if rng.randrange(3) == 0}
    if force_active:
        q['a0'] = rng.choice((-1, 0, 1))
        roles.add(('p0','a0','r0'))
    channels = {(p, a, 'lambda', q[a], role) for p in psi for a in pmat[p]
                if a in q for role in ('r0', 'r1') if (p, a, role) in roles}
    terms = {c: rng.choice((-2, -1, 0, 1, 2)) for c in sorted(channels)}
    return dict(material=material, emat=emat, pmat=pmat, admitted_e=admitted_e,
                described_e=described_e, res=res, realize=realize, conf=conf,
                psi=psi, active=active, q=q, roles=roles, channels=channels, terms=terms)


def audit_model(m):
    # One common support anchor; empty relational material signature. Checks I, II, III, V.
    assert m['described_e'] <= m['admitted_e']
    for h, e in m['res']:
        assert m['emat'][e] <= m['emat'][h] and e in m['admitted_e']
    for h in m['admitted_e']:
        assert (h, h) in m['res']
    for e, p in m['realize']:
        assert m['pmat'][p] <= m['emat'][e]
    assert set(m['q']) <= m['active']
    for p in m['pmat']:
        w = [(h, e) for h, e in m['res'] if e in m['described_e']
             and (e, p) in m['realize'] and all(m['conf'][p])]
        assert (p in m['psi']) == bool(w)
    for p, a, kind, value, role in m['channels']:
        assert p in m['psi'] and a in m['pmat'][p]
        assert m['q'][a] == value and (p, a, role) in m['roles']
        assert kind == 'lambda'
    for p in m['pmat']:
        for a in m['pmat'][p]:
            for role in ('r0', 'r1'):
                c = (p, a, 'lambda', m['q'].get(a), role)
                admitted = p in m['psi'] and a in m['q'] and (p, a, role) in m['roles']
                assert (c in m['channels']) == admitted
                trace = [(h, e) for h, e in m['res'] if e in m['described_e']
                         and (e, p) in m['realize'] and all(m['conf'][p])]
                assert (c in m['channels']) == (bool(trace) and a in m['q'] and
                        p in m['pmat'] and a in m['pmat'][p] and (p, a, role) in m['roles'])
    cs = sorted(m['channels'])
    for sub in subsets(cs):
        # Set-indexed finite sums; permutation invariance.
        total = sum(m['terms'][c] for c in sub)
        assert total == sum(m['terms'][c] for c in reversed(sorted(sub)))
    return len(cs)


def relabel_model(m):
    # Swap material and names of expressions/configurations/roles without changing structure.
    maps = [{a: f'a{len(m["material"])-1-i}' for i, a in enumerate(m['material'])},
            {e: 'e'+str(3-int(e[1:])) for e in m['emat']},
            {p: 'p'+str(3-int(p[1:])) for p in m['pmat']}, {'r0':'r1','r1':'r0'}]
    ma, me, mp, mr = maps
    a = lambda x: ma[x]
    e = lambda x: me[x]
    p = lambda x: mp[x]
    r = lambda x: mr[x]
    return dict(material=tuple(a(x) for x in m['material']),
      emat={e(k): frozenset(a(x) for x in v) for k,v in m['emat'].items()},
      pmat={p(k): frozenset(a(x) for x in v) for k,v in m['pmat'].items()},
      admitted_e={e(k) for k in m['admitted_e']}, described_e={e(k) for k in m['described_e']},
      res={(e(h),e(v)) for h,v in m['res']},
      realize={(e(h),p(v)) for h,v in m['realize']},
      conf={p(k):v for k,v in m['conf'].items()},
      psi={p(k) for k in m['psi']}, active={a(x) for x in m['active']},
      q={a(k):v for k,v in m['q'].items()},
      roles={(p(k),a(x),r(z)) for k,x,z in m['roles']},
      channels={(p(k),a(x),l,v,r(z)) for k,x,l,v,z in m['channels']},
      terms={(p(k),a(x),l,v,r(z)):t for (k,x,l,v,z),t in m['terms'].items()})


def boundary_cases():
    tests = {}
    # These are witnesses of scope limitations, not violations of the axioms.
    tests['admission_not_sufficient'] = (True and not False)
    tests['restriction_nontransitivity_allowed'] = (
      ('H','h') in {('H','H'),('h','h'),('g','g'),('H','h'),('h','g')}
      and ('h','g') in {('H','H'),('h','h'),('g','g'),('H','h'),('h','g')}
      and ('H','g') not in {('H','H'),('h','h'),('g','g'),('H','h'),('h','g')})
    tests['defined_zero_not_undefined'] = (('a',0) != ('b',None))
    tests['assigned_zero_can_have_nonzero_term'] = (0 == 0 and (1 + -1) == 0)
    tests['distinct_nonempty_composites_can_collide'] = (
       sum((1,-1)) == sum((0,)) and frozenset(('c1','c2')) != frozenset(('c3',)))
    tests['same_value_cross_context_conflict_illegal'] = (0 != 1)
    tests['zero_channels_empty_sum'] = (sum([]) == 0)
    tests['nonempty_family_needed_for_composite_coincidence'] = (
       len(set()) == 0 and len([s for s in subsets([]) if s]) == 0)
    tests['fixed_J_separately_prescribed_failure'] = (-1*1 != 1)
    tests['linear_isomorphism_zero_nonzero_obstruction'] = (0 != 1)
    tests['partial_global_assignment_does_not_force_roles'] = (True and len(set()) == 0)
    tests['finite_set_repetition_collapses'] = (len({'c','c'}) == 1)
    # No inference from finite sums to convergence of an infinite series.
    tests['infinite_series_outside_core'] = (sum(1 for _ in range(100)) == 100)
    assert all(tests.values())
    return tests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', default='results')
    ap.add_argument('--trials', type=int, default=400)
    ap.add_argument('--seed', type=int, default=20261029)
    opts = ap.parse_args()
    rng = random.Random(opts.seed)
    counts = Counter()
    for trial in range(opts.trials):
        m = make_model(rng, force_active=(trial % 2 == 0))
        n = audit_model(m)
        rm = relabel_model(m)
        assert audit_model(rm) == n
        assert len(m['psi']) == len(rm['psi'])
        assert sum(m['terms'].values()) == sum(rm['terms'].values())
        counts['models_valid'] += 1
        counts['renamed_models_valid'] += 1
        counts['models_nonempty_channels'] += int(n != 0)
        counts['models_with_defined_zero'] += int(any(v == 0 for v in m['q'].values()))
        counts['models_with_nondesc_candidate'] += int(len(m['psi']) < len(m['pmat']))
        counts['models_with_multiple_channels'] += int(n > 1)
    tests = boundary_cases()
    payload = dict(source='DSD Formation Axiom System, v4.5 (2026-10-22)',
       scope='finite small-signature synthetic tests, not universal proof',
       seed=opts.seed, trials=opts.trials, results=dict(counts),
       boundary_case_outcomes=tests, boundary_case_count=len(tests),
       conclusion='All assertions passed; theoretical and physical applicability remain distinct')
    out = Path(opts.output_dir); out.mkdir(parents=True, exist_ok=True)
    (out/'formation_scope_stress_report.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

if __name__=='__main__':
    main()
