#!/usr/bin/env python3
"""원문 표와 실제 SVG 표시 내용, 재료당 도형, 선 교차를 대조한다.
브라우저의 글꼴·곡선 렌더링 검사는 별도로 수행한다.
"""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
NS={'s':'http://www.w3.org/2000/svg'}
doc=(ROOT/'전문가 에이전트 정의.md').read_text()
part=doc.split('## 계통별 재료')[1].split('## 사용 구조')[0]
catalog={}
for line in part.splitlines():
    if line.startswith('| **') and '✅' in line:
        cols=[v.strip() for v in line.strip('|').split('|')]
        if len(cols)==6:catalog[re.search(r'\*\*(.*?)\*\*',cols[0]).group(1)]=cols[4].strip('*')
assert len(catalog)==79
usage=doc.split('## 사용 구조',1)[1]
assert len(re.findall(r'^### ',usage,re.M))==3
assert len(re.findall(r'!\[[^\n]*\]\(docs/images/expert-definition/usage-materials-[^\n)]*\.svg\)',usage))==3
results=[]
for mode in ('solo','orchestration','complex'):
    root=ET.parse(ROOT/f'docs/images/expert-definition/usage-materials-{mode}.svg').getroot()
    model=json.loads(root.find('s:metadata',NS).text)
    material_nodes=[n for n in model['nodes'].values() if n['material']]
    assert {n['material'] for n in material_nodes}==set(catalog)
    visible=set()
    for g in root.findall('.//s:g[@class="node"]',NS):
        mat=g.get('data-material')
        if not mat:continue
        bold=''.join(t.text or '' for t in g.findall('.//s:text[@font-weight="700"]',NS))
        assert bold==mat,(mode,g.get('id'),mat,bold)
        assert model['nodes'][g.get('id')]['type']==catalog[mat]
        visible.add(bold)
    assert visible==set(catalog)
    assert len([n for n in model['nodes'].values() if n['shape']=='terminal'])==2
    assert not root.findall('.//*[@transform]') # no horizontal-only scaling or text compensation
    edges=model['edges'];crossings=[];reverse_overlaps=[]
    for i,a in enumerate(edges):
        for j,b in enumerate(edges[:i]):
            for p,q in zip(a['points'],a['points'][1:]):
                for u,v in zip(b['points'],b['points'][1:]):
                    for axis in (0,1):
                        other=1-axis
                        if p[other]==q[other]==u[other]==v[other] and (q[axis]-p[axis])*(v[axis]-u[axis])<0:
                            overlap=min(max(p[axis],q[axis]),max(u[axis],v[axis]))-max(min(p[axis],q[axis]),min(u[axis],v[axis]))
                            if overlap>2:reverse_overlaps.append((j,i))
                    if p[0]==q[0] and u[1]==v[1]:x,y=p[0],u[1]
                    elif p[1]==q[1] and u[0]==v[0]:x,y=u[0],p[1]
                    else:continue
                    if all(min(a,b)-.1<=z<=max(a,b)+.1 for a,b,z in ((p[0],q[0],x),(p[1],q[1],y),(u[0],v[0],x),(u[1],v[1],y))):
                        if (x,y) not in map(tuple,(p,q,u,v)):crossings.append((j,i,x,y))
    assert not crossings,(mode,crossings)
    assert not reverse_overlaps,(mode,reverse_overlaps)
    results.append({'mode':mode,'visible_materials':len(visible),'one_material_per_material_shape':True,'nodes':len(model['nodes']),'proper_line_crossings':len(crossings),'opposite_direction_overlaps':len(reverse_overlaps),'dimensions':[model['width'],model['height']]})
print(json.dumps(results,ensure_ascii=False,indent=2))
