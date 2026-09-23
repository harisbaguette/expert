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
C=dict(ink='#17253B',muted='#475569',blue='#3974B8',red='#C45763',yellow='#B57C1F',
       pale='#EEF3FA',border='#D4DDE7',green='#EAF5EF',white='#FFFFFF')
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
edge('trust','version','확인한 근거',at=(480,1940))
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
edge('risk','strategy','위험 유무 확인 완료',sa='r',sb='l',at=(575,3135))
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
    node('choose'+str(fi),'어떤 재료가\n필요한가?',815,yy+4,450,160,kind='decisionwide')
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
N['live']['input_from']='live_start'
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

# Reserve space beside assignment for the explicitly unused material note.
assignment_y=N['progress']['y']
insert_space(assignment_y,230)
N['unused'].update(x=640,y=assignment_y+10,w=520,h=165)
remove('plan','progress')
edge('plan','unused','한 전문가가 모두 맡음')
edge('unused','progress','다른 AI에게 나누지 않고 직접 처리')

# Complete the entry, continuation and reference paths. These are data/control
# relations: a reference supplies an input and is not a second execution start.
N['watch']['title']='맡은 상황에서 변화 발견'
N['watchtype']['title']='어떤 대응이\n필요한가?'
for e in E:
    if (e['source'],e['target'])==('watchtype','early'):
        e['label']='새로 대응할 일'
    if (e['source'],e['target'])==('watchtype','change'):
        e['label']='기존 업무\n변경'

# Live conversation is an explicit entry and feeds the same request intake.
remove('live','communicate0')
N['live'].update(x=1270,y=158,w=410,h=145)
node('live_start','통화·실시간 채팅 요청',1270,40,410,68,kind='terminal')
edge('live_start','live')
edge('live','signal','받은 요청·답변',sa='l',sb='r')

# Performance criteria are retained with the goal and feed the work preparation.
remove('goal','measure0');remove('goal','search');remove('goal','original')
insert_space(next(g['y'] for g in G if g['id']=='evidence'),260)
N['measure0'].update(x=640,y=p('goal')[1]+85,w=520,h=135)
edge('goal','measure0','목표에 맞는 확인 기준')
by=next(g['y'] for g in G if g['id']=='evidence')-45
edge('measure0','search','필요한 근거 확인',po=-80,via=[(820,by),(480,by)])
edge('measure0','original','적용할 기준 확인',po=80,via=[(980,by),(1320,by)])

# Evidence cards are actual retrieval/use steps, not untriggered processes.
edge('search','case_ref','사례가 필요하면',sa='l',sb='l',via=[(125,p('search','l')[1]),(125,p('case_ref','l')[1])])
edge('search','reference','참고할 원리·방법',sa='b',sb='t',via=[(480,p('reference','t')[1]-35),(477.5,p('reference','t')[1]-35)])
edge('search','reuse','서식·부품이 필요하면',sa='r',sb='r',via=[(835,p('search','r')[1]),(835,p('reuse','r')[1])])
edge('search','trust','찾은 원문·자료',sa='l',sb='b',po=-30,qi=-100,via=[(95,p('search','l',-30)[1]),(95,p('trust','b')[1]+35),(380,p('trust','b')[1]+35)])
remove('absent','trust');remove('now','trust');remove('case_ref','trust');remove('reuse','trust')
edge('absent','trust','검색 결과',sa='b',sb='t',qi=-100,via=[(300,p('absent')[1]+35),(360,p('absent')[1]+35),(360,N['trust']['y']-35),(380,N['trust']['y']-35)])
edge('now','trust','조회 결과',sa='b',sb='t',qi=100,via=[(655,p('now')[1]+35),(595,p('now')[1]+35),(595,N['trust']['y']-35),(580,N['trust']['y']-35)])
edge('case_ref','trust','',sa='b',sb='l',via=[(242.5,p('case_ref')[1]+30),(125,p('case_ref')[1]+30),(125,p('trust','l')[1])])
edge('reuse','trust','',sa='b',sb='r',via=[(712.5,p('reuse')[1]+30),(835,p('reuse')[1]+30),(835,p('trust','r')[1])])
edge('version','memory','이전 기록도 대조',via=[])

# Rules and stored limits are supplied inputs. Name their consumer explicitly;
# the rule hierarchy remains a priority order, never a sequential checklist.
for k in ['ethics','principles','contract','platform','org','user_rule','style','rights','limit']:
    N[k]['kind']='reference'
    N[k]['input_role']='provided_reference'
N['rights']['applies_to']='guard';N['limit']['applies_to']='guard'
for k in ['ethics','principles','contract','platform','org','user_rule','style']:
    N[k]['reference_group']='rank'
for e in E:
    if (e['source'],e['target']) in [('rights','guard'),('limit','guard'),('rank','priority')]:
        e['kind']='reference'

edge('model','risk','목표·방법 초안',sa='l',sb='t',via=[(315,p('model','l')[1])])
edge('progress','isolation','작업',sa='l',sb='r')
remove('progress','control')
edge('record','control','기록한 작업·입력',sa='b',sb='r',via=[(1465,p('record')[1]+35),(1205,p('record')[1]+35),(1205,p('control','r',-30)[1])],qi=-30)
# Use the record already written above when evaluating the process.
remove('quality','process_eval');remove('record_read','process_eval')
N['record_read'].update(y=N['quality']['y'])
N['process_eval'].update(y=N['pack']['y'])
edge('quality','record_read','기록',sa='r',sb='l')
edge('record_read','process_eval','앞에서 남긴 기록')
for e in E:
    if (e['source'],e['target'])==('process_eval','outcome'):
        e['points']=[p('process_eval','r'),(1740,p('process_eval','r')[1]),(1740,p('outcome','r')[1]),p('outcome','r')]

# Re-check an important conclusion with counter-evidence before accepting it.
edge('identity','counter','중요 판단·근거 변경 시',sa='t',sb='t',via=[(1445,N['identity']['y']-65),(320,N['identity']['y']-65)])
remove('improve','capability')
edge('improve','testenv','개선안',sa='l',sb='r')

# An unused material is an annotation beside assignment, not a required step.
remove('plan','unused');remove('unused','progress')
N['unused'].update(x=120,y=p('plan')[1]+70,w=430,h=165)
edge('plan','unused','',kind='reference',sa='l',sb='r',via=[(585,p('plan','l')[1]),(585,p('unused','r')[1])])
edge('plan','progress','한 전문가가 직접 처리')

COPY=json.loads((ROOT/'docs/도식/단독-재료-쉬운설명.json').read_text())
assert set(COPY['materials'])==set(CAT)
assert set(COPY['blocks'])=={k for k,n in N.items() if not n['material']}
for k,copy in COPY['blocks'].items():N[k].update(copy)
for g in G:
    if g['id'] in COPY['groups']:g['title']=COPY['groups'][g['id']]
for a in A:a['text']=COPY['annotations'].get(a['text'],a['text'])
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

# Repeated columns and card rows share dimensions before text is measured.
for k in ['quality','pack','delivery','outcome','cause','improve','capability','memory2']:
    N[k].update(x=640,w=520)
for k in ['identity','wait','record_read','process_eval','wait2','memory_direct','memory_reuse']:
    N[k]['x']=1250
for k in ['counter','context2','testenv']:
    N[k].update(x=120,w=390)
N['passed']['x']=1265
material_rows=[
    ['signal','live'],['search','original'],['absent','now'],
    ['case_ref','reference','reuse'],['knowledge','experience'],
    ['ethics','principles'],['contract','platform'],['strategy','risk'],
    ['plan','state'],['progress','isolation','record'],['control','monitor'],
    ['guard','rights','limit'],['verify','counter','identity'],
    ['quality','record_read'],['pack','process_eval'],['improve','testenv'],
    *[[k for k,_,_ in items] for _,items in families],
]
for row in material_rows:
    title_lines=max(len(text_layout(N[k])[2]) for k in row)
    for k in row:N[k]['title_lines_reserved']=title_lines
for k,n in N.items():
    if n['material']:
        n['term']=CAT[n['material']]['term'];n['system']=CAT[n['material']]['system']
        n['body']=COPY['instances'].get(k,COPY['materials'][n['material']])
        z,bs,titles,body=text_layout(n)
        n['needed_height']=32+n.get('title_lines_reserved',len(titles))*(z+5)+10+len(body)*27+22
    else:
        z,bs,titles,body=text_layout(n)
        height=len(titles)*(z+5)+len(body)*25+(8 if body else 0)+28
        if n['kind'] in ('decision','decisionwide'):
            # Keep every line inside the diamond, including its narrow top/bottom.
            for i,line in enumerate(titles):
                distance=abs((i-(len(titles)-1)/2)*(z+5))+z*.65
                available=max(.12,1-measure(line,z)/n['w']-.08)
                height=max(height,2*distance/available)
        n['needed_height']=max(n['h'],math.ceil(height))

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
 ('goal','measure0'):'확인 기준',
 ('risk','strategy'):'위험 유무 확인 완료',('counter','verify'):'근거',
 ('vdecision','wait'):'확인\n불가',('capability','passed'):'결과',
 ('unused','progress'):'한 전문가가 직접 처리',
}
for e in E:
    if (e['source'],e['target'])==('absent','trust'):e['label']='검색 결과'
    if (e['source'],e['target'])==('now','trust'):e['label']='조회 결과'
    if (e['source'],e['target']) in label_edits:e['label']=label_edits[e['source'],e['target']]

