"""DSD Formation v4.5: independently constructed negative fixtures + stage comparer.

Audited theory author: Kwon Dominicus. This independent limited-scope test
uses a finite relational-empty material signature, one quantity kind, a fixed
finite pointed value set, and real one-dimensional component term spaces.
It does NOT decide strict isomorphism of arbitrary DSD formation models.
"""
import argparse
import copy
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

SOURCE_SHA256 = 'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'


def base():
    return {
        'M': ('a',), 'E': ('H', 'h'), 'P': ('p',), 'R': ('r',),
        'V': (0, 1), 'zero': 0, 'kind': 'lambda',
        'mat': {'H': frozenset(('a',)), 'h': frozenset(('a',))},
        'active': {'p': frozenset(('a',))},
        'aE': {'H': {'a': 's0'}, 'h': {'a': 's0'}},
        'aP': {'p': {'a': 's0'}},
        'mt': {'a': 'item'}, 'incidence': frozenset(),
        'admitted': frozenset(('H', 'h')), 'described': frozenset(('h',)),
        'res': frozenset((('H', 'H'), ('h', 'h'))),
        'realize': frozenset((('h', 'p'),)),
        'conf': {'p': (True, True, True)},
        'q': {'a': 1}, 'roles': frozenset((('p', 'a', 'r'),)),
        'terms': {('p', 'a', 'lambda', 1, 'r'): Fraction(1)},
    }


def derived(m):
    # Definitions 2.1, 3.2 (IV), 3.2 (VI), 3.2 (VII) reproduced independently.
    psi = set()
    for p in m['P']:
        if all(m['conf'][p]) and any(
            (H, h) in m['res'] and h in m['described'] and (h, p) in m['realize']
            for H in m['E'] for h in m['E']):
            psi.add(p)
    A = set().union(*(m['active'][p] for p in psi)) if psi else set()
    channels = frozenset((p, a, m['kind'], m['q'][a], role)
        for p in psi for a in m['active'][p] if a in m['q']
        for role in m['R'] if (p, a, role) in m['roles'])
    families = [frozenset(x) for n in range(len(channels)+1)
                for x in itertools.combinations(sorted(channels), n)]
    comps = {f: sum((m['terms'].get(c, Fraction(0)) for c in f), Fraction(0))
             for f in families}
    return {'psi': frozenset(psi), 'A': frozenset(A), 'channels': channels,
            'families': families, 'comps': comps}


def issues(m, supplied=None):
    """Return named violated obligations; no positive results inferred from absence alone."""
    faults = set()
    if set(m['described']) - set(m['admitted']):
        faults.add('AXIOM_I_DES_IMPL_ADM')
    for H, h in m['res']:
        if h not in m['admitted']:
            faults.add('AXIOM_II_TARGET_ADMISSION')
        if not m['mat'][h].issubset(m['mat'][H]) or m['aE'][h] != {
                a: m['aE'][H][a] for a in m['mat'][h] if a in m['aE'][H]}:
            faults.add('AXIOM_II_ANCHOR_INHERITANCE')
    for H in m['admitted']:
        if (H, H) not in m['res']:
            faults.add('AXIOM_II_IDENTITY_RESTRICTION')
    for h, p in m['realize']:
        if not m['active'][p].issubset(m['mat'][h]) or m['aP'][p] != {
                a: m['aE'][h][a] for a in m['active'][p] if a in m['aE'][h]}:
            faults.add('AXIOM_III_REALIZATION_INHERITANCE')
    d = derived(m)
    if not set(m['q']).issubset(d['A']):
        faults.add('AXIOM_V_ASSIGNMENT_DOMAIN')
    if supplied is not None:
        if supplied.get('psi', d['psi']) != d['psi']:
            faults.add('CLOSURE_IV_STALE_DESCRIBABILITY')
        if supplied.get('channels', d['channels']) != d['channels']:
            faults.add('CLOSURE_VI_STALE_CHANNELS')
        if supplied.get('comps', d['comps']) != d['comps']:
            faults.add('CLOSURE_VII_INCORRECT_SUM')
    if any(c not in m['terms'] for c in d['channels']):
        faults.add('TERM_MAP_NOT_TOTAL_ON_ADMITTED_CHANNELS')
    return sorted(faults)


