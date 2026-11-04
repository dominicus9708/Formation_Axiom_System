"""Source-free unit tests for the bilingual Formation v4.5 RC1 patcher.
The real 107KB manuscripts are NOT stored in the public repository.
"""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_DIR = HERE if (HERE / "apply_formation_phase10_patch.py").exists() else HERE.parent / "src"
sys.path.insert(0, str(MODULE_DIR))
import apply_formation_phase10_patch as patch  # noqa: E402


EN_BASE = r'''\documentclass{article}
\author{Kwon Dominicus}
\date{2026.10.22}
\begin{document}
% ----- Section 2.2 -----
Fix a typed material-record signature \(\mathcal S_{\mathrm{mat}}\).
% ----- Section 7.1 -----
Choose \(s\in\Supp(\Base)\), use the empty material-record signature, and set
% ----- Declarations -----
All model constructions, countermodels, and finite-witness counts used in this version are specified in Sections~4 and 7 and Appendix~C.
A separate executable reproducibility package for the finite witnesses and numerical counts is publicly available at \url{https://github.com/dominicus9708/Formation_Axiom_System}.
\end{document}
'''
KR_BASE = r'''\documentclass{article}
\author{Kwon Dominicus}
\date{2026.10.22}
\begin{document}
% ----- 제2.2절 -----
유형화된 재료 기록 서명 \(\mathcal S_{\mathrm{mat}}\)를 고정한다.
% ----- 제7.1절 -----
\(s\in\Supp(\Base)\)를 택하고, 공 재료 기록 서명을 사용하여
% ----- 선언 -----
이 판본에서 사용한 모든 모형 구성, 반모형 및 유한 증인 계수는 제4절, 제7절, 부록~C에 명시되어 있다.
유한 증인과 수치 계수를 위한 별도의 실행 가능한 재현성 패키지는 \url{https://github.com/dominicus9708/Formation_Axiom_System}에서 공개되어 있다.
\end{document}
'''

class PatchSafety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_one(self, language, source):
        old = self.root/f'{language}_RC1.tex'
        output = self.root/f'{language}_P10.tex'
        old.write_text(source, encoding='utf-8')
        before=old.read_bytes()
        info,diff=patch.apply_one(old, patch.EN if language=='EN' else patch.KR, output, language)
        self.assertEqual(old.read_bytes(),before)
        return info,diff,output.read_text(encoding='utf-8')

    def test_english_exact_three_sections(self):
        info,diff,new=self.run_one('EN', EN_BASE)
        self.assertEqual([e['section'] for e in info['edits']],['2.2','7.1','declarations'])
        self.assertIn('Sections~4--7',new)
        self.assertIn('existence witness',new)
        self.assertTrue(info['math_tokens_preserved'])
        self.assertIn('D2 checker',diff)

    def test_korean_exact_three_sections(self):
        info,diff,new=self.run_one('KR',KR_BASE)
        self.assertEqual(info['edits_count'],3)
        self.assertIn('제4--7절과 부록~C',new)
        self.assertIn('존재 증인',new)
        self.assertTrue(info['math_tokens_preserved'])

    def test_fails_closed_if_source_anchor_missing(self):
        with self.assertRaises(ValueError):
            self.run_one('EN',EN_BASE.replace('Fix a typed material-record signature','Altered signature statement'))

    def test_fails_closed_if_anchor_duplicated(self):
        with self.assertRaises(ValueError):
            self.run_one('EN',EN_BASE.replace('% ----- Section 7.1 -----',
                'Fix a typed material-record signature \\(\\mathcal S_{\\mathrm{mat}}\\).\n% ----- Section 7.1 -----'))

    def test_rejects_wrong_manuscript_date(self):
        with self.assertRaises(ValueError):
            self.run_one('KR',KR_BASE.replace('2026.10.22','2026.08.06'))

if __name__=='__main__':
    unittest.main()
