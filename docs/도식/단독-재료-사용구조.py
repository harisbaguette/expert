#!/usr/bin/env python3
"""Illustrated operational map: execution flow plus scoped material relationships.

Only the left-hand action/decision/terminal nodes form the control graph.
Material cards are explicitly scoped to an action or to the whole operation;
their arrangement never asserts that every material must execute in sequence.
"""
from pathlib import Path
from collections import Counter
import base64, hashlib, html, json, math, re

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / '전문가 에이전트 정의.md'
PREFIX = DOC.read_text().split('## 사용 구조', 1)[0]
CAT = {}
for line in PREFIX.split('## 계통별 재료', 1)[1].splitlines():
    if line.startswith('| **') and '✅' in line:
        cols = [x.strip() for x in line.strip('|').split('|')]
        if len(cols) == 6:
            name = re.search(r'\*\*(.*?)\*\*', cols[0])[1]
            CAT[name] = dict(name=name, definition=cols[2], usage=cols[4].strip('*'), condition=cols[5])
assert len(CAT) == 79

W = 1660
C = dict(ink='#202B32', muted='#506472', blue='#2094E6', red='#D95151', yellow='#D59B00',
         sky='#E6F5FD', gray='#879AA5', boundary='#BBD5E2', white='#FFFFFF')
ESC = lambda x: html.escape(str(x), quote=True)
N, M, G, E, T, I = {}, {}, {}, [], [], []
ATLAS = 'data:image/png;base64,' + base64.b64encode((ROOT / 'docs/images/expert-definition/assets/solo-expert-illustrations.png').read_bytes()).decode()


def width(text, size):
    return sum(size * (1 if ord(c) > 255 else .52 if c != ' ' else .28) for c in text)


def wrap(text, w, size):
    out = []
    for paragraph in text.split('\n'):
        row = ''
        for word in paragraph.split(' '):
            if row and width(row + ' ' + word, size) > w:
                out.append(row); row = word
            else:
                row += (' ' if row else '') + word
        out.append(row)
    return out


def text(x, y, s, size=21, weight=400, color=None, anchor='start'):
    T.append(dict(x=x, y=y, text=s, size=size, weight=weight, color=color or C['ink'], anchor=anchor))


def group(key, x, y, w, h, title, note='', owner=None, kind='materials'):
    G[key] = dict(id=key, x=x, y=y, w=w, h=h, title=title, note=note, owner=owner, kind=kind)


def material(key, name, x, y, w, note, scope, h=112, kind='material'):
    assert name in CAT
    title = wrap(name, w - 30, 24)
    lines = wrap(note, w - 30, 20)
    h = max(h, 28 * len(title) + 25 * len(lines) + 33)
    M[key] = dict(id=key, name=name, x=x, y=y, w=w, h=h, title=title, body=lines,
                  note=note, scope=scope, kind=kind, usage=CAT[name]['usage'])
    return h


def cards(prefix, items, x, y, w, cols, scope, gap=22, h=112):
    cw=(w-gap*(cols-1))/cols
    ids=[]; yy=y
    for r in range(math.ceil(len(items)/cols)):
        heights=[]
        for c, (name, note) in enumerate(items[r*cols:(r+1)*cols]):
            key=f'{prefix}_{r*cols+c}';ids.append(key)
            heights.append(material(key,name,x+c*(cw+gap),yy,cw,note,scope,h))
        yy+=max(heights)+22
    return ids, yy-22


def node(key, title, x, y, w=330, h=96, kind='process', note='', art=None):
    N[key]=dict(id=key,title=title,x=x,y=y,w=w,h=h,kind=kind,note=note,art=art)


def action(key, title, y, art, note=''):
    node(key,title,80,y,330,280,'action',note,art)


def port(key, side, offset=0):
    n=(N|M|G)[key];x,y,w,h=[n[k] for k in ('x','y','w','h')]
    return {'t':(x+w/2+offset,y),'b':(x+w/2+offset,y+h),
            'l':(x,y+h/2+offset),'r':(x+w,y+h/2+offset)}[side]


