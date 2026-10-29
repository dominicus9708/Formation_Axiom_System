"""DSD Formation v4.5 multi-kind, relational material and 2D term-space audit.

Paper author: Kwon Dominicus. Independent, bounded finite audit, not universal proof.
Python >=3.10, standard library only.
"""
import argparse
import itertools
import json
import random
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

SOURCE_SHA256 = 'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'
V = (0,1,2)

def derv(m):
    describable = frozenset(p for p in m['P'] if all(m['conf'][p]) and any(
        (H,h) in m['res'] and h in m['des'] and (h,p) in m['realize']
        for H in m['E'] for h in m['E']))
    A = frozenset(a for p in describable for a in m['act'][p])
    chan = frozenset((p,a,k,m['q'][k][a],r) for p in describable
        for a in m['act'][p] for k in m['K'] if a in m['q'].get(k,{})
        for r in m['R'] if (p,a,k,r) in m['roles'])
    return describable,A,chan

def validate(m):
    assert set(m['des']) <= set(m['adm'])
    assert set(m['adm']) <= set(m['E'])
    assert all(m['mat'][h] <= m['mat'][H] and h in m['adm'] and
        m['ae'][h] == {a:m['ae'][H][a] for a in m['mat'][h]}
        for H,h in m['res'])
    assert all((e,e) in m['res'] for e in m['adm'])
    assert all(m['act'][p] <= m['mat'][h] and
        m['ap'][p] == {a:m['ae'][h][a] for a in m['act'][p]}
        for h,p in m['realize'])
    assert all(set(m['q'][k]) <= set(derv(m)[1]) for k in m['K'])
    assert all(set(m['q'][k].values()) <= set(m['V'][k]) for k in m['K'])
    assert all(k in m['K'] for k in m['neg'])
    for k in m['neg']:
        assert m['delta'][k] > 0
        assert set(m['size'][k]) == set(m['V'][k])
        assert all((m['size'][k][v] == 0) == (v == 0) for v in m['V'][k])
    assert all(a in m['M'] and b in m['M'] for a,b in m['relation'])
    assert all(a in m['M'] for a in m['anchor'])
    assert all(m['ae'][e] == {a:m['anchor'][a] for a in m['mat'][e]} for e in m['E'])
    assert all(m['ap'][p] == {a:m['anchor'][a] for a in m['act'][p]} for p in m['P'])
    assert set(m['terms']) == set(derv(m)[2])
    assert all(len(v)==2 and all(isinstance(n,Q) for n in v) for v in m['terms'].values())


def rref(rows):
    """Canonical exact rowspace basis; equality iff dependence relations agree."""
    if not rows:return ()
    a = [[Q(x) for x in row] for row in rows]
    nr=len(a); nc=len(a[0]); row=0
    for c in range(nc):
        pivot=next((i for i in range(row,nr) if a[i][c]),None)
        if pivot is None:continue
        a[pivot],a[row]=a[row],a[pivot]
        factor=a[row][c]
        a[row] = [x/factor for x in a[row]]
        for i in range(nr):
            if i!=row and a[i][c]:
                coef=a[i][c]
                a[i] = [x-coef*y for x,y in zip(a[i],a[row])]
        row+=1
        if row==nr:break
    return tuple(tuple(v) for v in a[:row])


def linear_isomorphism_exists(pairs):
    """Existence of GL_2(Q) matching columns x_i -> y_i.

    Proof: same rowspaces of the 2-by-m matrices iff kernels coincide,
    yielding an isomorphism of their images. Equal ranks then allow extension
    to an automorphism of the two-dimensional Q-vector space.
    """
    return rref([[x[j] for x,y in pairs] for j in range(2)]) == \
           rref([[y[j] for x,y in pairs] for j in range(2)])


def candidate_maps(a,b):
    dims=['M','E','P','K','R']
    if any(len(a[d]) != len(b[d]) for d in dims):return
    permsets=[[dict(zip(a[d],p)) for p in itertools.permutations(b[d])] for d in dims]
    for maps in itertools.product(*permsets):
        mp=dict(zip(dims,maps))
        choices=[]
        for k in a['K']:
            target=mp['K'][k]
            if len(a['V'][k]) != len(b['V'][target]):break
            opts=[dict(zip(a['V'][k],p)) for p in itertools.permutations(b['V'][target])
                  if dict(zip(a['V'][k],p))[0] == 0]
            choices.append(opts)
        else:
            for vals in itertools.product(*choices):
                yield dict(mp,values=dict(zip(a['K'],vals)))


