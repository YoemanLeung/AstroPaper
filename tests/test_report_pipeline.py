"""Run with python3 -m unittest discover -s tests -v (requires pandoc)."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reading', ROOT / 'scripts/check_report_reading.py')
reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reading)


class ReadingGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report = self.root / 'report.md'
        self.report.write_text('## Key Findings\n[2609.12345](https://arxiv.org/abs/2609.12345) A result.\n'
                               '## Top Abstract URLs\n[2609.99999](https://arxiv.org/abs/2609.99999) Abstract-only.\n')
        snapshot = self.root / 'paper.html'
        snapshot.write_text('<section class="ltx_section">Results and limitations</section>')
        self.record = {
            'report': 'report.md',
            'report_sha256': hashlib.sha256(self.report.read_bytes()).hexdigest(),
            'papers': [{
                'id': '2609.12345',
                'source_url': 'https://arxiv.org/html/2609.12345v1',
                'snapshot': 'paper.html',
                'sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                'reading_depth': 'targeted-full-text',
                'checked_sections': ['data', 'methods', 'results', 'limitations'],
                'verified_claims': [{'claim': 'Measured result', 'locator': 'Section 4, Table 2'}],
                'limitations': 'Small sample; no population-wide inference.',
            }],
        }
        self.ledger = self.root / 'ledger.json'

    def check(self, record):
        self.ledger.write_text(json.dumps(record))
        return reading.validate(self.report, self.ledger, self.root)

    def test_complete_evidence_and_url_only_exception(self):
        self.assertEqual(self.check(self.record), 1)

    def test_invalid_evidence_blocks_completion(self):
        mutations = [
            ('source_url', 'https://arxiv.org/abs/2609.12345'),
            ('reading_depth', 'abstract-only'),
            ('checked_sections', ['results']),
            ('verified_claims', []),
            ('verified_claims', [{'claim': 'Unsupported', 'locator': ''}]),
            ('limitations', ''),
            ('sha256', 'wrong'),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                record = copy.deepcopy(self.record)
                record['papers'][0][key] = value
                with self.assertRaises(ValueError):
                    self.check(record)

    def test_missing_paper_blocks_completion(self):
        self.record['papers'] = []
        with self.assertRaisesRegex(ValueError, 'missing full-text'):
            self.check(self.record)

    def test_changed_report_requires_new_review(self):
        self.report.write_text(self.report.read_text().replace('A result.', 'A changed claim.'))
        with self.assertRaisesRegex(ValueError, 'Report changed'):
            self.check(self.record)

    def test_fake_manuscript_is_rejected_even_with_valid_hash(self):
        snapshot = self.root / 'paper.html'
        snapshot.write_text('<h1>Abstract only</h1>')
        self.record['papers'][0]['sha256'] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'not arXiv manuscript'):
            self.check(self.record)


class ColorFilterTests(unittest.TestCase):
    source = '''# Example

| Paper | Value |
|---|---|
| [2609.12345](https://arxiv.org/abs/2609.12345) José A. Smith: A title | Result |

José A. Smith finds a result; [2609.12345](https://arxiv.org/abs/2609.12345) José A. Smith.

- [2609.12345](https://arxiv.org/abs/2609.12345) José A. Smith et al. `Title`
  - **Position:** Nicholls+2017; [Jane Doe](https://arxiv.org/abs/2609.99999).

[Survey](https://example.org) stays normal. `José A. Smith 2609.12345` stays code.
'''

    def render(self, target, filtered=True):
        command = ['pandoc', '-f', 'markdown', '-t', target]
        if filtered:
            command += ['--filter', str(ROOT / 'scripts/report_pdf_colors.py')]
        return subprocess.check_output(command, input=self.source, text=True)

    def test_colors_in_table_body_and_literature_references(self):
        result = self.render('latex')
        self.assertEqual(result.count(r'\textcolor{arxivid}{2609.12345}'), 3)
        self.assertEqual(result.count(r'\textcolor{paperauthor}{\textbf{José A. Smith}}'), 4)
        self.assertIn(r'\textcolor{paperauthor}{\textbf{Nicholls+2017}}', result)
        self.assertRegex(result, r'\\textcolor\{paperauthor\}\{\\textbf\{Jane\s+Doe\}\}')
        self.assertEqual(result.count(r'\href{https://arxiv.org/abs/2609.12345}'), 3)
        self.assertIn(r'\href{https://example.org}{Survey}', result)
        self.assertIn(r'\texttt{José\ A.\ Smith\ 2609.12345}', result)

    def test_non_pdf_output_is_unchanged(self):
        self.assertEqual(self.render('html'), self.render('html', filtered=False))


if __name__ == '__main__':
    unittest.main()
