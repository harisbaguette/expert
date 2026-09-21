#!/usr/bin/env python3
"""Generate native Mermaid from the same materials and relations as the images.

Each relationship is recorded explicitly as source -> target.
Mermaid does not provide a reliable left-only flowchart arrow in the target
renderer: backward links use <--> with marker-end:none, leaving only the arrow
at the receiving end. This is a one-way rendered return, never a two-way exchange.
Original material and group endpoints remain unchanged. The layout-only
containers have no visible border or title.
"""
from pathlib import Path
import argparse, json, html, re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/도식'
MODES=('solo','orchestration','complex')
TITLES=('1. 단독 상황 — 한 건 · 한 전문가','2. 오케스트레이션 — 한 건 · 여러 전문가','3. 복합 상황 — 맞물린 여러 건 · 여러 전문가')

def export(d,engine='elk'):
 ns=d['nodes'];gs={k:v.copy() for k,v in d['groups'].items() if k!='TITLE'}
 parent={}
 for k,g in gs.items():
  c=[a for a,p in gs.items() if a!=k and p['x']<=g['x'] and p['y']<=g['y'] and p['x']+p['w']>=g['x']+g['w'] and p['y']+p['h']>=g['y']+g['h'] and p['w']*p['h']>g['w']*g['h']]
  parent[k]=min(c,key=lambda a:gs[a]['w']*gs[a]['h']) if c else None
 np={k:(n['containers'][0] if n['containers'] else None) for k,n in ns.items()}
 # Verification is one bounded operation before its explicit outcome decision.
 quality=['check_0','check_1','check_2','opposing','process_quality']
 gs['QUALITY']={'title':' ','subtitle':''};parent['QUALITY']='CHECK'
 for k in quality:np[k]='QUALITY'
 gs['WAIT']={'title':' '};parent['WAIT']='CHECK'
 for k in ['pending', 'wait_result']:np[k]='WAIT'
 gs['DELIVER']={'title':' '};parent['DELIVER']='CHECK'
 for k in ['delivery_0', 'delivery_1', 'received', 'receipt_wait']:np[k]='DELIVER'

 # Resource rows are layout-only groups, never execution steps.
 rows=[]
 for group,parts in [('INPUT',[[f'input_{j}' for j in range(i,min(i+3,11))] for i in range(0,11,3)]),('RULES',[['rule_source_0','rule_source_1'],['rule_rank0_0','rule_rank0_1'],['rule_rank1_0','rule_rank1_1'],['rule_last0','rule_last1','rule_last2'],['priority']])]:
  for i,part in enumerate(parts):
   key=group+'_row'+str(i);gs[key]={'title':' ','subtitle':''};parent[key]=group;rows.append(key)
   for k in part:np[k]=key
 def q(s):return html.escape(s,quote=True).replace('\n','<br/>')
 cfg={'layout':engine,'theme':'base','flowchart':{'defaultRenderer':engine,'htmlLabels':True,'nodeSpacing':24,'rankSpacing':32,'padding':16,'wrappingWidth':300,'curve':'basis','useMaxWidth':True},'themeVariables':{'fontFamily':'Apple SD Gothic Neo, sans-serif','fontSize':'20px','edgeLabelBackground':'#191d25','clusterBkg':'#222a35','clusterBorder':'#52677f'},'themeCSS':'.nodeLabel b{display:inline-block;max-width:280px;white-space:normal;font-size:21px;font-weight:700}.nodeLabel small{display:inline-block;max-width:260px;white-space:normal;word-break:keep-all;text-align:left;font-size:17px;line-height:1.35}.nodeLabel .kind{font-size:13px;color:#586b80}.nodeLabel p{margin:0}.edgeLabel{font-size:17px}.edgeLabel,.edgeLabel p,.edgeLabel span{color:#e5ecf5!important}.cluster-label{font-size:21px;font-weight:600}.cluster-label:has(.label-offset){translate:-160px 0}.cluster-label:has(.branch-offset){translate:-90px 0}.cluster-label:has(.plan-title){translate:-160px 0}.cluster-label:has(.human-title){translate:-60px 0}.cluster-label:has(.learn-title){translate:-180px 0}.cluster-label span{color:#e5ecf5!important}', 'elk':{'nodePlacementStrategy':'SIMPLE','mergeEdges':False,'considerModelOrder':'NODES_AND_EDGES','forceNodeModelOrder':False}}
 lines=['%%{init: '+json.dumps(cfg,ensure_ascii=False)+' }%%','flowchart TB','  %% 회색 무화살표 선은 적용 관계. 파랑은 결과 전달, 노랑은 실제 복귀, 빨강은 아니오·차단.','  %% 그룹의 소속은 실행 순서가 아니다. ~~~ 연결은 배치 제약만 뜻한다.', '  %% <--> 중 marker-end:none인 선은 왼쪽 화살촉만 표시한다. 양방향 관계가 아니다.', '  %% 모든 실제 관계의 방향은 각 선 위의 relation: 출발 -> 도착 주석에 명시한다.']
 def node(k,depth):
  n=ns[k];cl={'action':'action','support':'support','process':'process','decision':'decision','terminal':'terminal','stop':'stop','fork':'fork'}[n['kind']]
  if cl=='fork':return [' '*depth+k+'@{ shape: fork }',' '*depth+'class '+k+' fork']
  note=n['note']
  rank={'rule_rank0_0':'①','rule_rank0_1':'①','rule_rank1_0':'②','rule_rank1_1':'②','rule_last0':'③','rule_last1':'④','rule_last2':'⑤'}.get(k)
  if rank:note=rank+' 충돌 시 우선순위\n'+note
  label='<b>'+q(n['name'])+'</b>'
  if note:label+='<br/><small>'+q(note)+'</small>'
  if n['material']:label+='<br/><span class=\'kind\'>'+n['usage']+'</span>'
  a,z=('{','}') if cl=='decision' else ('([','])') if cl in ['terminal','stop'] else ('[',']')
  return [' '*depth+f'{k}{a}"{label}"{z}:::{cl}']
 def group(k,depth=2):
  g=gs[k];title=g['title']

  label=q(title)
  if g.get('subtitle'):label+="<br/><span style='font-size:16px;font-weight:400'>"+q(g['subtitle'])+"</span>"
  if k in ['CHECK','QUALITY']:label="<span class='label-offset'>"+label+"</span>"
  if k in ['WAIT','FOLLOW','DELIVER']:label="<span class='branch-offset'>"+label+"</span>"
  if k in ['PLAN','HUMAN','LEARN']:label="<span class='"+k.lower()+"-title'>"+label+"</span>"
  s=[' '*depth+f'subgraph {k}["{label}"]']
  dr='LR' if k in rows or k in ['INTAKE','PLAN','HUMAN','RUNBASE','COORD','CAPABILITY','QUALITY'] else 'TB'
  s+=[' '*(depth+2)+'direction '+dr]
  for n in ns:
   if np[n]==k:s+=node(n,depth+2)
  for child in gs:
   if parent[child]==k:s+=group(child,depth+2)
  s+=[' '*depth+'end'];return s
 for k in ns:
  if np[k] is None:lines+=node(k,2)
 for k in gs:
  if parent[k] is None:lines+=group(k)
 actual=[];reverse_indices=[]
 for i,e in enumerate(d['edges']):
  a,b=e['source'],e['target']
  label=q(e['label']);op='---' if e['kind']=='apply' else '-->'
  src=d['nodes'].get(e['source']) or d['groups'][e['source']];dst=d['nodes'].get(e['target']) or d['groups'][e['target']]
  if (dst['y']<src['y'] or (dst['y']==src['y'] and dst['x']<src['x'])) and not (e['source']=='permit' and e['target']=='human_0'):
   a,b=b,a
   if op=='-->':op='<-->';reverse_indices.append(i)
  lines.append(f'  %% relation {i}: {e["source"]} -> {e["target"]}; {e["kind"]}')
  lines.append(f'  {a} {op} '+(f'|"{label}"| ' if label else '')+b)
  actual.append(e['kind'])
 for a,b in [('start','notice'),('start','watch'),('INTAKE','INPUT'),('INTAKE','RULES'),('PLAN','CAPABILITY'),('permit','RUNBASE')]:
  lines.append(f'  {a} ~~~ {b}');actual.append('layout')
 for group in ['INPUT','RULES']:
  rowkeys=[k for k in rows if parent[k]==group]
  for a,b in zip(rowkeys,rowkeys[1:]):lines.append(f'  {a} ~~~ {b}');actual.append('layout')
 for key in rows+['RUNBASE']:
  members=[k for k in ns if np[k]==key]
  for a,b in zip(members,members[1:]):lines.append(f'  {a} ~~~ {b}');actual.append('layout')
 colors={'action':('#e3edf9','#889fb9','#1c344d'),'support':('#edf0f4','#9aa8b7','#293d50'),'process':('#d9eaff','#83a9d4','#183752'),'decision':('#fff5c4','#d3b34c','#664e13'),'terminal':('#dff6e7','#71b888','#174d2d'),'stop':('#ffe6e5','#df8e8e','#7f252a')}
 lines.append('  classDef fork fill:#e5ecf5,stroke:#e5ecf5,color:#e5ecf5')
 for k,(fill,stroke,col) in colors.items():lines.append(f'  classDef {k} fill:{fill},stroke:{stroke},stroke-width:1px,color:{col}'+(',rx:10px,ry:10px' if k in ['action','support','process'] else ''))
 for k in gs:lines.append(f'  style {k} fill:'+('transparent,stroke:transparent' if k in rows or k in ['QUALITY','WAIT','DELIVER'] else '#222a35,stroke:#52677f,stroke-width:1px,stroke-dasharray:2 6')+',color:#e5ecf5')
 palette={'flow':'#71aeff','data':'#71aeff','return':'#ffd452','blocked':'#ff8d91','apply':'#94a6b9'}
 for kind,color in palette.items():
  ix=[str(i) for i,k in enumerate(actual) if k==kind]
  if ix:lines.append(f'  linkStyle {",".join(ix)} stroke:{color},stroke-width:{"1.5" if kind=="apply" else "2"}px')
 for i in reverse_indices:lines.append(f'  linkStyle {i} stroke:{palette[actual[i]]},stroke-width:2px,marker-end:none')
 return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embed',action='store_true',help='Replace only the usage section in the definition document.')
    args=parser.parse_args()
    model=json.loads((OUT/'사용-구조-원본.json').read_text())
    charts={mode:export(model['diagrams'][mode]) for mode in MODES}
    for mode,source in charts.items():
        (OUT/f'usage-structure-{mode}.mmd').write_text(source)
        print(f'{mode}: native Mermaid generated')
    if args.embed:
        doc=ROOT/'전문가 에이전트 정의.md'
        prefix=doc.read_text().split('## 사용 구조',1)[0]
        parts=['## 사용 구조\n']
        for mode,title in zip(MODES,TITLES):
            parts.append(f'### {title}\n\n![{title}](docs/images/expert-definition/usage-structure-{mode}.svg)\n\n```mermaid\n{charts[mode]}```\n')
        doc.write_text(prefix+'\n'.join(parts))

if __name__=='__main__':
    main()
