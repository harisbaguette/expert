#!/usr/bin/env python3
"""A single material/data/control map. Canonical material names come from the document.

The selected operation produces a typed result. That result is checked and returned
to the current context before another operation is selected. The operation palette
is thus an executable branch of the graph, not an unconnected material catalogue.
"""
from pathlib import Path
from collections import Counter
import ast, bisect, hashlib, html, json, math, re

ROOT=Path(__file__).resolve().parents[2]
PREFIX=(ROOT/'전문가 에이전트 정의.md').read_text().split('## 사용 구조',1)[0]
formula_tree=ast.parse((ROOT/'docs/전개-수식/전개-수식-gen.py').read_text())
TERM_SYSTEMS=next(ast.literal_eval(n.value) for n in formula_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TERM_SYSTEMS' for t in n.targets))
SYSTEM_TERM={s:term for term,systems in TERM_SYSTEMS.items() for s in systems}
CAT={};current_system=''
for line in PREFIX.split('## 계통별 재료',1)[1].splitlines():
    if line.startswith('### '):current_system=line[4:].replace('✅','').strip()
    if line.startswith('| **') and '✅' in line:
        c=[s.strip() for s in line.strip('|').split('|')]
        if len(c)==6:
            n=re.search(r'\*\*(.*?)\*\*',c[0])[1]
            CAT[n]=dict(name=n,definition=c[2],usage=c[4].strip('*'),condition=c[5],system=current_system,term=SYSTEM_TERM[current_system])
assert len(CAT)==79
W=1800
C=dict(ink='#192C36',muted='#526773',blue='#228DE1',red='#D95750',yellow='#E3A512',
       pale='#E8F5FE',border='#CADFE9',green='#E7F5E9',white='#FFFFFF')
N={};E=[];G=[];A=[]
esc=lambda s:html.escape(str(s),quote=True)
def measure(s,z):return sum(z*(.97 if ord(c)>255 else .28 if c==' ' else .53) for c in s)
def wrap(s,w,z):
    rows=[]
    for p in s.split('\n'):
        row=''
        for word in p.split(' '):
            if row and measure(row+' '+word,z)>w:rows.append(row);row=word
            else:row+=(' ' if row else '')+word
        rows.append(row)
    return rows
def node(k,title,x,y,w=360,h=110,body='',kind='process',material=None):
    if material is None and title in CAT:material=title
    if material:assert material in CAT
    N[k]=dict(id=k,title=title,x=x,y=y,w=w,h=h,body=body,kind=kind,material=material)
    return k
def mat(k,name,x,y,w=360,h=110,body='',kind='process'):
    return node(k,name,x,y,w,h,body,kind,name)
def note(x,y,s,z=22,weight=500,color=None,anchor='start'):
    A.append(dict(x=x,y=y,text=s,size=z,weight=weight,color=color or C['muted'],anchor=anchor))
def group(k,x,y,w,h,title='',desc=''):
    G.append(dict(id=k,x=x,y=y,w=w,h=h,title=title,desc=desc))
def p(k,s='b',off=0):
    n=N[k] if k in N else next(g for g in G if g['id']==k)
    x,y,w,h=(n[t] for t in ('x','y','w','h'))
    return dict(t=(x+w/2+off,y),b=(x+w/2+off,y+h),l=(x,y+h/2+off),r=(x+w,y+h/2+off))[s]
def edge(a,b,label='',kind='flow',sa='b',sb='t',via=None,at=None,po=0,qi=0):
    start,end=p(a,sa,po),p(b,sb,qi) if b in N else (0,0)
    if via is None:
        if start[0]==end[0] or start[1]==end[1]:via=[]
        elif sa in ('l','r') and sb in ('l','r'):
            mid=(start[0]+end[0])/2;via=[(mid,start[1]),(mid,end[1])]
        else:
            mid=(start[1]+end[1])/2;via=[(start[0],mid),(end[0],mid)]
    E.append(dict(source=a,target=b,label=label,kind=kind,points=[start,*via,end],at=at))
def rowfan(source,keys,target,top,bottom,labels=None):
    # Strictly ordered fans: separate ports and straight segments, no shared bus.
    for i,k in enumerate(keys):
        off=(i-(len(keys)-1)/2)*28
        edge(source,k,(labels or ['']*len(keys))[i],po=off,via=[(p(source,'b',off)[0],top),(p(k,'t')[0],top)],at=(p(k,'t')[0],top+19) if labels else None)
        edge(k,target,via=[(p(k,'b')[0],bottom),(p(target,'t',off)[0],bottom)],qi=off)

# Request, interpretation and a concrete completion criterion.
node('start','한 건의 요청·재개',730,40,340,68,kind='terminal')
mat('signal','시작 신호',710,158,380,105,body='새 요청·변경·답변을\n해당 건에 연결')
edge('start','signal')
mat('early','먼저 알아채기',100,355,410,110,body='감시를 맡았다면\n문제·기회와 대응 이유를 발견')
mat('change','변경 감시·반영',100,550,410,120,body='추적할 변화가 생기면\n바뀐 근거와 영향받은 결과를 알림')
node('watch','상황 감시를 맡은 동안',120,40,370,68,kind='terminal')
node('watchtype','어떤 신호인가?',145,160,320,145,kind='decision')
edge('watch','watchtype')
edge('watchtype','early','새 문제·기회',at=(305,330))
edge('watchtype','change','기존 조건 변화',sa='l',sb='l',via=[(70,232.5),(70,610)],at=(145,510))
edge('early','signal','발견한 일',sa='r',sb='l',via=[(565,410),(565,210.5)],at=(600,270))
edge('change','signal','해당 건 재검토',sa='r',sb='l',via=[(620,610),(620,238.5)],qi=28,at=(615,530))
mat('case','업무별 정보',710,330,380,110,body='요청·대상·기한·상황과\n새로 들어온 자료를 모음')
edge('signal','case')
mat('understand','정보·자료 이해',710,510,380,110,body='자료의 내용·맥락을 읽어\n사실·주장·불명확한 점을 구별')
edge('case','understand','요청과 자료',at=(900,474))
mat('intent','지시·의도 파악',710,690,380,110,body='원하는 결과와 맡긴 범위를 파악\n해석에 따라 범위가 달라지면 확인')
edge('understand','intent','자료가 말하는 내용',at=(900,658))
mat('communicate0','사람과 소통',1270,690,410,110,body='범위를 바꾸는 모호함이 있으면\n구체적으로 묻고 답을 확인')
edge('intent','communicate0','확인이 필요할 때',sa='r',sb='l',at=(1180,745))
edge('communicate0','intent','확인한 답 반영',kind='return',sa='t',sb='t',via=[(1475,650),(995,650)],qi=95,at=(1230,650))
mat('live','실시간 대화',1270,510,410,110,body='즉시 주고받는 대화라면\n발언·중단·재접속을 연결')
edge('live','communicate0','대화 통로',at=(1475,657))
mat('goal','문제·목표·완료 조건',710,865,380,120,body='풀 문제·범위·우선순위와\n끝났음을 확인할 증거를 정함')
edge('intent','goal')
mat('measure0','성과 추적',1270,865,410,120,body='목표에서 확인 항목과 시점을 정함\n완료 뒤에도 실제 효과를 확인')
edge('goal','measure0','성과를 볼 기준',sa='r',sb='l',at=(1180,925))
mat('unused','나눠 맡기기',1270,160,410,110,body='이 상황에서는 쓰지 않음\n한 전문가가 전 과정을 담당',kind='unused')

# Evidence is refined before being used; references are distinct inputs.
group('evidence',90,1070,780,1515,'판단에 쓸 근거를 갖춘다')
group('rules',930,1070,780,1515,'이번 일에 적용할 기준을 맞춘다')
mat('search','정보·자료 찾기',295,1150,370,110,body='부족한 정보·방법·원문을 찾음\n찾은 출처와 미확보 항목을 남김')
edge('goal','search','부족한 근거',sa='b',sb='t',via=[(820,1030),(480,1030)],po=-80,at=(630,1030))
mat('absent','못 찾음·없음 구분',135,1360,330,125,body='빈 검색이면 범위·질의 확인\n근거 없이 “없다”로 단정하지 않음')
mat('now','현재 값·상태 확인',490,1360,330,125,body='현재 값이 판단을 바꾸면 조회\n처리 불명 거래는 재실행 전 확인')
edge('search','absent','빈 검색·없음 주장',via=[(480,1305),(300,1305)],at=(280,1305))
edge('search','now','지금 값이 필요',via=[(500,1315),(655,1315)],po=20,at=(675,1315))
mat('case_ref','적용 사례',135,1550,215,130,body='필요한 사례의\n조건·근거·결과 비교',kind='source')
mat('reference','참고 자료',370,1550,215,130,body='필요한 원리·방법·\n표현을 참고',kind='source')
mat('reuse','재사용 자료',605,1550,215,130,body='서식·부품을 쓰면\n권리·환경 확인',kind='source')
mat('trust','근거의 신뢰성·적합성',240,1780,480,125,body='찾은 자료·조회 결과·사례의 출처와 증거 등급 대조\n이번 대상에 맞고 받아들여질 근거인지 확인')
for k in ['absent','now']:
    side='l' if k=='absent' else 'r';xx=110 if k=='absent' else 845
    edge(k,'trust','검색·조회 결과',sa=side,sb=side,via=[(xx,p(k,side)[1]),(xx,p('trust',side)[1])],at=(xx+70 if side=='l' else xx-60,1720))
for i,k in enumerate(['case_ref','reference','reuse']):
    edge(k,'trust',po=0,qi=(i-1)*100,via=[(p(k)[0],1725),(480+(i-1)*100,1725)])
mat('version','자료의 시점·버전',240,1975,480,110,body='이번 대상·시점에 맞는 판본을 선택\n원문의 위치·확인 시각·변경 관계를 연결')
edge('trust','version','사용할 수 있는 근거',at=(480,1940))
mat('knowledge','업무 지식',135,2170,330,125,body='검증된 근거를 원리·방법으로 연결\n적용 조건·예외를 판단에 제공',kind='source')
mat('experience','실전 경험·감각',490,2170,330,125,body='관련 경험의 단서·요령을 대조\n지금 상황에 맞는 해석을 도움',kind='source')
edge('version','knowledge','원리·방법을 뒷받침',via=[(450,2125),(300,2125)],po=-30,at=(280,2125))
edge('version','experience','경험과 대조할 사실',via=[(510,2125),(655,2125)],po=30,at=(690,2125))
mat('memory','장기 기억',240,2385,480,115,body='해당 고객·건의 이전 결정·약속·교훈을 꺼냄\n현재 근거와 맞는지 확인해 사용',kind='source')

mat('original','규칙·기준 원문',1120,1150,400,100,body='출처·설정 권한·범위·시점을 확인',kind='source')
edge('goal','original','적용할 기준',via=[(980,1030),(1320,1030)],po=80,at=(1190,1030))
mat('law','법·의무 기준',985,1320,670,105,body='법령의 상하·특별·위임 관계와 대상 시점부터 확인\n유효한 명령·처분·예외를 반영')
edge('original','law')
note(975,1485,'충돌하는 조항에만 아래 순위를 적용',24,800,color=C['ink'])
rule_rows=[
 [('ethics','직업 윤리·의무','필수 직업 의무'),('principles','에이전트 기본 원칙','기본 원칙·승인된 보호 기준')],
 [('contract','계약·합의 조건','유효한 계약·약속'),('platform','플랫폼·제출처 규정','플랫폼의 필수 조건')],
 [('org','조직 규칙','조직의 필수 규정')],
 [('user_rule','사용자 지정 규칙','사용자가 추가한 조건')],
 [('style','표현 방식·스타일','대상·매체에 맞는 기본 표현')],
]
for r,items in enumerate(rule_rows):
    yy=1530+r*139
    note(982,yy+51,str(r+1),30,800,color=C['blue'])
    for j,(k,name,body) in enumerate(items):
        mat(k,name,1030+j*315,yy,295 if len(items)>1 else 610,99,body=body,kind='source')
    # Rank is spatial precedence, NOT a time arrow between rules.
group('rank',1010,1510,650,701)
mat('priority','규칙의 적용·우선순위',985,2300,670,175,body='法 적용 관계 + 위의 기준을 함께 대조\n충돌 없는 조건·보호 기준은 모두 유지\n예외 요건·변경 권한을 확인하고 미해결 쟁점을 남김')
N['priority']['body']=N['priority']['body'].replace('法','법적')
edge('law','priority','법적 적용 관계',sa='r',sb='r',via=[(1685,1372.5),(1685,2387.5)],at=(1640,2250))
# Each rank is an exact input to one named material. One bracket, not a fake sequence.
for r,items in enumerate(rule_rows):
    for j,(k,_,_) in enumerate(items):
        N[k]['applies_to']='priority';N[k]['priority_rank']=r+1
note(1325,2260,'위 기준을 함께 적용 ↓',22,600,anchor='middle')

# A real context/model/plan sequence. All preceding outputs have a consumer.
mat('context','현재 작업 정보',640,2675,520,145,body='목표 + 검증된 자료·지식 + 적용 기준 + 진행 상태\n이번 판단에 필요한 것만 모으고\n새 결과·변경이 오면 갱신',kind='source')
edge('knowledge','context','',qi=-160,via=[(300,2330),(110,2330),(110,2550)])
edge('memory','context','',qi=-30,via=[(480,2550)])
edge('experience','context','',qi=100,via=[(655,2330),(845,2330),(845,2550)])
edge('priority','context','지켜야 할 조건',sa='b',sb='r',via=[(1320,2747.5)],at=(1250,2695))
mat('model','AI 모델',640,2895,520,110,body='현재 작업 정보를 읽어 이해·판단·생성\n정해진 계산·조회는 모델 호출 없이 실행 가능')
edge('context','model','지금 판단할 정보',at=(900,2858))
mat('strategy','대안·전략 판단',640,3075,520,120,body='목표·근거·비용·위험으로 방법을 비교\n추가 조사·계속·보류·중단 중 적절한 방향을 정함')
edge('model','strategy','이해한 상황과 가능한 방법',at=(900,3043))
mat('risk','빠진 위험 확인',120,3075,390,120,body='계획·실행·전달 전에\n놓친 조건과 피해를 찾아 대조')
edge('risk','strategy','빠뜨린 위험',sa='r',sb='l',at=(575,3135))
mat('plan','업무 절차·실행 계획',640,3270,520,120,body='선택한 방법을 입력 → 작업 → 출력으로 연결\n순서·병렬·검사·중단·재개 조건을 정함')
edge('strategy','plan','선택한 방법',at=(900,3232))
mat('progress','작업 진행·연결',640,3465,520,120,body='완료분을 보존하고 시작 가능한 다음 작업 선택\n변경이 계획을 벗어나면 방법·계획부터 다시 판단')
edge('plan','progress','작업과 연결 조건',at=(900,3428))
mat('state','현재 진행 상태',1250,3270,430,120,body='완료·실패·대기·승인·남은 일 유지\n외부 처리 결과가 불명확한 상태도 보존',kind='source')
edge('state','progress','현재 상태',sa='l',sb='r',via=[(1205,3330),(1205,3485)],qi=-40,at=(1210,3420))
mat('record','판단 근거 기록',1250,3465,430,120,body='매 판단·실행·검사의 입력과 결과 기록\n왜 선택·수정했는지 근거를 연결',kind='source')
N['record']['applies_to']='ALL_DECISIONS_AND_ACTIONS'
edge('progress','record','선택·진행 근거',sa='r',sb='l',at=(1205,3525))
mat('control','실행 제어',640,3655,520,120,body='준비된 입력으로 함수·도구·모델 호출\n조건 분기·결과 합류·오류·대기·재개를 연결')
edge('progress','control','지금 할 작업과 입력',at=(900,3622))
mat('isolation','분리 실행',120,3465,390,120,body='실행할 자료·작업 공간과 자원을 분리\n허용한 공유만 열고 오류 확산을 막음')
edge('isolation','control','실행 공간·자원',sa='b',sb='l',via=[(315,3715)],at=(470,3685))
mat('monitor','운영 감시·복구',1250,3655,430,120,body='별도 운영 감시가 장애·지연을 감지\n격리·복구 후 저장 상태로 업무를 돌려줌')
edge('control','monitor','운영 상태',sa='r',sb='l',at=(1205,3715))
edge('monitor','state','복구한 상태',kind='return',sa='r',sb='r',via=[(1725,3715),(1725,3330)],at=(1690,3415))

# Permission is checked on every execution, including a retry.
mat('rights','업무 권한',120,3860,390,115,body='누구의 어떤 행위인지 확인\n현재 승인 범위·유효 기간·철회 반영',kind='source')
mat('limit','비용·위험 한도',1250,3860,430,115,body='사용·예약·진행분까지 합산\n실행·대기의 비용과 위험을 비교',kind='source')
mat('guard','안전장치',640,3885,520,120,body='매 정보 교환·실행·재시도·재개 때\n규칙·권한·한도와 대조해 허용·차단·보류')
edge('control','guard','실행 요청',at=(900,3830))
edge('rights','guard','현재 권한',sa='r',sb='l',at=(575,3945))
edge('limit','guard','남은 여유·위험',sa='l',sb='r',at=(1205,3945))
node('allowed','실행해도 되는가?',720,4070,360,170,kind='decision')
edge('guard','allowed')
mat('handoff','사람에게 넘기기',1250,4080,430,145,body='준비·조사·검증을 마친 뒤 필요한 결정만 요청\n되돌릴 수 없음·필수 승인·판단 불가\n한도 초과·자격자 전속일 때')
edge('allowed','handoff','아니오 · 사람 결정 필요',kind='blocked',sa='r',sb='l',at=(1180,4125))
node('hold','해당 작업 보류·중단',120,4100,390,82,kind='stop',body='사유와 재개 조건을 남김')
edge('allowed','hold','아니오 · 실행 불가',kind='blocked',sa='l',sb='r',at=(595,4135))
mat('identity0','보고 주체 확인',1250,4320,430,120,body='받은 승인·결정의 사람·권한·대상·판본 대조\n불일치한 답은 적용하지 않고 다시 확인')
edge('handoff','identity0','답변이 도착하면',at=(1465,4270))
edge('identity0','guard','유효한 결정 반영 후 재검사',kind='return',sa='r',sb='r',via=[(1735,4380),(1735,4025),(1130,4025)],qi=40,at=(1440,4025))
mat('tools','업무 도구·시스템',640,4345,520,110,body='선택한 작업의 도구 요청을 연결\n도구의 결과·오류·외부 처리 상태를 회수')
edge('allowed','tools','예 · 허용된 작업',at=(900,4295))

# Optional operations: six explicit types, selected functions, typed outputs.
# One selected function may be enough; a combination uses another pass with its
# validated output as the next input. No false mandatory calculation→prediction.
families=[
 ('자료를\n정리하는가?',[
  ('sort','자료 선별·분류','원자료 → 필요한 항목·분류'),
  ('combine','자료 정리·결합','흩어진 기록 → 연결·정리된 자료'),
  ('convert','형식·구조 변환','원본 → 필요한 형식·항목 구조')]),
 ('값·의미·결론을\n구하는가?',[
  ('calc','계산','수치·식 → 계산값'),
  ('analysis','분석','자료·계산값 → 관계·원인'),
  ('judge','기준 적용·판정','사실·기준 → 충족 여부'),
  ('forecast','예측','자료·가정 → 전망·불확실성'),
  ('optimize','조건 안에서 최선 찾기','후보·제약 → 최선의 안')]),
 ('결과물을\n만드는가?',[
  ('design','결과물 설계','목적·요건 → 구성·제작 설계'),
  ('reframe','내용 재구성','기존 내용 → 목적에 맞는 내용'),
  ('make','결과물 만들기·수정','설계·자료 → 결과물·수정본')]),
 ('사람과\n조율하는가?',[
  ('talk','사람과 소통','질문·내용 → 이해·답변 확인'),
  ('negotiate','협상·조율','서로 다른 요구 → 합의·남은 쟁점')]),
 ('외부 시스템에\n반영하는가?',[
  ('write','기록 입력·수정','확인한 내용 → 반영 기록·이력'),
  ('transaction','신청·거래 처리','승인된 요청 → 접수·처리 상태'),
  ('operate','설정·작동 제어','유지 조건·상태 → 설정·작동 조정'),
  ('publish','게시·배포','확인된 판본 → 공개·제공 상태')]),
 ('새 증거를\n만드는가?',[
  ('observe','관찰·측정','대상·방법 → 조건이 붙은 관측값'),
  ('experiment','실험','비교 조건 → 차이·영향·한계'),
  ('simulate','시뮬레이션','가정·모형 → 예상 진행·반응')]),
]
Y=4550
for fi,(question,items) in enumerate(families):
    yy=Y+fi*490
    group('opg'+str(fi),380,yy,1300,422)
    node('type'+str(fi),question,95,yy+4,240,150,kind='decision')
    node('choose'+str(fi),'필요한 재료를\n선택·조합',815,yy+4,450,160,kind='decisionwide')
    edge('type'+str(fi),'choose'+str(fi),'예',sa='r',sb='l',at=(515,yy+79))
    if fi==0:
        edge('tools','type0','실행할 작업의 종류',sa='b',sb='t',via=[(900,4500),(215,4500)],at=(555,4500))
    else:
        edge('type'+str(fi-1),'type'+str(fi),'아니오',kind='blocked',at=(215,yy-145))
    count=len(items);cw=(1220-22*(count-1))/count
    for j,(k,name,body) in enumerate(items):
        xx=420+j*(cw+22)
        mat(k,name,xx,yy+195,cw,135,body=body)
        # Fans start on the decision's lower sloping boundary (computed below).
        startx=790+j*(500/max(count-1,1)) if count>1 else 1040
        destx=xx+cw/2
        edge('choose'+str(fi),k,'',po=startx-1040,via=[])
    node('out'+str(fi),'선택한 작업의 결과',770,yy+365,540,60,kind='data')
    for j,(k,_,_) in enumerate(items):
        edge(k,'out'+str(fi),qi=(j-(count-1)/2)*55,via=[])
    # All paths have exactly the same named verification consumer.
    edge('out'+str(fi),'__VERIFY__','',sa='r',sb='r',via=[(1750,yy+395),(1750,0)])

V=Y+6*490+100
mat('verify','결과 검증·재검증',640,V,520,140,body='각 결과를 원문·완료 조건·다음 입력 요건과 대조\n문제없음 / 문제 있음 / 아직 확인 불가\n수정·변경이 생기면 영향받은 결과도 재검증')
for e in E:
    if e['target']=='__VERIFY__':
        e['target']='verify';e['points'][-2]=(1750,V+70);e['points'][-1]=p('verify','r')
mat('identity','보고 주체 확인',1230,V-30,430,120,body='외부 보고·결과와 명의의 주체 확인\n대상·요청·판본이 다르면 받아들이지 않음')
edge('identity','verify','받아도 되는 결과',sa='b',sb='r',via=[(1445,V+70)],at=(1360,V+40))
mat('counter','반대 근거·다시 확인',130,V,380,140,body='중요한 결론이면 반대 증거·다른 방법으로 대조\n판단을 유지·수정·유보할 근거를 제시')
edge('counter','verify','독립적으로 대조한 근거',sa='r',sb='l',at=(575,V+70))
node('vdecision','결과를 확인했는가?',720,V+225,360,175,kind='decision')
edge('verify','vdecision')
mat('wait','대기·후속 관리',1240,V+235,430,140,body='답변·승인·외부 처리·확인 시점 관리\n기한이 오면 조회·대체·인계를 연결\n응답이 오면 최신 조건으로 재개')
edge('vdecision','wait','아직 확인 불가',kind='blocked',sa='r',sb='l',at=(1160,V+310))
edge('wait','verify','답변·상태 확인 후 재검증',kind='return',sa='r',sb='r',via=[(1715,V+305),(1715,V+175),(1195,V+175),(1195,V+105)],qi=35,at=(1450,V+175))
node('more','완료 조건을\n모두 충족했는가?',720,V+485,360,190,kind='decision')
edge('vdecision','more','예 · 문제없음',at=(900,V+445))
mat('context2','현재 작업 정보',130,V+480,390,155,body='검증한 결과를 다음 판단·작업의 입력으로 보탬\n오류·부족한 근거·변경은 보완 대상으로 표시',kind='source')
edge('vdecision','context2','문제 있음 · 보완 필요',kind='blocked',sa='l',sb='t',via=[(630,V+312.5),(325,V+312.5)],at=(470,V+312.5))
edge('more','context2','아니오 · 다음 작업 필요',kind='blocked',sa='l',sb='r',at=(620,V+580))
edge('context2','context','새 입력으로 다음 작업·방법 판단',kind='return',sa='l',sb='l',via=[(45,V+557.5),(45,2850),(595,2850),(595,2782.5)],qi=35,at=(80,6100))

# Deliverable, reception, responsibility, and measured learning.
D=V+765
mat('quality','결과 품질 평가',650,D,500,120,body='목적·분야 기준으로 정확성·기능·이해·사용성 평가\n완료 기준에 못 미친 부분은 보완 작업으로 연결')
edge('more','quality','예',at=(900,V+720))
mat('process_eval','일하는 과정 평가',1240,D,430,120,body='각 단계와 종료 시 방법·절차·권한 준수 평가\n당시 조건에서 적절한 판단이었는지 확인')
edge('quality','process_eval','결과와 수행 기록',sa='r',sb='l',at=(1195,D+60))
mat('pack','납품 준비',650,D+200,500,120,body='확인한 결과·판본·원본·사용 설명을 갖춤\n미완료·후속 책임·담당과 검사 결과도 연결')
edge('quality','pack','넘길 수 있는 결과',at=(900,D+165))
mat('delivery','전달·인수 확인',650,D+400,500,120,body='정해진 상대에게 전달하고 도착·사용 조건 확인\n수정 요청·확인 대기·인수 완료를 구별')
edge('pack','delivery','결과와 인계 내용',at=(900,D+365))
node('receipt','약속한 인수를\n확인했는가?',720,D+595,360,175,kind='decision')
edge('delivery','receipt')
mat('wait2','대기·후속 관리',1240,D+605,430,140,body='확인·수정 요청과 남은 약속을 유지\n기한·응답에 맞춰 재확인 또는 보완 연결')
edge('receipt','wait2','아니오',kind='blocked',sa='r',sb='l',at=(1160,D+665))
edge('wait2','delivery','인수 확인 재개',kind='return',sa='t',sb='r',via=[(1455,D+460)],at=(1350,D+460))
mat('outcome','성과 추적',650,D+855,500,120,body='정한 시점에 목표 달성과 뒤늦은 효과·문제 확인\n난이도·환경·자원 차이를 고려해 비교')
edge('receipt','outcome','예 · 이후 성과도 추적',at=(900,D+815))
mat('cause','성공·실패 원인 분석',650,D+1055,500,120,body='재사용할 성과·반복 오류·큰 문제가 있으면\n지식·방법·도구·조건에서 원인과 개선점을 찾음')
edge('outcome','cause','성과·실패·평가 근거',at=(900,D+1015))
edge('process_eval','cause','과정 평가',sa='r',sb='r',via=[(1740,D+60),(1740,D+1115)],at=(1630,D+985))
mat('improve','능력 개선·확장',650,D+1255,500,120,body='개선점이나 새로운 업무가 있으면\n지식·방법·도구의 개선안을 만들고 시험에 연결')
edge('cause','improve','개선할 원인',at=(900,D+1215))
mat('testenv','시험 환경',120,D+1255,380,120,body='실제 업무·원본과 분리해 조건 재현\n미시험·실패 판본은 실제 적용 차단')
mat('capability','업무 능력 시험',650,D+1455,500,145,body='처음 투입·범위 밖 업무·능력 변경 때 시험\n개선 효과와 기존 능력 유지까지 확인\n통과한 범위·판본만 실제 업무에 적용')
edge('improve','capability','적용 전 시험할 개선안',at=(900,D+1415))
edge('testenv','capability','재현 가능한 시험 조건',sa='b',sb='l',via=[(310,D+1527.5)],at=(415,D+1480))
node('passed','능력 시험을\n통과했는가?',1240,D+1450,400,170,kind='decision')
edge('capability','passed','시험 결과',sa='r',sb='l',at=(1195,D+1528))
edge('passed','improve','아니오 · 개선안을 다시 보완',kind='return',sa='t',sb='r',via=[(1440,D+1315)],at=(1390,D+1355))
mat('memory2','장기 기억',650,D+1740,500,140,body='사실·약속·결정·교훈을 해당 건과 근거에 묶어 보존\n검증된 개선은 다음 업무의 지식·방법에 반영\n잘못된 기억은 정정하고 남은 책임은 유지',kind='source')
edge('passed','memory2','예 · 검증된 개선 반영',sa='b',sb='r',via=[(1440,D+1810)],at=(1410,D+1700))
node('finish','이번 건 처리 종료',710,D+1955,380,85,body='남은 약속·후속 확인은 계속 관리',kind='terminal')
edge('memory2','finish')

# Explicit absence of a need bypasses the optional learning branch.
edge('outcome','memory2','분석·개선이 필요 없으면 기록만 남김',sa='l',sb='l',via=[(585,D+915),(585,D+1430),(95,D+1430),(95,D+1635),(560,D+1635),(560,D+1810)],at=(585,D+1680))

# Actual job result is the input of the verification node (late binding above).
# Sources/always-on application relations are recorded in addition to control links.
for k in ['case_ref','reference','reuse']:
    N[k]['input_from']='search'
for k in ['trust','version','knowledge','experience','memory','priority']:
    N[k]['used_at']='each relevant judgment, execution and verification'
N['guard']['criteria_from']=['priority','rights','limit']
N['risk']['input_from']=['goal','plan','context2']
N['testenv']['guards_real_use_of']='capability'
N['record']['outputs_to']=['process_eval','cause','memory2']
N['live']['input_from']='communicate0'
N['identity']['input_from']='tools'

H=D+2120

def remove(a,b):
    E[:]=[e for e in E if (e['source'],e['target'])!=(a,b)]
def insert_space(y,dy):
    global H
    for n in N.values():
        if n['y']>=y:n['y']+=dy
    for g in G:
        if g['y']>=y:g['y']+=dy
        elif g['y']+g['h']>y:g['h']+=dy
    for e in E:
        e['points']=[(x,yy+dy if yy>=y else yy) for x,yy in e['points']]
        if e['at']:
            x,yy=e['at'];e['at']=(x,yy+dy if yy>=y else yy)
    for a in A:
        if a['y']>=y:a['y']+=dy
    H+=dy

# The question, not an ordinary process box, controls whether a clarification is needed.
insert_space(N['goal']['y'],170)
remove('intent','goal');remove('intent','communicate0');remove('communicate0','intent');remove('live','communicate0')
N['live'].update(x=100,y=700,w=410,h=105)
N['communicate0'].update(x=100,y=865,w=410,h=110)
node('clear','범위가 달라질 만큼\n모호한가?',720,845,360,155,kind='decision')
edge('intent','clear')
edge('clear','goal','아니오',kind='blocked',at=(900,1020))
edge('clear','communicate0','예 · 확인 필요',sa='l',sb='r',at=(605,922))
edge('live','communicate0','즉시 대화할 때의 통로',sa='l',sb='l',via=[(70,752.5),(70,920)],at=(240,832))
edge('communicate0','intent','확인한 뜻·범위 반영',kind='return',sa='t',sb='l',via=[(305,835),(610,835),(610,745)],at=(615,790))

# An untested capability cannot first meet its admission test after the live job.
insert_space(N['plan']['y'],650)
remove('strategy','plan')
sy=N['strategy']['y']+N['strategy']['h']+55
node('qualified','이번 일은 검증된\n능력 범위 안인가?',720,sy,360,170,kind='decision')
edge('strategy','qualified')
edge('qualified','plan','예 · 통과한 범위·판본',at=(920,sy+340))
mat('testenv0','시험 환경',120,sy,390,110,body='처음 투입·범위 밖 업무·능력 변경이면\n실제 업무와 분리한 시험을 준비')
mat('capability0','업무 능력 시험',120,sy+190,390,135,body='이번 일을 끝까지 처리할 수 있는지 시험\n예외·중단·재개와 기존 능력도 확인')
edge('qualified','testenv0','아니오 · 먼저 시험',kind='blocked',sa='l',sb='r',at=(610,sy+70))
edge('testenv0','capability0','시험 조건·통과 기준',at=(315,sy+150))
node('qualified_test','시험을 통과했는가?',120,sy+395,390,160,kind='decision')
edge('capability0','qualified_test')
edge('qualified_test','plan','예 · 가능한 범위만 계획',sa='r',sb='l',via=[(580,sy+475),(580,p('plan','l')[1])],at=(595,sy+555))
node('unqualified','해당 업무 투입 보류',120,sy+630,390,82,body='미통과 판본은 실제 투입 차단',kind='stop')
edge('qualified_test','unqualified','아니오',kind='blocked',at=(315,sy+593))

# The last type also has an explicit destination.
last=N['type5'];ctx=N['context2']
edge('type5','context2','아니오 · 필요한 작업을 다시 선택',kind='blocked',via=[(215,last['y']+285),(80,last['y']+285),(80,ctx['y']-80),(250,ctx['y']-80)],qi=-75,at=(340,last['y']+310))

# Quality failure is an actual correction path, not a sentence below a success arrow.
insert_space(N['pack']['y'],210)
remove('quality','pack')
qy=N['quality']['y']+N['quality']['h']+65
node('qualityok','받는 사람이 쓸 만큼\n품질이 충분한가?',720,qy,360,170,kind='decision')
edge('quality','qualityok')
edge('qualityok','pack','예',at=(900,qy+210))
mat('repair','작업 진행·연결',120,qy+25,390,120,body='미달한 항목을 보완 작업으로 연결\n바뀐 부분과 영향받은 결과를 다시 검사')
edge('qualityok','repair','아니오',kind='blocked',sa='l',sb='r',at=(610,qy+85))
edge('repair','context2','보완할 내용 반영',kind='return',sa='t',sb='b',via=[(315,p('context2','b')[1]+70),(325,p('context2','b')[1]+70)],at=(315,qy-70))

# Learning is conditional; facts and commitments can be remembered without an improvement.
insert_space(N['cause']['y'],220)
remove('outcome','cause');remove('outcome','memory2');remove('process_eval','cause')
oy=N['outcome']['y']+N['outcome']['h']+65
node('learnneed','원인을 분석할\n성과·문제가 있는가?',720,oy,360,170,kind='decision')
edge('outcome','learnneed')
edge('learnneed','cause','예',at=(900,oy+215))
mat('memory_direct','장기 기억',1240,oy+25,430,125,body='이번 건의 사실·결정·약속·교훈 보존\n남은 책임과 후속 확인도 함께 유지',kind='source')
edge('learnneed','memory_direct','아니오',kind='blocked',sa='r',sb='l',at=(1160,oy+85))
edge('memory_direct','finish','',sa='r',sb='r',via=[(1710,oy+87.5),(1710,p('finish','r')[1])])
edge('process_eval','outcome','과정 평가와 실제 성과 비교',sa='r',sb='r',via=[(1740,p('process_eval','r')[1]),(1740,p('outcome','r')[1])],at=(1620,p('outcome','r')[1]-85))

insert_space(N['improve']['y'],220)
remove('cause','improve')
iy=N['cause']['y']+N['cause']['h']+55
node('improveneed','능력을 바꿀\n필요가 있는가?',720,iy,360,170,kind='decision')
edge('cause','improveneed')
edge('improveneed','improve','예',at=(900,iy+215))
mat('memory_reuse','장기 기억',1240,iy+25,430,125,body='유지·재사용할 방법과 적용 조건 보존\n능력을 바꾸지 않아도 교훈은 다음 일에 활용',kind='source')
edge('improveneed','memory_reuse','아니오',kind='blocked',sa='r',sb='l',at=(1160,iy+85))
edge('memory_reuse','finish','',sa='r',sb='r',via=[(1710,iy+87.5),(1710,p('finish','r')[1])])
for e in E:
    if e['source']=='passed' and e['target']=='improve':e['label']='미통과한 개선안 보완'

# Provenance is inspected before the result is accepted for verification.
remove('identity','verify')
N['identity']['body']='보고한 주체·대상·요청·판본을 대조\n불일치하면 결과 대신 반려 사유를 전달'
for e in E:
    if e['source'].startswith('out') and e['target']=='verify':
        e['target']='identity'
        e['points'][-2]=(1750,p('identity','r')[1]);e['points'][-1]=p('identity','r')
edge('identity','verify','',sa='l',sb='r')

insert_space(N['vdecision']['y'],175)
remove('verify','vdecision')
vy=N['verify']['y']+N['verify']['h']+55
mat('state_result','현재 진행 상태',640,vy,520,115,body='검증 결과를 완료·보완·확인 대기 상태에 반영\n이미 끝난 외부 처리는 중복 실행하지 않음',kind='source')
edge('verify','state_result','검증 결과와 처리 상태',at=(900,vy-27))
edge('state_result','vdecision')
ry=N['quality']['y']-190
mat('record_read','판단 근거 기록',1240,ry,430,115,body='각 단계의 입력·선택·실행·검사 기록\n평가할 근거로 꺼냄',kind='source')
edge('record_read','process_eval','과정 평가의 근거',at=(1455,ry+155))
N['context2']['body']='검증한 결과·상태를 다음 작업의 입력으로 보탬\n오류·부족한 근거·변경은 보완 대상으로 표시'
N['design']['body']='목적·요건·표현 기준 → 구성·제작 설계'
N['make']['body']='설계·재사용 자료 → 결과물·수정본'
N['talk']['body']='상대·내용·표현 기준 → 이해·답변 확인'
for i,s in enumerate(['정리·분류·변환된 자료','판단에 필요한 값·결론','설계·내용·결과물','답변·합의·남은 쟁점','반영 결과·외부 처리 상태','관측·비교·가정의 결과']):
    N['out'+str(i)]['title']=s
N['type4']['title']='외부에\n반영하는가?'
short_labels={
 ('progress','record'):'근거',('control','monitor'):'상태',('limit','guard'):'한도',
 ('allowed','handoff'):'아니오\n사람 결정',('allowed','hold'):'아니오\n실행 불가',
 ('counter','verify'):'대조 근거',('more','context2'):'아니오\n다음 작업',
 ('quality','process_eval'):'결과',('capability','passed'):'검사값',
 ('live','communicate0'):'대화 통로',
}
for e in E:
    pair=(e['source'],e['target'])
    if pair in short_labels:e['label']=short_labels[pair]
    if pair==('early','signal'):e['at']=(558,330)
    if pair==('absent','trust'):e['at']=(170,N['trust']['y']-32)
    if pair==('allowed','handoff'):e['at']=(1165,p('allowed','r')[1])
    if pair==('allowed','hold'):e['at']=(615,p('allowed','l')[1])
    if pair==('context2','context'):
        e['label']='검증 결과로 다음 작업 선택';e['at']=(310,e['points'][2][1])
    if pair==('live','communicate0'):e['at']=(100,838)
    if pair==('type5','context2'):
        e['label']='아니오\n작업 재선택';yy=N['type5']['y']+480
        e['at']=(150,yy);e['points'][1]=(215,yy);e['points'][2]=(80,yy)
for k,s in {
 'calc':'수치·식\n→ 계산값',
 'analysis':'자료·계산값\n→ 관계·원인',
 'judge':'사실·기준\n→ 충족 여부',
 'forecast':'자료·가정\n→ 전망·불확실성',
 'optimize':'후보·제약\n→ 가장 나은 안',
}.items():N[k]['body']=s

# A correction request returns to the work itself, not merely to redelivery.
N['receipt']['title']='인수 상태는?'
for e in E:
    if (e['source'],e['target'])==('receipt','outcome'):e['label']='인수 완료'
    if (e['source'],e['target'])==('receipt','wait2'):e['label']='확인 대기'
dy=N['receipt']['y']+25
mat('delivery_repair','작업 진행·연결',120,dy,390,125,body='받은 수정 요청을 해당 작업에 연결\n수정·영향 범위 확인 뒤 다시 검증')
edge('receipt','delivery_repair','수정 요청',kind='blocked',sa='l',sb='r',at=(610,dy+62.5))
edge('delivery_repair','repair','수정할 작업으로 복귀',kind='return',sa='t',sb='b',at=(315,(dy+p('repair','b')[1])/2))
A[:]=[a for a in A if a['text']!='위 기준을 함께 적용 ↓']
rank=next(g for g in G if g['id']=='rank')
edge('rank','priority','함께 대조',at=(1325,(rank['y']+rank['h']+N['priority']['y'])/2))

# Keep the unused material at the point where work is assigned. Passing this
# explicitly inactive card means choosing direct execution, not invoking it.
assignment_y=N['progress']['y']
insert_space(assignment_y,230)
N['unused'].update(x=640,y=assignment_y+10,w=520,h=165)
remove('plan','progress')
edge('plan','unused','한 전문가가 모두 맡음')
edge('unused','progress','다른 AI에게 나누지 않고 직접 처리')

COPY=json.loads((ROOT/'docs/도식/단독-재료-쉬운설명.json').read_text())
assert set(COPY['materials'])==set(CAT)
SYSTEM_STYLE={
 '환경':dict(accent='#1766A6',fill='#EDF5FF'),
 '지식':dict(accent='#157267',fill='#EAF7F3'),
 '규칙':dict(accent='#7151A8',fill='#F3EEFC'),
 '실무':dict(accent='#995114',fill='#FFF3E5'),
 '검증':dict(accent='#A23C6B',fill='#FCEEF4'),
 '학습':dict(accent='#526E20',fill='#F1F6E5'),
}
def text_layout(n):
    z=25 if n['w']>=280 else 22
    tw=n['w']-32
    if n['kind']=='decision':tw=n['w']*.58;z=23
    if n['kind']=='decisionwide':tw=n['w']*.75;z=23
    titles=wrap(n['title'],tw,z)
    bs=21 if n['material'] else 20
    body=wrap(n['body'],n['w']-32,bs) if n['body'] else []
    return z,bs,titles,body
for k,n in N.items():
    if n['material']:
        n['term']=CAT[n['material']]['term'];n['system']=CAT[n['material']]['system']
        n['body']=COPY['instances'].get(k,COPY['materials'][n['material']])
        z,bs,titles,body=text_layout(n)
        n['needed_height']=32+len(titles)*(z+5)+10+len(body)*27+22
    else:n['needed_height']=n['h']

# Stretch only occupied row intervals that need room for the easier explanation
# and the category label. The same monotonic transform moves all line routes.
knots=sorted({0,H,*[n['y'] for n in N.values()],*[n['y']+n['h'] for n in N.values()]})
ys=[0.0];scales=[]
for a,b in zip(knots,knots[1:]):
    active=[n['needed_height']/n['h'] for n in N.values() if n['y']<b and n['y']+n['h']>a]
    scale=max([1,*active]);scales.append(scale);ys.append(ys[-1]+(b-a)*scale)
def yf(y):
    i=min(max(0,bisect.bisect_right(knots,y)-1),len(scales)-1)
    return ys[i]+(y-knots[i])*scales[i]
for n in N.values():n['y'],n['h']=yf(n['y']),yf(n['y']+n['h'])-yf(n['y'])
for g in G:g['y'],g['h']=yf(g['y']),yf(g['y']+g['h'])-yf(g['y'])
for e in E:
    e['points']=[(x,yf(y)) for x,y in e['points']]
    if e['at']:e['at']=(e['at'][0],yf(e['at'][1]))
for a in A:a['y']=yf(a['y'])
H=math.ceil(yf(H))
for k in ['goal','pack','state_result','progress']:
    insert_space(N[k]['y'],45)
label_edits={
 ('watchtype','change'):'조건\n변화',('goal','measure0'):'확인 기준',
 ('risk','strategy'):'위험',('counter','verify'):'근거',
 ('vdecision','wait'):'확인\n불가',('capability','passed'):'결과',
 ('unused','progress'):'한 전문가가 직접 처리',
}
for e in E:
    if (e['source'],e['target'])==('absent','trust'):e['label']='검색 결과'
    if (e['source'],e['target'])==('now','trust'):e['label']='조회 결과'
    if (e['source'],e['target']) in label_edits:e['label']=label_edits[e['source'],e['target']]

def rounded(points,r=14):
    # Polyline corners rounded without freeform splines wandering through labels.
    ps=[]
    for q in points:
        if not ps or q!=ps[-1]:ps.append(q)
    if len(ps)<2:return ''
    d=f'M{ps[0][0]},{ps[0][1]}'
    for i in range(1,len(ps)-1):
        a,b,c=ps[i-1:i+2];u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);lu=math.hypot(*u);lv=math.hypot(*v)
        rr=min(r,lu/2,lv/2)
        q=(b[0]+u[0]/lu*rr,b[1]+u[1]/lu*rr);z=(b[0]+v[0]/lv*rr,b[1]+v[1]/lv*rr)
        d+=f' L{q[0]},{q[1]} Q{b[0]},{b[1]} {z[0]},{z[1]}'
    return d+f' L{ps[-1][0]},{ps[-1][1]}'