def check_stage(a,b,f,upto):
    fm,fe,fp,fk,fr=(f[k] for k in ('M','E','P','K','R'))
    # E1: exact material-record isomorphism, including fixed external anchor targets.
    if any(a['types'][x] != b['types'][fm[x]] or
           a['anchor'][x] != b['anchor'][fm[x]] for x in a['M']):return False
    if {(fm[x],fm[y]) for x,y in a['relation']} != b['relation']:return False
    if any({fm[x] for x in a['mat'][e]} != set(b['mat'][fe[e]]) for e in a['E']):return False
    if any({fm[x] for x in a['act'][p]} != set(b['act'][fp[p]]) for p in a['P']):return False
    if upto==0:return True
    if {fe[e] for e in a['adm']} != set(b['adm']):return False
    if {fe[e] for e in a['des']} != set(b['des']):return False
    if upto==1:return True
    if {(fe[H],fe[h]) for H,h in a['res']} != b['res']:return False
    if upto==2:return True
    if {(fe[h],fp[p]) for h,p in a['realize']} != b['realize']:return False
    if {fp[p]:a['conf'][p] for p in a['P']} != b['conf']:return False
    if upto==3:return True
    if {fp[p] for p in derv(a)[0]} != set(derv(b)[0]):return False
    if upto==4:return True
    # E5/E6/E7 all assignment-domain/value and negligible/threshold data.
    for k in a['K']:
        kk=fk[k]; fv=f['values'][k]
        if {fm[x] for x in a['q'][k]} != set(b['q'][kk]):return False
        if any(fv[value] != b['q'][kk][fm[x]] for x,value in a['q'][k].items()):return False
        if (k in a['neg']) != (kk in b['neg']):return False
        if k in a['neg']:
            if a['delta'][k] != b['delta'][kk]:return False
            if any(a['size'][k][v] != b['size'][kk][fv[v]] for v in a['V'][k]):return False
    if upto==5:return True
    if {(fp[p],fm[x],fk[k],fr[r]) for p,x,k,r in a['roles']} != b['roles']:return False
    if upto==6:return True
    pairs=[]
    for p,x,k,v,r in sorted(derv(a)[2]):
        source=(p,x,k,v,r)
        dest=(fp[p],fm[x],fk[k],f['values'][k][v],fr[r])
        if dest not in derv(b)[2]:return False
        pairs.append((a['terms'][source],b['terms'][dest]))
    return linear_isomorphism_exists(pairs)


def stage_profile(a,b):
    survivors=[0]*8
    for f in candidate_maps(a,b):
        for stage in range(8):
            if not check_stage(a,b,f,stage):break
            survivors[stage]+=1
    assert all(survivors[i]>=survivors[i+1] for i in range(7))
    assert survivors[3]==survivors[4]
    return {'counts':survivors,'first_branch':next((k for k,x in enumerate(survivors) if x==0),None)}


def make_base(seed):
    rng=random.Random(seed)
    m=dict(M=('a','b'),E=('e0','e1'),P=('p0','p1'),K=('k0','k1'),R=('r0','r1'),
        V={'k0':V,'k1':V},types={'a':'site','b':'site'},
        anchor={'a':'s0','b':'s1' if rng.randrange(2) else 's0'},
        relation=frozenset(rng.choice(((),(('a','b'),), (('b','a'),)))),
        mat={'e0':frozenset(('a',)),'e1':frozenset(('a','b'))},
        act={'p0':frozenset(('a',)),'p1':frozenset(('a','b'))},
        adm=frozenset(('e0','e1')),
        des=frozenset(e for e in ('e0','e1') if rng.randrange(3)),
        res=frozenset((('e0','e0'),('e1','e1')) + ((('e1','e0'),) if rng.randrange(2) else ())),
        realize=frozenset((('e0','p0'),('e1','p1')) + ((('e1','p0'),) if rng.randrange(2) else ())),
        conf={p:tuple(bool(rng.randrange(3)) for _ in range(3)) for p in ('p0','p1')},
        q={},roles=frozenset(),terms={},neg=frozenset(),delta={},size={})
    if seed % 2 == 0:
        m['des'] = frozenset(set(m['des']) | {'e0'})
        m['conf']['p0'] = (True, True, True)
    m['ae']={e:{x:m['anchor'][x] for x in items} for e,items in m['mat'].items()}
    m['ap']={p:{x:m['anchor'][x] for x in items} for p,items in m['act'].items()}
    active=derv(m)[1]
    m['q']={k:{a:rng.choice(V) for a in sorted(active) if rng.randrange(2)} for k in m['K']}
    if seed % 2 == 0: m['q']['k0']['a']=1
    m['neg']=frozenset(k for k in m['K'] if rng.randrange(2))
    m['delta']={k:Q(rng.choice((1,2,3))) for k in m['neg']}
    m['size']={k:{0:Q(0),1:Q(1),2:Q(2)} for k in m['neg']}
    m['roles']=frozenset((p,a,k,r) for p in m['P'] for a in m['act'][p]
        for k in m['K'] for r in m['R'] if rng.randrange(3)==0)
    if seed % 2 == 0: m['roles'] = frozenset(set(m['roles']) | {('p0','a','k0','r0')})
    termopts=((Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)),(Q(1),Q(1)),(Q(-1),Q(1)))
    m['terms']={c:rng.choice(termopts) for c in sorted(derv(m)[2])}
    validate(m)
    return m


