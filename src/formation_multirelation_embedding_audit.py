"""Formation Axiom System v4.5: multi-kind ternary/external-annotation embeddings.
Paper author: Kwon Dominicus. Independent bounded model checker, Python >=3.10.
The checks illustrate original F1-F6/R1-R5; they are not universal proofs.
"""
import argparse
import copy
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

PAPER_SHA = 'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'


def derived(m):
    cfg = {p for p in m['P'] if all(m['gates'][p]) and any(
        (H,h) in m['res'] and h in m['des'] and (h,p) in m['real']
        for H in m['E'] for h in m['E'])}
    active = set().union(*(m['act'][p] for p in cfg)) if cfg else set()
    chan = {(p,a,k,m['q'][k][a],r) for p in cfg for a in m['act'][p]
            for k in m['K'] if a in m['q'][k] for r in m['R']
            if (p,a,k,r) in m['roles']}
    return cfg, active, chan


def full_model(m):
    if not set(m['des']) <= set(m['adm']): return 'I'
    if any(e not in m['E'] or not set(m['mat'][e]) <= set(m['M']) for e in m['E']):return 'TYPING'
    if any(not set(m['act'][p]) <= set(m['M']) for p in m['P']):return 'TYPING'
    if any(not set(t) <= set(m['M']) for t in m['tri']):return 'TYPING'
    if any(e not in m['adm'] or not m['mat'][e] <= m['mat'][H] or
           m['ae'][e] != {a:m['ae'][H][a] for a in m['mat'][e]}
           for H,e in m['res']):return 'II'
    if any((e,e) not in m['res'] for e in m['adm']):return 'II_ID'
    if any(not m['act'][p] <= m['mat'][e] or
           m['ap'][p] != {a:m['ae'][e][a] for a in m['act'][p]}
           for e,p in m['real']):return 'III'
    if any(m['ae'][e] != {a:m['support'][a] for a in m['mat'][e]} for e in m['E']):return 'TYPING'
    if any(m['ap'][p] != {a:m['support'][a] for a in m['act'][p]} for p in m['P']):return 'TYPING'
    active=derived(m)[1]
    if any(not set(m['q'][k]) <= active for k in m['K']):return 'V'
    if any(not set(m['q'][k].values()) <= set(m['V'][k]) for k in m['K']):return 'TYPING'
    if set(m['terms']) != derived(m)[2]:return 'TERM'
    if any(len(x)!=2 or any(not isinstance(z,Q) for z in x) for x in m['terms'].values()):return 'TERM'
    return None


def rebuild(m):
    m['ae']={e:{a:m['support'][a] for a in m['mat'][e]} for e in m['E']}
    m['ap']={p:{a:m['support'][a] for a in m['act'][p]} for p in m['P']}
    return m


def make_pair():
    a=dict(M=('a','b','c','d'),E=('H','h'),P=('p','p_bad'),K=('energy','phase'),
       R=('rE','rP'),V={'energy':(0,1),'phase':(0,1)},
       material_type={x:'unit' for x in 'abcd'},
       support={'a':'s0','b':'s1','c':'s2','d':'s3'},
       annotation={'a':'blue','b':'red','c':'blue','d':'green'},
       tri={('a','b','c'),('a','c','d')},
       mat={'H':frozenset('abcd'),'h':frozenset('abc')},
       act={'p':frozenset('abc'),'p_bad':frozenset('d')},
       adm={'H','h'},des={'h'},res={('H','H'),('h','h'),('H','h')},
       real={('h','p')},gates={'p':(True,True,True),'p_bad':(True,False,True)},
       q={'energy':{'a':1},'phase':{'b':0}},
       roles={('p','a','energy','rE'),('p','b','phase','rP'),('p','c','energy','rE')},
       terms={})
    rebuild(a)
    ca=derived(a)[2]
    a['terms']={c:((Q(1),Q(0)) if c[2]=='energy' else (Q(0),Q(1))) for c in ca}
    b=copy.deepcopy(a)
    b['M']+=('e',); b['material_type']['e']='unit';b['support']['e']='s4';b['annotation']['e']='gold'
    b['tri'] |= {('a','b','e'),('a','e','c')}
    b['mat']['H'] |= frozenset(('e',));b['mat']['h'] |= frozenset(('e',))
    b['act']['p'] |= frozenset(('e',))
    b['E']+=('g',);b['mat']['g']=frozenset(('a','b','e'))
    b['P']+=('p_extra',);b['act']['p_extra']=frozenset(('a','b','e'))
    b['adm']|={'g'};b['des']|={'g'}
    b['res']|={('g','g'),('H','g')};b['real']|={('g','p_extra')}
    b['gates']['p_extra']=(True,True,True)
    b['K']+=('temp',);b['V']['energy']=(0,1,2);b['V']['phase']=(0,1,2);b['V']['temp']=(0,1)
    b['q']['energy'].update({'c':2,'e':1}); b['q']['phase']['c']=2;b['q']['temp']={'e':1}
    b['R']+=('rX',);b['roles']|={('p','a','energy','rX'),('p_extra','e','temp','rX')}
    rebuild(b)
    for c in derived(b)[2]:
        b['terms'][c] = ((Q(2),Q(1)) if c[0]=='p' and c[1]=='a' and c[2]=='energy' and c[4]=='rE'
            else ((Q(1),Q(1)) if c[0]=='p' and c[1]=='b' and c[2]=='phase' and c[4]=='rP'
                  else (Q(3),Q(2))))
    f={t:{x:x for x in a[axis]} for t,axis in [('m','M'),('e','E'),('p','P'),('k','K'),('r','R')]}
    f['v']={k:{i:i for i in a['V'][k]} for k in a['K']}
    f['J']=((Q(2),Q(1)),(Q(1),Q(1)))
    assert full_model(a) is None and full_model(b) is None
    return a,b,f


