#!/usr/bin/env python3
"""Check canonical coverage, relationship integrity and measured SVG geometry.

This checks artifacts, not universal human comprehension. Functional containment
is checked separately from execution edges; it never implies execution order.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,html,itertools,json,math,re

ROOT=Path(__file__).resolve().parents[2]
MODES=('solo','orchestration','complex')

def overlap(a,b,pad=0):
    return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>pad

def inside(p,n,pad=2):
    x,y=p
    if n.get('kind')=='decision':
        return abs((x-n['x']-n['w']/2)/(n['w']/2))+abs((y-n['y']-n['h']/2)/(n['h']/2))<.97
    return n['x']+pad<x<n['x']+n['w']-pad and n['y']+pad<y<n['y']+n['h']-pad

def intersects_node(a,b,n):
    steps=max(1,math.ceil(math.dist(a,b)/3))
    return any(inside((a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps),n) for i in range(steps+1))

def crossing(a,b,c,d):
    dx,dy=b[0]-a[0],b[1]-a[1];ex,ey=d[0]-c[0],d[1]-c[1];det=dx*ey-dy*ex
    if abs(det)<.001:return False
    u=((c[0]-a[0])*ey-(c[1]-a[1])*ex)/det;v=((c[0]-a[0])*dy-(c[1]-a[1])*dx)/det
    return .001<u<.999 and .001<v<.999

def on_boundary(p,n,tol=.1):
    x,y=p
    if n.get('kind')=='decision':
        return abs(abs((x-n['x']-n['w']/2)/(n['w']/2))+abs((y-n['y']-n['h']/2)/(n['h']/2))-1)<.001
    return (n['x']-tol<=x<=n['x']+n['w']+tol and n['y']-tol<=y<=n['y']+n['h']+tol and min(abs(x-n['x']),abs(x-n['x']-n['w']),abs(y-n['y']),abs(y-n['y']-n['h']))<tol)

def run(geometry=None):
    doc=(ROOT/'전문가 에이전트 정의.md').read_text();prefix,usage=doc.split('## 사용 구조',1)
    names={};current=''
    for line in prefix.split('## 계통별 재료',1)[1].splitlines():
        if line.startswith('| **') and '✅' in line:
            cells=[c.strip() for c in line.strip('|').split('|')]
            if len(cells)==6:names[re.search(r'\*\*(.*?)\*\*',cells[0])[1]]=cells[4].strip('*')
    assert len(names)==79
    links=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',usage)
    assert links==[f'docs/images/expert-definition/usage-structure-{m}.svg' for m in MODES]
    blocks=re.findall(r'```mermaid\n(.*?)```',usage,re.S)
    assert len(blocks)==3
    assert blocks==[(ROOT/f'docs/도식/usage-structure-{m}.mmd').read_text() for m in MODES]
    model=json.loads((ROOT/'docs/도식/사용-구조-원본.json').read_text())
    assert set(model['catalog'])==set(names)
    results=[];trace={}
    for mode in MODES:
        d=model['diagrams'][mode];ns=d['nodes'];gs=d['groups'];es=d['edges'];objects=ns|{k:g for k,g in gs.items() if k!='TITLE'}
        sha=hashlib.sha256(prefix.encode()).hexdigest();assert d['source_prefix_sha256']==sha
        svg=(ROOT/f'docs/images/expert-definition/usage-structure-{mode}.svg').read_text()
        assert json.loads(html.unescape(re.search(r'<metadata id="usage-structure">(.*?)</metadata>',svg,re.S)[1]))==d
        assert set(n['name'] for n in ns.values() if n['material'])==set(names)
        assert Counter(re.findall(r'data-material="([^"]+)"',svg))==Counter(n['name'] for n in ns.values() if n['material'])
        outgoing=defaultdict(list);issues=[]
        for n in ns.values():
            if n['material']:
                assert n['usage']==names[n['name']] and n['note'] and n['owner'] and n['scope']
                assert n['canonical_condition']==model['catalog'][n['name']]['condition']
        for i,e in enumerate(es):
            assert e['source'] in objects and e['target'] in objects
            assert on_boundary(e['points'][0],objects[e['source']]),(mode,i,'start off boundary')
            assert on_boundary(e['points'][-1],objects[e['target']]),(mode,i,'arrow off boundary')
            if e['kind']!='apply':outgoing[e['source']].append(e)
            if e['kind'] in ('return','blocked'):assert e['label']
            for k,n in ns.items():
                if k not in (e['source'],e['target']) and any(intersects_node(a,b,n) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-node',i,k])
        for k,n in ns.items():
            if n['kind']=='decision':assert len(outgoing[k])>=2 and all(e['label'] for e in outgoing[k]),(mode,k,'decision branches')
            if n['kind'] in ('terminal','stop'):assert (k=='start' and len(outgoing[k])==1) or not outgoing[k]
            if n['kind'] not in ('decision','fork'):assert len(outgoing[k])<=1,(mode,k,'branch without decision')
        for (a,n),(b,m) in itertools.combinations(ns.items(),2):
            if overlap(n,m,2):issues.append(['node-overlap',a,b])
        for (i,e),(j,f) in itertools.combinations(enumerate(es),2):
            if any(crossing(a,b,c,q) for a,b in zip(e['points'],e['points'][1:]) for c,q in zip(f['points'],f['points'][1:])):issues.append(['edge-cross',i,j])
        # A single operation diagram includes input/output scopes. Check that
        # scopes and their members are connected without inventing execution.
        connected=defaultdict(set)
        for e in es:connected[e['source']].add(e['target']);connected[e['target']].add(e['source'])
        for k,n in ns.items():
            for group in n['containers']:connected[k].add(group);connected[group].add(k)
        todo=['start'];seen=set()
        while todo:
            k=todo.pop()
            if k not in seen:seen.add(k);todo.extend(connected[k]-seen)
        assert seen==set(objects),(mode,'disconnected',set(objects)-seen)
        has=lambda a,b:any(e['source']==a and e['target']==b for e in es)
        for a,b in [('permit','permission_stop'),('permit','human_0'),('human_1','human_valid'),('human_valid','safe'),('human_valid','human_stop'),('verdict','repair'),('verdict','pending'),('verdict','nextwork'),('wait_result','check_1'),('wait_result','hold'),('nextwork','handoff'),('handoff','permit'),('repair','permit'),('nextwork','delivery_0'),('received','receipt_wait'),('receipt_wait','received'),('received','check_1'),('received','hold'),('received','learn_0'),('learn_2','learn_env'),('learn_env','learn_test'),('learn_test','test_passed'),('test_passed','remember'),('test_passed','keep')]:assert has(a,b),(mode,a,b)
        if mode=='solo':assert '사용하지 않음' in ns['no_delegate']['note']
        else:
            assert ns['fork']['kind']=='fork' and '준비' in ns['ready']['note']
            if mode=='complex':
                assert all(k in gs for k in ['CASE0','CASE1'])
                assert all(ns[f'case{i}_0']['name']=='문제·목표·완료 조건' and ns[f'case_collect{i}']['name']=='나눠 맡기기' for i in range(2))
                assert '건 A 결과 → 건 B' in ns['handoff']['note'] and '공유 자원' in ns['handoff']['note']
        measured=None
        if geometry:
            measured=json.loads((geometry/f'{mode}-geometry.json').read_text())
            assert measured['svg_sha256']==hashlib.sha256(svg.encode()).hexdigest(),(mode,'stale render')
            assert {n['id'] for n in measured['nodes']}==set(ns)
            for n in measured['nodes']:
                box=ns[n['id']]
                for t in n['texts']:
                    if box['kind']=='decision':
                        corners=[(t['x']+2,t['y']+4),(t['x']+t['w']-2,t['y']+4),(t['x']+2,t['y']+t['h']-3),(t['x']+t['w']-2,t['y']+t['h']-3)]
                        if not all(inside(c,box,0) for c in corners):issues.append(['text-diamond',n['id'],t['text']])
                    elif t['x']<box['x']-1 or t['x']+t['w']>box['x']+box['w']+1 or t['y']<box['y']-1 or t['y']+t['h']>box['y']+box['h']+1:issues.append(['text-out',n['id'],t['text']])
            for label in measured['labels']:
                for k,n in ns.items():
                    if overlap(label,n,3):issues.append(['label-node',label['id'],k])
            for a,b in itertools.combinations(measured['labels'],2):
                if overlap(a,b,2):issues.append(['label-label',a['id'],b['id']])
            for t in measured['annotations']:
                for k,n in ns.items():
                    if overlap(t,n,3):issues.append(['annotation-node',t['text'],k])
                for i,e in enumerate(es):
                    if any(intersects_node(a,b,t) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-annotation',i,t['text']])
        assert not issues,(mode,issues)
        trace[mode]={name:{'canonical':model['catalog'][name],'uses':[{'id':k,'owner':n['owner'],'condition':n['note'],'scope':n['scope'],'containers':n['containers'],'connections':[e for e in es if k in (e['source'],e['target'])]} for k,n in ns.items() if n['material'] and n['name']==name]} for name in names}
        results.append({'scenario':mode,'materials':79,'types':dict(Counter(names.values())),'nodes':len(ns),'connections':len(es),'single_connected_operation_diagram':True,'prefix_sha256':sha,'svg_sha256':hashlib.sha256(svg.encode()).hexdigest(),'render_checked':bool(measured),'browser':measured['browser'] if measured else None,'geometry_issues':issues})
    return results,trace

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--geometry',type=Path);p.add_argument('--report',type=Path);p.add_argument('--trace',type=Path);args=p.parse_args()
    results,trace=run(args.geometry)
    if args.report:args.report.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    if args.trace:args.trace.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))
