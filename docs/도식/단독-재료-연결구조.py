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
# The execution graph, reference inputs and all-step responsibilities are distinct.
# A material appears once; its consumers are explicit and do not become control edges.
import heapq
W = 1620
N, E, G, A = {}, [], [], []
C = dict(ink='#192C36', muted='#526773', blue='#228DE1', red='#CF504A', yellow='#B67D00',
         pale='#E8F5FE', border='#CADFE9', green='#E7F5E9', white='#FFFFFF')
SYSTEM_STYLE = {
    '환경': dict(accent='#1766A6', fill='#EDF5FF'),
    '지식': dict(accent='#157267', fill='#EAF7F3'),
    '규칙': dict(accent='#7151A8', fill='#F3EEFC'),
    '실무': dict(accent='#995114', fill='#FFF3E5'),
    '검증': dict(accent='#A23C6B', fill='#FCEEF4'),
    '학습': dict(accent='#526E20', fill='#F1F6E5'),
}

def measure(s, size):
    return sum(size * (.96 if ord(c)>255 else .30 if c==' ' else .53) for c in s)

def wrap(s, width, size):
    rows = []
    for line in s.split('\n'):
        row = ''
        for word in line.split(' '):
            if row and measure(row+' '+word, size)>width:
                rows.append(row); row=word
            else:
                row += (' ' if row else '')+word
        rows.append(row)
    return rows

def note(x, y, text, size=22, weight=500, color=None):
    A.append(dict(x=x,y=y,text=text,size=size,weight=weight,color=color or C['muted']))

def node(key, title, y, body='', kind='process', side=False, material=None, **extra):
    x,w = (58,310) if side else (470,470)
    z = 23 if kind=='decision' else 25
    titles = wrap(title, w*(.67 if kind=='decision' else .9), z)
    bodies = wrap(body,w-34,20) if body else []
    h = max(150 if kind=='decision' else 82, len(titles)*29+len(bodies)*25+36)
    if kind=='decision':h=max(h,180 if len(titles)>2 else 150)
    N[key] = dict(id=key,title=title,body=body,kind=kind,x=x,y=y,w=w,h=h,
                  material=material,scope='all_steps',**extra)
    return key

def edge(a,b,label='',kind='flow',**extra):
    E.append(dict(source=a,target=b,label=label,kind=kind,**extra))

def section(key,y,title,subtitle=''):
    note(58,y,title,32,800,C['ink'])
    if subtitle:note(58,y+36,subtitle,21)
    return y+75

MATERIALS = {}
def cards(key,x,y,w,items,consumers,title,columns=2,scope=False):
    # Each row is a reference shelf, not a fork or a required sequence.
    start=y
    note(x,y+26,title,24,800,C['ink'])
    y+=46
    cw=(w-18*(columns-1))/columns
    for at in range(0,len(items),columns):
        row=items[at:at+columns];prepared=[]
        for name,body in row:
            assert name in CAT and name not in MATERIALS,name
            tt=wrap(name,cw-28,22);bt=wrap(body,cw-28,19)
            h=25+len(tt)*27+8+len(bt)*24+17
            prepared.append((name,body,h))
        rh=max(i[2] for i in prepared)
        for j,(name,body,h) in enumerate(prepared):
            k='m'+str(list(CAT).index(name)).zfill(2)
            typ='unused' if name=='나눠 맡기기' else 'reference'
            N[k]=dict(id=k,title=name,body=body,kind=typ,material=name,
                      x=x+j*(cw+18),y=y,w=cw,h=rh,
                      term=CAT[name]['term'],system=CAT[name]['system'],usage=CAT[name]['usage'],
                      reference_group=key,consumers=consumers,scope='all_steps' if scope else key)
            MATERIALS[name]=k
        y+=rh+16
    G.append(dict(id=key,x=x-12,y=start,w=w+24,h=y-start,title='',role='scope' if scope else 'reference',consumers=consumers))
    return y

# Runtime services are visible before the first entry, with a bounded all-step scope.
y=section('runtime',46,'한 건 · 한 전문가',
          '파란 화살표: 실행 순서   ·   노란 화살표: 다시 진행   ·   회색 점선: 해당 단계에서 쓰는 재료')
y=cards('runtime',58,y,1500,[
 ('AI 모델','이해·판단·생성이 필요한 모든 단계에서 사용'),
 ('실행 제어','선후관계·병렬 합류·실패·대기·재개를 실행'),
 ('현재 작업 정보','판단마다 목표·근거·상태 중 필요한 정보를 제공'),
 ('분리 실행','작업 공간·자료·자원을 분리하고 허용한 것만 공유'),
 ('업무 도구·시스템','조회·편집·전송 등 필요한 호출과 결과를 연결'),
 ('운영 감시·복구','장애를 감시하고 저장한 상태로 복구'),
 ('업무 권한','행위·대상·승인 범위·철회 여부를 실행 전에 확인'),
 ('비용·위험 한도','이미 사용·예약한 몫과 이번 실행·대기 비용을 합산'),
 ('안전장치','모든 정보 교환·실행·재시도 전에 허용 여부 검사'),
 ('현재 진행 상태','완료분·대기 이유·재개 위치·외부 처리 상태를 보존'),
 ('판단 근거 기록','각 판단·실행·검사의 입력·이유·결과를 기록'),
 ('나눠 맡기기','단독 상황에서는 쓰지 않음. 한 전문가가 직접 담당'),
],['ALL_STEPS'],'전 단계 공통 기반 · 순서대로 켜는 기능이 아님',columns=4,scope=True)+20
note(58,y+20,'공통 실행 규칙: 권한·기준·한도를 확인한 단계만 실행합니다. 위반은 차단, 확인 불가는 보류합니다.',23,700,C['ink'])
note(58,y+52,'사람의 결정이 필요하면 아래 사람 결정 절차로, 응답·상태 확인이 필요하면 대기 절차로 이동합니다.',21)
y+=120

