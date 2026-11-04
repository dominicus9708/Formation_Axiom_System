#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Non-destructive, three-region bilingual Formation v4.5 manuscript patch.

Author of the audited manuscript: Kwon Dominicus.
Works on the exact 2026-10-22 RC1 English/Korean LaTeX source that was
recorded in the existing user Library. Original inputs are never overwritten.
Each section patch fails closed if its original text is absent or duplicated.
"""
from __future__ import annotations
import argparse
import difflib
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

DATE = '2026.10.22'
NAME_EN = 'DSD_Formation_Axiom_System_EN_20261022_RC1.tex'
NAME_KR = 'DSD_Formation_Axiom_System_KR_20261022_RC1.tex'
TOKEN_PATTERNS = [
    r'\\begin\{(?:axiom|closureclause|theorem|proposition|corollary|lemma|definition|model|countermodel|example|remark)\}',
    r'\\(?:begin|end)\{(?:equation|align|gather|multline|array)\*?\}',
    r'\\(?:label|ref|eqref|cite|bibitem)\{[^}]+\}',
    r'\\\[', r'\\\]',
]


@dataclass(frozen=True)
class Edit:
    section: str
    old: str
    new: str


EN = (
    Edit('2.2',
         r'Fix a typed material-record signature \(\mathcal S_{\mathrm{mat}}\).',
         r'Fix a typed material-record signature \(\mathcal S_{\mathrm{mat}}\).' '\n'
         'This signature is held fixed for regimes compared within a common comparison family; in the existence constructions of Section~7, the signature itself may be selected as part of the existentially supplied typed data.'),
    Edit('7.1',
         r'Choose \(s\in\Supp(\Base)\), use the empty material-record signature, and set',
         r'Choose \(s\in\Supp(\Base)\) and select the empty material-record signature as part of the existence witness. Set'),
    Edit('declarations',
         'All model constructions, countermodels, and finite-witness counts used in this version are specified in Sections~4 and 7 and Appendix~C.\n'
         'A separate executable reproducibility package for the finite witnesses and numerical counts is publicly available at '
         r'\url{https://github.com/dominicus9708/Formation_Axiom_System}.',
         'Model constructions, countermodels, and finite-witness counts used in this version are specified in Sections~4--7 and Appendix~C.\n'
         'Executable checks of selected finite witnesses and numerical counts are publicly available at '
         r'\url{https://github.com/dominicus9708/Formation_Axiom_System}.' '\n'
         'The original D2 checker uses a lightweight stage profile; the original Proposition~5.14 checker uses a valid alternative construction. Supplementary source-matched checks are documented in the associated audit records.'),
)

KR = (
    Edit('2.2',
         r'유형화된 재료 기록 서명 \(\mathcal S_{\mathrm{mat}}\)를 고정한다.',
         r'유형화된 재료 기록 서명 \(\mathcal S_{\mathrm{mat}}\)를 고정한다.' '\n'
         '이 서명은 공통 비교 가족 안에서 비교되는 레짐들 사이에 고정한다. 다만 제7절의 존재 구성에서는 서명 자체도 존재 증인으로 공급되는 유형화 자료의 일부로 선택할 수 있다.'),
    Edit('7.1',
         r'\(s\in\Supp(\Base)\)를 택하고, 공 재료 기록 서명을 사용하여',
         r'\(s\in\Supp(\Base)\)를 택하고, 존재 증인의 일부로 공 재료 기록 서명을 선택하여'),
    Edit('declarations',
         '이 판본에서 사용한 모든 모형 구성, 반모형 및 유한 증인 계수는 제4절, 제7절, 부록~C에 명시되어 있다.\n'
         '유한 증인과 수치 계수를 위한 별도의 실행 가능한 재현성 패키지는 '
         r'\url{https://github.com/dominicus9708/Formation_Axiom_System}에서 공개되어 있다.',
         '이 판본에서 사용한 모형 구성, 반모형 및 유한 증인 계수는 제4--7절과 부록~C에 명시되어 있다.\n'
         '선별된 유한 증인과 수치 계수에 대한 실행 검사는 '
         r'\url{https://github.com/dominicus9708/Formation_Axiom_System}에 공개되어 있다.' '\n'
         '기존 D2 검사기는 간략한 단계 프로필을 사용하며, 기존 명제~5.14 검사기는 유효한 대체 구성을 사용한다. 원문의 구성과 일치하는 보완 검사는 관련 감사 기록에 별도로 문서화하였다.'),
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compile_pdf(tex: Path, output_dir: Path) -> dict:
    for i in range(2):
        p = subprocess.run([
            'xelatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
            '-output-directory='+str(output_dir), str(tex)],
            cwd=output_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            timeout=120)
        if p.returncode:
            (output_dir/(tex.stem+'.compile_error.txt')).write_text(p.stdout, encoding='utf-8')
            raise RuntimeError(f'XeLaTeX failed on {tex.name} pass {i+1}; see log')
    pdf = output_dir/(tex.stem+'.pdf')
    if not pdf.is_file():
        raise RuntimeError('XeLaTeX returned success but PDF missing')
    return {'pdf':str(pdf),'pdf_sha256':sha256_bytes(pdf.read_bytes())}


def markers(src: str) -> dict:
    return {p:re.findall(p,src) for p in TOKEN_PATTERNS}


def apply_one(src: Path, edits: tuple[Edit,...], out: Path, kind: str) -> tuple[dict,str]:
    source_bytes = src.read_bytes()
    decoded = source_bytes.decode('utf-8-sig')
    bom = b'\xef\xbb\xbf' if source_bytes.startswith(b'\xef\xbb\xbf') else b''
    line_sep = '\r\n' if '\r\n' in decoded else '\n'
    normalized = decoded.replace('\r\n','\n')
    if '\\author{Kwon Dominicus' not in normalized or DATE not in normalized:
        raise ValueError(f'{kind}: missing author/date anchor; wrong RC1 manuscript')
    old_markers = markers(normalized)
    version = normalized
    edit_log=[]
    prev=-1
    for e in edits:
        occurrences = version.count(e.old)
        if occurrences != 1:
            raise ValueError(f'{kind}: {e.section} expected exactly one source anchor, found {occurrences}')
        ix = version.index(e.old)
        if ix <= prev:
            raise ValueError(f'{kind}: section sequence is not 2.2 -> 7.1 -> declarations')
        prev=ix
        version = version.replace(e.old,e.new,1)
        edit_log.append({'section':e.section,'old':e.old,'new':e.new})
    if old_markers != markers(version):
        raise AssertionError(f'{kind}: a math environment/label/reference/bibliography token changed')
    if version.count('\\begin{document}') != 1 or version.count('\\end{document}') != 1:
        raise AssertionError(f'{kind}: incomplete document')
    if version.count(r'\author{Kwon Dominicus') != 1:
        raise AssertionError(f'{kind}: author identity changed')
    actual_bytes=bom+version.replace('\n',line_sep).encode('utf-8')
    if out.resolve()==src.resolve():
        raise ValueError('Refusing to overwrite the original source')
    out.write_bytes(actual_bytes)
    diff=''.join(difflib.unified_diff(normalized.splitlines(True),version.splitlines(True),
        fromfile=src.name,tofile=out.name,n=3))
    return {'original':str(src),'original_sha256':sha256_bytes(source_bytes),
        'candidate':str(out),'candidate_sha256':sha256_bytes(actual_bytes),
        'edits':edit_log,'edits_count':len(edit_log),
        'math_tokens_preserved':True,'line_ending':repr(line_sep)},diff


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--en',type=Path,required=True,help='Exact English RC1 TeX from Library')
    parser.add_argument('--kr',type=Path,required=True,help='Exact Korean RC1 TeX from Library')
    parser.add_argument('--output-dir',type=Path,default=Path('formation_phase10_candidates'))
    parser.add_argument('--compile',action='store_true',help='XeLaTeX build each patched full document twice')
    args=parser.parse_args()
    if not (args.en.is_file() and args.kr.is_file()):
        parser.error('Missing original RC1 TeX: use the actual library originals, not a reconstructed PDF')
    args.output_dir = args.output_dir.resolve()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    paths={'EN':(args.en,EN,args.output_dir/'DSD_Formation_Axiom_System_EN_20261105_P10_CANDIDATE.tex'),
           'KR':(args.kr,KR,args.output_dir/'DSD_Formation_Axiom_System_KR_20261105_P10_CANDIDATE.tex')}
    # Safety: verify BOTH complete inputs before writing either candidate.
    for language,(src,edits,out) in paths.items():
        data=src.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        assert all(data.count(e.old)==1 for e in edits),(language,'missing/duplicated patch anchor')
        assert src.resolve()!=out.resolve()
    report={'status':'PATCH_CANDIDATE_WRITTEN','manuscript_author':'Kwon Dominicus',
            'original_release':'2026-10-22 RC1','source_pdf_sha256':'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe',
            'languages':{},'numbered_math_claims_and_refs_preserved':True,
            'source_originals_overwritten':False,'compiled_full_manuscript':args.compile}
    for language,(src,edits,out) in paths.items():
        entry,diff=apply_one(src,edits,out,language)
        diffname=args.output_dir/('PHASE10_'+language+'_SECTION_DIFF.patch')
        diffname.write_text(diff,encoding='utf-8')
        if args.compile:
            entry['compiled']=compile_pdf(out,args.output_dir)
        report['languages'][language]=entry
    out=args.output_dir/'PHASE10_PATCH_MANIFEST.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS: three scoped patches in each language; original inputs preserved, math claim/label tokens preserved')
    print('Output:',args.output_dir)
    if not args.compile:
        print('NOTE: no full manuscript PDF compiled; pass --compile with accessible source TeX')


if __name__=='__main__':main()