def matJ(J,x):
    return tuple(sum((J[i][k]*x[k] for k in range(2)),Q(0)) for i in range(2))


def audit(a,b,f):
    assert full_model(a) is None,full_model(a)
    assert full_model(b) is None,full_model(b)
    fm,fe,fp,fk,fr=(f[k] for k in ('m','e','p','k','r'))
    fv=f['v'];J=f['J']
    inj=lambda d:len(set(d.values()))==len(d)
    injection=all(inj(d) for d in (fm,fe,fp,fk,fr)) and all(inj(z) for z in fv.values())
    det=J[0][0]*J[1][1]-J[0][1]*J[1][0]
    # Material relation embedding includes exact reflection on original-carrier tuples.
    image={fm[x] for x in a['M']}
    tri_image={(fm[x],fm[y],fm[z]) for x,y,z in a['tri']}
    F1=(all(a['material_type'][x]==b['material_type'][fm[x]] and
            a['support'][x]==b['support'][fm[x]] and
            a['annotation'][x]==b['annotation'][fm[x]] for x in a['M'])
        and tri_image<=b['tri']
        and all({fm[x] for x in a['mat'][e]}<=b['mat'][fe[e]] and
                all(a['ae'][e][x]==b['ae'][fe[e]][fm[x]] for x in a['mat'][e]) for e in a['E'])
        and all({fm[x] for x in a['act'][p]}<=b['act'][fp[p]] and
                all(a['ap'][p][x]==b['ap'][fp[p]][fm[x]] for x in a['act'][p]) for p in a['P']))
    relation_embedding=tri_image=={t for t in b['tri'] if set(t)<=image}
    F2=(all(e not in a['adm'] or fe[e] in b['adm'] for e in a['E']) and
        all(e not in a['des'] or fe[e] in b['des'] for e in a['E']) and
        all(all(not a['gates'][p][i] or b['gates'][fp[p]][i] for i in range(3)) for p in a['P']))
    F3=all((fe[h],fe[e]) in b['res'] for h,e in a['res']) and all((fe[e],fp[p]) in b['real'] for e,p in a['real'])
    F4=all((fm[x] in b['q'][fk[k]] and b['q'][fk[k]][fm[x]]==fv[k][v])
           for k in a['K'] for x,v in a['q'][k].items())
    F5=all((fp[p],fm[x],fk[k],fr[r]) in b['roles'] for p,x,k,r in a['roles'])
    cmap=lambda c:(fp[c[0]],fm[c[1]],fk[c[2]],fv[c[2]][c[3]],fr[c[4]])
    F6=all(cmap(c) in b['terms'] and matJ(J,a['terms'][c])==b['terms'][cmap(c)] for c in derived(a)[2])
    R1=all({fm[x] for x in a['mat'][e]}==b['mat'][fe[e]] & image for e in a['E']) and all(
           {fm[x] for x in a['act'][p]}==b['act'][fp[p]] & image for p in a['P'])
    R2=all((e in a['adm'])==(fe[e] in b['adm']) and (e in a['des'])==(fe[e] in b['des']) for e in a['E']) and all(
           a['gates'][p]==b['gates'][fp[p]] for p in a['P'])
    R3=all(((h,e) in a['res'])==((fe[h],fe[e]) in b['res']) for h in a['E'] for e in a['E']) and all(
           ((e,p) in a['real'])==((fe[e],fp[p]) in b['real']) for e in a['E'] for p in a['P'])
    R4=all(((x,v) in a['q'][k].items()) == ((fm[x],fv[k][v]) in b['q'][fk[k]].items())
           for k in a['K'] for x in a['M'] for v in a['V'][k])
    R5=all(((p,x,k,r) in a['roles'])==((fp[p],fm[x],fk[k],fr[r]) in b['roles'])
           for p in a['P'] for x in a['M'] for k in a['K'] for r in a['R'])
    witness=all(fp[p] not in derived(b)[0] or p in derived(a)[0] for p in a['P'])
    return dict(F1=bool(F1),F2=bool(F2),F3=bool(F3),F4=bool(F4),F5=bool(F5),F6=bool(F6),
                material_relation_embedding=bool(relation_embedding),
                R1=bool(R1),R2=bool(R2),R3=bool(R3),R4=bool(R4),R5=bool(R5),
                witness_reflection=bool(witness),injective_maps=bool(injection and det!=0),
                embedding=bool(all((F1,F2,F3,F4,F5,F6,relation_embedding,R1,R2,R3,R4,R5,witness,injection,det!=0))),
                source_channels=len(derived(a)[2]),target_channels=len(derived(b)[2]))