def boundary(n,point):
    # The material selection is a genuine diamond; attach to its outline.
    if n['kind'] not in ('decision','decisionwide'):return point
    cx=n['x']+n['w']/2;cy=n['y']+n['h']/2;dx=point[0]-cx;dy=point[1]-cy
    den=abs(dx)/(n['w']/2)+abs(dy)/(n['h']/2)
    return (cx+dx/den,cy+dy/den) if den else point
for e in E:
    if e['source'] in N:e['points'][0]=boundary(N[e['source']],e['points'][0])
    if e['target'] in N:e['points'][-1]=boundary(N[e['target']],e['points'][-1])
    end=e['points'][-1];before=next(q for q in reversed(e['points'][:-1]) if math.dist(q,end)>1)
    length=math.dist(before,end);u=((end[0]-before[0])/length,(end[1]-before[1])/length)
    tip=(end[0]-u[0]*5,end[1]-u[1]*5);base=(tip[0]-u[0]*18,tip[1]-u[1]*18)
    e['arrow']=[tip,(base[0]-u[1]*8,base[1]+u[0]*8),(base[0]+u[1]*8,base[1]-u[0]*8)]

def rect_overlap(a,b,pad=0):
    return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>pad
def line_rect(a,b,r,pad=1):
    xmin,xmax=r['x']+pad,r['x']+r['w']-pad;ymin,ymax=r['y']+pad,r['y']+r['h']-pad
    if min(a[0],b[0])>xmax or max(a[0],b[0])<xmin or min(a[1],b[1])>ymax or max(a[1],b[1])<ymin:return False
    t0,t1=0.,1.;dx=b[0]-a[0];dy=b[1]-a[1]
    for p0,q in [(-dx,a[0]-xmin),(dx,xmax-a[0]),(-dy,a[1]-ymin),(dy,ymax-a[1])]:
        if abs(p0)<1e-8:
            if q<0:return False
        elif p0<0:t0=max(t0,q/p0)
        else:t1=min(t1,q/p0)
        if t0>t1:return False
    return True