def rounded(points,r=14,bridges=()):
    # Polyline corners rounded without freeform splines wandering through labels.
    ps=[]
    for q in points:
        if not ps or q!=ps[-1]:ps.append(q)
    if len(ps)<2:return ''
    def line_to(a,b):
        jumps=sorted((j for j in bridges if a[1]==b[1]==j['y'] and min(a[0],b[0])<j['x']<max(a[0],b[0])),key=lambda j:j['x'],reverse=b[0]<a[0])
        out='';direction=1 if b[0]>a[0] else -1
        for j in jumps:
            x,y,rr=j['x'],j['y'],j['radius']
            out+=f' L{x-direction*rr},{y} Q{x},{y-2*rr} {x+direction*rr},{y}'
        return out+f' L{b[0]},{b[1]}'
    d=f'M{ps[0][0]},{ps[0][1]}';last=ps[0]
    for i in range(1,len(ps)-1):
        a,b,c=ps[i-1:i+2];u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);lu=math.hypot(*u);lv=math.hypot(*v)
        rr=min(r,lu/2,lv/2)
        q=(b[0]+u[0]/lu*rr,b[1]+u[1]/lu*rr);z=(b[0]+v[0]/lv*rr,b[1]+v[1]/lv*rr)
        d+=line_to(last,q)+f' Q{b[0]},{b[1]} {z[0]},{z[1]}';last=z
    return d+line_to(last,ps[-1])
def simplify_path(points):
    result=[]
    for point in points:
        if result and math.dist(point,result[-1])<.01:continue
        while len(result)>=2:
            a,b=result[-2:]
            cross=(b[0]-a[0])*(point[1]-b[1])-(b[1]-a[1])*(point[0]-b[0])
            forward=(b[0]-a[0])*(point[0]-b[0])+(b[1]-a[1])*(point[1]-b[1])
            if abs(cross)<.01:result.pop()
            else:break
        result.append(point)
    return result

def side_of(n,point):
    # Preserve the chosen side, then use exactly its midpoint after text reflow.
    x,y=point
    return min(('t','b','l','r'),key=lambda side:{
        't':abs(y-n['y']), 'b':abs(y-n['y']-n['h']),
        'l':abs(x-n['x']), 'r':abs(x-n['x']-n['w'])}[side])

# Capture the selected faces before the final row/column alignment moves boxes.
for e in E:
    source=N.get(e['source']) or next(g for g in G if g['id']==e['source'])
    e['source_port']=side_of(source,e['points'][0])
    e['target_port']=side_of(N[e['target']],e['points'][-1])

# Text reflow stretches different shapes by different amounts. Restore layout
# constraints afterwards, so every row uses one baseline and every fan one axis.
for row in material_rows:
    y=N[row[0]]['y'];height=max(N[k]['h'] for k in row)
    for k in row:N[k].update(y=y,h=height)
N['watchtype'].update(y=N['signal']['y'],h=N['signal']['h'])
for k in ['absent','now','case_ref','reference','reuse','knowledge','experience']:
    N[k]['x']+=2.5
rank=next(g for g in G if g['id']=='rank');rank['x']-=15
for k in ['ethics','principles','contract','platform','org','user_rule','style']:
    N[k]['x']-=15
for r,items in enumerate(rule_rows):
    number=next(a for a in A if a['text']==str(r+1))
    number.update(x=rank['x']-14,y=p(items[0][0],'l')[1],anchor='end',baseline='central')
    if len(items)>1:
        note(N[items[0][0]]['x'],p(items[0][0],'b')[1]+30,
             f'같은 {r+1}순위 · 함께 적용, 충돌하면 아래에서 조정',20,600)
for k in ['law','priority']:N[k]['text_align']='start'
center_rows=[
    ['clear','communicate0'],['qualified','testenv0'],
    ['allowed','hold','handoff'],['vdecision','wait'],['more','context2'],
    ['qualityok','repair'],['receipt','wait2','delivery_repair'],
    ['learnneed','memory_direct'],['improveneed','memory_reuse'],
    ['capability','passed'],
]
for row in center_rows:
    cy=p(row[0],'r')[1]
    for k in row[1:]:N[k]['y']=cy-N[k]['h']/2
trial_gap=N['capability0']['y']-p('testenv0','b')[1]
if trial_gap<72:insert_space(N['capability0']['y'],72-trial_gap)
for fi,(_,items) in enumerate(families):
    choose=N[f'choose{fi}'];type_node=N[f'type{fi}'];out=N[f'out{fi}']
    panel=next(g for g in G if g['id']==f'opg{fi}')
    cx=panel['x']+panel['w']/2
    choose['x']=cx-choose['w']/2;out['x']=cx-out['w']/2
    type_node.update(y=choose['y'],h=choose['h'])
    # Symmetric branch/merge rails need room for a full perpendicular arrow stem.
    first=N[items[0][0]]
    insert_space(first['y'],64-(first['y']-p(choose['id'],'b')[1]))
    insert_space(out['y'],64-(out['y']-p(first['id'],'b')[1]))
    panel.update(y=choose['y']-20,h=out['y']+out['h']+20-(choose['y']-20))

# Optional evidence inputs share one inlet and one collection rail. Their
# results then pass through the common absence and reliability checks.
evidence_options={
    'now':'현재 값이 필요할 때',
    'case_ref':'사례가 필요할 때',
    'reference':'설명이나 예시가 필요할 때',
    'reuse':'양식이나 부품이 필요할 때',
}
option_top=p('search','b')[1]+72
for k in [*evidence_options,'absent','trust']:N[k].update(x=160,w=640)
def evidence_height(k):
    z,bs,titles,body=text_layout(N[k])
    return 32+len(titles)*(z+5)+10+len(body)*27+22
option_height=max(evidence_height(k) for k in evidence_options)
for i,(k,condition) in enumerate(evidence_options.items()):
    N[k].update(y=option_top+i*(option_height+32),h=option_height,
                condition=condition,text_align='start',needed_height=evidence_height(k),title_lines_reserved=1)
N['absent'].update(y=p('reuse','b')[1]+64,h=evidence_height('absent'),needed_height=evidence_height('absent'))
N['trust'].update(y=p('absent','b')[1]+32,h=evidence_height('trust'),needed_height=evidence_height('trust'))
assert p('trust','b')[1]+72<=N['version']['y']
note(160,option_top-28,'필요한 항목만 골라 확인',22,700,color=C['ink'])
note(160,N['absent']['y']-28,'모은 결과를 확인',22,700,color=C['ink'])
remove('search','absent')
for e in E:
    if e['target']=='trust' and e['source'] in {'search',*evidence_options}:e['target']='absent'
    elif (e['source'],e['target'])==('absent','trust'):e['label']=''

# Knowledge, experience and memory are separate inputs to the same context.
# Match the evidence cards above without inventing a sequential dependency.
context_sources=['knowledge','experience','memory']
for k in ['version',*context_sources]:N[k].update(x=160,w=640)
N['version'].update(h=evidence_height('version'),needed_height=evidence_height('version'))
context_source_height=max(evidence_height(k) for k in context_sources)
context_source_top=p('version','b')[1]+72
for i,k in enumerate(context_sources):
    N[k].update(y=context_source_top+i*(context_source_height+32),h=context_source_height,
                condition=COPY['labels']['version->'+k],text_align='start',
                needed_height=evidence_height(k),title_lines_reserved=1)
evidence_group=next(g for g in G if g['id']=='evidence')
context_source_merge=evidence_group['y']+evidence_group['h']-35
assert p('memory','b')[1]+64<=context_source_merge
note(160,context_source_top-28,'판단에 참고할 내용',22,700,color=C['ink'])

# Keep supplied criteria on one side of the guard. The other three sides remain
# free for the execution request, the decision, and a verified human response.
guard_references=['rights','limit']
for k in guard_references:N[k].update(x=80,w=470,text_align='start')
criterion_height=max(evidence_height(k) for k in guard_references)
criterion_top=p('control','l')[1]+72
for i,k in enumerate(guard_references):
    N[k].update(y=criterion_top+i*(criterion_height+32),h=criterion_height,needed_height=evidence_height(k))
criterion_center=(N['rights']['y']+p('limit','b')[1])/2
N['guard'].update(y=criterion_center-evidence_height('guard')/2,h=evidence_height('guard'),needed_height=evidence_height('guard'))
assert p('limit','b')[1]+40<=N['hold']['y']
note(80,criterion_top-28,'안전장치가 확인할 기준',22,700,color=C['ink'])

