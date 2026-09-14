"""Verify document contracts, graph bypasses and bounded regression examples.

This checks the specification and synthetic state models, not professional skill.
"""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

from definition_lib import ROOT, implementation_text, validate_materials

RESULTS = []


def check(name, condition, detail=''):
    RESULTS.append({'check': name, 'passed': bool(condition), 'detail': detail})
    if not condition:
        raise AssertionError(f'{name}: {detail}')


def reachable(edges, start, target, removed=None):
    todo, seen = [start], set()
    while todo:
        node = todo.pop()
        if node == removed or node in seen:
            continue
        if node == target:
            return True
        seen.add(node)
        todo.extend(b for a, b, _ in edges if a == node)
    return False


def graph(block):
    edges = []
    pattern = r'^\s*(\w+)(?:\[.*?\]|\{.*?\})?\s*-->\s*(?:\|(.*?)\|)?\s*(\w+)'
    for line in block.splitlines():
        if '-->' not in line:
            continue
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f'미지원 연결 문법: {line}')
        edges.append((match[1], match[3], match[2] or ''))
    return edges


def dominates(edges, start, target, gate):
    return reachable(edges, start, target) and not reachable(edges, start, target, gate)


def heading_ids(text):
    # GitHub/Pandoc-compatible explicit IDs are unnecessary for linked Korean headings.
    counts, anchors = Counter(), set()
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        title = re.sub(r'[^\w\-\s]', '', title.lower()).replace(' ', '-')
        suffix = '' if counts[title] == 0 else f'-{counts[title]}'
        anchors.add(title + suffix)
        counts[title] += 1
    return anchors


def check_links(paths):
    total = 0
    for path in paths:
        body = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for raw in re.findall(r'\]\((<[^>]+>|[^)]+)\)', body):
            target = unquote(raw.strip('<>'))
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('//'):
                continue
            dest = (path.parent / parsed.path).resolve() if parsed.path else path
            if not dest.exists():
                raise AssertionError(f'끊긴 링크: {path.relative_to(ROOT)} -> {target}')
            if parsed.fragment and dest.suffix == '.md':
                if parsed.fragment not in heading_ids(dest.read_text()):
                    raise AssertionError(f'없는 제목: {path.relative_to(ROOT)} -> {target}')
            total += 1
    return total


def verify_registry():
    detail, mapping, summary = validate_materials()
    check('재료 57 ID·설명 59·계통 9·이름·적용 표시 대응', True)
    subkeys = {'M10': ('connection', 'isolation'), 'M18': ('evidence', 'version'),
               'M27': ('legal', 'professional'), 'M28': ('agreement', 'platform'),
               'M54': ('experiment', 'simulation')}
    keys = [(r['id'], key) for r in detail for key in subkeys.get(r['id'], ('core',))]
    check('추적할 하위 책임 키 62개·중복 없음', len(keys) == len(set(keys)) == 62)
    text = (ROOT / 'docs/materials.md').read_text()
    declared = {mid: tuple(keys.strip().split(' / ')) for mid, keys in re.findall(r'^\| (M\d{2}) \| ([a-z]+ / [a-z]+) \|', text, re.M)}
    check('하위 책임 키와 정본 선언 일치', declared == subkeys)
    return summary


def verify_guide():
    generated = ROOT / '전문가 에이전트 정의 2.md'
    check('정의 2와 정본 생성 결과 일치', generated.read_text() == implementation_text())
    check('57개 상세 책임 카드 각각 1개', len(re.findall(r'^#### M\d{2} ', generated.read_text(), re.M)) == 57)


def verify_scopes():
    with (ROOT / 'docs/definition/occupation-scopes.csv').open(encoding='utf-8-sig', newline='') as f:
        scopes = list(csv.DictReader(f))
    with (ROOT / 'docs/reviews/occupation-work-review.csv').open(encoding='utf-8-sig', newline='') as f:
        original = list(csv.DictReader(f))
    check('166개 직무 ID·명칭 보존', [(int(r['번호']), r['직무']) for r in scopes] == [(int(r['번호']), r['직무']) for r in original])
    check('166개 범위 필수 필드 존재', len(scopes) == 166 and all(all(str(v).strip() for v in row.values()) for row in scopes))
    check('직무 유형 58·80·28 보존', sorted(Counter(r['유형'] for r in scopes).values()) == [28, 58, 80])
    check('실제 능력 미검증 상태 보존', all(r['현재 지원 상태'] == '설계 범위 정리 / 실제 구현·전문 능력 미검증' for r in scopes))