def label_box(text,x,y):
    lines=text.split('\n');w=max(measure(s,20) for s in lines)+20;h=26*len(lines)+10
    return dict(x=x-w/2,y=y-h/2,w=w,h=h)
occupied=[]
for a in A:
    w=measure(a['text'],a['size']);x=a['x']-(w/2 if a['anchor']=='middle' else 0)
    occupied.append(dict(x=x,y=a['y']-a['size'],w=w,h=a['size']+5))
arrow_bounds=[]
for e in E:
    xs=[p[0] for p in e['arrow']];yy=[p[1] for p in e['arrow']]
    arrow_bounds.append(dict(x=min(xs)-2,y=min(yy)-2,w=max(xs)-min(xs)+4,h=max(yy)-min(yy)+4))
unplaced=[]
for i,e in enumerate(E):
    if not e['label']:continue
    preferred=e['at'] or ((e['points'][0][0]+e['points'][-1][0])/2,(e['points'][0][1]+e['points'][-1][1])/2)
    candidates=[]
    for a,b in zip(e['points'],e['points'][1:]):
        length=math.dist(a,b)
        if length<10:continue
        fractions={.5,*[j/20 for j in range(1,20)]}
        initial=label_box(e['label'],0,0)
        half=(initial['w'] if abs(b[0]-a[0])>=abs(b[1]-a[1]) else initial['h'])/2
        fractions.update(f for f in ((half+6)/length,1-(half+26)/length) if .02<f<.98)
        projection=((preferred[0]-a[0])*(b[0]-a[0])+(preferred[1]-a[1])*(b[1]-a[1]))/length**2
        fractions.add(max(.03,min(.97,projection)))
        for f in fractions:
            x=a[0]+f*(b[0]-a[0]);y=a[1]+f*(b[1]-a[1]);r=label_box(e['label'],x,y)
            if r['x']<6 or r['x']+r['w']>W-6 or r['y']<6:continue
            if any(rect_overlap(r,n,0) for n in N.values()):continue
            if any(rect_overlap(r,o,-2) for o in occupied+arrow_bounds):continue
            if any(j!=i and any(line_rect(c,z,r) for c,z in zip(other['points'],other['points'][1:])) for j,other in enumerate(E)):continue
            candidates.append((math.dist((x,y),preferred)+(60 if abs(b[1]-a[1])>abs(b[0]-a[0]) else 0),x,y,r))
    if candidates:
        _,x,y,r=min(candidates,key=lambda c:c[0]);e['at']=(x,y);e['label_rect']=r;occupied.append(r)
    else:
        e['label_rect']=label_box(e['label'],*preferred);e['at']=preferred;unplaced.append((i,e['source'],e['target'],e['label']))
