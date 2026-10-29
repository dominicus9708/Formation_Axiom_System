"""DSD Formation v4.5: independent, small R4 and witness-reflection tests.
Research author: Kwon Dominicus. Only finite witnesses, not a universal proof.
"""
import argparse
import json
from pathlib import Path


def graph(value):
    return set() if value is None else {('a', value)}


def r4(source, target, source_values=(0, 1)):
    # R4 requires equivalence only for source v in V_L.
    return all((('a', v) in graph(source)) == (('a', v) in graph(target))
               for v in source_values)


def described(expressions, describe, restrict, realize, config_ok=True):
    return config_ok and any((H, h) in restrict and h in describe and
                             (h, 'p') in realize for H in expressions for h in expressions)


def run():
    test = {}
    accepted = []
    for s in (None, 0, 1):
        for t in (None, 0, 1, 2):
            ok = r4(s, t)
            assert ok == (s == t if t in (None, 0, 1) else s is None)
            if ok: accepted.append([s, t])
    assert len(accepted) == 4 and [None, 2] in accepted
    test['R4_12_partial_assignments'] = {'cases': 12, 'accepted': accepted,
        'new_target_assignment_outside_source_image': [None, 2]}
    # Full source-graph and target-graph reflection can coexist with different
    # assignment-domain statuses, but not with a target value in Im(I).
    assert r4(None, 2) and not r4(None, 1)
    test['R4_non_surjective_value_boundary'] = True

    # Two full valid finite cores: same typed item and permitted expression h;
    # target-only expression g supplies a witness not seen in the source image.
    src_w = described(('h',), {'h'}, {('h','h')}, set())
    dst_w = described(('h','g'), {'h','g'}, {('h','h'),('g','g')}, {('g','p')})
    assert src_w is False and dst_w is True
    # R3 on source-indexed pairs remains true: target does not realize (h,p).
    assert ('h','p') not in {('g','p')}
    test['R1_R5_compatible_target_only_witness'] = {'source_psi':False,
        'target_psi':True, 'witness_reflection':False,
        'conclusion':'R1-R5 cannot replace independent witness-reflection clause'}

    # A value-map bijection removes the possibility of target-only values.
    accepted_surj = [[s,t] for s in (None,0,1) for t in (None,0,1) if r4(s,t)]
    assert accepted_surj == [[None,None],[0,0],[1,1]]
    test['R4_plus_value_surjectivity'] = {'cases':9,'accepted':accepted_surj,
        'assignment_definedness_reflected':True}

    # Hypothetical source-predicate differences at primitive Stage III.
    cases={}
    for label,index in [('assembly_boundary',2),('organization_admission',0),
                        ('laboratory_local_coherence',1)]:
        enabled=(True,True,True)
        disabled=list(enabled);disabled[index]=False
        src=described(('h',),{'h'},{('h','h')},{('h','p')},all(enabled))
        dst=described(('h',),{'h'},{('h','h')},{('h','p')},all(disabled))
        assert src and not dst
        cases[label]={'primitive_gate':('Adm_cfg','LC','BC')[index],
                      'source_describable':True,'target_describable':False,
                      'policy_truth_derived_by_formation':False}
    test['external_predicate_application_scenarios']=cases
    return {'source':'Formation Axiom System v4.5, 2026-10-22',
        'scope':'small finite source-bound tests; general Section 6 proof review separate',
        'checks':test, 'status':'PASS'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',default='results');args=p.parse_args()
    data=run();dest=Path(args.output_dir);dest.mkdir(parents=True,exist_ok=True)
    file=dest/'formation_embedding_r4_scope.json'
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print('PASS R4 12 exhaustive states; 9 surjective states; witness and three primitive gates')

if __name__=='__main__':main()
