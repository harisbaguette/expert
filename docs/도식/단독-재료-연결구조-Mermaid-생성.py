#!/usr/bin/env python3
"""단독-재료-연결구조.json(정본, 노드 128·재료 79)을 네이티브 Mermaid 순서도로 바꾼다.

참조 이미지(solo-material-relations.png)와 같은 구획·같은 상하좌우 배치를 목표로 한다.
 - 구획(subgraph)은 JSON의 groups 사각형 안에 들어가는 노드로 기하학적으로 정한다.
 - 위아래 차례는 정본 좌표 (y, x) 순서를 선언 순서로 그대로 옮겨 ELK에 넘긴다.
 - 되돌아가는 선도 목적지 상자로 가는 진짜 화살표(A --> B)로 그린다. `A <-- B`는 쓰지 않는다
   (ELK가 렌더에서 통째로 빼 버린다 — 도식-설계.md).
 - 배치 머리글은 도식-설계.md의 「업무 처리 흐름」 순서도(113 노드)에서 검증된 값을 쓴다:
   layout elk + NETWORK_SIMPLEX + mergeEdges:false + keepEntryNodeOnTop:true, curve linear.
사용법: python3 단독-재료-연결구조-Mermaid-생성.py [--embed]
"""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/도식'
DOC = ROOT / '전문가 에이전트 정의.md'
SECTION = '### 1. 단독 상황 — 한 건 · 한 전문가'
IMAGE = ('![한 건을 한 전문가가 처리할 때 79개 재료의 입력·결과·조건·다음 작업이 연결되는 구조]'
         '(docs/images/expert-definition/solo-material-relations.png)')

# 참조 SVG(단독-재료-연결구조.py)의 색을 그대로 옮긴다.
INK, MUTED = '#192C36', '#526773'
BLUE, RED, YELLOW = '#228DE1', '#D95750', '#E3A512'
FILL = {'process': '#FFFFFF', 'material': '#E8F5FE', 'decision': '#FFF5C6',
        'terminal': '#E7F5E9', 'stop': '#FFF0EC', 'source': '#F6FAFC',
        'unused': '#F3F3F1', 'data': '#FFFFFF'}
RANK_BADGE = {1: '①', 2: '②', 3: '③', 4: '④', 5: '⑤'}

CONFIG = {
    'layout': 'elk',
    'theme': 'base',
    'flowchart': {'defaultRenderer': 'elk', 'htmlLabels': True, 'wrappingWidth': 380,
                  'curve': 'linear', 'nodeSpacing': 70, 'rankSpacing': 85,
                  'padding': 20, 'useMaxWidth': True},
    'themeVariables': {'fontFamily': 'Apple SD Gothic Neo, Noto Sans KR, sans-serif',
                       'fontSize': '16px', 'lineColor': BLUE,
                       'clusterBkg': 'transparent', 'clusterBorder': '#CADFE9'},
    'themeCSS': ('.marker{overflow:visible !important}'
                 '.arrowMarkerPath{stroke-width:5px !important;stroke-linejoin:round !important;'
                 'stroke-linecap:round !important;transform:translateX(-6px)}'
                 f'.nodeLabel b{{display:inline-block;font-size:17px;font-weight:700;color:{INK}}}'
                 f'.nodeLabel small{{display:inline-block;font-size:14px;line-height:1.45;'
                 f'word-break:keep-all;color:{MUTED}}}'
                 f'.nodeLabel .rank{{font-size:17px;font-weight:800;color:{BLUE}}}'
                 '.nodeLabel p{margin:0}'
                 '.edgeLabel{font-size:14px}'
                 f'.edgeLabel,.edgeLabel p,.edgeLabel span{{color:{INK} !important;'
                 'background:#FFFFFF !important}'
                 f'.cluster-label{{font-size:18px;font-weight:700;color:{INK}}}'
                 f'.cluster-label span{{color:{INK} !important}}'),
    'elk': {'nodePlacementStrategy': 'NETWORK_SIMPLEX', 'mergeEdges': False,
            'keepEntryNodeOnTop': True},
}

# 구획 제목 — 정본 groups의 title이 빈 것은 배치용 상자이므로 테두리 없이 둔다.
GROUP_TITLE = {'rank': '충돌하는 조항에만 아래 순위를 적용'}
# 참조 이미지에서 줄로 나란히 선 재료들 — 보이지 않는 선으로 줄 순서만 고정한다.
ROW_CHAINS = [['ethics', 'contract', 'org', 'user_rule', 'style'],
              ['principles', 'platform']]


def mid(key):
    """Mermaid 예약어(style·end·class 등)와 부딪히지 않게 노드·구획 이름에 머리를 붙인다."""
    return 'n_' + key


def q(text):
    return html.escape(text, quote=True).replace('\n', '<br/>')


def load():
    return json.loads((OUT / '단독-재료-연결구조.json').read_text())


def drawn(gid, groups):
    """그림에 남길 구획인지 — 제목이 있는 구획만 그린다.

    정본 groups 9개 중 opg0~opg5 는 순수 SVG 를 그릴 때 좌표를 잡으려고 둔 배치용 상자다.
    참조 이미지에서도 테두리·제목이 없다. Mermaid 에서 subgraph 로 남기면 ELK 가 구획마다
    층을 따로 잡아 폭이 8800px 까지 벌어지므로(실측) 그리지 않는다.
    """
    return bool(GROUP_TITLE.get(gid, groups[gid]['title']))


