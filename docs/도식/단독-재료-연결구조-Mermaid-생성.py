#!/usr/bin/env python3
"""단독-재료-연결구조.json(현재 정본, 79재료)을 읽어
네이티브 Mermaid flowchart(dagre 레이아웃) 소스를 생성한다.

정의1 문서('## 사용 구조' > '### 1. 단독 상황')에 이미 박혀 있는
이미지(solo-material-relations.png)와 같은 데이터를 그대로 쓰되,
Mermaid 엔진이 배치를 다시 계산하므로 픽셀 단위 동일 위치는 낼 수 없고
흐름 순서·묶음(subgraph)·갈래 방향 같은 상대 배치만 맞춘다.

레이아웃은 dagre(기본 렌더러)를 쓴다 — elk는 이 그래프에서 진입 노드(시작)를
맨 위에, 종료 노드를 맨 아래에 두지 못했다(keepEntryNodeOnTop·
forceNodeModelOrder·considerModelOrder·선언 순서 재배치를 다 걸어도 시작 노드가
전체 높이의 36~49% 지점에 그대로 남음 — elk NETWORK_SIMPLEX가 진짜 위상 순서가
아니라 간선 길이 합을 기준으로 배치하기 때문으로 보임). 같은 데이터를 dagre로
그리면 별도 설정 없이 시작 노드가 0.1~3.2%, 종료 노드가 99.4% 지점에 온다
(단독-재료-연결구조-Mermaid-렌더.cjs 로 렌더 후 좌표 확인, 2026-09-22). 도식-설계.md의
elk 권고는 노드 113개짜리 다른(더 큰) 순서도 기준이고, 이 도식(129개 안팎)은
dagre로 그려도 폭이 elk보다 오히려 좁다(6249px < elk 6607px).
  - 6모양 6색 분류 + linkStyle 6역할 색상
  - 화살표는 항상 A --> B (A <-- B 는 렌더러가 조용히 버림)
  - 시작/종료 노드는 위치(dagre가 위상대로 배치)에 더해 글자(▶ 시작 ·/■ 종료 ·)와
    색(termstart/termend)으로도 이중 표시한다

사용법:
  python3 단독-재료-연결구조-Mermaid-생성.py [--out FILE] [--embed]
    --embed: 정의1 문서의 '### 1. 단독 상황' 절 기존 이미지 아래에 삽입
"""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'docs/도식/단독-재료-연결구조.json'
DOC = ROOT / '전문가 에이전트 정의.md'
OUT_DEFAULT = ROOT / 'docs/도식/usage-structure-solo.mmd'

# 8종 노드 → 6모양 6색 확장 매핑 (도식-설계.md 기존 6종 + source/unused 확장)
KIND_STYLE = {
    'terminal':      dict(cls='term',    open='(["',  close='"])'),   # 캡슐/녹색 — 시작-끝 단계
    'decision':      dict(cls='decide',  open='{"',   close='"}'),   # 마름모 — 판단
    'decisionwide':  dict(cls='decide',  open='{"',   close='"}'),
    'process':       dict(cls='action',  open='["',   close='"]'),    # 사각/파랑 — 실행
    'source':        dict(cls='human',   open='["',   close='"]'),    # 사각/주황 — 재료 조회(외부 교환)
    'reference':    dict(cls='human',   open='["',   close='"]'),
    'data':          dict(cls='record',  open='[("',  close='")]'),   # 실린더/회색 — 자료
    'stop':          dict(cls='stop',    open='(["',  close='"])'),    # 캡슐/빨강 — 정지
    'unused':        dict(cls='unused',  open='["',   close='"]'),    # 사각/점선회색 — 쓰지 않음
}

