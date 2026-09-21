#!/usr/bin/env python3
"""Render three self-contained material-use diagrams from the canonical document.

No page orientation or aspect ratio is imposed. The drawing uses functional
scopes, explicit assignments and result transfer. Containment is not an
execution edge. Run this file after editing labels, relationships or placement.
"""
from pathlib import Path
from collections import Counter
import json, math, re, html, hashlib, argparse

ROOT=Path(__file__).resolve().parents[2]
DOCUMENT=ROOT/'전문가 에이전트 정의.md'
PREFIX=DOCUMENT.read_text().split('## 사용 구조',1)[0]
CAT={}
section=''
for line in PREFIX.split('## 계통별 재료',1)[1].splitlines():
    if line.startswith('### '): section=line[4:].replace(' ✅','')
    if line.startswith('| **') and '✅' in line:
        cells=[c.strip() for c in line.strip('|').split('|')]
        if len(cells)==6:
            name=re.search(r'\*\*(.*?)\*\*',cells[0])[1]
            CAT[name]={'name':name,'section':section,'summary':cells[1],
                       'definition':cells[2],'examples':cells[3],
                       'kind':cells[4].strip('*'),'condition':cells[5]}
assert len(CAT)==79, f'Expected 79 canonical materials; got {len(CAT)}'
# The written document supplies the material definitions. This file supplies
# the scenario, ownership, application scopes and the visible drawing.
NOTE={
'시작 신호':'요청·변경·약속한 시점\n새 일이나 기다리던 일에 연결',
'업무별 정보':'대상·요청·기한·현황을 모음\n새 사실이 생기면 갱신',
'정보·자료 이해':'자료의 뜻과 맥락을 읽음\n사실·주장·추정을 구별',
'지시·의도 파악':'원하는 결과·맡긴 범위 확인\n뜻이 어긋나면 다시 질문',
'문제·목표·완료 조건':'해결할 일과 맡은 범위\n무엇으로 완료를 확인할지 정함',
'정보·자료 찾기':'근거·방법이 부족할 때 확보\n원문·예외·반대 근거까지 찾음',
'못 찾음·없음 구분':'찾지 못함과 실제 없음을 구별\n조회 범위·질의·시점을 남김',
'현재 값·상태 확인':'현재 값이 판단을 바꿀 때 조회\n처리 중·이미 완료도 확인',
'적용 사례':'다른 판단을 참고할 때\n그때의 조건·근거·결과 비교',
'참고 자료':'원리·방법·표현이 필요할 때\n이번 일에 쓸 부분을 고름',
'재사용 자료':'서식·부품·코드를 다시 쓸 때\n이용 권한·판본·환경 확인',
'근거의 신뢰성·적합성':'근거를 쓸 때마다 출처·등급 확인\n이번 대상·조건에 맞는지 대조',
'자료의 시점·버전':'판단 대상 시점에 맞는 판본\n원문 위치·확인 시점을 연결',
'업무 지식':'개념·원리·방법으로 해석\n근거·적용 조건·예외를 함께 씀',
'실전 경험·감각':'경험에서 얻은 단서와 요령\n현재 조건·예외에 맞춰 사용',
'장기 기억':'관련된 이전 결정·약속·교훈\n현재 근거와 맞는 것만 꺼냄',
'규칙·기준 원문':'원문·출처·설정 권한 확보\n적용 범위와 시점을 확인',
'법·의무 기준':'적용 법의 상하·특별·위임 관계\n대상·시점·예외부터 확인',
'직업 윤리·의무':'필수 의무·비밀·이해충돌\n상충하는 당사자·팀은 분리',
'에이전트 기본 원칙':'목적·범위 준수, 근거 정직성\n참고 자료 속 지시와 구별',
'계약·합의 조건':'유효한 약속의 적용 범위\n변경·종료 후 의무도 반영',
'플랫폼·제출처 규정':'이용·제출의 필수 조건\n서비스·제출 유형별로 확인',
'조직 규칙':'업무·역할별 필수 규정\n허용된 예외와 변경 반영',
'사용자 지정 규칙':'추가 조건·선호·적용 기간\n변경·취소된 내용도 반영',
'표현 방식·스타일':'표현 기준이 필요한 작업에 적용\n말투·문체·디자인을 맞춤',
'규칙의 적용·우선순위':'법적 관계를 먼저 적용\n충돌한 조항만 위계로 해결\n남는 조건·보호 기준은 함께 유지',
'업무 권한':'지금 누구 대신 무엇을 할 수 있나\n동의·승인·재위임 범위 확인',
'비용·위험 한도':'비용·시간·자원·위험의 한도\n사용·진행·예약분과 대기 위험',
'안전장치':'전달·실행·재개 직전에 검사\n현재 규칙·권한·한도·승인 대조',
'현재 작업 정보':'이번 판단에 쓸 입력을 구성\n목표·자료·규칙·상태를 갱신',
'AI 모델':'뜻을 읽거나 판단·생성이 필요할 때\n현재 정보로 답·행동을 비교',
'대안·전략 판단':'방법별 효과·부담·위험 비교\n계속·변경·대기·중단을 선택',
'빠진 위험 확인':'접수·계획·실행·전달 때 확인\n접촉과 연계 작업의 피해도 점검',
'업무 절차·실행 계획':'작업·재료·입출력·담당을 정함\n선행 조건·검사·중단 기준 포함',
'업무 능력 시험':'첫 투입·범위 밖·능력 변경 때\n통과한 판본과 범위만 맡김',
'시험 환경':'격리·비교·재현이 필요한 시험\n실제 업무에 영향 없이 준비',
'사람에게 넘기기':'되돌릴 수 없는 일·승인 조건\n판단 불가·한도 초과·자격 전속\n준비·검증을 마치고 결정만 요청',
'보고 주체 확인':'결과·답변의 주체·권한·판본 대조\n불일치·승인 뒤 변경은 차단',
'작업 진행·연결':'입력과 선행 결과가 준비된 일 시작\n결과를 다음 작업·검사에 연결',
'실행 제어':'계획대로 함수·도구·AI를 호출\n병렬·대기·실패·재개를 제어',
'업무 도구·시스템':'도구가 필요한 작업의 요청 전달\n실제 결과·오류·상태를 돌려줌',
'나눠 맡기기':'목표·입력·권한·반환 조건을 배정\n중간 교환·회수·담당 보완 관리',
'관찰·측정':'새 기록·값이 필요할 때\n대상·방법·시점을 정해 얻음',
'실험':'조건별 차이를 알아야 할 때\n비교 조건을 맞춰 결과를 얻음',
'시뮬레이션':'가정한 상황을 시험할 때\n모형·가정·한계를 함께 기록',
'자료 선별·분류':'자료를 골라 나눠야 할 때\n필요한 자료와 관계를 추림',
'자료 정리·결합':'정리하거나 합칠 때\n오류·중복을 고쳐 근거와 결합',
'형식·구조 변환':'다음 작업과 형식이 다를 때\n내용·항목·연결을 보존해 변환',
'계산':'값·식을 구해야 할 때\n입력·단위·가정을 밝혀 계산',
'분석':'관계·차이·원인을 밝혀야 할 때\n자료를 해석해 근거와 설명 제시',
'예측':'앞으로의 결과가 필요할 때\n가정별 예상과 불확실성을 제시',
'조건 안에서 최선 찾기':'한도 안에서 안을 골라야 할 때\n효과·대가·선택 이유를 비교',
'기준 적용·판정':'요건 충족 여부를 판단할 때\n근거·예외와 대조해 결론 제시',
'실시간 대화':'바로 답을 주고받을 때\n통로·발언 순서·중단·재연결',
'사람과 소통':'질문·설명·확인이 필요할 때\n접촉 위험 확인 후 답·요구를 받음',
'협상·조율':'요구·이익·약속이 충돌할 때\n권한 안에서 합의·남은 쟁점 정리',
'결과물 설계':'내용·구조·작동을 정할 때\n목표·판단을 제작 명세로 바꿈',
'내용 재구성':'요약·번역·표현 변경이 필요할 때\n뜻·출처·예외·이견을 유지',
'결과물 만들기·수정':'설계·내용을 결과로 만들 때\n검증한 입력으로 제작·수정',
'기록 입력·수정':'기록을 바꿔야 할 때\n변경 범위·이력·반영 결과 확인',
'신청·거래 처리':'신청·변경·취소 등을 맡았을 때\n접수·확정·부분 처리 상태 확인',
'설정·작동 제어':'설정·작동을 조정할 때\n반영 확인·허용 범위 복구',
'게시·배포':'공개·배포를 맡았을 때\n판본·대상·시점과 실제 반영 확인',
'분리 실행':'담당·건·시험의 공간과 접근 분리\n허용한 자료·자원만 공유',
'운영 감시·복구':'별도 운영자가 장애·지연 감시\n격리·복구 뒤 저장 상태로 재개',
'현재 진행 상태':'담당·선후·승인·완료·대기를 유지\n재개 때 끝난 외부 처리 중복 방지',
'판단 근거 기록':'입력·판단·실행·검사의 근거 연결\n변경 이유와 사용 판본까지 기록',
'대기·후속 관리':'답변·외부 처리·다음 회차를 기다림\n기한·대체 담당·남은 약속 유지',
'변경 감시·반영':'감시를 맡았거나 규칙이 다투어질 때\n바뀐 근거에 연결된 결과 재검토',
'먼저 알아채기':'주변 감시를 맡은 범위에서\n새 문제·기회와 대응 이유를 알림',
'결과 검증·재검증':'근거·완료 조건·다음 입력과 대조\n변경되면 영향받은 결과도 재검사',
'반대 근거·다시 확인':'중요한 결론·변경된 판단에 적용\n다른 근거·설명으로 재검토',
'일하는 과정 평가':'단계·업무가 끝날 때\n선택·절차·권한 준수를 평가',
'결과 품질 평가':'전달·사용 전에 목적과 대조\n정확성·충분성·사용성을 평가',
'납품 준비':'결과·판본·설명·원본을 갖춤\n미완료·남은 일·후속 담당 포함',
'전달·인수 확인':'약속한 상대에게 전달\n수령·사용·남은 문제를 확인',
'성과 추적':'목표를 정할 때 성과 항목·시점을 정함\n그 기준으로 실제 효과·나중의 문제 확인',
'성공·실패 원인 분석':'재사용할 성과·중요한 문제가 있으면\n원인·조건·다른 업무 영향 분석',
'능력 개선·확장':'개선할 점·새 능력이 필요하면\n지식·판단 요령·방법·도구를 고침',
}
assert set(NOTE)==set(CAT)