def edge(a,b,kind='flow',label='',sa='b',sb='t',via=(),at=None,start=None,end=None):
    pts=[start or port(a,sa),*via,end or port(b,sb)]
    if len(pts)==2 and pts[0][0]!=pts[1][0] and pts[0][1]!=pts[1][1]:
        ax,ay=pts[0];bx,by=pts[1]
        if sa in ('l','r') and sb in ('l','r'):
            xx=(ax+bx)/2;pts=[(ax,ay),(xx,ay),(xx,by),(bx,by)]
        else:
            yy=(ay+by)/2;pts=[(ax,ay),(ax,yy),(bx,yy),(bx,by)]
    E.append(dict(source=a,target=b,kind=kind,label=label,points=pts,at=at))


def stage(key,title,y,h,art,items=None,note=''):
    action(key,title,y+70,art)
    group(key+'_materials',490,y,1110,h,'이때 쓰는 재료',note,owner=key)
    edge(key,key+'_materials','apply',sa='r',sb='l',end=(490,y+210))
    if items:
        return cards(key,items,515,y+100,1060,3,key)


# A single enclosing scope says exactly which materials remain active.
group('all',55,35,1560,100,'',kind='scope',owner='ALL')
group('foundation',490,65,1110,350,'모든 단계에서 계속 작동',
      '아래 기반은 접수부터 대기·재개·종료까지 이어진다.',owner='ALL')
cards('base',[
    ('현재 작업 정보','판단에 필요한 목표·자료·상태'),
    ('AI 모델','그 정보를 읽고 판단·생성'),
    ('실행 제어','판단·도구 호출과 결과를 연결'),
    ('작업 진행·연결','준비된 작업을 끝까지 이어감'),
    ('현재 진행 상태','완료·대기·승인·남은 일 유지'),
    ('판단 근거 기록','입력·선택·변경·검사 근거 기록'),
    ('분리 실행','자료·작업·시험 공간과 권한 분리'),
    ('운영 감시·복구','별도 감시로 장애 복구·상태 복원'),
],515,155,1060,4,'ALL',gap=18,h=110)
G['foundation']['h']=max(n['y']+n['h'] for n in M.values())-65+25
node('start','한 건의 처리 시작',80,75,330,76,'terminal', '새 요청 또는 맡은 건의 재개')
material('no_delegate','나눠 맡기기',80,225,330,'이 상황에서는 미사용\n한 전문가가 직접 처리','ALL',kind='unused')
text(90,412,'파랑: 진행   노랑: 복귀',18,color=C['muted'])
text(90,440,'빨강: 아니오·보류',18,color=C['muted'])
text(90,468,'회색: 재료의 제공·적용',18,color=C['muted'])

# Intake: optional observers are scoped materials, not untriggered processes.
A=550
_,aend=stage('intake','요청과 목표를 정한다',A,680,0,[
    ('시작 신호','요청·변경·답변을 해당 건에 연결'),
    ('업무별 정보','대상·자료·기한·현황을 모음'),
    ('정보·자료 이해','내용·맥락과 사실·주장을 구별'),
    ('지시·의도 파악','원하는 결과·범위 확인\n중요한 모호함은 질문'),
    ('문제·목표·완료 조건','해결할 문제와\n완료를 판단할 기준을 정함'),
    ('성과 추적','무엇을 언제 확인해야\n성과를 알 수 있는지 정함'),
],note='새 건은 목표를 정하고, 재개한 건은 저장된 목표·완료분을 확인한다.')
text(515,aend+51,'감시까지 맡은 업무라면',23,700)
_,aend=cards('signal',[
    ('먼저 알아채기','여러 단서에서 새 문제·기회를 찾아\n맡은 범위 안의 대응 이유를 알림'),
    ('변경 감시·반영','바뀐 규칙·근거·상태가 영향을 주는\n자료·판단·결과를 재검토 대상으로 연결'),
],515,aend+75,1060,2,'intake')
G['intake_materials']['h']=aend-A+25
edge('start','intake',via=[(245,180),(65,180),(65,A+35),(245,A+35)])