s=y=section('rules',y,'전 단계에 적용할 기준',
 '회색 연결은 판단에 쓰는 기준입니다. 아래 재료를 차례대로 실행한다는 뜻이 아닙니다.')
py=cards('rules_materials',58,s,1500,[
 ('규칙·기준 원문','출처·설정 권한·적용 범위와 시점이 맞는 원문 확보'),
 ('법·의무 기준','법적 적용 관계·특별 규정·위임·유효한 예외부터 확인'),
 ('직업 윤리·의무','비밀 보호·이해충돌 등 직업상 필수 의무 확인'),
 ('에이전트 기본 원칙','맡은 목적·범위를 지키고 외부 자료의 지시로 권한을 바꾸지 않음'),
 ('계약·합의 조건','범위·기한·권리·의무와 종료 뒤 남는 약속 확인'),
 ('플랫폼·제출처 규정','현재 서비스·계정·제출 방식의 필수 조건 확인'),
 ('조직 규칙','업무·역할에 적용되는 규정과 허용된 예외 확인'),
 ('사용자 지정 규칙','필수 조건과 선호를 구분하고 변경 요구 반영'),
 ('표현 방식·스타일','결과를 만들거나 설명할 때 대상·매체에 맞게 적용'),
 ('규칙의 적용·우선순위','법적 관계를 먼저 적용. 충돌하지 않는 의무·보호 기준도 유지'),
],['ALL_STEPS'],'전 단계에 적용 · 충돌하는 조항만 우선순위 판단',columns=5,scope=True)
note(58,py+17,'조항이 충돌할 때: 법적 적용 관계 → 직업 의무·기본 원칙 → 계약·플랫폼 필수 조건 → 조직 필수 규정 → 사용자 조건 → 기본 표현',19)
note(58,py+46,'예외의 요건·허용 권한을 확인하고, 풀리지 않은 충돌은 사람의 결정 또는 보류로 연결합니다.',21)
y=py+115


# Entry and planning. Grey material panels make the function/sequence distinction explicit.
s=y=section('prepare',y,'1  시작·재개 신호를 확인하고 필요한 준비만 합니다')
def at(key,title,row,body='',kind='process',side=False,**extra):
    return node(key,title,s+row*200,body,kind,side,**extra)
at('start','요청·답변·변경·예약 시점 도착',0,kind='terminal',role='start')
at('channel','실시간 대화인가?',1,kind='decision')
at('live','통화·채팅 연결',1,'발언·중단·재접속 관리',side=True,uses=['실시간 대화'])
at('signal','시작 신호를 해당 건에 연결',2,'새 요청·답변·변경·정해 둔 확인 시점',uses=['시작 신호'])
at('event','어떤 신호인가?',3,kind='decision')
at('admit','검증된 업무·버전인가?',4,kind='decision')
at('admission_test','실제 업무와 분리해 능력 시험',4,'처음 투입·범위 밖·능력 변경 시',side=True,uses=['시험 환경','업무 능력 시험'])
at('admission_result','시험을 통과했는가?',5,kind='decision',side=True)
at('intake','요청·범위·완료 조건 정하기',5,'성과 확인 항목·시점도 함께 정함',uses=['업무별 정보','정보·자료 이해','지시·의도 파악','문제·목표·완료 조건','성과 추적'])
at('clear','범위가 달라질 만큼 모호한가?',6,kind='decision')
at('ask','필요한 뜻·범위를 질문',6,'질문 대상과 답변 기한을 기록',side=True,uses=['사람과 소통'])
at('ask_result','유효한 답이 왔는가?',7,kind='decision',side=True)
at('evidence','필요한 근거와 적용 기준 확보',7,'이미 충분하면 유효성만 재확인',uses=['정보·자료 찾기','규칙·기준 원문','근거의 신뢰성·적합성','자료의 시점·버전'])
at('risk_plan','계획의 빠진 위험 확인',8,'목표·방법·기한·뒤 작업에 줄 피해',uses=['빠진 위험 확인'])
at('strategy','방법과 진행 여부 판단',9,'근거·효과·비용·위험을 비교',uses=['대안·전략 판단'])
at('strategy_result','진행할 근거와 방법이 있는가?',10,kind='decision')
at('plan','순서·검사·중단·합류 조건 계획',11,'이미 끝난 일은 보존하고 필요한 부분만 변경',uses=['업무 절차·실행 계획'])
edge('start','channel');edge('channel','live','예');edge('live','signal');edge('channel','signal','아니오')
edge('signal','event');edge('event','admit','새 요청')
edge('event','restore','답변·재개');edge('event','change_kind','감시 중 변화');edge('event','outcome','예약한 후속 확인 시점',kind='event')
edge('admit','intake','예');edge('admit','admission_test','아니오');edge('admission_test','admission_result')
edge('admission_result','intake','예');edge('admission_result','stop','아니오 · 투입 보류',kind='blocked')
edge('intake','clear');edge('clear','evidence','아니오');edge('clear','ask','예');edge('ask','ask_result')
edge('ask_result','intake','유효한 답',kind='return');edge('ask_result','wait','미응답·불명확',kind='blocked',resume='intake')
edge('evidence','risk_plan');edge('risk_plan','strategy');edge('strategy','strategy_result')
edge('strategy_result','plan','예');edge('strategy_result','wait','추가 근거 대기',kind='blocked',resume='evidence')
edge('strategy_result','stop','진행 불가',kind='blocked')
py=cards('entry_materials',1080,s,480,[
 ('시작 신호','요청·답변·변경·예약한 시점을 해당 업무에 연결'),
 ('실시간 대화','바로 주고받는 통화·채팅에서 연결과 발언을 관리'),
 ('먼저 알아채기','반복 문의 같은 새 문제, 안내문 개선 같은 새 대응거리 발견'),
 ('변경 감시·반영','기존 업무의 자료·마감·규칙 변화와 영향 범위 확인'),
 ('업무별 정보','이번 요청의 대상·기한·상황·새 자료를 모음'),
 ('정보·자료 이해','사실·주장·맥락·불명확한 내용을 구별'),
 ('지시·의도 파악','원하는 결과와 어디까지 맡겼는지 확인'),
 ('문제·목표·완료 조건','범위·우선순위·완료를 입증할 증거를 정함'),
 ('시험 환경','초기 투입과 개선 시험을 실제 업무·원본에서 분리'),
 ('업무 능력 시험','처음 투입·변경 시 예외·재개·기존 능력까지 시험'),
],['channel','signal','admit','admission_test','intake','change_kind','learn_test'],'시작·이해·변화 판단에 쓰는 재료')
py=cards('evidence_materials',1080,py+28,480,[
 ('정보·자료 찾기','근거가 부족할 때 정보·방법·원문을 찾음'),
 ('못 찾음·없음 구분','빈 검색이면 검색 범위와 없음의 근거를 확인'),
 ('현재 값·상태 확인','현재 값이 중요하거나 외부 처리 여부가 불명확할 때 조회'),
 ('적용 사례','비슷한 사례가 필요하면 조건과 결과를 대조'),
 ('참고 자료','원리·방법·표현의 예가 필요할 때 참고'),
 ('재사용 자료','서식·부품을 쓸 때 권리와 현재 환경을 확인'),
 ('근거의 신뢰성·적합성','출처·증거 수준과 이번 판단에 쓸 수 있는지 확인'),
 ('자료의 시점·버전','적용 시점에 맞는 판본과 확인 시각을 남김'),
 ('업무 지식','검증된 원리·방법과 적용 조건·예외를 사용'),
 ('실전 경험·감각','경험의 단서·요령이 현재 상황에도 맞는지 대조'),
],['evidence','run','verify'],'필요한 근거만 확보 · 사용 전 신뢰성·시점 확인')
py=cards('planning_materials',1080,py+28,480,[
 ('빠진 위험 확인','계획·실행·변경·납품 전에 놓친 조건과 피해를 확인'),
 ('대안·전략 판단','기존 방법이 안 맞으면 대안을 비교하고 진행·보류 판단'),
 ('업무 절차·실행 계획','선후관계·검사·중단 조건과 선택한 작업들의 합류를 지정'),
],['risk_plan','strategy','plan','risk_exec','risk_delivery'],'계획에 쓰는 재료',columns=1)
# Additional vertical room is shared by the flow and its material shelf.
y=max(s+12*200,py)+85

