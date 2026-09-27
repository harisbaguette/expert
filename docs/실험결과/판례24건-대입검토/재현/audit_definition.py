"""보존한 정의의 실제 간선·대응표를 검사한다. 자연어 법률 판단은 채점하지 않는다."""
import json
import re
from collections import deque
from pathlib import Path

OUT = Path(__file__).resolve().parent
SNAPSHOT = OUT / '검토정의'


def path_between(edges, start, end, blocked=()):
    queue = deque([(start, [start])])
    seen = set(blocked)
    while queue:
        node, path = queue.popleft()
        if node in seen:
            continue
        if node == end:
            return path
        seen.add(node)
        queue.extend((b, path + [b]) for a, b, _ in edges if a == node)
    return None


def main():
    doc = (SNAPSHOT / '전문가 에이전트 정의.md').read_text()
    detail = (SNAPSHOT / 'materials.md').read_text()
    section = doc.split('## 계통별 재료')[1].split('## 사용 구조')[0]
    names = []
    for line in section.splitlines():
        if line.startswith('| **') and '✅' in line:
            cells = line.strip('|').split('|')
            if len(cells) == 6:
                names.append(re.search(r'\*\*(.*?)\*\*', cells[0]).group(1))
    mapping = detail.split('| 본문 계통 |')[1].split('## 환경 —')[0]
    missing = [name for name in names if f'| {name} |' not in mapping]
    flow = doc.split('## 업무 처리 흐름')[1].split('## 수식')[0]
    edges = []
    for line in flow.splitlines():
        match = re.match(r'\s*(\w+)\s+-->\s*(?:\|([^|]*)\|\s*)?(\w+)\s*$', line)
        if match:
            a, label, b = match.groups()
            edges.append((a, b, label))
    probes = [
        {'id': 'D02', 'issue': '목표 불변인 기존 건이 새 자료 검증을 우회할 수 있는 도식 경로',
         'path': path_between(edges, 'LOAD_CASE', 'OPTIONS', ['COLLECT', 'VALIDATE_DATA'])},
        {'id': 'D03', 'issue': '사용자 요청은 긴급피해 판단을 거치지 않고 접수로 들어가는 도식 경로',
         'path': path_between(edges, 'REQ', 'INTAKE_CHECK', ['HARM'])},
        {'id': 'D04', 'issue': '실패 판단 노드에 부분성공·결과불명 분기가 명시되지 않음',
         'branches': [e for e in edges if e[0] == 'EXEC_FAIL']},
        {'id': 'D05', 'issue': '의도 답변 대기의 반복 경로에 기한·종료 분기가 명시되지 않음',
         'branches': [e for e in edges if e[0] in ('INTENT_WAIT', 'INTENT_ASK', 'INTENT_CONFIRMED', 'ASSUME_SAFE')]},
    ]
    result = {'scope': '보존한 큰 업무 처리 흐름의 정적 도식 검사; 실행 엔진 동작 시험 아님',
              'material_count': len(names), 'mapped_material_count': len(names) - len(missing),
              'unmapped_names': missing, 'probes': probes,
              'limitation': '분기 의미와 상시 규칙을 자동 실행한 것이 아니다. 상세 runtime 및 새 사용 구조의 보완을 함께 읽어야 한다.'}
    (OUT / 'definition_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
