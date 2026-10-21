#!/usr/bin/env python3
"""전문성 획득 계획의 요구·원본·ID·의존 관계를 읽기 전용으로 대조한다."""
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

root=Path(__file__).resolve().parents[2]
data=json.loads((root/'docs/전문성-획득/plan-data.json').read_text())
doc=(root/'docs/전문성-획득-계획.md').read_text()
errors=[]
def need(condition,message):
    if not condition: errors.append(message)
def index(key):
    rows=data[key]
    ids=[x['id'] for x in rows]
    need(len(ids)==len(set(ids)),key+': duplicate IDs')
    return {x['id']:x for x in rows}
cases=index('input_cases')
research=index('research_groups')
domains=index('priority_domains')
experts=index('experts')
tasks=index('tasks')
reqs=index('user_requirements')
need(len(cases)==18,'입력 경우 18개 불일치')
need(len(research)==8,'연구 묶음 8개 불일치')
need(len(domains)==18,'우선 분야 18개 불일치')
need(len(tasks)==65,'작업 65개 불일치')
need(len(reqs)==15,'사용자 요구 15개 불일치')
lines=(root/'전문가 에이전트 정의 1.md').read_text().splitlines()
source_roles=[]
active=False
for line in lines:
    if line.startswith('#### ') and any(x in line for x in ['위임형','고용형','운영형']): active=True
    if line.startswith('## 전문 AI 에이전트'): active=False
    if active and line.startswith('|'):
        cols=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(cols)==5 and cols[0]!='분야' and not set(cols[0])<=set('- :'):
            source_roles.append((cols[0],cols[1]))
need(len(source_roles)==166,'원본 직무 수 변경: 계획 갱신 필요')
need(len(experts)==len(source_roles),'원본 직무 누락 또는 추가')
for i,(family,name) in enumerate(source_roles,1):
    id=f'{i:03}'
    row=experts.get(id,{})
    need(row.get('family')==family and row.get('name')==name,id+': 원본 직무 대응 불일치')
for id,r in experts.items():
    f=root/r['case_document']
    need(f.is_file(),id+': 직무별 파일 없음')
    if f.is_file():need(f.read_text().splitlines()[0].startswith('# '+id+'.'),id+': 직무 문서 ID 불일치')
    expected=sorted(d['id'] for d in domains.values() if id in d['roles'])
    need(sorted(r['priority_domain_ids'])==expected,id+': 우선 분야 역참조 불일치')
covered_cases=[]
for id,g in research.items():
    need('EA-'+id in tasks,id+': 연구 작업 없음')
    need('EA-X'+id[1:] in tasks,id+': 실행 모듈 작업 없음')
    for cid in g['cases']:
        need(cid in cases,id+': 없는 입력 '+cid)
        if cid in cases:need(cases[cid]['research']==id,cid+': 연구 묶음 불일치')
        covered_cases.append(cid)
need(sorted(covered_cases)==sorted(cases),'입력 경우가 연구에 누락 또는 중복 배정됨')
for id,c in cases.items():
    for key in ['method','tools','output','question','fallback']:
        need(bool(c.get(key)),id+': '+key+' 없음')
    need('| '+id+' |' in doc,id+': 사람이 읽는 표에서 누락')
for id,d in domains.items():
    need(all(x in experts for x in d['roles']),id+': 없는 직무 참조')
    need(all(x in cases for x in d['cases']),id+': 없는 입력 참조')
    need(d['research_task'] in tasks and d['build_task'] in tasks,id+': 작업 연결 없음')
    need(d['research_task'] in tasks[d['build_task']]['dependsOn'],id+': 분야 조사가 제작에 연결되지 않음')
    need('| '+id+' |' in doc,id+': 사람이 읽는 분야 표에서 누락')
for id,r in reqs.items():
    need(all(x in domains for x in r['domains']),id+': 없는 분야 참조')
    if r['type']=='domains':need(bool(r['domains']),id+': 분야 요구 미배정')
domain_coverage=set(x for r in reqs.values() for x in r['domains'])
need(domain_coverage==set(domains),'사용자 요구와 우선 분야 연결 누락')
for id,t in tasks.items():
    for key in ['output','inputs','steps','criteria','owner']:
        need(bool(t.get(key)),id+': '+key+' 없음')
    need(all(dep in tasks for dep in t['dependsOn']),id+': 없는 선행 작업')
seen=set()
stack=set()
def visit(id):
    if id in stack:errors.append('의존 순환: '+id);return
    if id in seen:return
    stack.add(id)
    for dep in tasks[id]['dependsOn']:
        if dep in tasks:visit(dep)
    stack.remove(id)
    seen.add(id)
for id in tasks:visit(id)
for target in re.findall(r'\]\(([^)]+)\)',doc):
    if target.startswith(('http://','https://','#')):continue
    p=(root/'docs'/unquote(target.split('#')[0])).resolve()
    need(p.exists(),'문서 로컬 링크 없음: '+target)
need(doc.count('~~~')%2==0,'문서 코드 블록 닫힘 불일치')
need('{{' not in doc,'미완성 문서 치환자')
mapfile=root/'.project-map/state.json'
if mapfile.is_file():
    state=json.loads(mapfile.read_text())
    mapped={t['id']:t for t in state['tasks'] if t['id'].startswith('EA-')}
    need(set(mapped)==set(tasks),'프로젝트 지도와 계획 작업 ID 불일치')
    for id,t in tasks.items():
        if id in mapped:
            need(sorted(mapped[id].get('dependsOn',[]))==sorted(t['dependsOn']),id+': 지도 선행 관계 불일치')
            need(mapped[id]['title']==t['title'],id+': 지도 제목 불일치')
result={'ok':not errors,'experts':len(experts),'priority_domains':len(domains),'input_cases':len(cases),'research_groups':len(research),'tasks':len(tasks),'requirements':len(reqs),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)