s=y=section('execution',y,'2  계획한 작업을 실행하고 결과를 확인합니다',
 '하나 또는 여러 재료를 선택합니다. 순서는 계획대로, 서로 독립된 작업만 동시에 진행합니다.')
at('dispatch','지금 가능한 다음 작업 선택',0,'완료분·대기분은 보존',uses=['작업 진행·연결'])
at('select','필요한 재료와 조합 선택',1,'선행 입력과 이번 합류에 필요한 결과를 지정')
at('risk_exec','실행 직전 위험 재확인',2,'계획 이후 바뀐 대상·상태·피해 확인',uses=['빠진 위험 확인'])
at('permit','지금 실행해도 되는가?',3,kind='decision',boundary=True)
at('run','선택한 작업 실행',4,'준비된 입력으로만 실행 · 기존 외부 처리 중복 금지')
at('join','선택한 필수 결과가 모두 준비됐는가?',5,kind='decision')
at('identity','결과의 주체·대상·버전 확인',6,'다른 대상·변경된 승인 결과는 받지 않음',uses=['보고 주체 확인'])
at('identity_valid','요청과 일치하는 결과인가?',7,kind='decision')
at('counter_needed','중요 판단 또는 근거 변경인가?',8,kind='decision')
at('counter','반대 근거·다른 방법으로 대조',8,'차이가 나면 결론·근거를 수정하거나 유보',side=True,uses=['반대 근거·다시 확인'])
at('verify','결과와 영향받은 부분 검증',9,'원문·완료 조건·다음 입력 요건 대조',uses=['결과 검증·재검증'])
at('verdict','검증 결과는?',10,kind='decision')
at('process_eval','과정의 필수 절차·권한 확인',11,'위반·누락은 보완 대상에 포함',uses=['일하는 과정 평가'])
at('process_valid','필수 절차도 충족했는가?',12,kind='decision')
at('complete','완료 조건을 모두 충족했는가?',13,kind='decision')
edge('plan','dispatch');edge('dispatch','select');edge('select','risk_exec');edge('risk_exec','permit')
edge('permit','run','허용');edge('permit','human','사람 결정 필요',kind='blocked',resume='permit')
edge('permit','wait','확인 불가',kind='blocked',resume='permit');edge('permit','stop','위반·실행 불가',kind='blocked')
edge('run','join');edge('join','identity','예');edge('join','repair','실패·누락',kind='blocked');edge('join','wait','진행·응답 대기',kind='blocked',resume='join');edge('identity','identity_valid')
edge('identity_valid','counter_needed','예');edge('identity_valid','repair','아니오 · 반려',kind='blocked')
edge('counter_needed','counter','예');edge('counter','verify');edge('counter_needed','verify','아니오')
edge('verify','verdict');edge('verdict','process_eval','문제없음');edge('verdict','repair','문제 있음',kind='blocked')
edge('verdict','wait','확인 불가',kind='blocked',resume='verify');edge('process_eval','process_valid')
edge('process_valid','complete','예');edge('process_valid','repair','아니오',kind='blocked')
edge('complete','dispatch','아니오 · 다음 작업',kind='return');edge('complete','quality','예')
py=cards('operations',1080,s,480,[
 ('자료 선별·분류','자료를 골라 분류하고 같은 대상의 기록을 연결'),
 ('자료 정리·결합','오류·중복을 정리해 합치고 원본 위치를 보존'),
 ('형식·구조 변환','내용·항목 관계를 유지하며 필요한 형식으로 변환'),
 ('계산','수치·식으로 필요한 값과 연동된 항목을 계산'),
 ('분석','자료·계산값에서 관계나 원인을 찾음'),
 ('기준 적용·판정','확인한 사실과 기준을 비교해 충족 여부 판단'),
 ('예측','자료·가정으로 미래 결과와 불확실성을 살핌'),
 ('조건 안에서 최선 찾기','제약 안에서 후보들을 비교해 가장 나은 안 선택'),
 ('결과물 설계','목적·요건에 맞게 구성·규격·만드는 방법 설계'),
 ('내용 재구성','기존 내용의 순서·표현을 이번 목적에 맞게 변경'),
 ('결과물 만들기·수정','설계·자료로 제작하고 요청한 부분을 수정'),
 ('사람과 소통','필요한 뜻·상태를 묻거나 설명하고 이해·답변 확인'),
 ('협상·조율','권한 안에서 조건·역할·약속을 협의하고 미합의 사항 기록'),
 ('기록 입력·수정','대상 기록을 등록·변경·삭제하고 반영 결과 대조'),
 ('신청·거래 처리','신청·예약·주문·지급과 변경·취소 상태를 확인'),
 ('설정·작동 제어','현재 상태와 유지 조건에 맞춰 설정·작동을 조절'),
 ('게시·배포','승인된 판본·대상·시점으로 공개하고 반영 확인'),
 ('관찰·측정','새 관측값을 당시 조건·빠진 기록과 함께 확보'),
 ('실험','조건 변화의 영향을 비교하고 다른 영향과 한계 기록'),
 ('시뮬레이션','가정한 상황의 진행·대응을 미리 계산하거나 연습'),
],['select','run'],'이번 작업에 필요한 재료만 선택 · 여러 개 조합 가능')
py=cards('checking',1080,py+28,480,[
 ('보고 주체 확인','보고·사람의 답변·대외 명의의 주체·권한·대상·판본 대조'),
 ('반대 근거·다시 확인','중요한 결론·바뀐 근거는 반대 증거와 다른 방법으로 확인'),
 ('결과 검증·재검증','수정·변경의 영향까지 검사해 통과·문제·미확인 구분'),
 ('일하는 과정 평가','당시 정보에서 방법·절차·권한이 적절했는지 평가'),
],['identity','human_valid','counter','verify','process_eval'],'결과·과정 검증에 쓰는 재료')
y=max(s+14*200,py)+85

