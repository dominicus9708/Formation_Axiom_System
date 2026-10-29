"""Independent rerun of selected 4.7 residual independence witnesses & closure.
Audited manuscript author: Kwon Dominicus. Restricted finite experiments.
"""
import argparse
import json
from pathlib import Path
from fractions import Fraction
import sys
HERE=Path(__file__).resolve()
for candidate_dir in (HERE.parent, HERE.parents[1], HERE.parents[1] / 'src'):
    if (candidate_dir / 'formation_negative_stage_audit.py').is_file():
        sys.path.insert(0, str(candidate_dir))
        break
else:
    raise RuntimeError('Required Phase-2 source fixture not found in existing repository')
from formation_negative_stage_audit import (base, new_negative_cases,
    issues, derived, variants)

RESIDUAL = [
    ('i', 'F02_Described_not_admitted', 'AXIOM_I_DES_IMPL_ADM'),
    ('ii', 'F04_Restriction_anchor_changed', 'AXIOM_II_ANCHOR_INHERITANCE'),
    ('iii', 'F04_Restriction_target_not_admitted', 'AXIOM_II_TARGET_ADMISSION'),
    ('iv', 'F04_Admitted_expression_no_identity', 'AXIOM_II_IDENTITY_RESTRICTION'),
    ('v', 'F05_Realization_anchor_changed', 'AXIOM_III_REALIZATION_INHERITANCE'),
    ('vi', 'F06_Assignment_outside_described_material', 'AXIOM_V_ASSIGNMENT_DOMAIN'),
]


def run():
    cases=new_negative_cases()
    proof=[]
    for label,name,target_fault in RESIDUAL:
        model, expected=cases[name]
        err=issues(model)
        assert expected==target_fault and err==[target_fault], (name,err)
        d=derived(model)
        assert len(d['psi'])>0 and len(d['channels'])>0
        assert len(d['comps']) == 2**len(d['channels'])
        proof.append({'residual_constraint':label,'source_fixture':name,
                      'sole_violated_residual':target_fault,
                      'unaffected_active_kernel':True,
                      'derived_channels':len(d['channels'])})
    models=list(variants())
    assert len(models)==80
    closure_checks=[]
    for i,m in enumerate(models):
        assert issues(m)==[]
        d=derived(m)
        # Stage 4 (Psi), 6 (channels) are insensitive to Stage 7 term changes.
        modified={**m, 'terms':{c:Fraction(i+3) for c in d['channels']}}
        d_mod=derived(modified)
        assert d['psi']==d_mod['psi']
        assert d['channels']==d_mod['channels']
        # Stage 7 is determined relative to each supplied term map.
        assert all(d_mod['comps'][f]==sum((modified['terms'][c] for c in f),Fraction(0))
                   for f in d_mod['families'])
        closure_checks.append((len(d['psi']),len(d['channels'])))
    return {'status':'PASS_FINITE_RESIDUAL_INDEPENDENCE_AND_RELATIVE_CLOSURE',
            'six_residual_single_fault_cases':proof,
            'valid_primitive_80_model_checks':80,
            'relative_closure_no_independent_status_change':True,
            'note':'A complete axiom-independence proof uses the explicit manuscript models; this checker certifies six selected witnesses and their nonempty formation kernel, not every interpretation.',
            'source':'Formation v4.5 Theorem 4.7, Theorem 3.3, original Phase2 bounded fixtures'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',default='results');a=p.parse_args()
    dst=Path(a.output_dir);dst.mkdir(parents=True,exist_ok=True)
    target=dst/'formation_residual_dependency_audit.json'
    target.write_text(json.dumps(run(),sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS six source-matched residual negative models and 80 valid model relative-closure checks')

if __name__=='__main__': main()
