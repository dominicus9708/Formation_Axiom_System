"""Formation v4.5: strict check of two composable multi-sort embeddings.
Paper author: Kwon Dominicus. Source for independent finite Phase-5 continuation.
"""
import argparse
import copy
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
from formation_multirelation_embedding_audit import (
    make_pair,full_model,audit,derived,rebuild,matJ)


def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(2)),Q(0))
                       for j in range(2)) for i in range(2))


def build_triple():
    a,b,f=make_pair()
    n=copy.deepcopy(b)
    n['M']+=('f',)
    n['material_type']['f']='unit';n['support']['f']='s5';n['annotation']['f']='silver'
    n['tri'].add(('b','f','e'))
    for e in ('H','h'):n['mat'][e] |= frozenset(('f',))
    n['act']['p'] |= frozenset(('f',))
    n['K']+=('info',)
    n['V']['info']=(0,1)
    n['V']['energy']=(0,1,2,3)
    n['q']['info']={'f':1}
    n['q']['energy']['f']=3
    n['R']+=('rN',)
    n['roles'].add(('p','f','info','rN'))
    n['roles'].add(('p','f','energy','rN'))
    rebuild(n)
    J2=((Q(1),Q(1)),(Q(0),Q(1)))
    n['terms']={c:(matJ(J2,b['terms'][c]) if c in b['terms'] else (Q(7),Q(3)))
                for c in derived(n)[2]}
    assert full_model(n) is None,full_model(n)
    g={t:{x:x for x in b[ax]} for t,ax in [('m','M'),('e','E'),('p','P'),('k','K'),('r','R')]}
    g['v']={k:{v:v for v in b['V'][k]} for k in b['K']}
    g['J']=J2
    h={t:{k:g[t][v] for k,v in f[t].items()} for t in ('m','e','p','k','r')}
    h['v']={k:{v:g['v'][f['k'][k]][x] for v,x in f['v'][k].items()} for k in a['K']}
    h['J']=mm(J2,f['J'])
    return a,b,n,f,g,h


def run():
    a,b,n,f,g,h=build_triple()
    results={'L_to_M':audit(a,b,f),'M_to_N':audit(b,n,g),'L_to_N':audit(a,n,h)}
    assert all(x['embedding'] for x in results.values())
    source=sorted(derived(a)[2]); image=lambda c:(h['p'][c[0]],h['m'][c[1]],h['k'][c[2]],h['v'][c[2]][c[3]],h['r'][c[4]])
    assert len(source)==2
    audits=[]
    for subset_len in range(len(source)+1):
        for S in itertools.combinations(source,subset_len):
            source_sum=tuple(sum((a['terms'][c][i] for c in S),Q(0)) for i in range(2))
            projected=matJ(h['J'],source_sum)
            image_sum=tuple(sum((n['terms'][image(c)][i] for c in S),Q(0)) for i in range(2))
            assert projected==image_sum
            audits.append({'family_size':len(S),'transported_sum':[str(x) for x in projected]})
    # This follows the source's finite SET semantics, not a multiset.
    return {'three_valid_full_models':3, 'pairwise_embeddings':results,
            'finite_source_channel_subsets':len(audits),'selected_families':audits,
            'composite_J':[list(map(str,row)) for row in h['J']],
            'positive_composition_associativity':True,
            'limitations':'one concrete triple with 2D rational terms; not general theorem proof'}


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output-dir',default='results');args=pa.parse_args()
    result=run();dest=Path(args.output_dir);dest.mkdir(parents=True,exist_ok=True)
    path=dest/'formation_embedding_composition_audit.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print('PASS 3 full models, 3 embeddings,',result['finite_source_channel_subsets'],'source finite channel subsets')
if __name__=='__main__':main()
