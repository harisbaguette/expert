"""로컬 판례의 수집 상태와 검토 후보를 재현한다. 점수는 후보 탐색용이다."""
import csv
import gzip
import hashlib
import html
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path('/Users/haris/Desktop/2. 프로토타입 수준/누리플렉스 법률 에이전트')
OUT = Path(__file__).resolve().parent


def child(parent, name):
    return next(p for p in parent.iterdir() if unicodedata.normalize('NFC', p.name) == name)


def clean(value):
    value = re.sub(r'<br\s*/?>', '\n', str(value or ''), flags=re.I)
    return html.unescape(re.sub(r'<[^>]*>', '', value))


def main():
    corpus = child(child(child(ROOT, '[지식] 법률 데이터'), '한국법령'), '04_판례')
    body = child(corpus, '본문')
    counts, errors, rows = Counter(), [], []
    for i, path in enumerate(sorted(body.glob('*.json')), 1):
        counts['files'] += 1
        try:
            data = json.loads(path.read_text())
        except (ValueError, OSError) as exc:
            counts['parse_error'] += 1
            errors.append({'file': str(path), 'reason': str(exc)})
            continue
        record = data.get('PrecService')
        if not isinstance(record, dict):
            counts['not_prec_service'] += 1
            errors.append({'file': str(path), 'reason': str(data)[:220]})
            continue
        text = clean(record.get('판례내용'))
        if len(text.strip()) < 100:
            counts['missing_or_short_body'] += 1
        else:
            counts['usable_body'] += 1
        issues = clean(record.get('판시사항'))
        issue_count = len(set(re.findall(r'\[(\d+)\]', issues)))
        refs = len(set(re.findall(r'\d{2,4}[가-힣]{1,5}\d{2,}', clean(record.get('참조판례')))))
        dissent = int('반대의견' in text or '별개의견' in text)
        en_banc = int('전원합의체' in str(record.get('판결유형', '')))
        # These objective text signals shortlist candidates, not legal difficulty judgments.
        score = round(min(math.log2(max(len(text), 1)), 18) + min(issue_count, 15) * 2 + min(refs, 30) / 3 + dissent * 6 + en_banc * 4, 3)
        rows.append({
            'id': str(record.get('판례정보일련번호', path.name.split('_')[0])),
            'case': record.get('사건번호', ''), 'date': record.get('선고일자', ''),
            'court': record.get('법원명', ''), 'category': record.get('사건종류명', ''),
            'title': record.get('사건명', ''), 'chars': len(text),
            'issue_markers': issue_count, 'reference_cases': refs,
            'dissent_signal': dissent, 'en_banc': en_banc, 'score': score,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'file': str(path),
        })
        if i % 30000 == 0:
            print(f'확인 {i:,}건', flush=True)
    rows.sort(key=lambda row: (-row['score'], row['id']))
    with gzip.open(OUT / 'corpus_inventory.csv.gz', 'wt', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {'source': str(corpus), 'metadata': json.loads((corpus / '_meta.json').read_text()),
               'counts': dict(counts), 'categories': dict(Counter(r['category'] for r in rows)),
               'error_examples': errors[:12], 'score_is_only_shortlist': True}
    (OUT / 'corpus_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    with gzip.open(OUT / 'corpus_errors.jsonl.gz', 'wt', encoding='utf-8') as f:
        for error in errors:
            f.write(json.dumps(error, ensure_ascii=False) + '\n')
    candidates = rows[:80]
    for category in sorted({r['category'] for r in rows}):
        candidates += [r for r in rows if r['category'] == category][:8]
    unique = {r['id']: r for r in candidates}
    (OUT / 'candidates.json').write_text(json.dumps(list(unique.values()), ensure_ascii=False, indent=2))
    print(json.dumps({'counts': dict(counts), 'candidates': len(unique)}, ensure_ascii=False))
    for row in rows[:45]:
        print(row['id'], row['case'], row['category'], row['score'], row['chars'], row['title'][:70])


if __name__ == '__main__':
    main()
