#!/usr/bin/env python3
"""정의 1 본문의 Mermaid 세 블록을 원문 재료 표와 대조한다.

문서의 Mermaid가 정본이며 외부 도형·이미지 파일에 의존하지 않는다.
문법·시각 검사는 Mermaid 렌더러에서 별도로 수행한다.
"""
from pathlib import Path
from html import unescape
from collections import Counter
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]
doc=(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'전문가 에이전트 정의.md').read_text()
part=doc.split('## 계통별 재료')[1].split('## 사용 구조')[0]
catalog={}
for line in part.splitlines():
    if line.startswith('| **') and '✅' in line:
        cells=[v.strip() for v in line.strip('|').split('|')]
        if len(cells)==6:catalog[re.search(r'\*\*(.*?)\*\*',cells[0]).group(1)]=cells[4].strip('*')
assert len(catalog)==79
usage=doc.split('## 사용 구조',1)[1]
blocks=re.findall(r'```mermaid\n([\s\S]*?)\n```',usage)
assert len(blocks)==3
assert not re.search(r'usage-materials-.*\.svg|<svg|<img',usage)
results=[]
for scenario,source in zip(('단독','오케스트레이션','복합'),blocks):
    nodes={};edges=[];materials={};groups=set()
    for line in source.splitlines():
        if m:=re.match(r'\s*subgraph (\w+)\[',line):groups.add(m[1])
        if m:=re.match(r'\s*(\w+)([\[({]+)"(.*?)"[\])}]+:::(\w+)\s*$',line):
            key,shape,label,style=m.groups();assert key not in nodes
            nodes[key]={'shape':shape,'label':label,'style':style}
            titles=re.findall(r'<b>(.*?)</b>',label)
            names=[unescape(re.sub(r'<[^>]+>','',v)) for v in titles]
            if names and names[0] in catalog:
                assert len(names)==1,(scenario,key,names)
                name=names[0];materials[key]=name
                body=unescape(re.sub(r'<[^>]+>','',label.split('</b>',1)[1]))
                assert body.startswith(catalog[name]),(key,name,body)
        if m:=re.match(r'\s*(\w+)@\{ shape: fork \}',line):
            nodes[m[1]]={'shape':'fork','label':'병렬 시작','style':'fork'}
        if m:=re.match(r'\s*(\w+)\s+(?:\w+@)?(-->|-\.->|~~~)\s*(?:\|"(.*?)"\|\s*)?(\w+)\s*$',line):
            a,kind,label,b=m.groups();edges.append((a,b,kind,label))
    assert set(materials.values())==set(catalog),(scenario,sorted(set(catalog)-set(materials.values())))
    annotations=re.findall(r'%% 재료: (\w+) \| (.*?) \| (.*?)\n',source)
    assert {k:n for k,n,t in annotations}==materials
    for key,name,typ in annotations:assert catalog[name]==typ
    for a,b,kind,label in edges:assert a in nodes|dict.fromkeys(groups) and b in nodes|dict.fromkeys(groups),(a,b)
    decisions=[k for k,n in nodes.items() if n['shape']=='{']
    for key in decisions:
        branches=[e for e in edges if e[0]==key and e[2]!='~~~']
        assert len(branches)>=2,(scenario,'조건 분기 부족',key)
        assert all(e[3] for e in branches),(scenario,'분기 조건 없음',key)
    for key in materials:assert any(key in e[:2] for e in edges if e[2]!='~~~'),(scenario,'연결되지 않은 재료',key)
    terminals={k for k,n in nodes.items() if n['shape']=='(['}
    assert 'stroke-dasharray:2 7' in source and '<small>' in source
    assert not re.search(r'<b>\s*\d+\s*재개',source)
    assert not re.search(r'왼쪽과 같은|오른쪽과 같은',source)

    # 실행선은 판단 도형 또는 명시적 병렬 분기에서만 갈라진다.
    for key,n in nodes.items():
        outgoing=[e for e in edges if e[0]==key and e[2]=='-->']
        assert len(outgoing)<=1 or n['shape'] in ('{','fork'),(scenario,'처리 도형에서 설명 없이 갈라짐',key)
        assert n['shape']!='((',(scenario,'의미 없는 빈 연결점',key)
    def graph_walk(start,reverse=False):
        todo=[start];seen=set()
        while todo:
            key=todo.pop()
            if key in seen:continue
            seen.add(key)
            todo.extend((a if reverse else b) for a,b,kind,_ in edges if kind!='~~~' and (b if reverse else a)==key)
        return seen
    starts={k for k in nodes if not any(b==k and kind!='~~~' for a,b,kind,_ in edges)}
    endings={k for k in nodes if not any(a==k and kind!='~~~' for a,b,kind,_ in edges)}
    assert starts | endings == terminals,(scenario,'시작·종료 도형과 실제 입출구 불일치')
    assert starts=={'start','learn_start'}|{f'choose_{f}' for f in ('DATA','JUDGE','MAKE','PEOPLE','OPERATE','OBSERVE','ANSWER')}
    from_starts=set().union(*(graph_walk(k) for k in starts))
    to_endings=set().union(*(graph_walk(k,True) for k in endings))
    assert set(nodes)<=from_starts,(scenario,'시작과 분리된 요소',set(nodes)-from_starts)
    assert set(nodes)<=to_endings,(scenario,'종료에 도달하지 못하는 요소',set(nodes)-to_endings)
    assert not starts & endings,(scenario,'연결 없는 시작·종료')
    assert not any(kind=='-.->' for a,b,kind,label in edges),(scenario,'뜻이 불분명한 점선 화살표')
    palette={}
    for ids,style in re.findall(r'^\s*linkStyle ([\d,]+) (.*)$',source,re.M):
        for index in map(int,ids.split(',')):palette[index]=re.search(r'stroke:(#[0-9a-fA-F]+)',style)[1].lower()
    returns=set(re.findall(r'%% 복귀선: (\w+) --> (\w+)',source))
    for index,(a,b,kind,label) in enumerate(edges):
        if kind=='~~~':continue
        assert index in palette,(scenario,'선 색 누락',a,b)
        assert palette[index] in {'#60a5fa','#f87171','#facc15'},(scenario,'정의되지 않은 선 색',a,b)
        expected='#facc15' if (a,b) in returns else None
        if expected:assert palette[index]==expected,(scenario,'참조·복귀 색 불일치',a,b)
        elif (label or '').startswith('아니오') or (a,b) in {('extra_q','enriched'),('receipt_q','receipt_wait')}:
            assert palette[index]=='#f87171',(scenario,'아니오·불가 분기는 빨강',a,b)
        assert (palette[index]=='#facc15')==((a,b) in returns),(scenario,'노랑은 실제 복귀만',a,b)
    assert all(any(a==x and b==y and kind=='-->' for a,b,kind,label in edges) for x,y in returns)
    calls={'repeat_work':('expert_entry','action_join')}
    if scenario!='단독':calls['batch_repeat']=('dispatch_state','collect')
    if scenario=='복합':calls['team_repeat']=('lead_a','team_collect_a')
    for call,(entry,exit_node) in calls.items():
        assert nodes[call]['shape']=='[[',(scenario,'재사용 절차 도형 누락',call)
        assert f'%% 재사용 절차: {call} | 시작 {entry}' in source
        assert entry in nodes and exit_node in nodes

    # 이름 존재 여부와 별도로, 지원·선행 재료의 결과가 소비되는 경로를 확인한다.
    # blocked는 그 재료를 사용하지 않고도 결과에 도달하는 잘못된 우회 검사에 쓴다.
    # 상태를 모은 뒤 다시 분기하는 도형은 들어온 상태에 맞는 출구만 탄다.
    # 이 구분 없이 단순 연결만 탐색하면, '배정 금지'가 '배정 가능' 출구로
    # 나가는 등 실제 도식에 없는 우회를 잘못 검출하게 된다.
    hubs={'outcome_state':'next_route','batch_state':'batch_route','dispatch_status':'dispatch_route'}
    def incoming_state(hub,label):
        label=(label or '').replace('<br/>',' ')
        if hub=='dispatch_status':
            if '배정 가능' in label:return 'ready'
            if '답변·조건' in label:return 'recheck'
            if '기한 종료' in label:return 'retry'
            if any(x in label for x in ('금지','거절','취소')):return 'stop'
        else:
            if '계속할 수 없음' in label:return 'stop'
            if '전체 완료' in label or '담당 작업 완료' in label:return 'done'
            if any(x in label for x in ('계속','재계획','보완','다음 재료')):return 'continue'
        raise AssertionError((scenario,'합류 상태를 식별할 수 없음',hub,label))

    recipes={f'choose_{f}':f'done_{f}' for f in ('DATA','JUDGE','MAKE','PEOPLE','OPERATE','OBSERVE','ANSWER')}
    assert nodes['select']['shape']=='[['
    for entry,returned in recipes.items():
        assert f'%% 조건별 조합: select | 시작 {entry} | 결과 {returned} | 검증 verify0' in source
        assert returned in graph_walk(entry),(scenario,'조건별 조합의 결과 반환 누락',entry)
        assert not any(kind!='~~~' and a==returned for a,b,kind,label in edges)
    def reaches(start, target, blocked=()):
        todo=[(start,())];seen=set();blocked=set(blocked)
        while todo:
            key,state_items=todo.pop()
            if key in blocked or (key,state_items) in seen:continue
            if key==target:return True
            seen.add((key,state_items));state=dict(state_items)
            if key in calls:todo.append((calls[key][0],state_items))
            if key=='select':todo.extend((entry,state_items) for entry in recipes)
            if key in recipes.values():todo.append(('action_join',state_items))
            for a,b,kind,label in edges:
                if a!=key or kind!='-->':continue
                label=(label or '').replace('<br/>',' ')
                if key=='allowed' and state.get('execution')=='blocked' and b!='human_hold':continue
                if key in hubs.values() and key in state:
                    value=state[key]
                    if key=='dispatch_route':
                        expected=('ready' if label=='배정 가능' else 'recheck' if '다시 검사' in label
                                  else 'retry' if '재조정' in label else 'stop')
                        if value!=expected:continue
                    elif label.startswith('예')!=(value=='continue'):continue
                updated=state.copy()
                if key in ('rule_hold','ability_hold'):updated['execution']='blocked'
                if b in hubs:updated[hubs[b]]=incoming_state(b,label)
                todo.append((b,tuple(sorted(updated.items()))))
        return False

    def has_edge(a,b):
        return any(x==a and y==b and kind=='-->' for x,y,kind,_ in edges)

    assert reaches('start','delivery_finish'),(scenario,'작업의 시작·종료 경로가 끊김')
    assert reaches('learn_start','finish'),(scenario,'학습의 시작·종료 경로가 끊김')
    assert reaches('expert_entry','action_join'),(scenario,'전문가의 실제 재료 사용 경로가 끊김')
    assert reaches('action_20','action_11'),(scenario,'대화 통로를 사용하는 소통 누락')
    assert not reaches('action_20','done_PEOPLE',{'action_11'}),(scenario,'대화 연결만으로 결과 처리')
    assert reaches('people_realtime','action_11',{'action_20'}),(scenario,'비실시간 소통 경로 누락')
    for consumer in ('action_18','action_19'):
        assert reaches('action_21',consumer),(scenario,'시험 환경의 사용처 누락',consumer)
        assert reaches('observe_env',consumer,{'action_21'}),(scenario,'별도 환경이 불필요한 경로 누락',consumer)
    assert not reaches('action_21','done_OBSERVE',{'action_18','action_19'}),(scenario,'시험 준비만으로 결과 처리')
    assert reaches('action_18','action_17'),(scenario,'실험 결과 관측 누락')
    assert reaches('action_8','action_10'),(scenario,'설계를 제작에 전달하지 않음')
    assert not reaches('action_8','action_10',{'design_verify'}),(scenario,'미검증 설계의 제작 우회')
    assert reaches('action_8','done_MAKE',{'action_10'}),(scenario,'설계 자체가 납품물인 경우 누락')
    assert reaches('make_design','action_10',{'action_8'}),(scenario,'기존 설계를 쓰는 제작 경로 누락')
    assert reaches('action_9','action_10'),(scenario,'재구성한 내용을 제작에 전달하지 않음')
    for a,b in [('action_0','action_1'),('action_1','action_2'),('action_3','action_4'),('action_4','action_6'),('action_6','action_7')]:
        assert reaches(a,b,{'action_join'}),(scenario,'재료의 직접 조합 경로 누락',a,b)
    assert not reaches('source_0','enriched',{'source_check'}),(scenario,'추가 자료의 신뢰성 검사 누락')
    assert not reaches('source_0','enriched',{'source_version'}),(scenario,'추가 자료의 판본 검사 누락')
    assert '충돌하는 조항만 아래 위계로 조정' in source
    for a,b in [('rule_source','rule_0'),('rule_0','rule_first'),('rule_first','rule_1'),('rule_first','rule_2'),('rule_first_join','rule_second'),('rule_second','rule_3'),('rule_second','rule_4'),('rule_3','rule_5'),('rule_4','rule_5'),('rule_5','rule_6')]:
        assert has_edge(a,b),(scenario,'규칙 확인 위계 누락',a,b)
    assert '충돌하지 않는 하위 조건은 유지' in source
    for guard in ('authority','limit','safety'):
        assert reaches('more',guard),(scenario,'다음 재료 사용 전 재검사 경로 누락',guard)
        assert not reaches('more','select',{guard}),(scenario,'다음 재료의 권한·한도 검사 우회',guard)
    assert reaches('more','expert_output',{'fix','rule_hold','ability_hold','human_hold','unknown_hold'}),(scenario,'담당 작업 완료를 재실행·중단 없이 반환하지 못함')
    semantic_checks=['지원 재료의 사용처','선행 결과의 전달','불필요한 처리 생략','추가 근거 검증','규칙 확인 위계와 하위 조건 유지','다음 실행 재검사']
    if scenario!='단독':
        assert reaches('follow','dispatch_state'),(scenario,'후속 작업의 현재 상태 확인 누락')
        assignment='dispatch2' if scenario=='오케스트레이션' else 'dispatch3'
        assert not reaches('follow',assignment,{'schedule'}),(scenario,'준비된 작업 선택 우회')
        assert not reaches('follow',assignment,{'dispatch_guard'}),(scenario,'위임 허용 검사 우회')
        a,b=('route_a','other_expert') if scenario=='오케스트레이션' else ('lead_a','lead_b')
        assert has_edge('assigned_to','one_ready') and has_edge('one_ready','expert_entry'),(scenario,'준비된 한 담당의 실행 경로 누락')
        assert has_edge('parallel_ready',a) and has_edge('parallel_ready',b),(scenario,'준비된 두 담당의 병렬 분기 누락')
        assert not reaches('expert_entry','other_expert',{'collect','reassign','final_fix'}),(scenario,'A의 내부 실행이 B의 실행으로 혼합됨')
        assert has_edge('collect','result_save'),(scenario,'부분 실패 판단 전에 완료 결과를 보존하지 않음')
        semantic_checks+=['독립·병렬 실행','완료 결과 보존','후속 작업 준비·권한 확인']
    if scenario=='복합':
        assert has_edge('result_save','cross_change'),(scenario,'진행 중 변경 확인 누락')
        assert has_edge('impact_ok','invalidate') and reaches('invalidate','dispatch_state'),(scenario,'변경으로 무효인 후속 결과의 재작업 누락')
        assert has_edge('team_next_a','team_repeat') and has_edge('team_repeat','team_collect_a'),(scenario,'각 팀의 후속 작업과 회수 반복 누락')
        assert has_edge('lead_a','expert_entry') and reaches('lead_b','expert_entry'),(scenario,'건별 전문가의 독립 실행 진입 누락')
        semantic_checks+=['진행 중 건 사이 변경 확인','의존 결과의 사용 중단·재작업','팀 내부 후속 작업']
    results.append({'scenario':scenario,'format':'inline Mermaid','materials':len(set(materials.values())),'types':dict(Counter(catalog.values())),'one_material_per_material_node':True,'nodes':len(nodes),'decisions_with_labeled_branches':len(decisions),'edges_excluding_layout':sum(e[2]!='~~~' for e in edges),'starts':len(starts),'endings':len(endings),'independent_material_combinations':len(recipes),'semantic_path_checks':semantic_checks+['각 흐름의 시작·종료 연결','명시적인 조건·병렬 분기','복귀선·부정 분기 색','재사용 절차의 범위']})
print(json.dumps(results,ensure_ascii=False,indent=2))
