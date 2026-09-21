#!/usr/bin/env python3
"""Check scoped materials and the control graph independently, then rendered geometry."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, hashlib, html, importlib.util, itertools, json, re

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('geom',Path(__file__).with_name('사용-구조-검증.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)


def shape_overlap(rect,node):
    if not v.overlap(rect,node,2):return False
    if node.get('kind')!='decision':return True
    x,y,w,h=[rect[k] for k in ('x','y','w','h')]
    ps=[(x+2,y+2),(x+w-2,y+2),(x+w-2,y+h-2),(x+2,y+h-2)]
    if any(v.inside(p,node,0) for p in ps):return True
    if any(v.intersects_node(a,b,node) for a,b in zip(ps,ps[1:]+ps[:1])):return True
    return v.inside((node['x']+node['w']/2,node['y']+node['h']/2),rect,0)


def run(render):
    d=json.loads((ROOT/'docs/도식/단독-재료-사용구조.json').read_text())
    g=json.loads((render/'geometry.json').read_text())
    svg=(ROOT/'docs/images/expert-definition/solo-material-use.svg').read_text()
    prefix=(ROOT/'전문가 에이전트 정의.md').read_text().split('## 사용 구조',1)[0]
    assert hashlib.sha256(prefix.encode()).hexdigest()==d['source_prefix_sha256']=='c65318f94f7ff41325f47dd2a3a4feedf56f4fee59deb94a4518b1a389068c0a'
    assert hashlib.sha256(svg.encode()).hexdigest()==g['svg_sha256'],'Stale render'
    assert json.loads(html.unescape(re.search(r'<metadata id="material-use-model">(.*?)</metadata>',svg,re.S)[1]))==d
    canonical={}
    for line in prefix.split('## 계통별 재료',1)[1].splitlines():
        if line.startswith('| **') and '✅' in line:
            cells=[c.strip() for c in line.strip('|').split('|')]
            if len(cells)==6:canonical[re.search(r'\*\*(.*?)\*\*',cells[0])[1]]=cells[4].strip('*')
    ns,ms,gs,es=d['nodes'],d['materials'],d['groups'],d['edges']
    material_names=Counter(m['name'] for m in ms.values())+Counter(n['material'] for n in ns.values() if n.get('material'))
    assert set(material_names)==set(canonical)==set(d['catalog']) and len(canonical)==79
    assert Counter(html.unescape(x) for x in re.findall(r'data-material="([^"]+)"',svg))==material_names
    for m in ms.values():
        assert m['scope']=='ALL' or m['scope'] in ns
        assert m['usage']==canonical[m['name']] and m['note']
    # Support/reference cards cannot silently become untriggered processes.
    outgoing,incoming=defaultdict(list),defaultdict(list)
    for e in es:
        if e['kind'] not in ('apply','data'):
            assert e['source'] in ns and e['target'] in ns
            outgoing[e['source']].append(e);incoming[e['target']].append(e)
    for k,n in ns.items():
        if k=='start':assert len(outgoing[k])==1 and not incoming[k]
        elif n['kind'] in ('terminal','stop'):assert incoming[k] and not outgoing[k]
        elif n['kind']=='decision':assert incoming[k] and len(outgoing[k])>=2 and all(e['label'] for e in outgoing[k])
        else:assert incoming[k] and len(outgoing[k])==1,k
    def reachable(start,links,key):
        seen=set();pending=list(start)
        while pending:
            n=pending.pop()
            if n not in seen:seen.add(n);pending.extend(e[key] for e in links[n])
        return seen
    assert reachable(['start'],outgoing,'target')==set(ns),'Unreachable control node'
    terminals=[k for k,n in ns.items() if k!='start' and n['kind'] in ('terminal','stop')]
    assert reachable(terminals,incoming,'source')==set(ns),'No route to an end'
    has=lambda a,b,kind=None:any(e['source']==a and e['target']==b and (kind is None or e['kind']==kind) for e in es)
    paths={
        'normal':['start','intake','evidence','rules','plan','permit','work','verify','quality','delivery','received','learn','finish'],
        'rework':['quality','plan','permit','work','verify'],
        'approval':['permit','human','identity','human_valid','permit'],
        'invalid_approval':['human_valid','human_hold'],
        'unconfirmed':['quality','wait','wait_result','verify'],
        'still_waiting':['wait_result','wait','wait_result'],
        'wait_expired':['wait_result','wait_hold'],
        'receipt_correction':['received','plan','permit','work'],
        'receipt_wait':['received','receipt_wait','received'],
        'receipt_rejected':['received','receipt_stop'],
    }
    for k,path in paths.items():assert all(has(a,b) for a,b in zip(path,path[1:])),k
    for a,b in [('quality','plan'),('human_valid','permit'),('wait_result','verify'),('received','plan'),('receipt_wait','received')]:assert has(a,b,'return')
    assert ms['no_delegate']['kind']=='unused' and '미사용' in ms['no_delegate']['note']
    issues=[];objects=ns|ms|gs;shapes=ns|ms
    for i,e in enumerate(es):
        assert v.on_boundary(e['points'][0],objects[e['source']]),('source',i)
        assert v.on_boundary(e['points'][-1],objects[e['target']]),('target',i)
        for k,n in shapes.items():
            if k not in (e['source'],e['target']) and any(v.intersects_node(a,b,n) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-node',i,k])
    for (a,n),(b,m) in itertools.combinations(shapes.items(),2):
        if v.overlap(n,m,2):issues.append(['shape-overlap',a,b])
    for (i,e),(j,f) in itertools.combinations(enumerate(es),2):
        if any(v.crossing(a,b,c,z) for a,b in zip(e['points'],e['points'][1:]) for c,z in zip(f['points'],f['points'][1:])):issues.append(['edge-cross',i,j])
    assert {n['id'] for n in g['nodes']}==set(shapes)
    for item in g['nodes']:
        n=shapes[item['id']]
        for t in item['texts']:
            if n.get('kind')=='decision':
                corners=[(t['x']+2,t['y']+4),(t['x']+t['w']-2,t['y']+4),(t['x']+2,t['y']+t['h']-3),(t['x']+t['w']-2,t['y']+t['h']-3)]
                if not all(v.inside(c,n,0) for c in corners):issues.append(['text-diamond',item['id'],t['text']])
            elif t['x']<n['x']-1 or t['x']+t['w']>n['x']+n['w']+1 or t['y']<n['y']-1 or t['y']+t['h']>n['y']+n['h']+1:issues.append(['text-out',item['id'],t['text']])
    labels=g['labels']+g['annotations']
    for t in labels:
        lid=t.get('id',t.get('text'))
        if t['x']<0 or t['x']+t['w']>d['width'] or t['y']<0 or t['y']+t['h']>d['height']:issues.append(['text-outside-image',lid])
        for k,n in shapes.items():
            if shape_overlap(t,n):issues.append(['label-node',lid,k])
        for i,e in enumerate(es):
            if lid!=f'e{i}' and any(v.intersects_node(a,b,t) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-label',i,lid])
    for a,b in itertools.combinations(labels,2):
        if v.overlap(a,b,2):issues.append(['label-overlap',a.get('id',a.get('text')),b.get('id',b.get('text'))])
    return dict(materials=len(canonical),types=dict(Counter(canonical.values())),control_nodes=len(ns),
                all_control_nodes_reachable=True,all_control_paths_have_terminal_routes=True,
                checked_paths=paths,dimensions=[d['width'],d['height']],display_width=1100,
                geometry_issues=issues,source_prefix_sha256=d['source_prefix_sha256'],
                svg_sha256=g['svg_sha256'],browser=g['browser'],
                limitation='Checks cover canonical names, modeled paths and measured geometry; they do not certify universal human comprehension.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('render',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    result=run(a.render)
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['geometry_issues']))
