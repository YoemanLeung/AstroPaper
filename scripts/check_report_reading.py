#!/usr/bin/env python3
"""Validate local full-text reading evidence before finalizing a new report.

This checks coverage, source snapshots and evidence records. It cannot certify
that a human or model understood the manuscript; scientific review is required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def validate(report, ledger, root):
    text = report.read_text()
    discussed = text.split('## Top Abstract URLs')[0]
    required = set(re.findall(r'https://arxiv.org/abs/(\d{4}\.\d{4,5})', discussed))
    if not required:
        raise ValueError('No discussed arXiv papers found in report')
    records = json.loads(ledger.read_text())
    if records.get('report') != report.relative_to(root).as_posix():
        raise ValueError('Ledger report path does not match')
    if records.get('report_sha256') != hashlib.sha256(report.read_bytes()).hexdigest():
        raise ValueError('Report changed since reading verification; refresh the evidence review')
    papers = records.get('papers', [])
    ids = [p['id'] for p in papers]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate paper IDs in reading ledger')
    by_id = {p['id']: p for p in papers}
    for paper_id in sorted(required):
        if paper_id not in by_id:
            raise ValueError(f'{paper_id}: missing full-text reading evidence')
        record = by_id[paper_id]
        url = record.get('source_url', '')
        if not re.fullmatch(r'https://arxiv.org/(html|pdf)/' + re.escape(paper_id)
                            + r'(?:v\d+)?(?:\.pdf)?', url):
            raise ValueError(f'{paper_id}: source must be manuscript HTML or PDF')
        if record.get('reading_depth') != 'targeted-full-text':
            raise ValueError(f'{paper_id}: abstract-only summaries cannot pass')
        sections = set(record.get('checked_sections', []))
        if not {'data', 'methods', 'results', 'limitations'} <= sections:
            raise ValueError(f'{paper_id}: missing required section checks')
        claims = record.get('verified_claims', [])
        if not claims or any(not c.get('claim', '').strip() or not c.get('locator', '').strip()
                             for c in claims):
            raise ValueError(f'{paper_id}: provide claims and section/table/figure locators')
        if not record.get('limitations', '').strip():
            raise ValueError(f'{paper_id}: record limitations or explicitly state none identified')
        snapshot = Path(record['snapshot'])
        if not snapshot.is_absolute():
            snapshot = root / snapshot
        data = snapshot.read_bytes()
        if hashlib.sha256(data).hexdigest() != record.get('sha256'):
            raise ValueError(f'{paper_id}: manuscript snapshot checksum mismatch')
        if '/html/' in url and b'ltx_section' not in data:
            raise ValueError(f'{paper_id}: snapshot is not arXiv manuscript HTML')
        if '/pdf/' in url and not data.startswith(b'%PDF-'):
            raise ValueError(f'{paper_id}: snapshot is not PDF')
    return len(required)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--ledger', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    ledger = args.ledger or root / '.codex/reading_checks' / (args.report.stem + '.json')
    try:
        count = validate(args.report.resolve(), ledger, root)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: full-text evidence for {count} discussed papers; scientific review still required')
    return 0


if __name__ == '__main__':
    sys.exit(main())