def new_negative_cases():
    neg = {}
    m = base(); m['E'] += ('x',); m['mat']['x'] = frozenset(('a',)); m['aE']['x'] = {'a': 's0'}
    m['described'] |= {'x'}
    neg['F02_Described_not_admitted'] = (m, 'AXIOM_I_DES_IMPL_ADM')

    m = base(); m['E'] += ('x',); m['mat']['x'] = frozenset(('a',)); m['aE']['x']={'a':'s1'}
    m['admitted'] |= {'x'}; m['res'] |= {('x','x'), ('H','x')}
    neg['F04_Restriction_anchor_changed'] = (m, 'AXIOM_II_ANCHOR_INHERITANCE')

    m = base(); m['E'] += ('x',); m['mat']['x']=frozenset(('a',)); m['aE']['x']={'a':'s0'}
    m['res'] |= {('H','x')}
    neg['F04_Restriction_target_not_admitted'] = (m, 'AXIOM_II_TARGET_ADMISSION')

    m = base(); m['E'] += ('x',); m['mat']['x']=frozenset(('a',)); m['aE']['x']={'a':'s0'}
    m['admitted'] |= {'x'}
    neg['F04_Admitted_expression_no_identity'] = (m, 'AXIOM_II_IDENTITY_RESTRICTION')

    m = base(); m['P'] += ('pbad',); m['active']['pbad']=frozenset(('a',))
    m['aP']['pbad'] = {'a':'s1'}; m['conf']['pbad']=(False,False,False)
    m['realize'] |= {('h', 'pbad')}
    neg['F05_Realization_anchor_changed'] = (m, 'AXIOM_III_REALIZATION_INHERITANCE')

    m = base(); m['M'] += ('b',); m['mt']['b']='item'; m['P'] += ('pbad',)
    m['active']['pbad']=frozenset(('a','b')); m['aP']['pbad']={'a':'s0','b':'s0'}
    m['conf']['pbad']=(False,False,False); m['realize'] |= {('h','pbad')}
    neg['F05_Realization_material_not_retained'] = (m, 'AXIOM_III_REALIZATION_INHERITANCE')

    m = base(); m['M'] += ('b',); m['mt']['b']='item'; m['q']['b']=1
    neg['F06_Assignment_outside_described_material'] = (m, 'AXIOM_V_ASSIGNMENT_DOMAIN')
    return neg


def new_closure_cases():
    m = base(); d = derived(m)
    c = next(iter(d['channels']))
    wrong1 = {'psi': frozenset()}
    wrong2 = {'channels': frozenset()}
    wrong3 = {'comps': {**d['comps'], frozenset((c,)): Fraction(17)}}
    return {
        'IV_stale_derived_status': (wrong1, 'CLOSURE_IV_STALE_DESCRIBABILITY'),
        'VI_stale_derived_channels': (wrong2, 'CLOSURE_VI_STALE_CHANNELS'),
        'VII_stale_composition': (wrong3, 'CLOSURE_VII_INCORRECT_SUM'),
    }


def maps_of(a, b):
    """Enumerate ALL bijections in selected small signature, before stage filtering."""
    keys = ('M','E','P','R')
    if any(len(a[k]) != len(b[k]) for k in keys) or len(a['V']) != len(b['V']):
        return
    if a['kind'] != b['kind']:  # fixed one-kind signature; no kind renaming necessary
        return
    lists = []
    for k in keys:
        lists.append([dict(zip(a[k], perm)) for perm in itertools.permutations(b[k])])
    valmaps = [dict(zip(a['V'], perm)) for perm in itertools.permutations(b['V'])
               if dict(zip(a['V'],perm))[a['zero']] == b['zero']]
    for parts in itertools.product(*lists, valmaps):
        yield dict(zip(keys + ('V',), parts))


