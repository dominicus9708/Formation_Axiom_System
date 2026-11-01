"""Reproducible proof-obligation INVENTORY for Kwon Dominicus's Formation v4.5.
NOT a formal proof assistant or a claim of 46 theorems being proved.
Requires local original source PDF and Poppler pdftotext; SHA256 locked.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

SOURCE_SHA256='af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'
PAT=re.compile(r'(?m)^\s*(Theorem|Proposition|Corollary|Lemma|Countermodel|Definition|Remark)\s+(\d+\.\d+)\s*\(')
REF=re.compile(r'\b(Theorem|Proposition|Corollary|Lemma|Definition|Countermodel|Remark)\s+(\d+\.\d+)\b')
DIRECT={
'Corollary 4.11':'Repeat Lemma 4.10 along a finite restriction chain; induction on n.',
'Corollary 5.3':'Partial-function domain: q(a) undefined outside Q, distinct from pointed zero.',
'Proposition 5.4':'Directly calculate the two branches of the total zero-padding definition.',
'Corollary 5.7':'Take the contrapositive of the Clause VI conjunction.',
'Proposition 5.9':'Substitute the defined zero graph-pair in Closure Clause VI.',
'Proposition 5.11':'Different role coordinates yield distinct admitted five-tuples.',
'Proposition 5.12':'T is declared only on C; absent candidates are outside dom(T).',
'Proposition 5.13':'The defined zero-extension sends both a missing candidate and a zero-valued present channel to zero under the explicit coexistence hypothesis.',
'Corollary 6.24':'Assignment-domain equivalence E5 is necessary for every strict isomorphism.',
'Corollary 6.25':'Role preservation/reflection E8 is necessary for every strict isomorphism.',
'Corollary 6.26':'An induced bijection on admitted channels is necessary for every strict isomorphism.',
'Corollary 7.2':'Theorem 7.1 provides a finite set-coded witness in ZFC; choose a finite field.',
'Corollary 7.4':'Theorem 7.3 applied to material carriers of each finite cardinality n.',
}


def main():
 p=argparse.ArgumentParser();p.add_argument('--pdf',type=Path,required=True)
 p.add_argument('--output-dir',default='results');args=p.parse_args()
 actual=hashlib.sha256(args.pdf.read_bytes()).hexdigest()
 if actual!=SOURCE_SHA256:raise ValueError('Manuscript SHA does not match locked original: '+actual)
 proc=subprocess.run(['pdftotext','-layout',str(args.pdf),'-'],capture_output=True,check=True)
 txt=proc.stdout.decode('utf-8')
 headings=list(PAT.finditer(txt));assert len(headings)==69
 allkeys={f'{m.group(1)} {m.group(2)}' for m in headings}
 proof=[]; non_proof=[]
 for i,m in enumerate(headings):
  key=f'{m.group(1)} {m.group(2)}'
  segment=txt[m.end():headings[i+1].start() if i+1<len(headings) else len(txt)]
  if m.group(1) not in ('Theorem','Proposition','Corollary','Lemma'):
   non_proof.append(key);continue
  match=re.search(r'(?<!\w)Proof\.',segment)
  if match:
   body=segment[match.end():]
   citations=sorted(set(f'{x.group(1)} {x.group(2)}' for x in REF.finditer(body)))
   # This is a source-indexing list, not a complete formal dependency graph:
   # axioms, closure clauses, implicit definitions and logic are not all named.
   assert all(c in allkeys for c in citations),(key,citations)
   proof.append({'claim':key,'presentation':'EXPLICIT_PROOF_PARAGRAPH',
       'explicit_named_references':citations})
  else:
   assert key in DIRECT,('unclassified proof omission',key)
   proof.append({'claim':key,'presentation':'DIRECT_UNLABELED_DERIVATION',
       'manual_proof_obligation_note':DIRECT[key]})
 expected={k:v for k,v in sorted(DIRECT.items())}
 assert len(proof)==46 and len(non_proof)==23
 assert len([x for x in proof if x['presentation']=='EXPLICIT_PROOF_PARAGRAPH'])==33
 assert len([x for x in proof if x['presentation']=='DIRECT_UNLABELED_DERIVATION'])==13
 assert set(x['claim'] for x in proof if x['presentation']=='DIRECT_UNLABELED_DERIVATION')==set(expected)
 report={'source_sha256':SOURCE_SHA256,'status':'PASS_SOURCE_INVENTORY_ONLY',
   'numbered_items':len(headings),'claims_requiring_math_review':len(proof),
   'claims_with_explicit_proof':33,'claims_with_direct_unlabeled_derivation':13,
   'definitions_countermodels_remarks':len(non_proof),
   'proof_index':proof,'non_proof_numbered_items':non_proof,
   'warning':'Extracted explicit references are not an exhaustive dependency graph. Every claim still requires a mathematical premise-to-conclusion check, and a finite example is never a general proof.'}
 path=Path(args.output_dir);path.mkdir(parents=True,exist_ok=True)
 target=path/'formation_phase8_proof_inventory.json'
 target.write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print('PASS 69 numbered items, 46 propositions including 33 explicit proofs + 13 direct derivations')

if __name__=='__main__':main()