# 참고 이미지(solo-material-relations.png)와 같은 옅은 파스텔 톤 — 흰 배경 문서 기준
CLASS_DEFS = '''\
classDef term fill:#d9f2e6,stroke:#4caf7d,stroke-width:1.5px,color:#1a1a2e
classDef decide fill:#e6d9f7,stroke:#9b6dd6,stroke-width:1.5px,color:#1a1a2e
classDef action fill:#dbe9fb,stroke:#5b8fd1,stroke-width:1.5px,color:#1a1a2e
classDef human fill:#fbe3c8,stroke:#d99a4e,stroke-width:1.5px,color:#1a1a2e
classDef record fill:#e3e7ee,stroke:#8f97a8,stroke-width:1.5px,color:#1a1a2e
classDef stop fill:#fbdada,stroke:#d16565,stroke-width:1.5px,color:#1a1a2e
classDef unused fill:#eceef1,stroke:#9aa0a8,stroke-width:1px,stroke-dasharray:4 3,color:#6b7280
classDef termstart fill:#c3f0d9,stroke:#16a34a,stroke-width:3.5px,color:#0f3d24
classDef termend fill:#d9f2e6,stroke:#4caf7d,stroke-width:3.5px,stroke-dasharray:2 2,color:#1a1a2e'''

GROUP_TITLE_STYLE = 'stroke:#94a3b8,stroke-width:1px,stroke-dasharray:2 4,color:#3a3f4b'
GROUP_EVIDENCE_STYLE = f'fill:#eef8f1,{GROUP_TITLE_STYLE}'
GROUP_RULES_STYLE = f'fill:#f3eefb,{GROUP_TITLE_STYLE}'
GROUP_PLAIN_STYLE = 'fill:none,stroke:none'

ROLE_COLOR = {
    '시작진입': '#4caf7d',
    '예':      '#5fb890',
    '그냥다음': '#5b8fd1',
    '아니오':   '#d99a4e',
    '되돌아감': '#c46ec4',
    '멈춤':    '#d16565',
    '참조':    '#718096',
}


RESERVED = {
    'graph', 'subgraph', 'end', 'style', 'linkstyle', 'classdef', 'class',
    'click', 'direction', 'tb', 'td', 'bt', 'rl', 'lr', 'flowchart',
}


def safe_id(raw_id: str) -> str:
    """Mermaid 예약어(style/end/class 등)와 겹치는 노드·그룹 id는 충돌을 피해 접미사를 붙인다."""
    return f'{raw_id}_n' if raw_id.lower() in RESERVED else raw_id


def esc(s: str) -> str:
    return html.escape(s, quote=True).replace('\n', '<br/>')


def node_label(n: dict, marker: str = '') -> str:
    title = esc(n.get('title', n['id']))
    if n.get('material') == '현재 작업 정보' and n.get('condition'):
        title += ' · ' + esc(n['condition'])
    if n.get('kind') == 'reference':
        title = '참조 기준 · ' + title
    if n.get('priority_rank'):
        title = f'{n["priority_rank"]}순위 · ' + title
    if marker:
        title = marker + title
    body = n.get('body', '')
    if n.get('caption'):
        body = '\n'.join(filter(None, [n['caption'], body]))
    if body:
        return f"<b>{title}</b><br/><span style='font-size:11px'>{esc(body)}</span>"
    return f'<b>{title}</b>'


def rect_contains(outer, inner) -> bool:
    ox1, oy1 = outer['x'], outer['y']
    ox2, oy2 = ox1 + outer['w'], oy1 + outer['h']
    ix1, iy1 = inner['x'], inner['y']
    ix2, iy2 = ix1 + inner['w'], iy1 + inner['h']
    return ox1 - 1 <= ix1 and oy1 - 1 <= iy1 and ix2 <= ox2 + 1 and iy2 <= oy2 + 1


def group_area(g):
    return g['w'] * g['h']