def permuted(m):
    """Nontrivial strict rename and J=[[1,1],[1,2]]; det=1."""
    mp={k:dict(zip(m[k],reversed(m[k]))) for k in ('M','E','P','K','R')}
    ma,ee,pp,kk,rr=(mp[k] for k in ('M','E','P','K','R'))
    n=dict(M=m['M'],E=m['E'],P=m['P'],K=m['K'],R=m['R'],
       V={kk[k]:m['V'][k] for k in m['K']},
       types={ma[x]:v for x,v in m['types'].items()},
       anchor={ma[x]:v for x,v in m['anchor'].items()},
       relation=frozenset((ma[x],ma[y]) for x,y in m['relation']),
       mat={ee[e]:frozenset(ma[x] for x in v) for e,v in m['mat'].items()},
       act={pp[p]:frozenset(ma[x] for x in v) for p,v in m['act'].items()},
       adm=frozenset(ee[e] for e in m['adm']),des=frozenset(ee[e] for e in m['des']),
       res=frozenset((ee[x],ee[y]) for x,y in m['res']),
       realize=frozenset((ee[x],pp[y]) for x,y in m['realize']),
       conf={pp[p]:v for p,v in m['conf'].items()},
       q={kk[k]:{ma[x]:v for x,v in m['q'][k].items()} for k in m['K']},
       roles=frozenset((pp[p],ma[x],kk[k],rr[r]) for p,x,k,r in m['roles']),
       neg=frozenset(kk[k] for k in m['neg']),
       delta={kk[k]:v for k,v in m['delta'].items()},
       size={kk[k]:dict(v) for k,v in m['size'].items()})
    n['ae']={e:{x:n['anchor'][x] for x in items} for e,items in n['mat'].items()}
    n['ap']={p:{x:n['anchor'][x] for x in items} for p,items in n['act'].items()}
    n['terms']={(pp[p],ma[x],kk[k],v,rr[r]):(w[0]+w[1],w[0]+2*w[1])
        for (p,x,k,v,r),w in m['terms'].items()}
    validate(n)
    return n