s=y=section('delivery',y,'3  품질 통과·인수 확인을 마친 뒤 이번 업무를 닫습니다')
at('quality','사용 목적에 맞는 품질 평가',0,'정확성·기능·이해·사용성을 확인',uses=['결과 품질 평가'])
at('quality_ok','받아 쓸 품질인가?',1,kind='decision')
at('pack','납품본·원본·설명·남은 일 준비',2,uses=['납품 준비'])
at('risk_delivery','납품 직전 위험 재확인',3,'대상·판본·사용 환경·남은 책임 확인',uses=['빠진 위험 확인'])
at('delivery_permit','지금 전달해도 되는가?',4,kind='decision',boundary=True)
at('deliver','정한 상대에게 결과 전달',5,'전달 완료분은 중복 발송하지 않음',uses=['전달·인수 확인'])
at('receipt','약속한 인수 상태는?',6,kind='decision')
at('register','후속 약속·성과 확인을 예약',7,'담당·기한·확인 항목·재개 위치를 저장')
at('remember','이번 건의 사실·결정·교훈 저장',8,'미완료 의무와 근거도 함께 보존',uses=['장기 기억'])
at('finish','이번 업무 처리 완료',9,'예약한 후속 일은 별도 시점에 시작',kind='terminal',role='success')
edge('quality','quality_ok');edge('quality_ok','pack','예');edge('quality_ok','repair','아니오',kind='blocked')
edge('pack','risk_delivery');edge('risk_delivery','delivery_permit');edge('delivery_permit','deliver','허용')
edge('delivery_permit','human','사람 결정 필요',kind='blocked',resume='delivery_permit')
edge('delivery_permit','wait','확인 불가',kind='blocked',resume='delivery_permit')
edge('delivery_permit','stop','위반·전달 불가',kind='blocked')
edge('deliver','receipt');edge('receipt','register','인수 완료');edge('receipt','repair','수정 요청',kind='blocked')
edge('receipt','wait','확인 대기',kind='blocked',resume='receipt_check');edge('receipt','stop','거절·인수 종료',kind='blocked')
edge('register','remember');edge('remember','finish')
py=cards('closing',1080,s,480,[
 ('결과 품질 평가','받는 사람이 이해하고 쓸 수 있는 품질인지 평가'),
 ('납품 준비','결과·판본·원본·설명과 남은 일·담당을 함께 준비'),
 ('전달·인수 확인','도착·사용 조건을 확인하고 미응답·수정·인수 완료 구분'),
 ('장기 기억','이전 기록을 유효성 확인 후 사용하고 이번 결정·교훈을 보존'),
],['quality','pack','deliver','receipt','evidence','remember','learn_save'],'납품과 기록에 쓰는 재료',columns=1)
py=cards('performance_material',1080,py+28,480,[
 ('성과 추적','목표를 정할 때 확인 항목·시점 설정. 그 시점에 실제 효과·문제 비교'),
],['intake','register','outcome'],'성과 기준 설정과 실제 측정은 서로 다른 시점',columns=1)
y=max(s+10*200,py)+85