def build(data: dict) -> str:
    nodes = list(data['nodes'].values())
    groups = data['groups']
    edges = data['edges']

    # 흐름 간선(참조 제외)만으로 진입/종료 노드 계산 — dagre가 이 순서대로 시작을 맨 위에,
    # 종료를 맨 아래에 배치해 주므로 위치가 곧 근거이고, 글자·색은 보조 표시다
    indeg, outdeg = {}, {}
    for e in edges:
        if e['kind'] == 'reference':
            continue
        outdeg[e['source']] = outdeg.get(e['source'], 0) + 1
        indeg[e['target']] = indeg.get(e['target'], 0) + 1
    start_ids = {n['id'] for n in nodes if n.get('kind') == 'terminal' and indeg.get(n['id'], 0) == 0}
    finish_ids = {n['id'] for n in nodes if n.get('kind') == 'terminal'
                  and outdeg.get(n['id'], 0) == 0 and n['id'] not in start_ids}

    # 노드 -> 가장 좁은(가장 구체적인) 소속 그룹 하나만 고름(=바로 담긴 subgraph)
    node_group = {}
    for n in nodes:
        candidates = [g for g in groups if rect_contains(g, n)]
        if not candidates:
            continue
        node_group[n['id']] = min(candidates, key=group_area)['id']

    # 그룹 -> 부모 그룹(자기보다 넓고 자길 담는 그룹 중 가장 좁은 것)
    group_by_id = {g['id']: g for g in groups}
    group_parent = {}
    for g in groups:
        parents = [p for p in groups if p['id'] != g['id'] and rect_contains(p, g)]
        if parents:
            group_parent[g['id']] = min(parents, key=group_area)['id']

    group_children_groups = {g['id']: [] for g in groups}
    for gid, pid in group_parent.items():
        group_children_groups[pid].append(gid)

    group_children_nodes = {g['id']: [] for g in groups}
    for n in nodes:
        gid = node_group.get(n['id'])
        if gid:
            group_children_nodes[gid].append(n)

    nodes_by_id = {n['id']: n for n in nodes}

    def node_line(n, indent):
        kind = n.get('kind', 'process')
        style = KIND_STYLE.get(kind, KIND_STYLE['process'])
        if n['id'] in start_ids:
            marker = '▶ 시작 · '
        elif n['id'] in finish_ids:
            marker = '■ 종료 · '
        else:
            marker = ''
        label = node_label(n, marker)
        return f'{indent}{safe_id(n["id"])}{style["open"]}{label}{style["close"]}'

    lines = []
    lines.append('%%{init: {"flowchart": {"defaultRenderer": "dagre-wrapper", "htmlLabels": true, '
                  '"nodeSpacing": 24, "rankSpacing": 32, "padding": 16, "wrappingWidth": 300, '
                  '"curve": "linear", "useMaxWidth": true}} }%%')
    lines.append('flowchart TB')
    lines.append('')

    top_groups = [g for g in groups if g['id'] not in group_parent]
    top_groups.sort(key=lambda g: g['y'])

    def emit_group(gid, indent):
        g = group_by_id[gid]
        title = g.get('title', '').strip()
        gtitle = esc(title) if title else ' '
        if gid == 'rank':
            gtitle = '이 도식의 업무 기준 순서 · 같은 순위는 함께 적용'
        lines.append(f'{indent}subgraph {safe_id(gid)}["{gtitle}"]')
        inner = indent + '  '
        members = sorted(
            group_children_nodes[gid] + [
                ('GROUP', cgid) for cgid in group_children_groups[gid]
            ],
            key=lambda m: (m['y'] if isinstance(m, dict) else group_by_id[m[1]]['y'])
        )
        for m in members:
            if isinstance(m, dict):
                lines.append(node_line(m, inner))
            else:
                emit_group(m[1], inner)
        lines.append(f'{indent}end')

    # dagre는 ELK와 달리 선언 순서를 배치에 안 쓰고 그래프 위상(누가 누구를 가리키는지)만
    # 본다(도식-설계.md 175행) — 그래서 선언 순서 재배치가 필요 없고, 원래 있던 대로
    # 그룹은 y좌표순, 묶이지 않은 노드도 y좌표순으로 그대로 나열한다
    ungrouped = [n for n in nodes if n['id'] not in node_group]
    ungrouped.sort(key=lambda n: n['y'])

    for g in top_groups:
        emit_group(g['id'], '  ')
        lines.append('')

    for n in ungrouped:
        lines.append(node_line(n, '  '))
    lines.append('')

    def edge_role(e):
        src = nodes_by_id.get(e['source'])
        tgt = nodes_by_id.get(e['target'])
        if e['kind'] == 'reference':
            return '참조'
        if e['kind'] == 'return':
            return '되돌아감'
        if e['kind'] == 'blocked':
            return '아니오'
        if src and src.get('kind') == 'terminal':
            return '시작진입'
        if tgt and tgt.get('kind') in ('stop', 'terminal'):
            return '멈춤'
        if src and src.get('kind') in ('decision', 'decisionwide'):
            return '예'
        return '그냥다음'

    roles = []
    for e in edges:
        label = e.get('label', '').strip()
        connector = '---' if e['kind'] == 'reference' else '-->'
        arrow = f'{safe_id(e["source"])} {connector}'
        if label:
            arrow += f'|{esc(label)}|'
        arrow += f' {safe_id(e["target"])}'
        lines.append(f'  {arrow}')
        roles.append(edge_role(e))
    lines.append('')

    lines.append(CLASS_DEFS)
    lines.append('')

    by_kind = {}
    for n in nodes:
        kind = n.get('kind', 'process')
        if kind == 'terminal' and n['id'] in start_ids:
            kind = 'terminal_start'
        elif kind == 'terminal' and n['id'] in finish_ids:
            kind = 'terminal_finish'
        by_kind.setdefault(kind, []).append(n['id'])
    term_cls = {'terminal_start': 'termstart', 'terminal_finish': 'termend'}
    for kind, ids in by_kind.items():
        cls = term_cls.get(kind) or KIND_STYLE.get(kind, KIND_STYLE['process'])['cls']
        lines.append(f'class {",".join(safe_id(i) for i in ids)} {cls}')
    lines.append('')

    group_fill = {'evidence': GROUP_EVIDENCE_STYLE, 'rules': GROUP_RULES_STYLE}
    for g in groups:
        if g.get('title', '').strip():
            style = group_fill.get(g['id'], GROUP_EVIDENCE_STYLE)
        else:
            style = GROUP_PLAIN_STYLE
        lines.append(f'style {safe_id(g["id"])} {style}')
    lines.append('')

    for i, role in enumerate(roles):
        color = ROLE_COLOR[role]
        dash = ',stroke-dasharray:5 4' if role in ('아니오', '되돌아감', '참조') else ''
        lines.append(f'linkStyle {i} stroke:{color},stroke-width:2px{dash}')

    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(OUT_DEFAULT))
    ap.add_argument('--embed', action='store_true')
    args = ap.parse_args()

    data = json.loads(DATA.read_text())
    mermaid = build(data)
    out_path = Path(args.out)
    out_path.write_text(mermaid)
    print(f'생성됨: {out_path} ({len(mermaid)} bytes)')

    if args.embed:
        text = DOC.read_text()
        marker = '![한 건을 한 전문가가 처리할 때 79개 재료의 입력·결과·조건·다음 작업이 연결되는 구조](docs/images/expert-definition/solo-material-relations.png)'
        if marker not in text:
            raise SystemExit('삽입 지점(이미지 마크다운)을 문서에서 찾지 못함')
        start = text.index(marker) + len(marker)
        next_heading = text.index('\n### 2.', start)
        head, tail = text[:start], text[next_heading:]
        block = f'\n\n```mermaid\n{mermaid}```\n'
        DOC.write_text(head + block + tail)
        print(f'삽입됨(이전 블록 교체): {DOC}')


if __name__ == '__main__':
    main()