# The working context exists before interpretation. Later occurrences update
# the same material; they do not create it for the first time after preparation.
insert_space(N['understand']['y'],220)
mat('context_initial','현재 작업 정보',640,p('case','b')[1]+45,520,148,
    body=COPY['instances']['context_initial'])
N['context_initial'].update(term=CAT['현재 작업 정보']['term'],system=CAT['현재 작업 정보']['system'],
                            condition='처음 구성',needed_height=evidence_height('context_initial'))
N['context_initial']['h']=N['context_initial']['needed_height']
N['context']['condition']='확인 결과 반영'
N['context2']['condition']='작업 결과 반영'
remove('case','understand')
for a,b in [('case','context_initial'),('context_initial','understand')]:
    edge(a,b);E[-1].update(source_port='b',target_port='t')

# Legal precedence and rule conflicts are executable decisions, not paragraphs
# hidden inside a material card. The numbered cards remain reference inputs.
rules_group=next(g for g in G if g['id']=='rules')
old_group_bottom=evidence_group['y']+evidence_group['h']
rank_keys=['ethics','principles','contract','platform','org','user_rule','style']
rank_annotations=[a for a in A if rank['y']-100<=a['y']<=rank['y']+rank['h']+35 and a['x']>=950]
rule_nodes=[]
def flow_node(k,title,y,body='',decision=False,wide=False):
    node(k,title,985 if wide else 960,y,670 if wide else 340,90,body,
         kind='decision' if decision else 'process')
    n=N[k];z,bs,titles,lines=text_layout(n)
    height=len(titles)*(z+5)+len(lines)*25+(8 if lines else 0)+28
    if decision:
        for i,line in enumerate(titles):
            distance=abs((i-(len(titles)-1)/2)*(z+5))+z*.65
            available=max(.12,1-measure(line,z)/n['w']-.08)
            height=max(height,2*distance/available)
    n['h']=n['needed_height']=max(90,math.ceil(height))
    rule_nodes.append(k)
    return p(k,'b')[1]+72
def side_node(k,title,aligned_to,body=''):
    flow_node(k,title,0,body)
    N[k].update(x=1420,w=250)
    z,bs,titles,lines=text_layout(N[k])
    N[k]['h']=N[k]['needed_height']=len(titles)*(z+5)+len(lines)*25+(8 if lines else 0)+28
    N[k]['y']=p(aligned_to,'r')[1]-N[k]['h']/2
def route(a,b,label='',sa='b',sb='t',via=None,kind='flow'):
    if via is None and (sa in ('t','b'))!=(sb in ('t','b')):
        start,end=p(a,sa),p(b,sb)
        via=[(start[0],end[1]) if sa in ('t','b') else (end[0],start[1])]
    edge(a,b,label,kind,sa,sb,via)
    E[-1].update(source_port=sa,target_port=sb,fixed_route=True)
def collect(a,b,label='',sa='r'):
    start,end=p(a,sa),p(b,'t');yy=end[1]-36
    route(a,b,label,sa,'t',[(1685,start[1]),(1685,yy),(end[0],yy)])
def reply_loop(a,b):
    start,end=p(a,'r'),p(b,'r')
    route(a,b,'재검토','r','r',[(1730,start[1]),(1730,end[1])],kind='return')

N['law'].update(h=evidence_height('law'),needed_height=evidence_height('law'))
y=p('law','b')[1]+88
legal_top=y
for k,title in [('law_constitution','헌법 확인'),('law_statute','법률 확인'),
                ('law_decree','대통령령 확인'),('law_ministry','총리령·부령 확인')]:
    y=flow_node(k,title,y,wide=True)-40
N['law_constitution']['caption']='한국 중앙정부 법령 예'
note(985,legal_top-28,N['law_constitution']['caption'],22,700,color=C['ink'])
y+=40
y=flow_node('law_higher','상위법과\n충돌하는가?',y,decision=True)
side_node('law_higher_apply','상위법 우선 적용','law_higher','충돌하는 부분에 적용합니다.')
y=flow_node('law_conflict','같은 효력의 법이\n충돌하는가?',y,decision=True)
y=flow_node('law_special','적용할 특별\n규정이 있는가?',y,decision=True)
side_node('law_special_apply','특별 규정 우선 적용','law_special','충돌하는 부분에 적용합니다.')
y=flow_node('law_new','새 법 적용 조건 확인',y,'시행일과 경과조치를\n대조합니다.')
y=flow_node('law_settle','적용할 법적 기준 확인',y,'판결·명령과 예외 요건도 함께 확인합니다.',wide=True)
y=flow_node('law_clear','따를 법적 기준이\n명확한가?',y,decision=True)
side_node('law_wait','관련 작업 보류·확인 요청','law_clear','권한 있는 담당자에게\n불명확한 기준을 확인합니다.')
side_node('law_reply','답변의 권한·적법성 확인','law_clear','답변이 법과 적용 범위에\n맞는지 확인합니다.')
N['law_reply']['y']=p('law_wait','b')[1]+72
y=flow_node('law_confirmed','적용할 법적 기준 확정',max(y,p('law_reply','b')[1]+72),wide=True)

rank_delta=y+80-rank['y']
rank['y']+=rank_delta
for k in rank_keys:N[k]['y']+=rank_delta
for a in rank_annotations:a['y']+=rank_delta
N['priority'].update(y=rank['y']+rank['h']+135,h=evidence_height('priority'),needed_height=evidence_height('priority'))
y=flow_node('rule_conflict','충돌하는 규칙이\n있는가?',p('priority','b')[1]+72,decision=True)
y=flow_node('rule_compare','근거·권한·범위 대조',y,'규칙의 근거와 정한 사람의\n권한을 확인합니다.')
y=flow_node('rule_order','우선할 규칙을\n정할 수 있는가?',y,decision=True)
side_node('rule_apply','충돌 부분에 우선 규칙 적용','rule_order')
y=flow_node('rule_exception','허용된 예외·변경 확인',y,'예외 요건·승인 권한과\n필요한 증거를 확인합니다.')
y=flow_node('rule_candidate','적용할 기준·남은 쟁점 정리',y,wide=True)
y=flow_node('rule_resolved','적용할 기준이\n모두 정해졌는가?',y,decision=True)
side_node('rule_wait','관련 작업 보류·확인 요청','rule_resolved','결정권자에게 충돌 내용과\n확인이 필요한 점을 보냅니다.')
side_node('rule_reply','답변의 권한·적법성 확인','rule_resolved','허용된 변경인지 확인하고\n규칙을 다시 대조합니다.')
N['rule_reply']['y']=p('rule_wait','b')[1]+72
y=flow_node('rule_confirmed','확인된 기준 적용·기록',max(y,p('rule_reply','b')[1]+72),
            '함께 지킬 조건과 판단 근거를 남깁니다.',wide=True)
new_group_bottom=y+8
# Insert height into the downstream workflow, then restore the deliberately
# positioned rule section. Everything outside this section keeps its spacing.
saved_y={k:N[k]['y'] for k in ['law','priority',*rank_keys,*rule_nodes]}
saved_rank=(rank['y'],rank['h'])
legal_annotation=next(a for a in A if a['text'].startswith('한국 중앙정부'))
saved_annotations=[(a,a['y']) for a in [*rank_annotations,legal_annotation]]
insert_space(old_group_bottom+1,new_group_bottom-old_group_bottom)
for k,yy in saved_y.items():N[k]['y']=yy
rank['y'],rank['h']=saved_rank
for a,yy in saved_annotations:a['y']=yy
for g in [evidence_group,rules_group]:g['h']=new_group_bottom-g['y']
remove('law','priority')
for e in E:
    if (e['source'],e['target'])==('priority','context'):
        e.update(source='rule_confirmed',label='적용 기준 확정')
for a,b in [('law','law_constitution'),('law_constitution','law_statute'),
            ('law_statute','law_decree'),('law_decree','law_ministry'),('law_ministry','law_higher')]:route(a,b)
route('law_higher','law_higher_apply','예','r','l')
collect('law_higher_apply','law_conflict')
route('law_higher','law_conflict','아니오')
route('law_conflict','law_special','예')
collect('law_conflict','law_settle','아니오')
route('law_special','law_special_apply','예','r','l')
collect('law_special_apply','law_settle')
route('law_special','law_new','아니오')
route('law_new','law_settle')
route('law_settle','law_clear')
route('law_clear','law_confirmed','예')
route('law_clear','law_wait','아니오','r','l')
route('law_wait','law_reply','답변 도착')
reply_loop('law_reply','law')
route('law_confirmed','priority',sa='r',sb='r',
      via=[(1685,p('law_confirmed','r')[1]),(1685,p('priority','r')[1])])
route('priority','rule_conflict')
route('rule_conflict','rule_compare','예')
collect('rule_conflict','rule_candidate','아니오')
route('rule_compare','rule_order')
route('rule_order','rule_apply','예','r','l')
collect('rule_apply','rule_candidate')
route('rule_order','rule_exception','아니오')
route('rule_exception','rule_candidate')
route('rule_candidate','rule_resolved')
route('rule_resolved','rule_confirmed','예')
route('rule_resolved','rule_wait','아니오','r','l')
route('rule_wait','rule_reply','답변 도착')
reply_loop('rule_reply','priority')