s=y=section('exceptions',y,'4  변경·대기·사람의 답변은 저장한 위치로 돌아갑니다',
 '보완 뒤 기존 계획으로 계속할 수 있으면 다음 작업만 진행합니다. 방법이 안 맞을 때만 다시 계획합니다.')
at('repair','반려·오류·수정 요청을 작업에 반영',0,'이미 끝난 외부 처리는 조회 후 남은 부분만 처리')
at('change_kind','감시 중 무엇을 발견했는가?',1,kind='decision')
at('early','새로 대응할 일인지 확인',1,'새 문제·개선 기회와 대응 이유',side=True,uses=['먼저 알아채기'])
at('impact','기존 자료·일정 변화의 영향 확인',2,'영향받은 근거·결과·작업만 표시',uses=['변경 감시·반영'])
at('replan','기존 계획으로 처리 가능한가?',3,kind='decision')
at('update_inputs','바뀐 목표·근거만 보완',3,'완료분 유지 · 필요한 범위만 재계획',side=True)
at('human','필요한 사람의 결정·작업 요청',4,'준비·검증 뒤 요청 · 답변 기한과 재개 위치 저장',uses=['사람에게 넘기기'])
at('human_valid','답변의 주체·권한·대상 확인',5,'승인과 사람이 수행한 결과를 구별',uses=['보고 주체 확인'])
at('human_result','받은 답은 유효한가?',6,kind='decision')
at('wait','대기 이유·기한·재개 위치 기록',7,'처리 불명 건은 재실행 대신 상태 조회',uses=['대기·후속 관리'])
at('wait_event','응답·확인 시점의 상태는?',8,kind='decision')
at('timeout','정해 둔 재시도·대체 여유가 있는가?',9,kind='decision')
at('retry','남은 횟수·한도 안에서 후속 조치',10,'재조회·대체 담당·인계와 다음 확인 기한 기록')
at('sleep','응답·예약 시점까지 대기',11,'확인 시점 도래 → 시작 신호로 재개',kind='terminal',role='suspended')
at('restore','저장된 상태·완료분·재개 위치 복원',12,'현재 권한·규칙·판본도 다시 확인')
at('changed','범위·근거·능력 조건이 바뀌었는가?',13,kind='decision')
at('resume','어디를 이어 할 차례인가?',14,kind='decision')
at('receipt_check','전달된 결과의 수령·사용 상태 조회',15,'이미 전달한 결과를 다시 보내지 않음')
at('stop','보류·중단·인계 기록 후 종료',16,'사유·남은 의무·재개 조건과 담당 보존',kind='terminal',role='stopped')
edge('repair','replan');edge('change_kind','early','새 문제·개선 기회');edge('early','admit','대응할 새 업무',kind='return')
edge('change_kind','impact','기존 업무의 변경');edge('impact','replan');edge('replan','dispatch','예',kind='return')
edge('replan','update_inputs','아니오');edge('update_inputs','admit','범위·능력부터 재확인',kind='return')
# Updated intake preserves completed work; it only revisits changed inputs.
edge('human','human_valid','답변 도착');edge('human','wait','미응답',kind='blocked',resume='human_valid')
edge('human_valid','human_result');edge('human_result','restore','유효한 승인');edge('human_result','verify','유효한 작업 결과',kind='return')
edge('human_result','wait','불일치·불명확 · 재확인',kind='blocked',resume='human_valid')
edge('human_result','stop','거절·철회',kind='blocked')
edge('wait','wait_event');edge('wait_event','restore','유효 응답·상태 변화')
edge('wait_event','sleep','기한 내 미응답');edge('wait_event','timeout','기한 만료·오류 반복')
edge('timeout','retry','예');edge('timeout','stop','아니오 · 한도 종료',kind='blocked')
edge('retry','sleep');edge('sleep','signal','저장한 신호가 도착',kind='event')
edge('restore','changed');edge('changed','impact','예 · 입력·조건 변경');edge('changed','resume','아니오')
for target,label in [('intake','뜻·범위 확인'),('evidence','근거 확보'),('permit','실행 승인'),('delivery_permit','전달 승인'),('join','선택한 작업 회수'),('verify','작업 결과 확인'),('human_valid','사람 답변 확인'),('receipt_check','인수 확인'),('outcome','후속 성과 확인')]:
    edge('resume',target,label,kind='return' if target!='outcome' else 'flow',resume_target=target)
edge('receipt_check','receipt','현재 상태 반영',kind='return')
py=cards('continuity',1080,s,480,[
 ('작업 진행·연결','준비된 다음 작업을 선택. 실패·변경은 보완 또는 재계획으로 연결'),
 ('사람에게 넘기기','필수 승인·자격·판단·직접 수행이 필요한 일을 자료와 함께 요청'),
 ('대기·후속 관리','기한·답변·외부 상태·재개 위치를 유지. 만료 시 정한 후속 조치'),
],['dispatch','repair','human','wait','retry','register'],'진행·대기·인계를 맡는 재료',columns=1)
note(1080,py+45,'재개할 위치는 기다리기 전에 정합니다.',22,700)
note(1080,py+78,'승인 답변 → 해당 실행의 허용 여부 재검사',20)
note(1080,py+109,'사람이 끝낸 작업 → 결과 검증',20)
note(1080,py+140,'인수 답변 → 수령·사용 상태 확인',20)
note(1080,py+171,'성과 확인 시점 → 실제 성과 측정',20)
y=max(s+17*200,py+220)+85

s=y=section('learning',y,'5  예약한 시점에 성과를 확인하고 필요한 개선만 합니다',
 '이번 업무의 완료와 별개입니다. 확인 시점·새 효과·문제가 생겼을 때 이 절차를 시작합니다.')