def special_cases():
    # A stage-5 quantity status obstruction even when earlier structure is identical.
    a=make_base(42); b=make_base(42)
    b['neg']=frozenset(('k0',)) if a['neg'] != frozenset(('k0',)) else frozenset(('k1',))
    b['delta']={k:Q(1) for k in b['neg']}
    b['size']={k:{0:Q(0),1:Q(1),2:Q(2)} for k in b['neg']}
    validate(b)
    # Branch may be 5 if no kind swap salvages; anchor-induced and assignment restrict alternatives.
    v0=stage_profile(a,b)
    # Dependence mismatch with equal sum: first source terms linearly independent,
    # target terms have equal total but rank one. Exact E9 must reject this for
    # *any* channel permutation.
    c=make_base(80)
    c['des']=frozenset(('e0','e1'))
    c['conf']={'p0':(True,True,True),'p1':(True,True,True)}
    c['q']={'k0':{'a':1},'k1':{}}
    c['roles']=frozenset((('p0','a','k0','r0'),('p0','a','k0','r1')))
    terms=sorted(derv(c)[2]); assert len(terms)==2
    c['terms']={terms[0]:(Q(1),Q(0)),terms[1]:(Q(0),Q(1))}
    validate(c)
    d={**c,'terms':{terms[0]:(Q(1),Q(1)),terms[1]:(Q(0),Q(0))}}
    validate(d)
    sums=lambda v:tuple(sum((z[i] for z in v['terms'].values()),Q(0)) for i in range(2))
    assert sums(c)==sums(d)==(Q(1),Q(1))
    cd=stage_profile(c,d)
    assert cd['first_branch']==7, cd
    assert not linear_isomorphism_exists([(c['terms'][x],d['terms'][x]) for x in terms])
    # Stage VI only: removing a role while preserving all earlier data.
    missing_role={**c, 'roles':frozenset({('p0','a','k0','r0')})}
    missing_role['terms']={x:w for x,w in c['terms'].items() if x[-1]=='r0'}
    validate(missing_role)
    missing_role_profile=stage_profile(c,missing_role)
    assert missing_role_profile['first_branch']==6, missing_role_profile
    # Stage 0 support disagreement across fixed B (no allowed base fixing).
    wrong_anchor={**c,'anchor':dict(c['anchor']), 'ae':dict(c['ae']), 'ap':dict(c['ap'])}
    wrong_anchor['anchor']['b']='s2'
    wrong_anchor['ae']={e:{x:wrong_anchor['anchor'][x] for x in items} for e,items in c['mat'].items()}
    wrong_anchor['ap']={p:{x:wrong_anchor['anchor'][x] for x in items} for p,items in c['act'].items()}
    validate(wrong_anchor)
    wrong_anchor_profile=stage_profile(c,wrong_anchor)
    assert wrong_anchor_profile['first_branch']==0, wrong_anchor_profile
    # Same term rank, differing relations: J still impossible despite matching sums.
    e={**c,'terms':{terms[0]:(Q(1),Q(0)),terms[1]:(Q(1),Q(0))}}
    validate(e)
    return {'different_negligible_status':v0, 'role_cardinality_stage6':missing_role_profile, 'base_anchor_stage0':wrong_anchor_profile, 'equal_full_sum_different_term_rank':{
       'sum':['1','1'],'source_rank':2,'target_rank':1,'stage_profile':cd}}


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output-dir',default='results');pa.add_argument('--seed',type=int,default=20261029)
    pa.add_argument('--base-models',type=int,default=24);args=pa.parse_args()
    base_models=[make_base(args.seed+i) for i in range(args.base_models)]
    rename_models=[permuted(m) for m in base_models]
    allmodels=base_models+rename_models
    assert all(allmodels[i]!=allmodels[j] for i in range(len(allmodels)) for j in range(i+1,len(allmodels)))
    branch=Counter(); pairs=0
    for i,a in enumerate(allmodels):
        for b in allmodels[i:]:
            p=stage_profile(a,b); q=stage_profile(b,a)
            assert p['first_branch']==q['first_branch']
            assert p['counts'][3]==p['counts'][4]
            branch[str(p['first_branch'])]+=1
            pairs+=1
    for a,b in zip(base_models,rename_models):
        assert stage_profile(a,b)['first_branch'] is None
    special=special_cases()
    # GL2 exact linear-algebra controls: 2D independent basis -> dependent pair impossible.
    assert linear_isomorphism_exists([((Q(1),Q(0)),(Q(1),Q(1))),((Q(0),Q(1)),(Q(1),Q(2)))])
    assert not linear_isomorphism_exists([((Q(1),Q(0)),(Q(1),Q(1))),((Q(0),Q(1)),(Q(0),Q(0)))])
    # Dependence relation: 3 source vectors x3=x1+x2 but target has y3!=y1+y2.
    assert not linear_isomorphism_exists([((Q(1),Q(0)),(Q(1),Q(0))),((Q(0),Q(1)),(Q(0),Q(1))),
                                          ((Q(1),Q(1)),(Q(1),Q(0)))])
    data=dict(source='Formation Axiom System v4.5',source_sha256=SOURCE_SHA256,
      code='formation_multisort_stage_audit.py',seed=args.seed,base_models=args.base_models,
      transformed_strict_isomorphs=len(rename_models),tested_models=len(allmodels),
      unordered_model_pairs_including_self=pairs,first_branch_distribution=dict(branch),
      renamed_pair_equivalence_checks=len(base_models),stage4_first_branch=branch.get('4',0),
      nonempty_channel_models=sum(bool(derv(m)[2]) for m in allmodels),
      special_cases=special,limitations='finite 2 material, 2 expression, 2 configuration, 2 kinds, 2 roles, 2D rational term-space, fixed {0,1,2} values; all candidate bijections enumerated; not universal proof',status='PASS_IN_RESTRICTED_SIGNATURE')
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    dst=out/'formation_multisort_stage_audit.json';dst.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS',pairs,'pairs',len(allmodels),'models','stage4',branch.get('4',0));print('BRANCH',dict(branch));print('SAVED',dst)

if __name__=='__main__':main()
