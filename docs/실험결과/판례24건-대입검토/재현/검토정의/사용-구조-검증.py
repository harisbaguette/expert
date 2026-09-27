#!/usr/bin/env python3
"""정의 1 본문의 Mermaid 세 블록을 원문 재료 표와 대조한다.

문서의 Mermaid가 정본이며 외부 도형·이미지 파일에 의존하지 않는다.
문법·시각 검사는 Mermaid 렌더러에서 별도로 수행한다.
"""
from pathlib import Path
from html import unescape
from collections import Counter
import json,re
ROOT=Path(__file__).resolve().parents[2]
doc=(ROOT/'전문가 에이전트 정의.md').read_text()
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
    assert len([n for n in nodes.values() if n['shape']=='(['])==2
    assert 'stroke-dasharray:2 7' in source and '<small>' in source
    assert not re.search(r'<b>\s*\d+\s*재개',source)
    assert not re.search(r'왼쪽과 같은|오른쪽과 같은',source)

    # 이름 존재 여부와 별도로, 지원·선행 재료의 결과가 소비되는 경로를 확인한다.
    # blocked는 그 재료를 사용하지 않고도 결과에 도달하는 잘못된 우회 검사에 쓴다.
    def reaches(start, target, blocked=()):
        todo=[start];seen=set(blocked)
        while todo:
            key=todo.pop()
            if key in seen:continue
            if key==target:return True
            seen.add(key)
            todo.extend(b for a,b,kind,_ in edges if a==key and kind=='-->')
        return False

    def has_edge(a,b):
        return any(x==a and y==b and kind=='-->' for x,y,kind,_ in edges)

    assert reaches('start','finish'),(scenario,'시작에서 종료까지 실선 경로가 끊김')
    assert reaches('expert_entry','action_join'),(scenario,'전문가의 실제 재료 사용 경로가 끊김')
    assert reaches('action_20','action_11'),(scenario,'대화 통로를 사용하는 소통 누락')
    assert not reaches('action_20','action_join',{'action_11'}),(scenario,'대화 연결만으로 결과 처리')
    assert reaches('people_realtime','action_11',{'action_20'}),(scenario,'비실시간 소통 경로 누락')
    for consumer in ('action_18','action_19'):
        assert reaches('action_21',consumer),(scenario,'시험 환경의 사용처 누락',consumer)
        assert reaches('observe_env',consumer,{'action_21'}),(scenario,'별도 환경이 불필요한 경로 누락',consumer)
    assert not reaches('action_21','action_join',{'action_18','action_19'}),(scenario,'시험 준비만으로 결과 처리')
    assert reaches('action_18','action_17'),(scenario,'실험 결과 관측 누락')
    assert reaches('action_8','action_10'),(scenario,'설계를 제작에 전달하지 않음')
    assert not reaches('action_8','action_10',{'design_verify'}),(scenario,'미검증 설계의 제작 우회')
    assert reaches('action_8','result_MAKE',{'action_10'}),(scenario,'설계 자체가 납품물인 경우 누락')
    assert reaches('make_design','action_10',{'action_8'}),(scenario,'기존 설계를 쓰는 제작 경로 누락')
    assert reaches('action_9','action_10'),(scenario,'재구성한 내용을 제작에 전달하지 않음')
    for a,b in [('action_0','action_1'),('action_1','action_2'),('action_3','action_4'),('action_4','action_6'),('action_6','action_7')]:
        assert reaches(a,b,{'action_join'}),(scenario,'재료의 직접 조합 경로 누락',a,b)
    assert not reaches('source_join','enriched',{'source_check'}),(scenario,'추가 자료의 신뢰성 검사 누락')
    assert not reaches('source_join','enriched',{'source_version'}),(scenario,'추가 자료의 판본 검사 누락')
    rule_nodes={f'rule_{i}' for i in range(8)}|{'rule_rank1'}
    assert not any(a in rule_nodes and b in rule_nodes and kind=='-->' for a,b,kind,_ in edges),(scenario,'규칙 위계를 실행 순서로 표기')
    assert has_edge('more','safety'),(scenario,'다음 재료 사용 전 권한·한도 검사 누락')
    semantic_checks=['지원 재료의 사용처','선행 결과의 전달','불필요한 처리 생략','추가 근거 검증','규칙 위계와 실행 구분','다음 실행 재검사']
    if scenario!='단독':
        assert has_edge('follow','dispatch_state'),(scenario,'후속 작업을 전체 재배정으로 처리')
        assignment='dispatch2' if scenario=='오케스트레이션' else 'dispatch3'
        assert not reaches('follow',assignment,{'schedule'}),(scenario,'준비된 작업 선택 우회')
        assert not reaches('follow',assignment,{'dispatch_guard'}),(scenario,'위임 허용 검사 우회')
        a,b=('expert_entry','other_expert') if scenario=='오케스트레이션' else ('lead_a','lead_b')
        assert has_edge('assigned_to',a) and has_edge('assigned_to',b),(scenario,'한 담당만 실행하는 분기 누락')
        assert has_edge('parallel_ready',a) and has_edge('parallel_ready',b),(scenario,'준비된 두 담당의 병렬 분기 누락')
        assert not reaches('expert_entry','other_expert',{'collect','reassign','final_fix'}),(scenario,'A의 내부 실행이 B의 실행으로 혼합됨')
        assert has_edge('collect','result_save'),(scenario,'부분 실패 판단 전에 완료 결과를 보존하지 않음')
        semantic_checks+=['독립·병렬 실행','완료 결과 보존','후속 작업 준비·권한 확인']
    if scenario=='복합':
        assert has_edge('result_save','cross_change'),(scenario,'진행 중 변경 확인 누락')
        assert has_edge('impact_ok','invalidate') and has_edge('invalidate','dispatch_state'),(scenario,'변경으로 무효인 후속 결과의 재작업 누락')
        for suffix in ('a','b'):
            assert has_edge('team_next_'+suffix,'lead_'+suffix),(scenario,'팀 내부 후속 작업 연결 누락')
        semantic_checks+=['진행 중 건 사이 변경 확인','의존 결과의 사용 중단·재작업','팀 내부 후속 작업']
    results.append({'scenario':scenario,'format':'inline Mermaid','materials':len(set(materials.values())),'types':dict(Counter(catalog.values())),'one_material_per_material_node':True,'nodes':len(nodes),'decisions_with_labeled_branches':len(decisions),'edges_excluding_layout':sum(e[2]!='~~~' for e in edges),'semantic_path_checks':semantic_checks})
print(json.dumps(results,ensure_ascii=False,indent=2))