# Sources are used as inputs, never asserted to be chronological steps.
B=A+G['intake_materials']['h']+95
_,bend=stage('evidence','필요한 근거를 갖춘다',B,720,1,[
    ('정보·자료 찾기','부족한 정보·방법·원문을 확보'),
    ('못 찾음·없음 구분','빈 검색을 “없음”으로 단정하지 않음'),
    ('현재 값·상태 확인','현재 값이 판단을 바꿀 때 조회'),
    ('적용 사례','조건·근거·결과가 비슷한 사례 비교'),
    ('참고 자료','필요한 원리·방법·표현을 참고'),
    ('재사용 자료','권리·판본·환경에 맞는 서식·부품'),
    ('업무 지식','원리·방법·적용 조건·예외로 해석'),
    ('실전 경험·감각','중요한 단서와 대응 요령을 대조'),
    ('장기 기억','관련된 이전 결정·약속·교훈을 꺼냄'),
    ('근거의 신뢰성·적합성','출처·증거 등급과 이번 대상 적합성'),
    ('자료의 시점·버전','판단할 시점에 맞는 원문·판본'),
],note='필요한 것만 확보한다. 자료·지식은 이후 계획·수행·검증에서도 쓰고, 새 정보가 오면 보완한다.')
G['evidence_materials']['h']=bend-B+25
edge('intake','evidence')

# Rule ranking is one application relationship, not seven execution stages.
R=B+G['evidence_materials']['h']+95
stage('rules','지킬 기준을 맞춘다',R,1000,1,note='법적 관계부터 확인하고, 충돌 조항에만 위계를 적용한다. 정한 기준은 이후 판단·실행에도 계속 적용한다.')
_,ry=cards('rulebase',[
    ('규칙·기준 원문','출처·설정 권한·적용 범위·시점 확보'),
    ('법·의무 기준','상하·특별·위임 관계와 적용 예외 확인'),
],515,R+100,1060,2,'rules')
for rank,label,items in [
    ('①','필수 의무·원칙',[('직업 윤리·의무','비밀·충실·이해충돌 관리'),('에이전트 기본 원칙','목적·범위 준수와 근거 정직성')]),
    ('②','유효한 약속·필수 규정',[('계약·합의 조건','변경·종료 후 남은 의무도 적용'),('플랫폼·제출처 규정','서비스·제출 유형의 필수 조건')]),
    ('③','조직의 필수 규정',[('조직 규칙','업무·역할별 규정과 유효한 예외')]),
    ('④','사용자의 추가 조건',[('사용자 지정 규칙','추가 조건·선호의 변경·취소 반영')]),
    ('⑤','표현 기준',[('표현 방식·스타일','표현이 필요한 작업의 문체·디자인')]),
]:
    yy=ry+25
    text(520,yy+32,rank,27,750);text(565,yy+32,label,20,650)
    _,ry=cards('rank'+rank,items,820,yy,755,2,'rules',h=92)
ry+=28
material('rule_apply','규칙의 적용·우선순위',515,ry,1060,
         '충돌 조항은 ①→⑤로 판단 · 충돌하지 않는 조건과 보호 기준은 함께 유지\n예외 요건·결정 권한까지 확인하고, 해결되지 않은 쟁점은 보류하거나 결정권자에게 연결','rules',h=120)
G['rules_materials']['h']=M['rule_apply']['y']+M['rule_apply']['h']-R+25
edge('evidence','rules')

