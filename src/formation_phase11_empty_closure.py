#!/usr/bin/env python3
"""Exact finite edge fixtures for Formation v4.5 relative definitional closure.

These fixtures are explanatory finite tests, not complete general proof checks.
Audited-paper author: Kwon Dominicus.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from fractions import Fraction


def close_formation(materials, expressions, configs, adm_expr, des_expr,
                    res, realize, adm_cfg, lc, bc, active, assigned,
                    kinds, roles, role_records, term_values, assigned_domains):
    if not des_expr <= adm_expr:
        raise ValueError('Primitive Axiom I violated')
    # Each chosen active-material set is well-typed; anchor inheritance is
    # stipulated identically in the two nonempty-candidate fixtures.
    assert all(set(active[p]) <= set(materials) for p in configs)
    assert all(p in configs and a in materials and k in kinds and r in roles
               for (p,a,k,r) in role_records)
    psi = {p for p in configs if p in adm_cfg and p in lc and p in bc and
           any((H,h) in res and h in des_expr and (h,p) in realize
               for H in expressions for h in expressions)}
    described_material = set().union(*(active[p] for p in psi)) if psi else set()
    if not all(assigned_domains[k] <= described_material for k in kinds):
        raise ValueError('Primitive Axiom V violated')
    channels = frozenset((p,a,k,assigned[k][a],r)
                         for p in psi for a in active[p] for k in kinds
                         if a in assigned_domains[k]
                         for r in roles
                         if (p,a,k,r) in role_records)
    # Term-value map is supplied for precisely the derived C-domain after Stage VI.
    assert set(term_values) == {(p,a,k,r) for (p,a,k,v,r) in channels}
    ts = { (p,a,k,v,r):term_values[(p,a,k,r)] for (p,a,k,v,r) in channels }
    all_finite_families = []
    c = sorted(channels)
    for mask in range(1<<len(c)):
        f=frozenset(c[i] for i in range(len(c)) if mask&(1<<i))
        all_finite_families.append({'channels':len(f),'sum':str(sum((ts[x] for x in f),Fraction(0)))})
    return {'stage4_psi_count':len(psi), 'stage4_described_material_count':len(described_material),
            'stage6_channels':len(channels),'stage7_family_count':len(all_finite_families),
            'stage7_composites':all_finite_families}


def run():
    cases={}
    common=dict(materials={'a'},expressions=set(),configs=set(),adm_expr=set(),des_expr=set(),
                res=set(),realize=set(),adm_cfg=set(),lc=set(),bc=set(),active={},assigned={},
                kinds=set(),roles=set(),role_records=set(),term_values={},assigned_domains={})
    cases['no_candidates_any_kind']=close_formation(**common)
    q={**common,'kinds':{'lambda'},'assigned':{'lambda':{}},'assigned_domains':{'lambda':set()}}
    cases['empty_configs_nonempty_kind']=close_formation(**q)
    # q undefined, role provisioned but no channels (not a value 0)
    r={**q, 'expressions':{'h'},'configs':{'p'},'adm_expr':{'h'},'des_expr':{'h'},
       'res':{('h','h')},'realize':{('h','p')},'adm_cfg':{'p'},'lc':{'p'},'bc':{'p'},
       'active':{'p':{'a'}}, 'roles':{'rho'}, 'role_records':{('p','a','lambda','rho')}}
    cases['describable_but_unassigned']=close_formation(**r)
    # Once assigning explicit zero, channel present while composite still zero.
    s={**r,'assigned':{'lambda':{'a':'0'}},'assigned_domains':{'lambda':{'a'}},
       'term_values':{('p','a','lambda','rho'):Fraction(0)}}
    cases['explicit_zero_channel']=close_formation(**s)
    assert [cases[k]['stage6_channels'] for k in cases]==[0,0,0,1]
    assert [cases[k]['stage7_family_count'] for k in cases]==[1,1,1,2]
    assert cases['describable_but_unassigned']['stage4_psi_count']==1
    assert cases['explicit_zero_channel']['stage4_psi_count']==1
    return {'status':'PASS_FOUR_FINITE_DEGENERATE_CLOSURE_CASES',
            'cases':cases,
            'proof_scope':'Finite typed fixture checks only; the general uniqueness of relative closure is a mathematical definitional argument, not proved by four samples.',
            'source':'Formation v4.5 Clauses IV/VI/VII, Axiom V and Theorem 3.3'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',default='results');a=p.parse_args()
    out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    target=out/'formation_phase11_empty_closure.json'
    target.write_text(json.dumps(run(),sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS 4 degenerate cases: 3 empty-channel closures and 1 admitted zero-channel closure')

if __name__ == '__main__':main()
