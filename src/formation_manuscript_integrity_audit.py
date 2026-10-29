#!/usr/bin/env python3
"""Source-locked editorial/inventory preflight of Kwon Dominicus's v4.5 Formation PDF.

Uses Poppler CLI tools pdftotext and pdfinfo (not a theorem prover). No PDF editing.
Windows example: python src\\formation_manuscript_integrity_audit.py --pdf "D:\\...\\DSD_Formation_Axiom_System_EN.pdf" --output-dir results
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

SOURCE_SHA256 = 'af721c4188a853880fcc896b80da494e4caa6000ab0af3131ee64cd0770fddfe'
CATEGORIES = {'Theorem': 14, 'Proposition': 16, 'Corollary': 14,
              'Lemma': 2, 'Countermodel': 6, 'Definition': 12, 'Remark': 5}


def read_pdf(pdf: Path) -> tuple[str, int, str]:
    h = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if h != SOURCE_SHA256:
        raise ValueError('Different manuscript: SHA256=' + h)
    for prog in ('pdftotext', 'pdfinfo'):
        if shutil.which(prog) is None:
            raise RuntimeError(f'{prog} required (Poppler CLI). Do not use a different PDF without source locking.')
    p = subprocess.run(['pdftotext', '-layout', str(pdf), '-'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.decode('utf-8').replace('\r\n', '\n')
    # Remove printed page footers inserted between a sentence split across pages.
    text = re.sub(r'\n\s*\d{1,2}\s*\n\f', '\n', text)
    info = subprocess.run(['pdfinfo', str(pdf)], check=True, capture_output=True, text=True).stdout
    m = re.search(r'(?m)^Pages:\s*(\d+)\s*$', info)
    if not m:
        raise ValueError('Cannot determine PDF page count')
    return text, int(m.group(1)), h


def analyze(text: str, page_count: int, sha: str) -> dict:
    # Source headings begin with an independent object name and a dotted numeric label.
    labels = {}
    for category, expected in CATEGORIES.items():
        found = re.findall(r'(?m)^\s*' + category + r'\s+(\d+\.\d+)\s*\(', text)
        if len(found) != expected or len(found) != len(set(found)):
            raise AssertionError((category, found, expected))
        labels[category] = found
    assert page_count == 34
    total = sum(map(len, labels.values()))
    assert total == 69
    flat = {f'{category} {label}' for category, ls in labels.items() for label in ls}
    for key in ('Theorem 4.7', 'Proposition 5.13', 'Proposition 5.14',
                'Theorem 6.5', 'Theorem 6.8', 'Proposition 6.11',
                'Theorem 6.17', 'Theorem 6.19', 'Theorem 6.20',
                'Proposition 6.22', 'Theorem 7.3'):
        assert key in flat, key
    assert re.search(r'\bA\s+Typing and Notation', text)
    assert re.search(r'\bE\s+Optional Infinite-Family Extension', text)
    availability = re.search(r'Data and code availability\.(.*?)\n\s*References', text, re.S)
    assert availability, 'Missing source provenance statement'
    a = re.sub(r'\s+', ' ', availability.group(1)).strip()
    assert 'Sections 4 and 7 and Appendix C' in a
    # Verify exact source-matched Proposition 5.14 distinguishing conditions.
    p514 = re.search(r'Proposition 5\.14.*?(?=\n\s*6\s+Structure-Preserving)', text, re.S)
    assert p514, 'Missing Proposition 5.14 source argument'
    p = re.sub(r'\s+', ' ', p514.group(0))
    assert 'three distinct roles' in p
    assert 'TL (c1 ) = 1' in p and 'TL (c2 ) = −1' in p and 'TL (c3 ) = 0' in p
    headers = list(re.finditer(r'(?m)^\s*E\s+Optional Infinite-Family Extension', text))
    assert len(headers) >= 2, 'Missing Appendix E or its table-of-contents listing'
    e = re.sub(r'\s+', ' ', text[headers[-1].end():text.find('Declarations', headers[-1].end())])
    assert 'unconditionally conver' in e and 'bounded linear' in e
    # Inspect only section presence and editorial scope. Not proofs of theorem validity.
    return {
        'status': 'PASS_SOURCE_LOCKED_EDITORIAL_INVENTORY',
        'source_sha256': sha, 'pdf_pages': page_count,
        'claim_count': total, 'claim_categories': labels,
        'source_exact_proposition_5_14': {
            'one_material_three_roles_source_text_verified': True,
            'term_values': ['1', '-1', '0'],
            'already_checked_by': 'src/formation_semantic_boundary_audit.py: S08',
            'frozen_baseline_alternative_fixture': 'src/formation_axiom_reproduction.py'
        },
        'appendix_e': {'unconditional_convergence': True, 'bounded_linear_transport': True},
        'availability_source_phrase': 'Sections 4 and 7 and Appendix C',
        'editorial_scope_finding': 'Section 5 Countermodel 5.10 and Proposition 5.14; Section 6 Proposition 6.22 are also model/countermodel constructions.',
        'reproducibility_qualification': 'Frozen baseline D2 is a lightweight stage-profile, and its P5.14 is an alternative witness; separate N2 and Phase2 provide source-exact alternatives.',
        'limitations': 'Counts numbered printed labels and detects source strings; does not verify the 69 proofs or any semantic theorem.',
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--pdf', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, default=Path('results'))
    args = p.parse_args()
    txt, pages, sha = read_pdf(args.pdf)
    result = analyze(txt, pages, sha)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / 'formation_manuscript_integrity_audit.json'
    output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')
    print('PASS: exactly 69 printed labels on 34 locked pages; P5.14 and Appendix E source anchors checked')
    print(output)


if __name__ == '__main__':
    main()