# Plan and pre-execution permission. The control flow includes a real human gate.
P=R+G['rules_materials']['h']+95
_,pend=stage('plan','방법과 작업을 정한다',P,770,2,[
    ('대안·전략 판단','효과·부담·위험을 비교해 방법 선택'),
    ('업무 절차·실행 계획','재료·입출력·선후·검사·중단 조건'),
    ('빠진 위험 확인','접수·계획·실행·전달 때 빠진 위험'),
    ('업무 권한','대상·행동·승인 범위와 유효성'),
    ('비용·위험 한도','사용·진행·예약분과 대기 위험'),
    ('안전장치','수신·실행·재개 직전 조건을 대조'),
    ('시험 환경','격리·비교·재현이 필요한 시험 준비'),
    ('업무 능력 시험','첫 투입·범위 밖·변경 때 시험\n통과한 능력·판본만 사용'),
],note='한 전문가가 할 작업과 필요한 재료를 고른다. 다음 작업과 재시도에도 현재 조건을 다시 확인한다.')
G['plan_materials']['h']=pend-P+25
node('permit','지금 실행할 수 있는가?',95,pend+90,300,170,'decision')
edge('plan','permit')
edge('rules','plan')
node('blocked','이 작업 중단·보류',520,pend+125,350,94,'stop','위반·필수 근거 미확보·해결 불가')
edge('permit','blocked','blocked','위반·\n확인 불가',sa='r',sb='l',at=(457,pend+150))
node('human','사람에게 넘기기',1010,pend+70,560,125,'process',
     '조사·대안·준비·검증 후 결정만 요청\n되돌릴 수 없는 일·필수 승인·판단 불가\n한도 초과·자격자 전속에 해당할 때')
N['human']['material']='사람에게 넘기기'
edge('permit','human','blocked','사람의 결정 필요',sa='r',sb='t',
     start=(335,pend+141),via=[(440,pend+40),(1290,pend+40)],at=(915,pend+40))
node('identity','보고 주체 확인',1010,pend+235,560,95,'process','답변 주체·권한·승인 대상·판본 대조')
N['identity']['material']='보고 주체 확인'
node('human_valid','유효한 결정을 받았는가?',1120,pend+395,340,155,'decision')
edge('human','identity');edge('identity','human_valid')
edge('human_valid','permit','return','예 · 현재 조건으로 재검사',sa='l',sb='b',
     via=[(940,pend+472.5),(940,pend+305),(360,pend+305)],end=(320,pend+217.5),at=(655,pend+305))
node('human_hold','결정 미확정 · 보류',1100,pend+625,380,85,'stop','거절·불일치·기한 종료 기록')
edge('human_valid','human_hold','blocked','아니오',at=(1290,pend+585))
PEND=pend+760

# A palette of named, conditional capabilities belongs to ONE execution action.
# This intentionally has no false calculation→prediction→optimization sequence.
X=PEND+50
stage('work','고른 재료로 직접 처리한다',X,1600,3,note='아래 재료 중 이번 작업에 필요한 것만 조합한다. 왼쪽에서 오른쪽으로 전부 실행하는 목록이 아니다.')
work_sets=[
 ('새 기록·시험 결과가 필요할 때',[
  ('관찰·측정','새 값·기록을 얻을 때'),('실험','조건 변화의 영향을 비교할 때'),('시뮬레이션','가정한 상황을 시험할 때')]),
 ('자료를 작업에 맞게 다듬을 때',[
  ('자료 선별·분류','필요한 항목을 고르고 나눌 때'),('자료 정리·결합','오류·중복을 정리하고 합칠 때'),('형식·구조 변환','다음 작업과 형식이 다를 때')]),
 ('값·해석·판단이 필요할 때',[
  ('계산','값·식·단위·가정을 확인'),('분석','관계·차이·원인을 해석'),('예측','미래 결과와 불확실성 예상'),
  ('조건 안에서 최선 찾기','조건 안의 유리한 안을 비교'),('기준 적용·판정','요건·예외에 맞는지 판단')]),
 ('결과물의 내용과 형태를 만들 때',[
  ('결과물 설계','구조·내용·작동을 정할 때'),('내용 재구성','요약·번역·표현을 바꿀 때'),('결과물 만들기·수정','설계·입력을 결과물로 만들 때')]),
 ('사람과 대화하거나 조정할 때',[
  ('실시간 대화','바로 답을 주고받는 통로'),('사람과 소통','질문·설명·이해 확인이 필요할 때'),('협상·조율','요구·역할·약속을 조정할 때')]),
 ('외부 시스템에 반영할 때',[
  ('기록 입력·수정','기록을 등록·변경·삭제할 때'),('신청·거래 처리','신청·취소·환불 등을 맡았을 때'),
  ('설정·작동 제어','설정·권한·작동을 바꿀 때'),('게시·배포','판본·대상·시점에 맞춰 공개')]),
]
wy=X+110
for r in range(3):
    ends=[]
    for col in range(2):
        idx=2*r+col;heading,items=work_sets[idx];xx=515+col*550
        text(xx,wy,heading,23,750)
        _,yy=cards('workset'+str(idx),items,xx,wy+25,510,2,'work',gap=18,h=118)
        ends.append(yy)
    wy=max(ends)+65