at('outcome','실제 성과·뒤늦은 문제 확인',0,'목표·기준·난이도·환경·쓴 자원 차이와 비교',uses=['성과 추적'])
at('outcome_valid','성과를 확인할 근거가 있는가?',1,kind='decision')
at('learn_needed','분석할 성과·반복 문제인가?',2,kind='decision')
at('cause','성공·실패의 원인과 적용 조건 분석',3,uses=['성공·실패 원인 분석'])
at('improve_needed','능력을 바꿀 필요가 있는가?',4,kind='decision')
at('improve','개선할 지식·방법·도구 준비',5,'실제 업무에는 아직 적용하지 않음',uses=['능력 개선·확장'])
at('learn_test','분리된 환경에서 개선안 시험',6,'개선 효과와 기존 능력·예외·재개까지 검사',uses=['시험 환경','업무 능력 시험'])
at('learn_pass','시험을 통과했는가?',7,kind='decision')
at('learn_budget','보완할 횟수·한도가 남았는가?',7,kind='decision',side=True)
at('apply','통과한 범위·버전만 적용',8,'미통과 개선은 적용하지 않고 기존 버전 유지')
at('learn_save','교훈·추가 작업·다음 확인 일정 기록',9,'추가 대응은 해당 건에 담당·기한·시작 신호 등록',uses=['장기 기억'])
at('followup_finish','이번 후속 확인 종료',10,'다음 예약·새 문제가 생기면 별도로 재개',kind='terminal',role='followup_success')
edge('outcome','outcome_valid');edge('outcome_valid','wait','아니오',kind='blocked',resume='outcome')
edge('outcome_valid','learn_needed','예');edge('learn_needed','cause','예');edge('learn_needed','learn_save','아니오')
edge('cause','improve_needed');edge('improve_needed','improve','예');edge('improve_needed','learn_save','아니오')
edge('improve','learn_test');edge('learn_test','learn_pass');edge('learn_pass','apply','예')
edge('learn_pass','learn_budget','아니오');edge('learn_budget','improve','예 · 보완 후 재시험',kind='return')
edge('learn_budget','learn_save','아니오 · 기존 버전 유지');edge('apply','learn_save');edge('learn_save','followup_finish')
edge('register','outcome','등록한 확인 시점 도래',kind='event')
edge('learn_save','signal','등록한 추가 작업·다음 확인 시점',kind='event')
py=cards('learning_materials',1080,s,480,[
 ('성공·실패 원인 분석','재사용할 성과·영향 큰 문제·반복 오류의 원인과 조건 분석'),
 ('능력 개선·확장','필요한 능력을 보완하고 시험을 통과한 변경만 적용'),
],['cause','improve','learn_test','apply'],'학습·개선에 쓰는 재료',columns=1)
H=max(s+11*200,py)+80
assert set(MATERIALS)==set(CAT),(set(CAT)-set(MATERIALS),set(MATERIALS)-set(CAT))
# Record the canonical uses on the material card even when it is consumed again.
for n in N.values():
    for material in n.get('uses',[]):
        m=N[MATERIALS[material]]
        if n['id'] not in m['consumers']:m['consumers'].append(n['id'])

# Tighten sections by compressing only empty vertical space (same transform for all objects).
# Material banks set the minimum; a long graph must not be scaled down to hide text.
objects=list(N.values())

def port(n,side):
    x,y,w,h=(n[k] for k in ('x','y','w','h'))
    return {'t':(x+w/2,y),'b':(x+w/2,y+h),'l':(x,y+h/2),'r':(x+w,y+h/2)}[side]

def rect_hit(a,b,n,pad=7):
    x0,x1=n['x']-pad,n['x']+n['w']+pad;y0,y1=n['y']-pad,n['y']+n['h']+pad
    if abs(a[0]-b[0])<.01:return x0<a[0]<x1 and max(min(a[1],b[1]),y0)<min(max(a[1],b[1]),y1)
    if abs(a[1]-b[1])<.01:return y0<a[1]<y1 and max(min(a[0],b[0]),x0)<min(max(a[0],b[0]),x1)
    return False

def crossing(a,b,c,d):
    dx,dy=b[0]-a[0],b[1]-a[1];ex,ey=d[0]-c[0],d[1]-c[1];det=dx*ey-dy*ex
    if abs(det)<.001:return None
    u=((c[0]-a[0])*ey-(c[1]-a[1])*ex)/det;v=((c[0]-a[0])*dy-(c[1]-a[1])*dx)/det
    return (a[0]+u*dx,a[1]+u*dy) if .001<u<.999 and .001<v<.999 else None

# Execution links never point into a material shelf. Scope links have no arrow.
for g in G:
    if g['role']=='reference':
        sources=[k for k in g['consumers'] if k in N]
        if sources:
            source=min(sources,key=lambda k:abs(N[k]['y']-g['y']))
            edge(source,g['id'],'이때 쓰는 재료',kind='reference')
all_objects=N|{g['id']:g for g in G}
segments=[]
route_issues=[]
# Route short neighbouring flows first; returns can share a destination corridor.
def route_cost(points,e):
    obstacles=[n for k,n in all_objects.items() if k not in (e['source'],e['target']) and k in N]
    if any(rect_hit(a,b,n) for a,b in zip(points,points[1:]) for n in obstacles):return None
    length=sum(math.dist(a,b) for a,b in zip(points,points[1:]))
    cross=sum(bool(crossing(a,b,c,d)) for a,b in zip(points,points[1:]) for c,d,other in segments
              if not {e['source'],e['target']}&{other['source'],other['target']})
    shared=0
    for a,b in zip(points,points[1:]):
        for c,d,other in segments:
            if {e['source'],e['target']}&{other['source'],other['target']}:continue
            if abs(a[0]-b[0])<.01 and abs(c[0]-d[0])<.01 and abs(a[0]-c[0])<.01:
                shared+=max(0,min(max(a[1],b[1]),max(c[1],d[1]))-max(min(a[1],b[1]),min(c[1],d[1])))
            if abs(a[1]-b[1])<.01 and abs(c[1]-d[1])<.01 and abs(a[1]-c[1])<.01:
                shared+=max(0,min(max(a[0],b[0]),max(c[0],d[0]))-max(min(a[0],b[0]),min(c[0],d[0])))
    return cross*5000+shared*400+length+max(0,len(points)-2)*70