# Both preparation branches are required. Their order is unspecified; the
# explicit collection step waits for evidence AND the applicable rules.
insert_space(evidence_group['y'],140)
insert_space(N['context']['y'],160)
node('checks_start','자료와 규칙을 모두 확인',600,p('measure0','b')[1]+45,600,96,
     body='차례로 확인하거나 함께 진행할 수 있습니다.')
node('checks_join','자료·규칙 확인 완료',600,evidence_group['y']+evidence_group['h']+75,600,96,
     body='두 확인이 끝나야 다음으로 넘어갑니다.')
N['checks_start'].update(control_role='all_required',required_branches=['search','original'],execution_order='unspecified')
N['checks_join'].update(control_role='all_complete',required_groups=['evidence','rules'],
                        completion_sources={'evidence':context_sources,'rules':['rule_confirmed']})
context_source_merge=evidence_group['y']+evidence_group['h']+25
for e in E:
    pair=(e['source'],e['target'])
    if e['source']=='measure0' and e['target'] in ('search','original'):
        e['label']=COPY['labels']['->'.join(pair)]
        e['source']='checks_start'
    elif e['target']=='context' and e['source'] in [*context_sources,'rule_confirmed']:
        e['label']=COPY['labels'].get('->'.join(pair),e['label'])
        e['target']='checks_join'
for a,b in [('measure0','checks_start'),('checks_join','context')]:
    edge(a,b)
    E[-1].update(source_port='b',target_port='t')

# Whole-flow review: a visible check must also control the next action. These
# repairs preserve the material catalogue and the established column layout.
def review_node(k,title,x,y,w=520,body='',kind='process',condition=None):
    node(k,title,x,y,w,90,body,kind)
    n=N[k]
    if n['material']:
        n.update(term=CAT[n['material']]['term'],system=CAT[n['material']]['system'])
        height=evidence_height(k)
    else:
        z,bs,titles,lines=text_layout(n)
        height=len(titles)*(z+5)+len(lines)*25+(8 if lines else 0)+28
        if kind=='decision':
            for i,line in enumerate(titles):
                distance=abs((i-(len(titles)-1)/2)*(z+5))+z*.65
                height=max(height,2*distance/max(.12,1-measure(line,z)/w-.08))
    n['h']=n['needed_height']=max(90,math.ceil(height))
    if condition:n['condition']=condition
    return n

# Understanding the request already uses the model; it is not first activated
# after the evidence/rule checks. Each repeated instance states its purpose.
insert_space(N['understand']['y'],220)
review_node('model_initial','AI 모델',640,p('context_initial','b')[1]+45,
            body=COPY['instances']['model_initial'],condition='처음 요청 이해')
N['model']['condition']='다음 작업 판단'
remove('context_initial','understand')
route('context_initial','model_initial');route('model_initial','understand')

# Intake supplies the received input before interpretation. The case summary is
# written only after the request's meaning/scope is clear, and then informs goals.
# Reuse the vacated space so the rest of the established chart stays in place.
intake_shift=N['context_initial']['y']-N['case']['y']
for k in ['context_initial','model_initial','understand','intent','clear','communicate0','change']:
    N[k]['y']-=intake_shift
N['case']['y']=N['goal']['y']-45-N['case']['h']
for a,b in [('signal','case'),('case','context_initial'),('clear','goal'),
            ('change','signal'),('communicate0','intent')]:remove(a,b)
route('signal','context_initial')
route('clear','case','아니오')
route('case','goal')
start,end=p('change','r'),p('signal','l')
route('change','signal','바뀐 내용 확인','r','l',[(620,start[1]),(620,end[1])])
start,end=p('communicate0','t'),p('intent','l')
return_y=N['clear']['y']-10
route('communicate0','intent','확인한 뜻·범위 반영','t','l',
      [(start[0],return_y),(610,return_y),(610,end[1])],kind='return')

# A failed evidence check cannot silently become "trusted material". Optional
# knowledge/experience/memory inputs join locally, then complete ONE branch.
review_node('evidence_usable','필요한 근거를\n쓸 수 있는가?',130,p('version','b')[1]+72,340,kind='decision')
review_node('evidence_repair','근거 보완·판단 보류',590,0,260,
            body='자료를 더 찾거나 요청합니다.\n해당 판단은 보류합니다.')
N['evidence_repair']['y']=p('evidence_usable','r')[1]-N['evidence_repair']['h']/2
review_node('evidence_use','필요한 지식·경험·기록 확인',160,p('evidence_usable','b')[1]+72,640,
            body='이번 판단에 필요한 항목만 참고합니다.')
source_top=p('evidence_use','b')[1]+72
for i,k in enumerate(context_sources):N[k]['y']=source_top+i*(context_source_height+32)
next(a for a in A if a['text']=='판단에 참고할 내용').update(y=source_top-28,text='필요한 항목만 참고')
review_node('evidence_done','판단에 쓸 자료 정리 완료',160,p('memory','b')[1]+96,640,
            body='확인한 자료와 아직 모르는 점을 함께 남깁니다.')
assert p('evidence_done','b')[1]+80<evidence_group['y']+evidence_group['h']
for k in context_sources:
    remove('version',k);remove(k,'checks_join')
    start,end=p('evidence_use','l'),p(k,'l')
    route('evidence_use',k,N[k]['condition'],'l','l',[(120,start[1]),(120,end[1])])
    E[-1]['label_node']=k
    start,end=p(k,'r'),p('evidence_done','t');yy=end[1]-48
    route(k,'evidence_done',sa='r',via=[(840,start[1]),(840,yy),(end[0],yy)])
route('version','evidence_usable')
route('evidence_usable','evidence_use','예')
route('evidence_usable','evidence_repair','아니오','r','l')
start,end=p('evidence_repair','r'),p('search','t')
route('evidence_repair','search','보완 자료 확인','r','t',
      [(860,start[1]),(860,end[1]-35),(end[0],end[1]-35)],kind='return')
start,end=p('evidence_use','r'),p('evidence_done','t');yy=end[1]-48
route('evidence_use','evidence_done','확인한 자료','r','t',[(840,start[1]),(840,yy),(end[0],yy)])
start,end=p('evidence_done','r'),p('checks_join','t')
route('evidence_done','checks_join',sa='r',via=[(840,start[1]),(840,context_source_merge),(end[0],context_source_merge)])
N['checks_join']['completion_sources']['evidence']=['evidence_done']

# Risk review precedes selecting a strategy. The choice can also request more
# information or end in a documented hold, rather than inevitably executing.
remove('model','strategy')
n=review_node('strategy_choice','어떻게 진행할까?',720,0,360,kind='decision')
insert_space(N['qualified']['y'],n['h']+132)
n['y']=p('strategy','b')[1]+60
review_node('strategy_more','부족한 정보 정리',120,0,390,
            body='더 알아야 할 내용과\n바뀐 조건을 정리합니다.')
review_node('strategy_stop','업무 보류·중단',1250,0,430,
            body='이유와 다시 시작할 조건을 남깁니다.',kind='stop')
for k in ['strategy_more','strategy_stop']:N[k]['y']=p('strategy_choice','r')[1]-N[k]['h']/2
remove('strategy','qualified')
route('strategy','strategy_choice');route('strategy_choice','qualified','진행')
route('strategy_choice','strategy_more','추가 확인','l','r')
route('strategy_choice','strategy_stop','보류·중단','r','l',kind='blocked')
start,end=p('strategy_more','l'),p('checks_start','l')
route('strategy_more','checks_start','추가\n확인','l','l',[(85,start[1]),(85,end[1])],kind='return')

# New evidence or changed conditions return to both preparation checks. Already
# checked, unchanged information can be reused on the next pass.
N['checks_start']['body']='자료와 규칙을 모두 확인합니다.\n다시 진행할 때는 바뀐 내용만 재확인합니다.'
N['checks_start']['h']=N['checks_start']['needed_height']=116
remove('context2','context')
start,end=p('context2','l'),p('checks_start','l')
route('context2','checks_start','다시\n확인','l','l',[(40,start[1]),(40,end[1])],kind='return')

# Establish progress from the plan before selecting the first operation. Space
# preparation and the decision record are both inputs of execution control.
remove('plan','progress')
route('plan','state','계획','r','l')
N['control'].update(control_role='all_complete',completion_sources=['isolation','record'])

# Accept only the expected result. Important/changed conclusions cannot bypass
# the counter-evidence check. Rejected results have a separate re-request loop.
identity_top=N['identity']['y']
old_state_top=N['state_result']['y']
review_node('identity_ok','요청한 쪽·대상·버전이\n모두 맞는가?',720,p('identity','b')[1]+72,360,kind='decision')
review_node('identity_reject','결과 반려·재요청',1250,0,430,
            body='맞지 않는 결과는 받지 않습니다.\n이유를 남기고 올바른 결과를 다시 요청합니다.')
