"""Read the canonical Markdown contracts without inferring their semantics."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / '전문가 에이전트 정의.md'
REGISTRY = ROOT / 'docs/materials.md'
USAGES = {'상시', '단계별', '조건부'}


def cells(line):
    return [part.strip() for part in line.strip().strip('|').split('|')]


def usage(value):
    match = re.search(r'\*\*(상시|단계별|조건부)\*\*', value)
    if not match:
        raise ValueError(f'적용 표시 누락: {value}')
    return match[1]


def load_materials():
    records, group = [], ''
    for line in REGISTRY.read_text().splitlines():
        if line.startswith('## '):
            group = line[3:].split(' — ')[0]
        if not line.startswith('| M'):
            continue
        row = cells(line)
        match = re.fullmatch(r'(M\d{2}) (.+)', row[0])
        if not match:
            continue
        if len(row) != 5:
            raise ValueError(f'상세 재료 열 수 오류: {row[0]}')
        records.append(dict(id=match[1], name=match[2], group=group,
                            contract=row[1], job_content=row[2], evidence=row[3],
                            note=row[4], usage=usage(row[4])))
    return records


def load_mapping():
    section = REGISTRY.read_text().split('## 본문과 세부 책임의 대응', 1)[1]
    section = section.split('\n## ', 1)[0]
    records = []
    for line in section.splitlines():
        if not line.startswith('| '):
            continue
        row = cells(line)
        if len(row) == 5 and re.search(r'M\d{2}', row[2]):
            records.append(dict(group=row[0], name=row[1],
                                ids=re.findall(r'M\d{2}', row[2]),
                                responsibility=row[2], usage=row[3], boundary=row[4]))
    return records


def load_summary():
    section = SUMMARY.read_text().split('## 계통별 재료 ✅', 1)[1]
    records, group = [], ''
    for line in section.splitlines():
        if line.startswith('### '):
            group = line[4:].removesuffix(' ✅')
        if not line.startswith('| **'):
            continue
        row = cells(line)
        if row[0].replace('**', '') in USAGES:
            continue
        if len(row) != 6:
            raise ValueError(f'본문 재료 열 수 오류: {row[0]}')
        records.append(dict(name=row[0].replace('**', ''), group=group,
                            usage=usage(row[4]), note=row[5]))
    return records


def validate_materials():
    detail, mapping, summary = load_materials(), load_mapping(), load_summary()
    ids = [row['id'] for row in detail]
    if len(ids) != 57 or set(ids) != {f'M{i:02}' for i in range(1, 58)}:
        raise ValueError('세부 책임 ID가 M01–M57와 일치하지 않음')
    if len(summary) != 59 or len(mapping) != 59:
        raise ValueError('본문·대응표가 59항목이 아님')
    for rows in (summary, mapping):
        if len({r['name'] for r in rows}) != 59 or len({r['group'] for r in rows}) != 9:
            raise ValueError('본문 이름 중복 또는 9계통 누락')
    expected = {r['name']: (r['group'], r['usage']) for r in mapping}
    actual = {r['name']: (r['group'], r['usage']) for r in summary}
    if actual != expected:
        raise ValueError('본문과 대응표의 이름·계통·구분 불일치')
    if {mid for r in mapping for mid in r['ids']} | {'M41'} != set(ids):
        raise ValueError('본문 설명 또는 업무 흐름에 연결되지 않은 세부 책임')
    return detail, mapping, summary


def implementation_text():
    records, _, _ = validate_materials()
    sections, group = [], ''
    for row in records:
        if row['group'] != group:
            group = row['group']
            sections.append(f"### {group}\n")
        sections.append(f"#### {row['id']} {row['name']}\n")
        sections.append(f"**책임·입출력:** {row['contract']}\n")
        sections.append(f"**직무별 내용:** {row['job_content']}\n")
        sections.append(f"**검증 증거:** {row['evidence']}\n")
        sections.append(f"**적용·수행 시점:** {row['note'].replace('<br>', ' — ')}\n")
    template = (ROOT / 'docs/definition/implementation-guide.md').read_text()
    return template.replace('<!-- MATERIAL_CARDS -->', '\n'.join(sections))
