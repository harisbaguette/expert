#!/usr/bin/env python3
"""One expert, one case: exact text and manually routed operation diagram."""
from pathlib import Path
import importlib.util, json, hashlib

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('materials',Path(__file__).with_name('사용-구조-생성.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.COL.update(bg='#FFFFFF',panel='#F7F9FC',ink='#19344F',muted='#52677C',blue='#2872D5',red='#D85860',yellow='#D99800',gray='#96A5B5',line='#CAD5E1')
d=m.Drawing('solo');d.width=2160
d.groups['TITLE']={'title':'단독 상황 — 한 건 · 한 전문가'}

def mat(key,name,x,y,w=350,note=None,kind='action'):
    return d.material(key,name,x,y,w,note=note,kind=kind)
def box(key,title,x,y,w=300,note='',kind='process'):
    return d.box(key,title,x,y,w,body=note,kind=kind)
def bottom(key):
    n=d.nodes.get(key) or d.groups[key];return n['y']+n['h']
def mid(key):return d.port(key,'b')[0]
def E(a,b,kind='flow',label='',sa='b',sb='t',via=(),at=None):
    d.edge(a,b,kind,label,sa,sb,via,at)
def row(prefix,names,x,y,w,notes=None,links=True,kind='action'):
    gap=44;cw=(w-gap*(len(names)-1))/len(names);ids=[]
    for i,n in enumerate(names):
        k=f'{prefix}{i}';mat(k,n,x+i*(cw+gap),y,cw,(notes or {}).get(n),kind);ids.append(k)
        if i and links:E(ids[-2],k,sa='r',sb='l')
    return ids,max(bottom(k) for k in ids)
def panel(key,x,y,w,h,title,sub=''):d.panel(key,x,y,w,h,title,sub)

# A real start and two optional event sources. No false sequence between observers.
box('start','요청 도착',100,36,240,kind='terminal')
mat('notice','먼저 알아채기',540,30,420,'주변 감시를 맡았을 때\n발견한 문제·기회를 시작 신호로 알림','support')
mat('watch','변경 감시·반영',1080,30,440,'감시를 맡았거나 규칙이 다투어질 때\n바뀐 근거와 영향받는 작업을 재확인','support')
mat('unused','나눠 맡기기',1660,30,400,'이 상황에서는 사용하지 않음\n한 전문가가 모든 작업을 직접 수행','support')
panel('INTAKE',60,210,2040,217,'요청 이해')
intro,ib=row('i',['시작 신호','업무별 정보','정보·자료 이해','지시·의도 파악','문제·목표·완료 조건'],80,270,2000,{
 '시작 신호':'새 요청·변경·약속한 시점을\n새 일 또는 기다리던 일에 연결',
 '업무별 정보':'대상·요청·기한·현재 상황 수집',
 '정보·자료 이해':'자료의 뜻·맥락을 읽고\n사실·주장·추정을 구분',
 '지시·의도 파악':'원하는 결과와 맡긴 범위 확인\n불분명하면 질문해 바로잡음',
 '문제·목표·완료 조건':'해결할 문제·목표와\n완료를 판단할 기준을 정함'})
E('start','i0',via=[(220,185),(mid('i0'),185)])
E('notice','i0',via=[(750,170),(350,170),(350,250)],sb='t')
d.edges[-1]['points'][-1]=(350,270)
E('watch','i1',via=[(1300,190),(mid('i1'),190)])

# Persistent support is a scope, not a sequence of tasks.
panel('PERSIST',60,490,2040,300,'업무를 수행하는 동안 계속 작동',
      '아래 기반은 모든 판단·실행·대기·재개에 적용된다. 상자를 차례로 실행한다는 뜻은 아니다.')
row('base',['실행 제어','작업 진행·연결','현재 진행 상태','판단 근거 기록'],80,580,2000,links=False,kind='support',notes={
 '실행 제어':'조건에 맞춰 AI·함수·도구 호출\n결과·오류·대기·재개를 연결',
 '작업 진행·연결':'선행 결과가 준비된 작업을 시작\n끝까지 다음 작업과 검사를 이어감',
 '현재 진행 상태':'완료·대기·승인·남은 일을 유지\n끝난 외부 처리는 중복 실행하지 않음',
 '판단 근거 기록':'입력·판단·실행·검증의 근거\n변경 이유와 사용 판본을 기록'})
row('ops',['분리 실행','운영 감시·복구'],80,705,1000,links=False,kind='support',notes={
 '분리 실행':'업무·코드·시험 공간과 권한을 분리',
 '운영 감시·복구':'장애·지연을 감시하고 저장 상태로 복구'})
mat('context','현재 작업 정보',1130,705,460,'판단할 때마다 목표·자료·규칙·상태를 구성','support')
mat('model','AI 모델',1640,705,440,'구성한 정보로 이해·판단·생성','support')
E('context','model','apply',sa='r',sb='l')
d.groups['PERSIST']['h']=max(bottom('ops0'),bottom('ops1'),bottom('context'),bottom('model'))-490+20

# Inputs and requirements are adjacent sources used by the continuing main flow.
Y=bottom('PERSIST')+90
panel('DATA',60,Y,760,920,'필요한 근거를 갖춘다','이번 판단에 필요한 자료·지식만 가져온다.')
data=['현재 값·상태 확인','적용 사례','참고 자료','재사용 자료','장기 기억','업무 지식','실전 경험·감각']
ids,dy=d.grid('src',data,80,Y+88,720,2,kind='support',notes={
 '현재 값·상태 확인':'현재 값·처리 상태가 중요할 때 조회',
 '적용 사례':'비슷한 사례의 조건·근거·결과 비교',
 '참고 자료':'필요한 원리·방법·표현을 참고',
 '재사용 자료':'이용 권한·판본·환경 확인 후 재사용',
 '장기 기억':'관련된 이전 결정·약속·교훈을 꺼냄',
 '업무 지식':'개념·원리·적용 조건·예외로 해석',
 '실전 경험·감각':'경험의 단서·대응 요령을 현재 조건과 대조'})
mat('trust','근거의 신뢰성·적합성',80,dy+55,340,'근거를 사용할 때 출처·등급과\n이번 대상에 맞는지 대조','support')
mat('version','자료의 시점·버전',460,dy+55,340,'판단 대상 시점에 맞는 판본\n원문 위치·확인 시점을 연결','support')
d.groups['DATA']['h']=max(bottom('trust'),bottom('version'))-Y+30

panel('RULES',1330,Y,770,1100,'현재 적용할 기준을 정한다',
      '법적 관계를 먼저 확인한다. 아래 위계는 규칙이 충돌할 때만 적용한다.')
_,ry=row('rule_source',['규칙·기준 원문','법·의무 기준'],1350,Y+90,730,links=True,kind='support',notes={
 '규칙·기준 원문':'원문·출처·설정 권한 확보',
 '법·의무 기준':'상하·특별·위임 관계와\n대상·시점·예외부터 확인'})
for n,(title,names) in enumerate([
 ('① 필수 의무·기본 원칙·승인된 보호 기준',['직업 윤리·의무','에이전트 기본 원칙']),
 ('② 유효한 약속·필수 이용 규정',['계약·합의 조건','플랫폼·제출처 규정']),
 ('③ 조직의 필수 규정',['조직 규칙']),
 ('④ 사용자의 추가 조건',['사용자 지정 규칙']),
 ('⑤ 표현 기준',['표현 방식·스타일'])]):
    ry+=44;d.text(1350,ry-12,title,17,weight=650)
    _,ry=row('rank'+str(n)+'_',names,1350,ry,730,links=False,kind='support',notes={
     '직업 윤리·의무':'필수 의무·비밀·이해충돌 관리',
     '에이전트 기본 원칙':'목적·범위 준수와 근거 정직성',
     '계약·합의 조건':'유효한 약속과 종료 후 의무',
     '플랫폼·제출처 규정':'이용·제출 유형별 필수 조건',
     '조직 규칙':'업무·역할별 필수 규정과 허용된 예외',
     '사용자 지정 규칙':'추가 조건·선호와 변경·취소 반영',
     '표현 방식·스타일':'표현 기준이 필요한 작업에 적용'})
mat('priority','규칙의 적용·우선순위',1350,ry+40,730,
    '법적 관계 → 충돌 조항의 위계 판단 → 함께 지킬 나머지 조건 유지\n예외는 요건·결정 권한 확인 · 미해결이면 사람의 결정 또는 보류')
d.groups['RULES']['h']=bottom('priority')-Y+25

mat('measure_goal','성과 추적',870,Y+10,380,'목표를 무엇으로 언제 확인할지 정함')
E('i4','measure_goal',via=[(mid('i4'),455),(2125,455),(2125,Y-35),(1060,Y-35)])
box('input_ok','필요한 근거와 조건을\n갖췄는가?',875,Y+215,370,kind='decision')
E('measure_goal','input_ok')
# Each resource scope explicitly supplies the nearby decision.
E('DATA','input_ok','apply','근거',sa='r',sb='l',at=(847,Y+195))
d.edges[-1]['points']=[(820,Y+195),(895,Y+195),(895,Y+305.75)]
E('priority','input_ok','apply','적용 조건',sa='l',sb='r',via=[(1320,d.port('priority','l')[1]),(1320,Y+175),(1210,Y+175)],at=(1270,Y+175))
d.edges[-1]['points'][-1]=(1210,Y+297.5)
mat('find','정보·자료 찾기',870,Y+545,380,'부족한 정보·근거·방법을 확보\n예외·반대 근거·원문까지 찾음')
mat('notfound','못 찾음·없음 구분',870,Y+715,380,'빈손인 검색은 범위·질의·시점 기록\n못 찾았다고 없다고 단정하지 않음')
box('found','필요한 근거를\n확보했는가?',895,Y+890,330,kind='decision')
E('input_ok','find','blocked','아니오',at=(1060,Y+485))
E('find','notfound')
E('notfound','found')
E('found','input_ok','return','보완 후\n재확인',sa='r',sb='r',via=[(1280,d.port('found','r')[1]),(1280,d.port('input_ok','r')[1])],at=(1280,Y+866))
box('input_hold','필수 근거 미확보 · 보류',870,Y+1140,380,'사유·재개 조건·후속 책임 기록',kind='stop')
E('found','input_hold','blocked','아니오',at=(1060,Y+1110))
prep_end=max(bottom('RULES'),bottom('DATA'),bottom('input_hold'))

# Method choice, a conditional capability test and the current execution gate.
P=prep_end+120
panel('PLAN',60,P,2040,910,'계획·실행 조건')
plan,py=row('plan',['대안·전략 판단','업무 절차·실행 계획','빠진 위험 확인'],80,P+80,1320,notes={
 '대안·전략 판단':'방법별 효과·부담·위험 비교\n계속·변경·보류·중단을 선택',
 '업무 절차·실행 계획':'필요한 재료·작업 순서·입출력\n검사·중단 기준과 선행 조건을 정함',
 '빠진 위험 확인':'접수·계획·실행·전달 때\n빠진 조건과 연계 피해를 점검'})
E('input_ok','plan0','flow','예',sa='l',sb='t',via=[(830,d.port('input_ok','l')[1]),(830,prep_end+55),(mid('plan0'),prep_end+55)],at=(830,prep_end-40))
box('ability_needed','처음 투입하거나\n검증된 능력 밖인가?',100,P+290,360,kind='decision')
E('plan2','ability_needed',via=[(mid('plan2'),P+270),(280,P+270)])
mat('testenv','시험 환경',520,P+320,340,'격리·비교·재현이 필요한 시험 준비')
mat('ability','업무 능력 시험',930,P+320,440,'첫 투입·범위 밖·능력 변경 전후\n통과한 판본과 수행 범위를 확인')
E('ability_needed','testenv','flow','예',sa='r',sb='l',at=(490,P+380))
E('testenv','ability',sa='r',sb='l')
box('capable','필요한 능력이\n확인됐는가?',970,P+535,340,kind='decision')
E('ability','capable')
E('capable','plan1','return','아니오 · 방법 재검토',sa='r',sb='t',via=[(1430,d.port('capable','r')[1]),(1430,P+55),(mid('plan1'),P+55)],at=(1130,P+55))
mat('right','업무 권한',1490,P+80,570,'지금 누구 대신 무엇을 할 수 있는가\n동의·승인·대상·내용·명의를 확인','support')
mat('limit','비용·위험 한도',1490,P+240,570,'사용·진행·예약분과 남은 한도\n실행과 대기의 위험을 함께 비교','support')
mat('safety','안전장치',1490,P+400,570,'수신·실행·재시도·재개 직전에\n현재 규칙·권한·한도·승인과 대조')
E('right','safety','apply',sa='l',sb='l',via=[(1450,d.port('right','l')[1]),(1450,d.port('safety','l')[1])])
E('limit','safety','apply')
box('permit','현재 조건으로\n작업을 실행해도 되는가?',895,P+795,390,kind='decision')

E('safety','permit','apply','매번 대조',sa='b',sb='r',via=[(1775,P+735),(1345,P+735),(1345,d.port('permit','r')[1])],at=(1500,P+735))
E('capable','permit','flow','예',at=(1090,P+755))
E('ability_needed','permit','blocked','아니오 · 검증된 범위',sa='b',sb='l',via=[(280,P+745),(840,P+745),(840,d.port('permit','l')[1])],at=(500,P+745))
mat('human','사람에게 넘기기',1490,P+810,570,'조사·대안 비교·준비·검증 후 결정만 요청\n되돌릴 수 없는 일·필수 승인·판단 불가\n한도 초과·자격자 전속에 해당할 때')
mat('humanid','보고 주체 확인',1490,P+1020,570,'답변한 본인·권한·승인 대상·판본 대조')
box('human_valid','유효한 결정을 받았는가?',1570,P+1170,410,kind='decision')
E('permit','human','blocked','사람의\n결정 필요',sa='r',sb='l',at=(1430,d.port('human','l')[1]))
E('human','humanid');E('humanid','human_valid')
E('human_valid','safety','return','예 · 재확인',sa='r',sb='r',via=[(2080,d.port('human_valid','r')[1]),(2080,d.port('safety','r')[1])],at=(2080,P+760))
box('human_hold','결정 미확정 · 보류',1480,P+1470,590,'거절·불일치·기한 종료 · 사유와 재개 조건 기록',kind='stop')
E('human_valid','human_hold','blocked','아니오',at=(1765,P+1430))
box('stop','허용되지 않은 작업 중단',150,P+960,590,'위반·해결 불가 · 사유와 후속 책임 기록',kind='stop')
E('permit','stop','blocked','위반·해결 불가',sa='l',sb='r',via=[(805,d.port('permit','l')[1]),(805,d.port('stop','r')[1])],at=(560,P+915))
d.groups['PLAN']['h']=bottom('human_hold')-P+30

# Actual execution. Conditional material combinations are selected by ONE expert.
X=bottom('PLAN')+90
panel('EXEC',60,X,2040,1220,'필요한 작업을 직접 수행한다',
      '작업마다 필요한 재료를 선택·조합한다. 아래 연결은 함께 쓸 때 결과가 넘어가는 관계이며, 전부 실행하는 순서가 아니다.')
box('select','이번 작업에\n무엇이 필요한가?',900,X+95,370,'여러 종류를 함께 사용할 수 있음',kind='decision')
E('permit','select','flow','허용',via=[(1090,bottom('PLAN')+40),(1085,bottom('PLAN')+40)],at=(1090,P+1330))
lane_x=[80,585,1090,1595];lane_w=485;ly=X+395
purposes=['자료를 얻고 다듬을 때','계산·판단이 필요할 때','사람과 주고받을 때','결과를 만들거나 반영할 때']
for i,x in enumerate(lane_x):panel(f'L{i}',x,ly,lane_w,970,purposes[i])
mat('experiment','실험',100,ly+70,205,'조건을 바꿔\n영향을 비교')
mat('simulate','시뮬레이션',340,ly+70,205,'가정한 상황의\n움직임·반응 예상')
mat('observe','관찰·측정',100,ly+245,205,'필요한 새 값·기록을\n당시 조건과 함께 얻음')
mat('classify','자료 선별·분류',340,ly+245,205,'필요한 자료를\n고르고 나눔')
mat('combine','자료 정리·결합',100,ly+475,445,'오류·중복·누락을 정리하고 합침')
mat('convert','형식·구조 변환',100,ly+650,445,'다음 작업·제출처의 형식이 다를 때 변환')
E('experiment','observe');E('simulate','classify')
E('observe','classify','data','',sa='r',sb='l',at=(322,ly+325))
E('classify','combine',via=[(442.5,ly+450),(322.5,ly+450)])
E('combine','convert')
mat('calc','계산',605,ly+70,210,'값·식을 구함\n단위·가정을 확인')
mat('analyze','분석',855,ly+70,195,'관계·차이·원인\n자료·값을 해석')
mat('forecast','예측',605,ly+275,210,'미래가 중요할 때\n예상·불확실성')
mat('optimize','조건 안에서 최선 찾기',855,ly+275,195,'조건 안에서\n유리한 안을 비교')
mat('judge','기준 적용·판정',605,ly+540,445,'요건·근거·예외를 대조해\n적합 여부·자격·책임 등을 판단')
mat('know_use','업무 지식',605,ly+755,445,'분석·판정에 원리·적용 조건·예외를 제공','support')
E('calc','analyze','data',sa='r',sb='l')
E('analyze','forecast','data','예상이 필요할 때',via=[(952.5,ly+245),(710,ly+245)],at=(850,ly+245))
E('forecast','optimize','data','',sa='r',sb='l',at=(835,ly+355))
E('optimize','judge',via=[(952.5,ly+510),(827.5,ly+510)])
E('know_use','judge','apply','해석 근거',sa='t',sb='b',at=(827.5,ly+735))
mat('live','실시간 대화',1110,ly+70,445,'바로 답을 주고받을 때 통로·발언 관리')
mat('communicate','사람과 소통',1110,ly+265,445,'질문·설명·확인이 필요할 때\n접촉 위험을 확인하고 답·요구를 받음')
mat('negotiate','협상·조율',1110,ly+520,445,'요구·이익·약속이 충돌할 때\n권한 안에서 합의·남은 쟁점을 정리')
E('live','communicate','data','주고받은 내용',at=(1332.5,ly+230))
E('communicate','negotiate','data','조정이 필요할 때',at=(1332.5,ly+465))
mat('design','결과물 설계',1615,ly+70,205,'내용·구조·작동을\n정할 때')
mat('restate','내용 재구성',1855,ly+70,205,'요약·번역·표현을\n바꿀 때')
mat('make','결과물 만들기·수정',1615,ly+290,445,'설계·검증한 입력으로 제작·수정\n원본과 수정 범위·판본을 함께 관리')
E('design','make',via=[(1717.5,ly+255),(1837.5,ly+255)])
E('restate','make',via=[(1957.5,ly+265),(1910,ly+265)])
d.edges[-1]['points'][-1]=(1910,ly+290)
panel('EXTERNAL',1615,ly+475,445,430,'외부 반영을 맡았을 때만','실행 직전 현재 권한·한도·승인 재확인')
for i,(name,note) in enumerate([
 ('기록 입력·수정','기록 등록·변경·삭제'),('신청·거래 처리','신청·변경·취소·환불'),
 ('설정·작동 제어','설정·접근·작동 조정'),('게시·배포','판본·대상·시점 확인')]):
    mat(f'ext{i}',name,1630+(i%2)*215,ly+555+(i//2)*150,200,note)
E('make','EXTERNAL','data','반영할 결과',at=(1837.5,ly+450))
for i in range(4):
    E('select',f'L{i}','flow', ['자료 작업','판단 작업','소통 작업','제작·반영 작업'][i],sa='b',sb='t',
      via=[(1000+i*55,X+[340,352,376,364][i]),(lane_x[i]+lane_w/2,X+[340,352,376,364][i])],at=(lane_x[i]+lane_w/2,X+382))
    # Separate ports on the decision lower sides; all lead into conditional scopes.
    sel=d.nodes['select'];px=1000+i*55;cy=sel['y']+sel['h']/2;cx=sel['x']+sel['w']/2
    d.edges[-1]['points'][0]=(px,cy+sel['h']/2*(1-abs(px-cx)/(sel['w']/2)))
outy=ly+1030
mat('tools','업무 도구·시스템',1615,outy,445,'도구가 필요한 작업의 요청·응답 연결\n실제 결과·오류·진행 상태를 받아 검증')
E('EXEC','tools','apply','연결',sa='r',sb='r',via=[(2115,X+700),(2115,d.port('tools','r')[1])],at=(2087.5,d.port('tools','r')[1]))
box('executed','이번 작업의 결과·상태',820,outy+215,530,'아래에서 근거·완료 조건과 대조',kind='process')
E('tools','executed',via=[(1837.5,outy+198),(1300,outy+198)])
d.edges[-1]['points'][-1]=(1300,outy+215)
E('EXTERNAL','tools','data')
for key,x,tx,yy in [('convert',322.5,900,outy+140),('judge',1070,1000,outy+155),('negotiate',1332.5,1100,outy+170),('make',1580,1200,outy+185)]:
    side='r' if key=='judge' else 'l' if key=='make' else 'b'
    st=d.port(key,side)
    E(key,'executed','data',sa=side,via=[(x,st[1]),(x,yy),(tx,yy)])
    d.edges[-1]['points'][-1]=(tx,outy+215)
d.groups['EXEC']['h']=bottom('executed')-X+30

# Verify/rework/wait. Main success flow is vertical; returns use the outer margins.
V=bottom('EXEC')+100
panel('VERIFY',60,V,2040,1220,'확인한 결과로 다음 행동을 정한다')
checks,vy=row('check',['보고 주체 확인','결과 검증·재검증','반대 근거·다시 확인','결과 품질 평가','일하는 과정 평가'],80,V+85,2000,notes={
 '보고 주체 확인':'외부 결과·답변을 받을 때\n주체·권한·대상·판본 대조',
 '결과 검증·재검증':'근거·완료 조건·다음 입력 대조\n변경된 부분과 영향 범위 재검사',
 '반대 근거·다시 확인':'중요한 판단·변경된 근거에\n다른 설명과 반대 근거 대조',
 '결과 품질 평가':'목적·분야 기준으로\n정확성·충분성·사용성 확인',
 '일하는 과정 평가':'단계 종료 때 방법·순서·권한\n준수와 상황 변화 대응을 평가'})
E('executed','check0',sb='l',via=[(1085,V+10),(65,V+10),(65,d.port('check0','l')[1])])
box('verdict','확인 결과는?',905,V+320,360,kind='decision')
E('check4','verdict',via=[(mid('check4'),V+285),(1085,V+285)])
mat('repair','업무 절차·실행 계획',110,V+440,560,'다음 작업·보완 범위의 재료·순서를 계획\n검증된 완료분 유지 · 현재 조건 재확인')
mat('wait','대기·후속 관리',1480,V+440,580,'미확인 외부 처리의 원래 상태 조회\n답변·기한·후속 책임 유지 · 중복 실행 금지')
E('verdict','repair','blocked','문제 있음',sa='l',sb='r',via=[(780,d.port('verdict','l')[1]),(780,d.port('repair','r')[1])],at=(780,V+465))
E('verdict','wait','blocked','아직 확인 불가',sa='r',sb='l',via=[(1370,d.port('verdict','r')[1]),(1370,d.port('wait','l')[1])],at=(1370,V+465))
E('repair','permit','return','계획한 작업 · 실행 조건 재확인',sa='l',sb='l',via=[(30,d.port('repair','l')[1]),(30,P+1090),(880,P+1090),(880,P+943.5)],at=(450,P+1090))
d.edges[-1]['points'][-1]=(970,P+943.5)
box('wait_answer','기다린 결과는?',1595,V+660,350,kind='decision')
E('wait','wait_answer')
E('wait_answer','check0','return','확인됨 · 재검증',sa='r',sb='t',via=[(2110,d.port('wait_answer','r')[1]),(2110,V+65),(300,V+65)],at=(1830,V+65))
d.edges[-1]['points'][-1]=(300,V+85)
E('wait_answer','wait','return','아직 대기',sa='l',sb='b',via=[(1420,d.port('wait_answer','l')[1]),(1420,V+625),(mid('wait'),V+625)],at=(1600,V+625))
box('hold','기한 종료·거절 · 보류',1480,V+940,580,'사유·재개 조건·후속 책임 기록',kind='stop')
E('wait_answer','hold','blocked','기한 종료·거절',at=(1770,V+905))
box('more','이어 할 작업이\n남아 있는가?',905,V+650,360,kind='decision')
E('verdict','more','flow','문제없음',at=(1085,V+570))
E('more','repair','return','예 · 다음 작업 계획',sa='l',sb='b',via=[(720,d.port('more','l')[1]),(720,V+610),(mid('repair'),V+610)],at=(650,V+610))

# Delivery is a visible ordinary sequence with its own receipt decision.
delivery,dy=row('delivery',['납품 준비','전달·인수 확인'],340,V+1020,1010,notes={
 '납품 준비':'결과·판본·설명과 남은 일을 정리',
 '전달·인수 확인':'약속한 상대에게 전달\n수령·사용·남은 문제를 확인'})
E('more','delivery0','blocked','아니오 · 최종 결과',via=[(1085,V+950),(mid('delivery0'),V+950)],at=(880,V+950))
box('receipt','인수 결과는?',1515,V+1185,450,kind='decision')
E('delivery1','receipt',sa='r',sb='l',via=[(1410,d.port('delivery1','r')[1]),(1410,d.port('receipt','l')[1])])
E('receipt','check0','return','반려·수정 요청 · 영향 범위 재검증',sa='r',sb='t',via=[(2135,d.port('receipt','r')[1]),(2135,V+45),(180,V+45)],at=(1460,V+45))
d.edges[-1]['points'][-1]=(180,V+85)
mat('receipt_wait','대기·후속 관리',1490,V+1520,560,'인수 답변과 기한·후속 책임을 유지\n답변 또는 기한 도래 시 인수 결과 재확인')
E('receipt','receipt_wait','blocked','미응답',at=(1760,V+1475))
E('receipt_wait','receipt','return','답변·기한 확인',sa='r',sb='r',via=[(2090,d.port('receipt_wait','r')[1]),(2090,V+1361)],at=(2090,V+1490))
d.edges[-1]['points'][-1]=(1870,V+1361)
E('receipt','hold','blocked','거절·\n만료',sa='r',sb='r',via=[(2095,V+1251),(2095,d.port('hold','r')[1])],at=(2095,V+1100))
d.edges[-1]['points'][0]=(1860,V+1251)
d.groups['VERIFY']['h']=bottom('receipt_wait')-V+35

# Outcomes, conditional improvement and a real end.
F=bottom('VERIFY')+100
panel('LEARN',60,F,2040,980,'실제 성과를 확인하고, 검증된 개선만 남긴다',
      '실패·보류 기록과 나중에 드러난 문제도 평가에 포함한다. 후속 확인은 기록한 책임과 시점에 이어서 수행한다.')
mat('outcome','성과 추적',100,F+100,450,'처음 정한 항목·시점으로\n실제 효과·실패·후속 문제를 확인')
box('improve_needed','개선할 점이 있는가?',720,F+80,360,kind='decision')
E('receipt','outcome','flow','인수 확인',sa='l',sb='l',via=[(1380,V+1372),(1380,F+72),(80,F+72),(80,d.port('outcome','l')[1])],at=(1150,F+72))
d.edges[-1]['points'][0]=(1630,V+1372)
E('outcome','improve_needed',sa='r',sb='l',via=[(625,d.port('outcome','r')[1]),(625,d.port('improve_needed','l')[1])])
learn,ly2=row('learn',['성공·실패 원인 분석','능력 개선·확장','시험 환경','업무 능력 시험'],100,F+390,1960,notes={
 '성공·실패 원인 분석':'재사용할 성과·중요한 문제의\n원인·조건·다른 업무 영향을 찾음',
 '능력 개선·확장':'지식·판단 요령·방법·도구를 개선',
 '시험 환경':'분리된 조건에서 개선안을 시험',
 '업무 능력 시험':'개선 효과와 기존 능력이\n모두 유지되는지 확인'})
E('improve_needed','learn0','flow','예',via=[(900,F+320),(mid('learn0'),F+320)],at=(640,F+320))
box('test_passed','개선과 기존 능력이\n모두 확인됐는가?',1645,F+650,360,kind='decision')
E('learn3','test_passed')
mat('remember','장기 기억',850,F+700,530,'시험을 통과한 지식·규칙·방법만 저장\n이후 업무의 근거와 조건에 맞춰 사용')
E('test_passed','remember','flow','예',sa='l',sb='r',at=(1510,F+755))
E('test_passed','learn1','return','아니오 · 기존 방법 유지 후 개선',sa='r',sb='t',via=[(2080,d.port('test_passed','r')[1]),(2080,F+350),(mid('learn1'),F+350)],at=(1450,F+350))
box('finish','이번 처리 종료',825,F+960,580,'남은 후속 확인·재개 조건·책임은 유지',kind='terminal')
E('remember','finish')
E('improve_needed','finish','blocked','아니오',sa='r',sb='r',via=[(2110,d.port('improve_needed','r')[1]),(2110,d.port('finish','r')[1])],at=(1510,d.port('improve_needed','r')[1]))
d.groups['LEARN']['h']=bottom('finish')-F+30
d.height=bottom('LEARN')+40

# Compress only genuinely empty horizontal strips. Shapes, labels, scope titles
# and connector turns retain their original dimensions and mutual order.
original_height=d.height
busy=[]
for n in d.nodes.values():busy.append((n['y']-12,n['y']+n['h']+12))
for g in d.groups.values():
    if 'y' in g:busy.append((g['y']-8,g['y']+50+(24*len(g['subtitle'].split('\n')) if g['subtitle'] else 0)))
for t in d.texts:busy.append((t['y']-t['size']-6,t['y']+(len(t['lines'])-1)*t['leading']+10))
for e in d.edges:
    for a,b in zip(e['points'],e['points'][1:]):
        if a[1]==b[1]:busy.append((a[1]-14,a[1]+14))
    if e['label']:
        x,y=e['label_at'] or ((e['points'][0][0]+e['points'][-1][0])/2,(e['points'][0][1]+e['points'][-1][1])/2)
        hh=23*len(e['label'].split('\n'))+10
        busy.append((y-hh/2-12,y+hh/2+12))
busy.sort();merged=[]
for a,z in busy:
    if merged and a<=merged[-1][1]:merged[-1][1]=max(z,merged[-1][1])
    else:merged.append([a,z])
cuts=[(a+22,z-22) for (_,a),(z,_) in zip(merged,merged[1:]) if z-a>44]
def compact_y(y):return y-sum(max(0,min(y,z)-a) for a,z in cuts if y>a)
for n in d.nodes.values():n['y']=compact_y(n['y'])
for g in d.groups.values():
    if 'y' in g:
        z=compact_y(g['y']+g['h']);g['y']=compact_y(g['y']);g['h']=z-g['y']
for t in d.texts:t['y']=compact_y(t['y'])
for e in d.edges:
    e['points']=[(x,compact_y(y)) for x,y in e['points']]
    if e['label_at']:e['label_at']=(e['label_at'][0],compact_y(e['label_at'][1]))
d.height=compact_y(d.height)
d.layout_notes={'original_height':original_height,'empty_space_removed':original_height-d.height,'fixed_aspect_ratio':False}

# Textual semantics remain in the file; the PNG is rendered from this exact SVG.
names={n['name'] for n in d.nodes.values() if n['material']}
assert names==set(m.CAT),(set(m.CAT)-names,names-set(m.CAT))
d.catalog=m.CAT
for n in d.nodes.values():
    if n['material']:
        n['canonical_condition']=m.CAT[n['name']]['condition']
d.source_prefix_sha256=hashlib.sha256(m.PREFIX.encode()).hexdigest()
out=ROOT/'docs/images/expert-definition';out.mkdir(parents=True,exist_ok=True)
svg=d.svg().replace('stroke-width="2.5"','stroke-width="3.2"').replace('stroke-dasharray="2 6"','stroke-dasharray="2 7"')
(out/'solo-one-expert-flow.svg').write_text(svg)
(ROOT/'docs/도식/단독-상황-이미지.json').write_text(json.dumps(d.__dict__,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'width':d.width,'height':d.height,'materials':len(names),'nodes':len(d.nodes),'edges':len(d.edges)},ensure_ascii=False))
