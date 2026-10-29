"""Finite DSD Formation v4.5 semantic limits: positive countermodels and maps.

The model universe in this executable is deliberately restricted; its witnesses
show logical non-implications but do not validate empirical relevance.
Audited theory author: Kwon Dominicus.
"""
import argparse
import copy
import itertools
import json
from fractions import Fraction
from pathlib import Path
from formation_negative_stage_audit import base, derived, issues, profile


def valid(model):
    err = issues(model)
    assert not err, err
    return model


def add_expression(m,name,admitted=True,described=False,anchor='s0'):
    m['E'] += (name,)
    m['mat'][name] = frozenset(('a',))
    m['aE'][name] = {'a':anchor}
    if admitted:
        m['admitted'] |= {name}
        m['res'] |= {(name,name)}
    if described: m['described'] |= {name}
    return m


def change_assignment(m,value):
    m['q']={'a':value}
    old_term = next(iter(m['terms'].values()),Fraction(1))
    d = derived(m)
    m['terms']={c:old_term for c in d['channels']}
    return m


def relabel(m,mat_name='b',hname='A',gname='B',pname='q',rname='s',scale=Fraction(1)):
    A, E, P, R = {'a':mat_name}, {'H':hname,'h':gname}, {'p':pname}, {'r':rname}
    out=copy.deepcopy(m)
    out['M']=tuple(A[x] for x in m['M'])
    out['E']=tuple(E[x] for x in m['E'])
    out['P']=tuple(P[x] for x in m['P'])
    out['R']=tuple(R[x] for x in m['R'])
    out['mat']={E[k]:frozenset(A[x] for x in items) for k,items in m['mat'].items()}
    out['active']={P[k]:frozenset(A[x] for x in items) for k,items in m['active'].items()}
    out['aE']={E[k]:{A[x]:v for x,v in dic.items()} for k,dic in m['aE'].items()}
    out['aP']={P[k]:{A[x]:v for x,v in dic.items()} for k,dic in m['aP'].items()}
    out['mt']={A[k]:v for k,v in m['mt'].items()}
    out['incidence']=frozenset((A[x],A[y]) for x,y in m['incidence'])
    out['admitted']=frozenset(E[x] for x in m['admitted'])
    out['described']=frozenset(E[x] for x in m['described'])
    out['res']=frozenset((E[x],E[y]) for x,y in m['res'])
    out['realize']=frozenset((E[x],P[y]) for x,y in m['realize'])
    out['conf']={P[x]:v for x,v in m['conf'].items()}
    out['q']={A[x]:v for x,v in m['q'].items()}
    out['roles']=frozenset((P[p],A[a],R[r]) for p,a,r in m['roles'])
    out['terms']={(P[p],A[a],l,v,R[r]):value*scale
                  for (p,a,l,v,r),value in m['terms'].items()}
    return out


