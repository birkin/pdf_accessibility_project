"""
Script to reduce the huge veraPDF JSON output to a more comprehensible summary.

Usage:

## default: accessibility-focused, top 15
uv run ./reduce_verapdf_json.py /path/to/your_verapdf.json -o /path/to/vera_reduced.json

## include all failed rules (not just accessibility)
uv run ./reduce_verapdf_json.py /path/to/your_verapdf.json --all-rules

## show only top 5 failed rules
uv run ./reduce_verapdf_json.py /path/to/your_verapdf.json --top 5

The original veraPDF json output was produced by this command:
```
    command: list[str] = [
        str(verapdf_cli_path),
        '-f', 'ua1',
        '--maxfailuresdisplayed', '999999',
        '--format', 'json',
        '--success',
        str(pdf_path),
    ]
```
"""

import argparse
import json
from pathlib import Path


## builds reduced dict
def reduce_verapdf(data: dict, focus_accessibility: bool = True, top_n: int = 15) -> dict:
    ## locate validation result
    vres = None
    try:
        vres = data['report']['jobs'][0]['validationResult'][0]
    except Exception:
        raise SystemExit('Could not locate validationResult[0] in JSON.')

    profile = vres.get('profileName')
    compliant = vres.get('compliant')
    statement = vres.get('statement')

    details = vres.get('details') or {}
    counts = {
        'rules_passed': details.get('passedRules', 0),
        'rules_failed': details.get('failedRules', 0),
        'checks_passed': details.get('passedChecks', 0),
        'checks_failed': details.get('failedChecks', 0),
    }

    rule_summaries = details.get('ruleSummaries') or []

    ## heuristics to select accessibility-centric rules
    access_tags = {
        'structure',
        'artifact',
        'text',
        'lang',
        'font',
        'table',
        'list',
        'link',
        'annotation',
        'toc',
        'heading',
        'alt-text',
        'page',
    }

    def is_access_rule(rs: dict) -> bool:
        tags = set(rs.get('tags') or [])
        if tags & access_tags:
            return True
        desc = (rs.get('description') or '') + ' ' + (rs.get('test') or '')
        phrases = [
            'StructTreeRoot',
            'Artifact',
            'tagged',
            'natural language',
            'Lang',
            'MarkInfo',
            'Alternative',
            'Alt',
            'Figure',
            'Table',
            'List',
            'Link',
            'Heading',
            'ViewerPreferences',
            'DisplayDocTitle',
            'Metadata',
        ]
        dlow = desc.lower()
        return any(p.lower() in dlow for p in phrases)

    # select failed rules (optionally accessibility-filtered)
    failed_rules = [
        rs
        for rs in rule_summaries
        if (rs.get('ruleStatus') == 'FAILED' or rs.get('status') == 'failed') and rs.get('failedChecks', 0) > 0
    ]
    if focus_accessibility:
        failed_rules = [rs for rs in failed_rules if is_access_rule(rs)]

    # sort by failedChecks desc
    failed_rules.sort(key=lambda r: (r.get('failedChecks', 0), r.get('passedChecks', 0)), reverse=True)

    # trim fields
    top = []
    for rs in failed_rules[:top_n]:
        top.append(
            {
                'clause': rs.get('clause'),
                'test_number': rs.get('testNumber'),
                'description': rs.get('description'),
                'failed_checks': rs.get('failedChecks', 0),
                'tags': rs.get('tags', []),
            }
        )

    # quick remediation hints (metadata-level)
    quick_hints = []
    # lang
    if any('lang' in (rs.get('tags') or []) for rs in failed_rules):
        quick_hints.append('Set Catalog /Lang (e.g., en-US) and/or per-structure Lang.')
    # markinfo / structure
    if any('structure' in (rs.get('tags') or []) for rs in failed_rules):
        quick_hints.append('Add /StructTreeRoot and tag meaningful content; mark decorative items as Artifacts.')
    # viewer prefs
    for rs in failed_rules:
        if 'DisplayDocTitle' in (rs.get('description') or ''):
            quick_hints.append('Set /ViewerPreferences/DisplayDocTitle = true.')
            break
    # metadata stream
    for rs in failed_rules:
        text = (rs.get('description') or '') + ' ' + (rs.get('test') or '')
        if 'Metadata' in text or 'XMP' in text:
            quick_hints.append('Embed XMP metadata stream (dc:title etc.).')
            break

    reduced = {
        'profile': profile,
        'compliant': compliant,
        'statement': statement,
        'counts': counts,
        'top_failed_rules': top,
        'focus_accessibility': focus_accessibility,
        'hints': quick_hints,
    }
    return reduced


def main():
    ap = argparse.ArgumentParser(description='reduce veraPDF JSON to a targeted summary')
    ap.add_argument('input', help='path to veraPDF JSON')
    ap.add_argument('-o', '--output', help='path to write reduced JSON', default='vera_reduced.json')
    ap.add_argument('--all-rules', action='store_true', help='do not filter to accessibility-centric rules')
    ap.add_argument('--top', type=int, default=15, help='number of top failed rules to include')
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text('utf-8'))
    reduced = reduce_verapdf(data, focus_accessibility=(not args.all_rules), top_n=args.top)
    Path(args.output).write_text(json.dumps(reduced, indent=2), encoding='utf-8')
    print(f'wrote {args.output}')


if __name__ == '__main__':
    main()