if unplaced:print('LABELS_NEED_PLACEMENT',json.dumps(unplaced,ensure_ascii=False))
names=Counter(n['material'] for n in N.values() if n['material'])
assert set(names)==set(CAT),(set(CAT)-set(names),set(names)-set(CAT))
model=dict(width=W,height=H,nodes=N,groups=G,edges=E,annotations=A,illustrations=[],catalog=CAT,system_styles=SYSTEM_STYLE,system_mapping=TERM_SYSTEMS,
           source_prefix_sha256=hashlib.sha256(PREFIX.encode()).hexdigest())
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   '<title>한 건을 한 전문가가 처리할 때의 재료 연결 구조</title>','<rect width="100%" height="100%" fill="white"/>',f'<g font-family="Apple SD Gothic Neo,Noto Sans CJK KR,sans-serif" fill="{C["ink"]}">']
for g in G:
    x,y,w,h=(g[k] for k in ('x','y','w','h'))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="none" stroke="{C["border"]}" stroke-width="1.7" stroke-dasharray="3 9"/>')
    if g['title']:o.append(f'<text class="annotation" x="{x+22}" y="{y+37}" font-size="27" font-weight="800">{esc(g["title"])}</text>')
for i,e in enumerate(E):
    col=C[{'flow':'blue','blocked':'red','return':'yellow'}[e['kind']]]
    route=e['points'][:-1]+[e['arrow'][0]]
    o.append(f'<path class="edge" data-id="e{i}" d="{rounded(route)}" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>')