def load_graphs():
    main_md = (ROOT / '전문가 에이전트 정의.md').read_text()
    blocks = re.findall(r'```mermaid\n(.*?)```', main_md, re.S)
    groups = {}
    for key in ('COVER', 'RECEIVE', 'ACTION', 'W_START'):
        matches = [b for b in blocks if re.search(rf'\b{key}\b', b)]
        check(f'{key} 기준 흐름이 하나 존재', len(matches) == 1)
        groups[key] = graph(matches[0])
    return main_md, blocks, groups


def graph_invariants():
    invariants = []
    for gate in ('COVER', 'QUALITY', 'HUMAN', 'AUTONOMY', 'COST', 'SUSTAIN'):
        invariants.append(('COVER', 'S', 'PASS', gate))
    for gate in ('RECEIVE', 'URGENT', 'SYNC', 'SCOPE', 'PROBLEM', 'DATA', 'PLAN', 'READY'):
        invariants.append(('RECEIVE', 'REQ', 'EXEC', gate))
    for gate in ('VERIFY', 'VALID', 'COMPLETE'):
        invariants.append(('RECEIVE', 'REQ', 'DELIVER', gate))
    for gate in ('GATE', 'SAVE', 'LIVE'):
        invariants.append(('ACTION', 'ACTION', 'CALL', gate))
    invariants += [('ACTION', 'ACTION', 'DONE', 'CHECK'), ('W_START', 'W_START', 'W_RETURN', 'W_SYNC')]
    return invariants


def verify_graph_gates(groups, invariants):
    for key, start, end, gate in invariants:
        check(f'필수 경유 {key}:{gate}', dominates(groups[key], start, end, gate))
    mutation_count = 0
    for key, start, end, gate in invariants:
        edges = groups[key]
        incoming = [a for a, b, _ in edges if b == gate]
        outgoing = [b for a, b, _ in edges if a == gate]
        mutated = [(a,b,label) for a,b,label in edges if a != gate and b != gate]
        mutated += [(a,b,'injected gate omission') for a in incoming for b in outgoing]
        check(f'우회 반례 검출 {key}:{gate}', not dominates(mutated, start, end, gate))
        mutation_count += 1
    return mutation_count


def verify_branches(groups, main_md):
    # Branch-level checks prevent deadlock and unsafe retry paths that dominators alone miss.
    main_edges, action, wait = groups['RECEIVE'], groups['ACTION'], groups['W_START']
    check('자료 직접 확보 경로', reachable(main_edges, 'ENOUGH', 'ACQUIRE', 'WAIT'))
    check('직접 확보 뒤 상태 재대조', dominates(main_edges, 'ACQUIRE', 'EXEC', 'SYNC'))
    check('기존 건·대기 재개 뒤 상태 재대조', dominates(main_edges, 'WAIT', 'EXEC', 'SYNC'))
    check('보호 조치 뒤 재대조', dominates(main_edges, 'PROTECT', 'EXEC', 'SYNC'))
    check('미해결 긴급 범위의 차단 설명', '긴급 대응이나 권한·검증이 막힌 범위는 계속 차단' in main_md)
    unknown = [(a, b, label) for a, b, label in action if not (a == 'QUERY' and b == 'STATE')]
    check('새 원천 증거 없이 불명 결과 재실행 불가', not reachable(unknown, 'QUERY', 'CALL'))
    check('처리 불명 확인 만료 출구', reachable(action, 'QUERY', 'RESULT', 'STATE'))
    check('부분 성공 뒤 전체 성공 직행 불가', dominates(action, 'PART', 'DONE', 'CHECK'))
    check('취소·보상 재실행은 권한 재검사', dominates(action, 'CANCEL', 'CALL', 'GATE'))
    check('대기 기한 만료·취소 종료 출구', reachable(wait, 'W_ALT', 'W_STOP') and reachable(wait, 'W_EVENT', 'W_STOP'))
    check('무응답이 실행 재개로 직행하지 않음', not reachable(wait, 'W_SLEEP', 'W_RETURN', 'W_EVENT'))
    check('모든 흐름 노드에 도달 가능', all(reachable(edges, start, node) for key, start in [('COVER','S'), ('RECEIVE','REQ'), ('ACTION','ACTION'), ('W_START','W_START')] for edges in [groups[key]] for node in {n for a,b,_ in edges for n in (a,b)}))