N['identity_reject']['y']=p('identity_ok','r')[1]-N['identity_reject']['h']/2
review_node('counter_needed','중요한 판단이거나\n근거가 바뀌었는가?',720,p('identity_ok','b')[1]+72,360,kind='decision')
N['counter']['y']=p('counter_needed','l')[1]-N['counter']['h']/2
N['verify']['y']=max(p('counter','b')[1],p('counter_needed','b')[1])+72
new_state_top=p('verify','b')[1]+72
preserve={k:N[k]['y'] for k in ['identity_ok','identity_reject','counter_needed','counter','verify']}
insert_space(old_state_top,new_state_top-old_state_top)
for k,y in preserve.items():N[k]['y']=y
remove('identity','verify');remove('identity','counter');remove('counter','verify')
route('identity','identity_ok')
route('identity_ok','identity_reject','아니오','r','l',kind='blocked')
start,end=p('identity_reject','r'),p('identity','r')
route('identity_reject','identity','재확인','r','r',[(1750,start[1]),(1750,end[1])],kind='return')
route('identity_ok','counter_needed','예')
route('counter_needed','counter','예','l','r')
route('counter_needed','verify','아니오')
route('counter','verify')
remove('wait','verify')
route('wait','verify','답변·상태를 확인하고 재검사','t','r',kind='return')

# The end-of-job evaluation starts after confirmed delivery. A side branch from
# quality evaluation must not let the work skip delivery/acceptance entirely.
old_outcome_top=N['outcome']['y']
extra=N['record_read']['h']+N['process_eval']['h']+144
insert_space(old_outcome_top,extra)
N['record_read']['y']=old_outcome_top
N['process_eval']['y']=p('record_read','b')[1]+72
remove('quality','record_read');remove('receipt','outcome');remove('process_eval','outcome')
route('receipt','record_read','받아 쓸 수 있음','b','l')
route('process_eval','outcome')

# A failed improvement may be parked; the existing verified capability remains
# usable. A failed proposal must never be stored as an applied improvement.
review_node('retry_improve','개선안을 고쳐\n다시 시험할까?',1285,0,360,kind='decision')
review_node('memory_unapplied','장기 기억',1250,0,430,
            body='시험 결과와 남은 문제를 저장합니다.\n실패한 변경은 적용하지 않고 기존 방법을 유지합니다.',condition='개선 적용 보류')
passed_y=p('capability','b')[1]+72
insert_space(N['memory2']['y'],passed_y+N['passed']['h']+80-N['memory2']['y'])
N['passed'].update(x=700,y=passed_y)
N['retry_improve']['y']=p('passed','r')[1]-N['retry_improve']['h']/2
N['memory_unapplied']['y']=N['memory2']['y']
for k in ['memory2','memory_unapplied']:N[k]['h']=max(N['memory2']['h'],N['memory_unapplied']['h'])
remove('capability','passed');remove('passed','improve');remove('passed','memory2')
route('capability','passed','결과')
route('passed','retry_improve','아니오','r','l')
route('passed','memory2','예')
route('retry_improve','memory_unapplied','아니오')
start,end=p('retry_improve','r'),p('improve','r')
route('retry_improve','improve','예','r','r',[(1685,start[1]),(1685,end[1])],kind='return')
start,end=p('memory_unapplied','r'),p('finish','r')
route('memory_unapplied','finish',sa='r',sb='r',via=[(1710,start[1]),(1710,end[1])])

# Dependency review: inputs precede decisions, returned results re-enter checks,
# and preparing a change is distinct from using it in the real job.
N['context_initial']['condition']='요청·변경 반영'
N['goal']['condition']='요청 기준 초안'
N['measure0']['condition']='확인 항목·시점'
N['progress']['produces']=['operation','target','inputs','tool','current_state']
for i in range(6):N[f'choose{i}']['dispatches']='operation_selected_at_progress'

# Select the applicable version before judging whether its content is usable.
N['trust']['y'],N['version']['y']=N['version']['y'],N['trust']['y']
for a,b in [('absent','trust'),('trust','version'),('version','evidence_usable')]:remove(a,b)
route('absent','version')
route('version','trust','이번 일에 맞는 자료')
route('trust','evidence_usable')

# Evidence and rules can invalidate an apparently clear initial request/goal.
n=review_node('goal_review','목표·범위·완료 기준을\n고쳐야 하는가?',720,0,360,kind='decision')
insert_space(N['strategy']['y'],n['h']+150)
n['y']=p('model','b')[1]+60
remove('model','risk')
route('model','goal_review')
start,end=p('goal_review','b'),p('risk','t')
route('goal_review','risk','아니오',via=[(start[0],end[1]-40),(end[0],end[1]-40)])
start,end=p('goal_review','r'),p('context_initial','r')
route('goal_review','context_initial','예 · 요청·조건 재확인','r','r',
      [(1780,start[1]),(1780,end[1])],kind='return')
E[-1]['at']=(1400,start[1])

# A received approval is not automatically a valid approval.
n=review_node('approval_valid','본인·권한·승인 대상이\n모두 맞는가?',1285,0,360,kind='decision')
insert_space(next(g['y'] for g in G if g['id']=='opg0'),n['h']+100)
n['y']=p('identity0','b')[1]+64
remove('identity0','guard')
route('identity0','approval_valid')
start,end=p('approval_valid','r'),p('guard','r')
route('approval_valid','guard','예 · 다시 검사','r','r',[(1735,start[1]),(1735,end[1])],kind='return')
start,end=p('approval_valid','l'),p('handoff','l')
route('approval_valid','handoff','아니오 · 다시 요청','l','l',[(1210,start[1]),(1210,end[1])],kind='return')

# New results must pass provenance checks; waiting for acceptance must not send
# the deliverable again. Only a delivery error justifies another transmission.
remove('wait','verify')
start,end=p('wait','b'),p('identity','r')
route('wait','identity','새 결과 도착','b','r',
      [(start[0],start[1]+40),(1750,start[1]+40),(1750,end[1])],kind='return')
E[-1]['at']=(1590,start[1]+40)
remove('identity_reject','identity')
start,end=p('identity_reject','b'),p('identity','r')
route('identity_reject','identity','다시 받은 결과','b','r',
      [(start[0],start[1]+35),(1750,start[1]+35),(1750,end[1])],kind='return')
E[-1]['at']=(1590,start[1]+35)
remove('wait2','delivery')
start,end=p('wait2','t'),p('receipt','t')
route('wait2','receipt','답변·수령 상태 확인','t','t',
      [(start[0],end[1]-36),(end[0],end[1]-36)],kind='return')

# Inspect the prepared delivery package before sending it. Risk and permission
# are rechecked for this recipient/version, not inherited from an earlier tool.
pack_top=N['quality']['y']
old_delivery_top=N['delivery']['y']
N['pack']['y']=pack_top
review_node('risk_delivery','빠진 위험 확인',640,p('pack','b')[1]+64,
            body='받을 사람과 사용할 상황에서 생길 문제를 확인합니다.\n빠진 조건이나 넘기면 안 되는 정보가 없는지 살핍니다.',condition='전달 전')
N['quality']['y']=p('risk_delivery','b')[1]+64
N['qualityok']['y']=p('quality','b')[1]+64
N['repair']['y']=p('qualityok','l')[1]-N['repair']['h']/2
review_node('delivery_guard','안전장치',640,p('qualityok','b')[1]+80,
            body='받는 사람·명의·파일·공개 범위를 현재 승인과 대조합니다.\n지킬 규칙과 권한·한도를 다시 확인합니다.',condition='전달 직전')
review_node('delivery_allowed','전달해도 되는가?',720,p('delivery_guard','b')[1]+64,360,kind='decision')
review_node('delivery_approval','사람에게 넘기기',1250,0,430,
            body='필요한 승인이나 수정 조건을 확인합니다.\n답한 사람의 권한과 승인한 대상·버전도 대조합니다.',condition='전달 승인 확인')
review_node('delivery_hold','전달 보류·중단',120,0,390,
            body='준비한 결과를 보존하고\n이유와 재개 조건을 남깁니다.',kind='stop')
for k in ['delivery_approval','delivery_hold']:N[k]['y']=p('delivery_allowed','r')[1]-N[k]['h']/2
new_delivery_top=max(p(k,'b')[1] for k in ['delivery_allowed','delivery_approval','delivery_hold'])+80
kept=['pack','risk_delivery','quality','qualityok','repair','delivery_guard','delivery_allowed','delivery_approval','delivery_hold']
saved_y={k:N[k]['y'] for k in kept}
insert_space(old_delivery_top,new_delivery_top-old_delivery_top)
for k,y in saved_y.items():N[k]['y']=y
for a,b in [('more','quality'),('qualityok','pack'),('pack','delivery')]:remove(a,b)
route('more','pack','예')
route('pack','risk_delivery')
route('risk_delivery','quality')
route('qualityok','delivery_guard','예')
route('delivery_guard','delivery_allowed')
route('delivery_allowed','delivery','예')
route('delivery_allowed','delivery_approval','확인 필요','r','l',kind='blocked')
route('delivery_allowed','delivery_hold','전달 불가','l','r',kind='blocked')
start,end=p('delivery_approval','t'),p('delivery_guard','r')
route('delivery_approval','delivery_guard','답변 확인 후 재검사','t','r',[(start[0],end[1])],kind='return')
N['receipt']['title']='전달·인수 상태는?'
start,end=p('receipt','b'),p('delivery_guard','r')
route('receipt','delivery_guard','전달 실패\n재시도','b','r',
      [(start[0],start[1]+40),(1750,start[1]+40),(1750,end[1])],kind='return')