for k,n in N.items():
    x,y,w,h=(n[t] for t in ('x','y','w','h'));kind=n['kind']
    o.append(f'<g class="node" data-id="{k}" data-material="{esc(n["material"] or "")}" data-system="{n.get("term","")}">')
    palette=SYSTEM_STYLE[n['term']] if n['material'] else None
    fill=palette['fill'] if palette else '#FFFFFF'
    if kind in ('decision','decisionwide'):
        fill='#FFF5C6';shape=f'<path class="shape" d="M{x+w/2} {y}L{x+w} {y+h/2}L{x+w/2} {y+h}L{x} {y+h/2}Z"'
    else:
        if kind in ('terminal','stop'):fill=C['green'] if kind=='terminal' else '#FFF0EC'
        if kind=='unused':fill='#F3F5F7'
        shape=f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if kind in ("terminal","stop") else 5}"'
    o.append(shape+f' fill="{fill}" stroke="{C["ink"]}" stroke-width="2.1"/>')
    z,bs,titles,body=text_layout(n)
    if palette:
        o.append(f'<path d="M{x+2} {y+8}V{y+h-8}" stroke="{palette["accent"]}" stroke-width="4"/>')
        badge=n['term']+(' · 이 상황에서는 미사용' if kind=='unused' else '')
        o.append(f'<text class="system-label" x="{x+16}" y="{y+25}" font-size="18" font-weight="800" fill="{palette["accent"]}">{esc(badge)}</text>')
        yy=y+35+z
    else:
        total=len(titles)*(z+5)+len(body)*25+(8 if body else 0);yy=y+(h-total)/2+z
    for s in titles:o.append(f'<text class="node-title" x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="{z}" font-weight="800">{esc(s)}</text>');yy+=z+5
    yy+=8 if body else 0
    for s in body:o.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="{bs}" fill="{C["muted"]}">{esc(s)}</text>');yy+=27 if palette else 25
    o.append('</g>')
