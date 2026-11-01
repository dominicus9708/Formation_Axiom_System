"""Finite rational countermodels for exact Stage-7 obstruction and symmetry.
Audited Formation Axiom System author: Kwon Dominicus.
This is a finite check, not a proof of all ZFC interpretations.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import json

ROLES=('r0','r1')


def rank_space_rows(terms):
    """RREF rowspace of term matrix (rows: term-space coordinates; cols: channels)."""
    d=len(terms[0]); assert d and all(len(t)==d for t in terms)
    A=[[F(terms[j][i]) for j in range(len(terms))] for i in range(d)]
    piv=0
    for col in range(len(terms)):
        k=next((k for k in range(piv,d) if A[k][col]),None)
        if k is None: continue
        A[piv],A[k]=A[k],A[piv]
        fac=A[piv][col]
        A[piv]=[x/fac for x in A[piv]]
        for r in range(d):
            if r != piv:
                mult=A[r][col]
                A[r]=[A[r][i]-mult*A[piv][i] for i in range(len(terms))]
        piv+=1
        if piv==d:break
    return tuple(tuple(row) for row in A if any(row))


def model(terms, role_names=ROLES):
    assert len(terms)==2 and len(set(role_names))==2
    d=len(terms[0]);assert all(len(t)==d for t in terms)
    result={
        'M':('a',),'E':('h',),'P':('p',),'K':('lambda',),'V':{'lambda':('0',)},
        'R':tuple(role_names),'support':{'a':'s'},
        'mat':{'h':('a',)},'act':{'p':('a',)},
        'adm':('h',),'des':('h',),'res':(('h','h'),),'real':(('h','p'),),
        'conf':('p',),'q':{'lambda':{'a':'0'}},
        'roles':tuple(('p','a','lambda',r) for r in role_names),
        'terms':{r:tuple(F(v) for v in t) for r,t in zip(role_names,terms)},
        'term_dimension':d}
    return result


def valid(m):
    assert m['mat']['h']==m['act']['p']==('a',)
    assert m['res']==(('h','h'),) and m['real']==(('h','p'),)
    assert m['adm']==m['des']==('h',)
    assert m['q']['lambda']=={'a':'0'}
    assert set(m['terms'])==set(m['R'])
    assert m['term_dimension']>=1
    assert all(len(v)==m['term_dimension'] for v in m['terms'].values())
    return True


def stage7_possible(L,M):
    assert valid(L) and valid(M)
    # At stages 0-6 the models have matching primitive data.  The term map J
    # in a full comparison tuple is unconstrained until stage 7.
    assert L['term_dimension']>=1 and M['term_dimension']>=1
    # J must be bijective linear at Stage 7; hence dimensions must agree.
    if L['term_dimension'] != M['term_dimension']:return False
    source=[L['terms'][r] for r in L['R']]
    # Two role bijections: source role r_i -> target role target_perm_i.
    for perm in permutations(M['R']):
        target=[M['terms'][r] for r in perm]
        # Existence J in GL_d(Q) such that J source_i = target_i
        # iff the two term matrices have the same kernel.
        if rank_space_rows(source)==rank_space_rows(target):
            return True
    return False


def case(name,L,M,expected):
    assert valid(L) and valid(M)
    # Independently check that the Stage-0 through Stage-6 primitive data
    # agree up to the explicitly allowed bijection of the role carrier.
    for k in ('M','E','P','K','V','support','mat','act','adm','des',
              'res','real','conf','q'):
        assert L[k]==M[k], (name,k)
    assert len(L['R'])==len(M['R'])==2
    assert L['roles']==tuple(('p','a','lambda',r) for r in L['R'])
    assert M['roles']==tuple(('p','a','lambda',r) for r in M['R'])
    p=stage7_possible(L,M)
    r=stage7_possible(M,L)
    assert p==r==expected,(name,p,r)
    return {'stages_0_through_6_nonempty':True,'stage_7_nonempty':p,
        'first_branch':None if p else 7,'reverse_first_branch':None if r else 7,
        'source_term_dimension':L['term_dimension'],
        'target_term_dimension':M['term_dimension'],
        'source_rowspace_rank':len(rank_space_rows([L['terms'][r] for r in L['R']])),
        'target_rowspace_rank':len(rank_space_rows([M['terms'][r] for r in M['R']]))}


def run():
    basis=model(((1,0),(0,1)))
    collapsed=model(((1,1),(0,0)))
    dim1=model(((1,),(1,)))
    unequal_ratio=model(((1,0),(2,0)))
    equal_ratio=model(((1,0),(1,0)))
    transported=model(((2,1),(1,1)))
    different_roles=model(((1,1),(2,1)),('x','y'))
    cases={
        'rank_obstruction_same_finite_sum':case('rank',basis,collapsed,False),
        'term_space_dimension_obstruction':case('dimension',basis,dim1,False),
        'same_rank_different_linear_dependence':case('dependency',equal_ratio,unequal_ratio,False),
        'invertible_term_transport':case('positive',basis,transported,True),
        'roles_relabel_and_invertible_transport':case('relabel',basis,different_roles,True),
    }
    assert tuple(map(sum,zip(*[basis['terms'][r] for r in basis['R']]))) == tuple(map(sum,zip(*[collapsed['terms'][r] for r in collapsed['R']])))
    return {
        'status':'PASS_FINITE_STAGE7_OBSTRUCTIONS_AND_STRICT_ISOMORPHISMS',
        'cases':cases,'number_of_checked_pairs':len(cases),
        'note':'Pairwise exact rational tests on two-channel full models; stages0-6 survive because primitive structures are identical up to role renaming. The general theorems still require mathematical proof.',
        'core_proof_condition':'GL_d(Q) term transport exists iff the source and target term matrices have equal kernels and equal ambient dimension; possible role bijections enumerated.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',default='results');a=p.parse_args()
    output=Path(a.output_dir);output.mkdir(parents=True,exist_ok=True)
    path=output/'formation_phase8_stage7_obstructions.json'
    path.write_text(json.dumps(run(),indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS Phase8: 3 b=7 pairs, 2 strict-isomorphism pairs; symmetry exact')
if __name__=='__main__':main()