E[-1]['at']=(1550,start[1]+40)
remove('delivery_repair','repair')
start,end=p('delivery_repair','l'),p('repair','l')
route('delivery_repair','repair','수정','l','l',[(85,start[1]),(85,end[1])],kind='return')
N['process_eval']['condition']='인수 후 회고'

# Future effects have a scheduled follow-up, while the current job can close.
n=review_node('effect_wait','대기·후속 관리',1250,0,430,
            body='나중에 확인할 효과의 담당자와 날짜를 정합니다.\n확인 시점이 오면 성과 추적으로 돌아갑니다.',condition='뒤늦게 나타나는 효과')
insert_space(N['learnneed']['y'],n['h']+125)
n['y']=p('outcome','b')[1]+75
start,end=p('outcome','b'),p('effect_wait','t')
route('outcome','effect_wait','나중에 확인할 효과',via=[(start[0],start[1]+35),(end[0],start[1]+35)])
start,end=p('effect_wait','r'),p('outcome','r')
route('effect_wait','outcome','확인 시점 도래','r','r',[(1730,start[1]),(1730,end[1])],kind='return')
N['outcome'].update(control_role='current_result_with_optional_followup')

# Prepare a safe test space before changing the proposal. Passing the test
# permits a distinct application step; merely storing memory is not deployment.
N['improve']['condition']='시험용 개선안'
for a,b in [('improveneed','improve'),('improve','testenv'),('testenv','capability')]:remove(a,b)
start,end=p('improveneed','b'),p('testenv','t')
route('improveneed','testenv','예',via=[(start[0],end[1]-40),(end[0],end[1]-40)])
route('testenv','improve','준비됨','r','l')
route('improve','capability','개선안 시험')
n=review_node('improve_apply','능력 개선·확장',640,0,520,
            body='시험을 통과한 범위와 버전만 실제 업무에 반영합니다.\n이후 성과를 살펴 문제가 생기면 다시 보완합니다.',condition='시험 통과 후 적용')
old_memory_y=N['memory2']['y']
insert_space(old_memory_y,n['h']+80)
n['y']=old_memory_y
remove('passed','memory2')
route('passed','improve_apply','예')
route('improve_apply','memory2','적용 내용 기록')

# A normal "no" branch is not an error/stop. Labelled work choices execute one
# operation, validate its result, and then choose the next required operation.
normal_branches={('clear','case'),('learnneed','memory_direct'),('improveneed','memory_reuse'),
                 ('more','context2'),('receipt','wait2'),*[(f'type{i}',f'type{i+1}') for i in range(5)]}
for e in E:
    if (e['source'],e['target']) in normal_branches:e['kind']='flow'
for i in range(6):N[f'choose{i}'].update(selection='one_operation_per_pass')
context_source_merge=evidence_group['y']+evidence_group['h']+25
remove('evidence_done','checks_join')
start,end=p('evidence_done','r'),p('checks_join','t')
route('evidence_done','checks_join',sa='r',via=[(840,start[1]),(840,context_source_merge),(end[0],context_source_merge)])

def center_route(e):
    if e.get('fixed_route'):
        e['points']=simplify_path(e['points'])
        start,end=p(e['source'],e['source_port']),p(e['target'],e['target_port'])
        if len(e['points']) == 2 and start[0] != end[0] and start[1] != end[1]:
            sa, sb = e['source_port'], e['target_port']
            if sa in ('t','b') and sb in ('t','b'):
                mid=(start[1]+end[1])/2
                e['points']=[start,(start[0],mid),(end[0],mid),end]
            elif sa in ('l','r') and sb in ('l','r'):
                mid=(start[0]+end[0])/2
                e['points']=[start,(mid,start[1]),(mid,end[1]),end]
            elif sa in ('t','b'):
                e['points']=[start,(start[0],end[1]),end]
            else:
                e['points']=[start,(end[0],start[1]),end]
        if len(e['points'])>2:
            if e['source_port'] in ('t','b'):e['points'][1]=(start[0],e['points'][1][1])
            else:e['points'][1]=(e['points'][1][0],start[1])
            if e['target_port'] in ('t','b'):e['points'][-2]=(end[0],e['points'][-2][1])
            else:e['points'][-2]=(e['points'][-2][0],end[1])
        e['points'][0],e['points'][-1]=start,end
        e['points']=simplify_path(e['points'])
        return
    source=N.get(e['source']) or next(g for g in G if g['id']==e['source'])
    target=N.get(e['target']) or next(g for g in G if g['id']==e['target'])
    old=e['points'];sa=e['source_port'];sb=e['target_port']
    start,end=p(e['source'],sa),p(e['target'],sb)
    if len(old)==2:
        if start[0]==end[0] or start[1]==end[1]:points=[start,end]
        elif sa in ('t','b') and sb in ('t','b'):
            mid=(start[1]+end[1])/2;points=[start,(start[0],mid),(end[0],mid),end]
        elif sa in ('l','r') and sb in ('l','r'):
            mid=(start[0]+end[0])/2;points=[start,(mid,start[1]),(mid,end[1]),end]
        elif sa in ('t','b'):points=[start,(start[0],end[1]),end]
        else:points=[start,(end[0],start[1]),end]
    else:
        core=old[1:-1]
        first=(start[0],core[0][1]) if sa in ('t','b') else (core[0][0],start[1])
        last=(end[0],core[-1][1]) if sb in ('t','b') else (core[-1][0],end[1])
        points=[start,first,*core,last,end]
    points=simplify_path(points)
    # A few old routes had diagonal intermediate segments. Make their elbow explicit.
    fixed=[points[0]]
    for point in points[1:]:
        before=fixed[-1]
        if abs(point[0]-before[0])>.01 and abs(point[1]-before[1])>.01:
            fixed.append((before[0],point[1]))
        fixed.append(point)
    points=simplify_path(fixed)
    pair=(e['source'],e['target'])
    # Use a different midpoint when an incoming and outgoing line would overlap.
    if pair==('state','progress'):
        sa='b';sb='t';start=p('state',sa);end=p('progress',sb);yy=end[1]-40
        points=[start,(start[0],yy),(end[0],yy),end]
    elif pair==('record','control'):
        sb='t';end=p('control','t');yy=end[1]-35
        points=[start,(start[0],yy),(end[0],yy),end]
    elif pair==('identity0','guard'):
        sa=sb='r';start=p('identity0',sa);end=p('guard',sb)
        points=[start,(1735,start[1]),(1735,end[1]),end]
        e['at']=((1735+end[0])/2,end[1])
    elif e['source']=='version' and e['target'] in context_sources:
        sa=sb='l';start=p('version',sa);end=p(e['target'],sb)
        points=[start,(120,start[1]),(120,end[1]),end]
        e['label_node']=e['target']
    elif e['source']=='checks_start' and e['target'] in ('search','original'):
        sa='b';sb='t';start=p('checks_start',sa);end=p(e['target'],sb)
        yy=start[1]+40
        points=[start,(start[0],yy),(end[0],yy),end]
        e['at']=((start[0]+end[0])/2,yy)
    elif e['target']=='checks_join' and e['source'] in context_sources:
        sa='r';sb='t';start=p(e['source'],sa);end=p('checks_join',sb)
        points=[start,(840,start[1]),(840,context_source_merge),(end[0],context_source_merge),end]
    elif pair==('rule_confirmed','checks_join'):
        sa='b';sb='t';start=p('rule_confirmed',sa);end=p('checks_join',sb)
        points=[start,(start[0],context_source_merge),(end[0],context_source_merge),end]
        e['at']=((start[0]+end[0])/2,context_source_merge)
    elif e['target']=='guard' and e['source'] in guard_references:
        sa='r';sb='l';start=p(e['source'],sa);end=p('guard',sb)
        points=[start,(595,start[1]),(595,end[1]),end]
        e['label_in_body']=e['source']
    elif e['source']=='search' and e['target'] in evidence_options:
        sa=sb='l';start=p('search',sa);end=p(e['target'],sb)
        points=[start,(120,start[1]),(120,end[1]),end]
        e['label_node']=e['target']
    elif e['target']=='absent' and e['source'] in {'search',*evidence_options}:
        sa='r';sb='t';start=p(e['source'],sa);end=p('absent',sb)
        merge_y=end[1]-32
        points=[start,(840,start[1]),(840,merge_y),(end[0],merge_y),end]
        if e['source']=='search':
            e['label']='검색 결과';e['at']=((start[0]+840)/2,start[1])
        elif e['source']=='now':
            # The current-value card already describes its query result.
            e['label_in_body']=e['source']
    elif pair==('absent','trust'):
        sa='b';sb='t';start=p('absent',sa);end=p('trust',sb)
        points=[start,end]
    if pair==('search','case_ref'):e['label']='사례 필요'
    # Direct neighbours should not keep a tiny staircase from their old positions.
    candidate=None
    if sa in ('l','r') and sb in ('l','r') and sa!=sb and abs(start[1]-end[1])<.01:
        candidate=[start,end]
    elif sa in ('t','b') and sb in ('t','b') and sa!=sb and abs(start[0]-end[0])<.01:
        candidate=[start,end]
    elif len(old)<=4 and (sa in ('t','b'))!=(sb in ('t','b')):
        corner=(start[0],end[1]) if sa in ('t','b') else (end[0],start[1])
        candidate=[start,corner,end]
    bundled_route=((e['source']=='search' and e['target'] in evidence_options) or
                   (e['target']=='absent' and e['source'] in {'search',*evidence_options}) or
                   (e['source']=='version' and e['target'] in context_sources) or
                   (e['target']=='checks_join' and e['source'] in [*context_sources,'rule_confirmed']) or
                   (e['target']=='guard' and e['source'] in guard_references))
    if candidate and not bundled_route:
        candidate=simplify_path(candidate)
        outward={'t':(0,-1),'b':(0,1),'l':(-1,0),'r':(1,0)}
        facing=all(sum((q[i]-point[i])*outward[side][i] for i in range(2))>0
                   for side,point,q in [(sa,candidate[0],candidate[1]),(sb,candidate[-1],candidate[-2])])
        def hits_box(a,b,n):
            return (min(a[0],b[0])<n['x']+n['w']-1 and max(a[0],b[0])>n['x']+1 and
                    min(a[1],b[1])<n['y']+n['h']-1 and max(a[1],b[1])>n['y']+1)
        blocked=any(hits_box(a,b,n) for a,b in zip(candidate,candidate[1:])
                    for k,n in N.items() if k not in pair)
        if facing and not blocked:points=candidate
    e.update(points=simplify_path(points),source_port=sa,target_port=sb)