material('tools','업무 도구·시스템',515,wy,1060,
         '도구가 필요한 작업에서 요청·응답을 연결하고 실제 결과·오류·진행 상태를 돌려받음\n미확인 외부 처리는 상태부터 조회 · 모든 외부 전송·변경은 현재 권한·한도 재확인','work',h=125)
G['work_materials']['h']=M['tools']['y']+M['tools']['h']-X+25
edge('permit','work','flow','허용',at=(245,PEND-5))

# One concrete combination clarifies the generic capability palette in situ.
exy=X+485
group('example',80,exy,330,595,'함께 쓰는 관계의 예',owner='work',kind='example')
material('ex_calc','계산',100,exy+60,290,'필요한 값을 구함','work',h=95)
material('ex_analyze','분석',100,exy+220,290,'계산값을 해석함','work',h=95)
edge('ex_calc','ex_analyze','data','계산값',at=(245,exy+190))
material('ex_knowledge','업무 지식',100,exy+400,290,'해석에 필요한 원리·조건·예외','work',h=105)
edge('ex_knowledge','ex_analyze','apply','해석 근거',sa='t',sb='b',at=(245,exy+358))
text(100,exy+552,'분석 결과는 다음 작업의 입력',18,color=C['muted'])
# The main connector travels outside this explanatory inset.

# Validation has meaningful failure, waiting and success routes.
V=X+G['work_materials']['h']+95
_,vend=stage('verify','결과와 완료 조건을 대조한다',V,520,4,[
    ('보고 주체 확인','외부 결과·답변의 주체·권한 확인'),
    ('결과 검증·재검증','근거·완료 조건·다음 입력과 대조'),
    ('반대 근거·다시 확인','중요한 판단은 다른 설명도 대조'),
    ('결과 품질 평가','정확성·충분성·사용성 확인'),
    ('일하는 과정 평가','방법·순서·권한 준수 평가'),
    ('빠진 위험 확인','사용·전달 전에 남은 위험 재확인'),
],note='중간 결과도 다음 작업에 쓰기 전에 확인한다. 바뀐 부분과 영향을 받은 결과를 함께 재검증한다.')
G['verify_materials']['h']=vend-V+25
edge('work','verify',via=[(245,X+430),(65,X+430),(65,V+40),(245,V+40)])
node('quality','완료 조건을 충족했는가?',95,vend+85,300,170,'decision')
edge('verify','quality')
edge('quality','plan','return','보완·\n남은 일',sa='l',sb='l',
     via=[(45,vend+170),(45,P+260)],end=(80,P+260),at=(85,vend+95))
node('wait','대기·후속 관리',550,vend+115,465,115,'process',
     '미확인 외부 처리·답변·기한 조회\n완료분 유지 · 같은 실행을 반복하지 않음')
