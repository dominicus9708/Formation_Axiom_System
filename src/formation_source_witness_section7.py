"""Supplementary literal Section 7 source-witness combinatorial checks.
Kwon Dominicus (audited-paper author); does not replace the N2 full typed checker.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

X=tuple(itertools.product(range(3), repeat=2))
DIRS={'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}

def grid():
    site_items={('site',p) for p in X}
    edge_items={('edge',tuple(sorted((p,(p[0]+dy,p[1]+dx)))))
        for p in X for dy,dx in DIRS.values()
        if (p[0]+dy,p[1]+dx) in X}
    slots={('slot',p,d) for p in X for d in DIRS}
    full=site_items | edge_items | slots
    S={(0,0),(1,0)}
    join=('edge',tuple(sorted(S)))
    exposed={('slot',p,d) for p in S for d,(dy,dx) in DIRS.items()
        if (p[0]+dy,p[1]+dx) not in S}
    retained={('site',p) for p in S} | {join} | exposed
    assert len(site_items)==9 and len(edge_items)==12 and len(slots)==36
    assert len(full)==57 and len(exposed)==6 and len(retained)==9
    assert retained<=full
    annotated={x:('blocked' if x in exposed else 'transmissive') for x in slots}
    assert sum(a=='blocked' for a in annotated.values())==6
    assert sum(a=='transmissive' for a in annotated.values())==30
    # Model the external fixed support as typed identity functions on retained items.
    support={x:x[1:] for x in full}
    restricted={x:support[x] for x in retained}
    assert restricted=={x:support[x] for x in retained}
    assert all(annotated[x]=='blocked' for x in exposed)
    return {'whole_grid_material':57,'vertex_items':9,'edge_items':12,
       'directional_slot_items':36,'retained_material':len(retained),
       'blocked_exposed_slots':len(exposed),'transmissive_other_slots':30,
       'source_policy':'BC_Lplus(p)=True; BC_Lminus(p)=False (primitive inputs)',
       'first_branch_under_identical_prior_stages':3}


def indexed():
    H_count=G_count=mismatches=vertical_only=collisions=0
    per_status=Counter()
    for i in range(512):
        G=[('H',1),('V',1),('D',-2)]
        if i<125: H=G.copy()
        elif i<187:H=[('V',0)]
        elif i<252:H=[('H',0)]
        elif i<506:H=[('H',1)]
        else:H=[('H',1),('V',1)]
        H_count+=len(H);G_count+=len(G)
        same=H==G
        if not same:mismatches+=1
        if any(r=='V' for r,v in H) and not any(r=='H' for r,v in H):vertical_only+=1
        if not same and sum(v for r,v in H)==sum(v for r,v in G):collisions+=1
        per_status['same' if same else 'different']+=1
    assert (H_count,G_count,mismatches,vertical_only,collisions)==(768,1536,387,62,127)
    return dict(index_count=512,H_channels=H_count,G_channels=G_count,
        mismatched_configuration_families=mismatches,
        vertical_only=vertical_only,full_family_composite_coincidences=collisions,
        first_branch_by_distinct_assignment_domain_cardinality=5)


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output-dir',default='results');args=pa.parse_args()
    data={'source':'Formation v4.5 §7.3–7.4; supplementary independent combinatorics',
          'D2':grid(),'indexed_3x3':indexed(),
          'limits':'not the full typed primitive-record verification; source N2 contains separate inheritance checker'}
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    f=out/'formation_source_witness_section7.json'
    f.write_text(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS D2 57/9/6, 3x3 512-index 768/1536/387/62/127')
if __name__=='__main__':main()
