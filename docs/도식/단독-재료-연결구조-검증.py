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
    for k,scope in groups.items():
        if scope.get('material'):instances[scope['material']].append(k)
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
            assert n['system']==cat[n['material']]['system']
            assert any(t['id']==k and (t['text']==n['system'] or t['text'].startswith(n['system']+' · ')) for t in g['system_labels'])
    execution_edges=[(i,e) for i,e in enumerate(es) if e['kind']!='reference']
    assert len(g['arrowheads'])==len(execution_edges)
    assert {a['id'] for a in g['arrowheads']}=={f'e{i}' for i,e in execution_edges}
    incoming,outgoing=defaultdict(list),defaultdict(list)
    for e in es:
        assert e['source'] in ns|groups and e['target'] in ns|groups
        if e['target'] in groups: assert e['kind']=='reference'
        incoming[e['target']].append(e);outgoing[e['source']].append(e)
    coverage=[]
    for name,ids in instances.items():
        use=[]
        for k in ids:
            if k in groups:
                scope=groups[k]
                use.append(dict(instance=k,visible_text=scope['title'],inputs=[],outputs=[],
                                application=scope['scope_members'],unused=False))
                continue
            n=ns[k]
            use.append(dict(instance=k,visible_text=n['body'],
                inputs=[e['source'] for e in incoming[k]],outputs=[e['target'] for e in outgoing[k]],
                application=n.get('applies_to'),priority_rank=n.get('priority_rank'),unused=n['kind']=='unused'))
        assert any(u['inputs'] or u['outputs'] or u['application'] or u['unused'] for u in use),name
        coverage.append(dict(material=name,usage=cat[name]['usage'],source_condition=cat[name]['condition'],instances=use))
    issues=[]
    has=lambda a,b:any(e['source']==a and e['target']==b and e['kind']!='reference' for e in es)
    flow_in=defaultdict(set);flow_out=defaultdict(set)
    for _,e in execution_edges:
        flow_out[e['source']].add(e['target']);flow_in[e['target']].add(e['source'])
    actual_flow_out = flow_out
    def reachable(start, omitted=()):
        seen=set();pending=[start]
        while pending:
            k=pending.pop()
            if k in seen or k in omitted:continue
            seen.add(k);pending.extend(actual_flow_out[k]-seen)
        return seen
    actions={k for k,n in ns.items() if n['kind'] not in ('reference','unused')}
    starts={k for k in actions if not flow_in[k]}
    assert starts=={'start','watch','live_start','improve_start','effect_start','monitor_event'},starts
    assert all(ns[k]['kind']=='terminal' for k in starts)
    terminals={k for k in actions if not flow_out[k]}
    assert all(ns[k]['kind'] in ('terminal','stop') for k in terminals),terminals
    reached=set().union(*(reachable(k) for k in starts))
    assert not actions-reached,('unreachable',actions-reached)
    assert all(reachable(k)&terminals for k in actions),'action cannot reach a terminal'
    for k,n in ns.items():
        if n['kind']=='reference':
            group=n.get('reference_group')
            assert n.get('applies_to') or incoming[k] or outgoing[k],('detached reference',k)
            if group:
                assert group in groups
                box=groups[group]
                assert box['x']<=n['x'] and n['x']+n['w']<=box['x']+box['w']+.1
                assert box['y']<=n['y'] and n['y']+n['h']<=box['y']+box['h']+.1,('reference outside group',k)
            if n.get('applies_to'):assert n['applies_to'] in actions
    # Contract only newly drawn material calls when comparing the established
    # workflow. The real graph above still checks starts, stops and reachability.
    original={k for k,n in ns.items() if not n.get('usage_added')}
    logical_out=defaultdict(set)
    for start in original:
        pending=list(actual_flow_out[start]);seen=set()
        while pending:
            k=pending.pop()
            if k in seen:continue
            seen.add(k)
            if k in original:logical_out[start].add(k)
            else:pending.extend(actual_flow_out[k])
    flow_out=logical_out;flow_in=defaultdict(set)
    for a,targets in flow_out.items():
        for b in targets:flow_in[b].add(a)
    has=lambda a,b:b in flow_out[a]
    supports={'control','isolation','monitor','guard','record'}
    assert not {'foundation','support_conditions'} & set(groups)
    assert not any(k.startswith('global_') and k!='global_tools' for k in ns)
    assert all(n.get('applies_to')!='ALL_WORK' and not n.get('applies_to_group') for n in ns.values())
    assert all(ns[k]['kind'] not in ('reference','unused') for k in supports)
    assert all(incoming[k] and outgoing[k] for k in supports)
    assert flow_out['signal']=={'isolation'} and flow_out['isolation']=={'context_initial'}
    assert ns['signal']['y']<ns['isolation']['y']<ns['context_initial']['y']
    assert not flow_in['monitor_event'] and flow_out['monitor_event']=={'monitor'}
    assert flow_in['monitor']=={'monitor_event'},'monitoring is not a normal task checkpoint'
    assert flow_out['control']=={'risk_exec'}
    roles={k:ns[k]['support_role'] for k in supports}
    for k,role in roles.items():
        assert k==role['local_node']
        assert role['target'] and role['period'] and role['actions'] and (ns[k]['used_by'] or incoming[k])
    assert roles['monitor']['actions']=={'fault_detected':'장애 복구'}
    assert roles['guard']['maintain_when'] is None and roles['record']['maintain_when'] is None
    # Concrete counterexamples to the rejected "all five run in every step"
    # interpretation. Availability, maintained state and new actions are separate.
    conditions=['active_job','allocated_workspace','running_system']
    scenarios={
        'unchanged_wait':(conditions,[],{'control','isolation','monitor'},set()),
        'system_without_job':(['running_system'],[],{'monitor'},set()),
        'workspace_not_created':(['active_job','running_system'],[],{'control','monitor'},set()),
        'fault_during_wait':(conditions,['fault_detected'],{'control','isolation','monitor'},{'monitor'}),
        'receive_information':(conditions,['info_receive'],{'control','isolation','monitor'},{'guard'}),
        'decision_record':(conditions,['decision_finished'],{'control','isolation','monitor'},{'record'}),
        'permission_changed':(conditions,['limits_changed'],{'control','isolation','monitor'},{'guard'}),
        'resume_work':(conditions,['resume_requested'],{'control','isolation','monitor'},{'control','guard'}),
        'execution_result':(conditions,['execution_completed'],{'control','isolation','monitor'},{'control','record'}),
    }
    activation_checks={}
    for name,(state,events,expected_maintained,expected_actions) in scenarios.items():
        maintained={k for k,r in roles.items() if r['maintain_when'] in state}
        triggered={k for k,r in roles.items() if set(r['actions'])&set(events)}
        assert maintained==expected_maintained and triggered==expected_actions,(name,maintained,triggered)
        activation_checks[name]=dict(maintained=sorted(maintained),triggered=sorted(triggered),events=events)
    assert 'foundation_scope' not in ns
    assert cat['업무 도구·시스템']['usage']=='단계별' and cat['실시간 대화']['usage']=='조건부'
    assert groups['global_tools']['scope_members']==['search']
    assert groups['model']['material']=='AI 모델' and groups['model']['scope_members']==['understand','intent']
    assert ns['live']['kind']=='process' and not ns['live'].get('applies_to')
    support_sources={'model','global_tools','live','isolation'}
    assert not any(n['kind']=='reference' and n.get('usage_source') in support_sources for n in ns.values())
    assert not {'model','global_tools'} & set(ns)
    assert not any(e['source'] in {'model','global_tools'} or e['target'] in {'model','global_tools'} for e in es)
    definitions=ns|groups
    dependency_count=0
    assert not any(n.get('usage_lines') for n in ns.values())
    assert not any(t['role']=='material-use' for n in g['nodes'] for t in n['texts'])
    for k,n in ns.items():
        for use in n.get('material_uses',[]):
            assert use['source'] in definitions and definitions[use['source']]['material']==use['material']
            assert use['condition'] and k in definitions[use['source']]['used_by']
            if use.get('visual_group'):
                scope=groups[use['visual_group']]
                assert scope['support_scope'] and use['source'] in scope['scope_sources'] and k in scope['scope_members']
                dependency_count+=1
                continue
            shown=use['visual_node'];assert shown in ns
            assert ns[shown].get('usage_source')==use['source'] or shown in {use['source'],'delivery_guard','improve_allowed'}
            if ns[shown]['kind']=='reference':
                assert any(e['source']==shown and e['target']==k and e['kind']=='reference' for e in es)
            elif shown.startswith('use_'):
                assert incoming[shown] and outgoing[shown]
            dependency_count+=1
    for group in groups.values():
        assert not group.get('usage_caption') and not group.get('usage_caption_extra')
        for use in group.get('material_uses',[]):
            assert definitions[use['source']]['material']==use['material']
            assert group['id'] in definitions[use['source']]['used_in_groups']
            if use.get('visual_group'):
                scope=groups[use['visual_group']]
                if scope.get('support_scope'):
                    assert use['source'] in scope['scope_sources']
                    assert set(scope['scope_members'])=={e['target'] for e in es if e['source']=='choose'+group['id'][-1]}
                else:
                    assert use['source']=='isolation' and scope['usage_material']==use['material']
                    assert scope['title']==scope['operation_family']+' · 작업 공간'
            else:
                shown=use['visual_node'];assert shown in ns
                if ns[shown]['kind']=='reference':
                    assert ns[shown]['usage_source']==use['source']
                    assert any(e['source']==shown and e['target'] in groups and e['kind']=='reference' for e in es)
            dependency_count+=1
    assert set(groups['model']['used_in_groups'])=={'opg0','opg1','opg2','opg3'}
    rendered_scopes={scope['id']:scope for scope in g['scopes']}
    for scope in groups.values():
        if not scope.get('support_scope'):continue
        assert all(abs(scope[q]-rendered_scopes[scope['id']][q])<.25 for q in ['x','y','w','h'])
        contained={k for k,n in ns.items() if scope['x']<=n['x'] and n['x']+n['w']<=scope['x']+scope['w']
                   and scope['y']<=n['y'] and n['y']+n['h']<=scope['y']+scope['h']}
        assert contained==set(scope['scope_members']),('incorrect support enclosure',scope['id'],contained)
        overlapping={k for k,n in ns.items() if min(n['x']+n['w'],scope['x']+scope['w'])>max(n['x'],scope['x'])
                     and min(n['y']+n['h'],scope['y']+scope['h'])>max(n['y'],scope['y'])}
        assert overlapping==contained,('partial support enclosure',scope['id'],overlapping-contained)
    assert set(groups['global_tools']['used_in_groups'])=={'opg0','opg1','opg2','opg4','opg5'}
    assert set(ns['live']['used_in_groups'])=={'opg3'}
    assert groups['support_testenv0']['scope_members']==['testenv0','capability0']
    assert groups['isolated_improvement']['scope_members']==['testenv','improve','capability']
    for owner in ['capability0','testenv','improve','capability']:
        use=next(u for u in ns[owner]['material_uses'] if u['source']=='isolation')
        assert owner in groups[use['visual_group']]['scope_members']
    for event,registration in [('improve_start','improve_queue'),('effect_start','effect_registered')]:
        assert ns[event]['registered_by']==registration
        assert any(e['source']==registration and e['target']==event and e['kind']=='reference' for e in es)
    routes={
        'new_request':['start','signal','isolation','context_initial','understand','intent','clear','case','goal','measure0','checks_start'],
        'new_live_request':['live_start','live','signal'],
        'discovered_work':['watch','watchtype','early','signal'],
        'changed_work':['watch','watchtype','change','signal'],
        'clarification':['clear','communicate0','intent'],
        'evidence':['search','absent','version','trust','evidence_usable','evidence_use','evidence_done','checks_join'],
        'missing_evidence':['evidence_usable','evidence_repair','evidence_hold'],
        'legal_applicability':['original','law','law_date','law_rank','law_higher','law_conflict','law_settle','law_clear','law_confirmed','priority'],
        'legal_priority':['law_higher','law_higher_apply','law_conflict','law_special','law_special_apply','law_settle'],
        'new_law':['law_special','law_new','law_settle'],
        'legal_wait':['law_clear','law_wait','law_reply','law'],
        'rule_conflict':['priority','rule_conflict','rule_compare','rule_order','rule_apply','rule_candidate','rule_resolved','rule_confirmed','checks_join'],
        'rule_exception':['rule_order','rule_exception','rule_candidate'],
        'rule_wait':['rule_resolved','rule_wait','rule_reply','priority'],
        'task_selection':['plan','state','progress','record','control','risk_exec','guard','allowed','precheck','precheck_ok','tools','dispatch'],
        'human_approval':['allowed','handoff','identity0','approval_valid','human_return','guard'],
        'human_completed':['human_return','identity','identity_ok','counter_needed','verify','process_step','process_check','state_result','vdecision'],
        'outage_detected':['monitor_event','monitor','recovery_ok','resume_changed'],
        'outage_changed':['monitor','recovery_ok','resume_changed','context_initial'],
        'outage_unchanged':['monitor','recovery_ok','resume_changed','state','progress'],
        'next_operation':['vdecision','more','context2','retry_scope','progress'],
        'new_evidence':['retry_scope','checks_start','original'],
        'new_scope':['retry_scope','communicate0','intent'],
        'verification_wait':['vdecision','wait_reason','wait','verification_event','identity'],
        'verification_impossible':['wait_reason','wait_expired'],
        'inspection_repair':['wait_reason','verify_help','verify'],
        'quality_repair':['qualityok','repair','context2'],
        'delivery':['more','pack','risk_delivery','delivery_risk_result','quality','qualityok','delivery_guard','delivery_allowed','delivery','receipt','record_read','process_eval','retrospective_result','outcome'],
        'delivery_modified':['delivery_allowed','delivery_approval','delivery_reply','repair'],
        'delivery_approved':['delivery_reply','delivery_guard'],
        'delivery_wait':['receipt','wait2','receipt_event','receipt'],
        'future_effect_registered':['outcome','effect_needed','effect_wait','effect_registered','learnneed'],
        'current_close':['learnneed','cause','improveneed','improve_queue','job_memory','finish'],
        'close_without_analysis':['learnneed','memory_direct','finish'],
        'close_without_improvement':['improveneed','memory_reuse','finish'],
        'scheduled_improvement':['improve_start','testenv','improve','capability','passed','improve_allowed','improve_apply','improvement_applied','memory2','improve_finish'],
        'failed_improvement':['passed','retry_improve','memory_unapplied','improve_finish'],
        'unapproved_improvement':['improve_allowed','memory_unapplied','improve_finish'],
        'scheduled_effect':['effect_start','effect_check','effect_measured','effect_action','effect_record','effect_end'],
    }
    for i in range(6):
        choose='choose'+str(i);out='out'+str(i)
        assert flow_out['dispatch']=={'choose'+str(j) for j in range(6)}
        assert ns[choose]['selection']=='one_operation_per_pass'
        for operation in flow_out[choose]:
            routes['operation_'+operation]=['dispatch',choose,operation,out,'identity']
    waits={'evidence_repair':'evidence_hold','law_wait':'law_timeout','rule_wait':'rule_timeout',
           'handoff':'handoff_timeout','verification_event':'wait_expired','delivery_approval':'delivery_timeout','receipt_event':'receipt_timeout',
           'identity_wait':'identity_timeout','counter_more':'counter_timeout'}
    for a,b in waits.items():routes['wait_can_end_'+a]=[a,b]
    routes.update({
        'risk_found':['risk','risk_result','risk_response','strategy','strategy_choice','strategy_feasible','qualified'],
        'risk_not_found':['risk_result','risk_scope','strategy'],
        'risk_missing_information':['strategy_choice','strategy_more','checks_start'],
        'no_allowed_method':['strategy_feasible','strategy_stop'],
        'identity_rejected':['identity_ok','identity_retry_allowed','identity_reject','identity_wait','identity'],
        'repeated_invalid_reply':['identity_wait','identity','identity_ok','identity_retry_allowed','identity_timeout'],
        'quality_unconfirmed':['qualityok','quality_unknown'],
        'counter_contradiction':['counter','counter_result','counter_compare','verify'],
        'counter_no_contradiction':['counter_result','verify'],
        'counter_inconclusive':['counter_result','counter_more','counter'],
        'procedure_correct':['process_step','process_check','state_result'],
        'procedure_violation':['process_check','process_repair','process_fixable','context2'],
        'procedure_cannot_correct':['process_fixable','process_hold'],
        'procedure_unknown':['process_check','process_unknown','wait_reason'],
        'delivery_risk_repair':['delivery_risk_result','delivery_risk_fix','context2'],
        'delivery_risk_unresolved':['delivery_risk_result','delivery_risk_hold'],
        'delivery_retry_bounded':['receipt','delivery_retry','delivery_guard'],
        'delivery_retry_stops':['delivery_retry','delivery_retry_hold'],
        'receipt_refused':['receipt','receipt_refused'],
        'effect_method_unknown':['effect_needed','effect_define','effect_wait'],
        'effect_registration_failed':['effect_registered','effect_registration_hold'],
        'clarification_unanswered':['communicate0','clarification_hold'],
        'recovery_failed':['recovery_ok','recovery_hold'],
        'effect_measure_missing':['effect_measured','effect_remeasure','effect_check'],
        'effect_measure_impossible':['effect_remeasure','effect_measure_hold'],
        'effect_action_needed':['effect_action','effect_issue','effect_record'],
        'retrospective_repair':['process_eval','retrospective_result','retrospective_repair','context2'],
        'retrospective_unconfirmed':['retrospective_result','retrospective_hold'],
        'improvement_failed':['improve_apply','improvement_applied','improvement_restore','improvement_restored','memory_unapplied'],
        'improvement_restore_failed':['improvement_restored','improvement_restore_hold'],
    })
    for i in range(6):
        key='choose'+str(i)
        branches=[e for e in es if e['source']==key]
        assert all(e['label'] for e in branches)
        assert len({e['label'] for e in branches})==len(branches)
        assert ns[key]['title']!='정해 둔 작업은?'
    for keys in [('progress','record','control'),('receipt','record_read','process_eval','retrospective_result','outcome')]:
        assert len({ns[k]['x']+ns[k]['w']/2 for k in keys})==1,('main path alignment',keys)
    for name,seq in routes.items():
        assert all(has(a,b) for a,b in zip(seq,seq[1:])),('route missing',name,seq)
    expected_outcomes={
        'risk_result':{'risk_response','risk_scope'},
        'strategy_choice':{'strategy_more','strategy_feasible'},
        'strategy_feasible':{'strategy_stop','qualified'},
        'identity_wait':{'identity','identity_timeout'},
        'identity_retry_allowed':{'identity_reject','identity_timeout'},
        'qualityok':{'repair','delivery_guard','quality_unknown'},
        'counter_result':{'counter_compare','counter_more','verify'},
        'process_check':{'state_result','process_repair','process_unknown'},
        'process_fixable':{'context2','process_hold'},
        'verification_event':{'identity','wait_expired'},
        'delivery_risk_result':{'quality','delivery_risk_fix','delivery_risk_hold'},
        'receipt':{'record_read','delivery_repair','wait2','delivery_retry','receipt_refused'},
        'receipt_event':{'receipt','receipt_timeout'},
        'effect_needed':{'effect_define','effect_wait','learnneed'},
        'effect_registered':{'learnneed','effect_registration_hold'},
        'retrospective_result':{'outcome','retrospective_repair','retrospective_hold'},
        'recovery_ok':{'resume_changed','recovery_hold'},
        'improvement_applied':{'memory2','improvement_restore'},
        'improvement_restored':{'memory_unapplied','improvement_restore_hold'},
        'effect_measured':{'effect_action','effect_remeasure'},
        'effect_action':{'effect_issue','effect_record'},
    }
    for decision,targets in expected_outcomes.items():
        assert flow_out[decision]==targets,('missing or accidental outcome',decision,flow_out[decision])
    required_checks=[
        ('signal','context_initial','isolation'),
        ('identity_ok','identity_reject','identity_retry_allowed'),
        ('risk','qualified','strategy_choice'),('risk','qualified','strategy_feasible'),
        ('verify','more','process_check'),('risk_delivery','delivery','delivery_risk_result'),
        ('monitor','progress','recovery_ok'),
        ('signal','case','understand'),('signal','case','intent'),('signal','case','clear'),
        ('signal','goal','case'),('communicate0','case','intent'),
        ('law','law_confirmed','law_date'),('original','priority','law_clear'),
        ('absent','evidence_usable','version'),('version','evidence_usable','trust'),
        ('identity','verify','identity_ok'),('identity','verify','counter_needed'),
        ('identity0','tools','approval_valid'),('progress','tools','guard'),
        ('progress','tools','risk_exec'),('progress','dispatch','precheck_ok'),
        ('more','delivery','pack'),('pack','delivery','qualityok'),('pack','delivery','risk_delivery'),
        ('pack','delivery','delivery_allowed'),('receipt','outcome','record_read'),
        ('improve_start','improve_apply','passed'),('improve_start','improve_apply','improve_allowed'),
        ('improve_start','improve','testenv'),
    ]
    for start,target,check in required_checks:
        assert target in reachable(start),(start,target)
        assert target not in reachable(start,{check}),('check bypass',start,target,check)
    # Newly exposed checks must actually gate the operation, not merely sit next
    # to it. A failed check ends in a hold and cannot enter the protected step.
    drawn_guards=[]
    for k,n in ns.items():
        if n.get('usage_source')!='guard' or n['kind']!='decisionwide':continue
        owner=n['usage_owner'];hold=k+'_hold'
        assert actual_flow_out[k]=={owner,hold},('guard outcomes',k)
        assert {e['source'] for e in incoming[owner] if e['kind']!='reference'}=={k},('drawn guard bypass',owner)
        assert ns[hold]['kind']=='stop' and owner not in reachable(hold)
        drawn_guards.append(k)
    assert len(drawn_guards)==8
    for owner in ['intent','goal','trust','priority','strategy','plan','process_step','quality','cause']:
        assert actual_flow_out[owner]=={'use_'+owner+'_record'}
    for event in ['effect_start','improve_start']:
        assert actual_flow_out[event]=={'use_'+event+'_control'}
    assert 'use_effect_start_control' not in reachable('effect_wait')
    assert 'use_improve_start_control' not in reachable('improve_queue')
    assert flow_out['human_return']=={'guard','identity','context_initial'}
    assert flow_out['delivery_reply']=={'repair','delivery_guard'}
    assert flow_out['resume_changed']=={'state','context_initial'}
    assert flow_out['retry_scope']=={'progress','checks_start','communicate0'}
    assert 'finish' in reachable('improveneed',{'improve','capability','improve_apply'})
    assert 'improve' not in reachable('start'),'registered future work incorrectly blocks current work'
    assert flow_out['checks_start']=={'search','original'}
    assert ns['checks_start']['control_role']=='all_required'
    assert ns['checks_start']['execution_order']=='unspecified'
    assert ns['checks_join']['control_role']=='all_complete'
    assert ns['checks_join']['completion_sources']=={'evidence':['evidence_done'],'rules':['rule_confirmed']}
    assert flow_in['checks_join']=={'evidence_done','rule_confirmed'}
    selection_cases=0
    for source,join in [('search','absent'),('evidence_use','evidence_done')]:
        options=set(ns[source]['selected_targets'])
        assert flow_out[source]==options|{join}
        assert all(flow_out[k]=={join} for k in options)
        assert ns[join]['control_role']=='all_selected_complete'
        assert ns[join]['selection_source']==source
        assert all(has(source,k) and has(k,join) for k in options)
        assert any(e['source']==source and e['target']==join and ''.join(e['label'].split())=='추가확인필요없음' for e in es)
        selection_cases+=1
    assert ns['context_initial']['y']<ns['understand']['y']<ns['intent']['y']<ns['case']['y']<ns['checks_start']['y']
    assert ns['version']['y']<ns['trust']['y']<ns['evidence_usable']['y']
    assert ns['evidence_done']['y']+ns['evidence_done']['h']<groups['rank']['y']
    assert flow_out['control']=={'risk_exec'}
    # Alignment is tested on repeated card rows and actual browser geometry.
    rendered={n['id']:n for n in g['nodes']};alignment=[]
    rows=[['ethics','principles'],['contract','platform']]
    rows += [sorted(flow_out['choose'+str(i)],key=lambda k:ns[k]['x']) for i in range(6)]
    for row in rows:
        for field in ['y','h']:
            values=[rendered[k]['shape'][field] for k in row]
            alignment.append(max(values)-min(values))
            assert max(values)-min(values)<.25,('row alignment',row,field,values)
        for role in ['node-title','node-body']:
            values=[next(t['y'] for t in rendered[k]['texts'] if t['role']==role) for k in row]
            alignment.append(max(values)-min(values))
            assert max(values)-min(values)<.25,('text alignment',row,role,values)
    for k,n in ns.items():
        assert all(abs(n[q]-rendered[k]['shape'][q])<.25 for q in ['x','y','w','h']),('render mismatch',k)
    bridge_pairs={frozenset((j['over_edge'],j['under_edge'])) for j in d['bridges']};crossing_pairs=set()
    assert len(d['bridges'])==len(g['bridges'])
    for j in d['bridges']:
        observed=min((b for b in g['bridges'] if b['over']=='e'+str(j['over_edge']) and b['under']=='e'+str(j['under_edge'])),key=lambda b:abs(b['x']-(j['x']-j['radius']))+abs(b['y']-(j['y']-j['radius'])))
        assert abs(observed['x']-(j['x']-j['radius']))<.25 and abs(observed['w']-2*j['radius'])<.25
        assert abs(observed['y']-(j['y']-j['radius']))<.25 and abs(observed['h']-j['radius'])<.25
    shapes={k:{**n,'kind':'decision' if n['kind']=='decisionwide' else n['kind']} for k,n in ns.items()}
    endpoints=shapes|{k:{**g,'kind':'process'} for k,g in groups.items()}
    for i,e in enumerate(es):
        if e['kind'] in ('flow','blocked'):
            if (e['source_port'],e['target_port'])!=('b','t'):issues.append(['forward-port-direction',i])
            if ns[e['source']]['y']+ns[e['source']]['h']>=ns[e['target']]['y']:issues.append(['forward-flow-not-downward',i])
        elif e['kind']=='return':
            if e['source_port'] not in ('l','r') or e['target_port'] not in ('l','r'):issues.append(['return-port-direction',i])
        for endpoint,which,neighbor in [(0,'source',1),(-1,'target',-2)]:
            n=endpoints[e[which]];x,y,w,h=(n[k] for k in ('x','y','w','h'))
            ports={'t':(x+w/2,y),'b':(x+w/2,y+h),'l':(x,y+h/2),'r':(x+w,y+h/2)}
            side=e[which+'_port'];point=e['points'][endpoint]
            assert math.dist(point,ports[side])<.01,('not midpoint',i,which)
            outward={'t':(0,-1),'b':(0,1),'l':(-1,0),'r':(1,0)}[side]
            q=e['points'][neighbor];delta=(q[0]-point[0],q[1]-point[1])
            if delta[0]*outward[0]+delta[1]*outward[1]<=0:issues.append(['inward connector',i,which])
            if abs(delta[0]*outward[1]-delta[1]*outward[0])>=.01:issues.append(['not perpendicular',i,which])
        if e['kind']!='reference':assert math.dist(e['arrow'][0],e['points'][-1])<.01,('arrow gap',i)
        assert v.on_boundary(e['points'][0],endpoints[e['source']]),('source-boundary',i)
        assert v.on_boundary(e['points'][-1],endpoints[e['target']]),('target-boundary',i)
        for k,n in shapes.items():
            if k not in (e['source'],e['target']) and any(v.intersects_node(a,b,n) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-node',i,e['source'],e['target'],k])
            if k not in (e['source'],e['target']) and n['kind']!='decision':
                padded={**n,'x':n['x']-3,'y':n['y']-3,'w':n['w']+6,'h':n['h']+6}
                if any(v.intersects_node(a,b,padded) for a,b in zip(e['points'],e['points'][1:])):issues.append(['edge-near-node-border',i,k])
    for (a,n),(b,m) in itertools.combinations(shapes.items(),2):
        if v.overlap(n,m,2):issues.append(['node-overlap',a,b])
    for (i,e),(j,f) in itertools.combinations(enumerate(es),2):
        related=(e['source']==f['source'] or e['target']==f['target']) and (e['kind']=='return')==(f['kind']=='return')
        if not related:
            for a,b in zip(e['points'],e['points'][1:]):
                for c,z in zip(f['points'],f['points'][1:]):
                    for axis in (0,1):
                        other=1-axis
                        if abs(a[axis]-b[axis])<.01 and abs(c[axis]-z[axis])<.01 and abs(a[axis]-c[axis])<.01:
                            shared=min(max(a[other],b[other]),max(c[other],z[other]))-max(min(a[other],b[other]),min(c[other],z[other]))
                            if shared>1:issues.append(['unrelated-edge-overlap',i,j,shared])
        if any(v.crossing(a,b,c,z) for a,b in zip(e['points'],e['points'][1:]) for c,z in zip(f['points'],f['points'][1:])):
            crossing_pairs.add(frozenset((i,j)))
            if frozenset((i,j)) not in bridge_pairs:issues.append(['unmarked-edge-cross',i,j,e['source'],f['source']])
    for n in g['nodes']:
        shape=shapes[n['id']]
        for a,b in itertools.combinations([t for t in n['texts'] if t['text']],2):
            if v.overlap(a,b,2):issues.append(['node-text-overlap',n['id'],a['text'],b['text']])
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
    for header in g.get('scope_headers',[]):
        scope=groups[header['scope']]
        assert all(abs(header[q]-scope[q])<.25 for q in ['x','y','w'])
        assert header['y']+header['h']<scope['y']+scope['h']
        for k,n in shapes.items():
            if helpers.shape_overlap(header,n):issues.append(['scope-header-node',header['scope'],k])
        for t in g['labels']:
            if v.overlap(header,t,0):issues.append(['scope-header-label',header['scope'],t['id']])
        for i,e in enumerate(es):
            if any(abs(a[1]-b[1])<.01 and v.intersects_node(a,b,header) for a,b in zip(e['points'],e['points'][1:])):issues.append(['scope-header-edge',header['scope'],i])
    for t in g['labels']:
        i=int(t['id'][1:]);e=es[i];x,y=e['at']
        dist=lambda p,a,b:__import__('math').dist(p,(a[0]+max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/max(.001,(b[0]-a[0])**2+(b[1]-a[1])**2)))*(b[0]-a[0]),a[1]+max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/max(.001,(b[0]-a[0])**2+(b[1]-a[1])**2)))*(b[1]-a[1])))
        if min(dist((x,y),a,b) for a,b in zip(e['points'],e['points'][1:]))>1:issues.append(['label-detached-from-own-edge',i])
        for arrow in g['arrowheads']:
            if v.overlap(t,arrow,0):issues.append(['label-hides-arrow',i,arrow['id']])
    assert crossing_pairs==bridge_pairs,('unmatched line jump',crossing_pairs,bridge_pairs)
    return_groups=defaultdict(list)
    for e in es:
        if e['kind']=='return':return_groups[e['target']].append(e)
    return_merges=[]
    for target,edges in return_groups.items():
        if len(edges)<2:continue
        assert len({e['target_port'] for e in edges})==1,('split return entry',target)
        assert len({tuple(e['points'][-2]) for e in edges})==1,('unmerged return trunk',target)
        return_merges.append(dict(target=target,sources=[e['source'] for e in edges]))
    straight_guards=['context_initial','search','original','communicate0','law_wait','rule_wait']
    for target in straight_guards:
        e=next(e for e in es if e['source']==f'use_{target}_guard' and e['target']==target)
        assert len(e['points'])==2,('unnecessary successful-branch detour',target)
    return dict(materials=len(cat),used_materials=78,intentionally_unused=['나눠 맡기기'],
        nodes=len(ns),edges=len(es),center_ports_checked=len(es)*2,
        forward_bottom_top_checked=sum(e['kind'] in ('flow','blocked') for e in es),
        return_side_to_side_checked=sum(e['kind']=='return' for e in es),
        edge_labels_checked=len(g['labels']),scope_headers_checked=len(g.get('scope_headers',[])),
        merged_return_groups=return_merges,straight_permission_paths_checked=len(straight_guards),
        checked_routes=routes,required_checks=required_checks,selection_cases=selection_cases,
        explicit_outcomes_checked={k:sorted(v) for k,v in expected_outcomes.items()},
        support_conditions_checked=len(supports),activation_checks=activation_checks,visible_use_relations_checked=dependency_count,
        starts=sorted(starts),terminals=sorted(terminals),unreachable_actions=[],nonterminal_dead_ends=[],
        material_coverage=coverage,alignment_checks=len(alignment),alignment_max_difference_px=max(alignment),
        marked_crossings=len(d['bridges']),geometry_issues=issues,
        support_scopes=[dict(id=s['id'],sources=s['scope_sources'],members=s['scope_members'])
                        for s in groups.values() if s.get('support_scope')],
        source_prefix_sha256=d['source_prefix_sha256'],svg_sha256=g['svg_sha256'],
        rendered_dimensions=[d['width'],d['height']],display_width=1100,
        limitation='도식에 표현된 관계와 경로, 렌더링을 검사했다. 현실의 모든 업무·법적 상황을 보증하는 검사는 아니다.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('render',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    result=run(a.render)
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('material_coverage','checked_routes','required_checks')},ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['geometry_issues']))