N['wait']['material']='대기·후속 관리'
edge('quality','wait','blocked','아직 확인 불가',sa='r',sb='l',at=(470,vend+150))
node('wait_result','기다린 결과는?',1170,vend+95,300,165,'decision')
edge('wait','wait_result',sa='r',sb='l')
edge('wait_result','verify','return','확인됨 · 재검증',sa='t',sb='r',
     via=[(1320,vend+50),(440,vend+50),(440,V+280)],end=(410,V+280),at=(975,vend+50))
edge('wait_result','wait','return','미확인 · 다음 시점까지 대기',sa='b',sb='b',
     via=[(1320,vend+315),(782.5,vend+315)],at=(1050,vend+315))
node('wait_hold','이번 처리 보류',1160,vend+420,350,85,'stop','기한 종료·거절 · 재개 조건 기록')
edge('wait_result','wait_hold','blocked','기한 종료·거절',sa='r',sb='r',
     via=[(1560,vend+177.5),(1560,vend+462.5)],at=(1500,vend+365))

# Receipt is not assumed merely because a deliverable was sent.
D=vend+610
_,dend=stage('delivery','결과를 전달하고 인수받는다',D,340,4,[
    ('납품 준비','결과·판본·설명·남은 일을 정리'),
    ('전달·인수 확인','약속한 상대의 수령·사용을 확인'),
],note='한 전문가가 최종 결과와 후속 책임까지 정리한다.')
G['delivery_materials']['h']=dend-D+25
edge('quality','delivery','flow','예',at=(245,D-45))
node('received','인수 결과는?',95,D+440,300,170,'decision')
edge('delivery','received')
edge('received','plan','return','수정 요청',sa='l',sb='l',
     via=[(25,D+525),(25,P+210)],end=(80,P+210),at=(85,D+465))
node('receipt_wait','대기·후속 관리',580,D+470,470,110,'process','답변·확인 시점·기한과 후속 책임 유지')
N['receipt_wait']['material']='대기·후속 관리'
edge('received','receipt_wait','blocked','미응답',sa='r',sb='l',at=(485,D+525))
edge('receipt_wait','received','return','답변·확인 시점 도래',sa='t',sb='r',
     via=[(815,D+370),(465,D+370),(465,D+480)],end=(315,D+479.6666666667),at=(690,D+370))
node('receipt_stop','인수 미완료 · 보류',1190,D+470,360,90,'stop','거절·기한 종료 · 남은 책임 기록')
edge('received','receipt_stop','blocked','거절·기한 종료',sa='b',sb='b',
     start=(320,D+567.5),via=[(450,D+655),(1370,D+655)],at=(1020,D+655))

# Outcome evaluation, conditional improvement and an explicit terminal.
F=D+785
_,fend=stage('learn','성과를 확인하고 다음에 반영한다',F,580,5,[
    ('성과 추적','처음 정한 시점·항목으로 실제 효과 확인'),
    ('성공·실패 원인 분석','재사용할 성과·중요한 문제의 원인'),
    ('능력 개선·확장','필요한 지식·방법·도구를 개선'),
    ('시험 환경','개선안을 분리된 조건에서 시험'),
    ('업무 능력 시험','개선 효과와 기존 능력 유지 확인'),
    ('장기 기억','결정·약속·교훈을 근거와 함께 보존'),
],note='실패·보류 기록도 평가에 포함한다. 개선이 필요하면 원인 분석→개선→시험으로 이어 가고, 통과한 변경만 적용한다.')
G['learn_materials']['h']=fend-F+25
edge('received','learn','flow','인수 확인',at=(245,F-65))
node('finish','이번 처리 종료',80,fend+90,330,85,'terminal','남은 후속 확인·책임은 유지')
edge('learn','finish')
H=fend+230
G['all']['h']=H-70

for key,title in {
    'intake':'요청·자료 → 목표와 완료 기준',
    'evidence':'자료·지식 → 판단의 근거',
    'rules':'원문·의무 → 함께 지킬 기준',
    'plan':'방법·조건 → 실행할 작업과 순서',
    'work':'선택한 재료 → 이번 작업의 결과',
    'verify':'작업 결과 → 근거와 완료 기준에 대조',
    'delivery':'최종 결과 → 상대의 수령·사용 확인',
    'learn':'실제 성과 → 검증된 지식·방법',
}.items():
    G[key+'_materials']['title']=title

