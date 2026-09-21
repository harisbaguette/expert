#!/usr/bin/env python3
"""Check canonical coverage, named relationships, specified routes and rendered geometry.

These checks do not certify universal comprehension. The rendered image also needs
visual inspection at the document's display width.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,html,importlib.util,itertools,json,re
ROOT=Path(__file__).resolve().parents[2]
def load_module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load_module('geometry','사용-구조-검증.py')
helpers=load_module('shapes','단독-재료-사용구조-검증.py')
def run(folder):
    d=json.loads((ROOT/'docs/도식/단독-재료-연결구조.json').read_text())
    g=json.loads((folder/'geometry.json').read_text())
    svg=(ROOT/'docs/images/expert-definition/solo-material-relations.svg').read_text()
    prefix=(ROOT/'전문가 에이전트 정의.md').read_text().split('## 사용 구조',1)[0]
    assert hashlib.sha256(prefix.encode()).hexdigest()==d['source_prefix_sha256']=='c65318f94f7ff41325f47dd2a3a4feedf56f4fee59deb94a4518b1a389068c0a'
    assert hashlib.sha256(svg.encode()).hexdigest()==g['svg_sha256']
    assert json.loads(html.unescape(re.search(r'<metadata>(.*?)</metadata>',svg,re.S)[1]))==d
    ns=d['nodes'];es=d['edges'];cat=d['catalog'];groups={g['id']:g for g in d['groups']}
    instances=defaultdict(list)
    for k,n in ns.items():
        if n['material']:instances[n['material']].append(k)
    assert len(cat)==79 and set(instances)==set(cat)
    assert all(n['title']==n['material'] for n in ns.values() if n['material'])
    assert ns['unused']['kind']=='unused' and '쓰지 않음' in ns['unused']['body']
    incoming,outgoing=defaultdict(list),defaultdict(list)
    for e in es:
        assert e['source'] in ns|groups and e['target'] in ns
        incoming[e['target']].append(e);outgoing[e['source']].append(e)
    coverage=[]
    for name,ids in instances.items():
        use=[]
        for k in ids:
            n=ns[k]
            use.append(dict(instance=k,visible_text=n['body'],
                inputs=[e['source'] for e in incoming[k]],outputs=[e['target'] for e in outgoing[k]],
                application=n.get('applies_to'),priority_rank=n.get('priority_rank'),unused=n['kind']=='unused'))
        assert any(u['inputs'] or u['outputs'] or u['application'] or u['unused'] for u in use),name
        coverage.append(dict(material=name,usage=cat[name]['usage'],source_condition=cat[name]['condition'],instances=use))
    assert {ns[k]['priority_rank'] for k in ns if ns[k].get('priority_rank')}=={1,2,3,4,5}
    has=lambda a,b:any(e['source']==a and e['target']==b for e in es)
    routes={
      'clarification':['intent','clear','communicate0','intent'],
      'initial_capability_gate':['strategy','qualified','testenv0','capability0','qualified_test','plan'],
      'initial_capability_failure':['qualified_test','unqualified'],
      'direct_execution':['qualified','plan','progress','control','guard','allowed','tools','type0'],
      'data_preparation':['type0','choose0','combine','out0','identity','verify','state_result','vdecision'],
      'calculation_then_next_input':['type1','choose1','calc','out1','identity','verify','state_result','vdecision','more','context2','context'],
      'system_action':['type4','choose4','transaction','out4','identity','verify'],
      'observation':['type5','choose5','observe','out5','identity','verify'],
      'other_work':['type5','context2','context'],
      'rework':['vdecision','context2','context','model','strategy'],
      'pending':['vdecision','wait','verify'],
      'human_decision':['allowed','handoff','identity0','guard'],
      'blocked':['allowed','hold'],
      'quality_repair':['quality','qualityok','repair','context2'],
      'delivery':['more','quality','qualityok','pack','delivery','receipt','outcome'],
      'receipt_wait':['receipt','wait2','delivery'],
      'receipt_correction':['receipt','delivery_repair','repair','context2'],
      'no_analysis_needed':['outcome','learnneed','memory_direct','finish'],
      'no_change_needed':['learnneed','cause','improveneed','memory_reuse','finish'],
      'tested_improvement':['improveneed','improve','capability','passed','memory2','finish'],
      'failed_improvement':['passed','improve','capability','passed'],
    }
    for name,route in routes.items():assert all(has(a,b) for a,b in zip(route,route[1:])),name
    for i in range(6):
        n=ns['choose'+str(i)]
        assert n['kind']=='decisionwide' and len(outgoing[n['id']])>=2
        assert all(ns[e['target']]['material'] for e in outgoing[n['id']])
    for e in es:
        if e['kind']=='return':
            assert ns[e['target']]['y']<ns[e['source']]['y'],('not a real return',e)
    issues=[]
    shapes={k:{**n,'kind':'decision' if n['kind']=='decisionwide' else n['kind']} for k,n in ns.items()}
    endpoints=shapes|{k:{**g,'kind':'process'} for k,g in groups.items()}
    assert {n['id'] for n in g['nodes']}==set(ns)
    for i,e in enumerate(es):
        assert v.on_boundary(e['points'][0],endpoints[e['source']]),('source-boundary',i)
        assert v.on_boundary(e['points'][-1],endpoints[e['target']]),('target-boundary',i)
        for k,n in shapes.items():
            if k not in (e['source'],e['target']) and any(v.intersects_node(a,b,n) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-node',i,e['source'],e['target'],k])
    for (a,n),(b,m) in itertools.combinations(shapes.items(),2):
        if v.overlap(n,m,2):issues.append(['node-overlap',a,b])
    for (i,e),(j,f) in itertools.combinations(enumerate(es),2):
        if any(v.crossing(a,b,c,z) for a,b in zip(e['points'],e['points'][1:]) for c,z in zip(f['points'],f['points'][1:])):issues.append(['edge-cross',i,j,e['source'],f['source']])
    for n in g['nodes']:
        shape=shapes[n['id']]
        for t in n['texts']:
            if not t['text']:continue
            if shape['kind']=='decision':
                corners=[(t['x']+2,t['y']+4),(t['x']+t['w']-2,t['y']+4),(t['x']+2,t['y']+t['h']-3),(t['x']+t['w']-2,t['y']+t['h']-3)]
                if not all(v.inside(p,shape,0) for p in corners):issues.append(['diamond-text',n['id'],t['text']])
            elif t['x']<shape['x']-1 or t['x']+t['w']>shape['x']+shape['w']+1 or t['y']<shape['y']-1 or t['y']+t['h']>shape['y']+shape['h']+1:issues.append(['text-out',n['id'],t['text']])
    for t in g['labels']+g['annotations']:
        lid=t.get('id',t.get('text'))
        if t['x']<0 or t['y']<0 or t['x']+t['w']>d['width'] or t['y']+t['h']>d['height']:issues.append(['label-out',lid])
        for k,n in shapes.items():
            if helpers.shape_overlap(t,n):issues.append(['label-node',lid,k])
        for i,e in enumerate(es):
            if lid!=f'e{i}' and any(v.intersects_node(a,b,t) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-label',i,lid])
    for a,b in itertools.combinations(g['labels']+g['annotations'],2):
        if v.overlap(a,b,2):issues.append(['label-overlap',a.get('id',a.get('text')),b.get('id',b.get('text'))])
    return dict(materials=len(cat),usage_types=dict(Counter(c['usage'] for c in cat.values())),
        material_coverage=coverage,checked_routes=routes,geometry_issues=issues,
        source_prefix_sha256=d['source_prefix_sha256'],svg_sha256=g['svg_sha256'],
        rendered_dimensions=[d['width'],d['height']],display_width=1100,
        limitation='명칭·표현된 관계·선택한 경로·렌더링 좌표 검사이며, 모든 독자의 이해를 보증하지 않는다.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('render',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    result=run(a.render)
    result['limitation']='명칭·표현된 관계·선택한 경로·렌더링 좌표 검사이며, 모든 독자의 이해를 보증하지 않는다.'
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('material_coverage','checked_routes')},ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['geometry_issues']))