def stage_pass(a, b, fm, stage):
    """Exact stages 0..7 for selected signature; J exists iff ratios consistent."""
    mm, ee, pp, rr, vv = (fm[k] for k in ('M','E','P','R','V'))
    # E1, anchored material, typed material structure and relational incidence
    if any(a['mt'][x] != b['mt'][mm[x]] for x in a['M']):
        return False
    if {(mm[x], mm[y]) for x,y in a['incidence']} != set(b['incidence']):
        return False
    for e in a['E']:
        if {mm[x] for x in a['mat'][e]} != set(b['mat'][ee[e]]):
            return False
        if any(a['aE'][e][x] != b['aE'][ee[e]][mm[x]] for x in a['mat'][e]):
            return False
    for p in a['P']:
        if {mm[x] for x in a['active'][p]} != set(b['active'][pp[p]]):
            return False
        if any(a['aP'][p][x] != b['aP'][pp[p]][mm[x]] for x in a['active'][p]):
            return False
    if stage == 0: return True
    # E2
    if {ee[x] for x in a['admitted']} != set(b['admitted']) or \
       {ee[x] for x in a['described']} != set(b['described']):
        return False
    if stage == 1: return True
    # E3 restriction part
    if {(ee[H],ee[h]) for H,h in a['res']} != set(b['res']):
        return False
    if stage == 2: return True
    # E3 realization and E4 primitive config predicates
    if {(ee[h], pp[p]) for h,p in a['realize']} != set(b['realize']) or \
       {pp[p]:flags for p,flags in a['conf'].items()} != b['conf']:
        return False
    if stage == 3: return True
    # definitional closure IV
    da, db = derived(a), derived(b)
    if {pp[p] for p in da['psi']} != set(db['psi']):
        return False
    if stage == 4: return True
    # E5,E6; no negligible kind in this selected signature
    if {mm[x] for x in a['q']} != set(b['q']):
        return False
    if any(b['q'][mm[x]] != vv[v] for x,v in a['q'].items()):
        return False
    if stage == 5: return True
    # E8 role relation
    if {(pp[p],mm[x],rr[r]) for p,x,r in a['roles']} != set(b['roles']):
        return False
    if stage == 6: return True
    # E9, exists nonzero real scalar J(x)=scale*x. One-dimensional W=R.
    for c in da['channels']:
        pc, ac, kind, val, role = c
        d = (pp[pc],mm[ac],kind,vv[val],rr[role])
        if d not in db['channels']:
            return False
    pairs = []
    for c in da['channels']:
        pc, ac, kind, val, role = c
        d = (pp[pc],mm[ac],kind,vv[val],rr[role])
        pairs.append((Fraction(a['terms'][c]), Fraction(b['terms'][d])))
    if any((x == 0) != (y == 0) for x,y in pairs):
        return False
    nonzero_ratios = {y/x for x,y in pairs if x != 0}
    return len(nonzero_ratios) <= 1


def profile(a,b):
    candidates = list(maps_of(a,b))
    sizes = [sum(stage_pass(a,b,f,k) for f in candidates) for k in range(8)]
    assert all(sizes[i] >= sizes[i+1] for i in range(7))
    assert sizes[3] == sizes[4]
    return {'counts': sizes, 'branch': next((i for i,v in enumerate(sizes) if v == 0), None)}


def variants():
    """80 distinct parameterized valid descriptors in this restricted family."""
    flags = list(itertools.product((False, True), repeat=3))
    for h_des, extra_res, conf_flags, assigned, use_role in itertools.product(
            (False, True), (False, True), flags, (False, True), (False, True)):
        if not all(conf_flags) and assigned:
            continue  # otherwise q domain would violate Axiom V
        # A component term can vary only if an admitted channel exists.
        term_options = (0,1,-1) if all(conf_flags) and assigned and use_role else (0,)
        for term in term_options:
            m = base()
            if h_des: m['described'] |= {'H'}
            if extra_res: m['res'] |= {('H','h')}
            m['conf']['p'] = conf_flags
            if not assigned: m['q'] = {}
            if not use_role: m['roles'] = frozenset()
            d = derived(m)
            m['terms'] = {c: Fraction(term) for c in d['channels']}
            assert not issues(m)
            yield m


