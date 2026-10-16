#!/usr/bin/env python3
"""신뢰성 사용 구조를 단독 상황 도식의 시각 규칙으로 그린다."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/images/expert-definition/judgment-reliability-usage.svg'
SOURCE = ROOT / 'docs/도식/judgment-reliability-usage.mmd'
W, H = 1800, 16080
INK, MUTED, BORDER = '#17253B', '#475569', '#BACBDD'
BLUE, AMBER, RED = '#3974B8', '#B57C1F', '#C45763'
N, E, P, SECTIONS = {}, [], [], []
esc = lambda s: html.escape(str(s), quote=True)


def width(s, size):
    return sum(size * (.96 if ord(c) > 255 else .30 if c == ' ' else .54) for c in s)


def wrap(s, available, size):
    lines = []
    for para in s.split('\n'):
        row = ''
        for word in para.split(' '):
            if row and width(row + ' ' + word, size) > available:
                lines.append(row)
                row = word
            else:
                row += (' ' if row else '') + word
        lines.append(row)
    return lines


def node(key, title, y, body='', tech='', role='', col='c', kind='process', h=None):
    x, w = {'c': (640, 520), 'l': (90, 440), 'r': (1270, 440)}[col]
    ts, bs = (26, 23) if kind != 'portal' else (23, 21)
    tl = wrap(title, w - (110 if kind == 'decision' else 50), ts)
    bl = wrap(body, w - 52, bs) if body else []
    techlines = wrap(tech, w - 48, 20) if tech else []
    calc_h = 40 + len(tl) * 34 + len(bl) * 31 + len(techlines) * 27
    if role:
        calc_h += 28
    if bl:
        calc_h += 10
    if techlines:
        calc_h += 14
    if kind == 'decision':
        calc_h = max(170, len(tl) * 40 + 88)
    if kind in ('terminal', 'stop', 'portal'):
        calc_h = max(86, len(tl) * 32 + 35)
    n = dict(id=key, title=title, body=body, tech=tech, role=role, x=x, y=y,
             w=w, h=max(h or 0, calc_h), kind=kind, tl=tl, bl=bl, techlines=techlines)
    N[key] = n
    return key


def pos(key, side, offset=0):
    n = N[key]
    x, y, w, h = (n[t] for t in ('x', 'y', 'w', 'h'))
    return {'t': (x + w / 2 + offset, y), 'b': (x + w / 2 + offset, y + h),
            'l': (x, y + h / 2 + offset), 'r': (x + w, y + h / 2 + offset)}[side]


def edge(a, b, label='', side='b', target='t', via=None, at=None, kind='flow', ao=0, bo=0):
    start, end = pos(a, side, ao), pos(b, target, bo)
    if via is None:
        if start[0] == end[0] or start[1] == end[1]:
            via = []
        elif side in ('l', 'r') and target in ('l', 'r'):
            mx = (start[0] + end[0]) / 2
            via = [(mx, start[1]), (mx, end[1])]
        else:
            my = (start[1] + end[1]) / 2
            via = [(start[0], my), (end[0], my)]
    E.append(dict(source=a, target=b, label=label, points=[start, *via, end], at=at, kind=kind))


def portal(key, dest, label, y, col, title):
    node(key, title, y, col=col, kind='portal')
    N[key]['destination'] = dest
    P.append(dict(id=key, destination=dest, label=label))
    return key


def section(num, title, y, subtitle):
    SECTIONS.append(dict(num=num, title=title, y=y, subtitle=subtitle))


# 같은 도형은 같은 역할을 나타낸다.
section('공통', '어느 단계에서나 지키는 것', 125, '조회·실행·전달의 전 과정에 적용')
node('RULE_EXEC', '허락된 조회와 실행만', 230,
     '정책 엔진이 허용 여부를 판정하고\n하네스가 실제 실행을 통제합니다.',
     '16 에이전트 하네스\n18 Policy as Code 정책 엔진', '프로그램', 'l')
node('RULE_TENANT', '고객마다 자료를 분리', 230,
     '자료·검색 범위·지식 그래프·기억을\n고객별로 나눕니다.',
     '19 멀티테넌트 격리', '프로그램')
node('RULE_RECORD', '실행과 조건을 남기기', 230,
     '실행 기록은 AI가 고치지 못합니다.\n다음 단계에 저장한 조건을 다시 줍니다.',
     '20 Agent tracing\n21 진행 기록·변경 이력', '프로그램', 'r')
node('RULE_BUDGET', '남은 기한·비용 확인', 620,
     '남은 일까지 하면 한도를 넘을 것 같으면\n다음 유료 호출 전에 멈추고\n맡긴 사람에게 묻습니다.', role='모든 단계', col='l')
node('RULE_SAFETY', '생명·신체 위험은 즉시 대응', 620,
     '도움받을 곳의 연락처를 당사자에게 알리고\n위급할 때 답할 사람에게도 알립니다.\n기한 안에 답이 없으면 정해 둔 곳에\n위치와 위험 내용만 알립니다.', role='모든 단계', col='r')
node('REQ', '한 건의 요청', 700, kind='terminal')

section('01', '접수', 1010, '맡을 일과 책임·범위를 확인합니다')
node('INTAKE', '요청과 원칙 확인', 1120,
     '업무·대상·위험·권한·기한·비용을 정합니다.\n당사자·관계자·위급할 때 답할 사람을 확인하고\n빠진 조건은 한 번에 묻습니다.\n새 대화가 위법한 요청·자동 판단 거부 등\n원칙이 걸린 요청인지 가립니다.',
     '13 SOP·Prompt chaining · 15 업무 플레이북\n14 행동 원칙 시스템 프롬프트', '판단 모델 · 새 대화')
node('CONFLICT', '이해 충돌 조회', 1570,
     '고객 자료와 따로 둔 관계자 목록에서\n충돌 후보를 찾습니다.', '23 Conflict check', '프로그램')
node('H1', '충돌 판정과 동의', 1570,
     '운영 책임자가 맡아도 되는지 정합니다.\n필요한 동의를 기록하기 전에는\n일을 시작하지 않습니다.', '25 Human-in-the-loop 승인', '사람', 'r')
node('DECLINE', '맡지 않음 · 결정 알림', 2000, col='r', kind='stop')
edge('REQ', 'INTAKE')
edge('INTAKE', 'CONFLICT')
edge('CONFLICT', 'H1', '충돌 후보 있음', 'r', 'l', at=(1215, 1515))
edge('H1', 'DECLINE', '맡지 않음', kind='stop')

section('02', '자료 확인', 2200, '원본을 보관하고, 허용된 자료의 내용·효력·현재 상태를 확인합니다')
node('READ', '자료 읽기', 2320,
     '원본은 그대로 보관합니다.\n글과 표를 뽑아 읽습니다.', '8 문서 파싱 VLM', '판독 모델')
node('HIDDEN', '숨긴 글 제거', 2660,
     '숨긴 글·보이지 않는 특수 문자를\n전달본에서 빼고 뺀 자리를 표시합니다.', '9 숨김 텍스트 탐지', '프로그램')
node('RANGE', '시험으로 확인된 범위 대조', 3000,
     '업무·법·언어·자료 양·집단을 대조합니다.\n집단은 특성을 가리기 전 원래 자료로 정하고\n대상과 건수는 프로그램이 직접 셉니다.',
     '16 에이전트 하네스 · 26 에이전트 평가 Evals', '프로그램')
node('RANGE_Q', '시험 범위 안이며\n사람의 결정이 필요 없고\n필요한 자격자가 있는가?', 3390, kind='decision')
node('OUT', '판단 중단 · 사람에게 인계\n범위 밖·사람 결정 사유와 자료 전달', 3450, col='l', kind='stop')
node('QUAR', 'AI에게 내리는 지시 분리', 3750,
     '도구 없는 새 대화가 자료 속 지시를 뺍니다.\n평가 업무라면 정해 둔 항목만 뽑습니다.',
     '10 Quarantined LLM', '격리된 새 대화')
node('INDEX', '고객 자료 색인과 관계 정리', 4090,
     '지시를 뺀 자료만 고객 저장소에 넣습니다.\n대상·관계를 정한 이름으로 연결합니다.\n새 관계자가 나오면 충돌을 다시 조회합니다.',
     '1 온톨로지 · 2 시간축 지식 그래프\n3 하이브리드 검색 RAG · 23 Conflict check', '판단 모델 · 프로그램')
node('H5', '새 충돌 판정과 동의', 4090,
     '운영 책임자가 계속 맡을지 정합니다.\n필요한 동의가 기록되기 전에는\n일을 이어 가지 않습니다.', '25 Human-in-the-loop 승인', '사람', 'r')
node('QUIT', '일을 그만둠 · 결정 알림', 4510, col='r', kind='stop')
node('SEARCH', '원문과 연결 자료 찾기', 4590,
     '별첨·참조를 따라 원문을 찾습니다.\n관련 자료는 순위와 상관없이 남깁니다.',
     '3 하이브리드 검색 RAG · 4 GraphRAG\n5 Decision Model', '프로그램 · 판단 전용 모델')
node('SOURCE', '원문·효력·현재 값 확인', 4980,
     '법령·판례 원문과 현재 효력,\n지금 값과 서류의 진위를 조회합니다.',
     '6 로컬 법령 데이터베이스\n7 System of Record', '원본 조회', kind='data')
node('ENOUGH', '결론을 바꿀 자료를\n모두 확인했는가?', 5380, kind='decision')
node('GAP_RISK', '틀렸을 때의 피해가\n감수할 위험을\n넘을 수 있는가?', 5380, col='r', kind='decision')
node('GAP_NOTE', '부족한 자료를 밝히고 판단', 5790,
     '찾은 자료로 판단합니다.\n못 찾은 곳과 다시 볼 시점을 적습니다.', role='판단 모델', col='l')
node('H2', '자료 부족 인계', 5780,
     '찾은 자료와 못 찾은 곳을 정리해\n맡긴 사람에게 넘기고 수신을 확인합니다.\n답이 없으면 해당 결론은 보류합니다.',
     '25 Human-in-the-loop 승인', '사람', 'r')
portal('P_MORE', 'SEARCH', '기한 안에 더 찾을 곳 있음', 5390, 'l', '02 · 원문과 연결 자료 찾기')
portal('P_H2_READ', 'READ', '새 자료가 옴', 6160, 'r', '02 · 자료 읽기')
portal('P_H2_JUDGE', 'JUDGE', '결정 도착 / 답 없음은 해당 결론 보류', 6160, 'c', '03 · 결론과 처리 방향 판단')
portal('P_H5_SEARCH', 'SEARCH', '맡아도 됨', 4490, 'l', '02 · 원문과 연결 자료 찾기')
edge('CONFLICT', 'READ', '충돌 후보 없음')
edge('H1', 'READ', '맡아도 됨', 'l', 'r', via=[(1220, pos('H1','l')[1]), (1220, pos('READ','r')[1])], at=(1210, 2100))
for a,b in [('READ','HIDDEN'),('HIDDEN','RANGE'),('RANGE','RANGE_Q'),('QUAR','INDEX'),('SEARCH','SOURCE'),('SOURCE','ENOUGH')]: edge(a,b)
edge('RANGE_Q','QUAR','예')
edge('RANGE_Q','OUT','아니오', 'l','r',kind='stop')
edge('INDEX','SEARCH','새 충돌 후보 없음')
edge('INDEX','H5','새 충돌 후보 있음','r','l', at=(1215,4025))
edge('H5','QUIT','그만둠',kind='stop')
edge('H5','P_H5_SEARCH','맡아도 됨','l','t',via=[(1215,pos('H5','l')[1]),(1215,4460),(310,4460)],at=(1215,4410),kind='return')
edge('ENOUGH','P_MORE','아니오 · 더 찾을 곳 있음','l','r',kind='return',at=(580,5320))
edge('ENOUGH','GAP_RISK','아니오 · 더 찾을 곳 없음 / 기한 종료','r','l',at=(1215,5300))
edge('GAP_RISK','H2','넘을 수 있음')
edge('GAP_RISK','GAP_NOTE','넘지 않음','l','t',via=[(1215,pos('GAP_RISK','l')[1]),(1215,5720),(310,5720)],at=(610,5720))
edge('H2','P_H2_READ','새 자료가 옴')
edge('H2','P_H2_JUDGE','결정 도착 / 답 없음은 해당 결론 보류','l','r',at=(1160,6110))

section('03', '판단·검증', 6440, '근거·계산·반대 의견을 대조하고, 통과한 판단만 다음으로 보냅니다')
node('JUDGE', '결론과 처리 방향 판단', 6560,
     '조건별로 충족·불충족·미확인·해당 없음을\n판정하고 반대 근거와 대안을 비교합니다.',
     '13 SOP·Prompt chaining · 15 업무 플레이북\n27 구조화 출력 Structured Outputs', '판단 모델')
node('CALC', '검증된 코드로 계산', 6940,
     '금액·기한·합계·비율을 계산합니다.',
     '12 코드 실행·Rules as Code', '프로그램')
node('DRAFT', '결론과 결과물 초안', 7250,
     '문장마다 확인·추정·미확인을 구분합니다.',
     '27 구조화 출력 Structured Outputs', '판단 모델')
node('PCHECK', '원문·계산·누락·공개 위험 검사', 7570,
     '인용·계산·출처·누락·자동 외부 호출을 검사합니다.\n볼 권한이 없는 값과 재식별 위험을 확인합니다.\n결론을 낸 뒤 같은 쟁점의 앞선 결론과 대조하고\n앞선 오류는 운영 책임자에게 알립니다.\n평가 결과의 집단별 쏠림도 코드로 잽니다.',
     '17 출력 가드레일 · 28 PII·재식별 위험 검사\n22 Decision Traces · 12 코드 실행', '프로그램')
node('ACHECK', '새 대화에서 기준별 검토', 8080,
     '합격 기준을 항목마다 판정하고\n받는 사람 입장에서 읽습니다.\n지켜야 할 원칙이 걸린 상황인지 가립니다.',
     '11 LLM-as-a-Judge\n14 행동 원칙 시스템 프롬프트', '새 대화')
node('RISK_Q', '감수할 위험 초과 가능·\n숨긴 글·갈리는 답 중\n하나라도 있는가?', 8500, kind='decision')
node('RISK_SUM', '위험은 합쳐서 확인', 8500,
     '같은 판단을 쓴 건의 피해를 모두 합칩니다.\n합산값이 한도 안이어도 새 대화가\n위험을 넘는다고 보면 재판단합니다.', role='프로그램 · 새 대화', col='l')
node('REJUDGE', '기존 답 없이 다시 판단', 8500,
     '질문 말투와 자료 순서를 바꾸고\n판단에 쓰면 안 되는 내용은 뺍니다.\n두 판단이 다르면 원문과 계산으로 가립니다.',
     '11 LLM-as-a-Judge', '새 대화', 'r')
node('RESULT_Q', '검사 결과는?', 8910, kind='decision')
node('H3', '남은 판단을 사람에게 인계', 8910,
     '사실·갈리는 해석·남은 쟁점과\n선택별 위험을 정리해 수신을 확인합니다.\n답이 없으면 해당 결론은 보류합니다.',
     '25 Human-in-the-loop 승인', '사람', 'r')
portal('P_RESULT_GAP','ENOUGH','자료가 모자람',8870,'l','02 · 자료를 모두 확인했는가?')
portal('P_RESULT_FIX','JUDGE','틀림·누락: 같은 원인도 모두 확인',9060,'l','03 · 결론과 처리 방향 판단')
portal('P_H3_JUDGE','JUDGE','결정이 옴: 조건에 넣고 다시 판단',9320,'r','03 · 결론과 처리 방향 판단')
node('QUAL_Q','자격자만 낼 수 있는\n결과물인가?',9470,kind='decision')
node('QUALIFIED','자격자의 직접 검토·승인',9470,
     '고객이 맡긴 자격자가 직접 검토하고\n승인한 결과물을 자기 이름으로 냅니다.',
     '25 Human-in-the-loop 승인','사람','r')
portal('P_QUAL_FIX','JUDGE','고칠 곳 있음',9810,'r','03 · 결론과 처리 방향 판단')
node('DIRECTION_Q','외부 전송이나\n실행이 필요한가?',10020,kind='decision')
portal('P_REPORT_ONLY','REPORT','아니오 · 맡긴 사람에게만 냄',10070,'l','05 · 보고와 실제 처리 대조')
edge('ENOUGH','JUDGE','예','b','t',via=[(900,5680),(590,5680),(590,6500),(900,6500)],at=(590,6330))
edge('GAP_NOTE','JUDGE','부족한 곳·재검토 시점 반영','b','l',via=[(310,6390),(590,6390),(590,pos('JUDGE','l')[1])],at=(310,6330))
for a,b in [('JUDGE','CALC'),('CALC','DRAFT'),('DRAFT','PCHECK'),('PCHECK','ACHECK'),('ACHECK','RISK_Q')]:edge(a,b)
edge('RISK_Q','RESULT_Q','아니오')
edge('RISK_Q','REJUDGE','예','r','l')
edge('REJUDGE','RESULT_Q','원문·계산으로 대조','b','r',via=[(1490,8845),(1215,8845),(1215,pos('RESULT_Q','r')[1])],at=(1400,8845))
edge('RESULT_Q','H3','판단 불가 / 사람이 정할 일','r','l',at=(1215,8860))
edge('RESULT_Q','P_RESULT_GAP','자료가 모자람','l','r',kind='return',at=(580,8810))
edge('RESULT_Q','P_RESULT_FIX','틀림·누락 / 같은 원인도 확인','l','r',via=[(585,pos('RESULT_Q','l')[1]),(585,pos('P_RESULT_FIX','r')[1])],kind='return',at=(580,9210))
edge('RESULT_Q','QUAL_Q','통과')
edge('H3','P_H3_JUDGE','결정이 옴 · 조건에 넣고 재판단',kind='return',at=(1490,9270))
edge('H3','QUAL_Q','답 없음 · 해당 결론 보류','l','r',via=[(1215,pos('H3','l')[1]+45),(1215,pos('QUAL_Q','r')[1])],ao=45,at=(1215,9410))
edge('QUAL_Q','QUALIFIED','예','r','l')
edge('QUAL_Q','DIRECTION_Q','아니오')
edge('QUALIFIED','P_QUAL_FIX','고칠 곳 있음',kind='return')
edge('QUALIFIED','DIRECTION_Q','승인함','l','r',via=[(1215,pos('QUALIFIED','l')[1]+45),(1215,pos('DIRECTION_Q','r')[1])],ao=45,at=(1215,9960))
edge('DIRECTION_Q','P_REPORT_ONLY','아니오','l','r')

section('04','처리',10360,'승인 내용과 실제 대상을 맞추고, 원본 시스템에서 완료를 확인합니다')
node('PRE','실행 전 권한·한도·복구 확인',10480,
     '실행하지 않고 실제 대상과 값을 맞춰 봅니다.\n이미 한 행동까지 합친 한도와 권한,\n되돌릴 방법을 검사합니다.',
     '16 에이전트 하네스 · 18 정책 엔진','프로그램')
node('H4','권한·한도·승인 요청',10480,
     '거절된 까닭과 필요한 권한·한도를 정리해\n맡긴 사람이나 다음 책임자에게 넘깁니다.\n수신을 확인하고 답이 없으면 실행하지 않습니다.',
     '25 Human-in-the-loop 승인','사람','l')
node('IRREV_Q','되돌릴 수 없고\n미리 허락한 범위 밖인가?',10860,kind='decision')
node('APPROVE','원문과 실제 대상·값 승인',10860,
     '권한 있는 승인자가 원문을 직접 읽고\n자기 판단을 먼저 적습니다.\n미리 맞춰 본 실제 대상과 값을 승인합니다.',
     '25 Human-in-the-loop 승인','사람','r')
node('JUSTBEFORE','실행 직전 승인 내용 대조',11280,
     '승인하거나 미리 허락한 대상·값·전제를\n실제 실행 내용과 한 글자까지 대조합니다.\n다르면 다시 승인받습니다.',
     '16 에이전트 하네스','프로그램')
node('EXEC','같은 요청 번호로 실행',11650,
     '다시 보낼 때도 처음 요청 번호를 씁니다.',
     '16 에이전트 하네스','프로그램')
node('ACTUAL','원본에서 실제 처리 상태 조회',11960,
     '처리 중이면 끝날 때까지 기다립니다.\n완료가 확인돼야 다음 단계로 갑니다.',
     '7 System of Record','원본 조회',kind='data')
node('RETRY_Q','미처리가 확인되고\n같은 요청 번호로\n다시 보낼 수 있는가?',11960,col='r',kind='decision')
node('H6','처리 불명 요청 인계',12300,
     '요청과 원본에서 조회한 상태를 넘기고\n수신을 확인합니다. 다시 보내지 않고\n확인한 상태를 보고에 적습니다.',
     '25 Human-in-the-loop 승인','사람','r')
portal('P_H4_PRE','PRE','권한·한도를 받거나 승인함',10900,'l','04 · 실행 전 권한·한도·복구 확인')
portal('P_H4_REPORT','REPORT','거절 / 답 없음: 하지 않은 행동 보고',11100,'l','05 · 보고와 실제 처리 대조')
portal('P_APPROVE_H4','H4','거절 / 기한 안에 답 없음',11350,'r','04 · 권한·한도·승인 요청')
portal('P_JUST_APPROVE','APPROVE','대상·값·전제가 다름',11690,'l','04 · 원문과 실제 대상·값 승인')
portal('P_RETRY_EXEC','EXEC','예 · 같은 요청 번호로 재시도',11690,'r','04 · 같은 요청 번호로 실행')
edge('DIRECTION_Q','PRE','예')
edge('PRE','IRREV_Q','권한과 한도 안')
edge('PRE','H4','권한이나 한도 초과','l','r',at=(585,10415),kind='stop')
edge('H4','P_H4_PRE','권한·한도·승인 확보',kind='return')
edge('H4','P_H4_REPORT','거절 / 답 없음','l','l',via=[(50,pos('H4','l')[1]),(50,pos('P_H4_REPORT','l')[1])],at=(270,11050),kind='stop')
edge('IRREV_Q','JUSTBEFORE','아니오')
edge('IRREV_Q','APPROVE','예','r','l')
edge('APPROVE','JUSTBEFORE','기한 안에 승인','l','r',via=[(1215,pos('APPROVE','l')[1]),(1215,pos('JUSTBEFORE','r')[1])],at=(1215,11215))
edge('APPROVE','P_APPROVE_H4','거절 / 답 없음',kind='stop')
edge('JUSTBEFORE','EXEC','같음')
edge('JUSTBEFORE','P_JUST_APPROVE','다름 · 다시 승인','l','t',via=[(585,pos('JUSTBEFORE','l')[1]),(585,11610),(310,11610)],at=(350,11610),kind='return')
edge('EXEC','ACTUAL')
edge('ACTUAL','RETRY_Q','실패 / 응답 끊김','r','l',at=(1215,11900))
edge('RETRY_Q','P_RETRY_EXEC','예','t','b',kind='return')
edge('RETRY_Q','H6','아니오',kind='stop')

section('05','완료·보고',12760,'보고와 기록을 양쪽으로 대조한 뒤 결과를 전달합니다')
node('REPORT','보고와 실제 처리 대조',12880,
     '보고 내용을 실행 기록·원본 상태와 맞춥니다.\n기록에 남은 수정·삭제·외부 전송도\n보고에 빠짐없이 있는지 거꾸로 대조합니다.\n건수는 기록에서 뽑아 “N건 중 M건”으로 씁니다.',
     '17 출력 가드레일 · 20 Agent tracing','프로그램')
node('FIX','기록대로 보고 수정',12880,
     '어긋난 내용을 고친 뒤\n보고와 기록을 다시 대조합니다.',role='판단 모델',col='l')
node('DELIVER','결과물·보고·검토표 전달',13350,
     '맡긴 사람에게 보냅니다.',role='프로그램')
edge('ACTUAL','REPORT','처리 끝남')
edge('H6','REPORT','다시 보내지 않고 상태 보고','b','r',via=[(1490,12715),(1215,12715),(1215,pos('REPORT','r')[1])],at=(1410,12715))
edge('REPORT','FIX','보고와 기록이 어긋남','l','r',at=(585,12815),kind='return')
edge('FIX','REPORT','수정 후 다시 대조','b','l',via=[(310,13240),(585,13240),(585,pos('REPORT','l')[1]+90)],bo=90,at=(350,13240),kind='return')
edge('REPORT','DELIVER','보고와 기록이 맞음')

section('06','남기기',13640,'다시 볼 조건과 후속 작업·전달처를 이어 둡니다')
node('KEEP','판단 근거와 후속 연결 저장',13760,
     '근거·재검토 조건·사용 기한을 남깁니다.\n이어 쓴 작업·전달처·보류한 부분과 이유를\n기록하고 앞선 판단 목록·변경 감시에 올립니다.',
     '21 진행 기록·변경 이력 · 22 Decision Traces\n24 Lineage·Citator형 변경 알림','프로그램',kind='data')
node('FINISH','한 건의 업무 종료',14170,kind='terminal')
edge('DELIVER','KEEP')
edge('KEEP','FINISH')

section('상시','건과 상관없이 계속 점검',14420,'진행 중이거나 이미 끝난 건에도 적용합니다')
node('W_LAW','근거 변경 확인',14550,
     '법령·판례·기준서 변경을 날마다 받고\n연결된 결론·전달 결과·플레이북·코드를 찾습니다.',
     '6 법령 데이터베이스 · 24 변경 알림','프로그램','l')
node('W_PARTY','새 이해 충돌 확인',14550,
     '공시·지분 보고를 날마다 받아\n이미 맡은 일과 충돌이 생겼는지 봅니다.',
     '23 Conflict check','프로그램')
node('W_TEST','업무 능력과 방어 시험',14550,
     '주기적으로 공격·숨긴 글·표식 문구·승인 시험과\n판단 전용 모델의 누락률을 검사합니다.\n무작위 실제 업무도 시험 결과와 견줍니다.',
     '26 에이전트 평가 Evals','프로그램','r')
node('W_Q','무엇이 드러났는가?',14970,kind='decision')
node('W_STOP','후속 행동 중단·알림',15300,
     '틀린 결론에 기댄 행동을 멈춥니다.\n맡긴 사람과 다음 작업 담당자에게 알리고\n바뀐 근거부터 다시 찾습니다.',role='프로그램',col='l')
node('W_NARROW','맡길 수 있는 범위 축소',15300,
     '나빠진 범위를 빼거나 기준을 다시 맞춥니다.\n줄인 범위는 다음 건부터 바로 적용합니다.',
     '26 에이전트 평가 Evals', '프로그램')
node('W_NEW','기준·프로그램·시험 보완',15300,
     '실패 원인을 찾아 플레이북·기준표·계산 코드·\n프로그램·시험을 고칩니다.\n막지 못한 원인에는 새 해결책을 더합니다.',role='운영하는 쪽',col='r')
node('W_CHANGE','재시험·일부 적용·복구',15700,
     '지난 건으로 재시험하고 일부 건에 먼저 씁니다.\n의도 밖 결과가 바뀌면 이전 버전으로 되돌립니다.',
     '16 에이전트 하네스','프로그램','r')
portal('P_W_SEARCH','SEARCH','바뀐 근거부터 다시 찾음',15700,'l','02 · 원문과 연결 자료 찾기')
portal('P_W_H5','H5','이미 맡은 일과 새 충돌 후보',14970,'l','02 · 새 충돌 판정과 동의')
for a in ['W_LAW','W_PARTY','W_TEST']:
    edge(a,'W_Q',bo={'W_LAW':-80,'W_PARTY':0,'W_TEST':80}[a], via=[(pos(a,'b')[0],14910),(900+{'W_LAW':-80,'W_PARTY':0,'W_TEST':80}[a],14910)])
edge('W_Q','W_STOP','근거 변경 / 틀린 결론','b','t',via=[(820,15235),(310,15235)],ao=-80,at=(360,15235),kind='stop')
edge('W_Q','W_NARROW','시험 결과가 나빠짐')
edge('W_Q','W_NEW','기준·프로그램 보완 필요','r','t',via=[(1490,pos('W_Q','r')[1])],at=(1490,15235))
edge('W_Q','P_W_H5','새 충돌 후보','l','r',at=(585,14925),kind='return')
edge('W_STOP','P_W_SEARCH',kind='return')
edge('W_NEW','W_CHANGE','고친 것을 적용')


def reroute(a, b, points, label_at=None):
    e=next(e for e in E if e['source']==a and e['target']==b)
    e['points']=points
    e['at']=label_at


# 분기 글자는 실제 선 위에 둔다. 긴 글자는 상자 위의 여백을 쓴다.
for a,b in [('CONFLICT','H1'),('INDEX','H5'),('ENOUGH','GAP_RISK'),
            ('RESULT_Q','H3'),('PRE','H4'),('ACTUAL','RETRY_Q'),('REPORT','FIX')]:
    right=N[b]['x']>N[a]['x']
    side='r' if right else 'l'
    gutter=1215 if right else 585
    top=min(N[a]['y'],N[b]['y'])-50
    cx=N[b]['x']+N[b]['w']/2
    reroute(a,b,[pos(a,side),(gutter,pos(a,side)[1]),(gutter,top),(cx,top),pos(b,'t')],(cx,top))

N['P_H5_SEARCH'].update(x=1270,y=4700)
reroute('H5','P_H5_SEARCH',[pos('H5','l'),(1235,pos('H5','l')[1]),(1235,4660),(1490,4660),pos('P_H5_SEARCH','t')],(1490,4660))
reroute('ENOUGH','P_MORE',[pos('ENOUGH','l'),(585,pos('ENOUGH','l')[1]),(585,5320),(310,5320),pos('P_MORE','t')],(310,5320))
reroute('H2','P_H2_JUDGE',[pos('H2','l'),(1215,pos('H2','l')[1]),(1215,6110),(900,6110),pos('P_H2_JUDGE','t')],(1015,6110))
reroute('REJUDGE','RESULT_Q',[pos('REJUDGE','b'),(1490,8830),(900,8830),pos('RESULT_Q','t')],(1080,8830))
reroute('RESULT_Q','P_RESULT_GAP',[pos('RESULT_Q','l'),(585,pos('RESULT_Q','l')[1]),(585,8825),(310,8825),pos('P_RESULT_GAP','t')],(310,8825))
reroute('RESULT_Q','P_RESULT_FIX',[pos('RESULT_Q','l'),(585,pos('RESULT_Q','l')[1]),(585,9230),(310,9230),pos('P_RESULT_FIX','b')],(310,9230))
reroute('H3','QUAL_Q',[pos('H3','l',45),(1235,pos('H3','l',45)[1]),(1235,9435),(900,9435),pos('QUAL_Q','t')],(1055,9435))
reroute('H4','P_H4_REPORT',[pos('H4','l'),(50,pos('H4','l')[1]),(50,11050),(310,11050),pos('P_H4_REPORT','t')],(310,11050))
reroute('W_Q','P_W_H5',[pos('W_Q','l'),(585,pos('W_Q','l')[1]),(585,14930),(310,14930),pos('P_W_H5','t')],(310,14930))
reroute('IRREV_Q','APPROVE',[pos('IRREV_Q','r'),(1215,pos('IRREV_Q','r')[1]),(1215,10810),(1490,10810),pos('APPROVE','t')],(1490,10810))
reroute('RETRY_Q','P_RETRY_EXEC',[pos('RETRY_Q','r'),(1750,pos('RETRY_Q','r')[1]),(1750,pos('P_RETRY_EXEC','r')[1]),pos('P_RETRY_EXEC','r')],(1750,11840))
next(e for e in E if e['source']=='H1' and e['target']=='READ')['at']=(1220,2130)

# 화살촉을 마름모의 실제 윤곽에 맞춘다.
for e in E:
    for index, key in [(0,e['source']),(-1,e['target'])]:
        n=N[key]
        if n['kind']!='decision':continue
        x,y=e['points'][index]; cx=n['x']+n['w']/2;cy=n['y']+n['h']/2
        if abs(y-n['y'])<.01:y+=abs(x-cx)*n['h']/n['w']
        elif abs(y-n['y']-n['h'])<.01:y-=abs(x-cx)*n['h']/n['w']
        e['points'][index]=(x,y)


def label_box(label, x, y):
    lines=wrap(label,310,21)
    w=max(width(t,21) for t in lines)+22;h=len(lines)*28+12
    return dict(x=x-w/2,y=y-h/2,w=w,h=h,lines=lines)


def intersects(a,b):
    return min(a['x']+a['w'],b['x']+b['w'])>max(a['x'],b['x'])+1 and min(a['y']+a['h'],b['y']+b['h'])>max(a['y'],b['y'])+1


def box_hits_node(box,n):
    if not intersects(box,n):return False
    if n['kind']!='decision':return True
    cx=n['x']+n['w']/2;cy=n['y']+n['h']/2
    x=max(box['x'],min(cx,box['x']+box['w']))
    y=max(box['y'],min(cy,box['y']+box['h']))
    return abs(x-cx)/(n['w']/2)+abs(y-cy)/(n['h']/2)<1.02


def segment_hits_box(a,b,box):
    t0,t1=0.,1.
    for start,delta,low,high in [(a[0],b[0]-a[0],box['x']-3,box['x']+box['w']+3),
                                  (a[1],b[1]-a[1],box['y']-3,box['y']+box['h']+3)]:
        if abs(delta)<.0001:
            if not low<start<high:return False
        else:
            p,q=(low-start)/delta,(high-start)/delta
            t0=max(t0,min(p,q));t1=min(t1,max(p,q))
            if t0>=t1:return False
    return True


def place_labels():
    placed=[]
    for e in E:
        if not e['label']:continue
        candidates=[]
        for a,b in zip(e['points'],e['points'][1:]):
            length=((b[0]-a[0])**2+(b[1]-a[1])**2)**.5
            if length<20:continue
            for f in [.5,.3,.7,.15,.85]:
                candidates.append((a[0]+f*(b[0]-a[0]),a[1]+f*(b[1]-a[1])))
            if e['at']:
                px,py=e['at'];dx=b[0]-a[0];dy=b[1]-a[1]
                t=max(0,min(1,((px-a[0])*dx+(py-a[1])*dy)/(length*length)))
                candidates.append((a[0]+t*dx,a[1]+t*dy))
        preferred=e['at'] or candidates[0]
        candidates.sort(key=lambda p:(p[0]-preferred[0])**2+(p[1]-preferred[1])**2)
        for x,y in candidates:
            box=label_box(e['label'],x,y)
            if box['x']<10 or box['x']+box['w']>W-10:continue
            if any(box_hits_node(box,n) for n in N.values()):continue
            if any(intersects(box,p) for p in placed):continue
            if any(segment_hits_box(a,b,box) for other in E if other is not e for a,b in zip(other['points'],other['points'][1:])):continue
            e['at']=(x,y);placed.append(box);break
        else:
            raise ValueError(f'선 위에 문구를 둘 공간이 없음: {e["source"]} → {e["target"]}')


place_labels()


def bridges():
    found=[]
    for i,e in enumerate(E):
        for j,f in enumerate(E[:i]):
            if e['source']==f['source'] or e['target']==f['target']:continue
            for a,b in zip(e['points'],e['points'][1:]):
                for c,d in zip(f['points'],f['points'][1:]):
                    vertical=a[0]==b[0] and c[1]==d[1]
                    horizontal=a[1]==b[1] and c[0]==d[0]
                    if not (vertical or horizontal):continue
                    x,y=(a[0],c[1]) if vertical else (c[0],a[1])
                    if (min(a[0],b[0])+1<x<max(a[0],b[0])-1 if horizontal else min(a[1],b[1])+1<y<max(a[1],b[1])-1) and (min(c[1],d[1])+1<y<max(c[1],d[1])-1 if horizontal else min(c[0],d[0])+1<x<max(c[0],d[0])-1):
                        found.append(dict(x=x,y=y,vertical=vertical,kind=e['kind'],over=i,under=j))
    return found


def text(lines, x, y, size, lineheight, weight=500, fill=INK, cls=''):
    return '\n'.join(f'<text class="{cls}" x="{x}" y="{y+i*lineheight}" text-anchor="middle" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(t)}</text>' for i,t in enumerate(lines))


def rounded_path(points, radius=12):
    # 직각 선의 모서리만 둥글린다. 목적지와 화살촉은 실제 상자에 닿는다.
    pts=[]
    for point in points:
        if not pts or point != pts[-1]: pts.append(point)
    out=[f'M {pts[0][0]} {pts[0][1]}']
    for i in range(1,len(pts)-1):
        a,b,c=pts[i-1],pts[i],pts[i+1]
        d1=((a[0]-b[0])**2+(a[1]-b[1])**2)**.5
        d2=((c[0]-b[0])**2+(c[1]-b[1])**2)**.5
        r=min(radius,d1/2,d2/2)
        p=(b[0]+(a[0]-b[0])*r/d1,b[1]+(a[1]-b[1])*r/d1)
        q=(b[0]+(c[0]-b[0])*r/d2,b[1]+(c[1]-b[1])*r/d2)
        out.extend([f'L {p[0]} {p[1]}',f'Q {b[0]} {b[1]} {q[0]} {q[1]}'])
    out.append(f'L {pts[-1][0]} {pts[-1][1]}')
    return ' '.join(out)


def render():
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">전문 판단의 신뢰성 — 사용 구조</title>',
           '<desc id="desc">접수, 자료 확인, 판단·검증, 처리, 완료·보고, 남기기의 흐름과 상시 점검. 점선 복귀 표시는 적힌 단계와 상자로 이어집니다.</desc>',
           '<defs>']
    for name,color in [('flow',BLUE),('return',AMBER),('stop',RED)]:
        parts.append(f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9" fill="{color}"/></marker>')
    parts.extend(['</defs>','<rect width="100%" height="100%" fill="white"/>',
                  f'<g font-family="Apple SD Gothic Neo,Noto Sans CJK KR,sans-serif" fill="{INK}">'])
    parts.append(text(['전문 판단의 신뢰성 · 사용 구조'],900,60,38,46,800))
    parts.append(text(['점선 상자는 표시된 단계·상자로 이어집니다.'],900,100,22,30,500,MUTED))
    for s in SECTIONS:
        y=s['y']
        parts.append(f'<g class="section"><line x1="90" y1="{y}" x2="1710" y2="{y}" stroke="#D4DDE7" stroke-width="1.5"/>')
        parts.append(f'<text x="90" y="{y+43}" font-size="28" font-weight="800" fill="{BLUE}">{s["num"]}</text>')
        parts.append(f'<text x="190" y="{y+43}" font-size="30" font-weight="800">{esc(s["title"])}</text>')
        parts.append('</g>')
    for i,e in enumerate(E):
        color={'flow':BLUE,'return':AMBER,'stop':RED}[e['kind']]
        dash=' stroke-dasharray="9 6"' if e['kind']=='return' else ''
        parts.append(f'<path class="edge" data-id="{i}" d="{rounded_path(e["points"])}" fill="none" stroke="{color}" stroke-width="2.3"{dash} marker-end="url(#arrow-{e["kind"]})"/>')
    for b in bridges():
        x,y=b['x'],b['y'];color={'flow':BLUE,'return':AMBER,'stop':RED}[b['kind']]
        curve=f'M {x} {y-10} Q {x+15} {y} {x} {y+10}' if b['vertical'] else f'M {x-10} {y} Q {x} {y-15} {x+10} {y}'
        parts.append(f'<circle class="bridge" cx="{x}" cy="{y}" r="10" fill="white"/><path d="{curve}" fill="none" stroke="{color}" stroke-width="2.3"/>')
    parts.append(f'<path class="note-connector" d="{rounded_path([pos("RISK_SUM","r"),pos("RISK_Q","l")])}" fill="none" stroke="{BORDER}" stroke-width="1.5" stroke-dasharray="3 6"/>')
    for key,n in N.items():
        x,y,w,h=n['x'],n['y'],n['w'],n['h']; kind=n['kind'];cx=x+w/2
        parts.append(f'<g id="{key}" class="node {kind}" data-id="{key}">')
        if kind=='portal': parts.append(f'<a href="#{n["destination"]}">')
        fill={'decision':'#FFF7DE','terminal':'#E9F5EE','stop':'#FFF0ED','portal':'#FFFCF4','data':'#F3F6FA'}.get(kind,'white')
        if kind=='decision':
            parts.append(f'<polygon class="shape" points="{cx},{y} {x+w},{y+h/2} {cx},{y+h} {x},{y+h/2}" fill="{fill}" stroke="{BORDER}" stroke-width="1.7"/>')
            parts.append(text(n['tl'],cx,y+h/2-(len(n['tl'])-1)*18+9,26,36,800,cls='title'))
        else:
            rx=h/2 if kind in ('terminal','stop') else 11
            stroke=AMBER if kind=='portal' else BORDER
            dash=' stroke-dasharray="5 5"' if kind=='portal' else ''
            parts.append(f'<rect class="shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{dash}/>')
            if kind in ('terminal','stop','portal'):
                parts.append(text(n['tl'],cx,y+h/2-(len(n['tl'])-1)*16+9,23 if kind=='portal' else 26,32,800,cls='title'))
            else:
                yy=y+40
                if n['role']:
                    color={'프로그램':BLUE,'사람':'#995114','새 대화':'#A23C6B','원본 조회':'#157267','판단 모델':'#7151A8'}.get(n['role'],MUTED)
                    parts.append(f'<text class="role" x="{x+16}" y="{y+27}" font-size="19" font-weight="700" fill="{color}">{esc(n["role"])}</text>')
                    yy+=28
                parts.append(text(n['tl'],cx,yy,26,34,800,cls='title'));yy+=len(n['tl'])*34
                if n['bl']:
                    yy+=10;parts.append(text(n['bl'],cx,yy,23,31,500,MUTED,'body'));yy+=len(n['bl'])*31
                if n['techlines']:
                    yy+=4
                    parts.append(f'<line x1="{x+24}" y1="{yy-10}" x2="{x+w-24}" y2="{yy-10}" stroke="#E4EAF1"/>')
                    yy+=14;parts.append(text(n['techlines'],cx,yy,20,27,600,'#45627E','tech'))
        if kind=='portal':parts.append('</a>')
        parts.append('</g>')
    for i,e in enumerate(E):
        if not e['label']:continue
        if e['at']:
            x,y=e['at']
        else:
            p,q=max(zip(e['points'],e['points'][1:]),key=lambda pq:(pq[0][0]-pq[1][0])**2+(pq[0][1]-pq[1][1])**2)
            x,y=(p[0]+q[0])/2,(p[1]+q[1])/2
        lines=wrap(e['label'],310,21);w=max(width(t,21) for t in lines)+22;h=len(lines)*28+12
        parts.append(f'<g class="edge-label" data-id="{i}"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="5" fill="white" stroke="#DCE5EF"/>')
        parts.append(text(lines,x,y-(len(lines)-1)*14+7,21,28,600,cls='label-text'))
        parts.append('</g>')
    parts.append('</g></svg>')
    OUT.write_text('\n'.join(parts))
    data=dict(width=W,height=H,nodes=N,edges=E,portals=P,sections=SECTIONS)
    (ROOT/'docs/도식/신뢰성-사용구조.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps(dict(svg=str(OUT.relative_to(ROOT)),nodes=len(N),edges=len(E),size=[W,H]),ensure_ascii=False))


if __name__=='__main__':render()