for e in E:
    center_route(e)
    e['label']=COPY['labels'].get(e['source']+'->'+e['target'],e['label'])
    end=e['points'][-1];before=next(q for q in reversed(e['points'][:-1]) if math.dist(q,end)>1)
    length=math.dist(before,end);u=((end[0]-before[0])/length,(end[1]-before[1])/length)
    tip=end;base=(tip[0]-u[0]*14,tip[1]-u[1]*14)
    e['arrow']=[tip,(base[0]-u[1]*6,base[1]+u[0]*6),(base[0]+u[1]*6,base[1]-u[0]*6)]

# Apply the final reader review once, after the inherited layout has settled.
# Edge labels here are authoritative; old copy overrides must not replace them.
import runpy
repairs = runpy.run_path(str(ROOT/'docs/도식/단독-재료-최종교정.py'))
repair = repairs['apply']
H = repair(N,E,G,A,review_node,insert_space,p,route,text_layout)
# Description edits are applied last so layout migrations cannot restore
# older copy. Keep titles, node positions and workflow edges unchanged.
descriptions=COPY['final_descriptions']
for k,body in descriptions.items():
    if k in N:N[k]['body']=body
H = repairs['place_usage'](N,E,G,A,review_node,insert_space,p,route,text_layout,descriptions,COPY['support_roles'],H)
assert set(descriptions)=={k for k,n in N.items() if n['body']},'description coverage changed'
H = repairs['draw_usage'](N,E,G,A,review_node,insert_space,p,route,text_layout,H)
for e in E:
    center_route(e)
polish = runpy.run_path(str(ROOT/'docs/도식/단독-재료-배치교정.py'))
H = polish['apply'](N,E,G,A,insert_space,p,text_layout,H,measure)
clarification = runpy.run_path(str(ROOT/'docs/도식/단독-재료-분기교정.py'))
H = clarification['apply'](N,E,G,A,review_node,insert_space,p,H)
for e in E:
    center_route(e)
polish['finish_routes'](N,E,G,A,p,measure)
for e in E:
    center_route(e)
    end=e['points'][-1];before=next(q for q in reversed(e['points'][:-1]) if math.dist(q,end)>1)
    length=math.dist(before,end);u=((end[0]-before[0])/length,(end[1]-before[1])/length)
    base=(end[0]-u[0]*14,end[1]-u[1]*14)
    e['arrow']=[end,(base[0]-u[1]*6,base[1]+u[0]*6),(base[0]+u[1]*6,base[1]-u[0]*6)]

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

# The attached header belongs to the working area; only the white cards are
# workflow steps. Category colour stays in the small badges on those cards.
SCOPE_STYLE={
    'model':dict(accent='#334E82',fill='#F0F4FA',header='#DEE7F5',border='#AFBED5'),
    'global_tools':dict(accent='#475A70',fill='#F4F6F9',header='#E3E9F0',border='#BCC8D5'),
    'live':dict(accent='#226C66',fill='#EFF6F4',header='#DCEDE8',border='#AFCBC5'),
    'isolation':dict(accent='#596579',fill='#F7F8FA',header='#E7ECF2',border='#B8C2CF'),
}
def scope_headings(g):
    if not g.get('support_scope') and not g['id'].startswith('opg'):return []
    sources=g.get('scope_sources',['isolation']);parts=[];source_index=0
    for j,line in enumerate(g.get('title_lines',[g['title']])):
        y=g['y']+37+j*32
        if line.startswith('('):
            parts.append(dict(kind='condition',text=line,x=g['x']+22,y=y,size=20))
            continue
        name,sep,condition=line.partition(' (')
        source=sources[min(source_index,len(sources)-1)];source_index+=1
        width=measure(name,22)
        parts.append(dict(kind='name',text=name,x=g['x']+22,y=y,size=22,source=source))
        if sep:parts.append(dict(kind='condition',text='('+condition,x=g['x']+22+width+12,y=y,size=20))
    return parts
# The receipt retry crosses the reply-return line once. A visible line jump
# distinguishes that crossing from a junction; it is included in the model.
bridges=[]
for i,e in enumerate(E):
    for j,f in enumerate(E):
        if i == j:continue
        for a,b in zip(e['points'],e['points'][1:]):
            if a[1]!=b[1]:continue
            for c,z in zip(f['points'],f['points'][1:]):
                if c[0]!=z[0]:continue
                if min(a[0],b[0])<c[0]<max(a[0],b[0]) and min(c[1],z[1])<a[1]<max(c[1],z[1]):
                    bridges.append(dict(over_edge=i,under_edge=j,x=c[0],y=a[1],radius=12))
occupied=[dict(x=j['x']-16,y=j['y']-28,w=32,h=32) for j in bridges]
for g in G:
    if g['title']:
        headings=scope_headings(g)
        if headings:
            occupied.append(dict(x=g['x'],y=g['y'],w=g['w'],h=max(part['y'] for part in headings)+12-g['y']))
            continue
        z=g.get('title_size',27)
        for j,line in enumerate(g.get('title_lines',[g['title']])):
            occupied.append(dict(x=g['x']+22,y=g['y']+37+j*32-z,w=measure(line,z),h=z+5))
for a in A:
    w=measure(a['text'],a['size']);x=a['x']-(w/2 if a['anchor']=='middle' else 0)
    occupied.append(dict(x=x,y=a['y']-a['size'],w=w,h=a['size']+5))
arrow_bounds=[]
for e in E:
    xs=[p[0] for p in e['arrow']];yy=[p[1] for p in e['arrow']]
    arrow_bounds.append(dict(x=min(xs)-2,y=min(yy)-2,w=max(xs)-min(xs)+4,h=max(yy)-min(yy)+4))
unplaced=[]
for i,e in enumerate(E):
    if not e['label'] or e.get('label_node') or e.get('label_in_body'):continue
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
            if any(j!=i and any(line_rect(c,z,r,pad=-5) for c,z in zip(other['points'],other['points'][1:])) for j,other in enumerate(E)):continue
            candidates.append((math.dist((x,y),preferred)+(60 if abs(b[1]-a[1])>abs(b[0]-a[0]) else 0),x,y,r))
    if candidates:
        _,x,y,r=min(candidates,key=lambda c:c[0]);e['at']=(x,y);e['label_rect']=r;occupied.append(r)
    else:
        e['label_rect']=label_box(e['label'],*preferred);e['at']=preferred;unplaced.append((i,e['source'],e['target'],e['label']))
