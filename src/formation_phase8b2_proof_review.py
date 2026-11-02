"""Source-locked editorial/mathematical proof-obligation register.

Paper author Kwon Dominicus. A register of human reasoning about the actual
printed proof steps, NOT proof-assistant verification or a computational proof.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

PDF_SHA='af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'
PRIOR={'Theorem 3.3','Theorem 4.7','Theorem 6.5','Proposition 6.11',
       'Theorem 6.17','Theorem 6.19','Theorem 6.20','Theorem 7.3'}
# Notes are author-independent checks of the displayed arguments; no claim of automated formal proof.
REVIEWS={
'Proposition 2.5':('Record projections erase nested coordinates; erasing by stages composes associatively.','SUPPORTED_UNDER_DEFINITIONS'),
'Theorem 3.6':('Membership in C iff the existential structural trace exists by Clauses IV and VI; T is defined exactly on C.','SUPPORTED_UNDER_DEFINITIONS'),
'Theorem 4.5':('Countermodels 4.1-4.4 retain a nonempty common formation kernel and each violates only its named primitive axiom; closure is defined even for a typed counterinterpretation.','SUPPORTED_WITH_SOURCE_COUNTERMODELS'),
'Proposition 4.6':('Equality of anchor functions forces restriction-domain inclusion; induced relational substructures and a single partial function make remaining clauses dependent.','SUPPORTED_UNDER_DECLARED_TYPING'),
'Corollary 4.8':('Contrapositive of Primitive Axiom I.','SUPPORTED_BY_LOGIC'),
'Lemma 4.10':('Nested material inclusions and successive anchor restrictions yield direct restriction of the original anchor.','SUPPORTED_BY_AXIOM_II'),
'Proposition 4.12':('Two sound restriction arrows plus identities do not require their composite arrow; transitivity was not imposed.','SUPPORTED_BY_SEPARATION_WITNESS'),
'Lemma 4.13':('Axiom II and Axiom III compose material inclusion and anchor-function restriction.','SUPPORTED_BY_AXIOMS_II_III'),
'Corollary 4.14':('The two displayed alternatives each negate a necessary conjunct in Psi.','SUPPORTED_BY_CLAUSE_IV'),
'Proposition 5.2':('Undefined assignments lie outside Q; defined zero and nonzero negligible are disjoint. N_delta is typed only when lambda belongs to Lambda_delta.','SUPPORTED_WITH_LAMBDA_DELTA_SCOPE'),
'Proposition 5.5':('An active describable configuration with the selected empty assignment domain satisfies Axiom V but not universal assignability.','SUPPORTED_BY_COUNTERMODEL'),
'Proposition 5.6':('Clause VI supplies admitted channel, graph and role; Clause IV supplies witness; III and II supply anchored inheritance.','SUPPORTED_BY_CLOSURES_AND_INHERITANCE'),
'Proposition 5.8':('A describable active assigned item has no admitted role when the primitive role relation is empty.','SUPPORTED_BY_COUNTERMODEL'),
'Proposition 5.14':('One material item, defined zero, three role-separated channels and freely supplied component terms +1,-1,0 yield distinct families with identical finite sum.','SUPPORTED_BY_SOURCE_EXACT_WITNESS'),
'Proposition 6.3':('F1-F3 preserve Psi and active material; F2,F4,F5 preserve channels; finite sum covariance additionally requires channel injection plus F6.','SUPPORTED_WITH_INJECTIVITY_CONDITION'),
'Corollary 6.6':('Identity and composition of the typed maps are associative, giving a possibly large category and its wide embedding subcategory.','SUPPORTED_BY_THEOREM_6_5'),
'Corollary 6.7':('Inclusion identity is reflexive and composition of inclusion embeddings is again inclusion; preorder need not be antisymmetric.','SUPPORTED_BY_THEOREM_6_5'),
'Theorem 6.8':('Witness reflection applies on candidate images; reflected graph and role data give channel reflection; induced injection gives finite-set covariance.','SUPPORTED_ON_IMAGE_ONLY'),
'Corollary 6.12':('Strict isomorphism induces a channel bijection; term transport and J linearity commute with each finite set sum.','SUPPORTED_BY_E1_TO_E9'),
'Theorem 6.14':('Inverse and composition of typed bijections preserve all E1-E9; the term-space inverse and pointwise inverse value maps are required.','SUPPORTED_BY_E1_TO_E9'),
'Theorem 6.16':('Nested staged comparison sets follow by incremental constraints; I7 is exactly strict isomorphism; first empty stage is minimum when I7 empty.','SUPPORTED_BY_DEFINITIONS_6_10_6_15'),
'Corollary 6.18':('I3=I4 in Theorem 6.17 excludes a first branch at index 4.','SUPPORTED_BY_THEOREM_6_17'),
'Proposition 6.22':('One-channel zero term and two-channel +1/-1 model have identical nonempty family composite under fixed identity J but unequal channel cardinalities.','SUPPORTED_BY_SOURCE_COUNTERMODEL'),
'Theorem 6.23':('Universal failure of at least one E1-E9 for every typed candidate negates existence of any strict isomorphism, even if candidate set is empty.','SUPPORTED_BY_DEFINITION_6_10'),
'Theorem 7.1':('Construction chooses an empty material-record signature; Section 2.2 earlier fixes S_mat. Valid when signature is a selectable model parameter; if S_mat is externally fixed, this particular proof must interpret that fixed signature instead.','SCOPE_CLARIFICATION_RECOMMENDED')
}

PAT=re.compile(r'(?m)^\s*(Theorem|Proposition|Corollary|Lemma|Definition|Remark|Countermodel)\s+(\d+\.\d+)\s*\(')

def run(pdf):
    sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
    if sha != PDF_SHA: raise ValueError('Source mismatch: '+sha)
    text=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,check=True).stdout.decode('utf-8')
    matches=list(PAT.finditer(text))
    assert len(matches)==69,len(matches)
    found=[]
    for i,match in enumerate(matches):
        key=' '.join(match.groups())
        segment=text[match.end():matches[i+1].start() if i+1<len(matches) else len(text)]
        if key in PRIOR: continue
        if key in REVIEWS:
            proof=re.search(r'(?<!\w)Proof\.',segment)
            assert proof,key+' missing proof label'
            note,status=REVIEWS[key]
            found.append({'item':key,'pdf_page':text[:match.start()].count('\f')+1,
                'review_status':status,'premise_to_conclusion_check':note,
                'printed_proof_present':True})
    assert len(found)==len(REVIEWS)==25 and set(x['item'] for x in found)==set(REVIEWS)
    assert sum(x['review_status']=='SCOPE_CLARIFICATION_RECOMMENDED' for x in found)==1
    return {'source_sha256':sha,'paper_author':'Kwon Dominicus','scope':'25 remaining printed proof paragraphs, excluding eight Phase8B1 proof chains',
            'status':'25_SOURCE_ARGUMENTS_REVIEWED_1_SIGNATURE_SCOPE_CLARIFICATION',
            'supports_under_declared_assumptions':24,'signature_scope_clarification':1,
            'proofs':found,'formal_proof_certification':'OPEN',
            'limitation':'Argument review and source coverage, not theorem-prover formalization; further criticism may find errors.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--pdf',type=Path,required=True);p.add_argument('--output-dir',type=Path,default=Path('results'))
    args=p.parse_args();output=args.output_dir;output.mkdir(parents=True,exist_ok=True)
    path=output/'formation_phase8b2_25_proof_review.json';path.write_text(json.dumps(run(args.pdf),ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('PASS source-locked 25 printed proof paragraphs; 24 supported under assumptions, 1 signature-scope clarification')
if __name__=='__main__':main()