def verify_regression():
    # Historical regression is executed in a temporary directory; archive outputs remain untouched.
    with tempfile.TemporaryDirectory(prefix='expert-definition-check-') as directory:
        model = Path(directory) / 'occupation-dynamic-models.py'
        shutil.copyfile(ROOT / 'docs/실험 결과/재현/occupation-dynamic-models.py', model)
        subprocess.run([sys.executable, str(model)], check=True, capture_output=True, text=True)
        regression = json.loads(model.with_suffix('.json').read_text())['summary']
    check('기존 복합 모형 회귀 8모형·42구성·19누락 반례', regression == {'model_count':8, 'enumerated_configurations':42, 'omission_counterexamples':19}, regression)
    return regression


def verify_active_links():
    active = [ROOT / p for p in ['전문가 에이전트 정의.md', '전문가 에이전트 정의 2.md', '진행-계획.md', 'docs/README.md', 'docs/materials.md', 'docs/runtime.md', 'docs/evaluation.md', 'docs/reviews/material-baseline-review.md', 'docs/reviews/material-counterexamples-v2.md', 'docs/definition/README.md']]
    # This generated file is linked by the index and is finalized below.
    result_path = ROOT / 'docs/definition/verification-result.json'
    if not result_path.exists():
        result_path.write_text('{}\n')
    total_links = check_links(active)
    check('활성 문서의 로컬 링크·제목 연결', True, {'links_checked': total_links})
    return active


def verify_artifacts(blocks, summary):
    for name in ('전문가 에이전트 정의', '진행-계획'):
        md, html = ROOT / f'{name}.md', ROOT / f'{name}.html'
        digest = hashlib.sha256(md.read_bytes()).hexdigest()
        check(f'{name} HTML 판본 일치', f'source-sha256: {digest}' in html.read_text())
    render_manifest = json.loads((ROOT / 'docs/definition/rendered/manifest.json').read_text())
    check('Mermaid 전부 렌더됨', render_manifest['diagram_count'] == len(blocks) and render_manifest['source_sha256'] == hashlib.sha256((ROOT / '전문가 에이전트 정의.md').read_bytes()).hexdigest())
    for svg in (ROOT / 'docs/definition/rendered').glob('*.svg'):
        ET.parse(svg)
    formula = ET.parse(ROOT / 'docs/전개-수식/전개-수식.svg')
    labels = [el.text for el in formula.iter() if el.tag.endswith('}text')]
    check('구성 도식에 59개 본문 이름 포함', all(row['name'] in labels for row in summary))
    check('생성 SVG XML 유효', True)


def write_results(active, mutation_count, regression):
    result_path = ROOT / 'docs/definition/verification-result.json'
    snapshot = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in active + [ROOT / 'docs/definition/occupation-scopes.csv', ROOT / 'docs/전개-수식/전개-수식.svg']}
    result = {'kind': 'definition consistency and bounded counterexamples; not professional performance', 'generated_at': datetime.now(timezone.utc).isoformat(), 'baseline': 'v2', 'counts': {'systems':9, 'display_items':59, 'responsibility_ids':57, 'tracking_keys':62, 'occupations':166}, 'checks_passed':len(RESULTS), 'graph_mutations_detected':mutation_count, 'historical_regression':regression, 'checks':RESULTS, 'source_sha256':snapshot, 'tool_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for pattern in ('*.py', '*.cjs', '*.css') for p in (ROOT / 'docs/definition').glob(pattern)}, 'limits':['작성자에 의한 문서 구조·경로 검사', '그래프 연결 검사는 노드 안의 전문 판단 능력을 검증하지 않음', '과거 모형은 제한된 합성 상태·계산 검사', '실제 직무 에이전트·외부 시스템·독립 전문가 비교 미실행']}
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('checks_passed','graph_mutations_detected','historical_regression')}, ensure_ascii=False))


def main():
    summary = verify_registry()
    verify_guide()
    verify_scopes()
    main_md, blocks, groups = load_graphs()
    mutation_count = verify_graph_gates(groups, graph_invariants())
    verify_branches(groups, main_md)
    regression = verify_regression()
    active = verify_active_links()
    verify_artifacts(blocks, summary)
    write_results(active, mutation_count, regression)


if __name__ == '__main__':
    main()
