#!/usr/bin/env python3
"""Verify the three usage diagrams against the canonical material table.
Execution, application relationships and invisible layout constraints are separate.
Visual geometry is checked from a rendering of the exact saved source.
"""
from pathlib import Path
from collections import Counter,defaultdict
from html import unescape
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]
path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'전문가 에이전트 정의.md'
doc=path.read_text();prefix,usage=doc.split('## 사용 구조',1)
catalog={}
for line in prefix.split('## 계통별 재료',1)[1].splitlines():
 if line.startswith('| **') and '✅' in line:
  c=line.strip('|').split('|')
  if len(c)==6:
   name=re.search(r'\*\*(.*?)\*\*',c[0])[1]
   catalog[name]={'type':c[4].strip().strip('*'),'condition':c[5].strip(),'definition':c[2].strip()}
assert len(catalog)==79
blocks=re.findall(r'```mermaid\n([\s\S]*?)\n```',usage)
assert len(blocks)==3 and not re.search(r'<svg|!\[',usage)
results=[];trace={}
for scenario,src in zip(('단독','오케스트레이션','복합'),blocks):
 assert len(src)<50000
 nodes={};groups={};stack=[];edges=[];materials={}
 for line in src.splitlines():
  if m:=re.fullmatch(r'\s*subgraph (\w+)\[".*?"\]',line):
   key=m[1];groups[key]={'parent':stack[-1] if stack else None,'nodes':[]};stack.append(key)
  elif line.strip()=='end':stack.pop()
  elif m:=re.fullmatch(r'\s*(\w+)([\[({]+)"(.*?)"[\])}]+:::(\w+)',line):
   key,shape,label,style=m.groups();assert key not in nodes
   nodes[key]={'shape':shape,'label':label,'style':style,'group':stack[-1] if stack else None}
   if stack:groups[stack[-1]]['nodes'].append(key)
   titles=re.findall(r'<b>(.*?)</b>',label)
   helper=unescape(re.sub(r'<[^>]+>',' ',label.split('</b>',1)[-1])).strip()
   if any(helper.startswith(t) for t in ['상시','단계별','조건부']):
    assert titles and len(titles)==1 and titles[0] in catalog,(scenario,key,'invalid material title')
    name=titles[0];assert helper.startswith(catalog[name]['type']),(scenario,key,'wrong usage type');materials[key]=name
  elif m:=re.fullmatch(r'\s*(\w+)@\{ shape: fork \}',line):nodes[m[1]]={'shape':'fork','label':'','style':'fork','group':stack[-1] if stack else None}
  elif m:=re.fullmatch(r'\s*(\w+)\s+(-->|<---|---|~~~)\s*(?:\|"(.*?)"\|\s*)?(\w+)',line):
   a,op,label,b=m.groups()
   if op=='<---':a,b,op=b,a,'-->'
   edges.append((a,b,op,unescape(re.sub(r'<br\s*/?>',' ',label or ''))))
 assert not stack
 assert set(materials.values())==set(catalog),(scenario,'missing',set(catalog)-set(materials.values()))
 assert len(edges)<=500,(scenario,len(edges))
 support={k for k,n in nodes.items() if n['style']=='support'};flow=set(nodes)-support
 assert support<=set(materials)
 g=defaultdict(list);rev=defaultdict(list);bound=set();applications={}
 for a,b,op,label in edges:
  assert a in nodes or a in groups,(scenario,a)
  assert b in nodes or b in groups,(scenario,b)
  if op=='-->':
   assert a in flow and b in flow,(scenario,'support serialized',a,b)
   g[a].append((b,label));rev[b].append(a)
  elif op=='---':
   assert a in flow and b in groups and label
   members=set(groups[b]['nodes']);assert members and members<=support
   assert not members&bound;bound|=members
   for n in members:applications[n]={'action':a,'scope':label}
 assert bound==support,(scenario,'unbound materials',support-bound)
 def walk(start,reverse=False,cut=()):
  seen=set();todo=[start]
  while todo:
   n=todo.pop()
   if n in seen:continue
   seen.add(n)
   if n not in cut:todo+=rev[n] if reverse else [x for x,l in g[n]]
  return seen
 def has(a,b,label=None):return any(x==b and (label is None or label in l) for x,l in g[a])
 roots={n for n in flow if not rev[n]};ends={n for n in flow if not g[n]}
 assert roots=={'start'} and walk('start')==flow,(scenario,'disconnected execution',roots,flow-walk('start'))
 assert flow<=set().union(*(walk(n,True) for n in ends))
 terminals={n for n in flow if nodes[n]['shape']=='(['};assert terminals==roots|ends
 for n in flow:
  if nodes[n]['shape']=='{':assert len(g[n])>=2 and all(l for b,l in g[n]),(scenario,'incomplete decision',n,g[n])
  elif nodes[n]['shape']!='fork':assert len(g[n])<=1,(scenario,'branch without decision',n,g[n])
 assert not re.search(r'-.->|\[\[|\(\(',src)
 colors={}
 for ids,style in re.findall(r'^\s*linkStyle ([\d,]+) (.*)$',src,re.M):
  for i in map(int,ids.split(',')):colors[i]=re.search(r'stroke:(#[\da-fA-F]+)',style)[1].lower()
 returns=set(re.findall(r'%% 복귀선: (\w+) --> (\w+)',src))
 for i,(a,b,op,label) in enumerate(edges):
  if op=='~~~':assert i not in colors;continue
  if op=='---':assert colors[i]=='#a8b2c1';continue
  assert colors[i] in {'#60a5fa','#f87171','#facc15'}
  assert (colors[i]=='#facc15')==((a,b) in returns)
  if label.startswith('아니오') and (a,b) not in returns:assert colors[i]=='#f87171'
 # Material-specific conditions and concrete transfer / failure routes.
 assert has('resume','saved','예') and has('resume','facts','아니오')
 assert has('monitorq','monitor','예') and has('noticeq','notice','예')
 assert has('styleq','style_rule','예') and has('styleq','resolved','아니오')
 assert all(t in nodes['priority']['label'] for t in ['법적 관계','충돌한 조항만','함께 지킴'])
 assert has('identity_ok','identity_stop','아니오') and has('known','unknown','아니오')
 assert has('repair','replan') and has('replan','repair_guard') and has('repair_guard','repair_allowed')
 assert has('repair_allowed','rework_hold','아니오')
 assert has('change_possible','repair','예')
 assert has('improve','learn_env') and has('learn_env','test')
 assert has('test_ok','remember','예') and has('test_ok','keep','아니오')
 roles=['s'] if scenario=='단독' else ['aw','bw']
 practical={'시험 환경','관찰·측정','실험','시뮬레이션','자료 선별·분류','자료 정리·결합','형식·구조 변환','계산','분석','예측','조건 안에서 최선 찾기','기준 적용·판정','실시간 대화','사람과 소통','협상·조율','결과물 설계','내용 재구성','결과물 만들기·수정','기록 입력·수정','신청·거래 처리','설정·작동 제어','게시·배포'}
 for p in roles:
  def owned(n):
   group=nodes[n]['group']
   while group:
    if group==p+'WORK':return True
    group=groups[group]['parent']
   return False
  own={n:t for n,t in materials.items() if owned(n) and n in flow}
  assert practical<=set(own.values()),(scenario,p,'opaque practical processing')
  for n,t in own.items():
   if t in practical:assert any(nodes[a]['shape']=='{' and has(a,n,'예') for a in rev[n]),(scenario,n,'missing conditional entry')
  assert has(p+'fixed',p+'choice','예') and has(p+'fixed',p+'think','아니오')
  assert has(p+'choice',p+'clarify','아니오') and (p+'clear',p+'think') in returns
  assert has(p+'permit',p+'state','아니오') and has(p+'permit',p+'run','예')
  for q in ['contact','designok','writeok']:
   target=p+('TALKLANE' if q=='contact' else 'MAKELANE')+'hold'
   assert has(p+q,target,'아니오') and has(target,p+'verify')
  assert {l for b,l in g[p+'valid']}=={'미확인','문제 있음','문제없음'}
  assert (p+'continue',p+'in') in returns
  assert has(p+'next',p+'continue') and has(p+'state',p+'more')
  assert not (set(own)-walk(p+'in')),(scenario,p,'unreachable owned materials')
 if scenario=='단독':
  assert any(t=='나눠 맡기기' and '미사용' in nodes[n]['label'] for n,t in materials.items())
  assert ('repair_allowed','sin') in returns
 else:
  assert nodes['parallel']['shape']=='fork' and len(g['parallel'])==2
  assert ('repair_allowed','assign') in returns
  assert has('collect_deadline','collect_missing','아니오')
  for k in ['a','b']:
   assert has(k+'_input',k+'win') and has(k+'wmore',k+'wdone','아니오') and has(k+'wdone',k+'_done')
  if scenario=='오케스트레이션':
   assert has('dependency','a_input','예') and has('dependency','parallel','아니오')
   assert has('a_valid','a_to_b','예') and has('a_to_b','b_ready') and has('b_ready','b_input','예') and has('a_valid','b_hold','아니오')
  if scenario=='복합':
   assert has('dependency','parallel','아니오') and has('dependency','a_plan','예')
   assert has('a_valid','a_to_b','예') and has('a_valid','b_hold','아니오') and has('a_to_b','b_ready') and has('b_ready','b_plan','예')
   for k in ['a','b']:
    assert has(k+'_collect',k+'_team_all') and has(k+'_team_deadline',k+'_team_missing','아니오')
 # Auditable inventory: direct relation evidence, not presence-only matching.
 trace[scenario]={}
 clean=lambda s:unescape(re.sub('<[^>]+>',' ',s)).strip()
 for name,cat in catalog.items():
  occurrences=[]
  for n,t in materials.items():
   if t!=name:continue
   chain=[];group=nodes[n]['group']
   while group:
    chain.append(group);group=groups[group]['parent']
   if scenario=='단독':owner='한 전문가'
   elif 'a_TEAM' in chain:owner='건 A 총괄·해당 전문가' if scenario=='복합' else '전문가 A'
   elif 'b_TEAM' in chain:owner='건 B 총괄·해당 전문가' if scenario=='복합' else '전문가 B'
   elif any(k in chain for k in ['RUNTIME','RULE_INPUT','SOURCE_CHECK','JUDGMENT']):owner='모든 담당에게 적용'
   else:owner='전체 총괄' if scenario=='복합' else '총괄'
   occurrences.append({'node':n,'group':nodes[n]['group'],'owner':owner,'canonical_condition':cat['condition'],'explanation':clean(nodes[n]['label']),'incoming':[{'from':a,'condition':l} for a,b,op,l in edges if b==n and op=='-->'],'outgoing':[{'to':b,'transfer':l} for a,b,op,l in edges if a==n and op=='-->'],'application':applications.get(n)})
  trace[scenario][name]={**cat,'occurrences':occurrences}
 results.append({'scenario':scenario,'materials':len(set(materials.values())),'types':dict(Counter(c['type'] for c in catalog.values())),'nodes':len(nodes),'execution_nodes':len(flow),'support_nodes':len(support),'execution_arrows':sum(e[2]=='-->' for e in edges),'application_relations':sum(e[2]=='---' for e in edges),'layout_edges':sum(e[2]=='~~~' for e in edges),'starts':len(roots),'endings':len(ends),'reachable_execution_nodes':len(walk('start')),'bound_support_nodes':len(bound),'source_characters':len(src),'checks':'pass'})
if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
