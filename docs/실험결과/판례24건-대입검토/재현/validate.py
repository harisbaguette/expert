"""검토 산출물의 출처·참조·집계를 검사한다. 법률 능력 합격 검사가 아니다."""
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
REPORT = HERE.parent
PROJECT = HERE.parents[3]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_checks(selected, assessments):
    assert len(selected) == len(assessments) == 24
    assert {r['review_id'] for r in selected} == {f'C{i:02}' for i in range(1, 25)}
    assert len({(r['court'], r['date'], r['case']) for r in selected}) == 24
    details = {r['review_id']: r for r in assessments}
    material_ids = set(re.findall(r'\| (M\d{2}) ', (HERE / '검토정의/materials.md').read_text()))
    assert len(material_ids) == 57
    for row in selected:
        raw = gzip.decompress((HERE / '원본' / f'{row["id"]}.json.gz').read_bytes())
        assert digest(raw) == row['sha256'], row['review_id']
        record = json.loads(raw)['PrecService']
        assert record['사건번호'] == row['case']
        assert record['선고일자'] == row['date']
        item = details[row['review_id']]
        assert set(item['materials']) <= material_ids
        assert item['autonomous_execution'] == '미실시'
        for term in item['evidence_terms']:
            assert term in raw.decode(), (row['review_id'], term)
        assert row['order'], row['review_id']
        assert (HERE / '원문' / f'{row["review_id"]}_{row["id"]}.txt').exists()
    return {'source_hashes': 24, 'unique_cases': 24, 'material_references': '유효', 'evidence_anchor_presence': '통과'}


def report_checks(selected):
    with (REPORT / '02_24건_대입결과.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert [r['ID'] for r in rows] == [r['review_id'] for r in selected]
    markdown = (REPORT / '02_24건_대입결과.md').read_text()
    assert len(re.findall(r'^## C\d{2} ·', markdown, re.M)) == 24
    links = 0
    for document in REPORT.glob('*.md'):
        for target in re.findall(r'\]\(([^\n]+?)\)', document.read_text()):
            if target.startswith(('http:', 'https:', '#')):
                continue
            target = unquote(target.strip('<>').split('#')[0])
            assert (document.parent / target).exists(), (document.name, target)
            links += 1
    return {'case_cards': 24, 'csv_rows': len(rows), 'local_links': links}


def corpus_checks():
    summary = json.loads((HERE / 'corpus_summary.json').read_text())
    with gzip.open(HERE / 'corpus_inventory.csv.gz', 'rt', encoding='utf-8') as f:
        count = sum(1 for _ in csv.DictReader(f))
    with gzip.open(HERE / 'corpus_errors.jsonl.gz', 'rt', encoding='utf-8') as f:
        errors = sum(1 for _ in f)
    counts = summary['counts']
    assert count == counts['usable_body'] + counts['missing_or_short_body']
    assert errors == counts['not_prec_service']
    assert count + errors == counts['files']
    return {'inventory_rows': count, 'error_rows': errors, 'total': count + errors}


def definition_checks():
    manifest = json.loads((HERE / 'definition_manifest.json').read_text())
    changed = []
    for item in manifest:
        snapshot = HERE / '검토정의' / Path(item['file']).name
        assert digest(snapshot.read_bytes()) == item['sha256']
        original = PROJECT / item['file']
        if original.exists() and digest(original.read_bytes()) != item['sha256']:
            changed.append(item['file'])
    return {'snapshot_files': len(manifest), 'live_files_changed_since_snapshot': changed}


def main():
    selected = json.loads((HERE / 'selected_cases.json').read_text())
    assessments = json.loads((HERE / 'case_assessments.json').read_text())
    result = {'scope': '검토 산출물의 무결성·참조·집계만 검사. 법리 정확도·에이전트 실행 능력·승소율은 채점하지 않음.',
              'source': source_checks(selected, assessments), 'corpus': corpus_checks(),
              'definition': definition_checks()}
    # Write before link validation so the report can reference this artifact.
    (HERE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    result['reports'] = report_checks(selected)
    result['status'] = '검토 기록 검증 통과'
    (HERE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