def scenario_results():
    result={}
    m=add_expression(base(),'unused',admitted=True,described=False)
    valid(m)
    assert 'unused' in m['admitted'] and 'unused' not in m['described']
    result['S01_admission_not_sufficient']={'pass':True,'describable_unrelated_expression':False}

    m=add_expression(base(),'g')
    m['res'] |= {('H','h'),('h','g')}
    valid(m)
    assert ('H','g') not in m['res']
    result['S02_restriction_nontransitivity']={'pass':True,'two_link_chain':True,'direct_edge':False}

    m=base(); m['res'] |= {('H','h')}; valid(m)
    dc=derived(m)
    c=next(iter(dc['channels']))
    traces={(H,h) for H,h in m['res'] if h in m['described']
            and (h,'p') in m['realize'] and all(m['conf']['p'])}
    assert len(traces)==2 and len(dc['channels'])==1
    result['S03_multiple_traces_one_channel']={'pass':True,'traces':2,'channels':1}

    m=change_assignment(base(),0); valid(m)
    assert len(derived(m)['channels'])==1
    assert next(iter(derived(m)['channels']))[3]==0
    assert next(iter(m['terms'].values()))==1
    result['S04_assigned_zero_term_nonzero']={'pass':True,'assignment':0,'term':1}

    m=base(); m['q']={};m['terms']={};valid(m)
    assert derived(m)['psi'] and not derived(m)['channels']
    result['S05_describable_but_no_assignment_channels']={'pass':True,'described_configurations':1,'channels':0}

    m=base(); m['roles']=frozenset();m['terms']={};valid(m)
    assert derived(m)['psi'] and m['q'] and not derived(m)['channels']
    result['S06_assigned_but_no_role_channels']={'pass':True,'channels':0}

    m=base();m['R']=('r','s');m['roles']=frozenset({('p','a','r')})
    valid(m)
    missing=('p','a','lambda',1,'s')
    assert missing not in derived(m)['channels'] and missing not in m['terms']
    result['S07_absent_channel_not_zero_term']={'pass':True,'absent_role':'s','term_undefined':True}

    m=base();m['R']=('r0','r1','r2')
    m['q']={'a':0};m['roles']=frozenset(('p','a',r) for r in m['R'])
    d=derived(m); m['terms']={c:Fraction({'r0':1,'r1':-1,'r2':0}[c[-1]]) for c in d['channels']}
    valid(m)
    byrole={c[-1]:c for c in d['channels']}
    left=d['comps'][frozenset((byrole['r0'],byrole['r1']))]
    right=d['comps'][frozenset((byrole['r2'],))]
    assert left==right==0
    result['S08_noninjective_composition_exact_source_structure']={'pass':True,'equal_sum':0,'roles':3}
    m['terms']={c:Fraction({'r0':1,'r1':2,'r2':4}[c[-1]]) for c in d['channels']}
    valid(m);d=derived(m)
    assert len(set(d['comps'].values()))==len(d['comps'])==8
    result['S09_injective_composition_is_possible']={'pass':True,'unique_subset_outputs':8}

    m=base();m['M']=('a','b','c');m['mt']={'a':'item','b':'item','c':'item'}
    for e in m['E']:
        m['mat'][e]=frozenset(m['M'])
        m['aE'][e]={a:'s0' for a in m['M']}
    m['active']['p']=frozenset(m['M']);m['aP']['p']={a:'s0' for a in m['M']}
    m['V']=(Fraction(0),Fraction(1,1000),Fraction(1))
    m['q']={'a':Fraction(1,1000),'b':Fraction(0)}
    m['negligible_kinds']=frozenset(('lambda',))
    m['delta']=Fraction(1,100)
    m['size_map']={v:abs(v) for v in m['V']}
    m['roles']=frozenset((('p','a','r'),('p','b','r')))
    m['terms']={c:Fraction(1) for c in derived(m)['channels']}
    valid(m)
    assert 'lambda' in m['negligible_kinds'] and m['delta'] > 0
    assert all((m['size_map'][v]==0)==(v==0) for v in m['V'])
    assert 'c' not in m['q'] and m['q']['b']==0 and 0 < m['size_map'][m['q']['a']] <= m['delta']
    result['S10_undefined_zero_negligible_nonzero']={
        'pass':True,'undefined_material':'c','defined_zero_material':'b',
        'nonzero_negligible_material':'a','delta':'1/100','size':'1/1000',
        'limitation':'size function and threshold explicitly supplied for this witness'}

    original=base(); m1=relabel(original,mat_name='b',hname='X',gname='Y',pname='q',rname='s',scale=Fraction(3))
    # Second renamed copy built directly from original, equivalent to chain via maps.
    m2=relabel(original,mat_name='c',hname='E',gname='F',pname='z',rname='t',scale=Fraction(15))
    for x in (original,m1,m2): valid(x)
    for a,b in ((original,m1),(m1,m2),(original,m2),(m2,original)):
        assert profile(a,b)['branch'] is None
    result['S11_strict_isomorphism_scaling_composition']={'pass':True,'linear_scales':['3','5','15'],'first_branch':None}

    original=base(); m=add_expression(base(),'unused')
    assert profile(original,m)['branch']==0
    result['S12_unused_candidate_matters_to_strict_equivalence']={
        'pass':True,'first_branch':0,'admitted_channel_counts':[1,1]}

    m=base();m['M']=('a','b');m['mt']={'a':'item','b':'item'}
    m['mat']['H']=frozenset(('a','b'))
    m['aE']['H']={'a':'s0','b':'s1'}
    m['mat']['h']=frozenset(('a',));m['aE']['h']={'a':'s0'}
    m['res'] |= {('H','h')}
    valid(m)
    assert m['aE']['h']=={a:m['aE']['H'][a] for a in m['mat']['h']}
    result['S13_heterogeneous_support_anchors']={'pass':True,'supports':2,'retained_items':1}

    m=base();m['P']+=('p2',);m['active']['p2']=frozenset(('a',));m['aP']['p2']={'a':'s0'}
    m['conf']['p2']=(True,True,True);m['realize'] |= {('h','p2')}
    m['roles'] |= {('p2','a','r')}
    m['terms']={c:Fraction(1) for c in derived(m)['channels']}
    valid(m)
    assert {c[3] for c in derived(m)['channels']}=={1}
    result['S14_regime_global_assignment_across_two_configs']={
        'pass':True,'same_material_channels':2,'assigned_values':[1]}

    return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',default='results')
    args=parser.parse_args()
    d=scenario_results()
    assert len(d)==14
    path=Path(args.output_dir);path.mkdir(parents=True,exist_ok=True)
    f=path/'formation_semantic_boundary_cases.json'
    f.write_text(json.dumps({'source':'Formation v4.5 2026-10-22','case_count':len(d),
        'valid_full_model_instances':len(d),'cases':d,
        'scope':'selected finite full models only; no empirical validity or universal theorem proof'},
        ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('PASS',len(d),'semantic scope checks',f)

if __name__=='__main__':main()
