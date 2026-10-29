"""DSD Formation v4.5: forward-map collision and strict-map composition controls.
Audited manuscript author: Kwon Dominicus. Finite illustrative verification.
"""
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
from formation_multisort_stage_audit import make_base,permuted,validate,stage_profile,derv


def collapse_forward_witness():
    """Fully spelled-out F1-F6 preservation, with a noninjective role map."""
    # Material and active support identical, one typed item with fixed base anchor s0.
    # Source two roles admitted; target only one; map both source roles -> rho.
    p,a,k,v='p','a','lambda',0
    c1=(p,a,k,v,'rho1');c2=(p,a,k,v,'rho2');d=(p,a,k,v,'rho')
    source={'material':{'a':'s0'},'expressions':{'h':frozenset({'a'})},
        'configurations':{'p':frozenset({'a'})},'adm_expr':frozenset({'h'}),
        'des_expr':frozenset({'h'}),'res':frozenset({('h','h')}),
        'realize':frozenset({('h','p')}),'conf':{'p':(True,True,True)},
        'q':{'a':0},'role':frozenset({(p,a,k,'rho1'),(p,a,k,'rho2')}),
        'channels':frozenset({c1,c2}), 'terms':{c1:Q(1),c2:Q(1)}}
    target={**source,'role':frozenset({(p,a,k,'rho')}),
            'channels':frozenset({d}),'terms':{d:Q(1)}}
    role_map={'rho1':'rho','rho2':'rho'}
    channel_map=lambda c:(c[0],c[1],c[2],c[3],role_map[c[-1]])
    # Directly check identity on all other carriers and forward F1-F5;
    # F6 for every admitted channel, with J=id on Q.
    assert source['material']==target['material']
    assert source['expressions']==target['expressions']
    assert source['configurations']==target['configurations']
    assert source['adm_expr']==target['adm_expr']
    assert source['des_expr']==target['des_expr']
    assert source['res']==target['res'] and source['realize']==target['realize']
    assert source['conf']==target['conf'] and source['q']==target['q']
    assert {(p,a,k,role_map[r]) for p,a,k,r in source['role']} <= target['role']
    assert all(channel_map(c) in target['channels'] and source['terms'][c]==target['terms'][channel_map(c)]
               for c in source['channels'])
    # F1-F6 hold but the selected set image is one channel, hence 2 != 1.
    assert len({channel_map(c) for c in source['channels']})==1
    original_sum=sum(source['terms'][c] for c in source['channels'])
    image_sum=sum(target['terms'][d] for d in {channel_map(c) for c in source['channels']})
    assert original_sum == 2 and image_sum == 1
    return {'forward_conditions':'F1-F6 satisfied in this finite example',
        'role_map_injective':False,'source_channels':2,'target_channels':1,
        'source_composite':2,'image_composite':1,
        'interpretation':'noninjective channel map permits collision of finite set elements; Prop 6.3 needs the channel injection for composite covariance'}


def strict_composition_controls():
    tests=[]
    for i in range(12):
        a=make_base(20262000+i)
        b=permuted(a)
        c=permuted(b)
        for x in (a,b,c):validate(x)
        ab=stage_profile(a,b)
        bc=stage_profile(b,c)
        ac=stage_profile(a,c)
        assert all(v['first_branch'] is None for v in (ab,bc,ac))
        assert stage_profile(c,a)['first_branch'] is None
        tests.append({'seed':20262000+i,'admitted_channels':len(derv(a)[2]),
                      'first_branch_A_B':None,'first_branch_B_C':None,'first_branch_A_C':None})
    return {'verified_isomorphism_triplets':len(tests),
        'note':'12 independent typed source models, rename+invertible 2D transport twice; verifies selected triple compositions and inverses, not all morphisms',
        'case_summaries':tests}


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output-dir',default='results');args=pa.parse_args()
    out={'source':'Formation Axiom System v4.5',
         'noninjective_forward_map':collapse_forward_witness(),
         'strict_isomorphism_composition':strict_composition_controls(),
         'scope':'finite correctly typed examples, not full general theorem proofs'}
    dest=Path(args.output_dir);dest.mkdir(parents=True,exist_ok=True)
    file=dest/'formation_map_boundary_audit.json'
    file.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS forward-map collision and',len(out['strict_isomorphism_composition']['case_summaries']),'strict triple comparisons', file)

if __name__=='__main__':main()