for e in sorted(E,key=lambda e:(e['kind'] in ('return','event'),abs(all_objects[e['source']]['y']-all_objects[e['target']]['y']))):
    a,b=all_objects[e['source']],all_objects[e['target']]
    opts=[]
    if e['kind']=='reference':
        sides=[('r','l')]
    elif a['x']==b['x'] and b['y']>a['y']:
        sides=[('b','t'),('l','l'),('r','r')]
    elif a['x']!=b['x']:
        sides=[('l','r') if a['x']>b['x'] else ('r','l'),('b','t'),('t','b')]
    else:sides=[('l','l'),('r','r'),('t','b')]
    for pair in [('l','t'),('r','t'),('b','l'),('b','r'),('l','b'),('r','b')]:
        if pair not in sides:sides.append(pair)
    for sa,sb in sides:
        p,q=port(a,sa),port(b,sb)
        candidates=[]
        if p[0]==q[0] or p[1]==q[1]:candidates.append([p,q])
        candidates.extend([[p,(p[0],q[1]),q],[p,(q[0],p[1]),q]])
        for xx in [18,32,390,404,418,432,446,964,978,992,1006,1020,1580,1598]:
            candidates.append([p,(xx,p[1]),(xx,q[1]),q])
            off={'t':(0,-22),'b':(0,22),'l':(-22,0),'r':(22,0)}
            u=(p[0]+off[sa][0],p[1]+off[sa][1]);v=(q[0]+off[sb][0],q[1]+off[sb][1])
            candidates.append([p,u,(xx,u[1]),(xx,v[1]),v,q])
        for yy in [(p[1]+q[1])/2,a['y']-22,a['y']+a['h']+22,b['y']-22,b['y']+b['h']+22]:
            candidates.append([p,(p[0],yy),(q[0],yy),q])
        for points in candidates:
            points=[v for i,v in enumerate(points) if i==0 or v!=points[i-1]]
            # The first/last segments must leave/enter the outside of the node.
            if len(points)<2:continue
            valid=True
            for obj,tip,nxt,side in [(a,points[0],points[1],sa),(b,points[-1],points[-2],sb)]:
                if side=='l' and nxt[0]>tip[0] or side=='r' and nxt[0]<tip[0] or side=='t' and nxt[1]>tip[1] or side=='b' and nxt[1]<tip[1]:valid=False
            if not valid:continue
            score=route_cost(points,e)
            if score is not None:opts.append((score,points))
    if not opts:
        route_issues.append((e['source'],e['target']));p,q=port(a,'l'),port(b,'l');pts=[p,(405,p[1]),(405,q[1]),q]
    else:_,pts=min(opts,key=lambda p:p[0])
    e['points']=pts
    for p,q in zip(pts,pts[1:]):segments.append((p,q,e))

# Place each label on its own line, away from cards and arrowheads.
def overlap(a,b,pad=0):
    return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>pad
occupied=[]
for a in A:occupied.append(dict(x=a['x'],y=a['y']-a['size'],w=measure(a['text'],a['size']),h=a['size']+7))
label_issues=[]
for i,e in enumerate(E):
    if not e['label']:continue
    lines=wrap(e['label'],210,18);w=max(measure(s,18) for s in lines)+16;h=len(lines)*24+8
    choices=[]
    for a,b in zip(e['points'],e['points'][1:]):
        length=math.dist(a,b)
        if length<30:continue
        for f in [j/40 for j in range(1,40)]:
            x=a[0]+(b[0]-a[0])*f;y=a[1]+(b[1]-a[1])*f
            r=dict(x=x-w/2,y=y-h/2,w=w,h=h)
            if r['x']<5 or r['x']+w>W-5:continue
            if any(overlap(r,n,-3) for n in N.values()):continue
            if any(overlap(r,n,-3) for n in occupied):continue
            if any(j!=i and not {e['source'],e['target']}&{other['source'],other['target']} and any(rect_hit(c,d,r,1) for c,d in zip(other['points'],other['points'][1:])) for j,other in enumerate(E)):continue
            # Keep a minimum clear distance before the arrow tip.
            if math.dist((x,y),e['points'][-1])<(h/2 if a[0]==b[0] else w/2)+18:continue
            choices.append((math.dist((x,y),e['points'][0])+(80 if a[0]==b[0] else 0),x,y,r))
    if choices:
        _,x,y,r=min(choices)
    else:
        a,b=max(zip(e['points'],e['points'][1:]),key=lambda pair:math.dist(*pair))
        x,y=(a[0]+b[0])/2,(a[1]+b[1])/2;r=dict(x=x-w/2,y=y-h/2,w=w,h=h)
        label_issues.append((e['source'],e['target'],e['label']))
    e.update(at=(x,y),label_rect=r,label_lines=lines);occupied.append(r)

# Non-joining crossings are rendered with a visible bridge, never as a junction.
bridges=[]
for i,e in enumerate(E):
    for j,f in enumerate(E[:i]):
        if {e['source'],e['target']}&{f['source'],f['target']}:continue
        for a,b in zip(e['points'],e['points'][1:]):
            for c,d in zip(f['points'],f['points'][1:]):
                point=crossing(a,b,c,d)
                if point:bridges.append(dict(edge=i,point=point,horizontal=abs(a[1]-b[1])<.1))