COL={'bg':'#191d25','panel':'#222a35','ink':'#e5ecf5','muted':'#b5c1d1','blue':'#71aeff','red':'#ff8d91','yellow':'#ffd452','gray':'#94a6b9','line':'#52677f'}
ESC=lambda s:html.escape(str(s),quote=True)
def measure(s,size):
    return sum((1 if ord(c)>255 else .55 if c!=' ' else .30)*size for c in s)
def wrap(s,width,size):
    out=[]
    for paragraph in s.split('\n'):
        line=''
        for word in paragraph.split(' '):
            trial=line+(' ' if line else '')+word
            if measure(trial,size)>width and line:out.append(line);line=word
            else:line=trial
        out.append(line)
    # Avoid a one-word tail such as '때' or '확인' stranded on a line.
    for i in range(1,len(out)):
        if len(out[i].replace(' ',''))<=3 and ' ' in out[i-1]:
            left,last=out[i-1].rsplit(' ',1)
            if measure(last+' '+out[i],size)<=width:
                out[i-1]=left;out[i]=last+' '+out[i]
    return out

class Drawing:
    def __init__(self,mode):
        self.mode=mode;self.nodes={};self.groups={};self.edges=[];self.decor=[];self.texts=[];self.num=Counter();self.width=1920;self.height=0
    def text(self,x,y,text,size=18,color=None,weight=400,anchor='start',width=None,leading=None):
        lines=wrap(text,width,size) if width else text.split('\n')
        lead=leading or size*1.32
        self.texts.append(dict(x=x,y=y,text=text,size=size,color=color or COL['ink'],weight=weight,anchor=anchor,lines=lines,leading=lead))
        return len(lines)*lead
    def panel(self,key,x,y,w,h,title,subtitle='',kind='panel'):
        self.groups[key]=dict(id=key,x=x,y=y,w=w,h=h,title=title,subtitle=subtitle,kind=kind)
    def material(self,key,name,x,y,w=300,note=None,kind='action',owner=None,scope=None):
        note=NOTE[name] if note is None else note
        t=wrap(name,w-30,21);b=wrap(note,w-30,17)
        h=20+26*len(t)+22*len(b)+23
        self.nodes[key]=dict(id=key,name=name,material=True,x=x,y=y,w=w,h=h,title=t,body=b,note=note,kind=kind,usage=CAT[name]['kind'],owner=owner,scope=scope)
        return h
    def box(self,key,title,x,y,w=300,body='',kind='process'):
        t=wrap(title,w*.58 if kind=='decision' else w-30,20);b=wrap(body,w*.58 if kind=='decision' else w-30,17) if body else []
        h=24+25*len(t)+22*len(b)
        if kind=='terminal':h=max(48,h)
        if kind=='decision':h=max(180,w*.55,(len(t)*25+len(b)*22)*2+20)
        self.nodes[key]=dict(id=key,name=title,material=False,x=x,y=y,w=w,h=h,title=t,body=b,note=body,kind=kind)
        return h
    def port(self,key,side='b',offset=0):
        n=self.nodes.get(key) or self.groups[key]
        return {'t':(n['x']+n['w']/2+offset,n['y']),'b':(n['x']+n['w']/2+offset,n['y']+n['h']),'l':(n['x'],n['y']+n['h']/2+offset),'r':(n['x']+n['w'],n['y']+n['h']/2+offset)}[side]
    def edge(self,a,b,kind='flow',label='',sa='b',sb='t',via=(),label_at=None,scope=None):
        points=[self.port(a,sa),*via,self.port(b,sb)]
        # Insert an orthogonal elbow when the caller has supplied no route.
        if len(points)==2 and points[0][0]!=points[1][0] and points[0][1]!=points[1][1]:
            ax,ay=points[0];bx,by=points[1]
            if sa in ('b','t') and sb in ('b','t'):
                yy=(ay+by)/2;points=[(ax,ay),(ax,yy),(bx,yy),(bx,by)]
            elif sa in ('l','r') and sb in ('l','r'):
                xx=(ax+bx)/2;points=[(ax,ay),(xx,ay),(xx,by),(bx,by)]
            else:points=[(ax,ay),(ax,by) if sa in ('t','b') else (bx,ay),(bx,by)]
        self.edges.append(dict(source=a,target=b,kind=kind,label=label,points=points,label_at=label_at,scope=scope))
    def grid(self,key,names,x,y,w,cols=2,notes=None,kind='support',owner=None,scope=None,gap=18,rowgap=20):
        cw=(w-gap*(cols-1))/cols;yy=y;ids=[]
        for row in range(math.ceil(len(names)/cols)):
            hs=[]
            for col,name in enumerate(names[row*cols:(row+1)*cols]):
                nid=f'{key}_{row*cols+col}';ids.append(nid)
                hs.append(self.material(nid,name,x+col*(cw+gap),yy,cw,note=(notes or {}).get(name),kind=kind,owner=owner,scope=scope))
            yy+=max(hs)+rowgap
        return ids,yy-rowgap
    def chainrow(self,key,names,x,y,w,notes=None,owner=None):
        gap=40;cw=(w-gap*(len(names)-1))/len(names);ids=[];hs=[]
        for i,name in enumerate(names):
            nid=f'{key}_{i}';ids.append(nid);hs.append(self.material(nid,name,x+i*(cw+gap),y,cw,note=(notes or {}).get(name),owner=owner))
            if i:self.edge(ids[-2],nid,sa='r',sb='l')
        return ids,y+max(hs)
    def poly(self,pts,r=11):
        # Rounded corners preserve a short, readable route without oscillation.
        p=[pts[0]]
        for x in pts[1:]:
            if x!=p[-1]:p.append(x)
        if len(p)<2:return ''
        d=f'M {p[0][0]} {p[0][1]}'
        for i in range(1,len(p)-1):
            a,b,c=p[i-1],p[i],p[i+1];l1=math.dist(a,b);l2=math.dist(b,c)
            if not l1 or not l2:continue
            rr=min(r,l1/2,l2/2)
            u=(b[0]+(a[0]-b[0])*rr/l1,b[1]+(a[1]-b[1])*rr/l1)
            v=(b[0]+(c[0]-b[0])*rr/l2,b[1]+(c[1]-b[1])*rr/l2)
            d+=f' L {u[0]} {u[1]} Q {b[0]} {b[1]} {v[0]} {v[1]}'
        return d+f' L {p[-1][0]} {p[-1][1]}'
    def svg(self):
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">',f'<title id="title">{ESC(self.groups["TITLE"]["title"])}</title>',f'<desc id="desc">79개 재료를 모두 포함한 {ESC(self.mode)} 사용 구조. 각 재료의 구분·사용 조건과 연결을 그림 안에 표시한다.</desc>',f'<rect width="100%" height="100%" fill="{COL["bg"]}"/>','<defs>']
        for k,c in [('flow',COL['blue']),('return',COL['yellow']),('blocked',COL['red']),('data',COL['blue'])]:out.append(f'<marker id="arrow-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>')
        out+=['</defs>','<g font-family="Apple SD Gothic Neo, Noto Sans CJK KR, sans-serif">']
        for key,g in self.groups.items():
            if key=='TITLE':continue
            x,y,w,h=g['x'],g['y'],g['w'],g['h']
            out.append(f'<g class="scope" data-id="{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{COL["panel"]}" stroke="{COL["line"]}" stroke-width="1" stroke-dasharray="2 6"/><text x="{x+20}" y="{y+32}" font-size="22" font-weight="650" fill="{COL["ink"]}">{ESC(g["title"])}</text>')
            for i,line in enumerate(g['subtitle'].split('\n')):
                if line:out.append(f'<text x="{x+20}" y="{y+58+23*i}" font-size="17" fill="{COL["muted"]}">{ESC(line)}</text>')
            out.append('</g>')
        for i,e in enumerate(self.edges):
            color={'flow':COL['blue'],'data':COL['blue'],'apply':COL['gray'],'return':COL['yellow'],'blocked':COL['red']}[e['kind']]
            marker='' if e['kind']=='apply' else f' marker-end="url(#arrow-{e["kind"]})"'
            out.append(f'<path class="edge" data-id="e{i}" data-source="{e["source"]}" data-target="{e["target"]}" data-kind="{e["kind"]}" d="{self.poly(e["points"])}" fill="none" stroke="{color}" stroke-width="{1.7 if e["kind"]=="apply" else 2.5}"{marker}/>')
        for key,n in self.nodes.items():
            x,y,w,h=n['x'],n['y'],n['w'],n['h'];k=n['kind']
            fill,stroke,ink=('#e3edf9','#889fb9','#1c344d') if k=='action' else ('#edf0f4','#9aa8b7','#293d50')
            if k=='decision':fill,stroke,ink='#fff5c4','#d3b34c','#664e13'
            if k=='terminal':fill,stroke,ink='#dff6e7','#71b888','#174d2d'
            if k=='stop':fill,stroke,ink='#ffe6e5','#df8e8e','#7f252a'
            if k=='process':fill,stroke,ink='#d9eaff','#83a9d4','#183752'
            out.append(f'<g class="node" data-id="{key}" data-material="{ESC(n["name"]) if n["material"] else ""}" data-usage="{n.get("usage","")}"><title>{ESC(n["name"]+": "+n["note"])}</title>')
            if k=='decision':
                out.append(f'<path class="shape" d="M {x+w/2} {y} L {x+w} {y+h/2} L {x+w/2} {y+h} L {x} {y+h/2} Z" fill="{fill}" stroke="{stroke}"/>')
            elif k=='fork':out.append(f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" fill="{COL["ink"]}"/>')
            else:out.append(f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if k in ("terminal","stop") else 10}" fill="{fill}" stroke="{stroke}"/>')
            if n['material']:
                yy=y+26
                for line in n['title']:out.append(f'<text class="material-name" x="{x+15}" y="{yy}" font-size="21" font-weight="700" fill="{ink}">{ESC(line)}</text>');yy+=26
                yy+=1
                for line in n['body']:out.append(f'<text class="helper" x="{x+15}" y="{yy}" font-size="17" fill="{ink}">{ESC(line)}</text>');yy+=22
                out.append(f'<text class="usage-type" x="{x+w-13}" y="{y+h-10}" text-anchor="end" font-size="13" fill="#54687b">{n["usage"]}</text>')
            else:
                yy=y+(h-(len(n['title'])*25+len(n['body'])*22))/2+19
                for line in n['title']:out.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="20" font-weight="700" fill="{ink}">{ESC(line)}</text>');yy+=25
                for line in n['body']:out.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="17" fill="{ink}">{ESC(line)}</text>');yy+=22
            out.append('</g>')
        for i,e in enumerate(self.edges):
            if not e['label']:continue
            pts=e['points'];x,y=e['label_at'] or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
            lines=e['label'].split('\n');w=max(measure(t,17) for t in lines)+16;h=23*len(lines)+10
            out.append(f'<g class="edge-label" data-edge="e{i}"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="5" fill="{COL["bg"]}"/>')
            for j,line in enumerate(lines):out.append(f'<text x="{x}" y="{y-h/2+22+j*23}" text-anchor="middle" font-size="17" fill="{COL["yellow"] if e["kind"]=="return" else COL["ink"]}">{ESC(line)}</text>')
            out.append('</g>')
        for t in self.texts:
            out.append('<g class="annotation">')
            for i,l in enumerate(t['lines']):out.append(f'<text x="{t["x"]}" y="{t["y"]+i*t["leading"]}" font-size="{t["size"]}" font-weight="{t["weight"]}" text-anchor="{t["anchor"]}" fill="{t["color"]}">{ESC(l)}</text>')
            out.append('</g>')
        out+=['</g>', '<metadata id="usage-structure">'+ESC(json.dumps(self.__dict__,ensure_ascii=False))+'</metadata>','</svg>']
        return '\n'.join(out)

def inputs(d,y):
    # A resource panel is attached to the judgment that consumes its contents.
    x=60;w=840
    d.panel('INPUT',x,y,w,640,'판단에 가져오는 자료와 지식','아래 자료 중 이번 일에 필요한 것을 골라 현재 작업 정보에 넣음')
    names=['정보·자료 찾기','현재 값·상태 확인','못 찾음·없음 구분','적용 사례','참고 자료','재사용 자료','근거의 신뢰성·적합성','자료의 시점·버전','장기 기억','업무 지식','실전 경험·감각']
    ids,end=d.grid('input',names,x+20,y+90,w-40,3,scope='현재 작업 정보와 대안·전략 판단의 입력·근거',rowgap=18)
    d.groups['INPUT']['h']=end-y+45
    d.text(x+20,end+28,'자료가 부족하거나 적용 조건을 모르면 → 추가 확인 · 확보 불가이면 보류',16,color=COL['muted'])
    return y+d.groups['INPUT']['h']

def rules(d,y):
    x=950;w=910
    d.panel('RULES',x,y,w,640,'어느 담당이든 지켜야 하는 기준','아래 번호는 충돌할 때의 위계 · 실행 순서가 아님')
    # Legal relations and authority are resolved before the ranked rules.
    ids,e=d.grid('rule_source',['규칙·기준 원문','법·의무 기준'],x+20,y+90,w-40,2,scope='법적 관계·적용 범위·시점 확인')
    yy=e+44
    ranks=[('① 필수 의무·기본 원칙·승인된 보호 기준',['직업 윤리·의무','에이전트 기본 원칙']),('② 유효한 약속·필수 이용 규정',['계약·합의 조건','플랫폼·제출처 규정'])]
    for k,(label,names) in enumerate(ranks):
        d.text(x+20,yy-12,label,17,weight=600)
        ids,e=d.grid('rule_rank'+str(k),names,x+20,yy,w-40,2,scope=label)
        yy=e+42
    for col,(name,label) in enumerate([('조직 규칙','③'),('사용자 지정 규칙','④'),('표현 방식·스타일','⑤')]):
        cw=(w-76)/3
        d.text(x+20+col*(cw+18),yy-12,label,17,weight=600)
        h=d.material('rule_last'+str(col),name,x+20+col*(cw+18),yy,cw,kind='support',scope='규칙의 적용·우선순위')
    yy+=max(d.nodes['rule_last'+str(i)]['h'] for i in range(3))+32
    h=d.material('priority','규칙의 적용·우선순위',x+20,yy,w-40,note='법적 관계 → 충돌한 조항의 위계 판단 → 남는 조건도 함께 충족\n예외는 요건·결정 권한 확인 · 미해결은 사람의 결정 또는 보류',kind='action')
    d.groups['RULES']['h']=yy+h-y+20
    return y+d.groups['RULES']['h']

def build(mode):
    d=Drawing(mode)
    title={'solo':'단독 · 한 전문가가 재료를 조합해 끝까지 처리','orchestration':'오케스트레이션 · 전문가들이 나눠 맡고 결과를 합침','complex':'복합 · 서로 연결된 여러 건을 함께 조정'}[mode]
    d.groups['TITLE']={'title':title}
    d.text(60,52,title,32,weight=700)
    d.text(60,88,'파랑  결과·작업 전달     노랑  다시 확인·보완     빨강  차단·보류     회색선  자료·규칙·기반의 적용',18,color=COL['muted'])
    owner={'solo':'한 전문가','orchestration':'총괄','complex':'전체 총괄 · 각 건의 목표를 구별'}[mode]
    d.box('start','요청·변경·재개',60,125,250,kind='terminal')
    d.material('notice','먼저 알아채기',760,125,480,kind='support',scope='시작 신호')
    d.material('watch','변경 감시·반영',1320,125,540,kind='support',scope='시작 신호와 영향받은 결과의 재검증')
    top=max(d.nodes['notice']['y']+d.nodes['notice']['h'],d.nodes['watch']['y']+d.nodes['watch']['h'])+65
    d.panel('INTAKE',60,top,1800,250,owner+' · 요청과 완료 기준을 맞춤')
    ids,end=d.chainrow('intake',['시작 신호','업무별 정보','정보·자료 이해','지시·의도 파악','문제·목표·완료 조건'],80,top+65,1760,owner=owner)
    d.groups['INTAKE']['h']=end-top+24
    d.edge('start',ids[0],via=[(185,top-24),(d.port(ids[0],'t')[0],top-24)])
    # These are signal inputs, not extra processing starts.
    for key,yy in [('notice',top-40),('watch',top-20)]:d.edge(key,ids[0],'data',sa='l',sb='t',via=[(d.nodes[key]['x']-24,d.port(key,'l')[1]),(d.nodes[key]['x']-24,yy),(d.port(ids[0],'t')[0],yy)])
    y=end+78
    e1=inputs(d,y);e2=rules(d,y)
    y=max(e1,e2)+84
    # Actual judgment draws from the resource and rule panels above.
    d.panel('PLAN',60,y,930,390,owner+' · 쓸 방법과 작업을 정함','각 담당도 자기 작업마다 같은 판단을 수행 · 입력·권한은 담당별 분리')
    ids,pe=d.chainrow('plan',['현재 작업 정보','대안·전략 판단','업무 절차·실행 계획'],80,y+92,890,owner=owner)
    d.material('model','AI 모델',80,pe+45,420,kind='support',owner=owner,scope='대안·전략 판단과 뜻·내용의 판단·생성')
    d.material('risk','빠진 위험 확인',540,pe+45,430,kind='support',scope='접수·계획·접촉·실행·전달의 위험 확인')
    pend=max(d.nodes['model']['y']+d.nodes['model']['h'],d.nodes['risk']['y']+d.nodes['risk']['h'])
    d.groups['PLAN']['h']=pend-y+22
    d.edge('INPUT',ids[0],'apply',label='이번 판단의 입력·근거',label_at=(325,y-34))
    d.edge('model',ids[1],'apply',sa='t',sb='b')
    d.edge('risk',ids[2],'apply',sa='t',sb='b')
    # The goal enters the plan along the outside, not through every reference item.
    gy=top+d.groups['INTAKE']['h']+30
    d.edge('intake_4','plan_2',label='목표·완료 조건',sa='r',sb='r',via=[(1888,d.port('intake_4','r')[1]),(1888,y-45),(1008,y-45),(1008,d.port('plan_2','r')[1])],label_at=(1450,y-45))
    # Current rules / permissions jointly feed the safety check.
    d.panel('GUARD',1040,y,820,390,'실행 전에 허용 범위를 확인','자료 수신·위임·실행·재시도·재개마다 현재 조건으로 검사')
    ids,ge=d.grid('guard_input',['업무 권한','비용·위험 한도'],1060,y+92,780,2,scope='안전장치')
    d.material('safe','안전장치',1060,ge+42,780)
    gend=d.nodes['safe']['y']+d.nodes['safe']['h'];d.groups['GUARD']['h']=gend-y+22
    for k in ids:d.edge(k,'safe','apply',sa='b',sb='t')
    d.edge('priority','GUARD','apply',label='현재 적용 기준',label_at=(1520,y-33))
    y=max(pend,gend)+72
    # Capability and human decisions remain next to the gate they unblock.
    d.panel('CAPABILITY',60,y,930,245,'검증된 능력으로만 착수','첫 업무·검증 범위 밖·능력 변경이면 시험 · 실패한 판본은 실제 실행 금지')
    ids,ce=d.chainrow('cap',['시험 환경','업무 능력 시험'],80,y+88,890)
    d.groups['CAPABILITY']['h']=ce-y+22
    d.panel('HUMAN',1040,y,820,245,'사람의 판단이 필요한 부분','다섯 예외만 요청 · 조사·대안 비교·준비·검증을 마친 뒤 결정만 받음')
    ids,he=d.chainrow('human',['사람에게 넘기기','보고 주체 확인'],1060,y+88,780,notes={'보고 주체 확인':'답변자·권한·승인 대상 확인\n유효한 결정만 실행 조건에 반영'})
    d.groups['HUMAN']['h']=he-y+22
    y=max(ce,he)+78
    d.box('permit','능력·규칙·권한·한도가\n현재 작업을 허용하는가?',710,y,500,kind='decision')
    d.edge('plan_2','permit',label='작업·입출력·담당',sa='b',sb='t',via=[(d.port('plan_2','b')[0],d.groups['CAPABILITY']['y']-22),(1018,d.groups['CAPABILITY']['y']-22),(1018,y-30),(960,y-30)],label_at=(960,y-31))
    d.edge('CAPABILITY','permit','apply',sa='b',sb='l',label='통과한 수행 범위',label_at=(530,y+42))
    d.edge('GUARD','permit','apply',sa='l',sb='r',via=[(1015,d.port('GUARD','l')[1]),(1015,y-55),(1250,y-55),(1250,d.port('permit','r')[1])])
    d.edge('permit','human_0','blocked','미확인 · 사람의 결정 필요',sa='r',sb='b',via=[(1400,d.port('permit','r')[1]),(1400,he+26),(d.port('human_0','b')[0],he+26)],label_at=(1530,y+54))
    d.box('human_valid','유효한 결정을\n받았는가?',1460,y,320,kind='decision')
    d.edge('human_1','human_valid')
    d.box('human_stop','결정 미확정 · 해당 처리 보류',1450,y+225,390,body='불일치·거절·기한 종료\n이유·후속 담당·재개 조건 기록',kind='stop')
    d.edge('human_valid','human_stop','blocked','아니오',label_at=(1680,y+202))
    d.edge('human_valid','safe','return','예 · 확인한 결정으로 재검사',sa='r',sb='r',via=[(1880,d.port('human_valid','r')[1]),(1880,d.port('safe','r')[1])],label_at=(1650,he+45))
    d.box('permission_stop','허용되지 않은 작업 중단',80,y+90,500,body='위반·거절·해결 불가 · 이유와 후속 담당 기록',kind='stop')
    d.edge('permit','permission_stop','blocked','위반·해결 불가',sa='l',sb='r',label_at=(645,y+120))
    y+=d.nodes['permit']['h']+100
    # Scope is visible: these support materials belong to all work inside WORK.
    d.panel('RUNBASE',60,y,1800,225,'작업이 진행되는 동안 · 담당·건별로 계속 유지','아래 실행 구역 전체에 적용 · 자료·권한·상태는 분리하고 허용된 정보만 공유')
    baseids,be=d.grid('base',['분리 실행','현재 진행 상태','판단 근거 기록','운영 감시·복구','대기·후속 관리'],80,y+90,1760,5,scope='모든 담당의 전체 실행 구역',kind='support')
    d.groups['RUNBASE']['h']=be-y+22
    y=be+90
    # Each scenario has a different ownership structure, not a copy of one long flow.
    if mode=='solo':
        d.panel('COORD',60,y,1800,215,'한 전문가가 직접 처리','목표에서 정한 작업만 실행 · 앞 결과를 다음 입력으로 사용 · 필요한 순서는 계획에서 정함')
        ids,co=d.chainrow('coord',['작업 진행·연결','실행 제어','업무 도구·시스템'],80,y+90,1280,notes={'업무 도구·시스템':'도구를 쓰는 작업의 요청·응답 연결\n도구 없이 판단·생성하는 일도 있음'},owner='한 전문가')
        d.material('no_delegate','나눠 맡기기',1420,y+90,420,note='이 상황에서는 사용하지 않음\n한 전문가가 끝까지 담당',kind='support',owner='한 전문가',scope='단독 수행')
        co=max(co,d.nodes['no_delegate']['y']+d.nodes['no_delegate']['h'])
        d.groups['COORD']['h']=co-y+25
    else:
        who='총괄' if mode=='orchestration' else '전체 총괄 → 건별 총괄'
        d.panel('COORD',60,y,1800,215,who+' · 분담과 선행 조건을 조정','준비된 독립 작업은 동시 진행 · 필요한 결과·자원이 없으면 그 작업만 대기')
        ids,co=d.chainrow('coord',['나눠 맡기기','작업 진행·연결','실행 제어','업무 도구·시스템'],80,y+90,1760,notes={
            '나눠 맡기기':('각 전문가에게 목표·입력·권한 전달\n반환 조건·중간 교환·보완 담당 지정' if mode=='orchestration' else '건별 목표·권한·한도를 나눠 배정\n건별 총괄이 자기 전문가에게 재배정'),
            '작업 진행·연결':('전문가별 선행 결과·입력 확인\n준비된 작업만 착수' if mode=='orchestration' else '건 사이 선행 결과·공유 자원 확인\n막힌 건 외의 독립 작업은 계속'),
            '실행 제어':'각 담당의 함수·도구·AI 실행\n정해진 계산·조회는 AI 판단 생략',
            '업무 도구·시스템':'각 담당의 권한 안에서 요청\n실제 결과·오류·상태를 받음'},owner=who)
        d.groups['COORD']['h']=co-y+25
    d.edge('permit','COORD','flow','허용된 작업만 착수',via=[(960,d.nodes['permit']['y']+d.nodes['permit']['h']+32),(34,d.nodes['permit']['y']+d.nodes['permit']['h']+32),(34,y-30),(960,y-30)],label_at=(440,y-30))
    d.edges=[e for e in d.edges if not(e['target']==ids[-1] and e['source']==ids[-2])]
    d.edge(ids[-1],ids[-2],'apply',sa='l',sb='r',scope='도구를 쓰는 작업에만 요청·응답 연결')
    d.edge('RUNBASE','COORD','apply',label='상태·기록·분리·복구·대기 지원',label_at=(1310,y-34))
    y=co+70
    action_top=y
    action_end=actions(d,y,mode)
    d.edge('COORD','WORK','flow',label='작업 목적에 해당하는 갈래만 사용 · 미해당은 건너뜀',label_at=(960,y-30))
    y=action_end+75
    checks_end=checks(d,y,mode)
    # A failure is repaired where the affected task was assigned; completed work remains.
    target='permit'
    d.edge('repair',target,'return','문제 작업 재계획 → 현재 허용 범위부터 재검사',sa='l',sb='l',via=[(24,d.port('repair','l')[1]),(24,d.port(target,'l')[1])],label_at=(390,action_top-24))
    y=checks_end+85
    learn_end=learning(d,y)
    d.height=learn_end+70
    d.text(60,d.height-28,'상시: 해당 활동 동안 계속 적용   ·   단계별: 정한 시점에 사용·재확인   ·   조건부: 해당하면 사용, 불명확하면 먼저 확인',16,color=COL['muted'])
    # Every material is drawn and has a declared ownership / application context.
    assert set(n['name'] for n in d.nodes.values() if n['material'])==set(CAT)
    return d

def fork(d,key,x,y,w=220):
    d.nodes[key]=dict(id=key,name='준비된 작업의 분담',material=False,x=x,y=y,w=w,h=10,title=[],body=[],note='시작할 조건이 갖춰진 배정 작업만 분담',kind='fork')

def mat(d,key,name,x,y,w,owner,short=None):
    return d.material(key,name,x,y,w,note=short,owner=owner,scope='그림에 표시한 작업 목적에 해당하는 재료만 선택')

def tile(d,key,title,x,y,w,layout,arcs,owner,subtitle):
    d.panel(key,x,y,w,700,title,subtitle)
    cw=(w-60)/2;row=y+114;row_ids=[];ids={}
    for ri,items in enumerate(layout):
        if key=='LANE3' and ri==2:
            effect_top=row-18
            d.panel('EFFECTS',x+8,effect_top,w-16,400,'승인된 요청·내용 반영','아래 중 맡긴 처리만 선택')
            row+=64
        hs=[];new=[]
        for col,(name,short) in enumerate(items):
            k=f'{key}_{len(ids)}';ids[name]=k
            nodew=w-36 if len(items)==1 else cw
            hs.append(mat(d,k,name,x+18+col*(cw+24),row,nodew,owner,short));new.append(k)
        row_ids.append(new);row+=max(hs)+46
    # These arrows denote the stated input/output relationship, not compulsory
    # execution of every conditional item in the panel.
    for src,dst,label in arcs:
        a,c=ids[src],ids[dst];n,m=d.nodes[a],d.nodes[c]
        if n['y']==m['y']:
            d.edge(a,c,'data',label,sa='r' if n['x']<m['x'] else 'l',sb='l' if n['x']<m['x'] else 'r')
        else:
            # Route across the free band separating rows.
            yy=n['y']+n['h']+22
            d.edge(a,c,'data',label,via=[(d.port(a,'b')[0],yy),(d.port(c,'t')[0],yy)],label_at=((d.port(a,'b')[0]+d.port(c,'t')[0])/2,yy) if label else None)
    if key=='LANE3':
        # External effects are a choice, never four mandatory consecutive calls.
        d.text(x+18,row-19,'외부 반영은 위임·승인된 종류만 선택',15,color=COL['muted'])
        d.text(x+18,row+3,'각 요청의 실제 반영·미결 상태를 아래로 반환',15,color=COL['muted'])
        row+=40
        d.groups['EFFECTS']['h']=row-effect_top-30
    d.groups[key]['h']=row-y-22
    # The panel is an input/output operation, and its materials are its visible
    # optional composition. The boundary is explicitly labelled at both ends.
    d.groups[key]['subtitle']+='\n입력 → 해당 재료 조합 → 결과·상태'
    return row-22,ids

LAYOUTS=[
 [
  [('실험','조건을 바꿔 비교할 때\n차이·한계를 얻음'),('시뮬레이션','가정한 상황을 시험할 때\n예상 결과·가정을 얻음')],
  [('관찰·측정','새 기록·값이 필요할 때\n대상·조건과 함께 측정'),('자료 선별·분류','쓸 자료를 고를 때\n필요한 자료·관계를 추림')],
  [('자료 정리·결합','정리·결합이 필요할 때\n오류·중복을 고쳐 합침'),('형식·구조 변환','사용 형식이 다를 때\n내용·항목을 보존해 변환')]
 ],
 [
  [('계산','값·식을 구해야 할 때\n단위·가정을 밝혀 계산'),('분석','관계·원인을 밝힐 때\n자료·계산값을 해석')],
  [('예측','앞으로의 결과가 필요할 때\n예상·불확실성을 제시'),('조건 안에서 최선 찾기','한도 안에서 안을 고를 때\n효과·대가·이유를 비교')],
  [('기준 적용·판정','요건 충족 여부를 판단할 때\n사실·근거·예외와 대조해 결론을 냄')]
 ],
 [
  [('실시간 대화','바로 주고받을 때 통로 관리\n발언 순서·중단·재연결')],
  [('사람과 소통','질문·설명·확인이 필요할 때\n접촉 위험을 확인하고 답변·요구를 받음')],
  [('협상·조율','요구·이익·약속이 충돌할 때\n권한 안에서 합의·남은 쟁점을 정리')]
 ],
 [
  [('결과물 설계','구조·내용을 정할 때\n판단을 제작 명세로 바꿈'),('내용 재구성','요약·번역·표현 변경 때\n뜻·출처·예외를 유지')],
  [('결과물 만들기·수정','검증한 설계·입력을 제작·수정\n원본과 수정 범위·판본을 함께 관리')],
  [('기록 입력·수정','기록을 바꿀 때\n변경 이력·반영 확인'),('신청·거래 처리','신청·변경·취소를 맡을 때\n접수·확정·미결 확인')],
  [('설정·작동 제어','설정·작동을 바꿀 때\n반영·허용 범위 복구'),('게시·배포','공개·제공을 맡을 때\n판본·대상·반영 확인')]
 ]
]
ARCS=[
 [('실험','관찰·측정',''),('시뮬레이션','자료 선별·분류',''),('관찰·측정','자료 선별·분류',''),('자료 선별·분류','자료 정리·결합',''),('자료 정리·결합','형식·구조 변환','')],
 [('계산','분석',''),('분석','예측',''),('예측','조건 안에서 최선 찾기',''),('조건 안에서 최선 찾기','기준 적용·판정','')],
 [('실시간 대화','사람과 소통',''),('사람과 소통','협상·조율','')],
 [('결과물 설계','결과물 만들기·수정',''),('내용 재구성','결과물 만들기·수정','')]
]

SHORTS={'실험': '조건별 차이를 볼 때\n비교한 결과·한계', '시뮬레이션': '가정을 시험할 때\n예상 결과·한계', '관찰·측정': '값·기록이 필요할 때\n조건과 함께 측정', '자료 선별·분류': '자료를 골라 나눌 때\n필요한 자료·관계', '자료 정리·결합': '정리·결합할 때\n오류·중복 고쳐 합침', '형식·구조 변환': '형식이 다를 때\n뜻·항목 유지해 변환', '계산': '값·식이 필요할 때\n단위·가정과 계산', '분석': '관계·원인을 볼 때\n자료·계산값 해석', '예측': '미래를 예상할 때\n예상값·불확실성', '조건 안에서 최선 찾기': '한도 안에서 고를 때\n효과·대가·이유 비교', '결과물 설계': '구조·내용을 정할 때\n판단 → 제작 명세', '내용 재구성': '요약·번역·수정 때\n뜻·출처·예외 유지', '기록 입력·수정': '기록을 바꿀 때\n변경 이력·반영 확인', '신청·거래 처리': '신청·취소를 맡을 때\n접수·확정·미결 확인', '설정·작동 제어': '설정·작동을 바꿀 때\n반영 확인·허용 복구', '게시·배포': '공개·배포할 때\n판본·대상·반영 확인'}
for layout in LAYOUTS:
    for row in layout:
        for i,(name,note) in enumerate(row):
            row[i]=(name,SHORTS.get(name,note))

def actions(d,y,mode):
    iscomplex=mode=='complex'
    main={'solo':'한 전문가 안에서 필요한 재료를 조합','orchestration':'준비된 일을 여러 전문가가 나눠 수행','complex':'전체 총괄 아래에서 건별 총괄과 전문가들이 수행'}[mode]
    d.panel('WORK',60,y,1800,1600,main,'파랑은 결과를 넘겨 쓰는 연결 · 모든 재료를 차례로 실행하는 뜻이 아님\n각 재료에 적힌 조건에 해당할 때만 사용 · 실제 순서와 조합은 계획에서 정함')
    if mode!='solo':
        d.groups['WORK']['subtitle']+='\n아래는 역할 분담의 예 · 업무에 맞춰 담당을 늘리거나 합치고, 필요한 재료를 다시 조합'
    yy=y+125
    if mode=='solo':
        d.box('ready','이번 작업에 무엇이 필요한가?',770,yy,380,kind='decision')
    else:
        d.box('ready','배정된 작업 중 시작할 수 있는 일',620,yy,680,body='필요한 입력·권한·선행 결과가 준비된 일만 시작\n준비되지 않은 부분은 대기 · 독립된 부분은 동시 진행')
    yy+=d.nodes['ready']['h']+100
    if mode!='solo':
        fork(d,'fork',280,yy-55,1360);d.edge('ready','fork')
    # Every lane is owned. Complex scenarios have a second coordination level.
    if iscomplex:
        for j,(xx,case) in enumerate([(80,'건 A'),(980,'건 B')]):
            d.panel('CASE'+str(j),xx,yy,880,1500,case+' · 자기 목표와 완료 기준을 가진 업무','건별 총괄이 내부 전문가를 배정·회수 · 허용된 선행 결과와 자원만 다른 건과 공유')
            notes={'문제·목표·완료 조건':case+'의 목표·범위·완료 기준\n다른 건의 완료와 따로 판정','나눠 맡기기':case+' 총괄 → 담당 전문가\n목표·입력·권한·반환 조건 전달'}
            ids,e=d.chainrow('case'+str(j),['문제·목표·완료 조건','나눠 맡기기'],xx+18,yy+86,844,notes=notes,owner=case+' 총괄')
            d.edge('fork','case'+str(j)+'_0','flow',label=case+'의 준비된 작업',via=[(xx+220,yy-24)],label_at=(xx+220,yy-24))
            d.edges[-1]['points'][0]=(xx+220,yy-45)
        row=max(n['y']+n['h'] for k,n in d.nodes.items() if k.startswith('case') and k.endswith('_1'))+100
        for j,xx in enumerate([98,998]):
            fork(d,'case_fork'+str(j),xx+100,row-40,650)
            d.edge('case'+str(j)+'_1','case_fork'+str(j))
    else:row=yy
    titles={
      'solo':['자료를 얻고 다듬음','값과 이유를 밝혀 판단','사람에게 확인하고 조율','내용을 만들고 실제로 반영'],
      'orchestration':['자료를 맡은 전문가','판단을 맡은 전문가','소통을 맡은 전문가','제작·실행을 맡은 전문가'],
      'complex':['건 A · 자료 담당','건 A · 판단 담당','건 B · 소통 담당','건 B · 제작·실행 담당']}[mode]
    cols=[98,530,998,1430] if iscomplex else [80,525,970,1415]
    cw=414 if iscomplex else 425
    endlist=[]
    for col,(xx,title) in enumerate(zip(cols,titles)):
        key='LANE'+str(col)
        subtitle=['얻은 값·자료를 가공해 전달','자료·계산값을 판단의 근거로','접촉 전 위험·허용 범위 확인','설계 검증 후 제작 · 반영 직전 승인 검사'][col]
        end,ids=tile(d,key,title,xx,row,cw,LAYOUTS[col],ARCS[col],title,subtitle)
        endlist.append(end)
        d.groups[key]['kind']='lane'
        if mode=='solo':
            d.edge('ready',key,'flow',label=['자료 작업','판단 작업','소통 작업','제작·반영 작업'][col],via=[(960+(col-1.5)*55,row-28-col*7),(xx+cw/2,row-28-col*7)],label_at=(xx+cw/2,row-27-col*7))
            # Separate exits on the diamond, never a branching dot on a wire.
            n=d.nodes['ready'];dx=(col-1.5)*55
            d.edges[-1]['points'][0]=(960+dx,n['y']+n['h']-abs(dx)*n['h']/n['w'])
        elif not iscomplex:
            d.edge('fork',key,'flow',label=['자료 담당','판단 담당','소통 담당','제작·실행 담당'][col],label_at=(xx+cw/2,row-25))
            d.edges[-1]['points']=[(xx+cw/2,yy-45),d.port(key,'t')]
        else:
            a='case_fork'+str(col//2);d.edge(a,key,'flow')
            d.edges[-1]['points']=[(xx+cw/2,row-30),d.port(key,'t')]
    end=max(endlist)
    for col in range(4):
        # Equal output baselines make collection visible without extra detours.
        d.groups['LANE'+str(col)]['h']=end-row
        xx=cols[col]
        d.box('out'+str(col),['가공한 자료·출처','판단·계산·근거','답변·합의·미합의','결과물·반영 상태'][col],xx+18,end+25,cw-36,body='완료·실패·미확인 구별')
        d.edge('LANE'+str(col),'out'+str(col),'flow')
    outend=max(d.nodes['out'+str(i)]['y']+d.nodes['out'+str(i)]['h'] for i in range(4))
    if iscomplex:
        for j,(xx,case) in enumerate([(80,'건 A'),(980,'건 B')]):
            d.material('case_collect'+str(j),'나눠 맡기기',xx+18,outend+55,844,note=case+' 총괄 · 시작한 내부 작업의 결과·상태를 모두 회수\n빠진 결과·이견·실패를 구별하고 미완료의 담당·기한 유지',owner=case+' 총괄')
            for k in [j*2,j*2+1]:d.edge('out'+str(k),'case_collect'+str(j),'flow',via=[(d.port('out'+str(k),'b')[0],outend+27),(d.port('case_collect'+str(j),'t')[0],outend+27)])
            d.groups['CASE'+str(j)]['h']=outend+55+d.nodes['case_collect'+str(j)]['h']+22-yy
        outend=max(d.nodes['case_collect'+str(j)]['y']+d.nodes['case_collect'+str(j)]['h'] for j in range(2))
    joiny=outend+90
    d.box('join',{'solo':'이번 작업의 결과·상태를 모음','orchestration':'총괄이 시작한 모든 담당의 결과·상태를 회수','complex':'전체 총괄이 건별 결과·상태를 함께 확인'}[mode],600,joiny,720,body='완료·실패·보류·미응답을 구별 · 누락·중복·이견 확인')
    for j in range(2 if iscomplex else 4):
        src='case_collect'+str(j) if iscomplex else 'out'+str(j)
        d.edge(src,'join','flow',via=[(d.port(src,'b')[0],joiny-35),(960,joiny-35)])
    d.text(82,joiny+20,'다음 작업에 넘길 내용',19,weight=700)
    d.text(82,joiny+47,'자료 → 판단의 입력\n판단·합의 → 제작·실행의 조건\n바뀐 사실·조건 → 관련 작업 재검토',16,color=COL['muted'])
    d.text(1390,joiny+20,'전달 전에 반드시 확인',19,weight=700)
    d.text(1390,joiny+47,'주체·권한·근거·판본·선행 조건\n미확인·무효이면 후속 작업 대기\n공유 자원·한도 충돌도 전체 계획에서 조정',16,color=COL['muted'])
    bottom=joiny+d.nodes['join']['h']+42
    d.groups['WORK']['h']=bottom-y
    return bottom

def checks(d,y,mode):
    d.panel('CHECK',60,y,1800,1500,{'solo':'검사한 결과를 다음 작업 또는 인수로 연결','orchestration':'총괄이 검증한 중간 결과를 다음 전문가에게 연결','complex':'검증한 결과만 다른 건의 선행 조건으로 넘김'}[mode],'중간 결과와 최종 결과를 모두 검사 · 일부 성공·미응답·외부 처리 중을 전체 완료로 보지 않음')
    ids,ce=d.chainrow('check',['보고 주체 확인','결과 검증·재검증','결과 품질 평가'],80,y+130,1160)
    d.material('opposing','반대 근거·다시 확인',1280,y+130,560,kind='support',scope='결과 검증·재검증')
    d.material('process_quality','일하는 과정 평가',1280,y+130+d.nodes['opposing']['h']+24,560,kind='support',scope='결과 품질 평가')
    d.edge('join','check_0','flow','담당별 결과·상태',label_at=(450,y-33))
    d.edge('opposing','check_1','apply',sa='l',sb='b',via=[(1260,d.port('opposing','l')[1]),(1260,ce+25),(d.port('check_1','b')[0],ce+25)])
    d.edge('process_quality','check_2','apply',sa='l',sb='b',via=[(d.port('check_2','b')[0],d.port('process_quality','l')[1])])
    yy=max(ce+85,d.nodes['process_quality']['y']+d.nodes['process_quality']['h']+50)
    d.box('verdict','확인한 결과는?',790,yy,340,kind='decision')
    d.edge('check_2','verdict',via=[(d.port('check_2','b')[0],yy-28),(960,yy-28)])
    d.material('repair','업무 절차·실행 계획',80,yy+30,540,note=('문제 있는 작업·영향받은 결과만 보완\n같은 전문가가 결과·방법·작업 순서를 다시 정함\n완료분 보존 · 바뀐 조건·권한 재확인' if mode=='solo' else '문제 있는 작업·영향받은 결과만 보완\n결과는 담당이 보완 · 방법·분담은 총괄이 재계획\n완료분 보존 · 바뀐 조건·권한 재확인'))
    d.edge('verdict','repair','blocked','문제 있음',sa='l',sb='r',label_at=(710,yy+95))
    d.material('pending','대기·후속 관리',1280,yy+30,560,note='미확인 결과·외부 처리의 원래 상태 조회\n답변·기한·후속 담당 유지 · 임의로 성공 처리·재실행 금지')
    d.edge('verdict','pending','blocked','미확인',sa='r',sb='l',label_at=(1200,yy+95))
    yy+=max(d.nodes[k]['h']+30 for k in ['verdict','repair','pending'])+75
    d.box('nextwork','이어 할 작업이\n남아 있는가?',780,yy,360,kind='decision')
    d.edge('verdict','nextwork','flow','문제없음',label_at=(960,yy-38))
    handnote={
      'solo':'검증한 결과·근거를 같은 전문가의 다음 입력으로\n자료 → 판단 · 판단·합의 → 제작·반영\n바뀐 조건·규칙·권한도 갱신',
      'orchestration':'검증한 결과·근거를 다음 담당에게 전달\n자료 담당 → 판단 담당 → 제작 담당 등 계획에 따라 연결\n받는 담당의 권한·입력·선행 조건 재확인',
      'complex':'허용된 결과·근거·판본을 받는 건의 총괄에게 전달\n건 A 결과 → 건 B 선행 입력 등 건 사이 연결\n건별 권한·공유 자원·예약분·의존 조건을 재확인'}[mode]
    d.material('handoff','현재 작업 정보',80,yy+30,540,note=handnote,owner='다음 작업의 담당 또는 받는 건의 총괄')
    d.edge('nextwork','handoff','flow','예 · 다음 입력',sa='l',sb='r',label_at=(690,yy+95))
    d.box('wait_result','기다린 결과는?',1400,yy,320,kind='decision')
    d.edge('pending','wait_result')
    d.edge('wait_result','check_1','return','확인됨 · 재검증',sa='r',sb='t',via=[(1880,d.port('wait_result','r')[1]),(1880,y+72),(d.port('check_1','t')[0],y+72)],label_at=(1600,y+72))
    d.edge('wait_result','pending','return','아직 대기',sa='l',sb='l',via=[(1260,d.port('wait_result','l')[1]),(1260,d.port('pending','l')[1])],label_at=(1250,yy-32))
    # Returned results always pass the current gate; the dispatcher then selects
    # only the affected/next task, not every material again.
    d.edge('handoff','permit','return','갱신한 입력으로 다음 작업 허용 여부 재검사',sa='l',sb='b',via=[(42,d.port('handoff','l')[1]),(42,d.nodes['permit']['y']+d.nodes['permit']['h']+52),(d.port('permit','b')[0],d.nodes['permit']['y']+d.nodes['permit']['h']+52)],label_at=(530,d.nodes['permit']['y']+d.nodes['permit']['h']+52))
    yy+=max(d.nodes[k]['h']+30 for k in ['nextwork','handoff','wait_result'])+85
    d.box('hold','이번 처리 보류',1330,yy,510,body='거절·기한 종료·해결 불가\n이유·남은 일·후속 담당·재개 조건 유지',kind='stop')
    d.edge('wait_result','hold','blocked','기한 종료·거절',label_at=(1580,yy-35))
    ids,de=d.chainrow('delivery',['납품 준비','전달·인수 확인'],80,yy,1160)
    d.edge('nextwork','delivery_0','blocked','아니오 · 최종 결과 인계',via=[(960,yy-42),(d.port('delivery_0','t')[0],yy-42)],label_at=(780,yy-42))
    yy=max(de,d.nodes['hold']['y']+d.nodes['hold']['h'])+65
    d.box('received','인수 결과는?',740,yy,350,kind='decision')
    d.edge('delivery_1','received')
    d.material('receipt_wait','대기·후속 관리',1320,yy+12,520,note='미응답이면 수령·사용 가능 여부 확인\n반려·수정 요청이면 영향받은 결과 재검증\n기한 종료는 남은 일·담당을 기록해 보류')
    d.edge('received','receipt_wait','blocked','미응답',sa='r',sb='l',label_at=(1200,yy+88))
    d.edge('received','check_1','return','반려·수정 요청',sa='r',sb='t',via=[(1895,d.port('receipt_wait','r')[1]),(1895,y+12),(d.port('check_1','t')[0]+90,y+12)],label_at=(1560,y+12))
    d.edges[-1]['points'][-1]=(d.port('check_1','t')[0]+90,d.port('check_1','t')[1])
    d.edge('received','hold','blocked','거절·기한 종료',sa='r',sb='l',label_at=(1235,yy-32))
    d.edge('receipt_wait','received','return','후속 확인',sa='b',sb='r',label_at=(1550,yy+195))
    end=yy+d.nodes['received']['h']+28;d.groups['CHECK']['h']=end-y
    return end

def learning(d,y):
    d.panel('LEARN',60,y,1800,600,'실제 성과로 배우고, 시험한 개선만 다음 업무에 적용','계획 때 정한 성과 항목·시점으로 확인 · 실패·보류와 나중에 드러난 문제도 학습에 포함')
    d.material('learn_0','성과 추적',80,y+90,380)
    d.box('learn_needed','재사용할 성과·개선할\n문제가 있는가?',500,y+90,300,kind='decision')
    d.material('learn_1','성공·실패 원인 분석',850,y+90,470)
    d.material('learn_2','능력 개선·확장',1370,y+90,470)
    d.edge('received','learn_0','flow','인수 확인 · 후속 성과',label_at=(930,y-32))
    d.edge('learn_0','learn_needed',sa='r',sb='l')
    d.edge('learn_needed','learn_1','flow','예',sa='r',sb='l')
    d.edge('learn_1','learn_2',sa='r',sb='l')
    yy=max(d.nodes[k]['y']+d.nodes[k]['h'] for k in ['learn_0','learn_needed','learn_1','learn_2'])+80
    d.material('learn_env','시험 환경',80,yy,400,note='새 방식과 기존 능력을 비교할\n격리·재현 조건을 준비')
    d.material('learn_test','업무 능력 시험',530,yy,400,note='개선 효과와 기존 능력 유지 확인\n실패한 판본은 실제 업무에 쓰지 않음')
    d.box('test_passed','새 방식이 시험을\n통과했는가?',980,yy,300,kind='decision')
    d.material('remember','장기 기억',1330,yy,510,note='검증한 교훈·결정·조건을 저장\n확인된 지식·방법의 갱신에 연결')
    d.edge('learn_2','learn_env','flow','개선안과 비교 기준',sa='b',sb='t',via=[(d.port('learn_2','b')[0],yy-35),(280,yy-35)],label_at=(960,yy-35))
    d.edge('learn_env','learn_test',sa='r',sb='l')
    d.edge('learn_test','test_passed',sa='r',sb='l')
    d.edge('test_passed','remember','flow','예',sa='r',sb='l')
    yy=max(d.nodes[k]['y']+d.nodes[k]['h'] for k in ['learn_env','learn_test','test_passed','remember'])+80
    d.box('keep','기존 방식 유지',420,yy,460,body='개선할 필요가 없거나 새 방식이 검증되지 않음')
    d.box('finish','이번 처리 종료',1230,yy,610,body='남은 약속·후속 확인은 담당·시점을 유지',kind='terminal')
    d.edge('learn_needed','keep','blocked','아니오',sa='b',sb='l',via=[(650,d.nodes['learn_needed']['y']+d.nodes['learn_needed']['h']+22),(35,d.nodes['learn_needed']['y']+d.nodes['learn_needed']['h']+22),(35,d.port('keep','l')[1])],label_at=(200,yy+38))
    d.edge('test_passed','keep','blocked','아니오',sa='b',sb='t',via=[(1130,yy-32),(650,yy-32)],label_at=(1070,yy-32))
    d.edge('keep','finish',sa='r',sb='l')
    d.edge('remember','finish')
    end=yy+max(d.nodes['keep']['h'],d.nodes['finish']['h'])+26
    d.groups['LEARN']['h']=end-y
    return end

def finish_design(d):
    gate=d.nodes['permit'];bottom=gate['y']+gate['h']
    for e in d.edges:
        pair=(e['source'],e['target'])
        if e['target']=='intake_0':
            # Enter the complete intake panel; its first row shows the local order.
            e['target']='INTAKE';end=d.port('INTAKE','t')
            a=d.port(e['source'],'b');yy=d.groups['INTAKE']['y']-20
            e['points']=[a,(a[0],yy),(end[0],yy),end]
        elif pair==('INPUT','plan_0'):
            a=d.port('INPUT','b');end=d.port('plan_0','l');yy=d.groups['PLAN']['y']-34
            e['points']=[a,(a[0],yy),(70,yy),(70,end[1]),end]
        elif pair==('join','check_0'):
            a=d.port('join','b');end=d.port('check_0','l');yy=d.groups['CHECK']['y']-16
            e['points']=[a,(a[0],yy),(70,yy),(70,end[1]),end]
        elif e['source']=='fork' and e['target'].startswith('case'):
            j=e['target'][4];e['target']='CASE'+j;end=d.port(e['target'],'t');a=(end[0],d.port('fork','b')[1])
            e['points']=[a,end];e['label_at']=((a[0]+end[0])/2,(a[1]+end[1])/2)
        elif pair==('intake_4','plan_2'):
            a=d.port('intake_4','b');end=d.port('plan_2','t');yy=d.groups['INPUT']['y']-35
            e['points']=[a,(a[0],yy),(925,yy),(925,end[1]-35),(end[0],end[1]-35),end]
            e['label_at']=(1280,yy)
        elif pair==('plan_2','permit'):
            a=d.port('plan_2','r');end=d.port('permit','t');x=1018
            e['points']=[a,(x,a[1]),(x,end[1]-30),(end[0],end[1]-30),end]
        elif pair==('CAPABILITY','permit'):
            a=d.port('CAPABILITY','b');end=d.port('permit','t')
            e['points']=[a,(a[0],end[1]-45),(end[0]-100,end[1]-45),(end[0]-100,end[1]+55)]
            e['label_at']=(470,end[1]-45)
        elif pair==('GUARD','permit'):
            a=d.port('GUARD','l');end=(1060,gate['y']+gate['h']*.2)
            e['points']=[a,(1030,a[1]),(1030,gate['y']-60),(end[0],gate['y']-60),end]
        elif pair==('permit','COORD'):
            a=d.port('permit','b');end=d.port('COORD','t',40)
            e['points']=[a,(a[0],bottom+72),(1908,bottom+72),(1908,end[1]-55),(end[0],end[1]-55),end]
            e['label_at']=(1570,bottom+72)
        elif pair==('human_valid','safe'):
            e['label']='예';e['label_at']=(1830,d.port('human_valid','r')[1])
        elif pair==('permit','human_0'):
            e['label']='사람의 결정 필요';e['label_at']=(1300,gate['y']+gate['h']/2)
        elif pair==('handoff','permit'):
            a=d.port('handoff','l');end=(835,gate['y']+gate['h']*.75)
            e['points']=[a,(24,a[1]),(24,bottom+24),(835,bottom+24),end]
            e['label']='다음 작업 · 현재 조건 재검사';e['label_at']=(450,bottom+24)
        elif pair==('repair','permit'):
            a=d.port('repair','l');end=(900,gate['y']+gate['h']*.88)
            e['points']=[a,(42,a[1]),(42,bottom+64),(900,bottom+64),end]
            e['label']='보완 작업 · 현재 조건 재검사';e['label_at']=(450,bottom+64)
        elif e['source']=='ready' and e['target'].startswith('LANE'):
            col=int(e['target'][-1]);a=e['points'][0];end=d.port(e['target'],'t');yy=end[1]-(60 if col in [0,3] else 28)
            e['points']=[a,(a[0],yy),(end[0],yy),end];e['label_at']=(end[0],yy)
        elif pair==('opposing','check_1'):
            a=d.port('opposing','l');end=(800,d.nodes['check_1']['y']);yy=end[1]-8
            e['points']=[a,(1260,a[1]),(1260,yy),(end[0],yy),end]
        elif pair==('process_quality','check_2'):
            a=d.port('process_quality','l');end=d.port('check_2','r',20)
            e['points']=[a,(1250,a[1]),(1250,end[1]),end]
        elif pair==('wait_result','check_1'):
            a=d.port('wait_result','r');end=(750,d.nodes['check_1']['y']);yy=d.groups['CHECK']['y']+110
            e['label_at']=(1600,yy)
            e['points']=[a,(1880,a[1]),(1880,yy),(end[0],yy),end]
        elif pair==('received','check_1'):
            n=d.nodes['received'];a=(n['x']+n['w']*.75,n['y']+n['h']*.75);end=(600,d.nodes['check_1']['y']);yy=d.groups['CHECK']['y']+78
            e['label_at']=(1000,yy)
            e['points']=[a,(a[0],n['y']+n['h']+16),(1895,n['y']+n['h']+16),(1895,yy),(end[0],yy),end]
            e['label']='반려·수정 요청 · 재검증'
        elif pair==('received','hold'):
            n=d.nodes['received'];a=(n['x']+n['w']*.75,n['y']+n['h']*.25);end=d.port('hold','l')
            e['points']=[a,(1250,a[1]),(1250,end[1]),end];e['label_at']=(1250,n['y']-30)
        elif pair==('receipt_wait','received'):
            n=d.nodes['received'];a=d.port('receipt_wait','b');end=(n['x']+n['w']/2+125,n['y']+n['h']/2+n['h']*(.5-125/n['w']))
            e['points']=[a,(a[0],a[1]+20),(1200,a[1]+20),(1200,end[1]),end]
            e['label_at']=(1480,a[1]+20)
        elif pair==('received','learn_0'):
            a=d.port('received','b');end=d.port('learn_0','l');yy=d.groups['LEARN']['y']-18
            e['points']=[a,(a[0],yy),(70,yy),(70,end[1]),end]
    return d


def enrich(d):
    for key,n in d.nodes.items():
        containers=[]
        for group,g in d.groups.items():
            if group=='TITLE': continue
            if g['x']<=n['x'] and g['y']<=n['y'] and g['x']+g['w']>=n['x']+n['w'] and g['y']+g['h']>=n['y']+n['h']:
                containers.append(group)
        containers.sort(key=lambda k:d.groups[k]['w']*d.groups[k]['h'])
        n['containers']=containers
        if n['material']:
            n['canonical_condition']=CAT[n['name']]['condition']
            n['owner']=n.get('owner') or (d.groups[containers[0]]['title'] if containers else '전체 사용 구조')
            n['scope']=n.get('scope') or ((d.groups[containers[0]]['subtitle'] or d.groups[containers[0]]['title']) if containers else n['note'])
    d.source_prefix_sha256=hashlib.sha256(PREFIX.encode()).hexdigest()
    d.meanings={'flow':'작업·결과 전달','data':'그 결과를 입력으로 사용','return':'이전 판단·검사에 다시 연결','blocked':'미확인·아니오·중단 조건','apply':'자료·규칙·기반이 적용되는 대상','containment':'공통 담당·목적·입출력을 가진 재료의 구성; 실행 순서를 뜻하지 않음'}
    return d


def polish(d):
    """Remove duplicate chrome and compress only empty vertical space."""
    titles={'INTAKE':'요청·완료 기준','INPUT':'자료·지식','RULES':'적용 기준과 우선순위','PLAN':'방법·작업 선택','GUARD':'실행 전 확인','CAPABILITY':'수행 능력 확인','HUMAN':'사람의 결정','RUNBASE':'전 과정에 적용','COORD':{'solo':'한 전문가의 실행','orchestration':'총괄의 배정·연결','complex':'전체 총괄의 배정·연결'}[d.mode],'WORK':{'solo':'필요한 재료의 조합','orchestration':'전문가별 수행 · 분담 예','complex':'건별 수행 · 분담 예'}[d.mode],'CHECK':'검증·후속 작업','LEARN':'성과·학습','EFFECTS':'외부 반영','CASE0':'건 A · 건별 총괄','CASE1':'건 B · 건별 총괄'}
    subtitles={'RULES':'법적 관계 먼저 · 아래 위계는 규칙이 충돌할 때 적용','GUARD':'수신·위임·실행·재시도·재개마다 확인','WORK':'해당하는 재료만 사용 · 연결은 결과를 다음 입력으로 쓰는 관계','EFFECTS':'승인받은 처리만 선택','CHECK':'중간 결과와 최종 결과를 모두 확인','LEARN':'완료·실패·보류 기록으로 평가'}
    for k,g in d.groups.items():
        if k=='TITLE':continue
        g['scope_note']=g['subtitle']
        g['title']=titles.get(k,g['title']);g['subtitle']=subtitles.get(k,'')
        if k.startswith('LANE'):
            i=int(k[-1]);purpose=['자료 확보·가공','계산·판단','소통·조율','제작·반영'][i]
            g['title']=purpose if d.mode=='solo' else (['자료 전문가','판단 전문가','소통 전문가','제작·실행 전문가'][i] if d.mode=='orchestration' else ('건 A · ' if i<2 else '건 B · ')+purpose)
    # Keep only the rule hierarchy and the consequential missing-evidence condition.
    d.texts=[t for t in d.texts if t['text'].startswith(('①','②','③','④','⑤','자료가 부족'))]
    # These compact condition labels carry their own meaning; no page footer needed.
    d.decoration_removed=['visible document title','repeated subtitles','footer legend']
    busy=[]
    for n in d.nodes.values():busy.append((n['y']-12,n['y']+n['h']+12))
    for g in d.groups.values():
        if 'y' in g:busy.append((g['y'],g['y']+40+(24 if g['subtitle'] else 0)))
    for t in d.texts:busy.append((t['y']-t['size']-5,t['y']+(len(t['lines'])-1)*t['leading']+8))
    for e in d.edges:
        for a,b in zip(e['points'],e['points'][1:]):
            if a[1]==b[1]:busy.append((a[1]-12,a[1]+12))
        if e['label']:
            pts=e['points'];x,y=e['label_at'] or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
            hh=23*len(e['label'].split('\n'))+10;busy.append((y-hh/2-8,y+hh/2+8))
    busy.sort();merged=[]
    for a,z in busy:
        if merged and a<=merged[-1][1]:merged[-1][1]=max(z,merged[-1][1])
        else:merged.append([a,z])
    cuts=[(0,max(0,merged[0][0]-20))]
    for (_,left),(right,_) in zip(merged,merged[1:]):
        if right-left>32:cuts.append((left+16,right-16))
    def yy(y):return y-sum(max(0,min(y,z)-a) for a,z in cuts if y>a)
    for n in d.nodes.values():
        end=yy(n['y']+n['h']);n['y']=yy(n['y']);n['h']=end-n['y']
    for g in d.groups.values():
        if 'y' in g:end=yy(g['y']+g['h']);g['y']=yy(g['y']);g['h']=end-g['y']
    for t in d.texts:t['y']=yy(t['y'])
    for e in d.edges:
        e['points']=[(x,yy(y)) for x,y in e['points']]
        if e['label_at']:e['label_at']=(e['label_at'][0],yy(e['label_at'][1]))
    d.height=max(n['y']+n['h'] for n in d.nodes.values())+42
    return d

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'docs/images/expert-definition')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    drawings={}
    for mode in ('solo','orchestration','complex'):
        d=polish(enrich(finish_design(build(mode))))
        path=args.out/f'usage-structure-{mode}.svg'
        path.write_text(d.svg())
        drawings[mode]=d.__dict__
        print(f'{mode}: {len(set(n["name"] for n in d.nodes.values() if n["material"]))}/79 materials; {len(d.nodes)} nodes')
    model={'schema_version':1,'catalog':CAT,'diagrams':drawings}
    (ROOT/'docs/도식/사용-구조-원본.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