def run():
    a,b,f=make_pair();checks={}
    good=audit(a,b,f);assert good['embedding'],good
    checks['valid_multi_kind_ternary_annotation_embedding']=good
    def expect(label,mut,expected):
        n=copy.deepcopy(b);mut(n);rebuild(n)
        # After changing a partial-assignment value, the candidate channel identity changes.
        # Supply terms on the NEW admitted-channel domain rather than creating an invalid model.
        previous=n['terms']
        n['terms']={c:previous.get(c,(Q(3),Q(2))) for c in derived(n)[2]}
        if full_model(n) is not None:raise AssertionError((label,'invalid target',full_model(n)))
        z=audit(a,n,f)
        assert not z['embedding'] and z[expected] is False,(label,expected,z)
        checks[label]={'expected_failed_condition':expected,'observed':z}
    expect('target_only_source_tuple_breaks_material_embedding',lambda m:m['tri'].add(('b','a','c')),'material_relation_embedding')
    expect('annotation_mismatch_breaks_F1',lambda m:m['annotation'].__setitem__('a','violet'),'F1')
    expect('fixed_external_support_mismatch_breaks_F1',lambda m:m['support'].__setitem__('a','s4'),'F1')
    expect('additional_source_item_in_target_expression_breaks_R1',lambda m:m['mat'].__setitem__('h',m['mat']['h']|{'d'}),'R1')
    expect('new_in_image_assignment_breaks_R4',lambda m:m['q']['energy'].__setitem__('c',1),'R4')
    expect('new_in_image_role_breaks_R5',lambda m:m['roles'].add(('p','a','phase','rE')),'R5')
    expect('target_original_realization_breaks_R3',lambda m:m['real'].add(('H','p')),'R3')
    expect('missing_term_transport_breaks_F6',lambda m:m['terms'].__setitem__(('p','a','energy',1,'rE'),(Q(8),Q(8))),'F6')
    expect('configuration_boundary_change_breaks_R2',lambda m:m['gates'].__setitem__('p_bad',(True,False,False)),'R2')
    # Confirm no illicit source-valued target graph item in positive example.
    assert a['q']['energy'].get('c') is None and b['q']['energy']['c']==2
    assert b['V']['energy']==(0,1,2)
    assert derived(b)[2] - derived(a)[2]
    # The prior phase 4 relative reflection lemma is now exercised with 2 kinds.
    checks['relative_assignment_reflection_two_kinds']={
        'source_energy_c_defined':False,'target_energy_c_value':2,
        'value_in_source_energy_image':False,'R4':good['R4'],
        'other_kind_phase_source_b_zero':True}
    return dict(paper_sha256=PAPER_SHA,signature='ternary relation; 2 kinds; external annotations and anchored support; Q^2 terms',
                positive=1,negative=9,checks=checks,
                conclusion='10 finite fixtures passed their expectations; unrestricted theorem proof remains open')


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output-dir',default='results');args=pa.parse_args()
    result=run();out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    path=out/'formation_multirelation_embedding_audit.json'
    path.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
    print('PASS: 1 valid embedding, 9 targeted mutations, 2 quantity kinds; output:',path)

if __name__=='__main__':main()