# Typed relationships and explicit ownership make disconnected execution tests
# possible without mistaking support material for an untriggered action.
seen={m['name'] for m in M.values()}|{n['material'] for n in N.values() if n.get('material')}
assert seen==set(CAT),(set(CAT)-seen,seen-set(CAT))
MODEL=dict(width=W,height=H,nodes=N,materials=M,groups=G,edges=E,texts=T,catalog=CAT,
           source_prefix_sha256=hashlib.sha256(PREFIX.encode()).hexdigest())


def poly(points,r=12):
    pts=[points[0]]
    for p in points[1:]:
        if p!=pts[-1]:pts.append(p)
    out=f'M {pts[0][0]} {pts[0][1]}'
    for i in range(1,len(pts)-1):
        a,b,c=pts[i-1:i+2];l1=math.dist(a,b);l2=math.dist(b,c);rr=min(r,l1/2,l2/2)
        u=(b[0]+(a[0]-b[0])*rr/l1,b[1]+(a[1]-b[1])*rr/l1)
        v=(b[0]+(c[0]-b[0])*rr/l2,b[1]+(c[1]-b[1])*rr/l2)
        out+=f' L {u[0]} {u[1]} Q {b[0]} {b[1]} {v[0]} {v[1]}'
    return out+f' L {pts[-1][0]} {pts[-1][1]}'


def illustration(idx,x,y,w,h):
    sx=(idx%2)*627;sy=(idx//2)*418
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{sx} {sy} 627 418" overflow="hidden"><use href="#expert-atlas"/></svg>'


out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
     '<title>한 건 · 한 전문가의 재료 사용 구조</title>', '<rect width="100%" height="100%" fill="white"/>',
     '<defs>']
out.append(f'<image id="expert-atlas" href="{ATLAS}" x="0" y="0" width="1254" height="1254"/>')
for k,col in [('flow',C['blue']),('blocked',C['red']),('return',C['yellow'])]:
    out.append(f'<marker id="{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{col}"/></marker>')
out+=['</defs>','<g font-family="Apple SD Gothic Neo, Noto Sans CJK KR, sans-serif" fill="'+C['ink']+'">']
for k,g in G.items():
    x,y,w,h=[g[t] for t in ('x','y','w','h')]
    out.append(f'<g class="scope" data-id="{k}"><rect class="scope-shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="white" stroke="{C["boundary"]}" stroke-width="1.6" stroke-dasharray="3 9"/>')
    if g['title']:
        out.append(f'<text x="{x+24}" y="{y+38}" font-size="27" font-weight="800">{ESC(g["title"])}</text>')
    if g['note']:
        lines=wrap(g['note'],w-45,20)
        for i,line in enumerate(lines):out.append(f'<text x="{x+24}" y="{y+68+24*i}" font-size="20" fill="{C["muted"]}">{ESC(line)}</text>')
    out.append('</g>')
for i,e in enumerate(E):
    color={'flow':C['blue'],'blocked':C['red'],'return':C['yellow'],'apply':C['gray'],'data':C['gray']}[e['kind']]
    marker=f' marker-end="url(#{e["kind"]})"' if e['kind'] in ('flow','blocked','return') else ''
    out.append(f'<path class="edge" data-id="e{i}" data-kind="{e["kind"]}" d="{poly(e["points"])}" fill="none" stroke="{color}" stroke-width="{4 if marker else 2}" stroke-linejoin="round" stroke-linecap="round"{marker}/>')