def run():
    checked = {'negative_cases':{}, 'closure_corruption':{}, 'designed_branches':{},
               'variant_family':{}, 'status':'PASS_IN_DECLARED_FINITE_SIGNATURE'}
    for name,(m,expected) in new_negative_cases().items():
        found = issues(m)
        assert found == [expected], (name, found, expected)
        assert derived(m)['channels'], 'negative case lost nondegenerate active kernel'
        checked['negative_cases'][name] = found
    for name,(cache,expected) in new_closure_cases().items():
        found = issues(base(),cache)
        assert found == [expected], (name,found,expected)
        checked['closure_corruption'][name] = found
    ok = base()
    assert not issues(ok)
    case = {}
    m = copy.deepcopy(ok); m['M'] += ('b',); m['mt']['b'] = 'item'
    case[0] = m
    m = copy.deepcopy(ok); m['described'] |= {'H'}
    case[1] = m
    m = copy.deepcopy(ok); m['res'] |= {('H','h')}
    case[2] = m
    m = copy.deepcopy(ok); m['conf']['p'] = (True,True,False); m['q'] = {}
    m['terms'] = {}
    orig3 = copy.deepcopy(ok); orig3['q'] = {}; orig3['terms'] = {}
    case[3] = (orig3,m)
    m = copy.deepcopy(ok); m['q'] = {}; m['terms'] = {}
    case[5] = m
    m = copy.deepcopy(ok); m['roles'] = frozenset(); m['terms'] = {}
    case[6] = m
    m = copy.deepcopy(ok); m['terms'] = {c:Fraction(0) for c in m['terms']}
    case[7] = m
    for expect, candidate in case.items():
        a,b = candidate if isinstance(candidate,tuple) else (ok,candidate)
        assert not issues(a) and not issues(b), expect
        p = profile(a,b)
        assert p['branch'] == expect, (expect,p)
        assert profile(b,a)['branch'] == expect
        checked['designed_branches'][str(expect)] = p
    # Identity, strict isomorphism and Stage7 scaling in 1D.
    assert profile(ok,ok)['branch'] is None
    scaled = copy.deepcopy(ok); scaled['terms']={c:Fraction(7) for c in ok['terms']}
    assert profile(ok,scaled)['branch'] is None
    checked['designed_branches']['strict_identity'] = profile(ok,ok)
    checked['designed_branches']['nonzero_scalar_J'] = profile(ok,scaled)
    models = list(variants())
    assert len(models) == 80
    assert all(models[i] != models[j] for i in range(len(models))
               for j in range(i + 1, len(models)))
    pair_branches = Counter()
    closure_discrepancies = 0
    asymmetry = 0
    for i,a in enumerate(models):
        for j in range(i,len(models)):
            b = models[j]
            ab = profile(a,b)
            ba = profile(b,a)
            closure_discrepancies += int(ab['counts'][3] != ab['counts'][4])
            asymmetry += int(ab['branch'] != ba['branch'])
            pair_branches[str(ab['branch'])] += 1
    assert closure_discrepancies == asymmetry == 0
    assert '4' not in pair_branches
    checked['variant_family'] = {
       'distinct_parameterized_models':len(models),
       'unordered_pairs_with_diagonal':sum(pair_branches.values()),
       'branch_distribution_unordered':dict(sorted(pair_branches.items())),
       'first_branch_4_cases':0, 'asymmetric_branch_cases':0,
       'note':'All bijections enumerated in the deliberately restricted signature; no claim about unrestricted infinite model classes.'
    }
    checked['scope'] = (
       'Negative Axiom I/II/III/V and closure corruption: 10 source-linked fixtures. '
       'Stage 0-7 comparison: finite one-kind, one-dimensional REAL term space, '
       'fixed value carrier {0,1}, empty material relations, common support anchor; '
       'all carrier bijections enumerated, scalar isomorphism existence solved exactly.'
    )
    checked['source_sha256'] = SOURCE_SHA256
    return checked


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',default='results')
    args=parser.parse_args()
    report = run()
    path = Path(args.output_dir)
    path.mkdir(parents=True,exist_ok=True)
    dest = path/'formation_negative_stage_audit.json'
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf8')
    print('PASS',len(report['negative_cases']),'axiom-negative fixtures',
          len(report['closure_corruption']),'closure-corruption fixtures',
          report['variant_family']['unordered_pairs_with_diagonal'],'pair comparisons',
          'output:',dest)
    print('BRANCH DISTRIBUTION',report['variant_family']['branch_distribution_unordered'])


if __name__ == '__main__':
    main()