model=dict(width=W,height=math.ceil(H),nodes=N,groups=G,edges=E,annotations=A,catalog=CAT,
           system_styles=SYSTEM_STYLE,system_mapping=TERM_SYSTEMS,illustrations=[],
           source_prefix_sha256=hashlib.sha256(PREFIX.encode()).hexdigest(),
           execution_contract=dict(guarded_scope='all_steps',before_every=['input','output','action','retry','resume'],
               gate='permit',deny='stop',unknown='wait',human='human',preserve_completed=True,
               selected_join='join',join_requires='all selected required results or explicit failed/pending status',
               resume_uses_saved_target=True,retry_limit_required=True),
           bridges=bridges,route_issues=route_issues,label_issues=label_issues)
esc=lambda s:html.escape(str(s),quote=True)
colors={'flow':C['blue'],'return':C['yellow'],'blocked':C['red'],'reference':'#8396A1','event':'#27866A'}
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{math.ceil(H)}" viewBox="0 0 {W} {math.ceil(H)}">',
 '<title>한 건을 한 전문가가 처리하는 실행 흐름과 79개 재료</title>',
 '<rect width="100%" height="100%" fill="white"/>',
 '<g font-family="Apple SD Gothic Neo,Noto Sans CJK KR,sans-serif" fill="#192C36">']
for g in G:
    o.append(f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="12" fill="#FAFCFD" stroke="#CADFE9" stroke-dasharray="3 7"/>')
for i,e in enumerate(E):
    pts=e['points'];dash=' stroke-dasharray="6 6"' if e['kind'] in ('reference','event') else ''
    d='M'+' L'.join(f'{x},{y}' for x,y in pts)
    o.append(f'<path class="edge" data-id="e{i}" d="{d}" fill="none" stroke="{colors[e["kind"]]}" stroke-width="2.7"{dash}/>')
for bridge in bridges:
    x,y=bridge['point'];e=E[bridge['edge']]
    d=f'M{x-8},{y} Q{x},{y-12} {x+8},{y}' if bridge['horizontal'] else f'M{x},{y-8} Q{x-12},{y} {x},{y+8}'
    o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="white"/><path class="bridge" d="{d}" fill="none" stroke="{colors[e["kind"]]}" stroke-width="2.7"/>')
for k,n in N.items():
    x,y,w,h=(n[t] for t in ('x','y','w','h'));kind=n['kind'];is_material=bool(n['material'])
    palette=SYSTEM_STYLE[n['term']] if is_material else None
    fill=palette['fill'] if palette else '#FFFFFF'
    if kind=='unused':fill='#F2F4F6'
    o.append(f'<g class="node" data-id="{k}" data-material="{esc(n["material"] or "")}">')
    if kind=='decision':
        shape=f'<path class="shape" d="M{x+w/2},{y} L{x+w},{y+h/2} L{x+w/2},{y+h} L{x},{y+h/2} Z"';fill='#FFF5C6'
    else:
        if kind=='terminal':fill='#E7F5E9' if n.get('role') in ('start','success','followup_success') else '#FFF0EC'
        shape=f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if kind=="terminal" else 5}"'
    o.append(shape+f' fill="{fill}" stroke="#314650" stroke-width="1.7"/>')
    z=22 if is_material else 23 if kind=='decision' else 25
    titles=wrap(n['title'],w*(.67 if kind=='decision' else 1)-28,z)
    bs=19 if is_material else 20;body=wrap(n['body'],w-28,bs) if n['body'] else []
    if is_material:
        badge=n['term']+' · '+('단독 미사용' if kind=='unused' else n['usage'])
        o.append(f'<text class="system-label" x="{x+13}" y="{y+22}" font-size="16" font-weight="700" fill="{palette["accent"]}">{esc(badge)}</text>')
        yy=y+25+z
    else:yy=y+(h-(len(titles)*29+len(body)*25+(6 if body else 0)))/2+z
    for text in titles:
        o.append(f'<text class="node-title" x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="{z}" font-weight="800">{esc(text)}</text>');yy+=27 if is_material else 29
    yy+=6 if body else 0
    for text in body:
        o.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="{bs}" fill="#526773">{esc(text)}</text>');yy+=24 if is_material else 25
    o.append('</g>')
for i,e in enumerate(E):
    if e['label']:
        r=e['label_rect'];x,y=e['at']
        o.append(f'<g class="edge-label" data-edge="e{i}"><rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" rx="4" fill="white" stroke="{colors[e["kind"]]}" stroke-width=".8"/>')
        for j,t in enumerate(e['label_lines']):
            o.append(f'<text x="{x}" y="{r["y"]+23+j*24}" text-anchor="middle" font-size="18" font-weight="600">{esc(t)}</text>')
        o.append('</g>')
    if e['kind']=='reference':continue
    a,b=e['points'][-2:];length=math.dist(a,b);u=((b[0]-a[0])/length,(b[1]-a[1])/length)
    tip=(b[0]-u[0]*3,b[1]-u[1]*3);base=(tip[0]-u[0]*15,tip[1]-u[1]*15)
    arrow=[tip,(base[0]-u[1]*6,base[1]+u[0]*6),(base[0]+u[1]*6,base[1]-u[0]*6)]
    e['arrow']=arrow
    o.append(f'<polygon class="arrowhead" data-edge="e{i}" points="'+ ' '.join(f'{x},{y}' for x,y in arrow)+f'" fill="{colors[e["kind"]]}"/>')
for a in A:o.append(f'<text class="annotation" x="{a["x"]}" y="{a["y"]}" font-size="{a["size"]}" font-weight="{a["weight"]}" fill="{a["color"]}">{esc(a["text"])}</text>')
o+=['</g>','<metadata>'+esc(json.dumps(model,ensure_ascii=False))+'</metadata>','</svg>']
(ROOT/'docs/images/expert-definition/solo-material-relations.svg').write_text('\n'.join(o))
(ROOT/'docs/도식/단독-재료-연결구조.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(materials=len(MATERIALS),nodes=len(N),edges=len(E),width=W,height=H,
                     route_issues=route_issues,label_issues=label_issues,bridges=len(bridges)),ensure_ascii=False))