def membership(nodes, groups):
    """노드가 어느 구획 사각형 안에 들어가는지 기하학적으로 정한다(가장 작은 것 우선)."""
    def inside(n, g):
        return (g['x'] <= n['x'] and g['y'] <= n['y']
                and n['x'] + n['w'] <= g['x'] + g['w']
                and n['y'] + n['h'] <= g['y'] + g['h'])
    owner = {}
    for key, n in nodes.items():
        hits = [gid for gid, g in groups.items() if inside(n, g)]
        if hits:
            owner[key] = min(hits, key=lambda gid: groups[gid]['w'] * groups[gid]['h'])
    return owner


def nesting(groups):
    parent = {}
    for a, ga in groups.items():
        outer = [b for b, gb in groups.items()
                 if b != a and gb['x'] <= ga['x'] and gb['y'] <= ga['y']
                 and gb['x'] + gb['w'] >= ga['x'] + ga['w']
                 and gb['y'] + gb['h'] >= ga['y'] + ga['h']]
        parent[a] = min(outer, key=lambda b: groups[b]['w'] * groups[b]['h']) if outer else None
    return parent


def node_line(key, n, indent):
    label = ''
    if n.get('priority_rank'):
        label += "<span class='rank'>" + RANK_BADGE[n['priority_rank']] + '</span> '
    label += '<b>' + q(n['title']) + '</b>'
    if n['body']:
        label += '<br/><small>' + q(n['body']) + '</small>'
    kind = n['kind']
    cls = ('decision' if kind in ('decision', 'decisionwide')
           else 'material' if n['material'] and kind == 'process'
           else kind)
    open_, close = (('{"', '"}') if kind in ('decision', 'decisionwide')
                    else ('(["', '"])') if kind in ('terminal', 'stop')
                    else ('["', '"]'))
    return f'{" " * indent}{mid(key)}{open_}{label}{close}:::{cls}'


def export(d):
    nodes = d['nodes']
    groups = {g['id']: g for g in d['groups']}
    owner = {k: g for k, g in membership(nodes, groups).items() if drawn(g, groups)}
    parent = nesting(groups)
    order = sorted(nodes, key=lambda k: (nodes[k]['y'], nodes[k]['x']))

    lines = ['%%{init: ' + json.dumps(CONFIG, ensure_ascii=False) + ' }%%', 'flowchart TB',
             '  %% 파란 선은 흐름·전달, 빨간 선은 아니오·차단, 노란 선은 앞 단계로 되돌아감.',
             '  %% 점선 테두리는 배치 구획이며 실행 단계가 아니다. ~~~ 는 보이지 않는 줄 맞춤이다.']

    def emit_group(gid, indent=2):
        g = groups[gid]
        title = GROUP_TITLE.get(gid, g['title'])
        out = [f'{" " * indent}subgraph {mid(gid)}["{q(title) if title else " "}"]',
               f'{" " * (indent + 2)}direction TB']
        for key in order:
            if owner.get(key) == gid:
                out.append(node_line(key, nodes[key], indent + 2))
        for child in groups:
            if drawn(child, groups) and parent[child] == gid:
                out += emit_group(child, indent + 2)
        out.append(f'{" " * indent}end')
        return out

    for key in order:
        if key not in owner:
            lines.append(node_line(key, nodes[key], 2))
    for gid in groups:
        if drawn(gid, groups) and parent[gid] is None:
            lines += emit_group(gid)

    kinds = []
    for e in d['edges']:
        label = q(e['label'])
        arrow = '-->' + (f'|"{label}"|' if label else '')
        lines.append(f'  {mid(e["source"])} {arrow} {mid(e["target"])}')
        kinds.append(e['kind'])
    for chain in ROW_CHAINS:
        for a, b in zip(chain, chain[1:]):
            lines.append(f'  {mid(a)} ~~~ {mid(b)}')
            kinds.append('layout')

    for cls, fill in FILL.items():
        radius = ',rx:6px,ry:6px' if cls not in ('decision',) else ''
        lines.append(f'  classDef {cls} fill:{fill},stroke:{INK},stroke-width:1.6px,'
                     f'color:{INK}{radius}')
    for gid in groups:
        if drawn(gid, groups):
            lines.append(f'  style {mid(gid)} fill:none,stroke:#CADFE9,stroke-width:1.7px,'
                         f'stroke-dasharray:3 9,color:{INK}')
    for kind, color in (('flow', BLUE), ('blocked', RED), ('return', YELLOW)):
        ix = [str(i) for i, k in enumerate(kinds) if k == kind]
        if ix:
            lines.append(f'  linkStyle {",".join(ix)} stroke:{color},stroke-width:2.2px')
    return '\n'.join(lines) + '\n'


def embed(chart):
    text = DOC.read_text()
    head, rest = text.split(SECTION, 1)
    tail = rest.split('\n### ', 1)[1]
    body = f'{SECTION}\n\n{IMAGE}\n\n```mermaid\n{chart}```\n\n### {tail}'
    DOC.write_text(head + body)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--embed', action='store_true', help='정의 문서의 「1. 단독 상황」 절에 넣는다.')
    ap.add_argument('--out', type=Path, default=OUT / 'solo-material-relations.mmd')
    args = ap.parse_args()
    chart = export(load())
    args.out.write_text(chart)
    print(f'{args.out}: {chart.count(chr(10))} lines')
    if args.embed:
        embed(chart)
        print(f'{DOC}: embedded')


if __name__ == '__main__':
    main()