for k,m in M.items():
    x,y,w,h=[m[t] for t in ('x','y','w','h')]
    unused=m['kind']=='unused'
    out.append(f'<g class="material" data-id="{k}" data-material="{ESC(m["name"])}" data-scope="{ESC(m["scope"])}">')
    # Material cards have a small folded corner, unlike executable process boxes.
    out.append(f'<path class="shape" d="M{x} {y}H{x+w-14}L{x+w} {y+14}V{y+h}H{x}Z" fill="{C["white"]}" stroke="{C["gray"] if unused else C["ink"]}" stroke-width="1.4"/>')
    out.append(f'<path d="M{x+w-14} {y}V{y+14}H{x+w}" fill="none" stroke="{C["gray"]}" stroke-width="1"/>')
    yy=y+29
    for line in m['title']:
        out.append(f'<text class="material-name" x="{x+14}" y="{yy}" font-size="24" font-weight="800">{ESC(line)}</text>');yy+=28
    yy+=3
    for line in m['body']:
        out.append(f'<text x="{x+14}" y="{yy}" font-size="20" fill="{C["muted"]}">{ESC(line)}</text>');yy+=25
    out.append('</g>')
for k,n in N.items():
    x,y,w,h=[n[t] for t in ('x','y','w','h')];kind=n['kind']
    out.append(f'<g class="node" data-id="{k}" data-material="{ESC(n.get("material",""))}" data-kind="{kind}">')
    fill={'terminal':'#E3F4E8','stop':'#FFF0EC','decision':'#FFF5C5','action':'#FFFFFF','process':'#EDF8FE'}[kind]
    if kind=='decision':out.append(f'<path class="shape" d="M{x+w/2} {y}L{x+w} {y+h/2}L{x+w/2} {y+h}L{x} {y+h/2}Z" fill="{fill}" stroke="{C["ink"]}" stroke-width="2"/>')
    else:out.append(f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if kind in ("terminal","stop") else 7}" fill="{fill}" stroke="{C["ink"]}" stroke-width="2"/>')
    if kind=='action':
        out.append(illustration(n['art'],x+15,y+8,w-30,190))
        lines=wrap(n['title'],w-28,27);yy=y+224
        for line in lines:out.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="27" font-weight="850">{ESC(line)}</text>');yy+=33
    else:
        titles=wrap(n['title'],w*.7 if kind=='decision' else w-25,24)
        notes=wrap(n['note'],w-26,20) if n['note'] else []
        yy=y+(h-len(titles)*29-len(notes)*24)/2+23
        for line in titles:out.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="24" font-weight="800">{ESC(line)}</text>');yy+=29
        for line in notes:out.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="20" fill="{C["muted"]}">{ESC(line)}</text>');yy+=24
    out.append('</g>')
for i,e in enumerate(E):
    if not e['label']:continue
    x,y=e['at'] or ((e['points'][0][0]+e['points'][-1][0])/2,(e['points'][0][1]+e['points'][-1][1])/2)
    lines=e['label'].split('\n');w=max(width(s,20) for s in lines)+18;h=26*len(lines)+12
    out.append(f'<g class="edge-label" data-edge="e{i}"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="5" fill="white"/>')
    for j,line in enumerate(lines):out.append(f'<text x="{x}" y="{y-h/2+25+j*26}" text-anchor="middle" font-size="20" font-weight="600" fill="{C["yellow"] if e["kind"]=="return" else C["ink"]}">{ESC(line)}</text>')
    out.append('</g>')
for t in T:
    out.append(f'<text class="annotation" x="{t["x"]}" y="{t["y"]}" font-size="{t["size"]}" font-weight="{t["weight"]}" text-anchor="{t["anchor"]}" fill="{t["color"]}">{ESC(t["text"])}</text>')
out+=['</g>','<metadata id="material-use-model">'+ESC(json.dumps(MODEL,ensure_ascii=False))+'</metadata>','</svg>']
(ROOT/'docs/images/expert-definition/solo-material-use.svg').write_text('\n'.join(out))
(ROOT/'docs/도식/단독-재료-사용구조.json').write_text(json.dumps(MODEL,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(materials=len(seen),control_nodes=len(N),material_cards=len(M),edges=len(E),width=W,height=H),ensure_ascii=False))