for i,e in enumerate(E):
    if not e['label']:continue
    pts=e['points'];x,y=e['at'] or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
    lines=e['label'].split('\n');tw=e['label_rect']['w'];th=e['label_rect']['h']
    col=C[{'flow':'blue','blocked':'red','return':'yellow'}[e['kind']]]
    o.append(f'<g class="edge-label" data-edge="e{i}"><rect x="{x-tw/2}" y="{y-th/2}" width="{tw}" height="{th}" rx="4" fill="white" stroke="{col}" stroke-width="1"/>')
    for j,s in enumerate(lines):o.append(f'<text x="{x}" y="{y-th/2+24+j*26}" text-anchor="middle" font-size="20" font-weight="600">{esc(s)}</text>')
    o.append('</g>')
for a in A:o.append(f'<text class="annotation" x="{a["x"]}" y="{a["y"]}" font-size="{a["size"]}" font-weight="{a["weight"]}" fill="{a["color"]}" text-anchor="{a["anchor"]}">{esc(a["text"])}</text>')
for i,e in enumerate(E):
    col=C[{'flow':'blue','blocked':'red','return':'yellow'}[e['kind']]]
    o.append(f'<polygon class="arrowhead" data-edge="e{i}" points="'+ ' '.join(f'{x},{y}' for x,y in e['arrow'])+f'" fill="{col}"/>')
o+=['</g>','<metadata>'+esc(json.dumps(model,ensure_ascii=False))+'</metadata>','</svg>']
(ROOT/'docs/images/expert-definition/solo-material-relations.svg').write_text('\n'.join(o))
(ROOT/'docs/도식/단독-재료-연결구조.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(materials=len(names),nodes=len(N),edges=len(E),width=W,height=H),ensure_ascii=False))
