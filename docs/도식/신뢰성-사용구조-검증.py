#!/usr/bin/env python3
"""원래 흐름의 경로 보존과 실제 렌더의 글자·도형 충돌을 검사한다."""
from pathlib import Path
import json
import math
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
DATA=json.loads((ROOT/'docs/도식/신뢰성-사용구조.json').read_text())
GEOM=json.loads((Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/judgment-reliability-review')/'geometry.json').read_text())
SOURCE=(ROOT/'docs/도식/judgment-reliability-usage.mmd').read_text()
nodes=DATA['nodes']
expected=set()
for line in SOURCE.splitlines():
    m=re.match(r'\s*(\w+)\s+(?:-->|--\s*".*?"\s*-->)\s*(\w+)\s*$',line)
    if m:expected.add(m.groups())
actual={(e['source'],nodes[e['target']].get('destination',e['target'])) for e in DATA['edges']}
missing=sorted(expected-actual)
extra=sorted(actual-expected)
issues=[]
if missing:issues.append(dict(kind='missing_edges',values=missing))
if extra:issues.append(dict(kind='extra_edges',values=extra))


def overlap(a,b,pad=1):
    return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>pad


for i,n in enumerate(GEOM['nodes']):
    if n['x']<0 or n['y']<0 or n['x']+n['w']>DATA['width'] or n['y']+n['h']>DATA['height']:
        issues.append(dict(kind='node_outside_canvas',id=n['id']))
    for t in n['texts']:
        if t['x']<n['x']+5 or t['x']+t['w']>n['x']+n['w']-5 or t['y']<n['y']+3 or t['y']+t['h']>n['y']+n['h']-3:
            issues.append(dict(kind='text_outside_node',id=n['id'],text=t['text']))
    for other in GEOM['nodes'][i+1:]:
        if overlap(n,other):issues.append(dict(kind='node_overlap',ids=[n['id'],other['id']]))
    for l in GEOM['labels']:
        # 마름모 바깥의 빈 모서리는 판독 영역이 아니다.
        if nodes[n['id']]['kind']=='decision':
            cx=n['x']+n['w']/2;cy=n['y']+n['h']/2
            corners=[(l['x'],l['y']),(l['x']+l['w'],l['y']),(l['x'],l['y']+l['h']),(l['x']+l['w'],l['y']+l['h'])]
            hit=any(abs(x-cx)/(n['w']/2)+abs(y-cy)/(n['h']/2)<.97 for x,y in corners)
        else:hit=overlap(n,l)
        if hit:issues.append(dict(kind='label_node_overlap',node=n['id'],edge=l['id']))
for i,l in enumerate(GEOM['labels']):
    for m in GEOM['labels'][i+1:]:
        if overlap(l,m):issues.append(dict(kind='labels_overlap',edges=[l['id'],m['id']]))


def inside(x,y,n):
    if n['kind']=='decision':
        return abs(x-n['x']-n['w']/2)/(n['w']/2)+abs(y-n['y']-n['h']/2)/(n['h']/2)<.96
    return n['x']+4<x<n['x']+n['w']-4 and n['y']+4<y<n['y']+n['h']-4


for i,e in enumerate(DATA['edges']):
    for key,n in nodes.items():
        if key in [e['source'],e['target']]:continue
        hit=False
        for a,b in zip(e['points'],e['points'][1:]):
            steps=max(1,int(math.dist(a,b)/5))
            if any(inside(a[0]+(b[0]-a[0])*t/steps,a[1]+(b[1]-a[1])*t/steps,n) for t in range(1,steps)):
                hit=True;break
        if hit:issues.append(dict(kind='edge_crosses_node',edge=i,node=key))
    for j,f in enumerate(DATA['edges'][i+1:],i+1):
        if e['source']==f['source'] or e['target']==f['target']:continue
        for a,b in zip(e['points'],e['points'][1:]):
            for c,d in zip(f['points'],f['points'][1:]):
                for fixed,other in [(0,1),(1,0)]:
                    if a[fixed]==b[fixed]==c[fixed]==d[fixed]:
                        length=min(max(a[other],b[other]),max(c[other],d[other]))-max(min(a[other],b[other]),min(c[other],d[other]))
                        if length>20:issues.append(dict(kind='unrelated_shared_line',edges=[i,j]))

if GEOM['arrows']!=len(DATA['edges']):issues.append(dict(kind='missing_arrows'))
numbers=set()
for n in nodes.values():
    numbers.update(int(x) for x in re.findall(r'(\d+)\s',n['tech']))
if numbers!=set(range(1,29)):issues.append(dict(kind='solution_coverage',missing=sorted(set(range(1,29))-numbers)))
report=dict(original_edges=len(expected),rendered_edges=len(actual),solutions=len(numbers),nodes=len(nodes),issues=issues)
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/judgment-reliability-review')/'verification.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(issues))
