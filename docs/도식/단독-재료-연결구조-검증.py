#!/usr/bin/env python3
"""Check canonical coverage, named relationships, specified routes and rendered geometry.

These checks do not certify universal comprehension. The rendered image also needs
visual inspection at the document's display width.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,html,importlib.util,itertools,json,math,re
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
    assert ns['unused']['kind']=='unused' and '쓰지 않습니다' in ns['unused']['body']
    assert not d['illustrations'] and g['illustration_count']==0
    assert set(d['system_styles'])=={'환경','지식','규칙','실무','검증','학습'}
    assert len(g['system_labels'])==sum(bool(n['material']) for n in ns.values())
    for k,n in ns.items():
        if n['material']:
            assert n['term']==cat[n['material']]['term']
            assert cat[n['material']]['system'] in d['system_mapping'][n['term']]
            assert any(t['id']==k and t['text'].startswith(n['term']) for t in g['system_labels'])
    execution_edges=[(i,e) for i,e in enumerate(es) if e['kind']!='reference']
    assert len(g['arrowheads'])==len(execution_edges)
    assert {a['id'] for a in g['arrowheads']}=={f'e{i}' for i,e in execution_edges}
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
      'direct_execution':['qualified','plan','progress','record','control','guard','allowed','tools','type0'],
      'live_request':['live_start','live','signal','case','context_initial','understand','intent'],
      'performance_criteria':['goal','measure0','checks_start','search','absent','trust'],
      'reference_lookup':['search','reference','absent','trust','version','memory','checks_join','context'],
      'mandatory_rules':['checks_start','original','law','law_constitution','law_statute','law_decree','law_ministry','law_higher','law_conflict','law_settle','law_clear','law_confirmed','priority','rule_conflict','rule_candidate','rule_resolved','rule_confirmed','checks_join','context'],
      'higher_law_priority':['law_higher','law_higher_apply','law_conflict'],
      'special_legal_rule':['law_conflict','law_special','law_special_apply','law_settle'],
      'new_law_conditions':['law_special','law_new','law_settle'],
      'legal_uncertainty':['law_clear','law_wait','law_reply','law','law_constitution'],
      'rule_precedence':['rule_conflict','rule_compare','rule_order','rule_apply','rule_candidate'],
      'rule_exception':['rule_order','rule_exception','rule_candidate','rule_resolved'],
      'unresolved_rule_conflict':['rule_resolved','rule_wait','rule_reply','priority','rule_conflict'],
      'risk_check':['model','risk','strategy'],
      'isolated_execution':['progress','isolation','control'],
      'counter_evidence':['identity','counter','verify'],
      'process_records':['quality','record_read','process_eval','outcome'],
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
      'tested_improvement':['improveneed','improve','testenv','capability','passed','memory2','finish'],
      'failed_improvement':['passed','improve','testenv','capability','passed'],
    }
    for name,route in routes.items():assert all(has(a,b) for a,b in zip(route,route[1:])),name
    assert incoming['unused'] and all(e['kind']=='reference' for e in incoming['unused'])
    assert not outgoing['unused']
    starts={k for k,n in ns.items() if n['kind']=='terminal' and not incoming[k]}
    terminals={k for k,n in ns.items() if n['kind'] in ('terminal','stop') and not outgoing[k]}
    references={k for k,n in ns.items() if n['kind']=='reference'}
    unused={k for k,n in ns.items() if n['kind']=='unused'}
    assert starts=={'start','watch','live_start'}
    assert terminals=={'finish','hold','unqualified'}
    for k,n in ns.items():
        if k in starts|references|unused:continue
        assert incoming[k],('missing input',k,n['title'])
        if k not in terminals:assert outgoing[k],('non-terminal dead end',k,n['title'])
    reachable=set(starts);pending=list(starts)
    while pending:
        for e in outgoing[pending.pop()]:
            if e['kind']=='reference':continue
            k=e['target']
            if k not in reachable:reachable.add(k);pending.append(k)
    assert set(ns)-references-unused<=reachable,('unreachable actions',set(ns)-references-unused-reachable)
    can_finish=set(terminals);pending=list(terminals)
    while pending:
        for e in incoming[pending.pop()]:
            if e['kind']=='reference':continue
            k=e['source']
            if k not in can_finish:can_finish.add(k);pending.append(k)
    assert reachable<=can_finish,('no terminal route',reachable-can_finish)
    for k in references:
        consumer=ns[k]['applies_to']
        assert consumer in reachable
        group=ns[k].get('reference_group')
        assert has(group or k,consumer),('unconnected reference',k,consumer)
    assert {ns[k]['material'] for k in unused}=={'나눠 맡기기'}
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
    # Check rendered geometry, not just the layout values stored in metadata.
    rendered={n['id']:n for n in g['nodes']}
    alignment_checks=[]
    def aligned(name,values):
        delta=max(values)-min(values)
        alignment_checks.append(dict(check=name,max_difference_px=round(delta,6)))
        assert delta<.03,('alignment',name,values)
    def cy(k):
        s=rendered[k]['shape'];return s['y']+s['h']/2
    def cx(k):
        s=rendered[k]['shape'];return s['x']+s['w']/2
    material_rows=[
        ['signal','live'],['search','original'],
        ['ethics','principles'],['contract','platform'],['strategy','risk'],
        ['plan','state'],['progress','isolation','record'],['control','monitor'],
        ['verify','counter','identity'],
        ['quality','record_read'],['pack','process_eval'],['improve','testenv'],
    ]
    center_rows=[
        ['watchtype','signal','live'],['clear','communicate0'],['qualified','testenv0'],
        ['allowed','hold','handoff'],['vdecision','wait'],['more','context2'],
        ['qualityok','repair'],['receipt','wait2','delivery_repair'],
        ['learnneed','memory_direct'],['improveneed','memory_reuse'],['capability','passed'],
    ]
    for row in center_rows:aligned('row centers: '+','.join(row),[cy(k) for k in row])
    for column in [
        ['watch','watchtype','early','change','communicate0'],
        ['risk','testenv0','capability0','qualified_test','unqualified','isolation','rights','limit','hold','counter','context2','repair','delivery_repair','testenv'],
        ['state','record','monitor','handoff','identity0','identity','wait','record_read','process_eval','wait2','memory_direct','memory_reuse','passed'],
    ]:aligned('column centers: '+column[0],[cx(k) for k in column])
    def edge_between(a,b):return next(e for e in es if e['source']==a and e['target']==b)
    evidence_options=['now','case_ref','reference','reuse']
    for coord in ['x','w','h']:
        aligned('evidence card '+coord,[rendered[k]['shape'][coord] for k in evidence_options])
    aligned('evidence card gaps',[32,*[ns[b]['y']-ns[a]['y']-ns[a]['h'] for a,b in zip(evidence_options,evidence_options[1:])]])
    for k in evidence_options:
        inlet=edge_between('search',k);outlet=edge_between(k,'absent')
        assert inlet['label_node']==k and ns[k]['condition']
        assert any(t['role']=='node-condition' and t['text']==ns[k]['condition'] for t in rendered[k]['texts'])
        assert inlet['source_port']==inlet['target_port']=='l'
        assert outlet['source_port']=='r' and outlet['target_port']=='t'
        assert all(p[0]==120 for p in inlet['points'][1:-1])
        assert all(p[0]==840 for p in outlet['points'][1:3])
        assert outlet['points'][-2][0]==cx('absent')
        assert all(e['target']=='absent' for e in outgoing[k]),('optional cards became sequential',k)
        for role in ['system-label','node-title','node-body']:
            t=next(t for t in rendered[k]['texts'] if t['role']==role)
            aligned(k+' '+role+' left inset',[16,t['x']-ns[k]['x']])
    assert not ns['absent'].get('condition') and not edge_between('search','absent').get('label_node')
    assert {e['source'] for e in incoming['absent']}=={'search',*evidence_options}
    assert {e['source'] for e in incoming['trust']}=={'absent'},'result interpretation can be skipped'
    assert {e['target'] for e in outgoing['absent']}=={'trust'}
    common_check=edge_between('absent','trust')
    assert len(common_check['points'])==2 and common_check['source_port']=='b' and common_check['target_port']=='t'
    aligned('common evidence checks centerline',[cx('absent'),cx('trust'),cx('version')])
    aligned('common evidence checks gap',[32,ns['trust']['y']-ns['absent']['y']-ns['absent']['h']])
    assert ns['absent']['y']>=ns['reuse']['y']+ns['reuse']['h']+64
    context_sources=['knowledge','experience','memory']
    for coord in ['x','w','h']:
        aligned('context input card '+coord,[rendered[k]['shape'][coord] for k in context_sources])
    for coord in ['x','w']:
        aligned('evidence section '+coord,[rendered[k]['shape'][coord] for k in ['trust','version',*context_sources]])
    aligned('context input card gaps',[32,*[ns[b]['y']-ns[a]['y']-ns[a]['h'] for a,b in zip(context_sources,context_sources[1:])]])
    merge_y=[]
    for k in context_sources:
        inlet=edge_between('version',k);outlet=edge_between(k,'checks_join')
        assert inlet['label_node']==k and ns[k]['condition']==inlet['label']
        assert any(t['role']=='node-condition' and t['text']==ns[k]['condition'] for t in rendered[k]['texts'])
        assert inlet['source_port']==inlet['target_port']=='l'
        assert outlet['source_port']=='r' and outlet['target_port']=='t'
        assert all(p[0]==120 for p in inlet['points'][1:-1])
        assert all(p[0]==840 for p in outlet['points'][1:3])
        merge_y.append(outlet['points'][-2][1])
        assert all(e['target']=='checks_join' for e in outgoing[k]),('context inputs became sequential',k)
        for role in ['system-label','node-title','node-body']:
            t=next(t for t in rendered[k]['texts'] if t['role']==role)
            aligned(k+' '+role+' left inset',[16,t['x']-ns[k]['x']])
    aligned('context input merge',merge_y)
    fork=ns['checks_start'];join=ns['checks_join']
    assert fork['control_role']=='all_required' and fork['execution_order']=='unspecified'
    assert set(fork['required_branches'])=={'search','original'}
    assert {e['target'] for e in outgoing['checks_start']}==set(fork['required_branches'])
    assert {e['target'] for e in outgoing['measure0']}=={'checks_start'}
    assert join['control_role']=='all_complete' and set(join['required_groups'])=={'evidence','rules'}
    assert join['completion_sources']=={'evidence':context_sources,'rules':['rule_confirmed']}
    assert {e['source'] for e in incoming['checks_join']}==set(context_sources)|{'rule_confirmed'}
    assert {e['target'] for e in outgoing['checks_join']}=={'context'}
    assert {e['source'] for e in incoming['context'] if e['kind']!='return'}=={'checks_join'},'preparation bypasses both-check completion'
    assert all(has(k,'checks_join') and not has(k,'context') for k in [*context_sources,'rule_confirmed'])
    assert len(edge_between('measure0','checks_start')['points'])==len(edge_between('checks_join','context')['points'])==2
    aligned('both-check completion rail',[*merge_y,edge_between('rule_confirmed','checks_join')['points'][1][1]])
    aligned('both-check centerline',[cx(k) for k in ['measure0','checks_start','checks_join','context']])
    assert ns['context_initial']['y']<ns['understand']['y']<ns['checks_start']['y']<ns['context']['y']
    assert ns['context_initial']['material']==ns['context']['material']==ns['context2']['material']=='현재 작업 정보'
    assert ns['context_initial']['condition']=='처음 구성' and ns['context']['condition']=='확인 결과 반영'
    assert {e['source'] for e in incoming['context_initial']}=={'case'}
    for k in ['law_higher','law_conflict','law_special','law_clear','rule_conflict','rule_order','rule_resolved']:
        assert ns[k]['kind']=='decision'
        assert {e['label'] for e in outgoing[k]}=={'예','아니오'}
    for wait,reply,recheck in [('law_wait','law_reply','law'),('rule_wait','rule_reply','priority')]:
        assert {e['target'] for e in outgoing[wait]}=={reply}
        assert {e['target'] for e in outgoing[reply]}=={recheck}
        assert edge_between(reply,recheck)['kind']=='return'
    assert not has('law','priority') and not has('priority','checks_join')
    guard_references=['rights','limit']
    for coord in ['x','w','h']:
        aligned('guard reference card '+coord,[rendered[k]['shape'][coord] for k in guard_references])
    aligned('guard reference card gap',[32,ns['limit']['y']-ns['rights']['y']-ns['rights']['h']])
    aligned('guard centered beside criteria',[cy('guard'),(cy('rights')+cy('limit'))/2])
    for k in guard_references:
        e=edge_between(k,'guard')
        assert e['kind']=='reference' and e['source_port']=='r' and e['target_port']=='l'
        assert all(p[0]==595 for p in e['points'][1:-1])
        assert e['label_in_body']==k
        for role in ['system-label','node-title','node-body']:
            t=next(t for t in rendered[k]['texts'] if t['role']==role)
            aligned(k+' '+role+' left inset',[16,t['x']-ns[k]['x']])
    aligned('guard execution centerline',[cx(k) for k in ['control','guard','allowed']])
    assert all(len(edge_between(a,b)['points'])==2 for a,b in [('control','guard'),('guard','allowed')])
    approval_return=edge_between('identity0','guard')
    assert approval_return['source_port']==approval_return['target_port']=='r'
    assert len(approval_return['points'])==4 and all(p[0]==1735 for p in approval_return['points'][1:-1])
    hidden_labels={f'e{i}' for i,e in enumerate(es) if e.get('label_node') or e.get('label_in_body')}
    assert hidden_labels.isdisjoint(t['id'] for t in g['labels'])
    for fi in range(6):
        choose=f'choose{fi}';out=f'out{fi}';type_node=f'type{fi}';panel=groups[f'opg{fi}']
        cards=sorted((e['target'] for e in outgoing[choose]),key=lambda k:ns[k]['x'])
        material_rows.append(cards)
        aligned(f'operation {fi} centerline',[cx(choose),cx(out),panel['x']+panel['w']/2,
            (ns[cards[0]]['x']+ns[cards[-1]]['x']+ns[cards[-1]]['w'])/2])
        aligned(f'operation {fi} decision centers',[cy(type_node),cy(choose)])
        assert len(edge_between(type_node,choose)['points'])==2,('bent horizontal connector',fi)
        aligned(f'operation {fi} card widths',[ns[k]['w'] for k in cards])
        aligned(f'operation {fi} card gaps',[22,*[ns[b]['x']-ns[a]['x']-ns[a]['w'] for a,b in zip(cards,cards[1:])]])
        aligned(f'operation {fi} panel side padding',[40,ns[cards[0]]['x']-panel['x'],
            panel['x']+panel['w']-ns[cards[-1]]['x']-ns[cards[-1]]['w']])
        aligned(f'operation {fi} panel end padding',[20,ns[choose]['y']-panel['y'],
            panel['y']+panel['h']-ns[out]['y']-ns[out]['h']])
        aligned(f'operation {fi} branch and merge gaps',[64,ns[cards[0]]['y']-ns[choose]['y']-ns[choose]['h'],
            ns[out]['y']-ns[cards[0]]['y']-ns[cards[0]]['h']])
        for direction in ['branch','merge']:
            rail_y=[]
            for k in cards:
                e=edge_between(choose,k) if direction=='branch' else edge_between(k,out)
                if len(e['points'])==2:continue
                assert len(e['points'])==4,('extra fan bend',fi,k,direction)
                rail_y.extend([e['points'][1][1],e['points'][2][1]])
            aligned(f'operation {fi} {direction} rail',rail_y)
    for row in material_rows:
        for coord in ['y','h']:aligned('card '+coord+': '+','.join(row),[rendered[k]['shape'][coord] for k in row])
        for role in ['system-label','node-title','node-body']:
            aligned(role+': '+','.join(row),[next(t['y'] for t in rendered[k]['texts'] if t['role']==role) for k in row])
    for k,n in ns.items():
        for coord in ['x','y','w','h']:aligned(k+' rendered '+coord,[n[coord],rendered[k]['shape'][coord]])
    for rank,ids in enumerate([['ethics','principles'],['contract','platform'],['org'],['user_rule'],['style']],1):
        t=next(a for a in g['annotations'] if a['text']==str(rank))
        aligned('priority number '+str(rank),[t['y']+t['h']/2,cy(ids[0])])
    for i,e in enumerate(es):
        for endpoint,which,neighbor in [(0,'source',1),(-1,'target',-2)]:
            n=endpoints[e[which]];x,y,w,h=(n[k] for k in ('x','y','w','h'))
            ports={'t':(x+w/2,y),'b':(x+w/2,y+h),'l':(x,y+h/2),'r':(x+w,y+h/2)}
            side=e[which+'_port'];point=e['points'][endpoint]
            assert math.dist(point,ports[side])<.01,('not midpoint',i,which)
            outward={'t':(0,-1),'b':(0,1),'l':(-1,0),'r':(1,0)}[side]
            q=e['points'][neighbor];delta=(q[0]-point[0],q[1]-point[1])
            assert delta[0]*outward[0]+delta[1]*outward[1]>0,('inward connector',i,which)
            assert abs(delta[0]*outward[1]-delta[1]*outward[0])<.01,('not perpendicular',i,which)
        if e['kind']!='reference':assert math.dist(e['arrow'][0],e['points'][-1])<.01,('arrow gap',i)
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
    for t in g['labels']:
        i=int(t['id'][1:]);e=es[i];x,y=e['at']
        dist=lambda p,a,b:__import__('math').dist(p,(a[0]+max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/max(.001,(b[0]-a[0])**2+(b[1]-a[1])**2)))*(b[0]-a[0]),a[1]+max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/max(.001,(b[0]-a[0])**2+(b[1]-a[1])**2)))*(b[1]-a[1])))
        if min(dist((x,y),a,b) for a,b in zip(e['points'],e['points'][1:]))>1:issues.append(['label-detached-from-own-edge',i])
        for arrow in g['arrowheads']:
            if v.overlap(t,arrow,0):issues.append(['label-hides-arrow',i,arrow['id']])
    return dict(materials=len(cat),usage_types=dict(Counter(c['usage'] for c in cat.values())),
        system_counts=dict(Counter(c['term'] for c in cat.values())),illustrations=g['illustration_count'],arrowheads=len(g['arrowheads']),
        center_ports_checked=2*len(es),arrowheads_touch_boundary=True,
        alignment_checks=len(alignment_checks),alignment_max_difference_px=max(c['max_difference_px'] for c in alignment_checks),
        material_coverage=coverage,checked_routes=routes,geometry_issues=issues,
        flow_audit=dict(starts=sorted(starts),terminals=sorted(terminals),
            reachable_actions=len(reachable),reference_inputs=sorted(references),
            used_materials=len(cat)-len(unused),intentionally_unused=['나눠 맡기기'],
            missing_materials=[],unreachable_actions=[],nonterminal_dead_ends=[],
            required_preparation=dict(branches=fork['required_branches'],execution_order=fork['execution_order'],
                completion_groups=join['required_groups'],completion_node='checks_join',bypass_to_context=False)),
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