if unplaced:raise RuntimeError('LABELS_NEED_PLACEMENT '+json.dumps(unplaced,ensure_ascii=False))
names=Counter(n['material'] for n in N.values() if n['material'])
names.update(g['material'] for g in G if g.get('material'))
assert set(names)==set(CAT),(set(CAT)-set(names),set(names)-set(CAT))
model=dict(width=W,height=H,nodes=N,groups=G,edges=E,annotations=A,bridges=bridges,illustrations=[],catalog=CAT,system_styles=SYSTEM_STYLE,system_mapping=TERM_SYSTEMS,
           visual_style=dict(scope_styles=SCOPE_STYLE,card_fill='#FFFFFF',card_border='#B7C4D2',scope_heading='integrated header band',category_style='tinted badge'),
           source_prefix_sha256=hashlib.sha256(PREFIX.encode()).hexdigest())
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   '<title>한 건을 한 전문가가 처리할 때의 재료 연결 구조</title>','<rect width="100%" height="100%" fill="white"/>',f'<g font-family="Apple SD Gothic Neo,Noto Sans CJK KR,sans-serif" fill="{C["ink"]}">']
for g in sorted(G,key=lambda g:g['w']*g['h'],reverse=True):
    x,y,w,h=(g[k] for k in ('x','y','w','h'))
    scope_style=SCOPE_STYLE[g.get('scope_sources',['isolation'])[0]] if g.get('support_scope') or g['id'].startswith('opg') else None
    dash='' if g.get('border_style')=='solid' else ' stroke-dasharray="3 9"'
    fill=scope_style['fill'] if scope_style else 'none'
    stroke=scope_style['border'] if scope_style else C['border']
    if scope_style and g.get('scope_sources',['isolation'])==['isolation']:dash=' stroke-dasharray="7 6"'
    o.append(f'<rect class="scope-border" data-id="{g["id"]}" x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{dash}/>')
    headings=scope_headings(g)
    if headings:
        bottom=max(part['y'] for part in headings)+12
        o.append(f'<path class="scope-header-band" data-scope="{g["id"]}" d="M{x+20} {y}H{x+w-20}Q{x+w} {y} {x+w} {y+20}V{bottom}H{x}V{y+20}Q{x} {y} {x+20} {y}Z" fill="{scope_style["header"]}"/>')
        o.append(f'<path d="M{x} {bottom}H{x+w}" fill="none" stroke="{stroke}" stroke-width="1"/>')
        for part in headings:
            if part['kind']=='name':color=SCOPE_STYLE[part['source']]['accent'];weight=750
            else:color='#57677C';weight=500
            o.append(f'<text class="annotation scope-heading" data-scope="{g["id"]}" x="{part["x"]}" y="{part["y"]}" font-size="{part["size"]}" font-weight="{weight}" fill="{color}">{esc(part["text"])}</text>')
    elif g['title']:
        for j,line in enumerate(g.get('title_lines',[g['title']])):
            o.append(f'<text class="annotation" x="{x+22}" y="{y+37+j*32}" font-size="{g.get("title_size",27)}" font-weight="800">{esc(line)}</text>')
    if g.get('usage_caption'):
        for j,line in enumerate([g['usage_caption'],*g.get('usage_caption_extra',[])]):
            o.append(f'<text class="annotation group-usage" x="{x+22}" y="{y+36+j*28}" font-size="21" fill="{C["muted"]}">{esc(line)}</text>')
for i,e in sorted(enumerate(E),key=lambda item:any(j['over_edge']==item[0] for j in bridges)):
    col=C[{'flow':'blue','blocked':'red','return':'yellow','reference':'muted'}[e['kind']]]
    route=e['points'] if e['kind']=='reference' else e['points'][:-1]+[e['arrow'][0]]
    dash=' stroke-dasharray="6 6"' if e['kind']=='reference' else ''
    jumps=[j for j in bridges if j['over_edge']==i]
    for j in jumps:
        x,y,rr=j['x'],j['y'],j['radius']
        o.append(f'<path class="edge-bridge" data-over="e{i}" data-under="e{j["under_edge"]}" d="M{x-rr},{y} Q{x},{y-2*rr} {x+rr},{y}" fill="none" stroke="white" stroke-width="8"><title>서로 연결되지 않는 선</title></path>')
    o.append(f'<path class="edge" data-id="e{i}" d="{rounded(route,bridges=jumps)}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linecap="round"{dash}/>')
for k,n in N.items():
    x,y,w,h=(n[t] for t in ('x','y','w','h'));kind=n['kind']
    o.append(f'<g class="node" data-id="{k}" data-material="{esc(n["material"] or "")}" data-system="{n.get("term","")}">')
    palette=SYSTEM_STYLE[n['term']] if n['material'] else None
    fill='#FFFFFF'
    if n.get('usage_material'):fill='#F3F6FA'
    if kind in ('decision','decisionwide'):
        fill='#FFF7DD';shape=f'<path class="shape" d="M{x+w/2} {y}L{x+w} {y+h/2}L{x+w/2} {y+h}L{x} {y+h/2}Z"'
    else:
        if kind in ('terminal','stop'):fill=C['green'] if kind=='terminal' else '#FFF0EC'
        if kind=='unused':fill='#F3F5F7'
        shape=f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if kind in ("terminal","stop") else 12}"'
    o.append(shape+f' fill="{fill}" stroke="#B7C4D2" stroke-width="1.6"/>')
    z,bs,titles,body=text_layout(n)
    if palette:
        badge=n['system']+(' · 이 상황에서는 미사용' if kind=='unused' else ' · '+n.get('relation_label','참조 기준') if kind=='reference' else '')
        o.append(f'<rect class="category-badge" x="{x+10}" y="{y+6}" width="{measure(badge,17)+12}" height="26" rx="6" fill="{palette["fill"]}"/>')
        o.append(f'<text class="system-label" x="{x+16}" y="{y+25}" font-size="17" font-weight="700" fill="{palette["accent"]}">{esc(badge)}</text>')
        if n.get('condition'):
            o.append(f'<text class="node-condition" x="{x+w-16}" y="{y+25}" text-anchor="end" font-size="18" font-weight="600" fill="{palette["accent"]}">{esc(n["condition"])}</text>')
        yy=y+35+z
    else:
        total=len(titles)*(z+5)+len(body)*25+(8 if body else 0)+(len(n.get('usage_lines',[]))*23+26 if n.get('usage_lines') else 0);yy=y+(h-total)/2+z
    text_anchor=n.get('text_align','middle');text_x=x+16 if text_anchor=='start' else x+w/2
    for s in titles:o.append(f'<text class="node-title" x="{text_x}" y="{yy}" text-anchor="{text_anchor}" font-size="{z}" font-weight="800">{esc(s)}</text>');yy+=z+5
    if palette:yy+=(n.get('title_lines_reserved',len(titles))-len(titles))*(z+5)
    yy+=8 if body else 0
    for s in body:o.append(f'<text class="node-body" x="{text_x}" y="{yy}" text-anchor="{text_anchor}" font-size="{bs}" fill="{C["muted"]}">{esc(s)}</text>');yy+=27 if palette else 25
    if n.get('usage_lines'):
        cy=y+h-14-(len(n['usage_lines'])-1)*23
        o.append(f'<path d="M{x+16} {cy-22}H{x+w-16}" stroke="{C["border"]}" stroke-width="1"/>')
        for s in n['usage_lines']:
            o.append(f'<text class="material-use" x="{x+w/2}" y="{cy}" text-anchor="middle" font-size="18" font-weight="600" fill="#32627A">{esc(s)}</text>')
            cy+=23
    o.append('</g>')
for i,e in enumerate(E):
    if not e['label'] or e.get('label_node') or e.get('label_in_body'):continue
    pts=e['points'];x,y=e['at'] or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
    lines=e['label'].split('\n');tw=e['label_rect']['w'];th=e['label_rect']['h']
    col=C[{'flow':'blue','blocked':'red','return':'yellow','reference':'muted'}[e['kind']]]
    o.append(f'<g class="edge-label" data-edge="e{i}"><rect x="{x-tw/2}" y="{y-th/2}" width="{tw}" height="{th}" rx="6" fill="white" stroke="#C9D5E2" stroke-width="1"/>')
    for j,s in enumerate(lines):o.append(f'<text x="{x}" y="{y-th/2+24+j*26}" text-anchor="middle" font-size="20" font-weight="600">{esc(s)}</text>')
    o.append('</g>')
for a in A:
    baseline=f' dominant-baseline="{a["baseline"]}"' if a.get('baseline') else ''
    o.append(f'<text class="annotation" x="{a["x"]}" y="{a["y"]}" font-size="{a["size"]}" font-weight="{a["weight"]}" fill="{a["color"]}" text-anchor="{a["anchor"]}"{baseline}>{esc(a["text"])}</text>')
for i,e in enumerate(E):
    if e['kind']=='reference':continue
    col=C[{'flow':'blue','blocked':'red','return':'yellow','reference':'muted'}[e['kind']]]
    o.append(f'<polygon class="arrowhead" data-edge="e{i}" points="'+ ' '.join(f'{x},{y}' for x,y in e['arrow'])+f'" fill="{col}"/>')
o+=['</g>','<metadata>'+esc(json.dumps(model,ensure_ascii=False))+'</metadata>','</svg>']
(ROOT/'docs/images/expert-definition/solo-material-relations.svg').write_text('\n'.join(o))
(ROOT/'docs/도식/단독-재료-연결구조.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(materials=len(names),nodes=len(N),edges=len(E),width=W,height=H),ensure_ascii=False))
