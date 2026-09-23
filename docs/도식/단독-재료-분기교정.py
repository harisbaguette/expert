"""Expose decision outcomes and recovery paths at the point of the check."""


def apply(N, E, G, A, node, space, port, height):
    groups = {g['id']: g for g in G}
    create_node = node
    def node(*args, **kwargs):
        n = create_node(*args, **kwargs)
        if kwargs.get('kind') == 'decision':
            n['h'] = n['needed_height'] = max(160, n['h'])
        return n

    def bottom(k):
        return N[k]['y'] + N[k]['h']

    def cut(a, b):
        E[:] = [e for e in E if (e['source'], e['target']) != (a, b)]

    def connect(a, b, label='', kind='flow', y=None, lane=None, side='l'):
        cut(a, b)
        sa, sb = (side, side) if kind == 'return' else ('b', 't')
        start, end = port(a, sa), port(b, sb)
        if kind == 'return':
            points = [start, (lane, start[1]), (lane, end[1]), end]
        elif lane is not None:
            points = [start, (start[0], start[1]+60), (lane, start[1]+60),
                      (lane, end[1]-70), (end[0], end[1]-70), end]
        elif abs(start[0]-end[0]) < .01:
            points = [start, end]
        else:
            y = y if y is not None else start[1]+60
            points = [start, (start[0], y), (end[0], y), end]
        e = dict(source=a, target=b, label=label, kind=kind, points=points,
                 at=None, source_port=sa, target_port=sb, fixed_route=True)
        E.append(e)
        return e

    def reserve(cut_y, needed_y):
        if needed_y > cut_y:
            space(cut_y, needed_y-cut_y)

    # Both risk outcomes carry usable input to strategy comparison. Failure to
    # find a risk does not establish that every condition is safe.
    N['risk'].update(x=640, w=520)
    connect('goal_review', 'risk', '아니오')
    y = bottom('risk')+100
    reserve(groups['ai_strategy']['y'], y+650)
    node('risk_result', '위험을 발견했는가?', 640, y, w=520, kind='decision')
    y = bottom('risk_result')+140
    node('risk_response', '위험 줄일 방법 정리', 240, y, w=520,
         body='생길 피해와 가능성을 살피고,\n피하거나 줄일 방법과 남는 위험을 적습니다.')
    node('risk_scope', '확인한 범위·모르는 점 정리', 1040, y, w=520,
         body='어떤 자료와 조건을 살폈는지 적습니다.\n확인하지 못한 부분은 모르는 점으로 남깁니다.')
    row_h = max(N[k]['h'] for k in ('risk_response', 'risk_scope'))
    for k in ('risk_response', 'risk_scope'):
        N[k]['h'] = row_h
    cut('risk', 'strategy')
    connect('risk', 'risk_result')
    connect('risk_result', 'risk_response', '발견함')
    connect('risk_result', 'risk_scope', '발견하지 못함')
    for k in ('risk_response', 'risk_scope'):
        connect(k, 'strategy', y=N['strategy']['y']-110)

    # Information sufficiency and the existence of an allowed, feasible method
    # are different decisions; an unknown risk is not automatically a refusal.
    n=N['strategy_choice']
    node('strategy_choice', '방법을 고르는 데 필요한\n정보가 충분한가?', 620, n['y'], w=560, kind='decision')
    y=bottom('strategy_choice')
    reserve(N['qualified']['y'], y+1000)
    N['strategy_more'].update(x=180, w=440, y=y+140)
    node('strategy_feasible', '규칙·허용 한도 안에서\n목표를 이룰 방법이 있는가?', 590, y+410, w=620, kind='decision')
    N['strategy_stop'].update(y=bottom('strategy_feasible')+140)
    for target in ('qualified', 'strategy_more', 'strategy_stop'):
        cut('strategy_choice', target)
    connect('strategy_choice', 'strategy_more', '아니오')
    connect('strategy_choice', 'strategy_feasible', '예')
    connect('strategy_more', 'checks_start', '빠진 정보\n확인', kind='return', lane=52)
    connect('strategy_feasible', 'strategy_stop', '아니오', kind='blocked')
    connect('strategy_feasible', 'qualified', '예')

    # Category dispatch and the already selected operation are distinct levels.
    N['dispatch']['title']='선택한 작업은\n어떤 종류인가?'
    families = [
        ('자료 정리', '선택한 자료 정리\n작업은?', ['골라 분류', '모아 정리', '형식 변환']),
        ('계산·판단', '선택한 계산·판단\n작업은?', ['값 계산', '특징·관계 분석', '기준 충족 판정', '앞일 예상', '최선의 방법 선택']),
        ('설계·제작', '선택한 설계·제작\n작업은?', ['구성·방법 설계', '내용 재구성', '제작·수정']),
        ('소통·조율', '선택한 소통·조율\n작업은?', ['정보·의견 교환', '조건·의견 조율']),
        ('외부 변경·공개', '선택한 외부 변경·공개\n작업은?', ['기록 변경', '신청·거래', '설정·작동', '게시·배포']),
        ('관찰·시험', '선택한 관찰·시험\n작업은?', ['관찰·측정', '실제 조건 시험', '가상 조건 시험']),
    ]
    for i, (family, question, labels) in enumerate(families):
        choose=f'choose{i}';g=groups[f'opg{i}']
        g.update(title=f'{family} · 작업 공간', operation_family=family)
        g.pop('title_lines', None)
        N[choose]['title']=question
        dispatch_edge=next(e for e in E if e['source']=='dispatch' and e['target']==choose)
        dispatch_edge['label']=family
        targets=sorted([e['target'] for e in E if e['source']==choose], key=lambda k:N[k]['x'])
        row=N[targets[0]]['y']
        space(row, 110)
        for target,label in zip(targets,labels):
            e=connect(choose,target,label,y=N[target]['y']-120)
            e['at']=(port(target,'t')[0],N[target]['y']-60)

    # Rejection is sent to the original assignee, or used to look up the result
    # of an existing tool operation. It must not silently repeat a transaction.
    y=bottom('identity_reject')+120
    reserve(N['counter_needed']['y'],y+560)
    node('identity_wait', '재요청 결과 대기', 1050, y, w=430,
         body='담당자의 답변이나 도구의 조회 결과를\n정한 기한까지 기다립니다.')
    node('identity_timeout', '결과를 받지 못해\n해당 작업을 보류함', 1050, bottom('identity_wait')+160,
         w=430, body='요청 내용과 미해결 항목을 남깁니다.', kind='stop')
    cut('identity_reject','identity')
    connect('identity_reject','identity_wait')
    connect('identity_wait','identity','결과 도착',kind='return',lane=1732,side='r')
    connect('identity_wait','identity_timeout','확보 불가·기한 초과',kind='blocked')

    # A counter-check can contradict the conclusion, find no contradiction,
    # or remain inconclusive. Each outcome has a distinct next action.
    N['counter'].update(x=665)
    groups['ai_counter']['x']=641
    N['counter_needed'].update(title='중요한 판단이거나\n근거·결과에 의문이나 변경이 있는가?', x=575,w=650,h=200)
    # Keep the first side branch below the taller question and its AI header.
    space(groups['ai_counter']['y'], 70)
    connect('counter_needed','counter','예')
    y=bottom('counter')+120
    reserve(groups['ai_verify']['y'],y+1020)
    node('counter_result','반대 근거 확인 결과는?',620,y,w=560,kind='decision')
    row=bottom('counter_result')+150
    node('counter_compare','엇갈린 근거 비교',120,row,w=470,
         body='근거의 출처와 적용 조건을 비교합니다.\n고칠 결론과 아직 판단할 수 없는 부분을\n구분해 결과 검사에 넘깁니다.')
    node('counter_more','비교 근거 보완·대기',1090,row,w=500,
         body='필요한 자료를 찾거나 담당자에게 요청하고\n받을 기한을 정합니다.\n자료를 받기 전에는 결론을 확정하지 않습니다.')
    node('counter_timeout','비교 근거를 확보하지 못해\n판단을 보류함',1090,bottom('counter_more')+160,w=500,
         body='부족한 근거와 다시 확인할 조건을 남깁니다.',kind='stop')
    cut('counter','verify')
    connect('counter','counter_result')
    connect('counter_result','counter_compare','엇갈림 발견')
    connect('counter_result','counter_more','비교 근거 부족')
    connect('counter_result','verify','엇갈림 못 찾음')
    connect('counter_compare','verify','비교 결과',y=N['verify']['y']-105)
    # The skip branch stays in the main column and joins only at verification.
    connect('counter_needed','verify','아니오',lane=80)
    connect('counter_more','counter','근거 확보',kind='return',lane=1710,side='r')
    connect('counter_more','counter_timeout','확보 불가·기한 초과',kind='blocked')

    # Audit the procedure before any step can be called complete. In particular,
    # a correct-looking output does not erase missing authorization.
    y=bottom('use_process_step_record')+120
    reserve(N['state_result']['y'],y+1040)
    node('process_check','절차·승인 확인 결과는?',620,y,w=560,kind='decision')
    row=bottom('process_check')+150
    node('process_repair','위반 영향 확인·시정 요청',140,row,w=470,
         body='영향받는 후속 작업을 멈추고 담당자에게 알립니다.\n빠진 확인과 필요한 수정·취소·복구를 정리합니다.')
    node('process_unknown','확인할 기록·답변 정리',1180,row,w=470,
         body='어떤 절차나 승인을 확인하지 못했는지 적고,\n확인할 기록과 답을 받을 담당자를 정합니다.')
    node('process_fixable','허용된 보완·복구 방법이\n확인됐는가?',110,bottom('process_repair')+130,w=530,kind='decision')
    node('process_hold','시정 방법이 확인되지 않아\n해당 작업을 보류함',120,bottom('process_fixable')+150,w=510,
         body='담당자에게 위반 내용과 중단 범위를 남깁니다.',kind='stop')
    cut('use_process_step_record','state_result')
    connect('use_process_step_record','process_check')
    connect('process_check','state_result','지킴')
    connect('process_check','process_repair','누락·위반',kind='blocked')
    connect('process_check','process_unknown','확인 못 함')
    connect('process_repair','process_fixable')
    connect('process_fixable','process_hold','아니오·확인 못 함',kind='blocked')
    # These longer forward paths use separate gutters and merge at their actual
    # destination. Existing sources keep the same terminal entry segment.
    for target,source,label,lane in [('context2','process_fixable','예 · 시정 작업으로 연결',670),
                                     ('wait_reason','process_unknown','확인 항목',1205)]:
        incoming=[e for e in E if e['target']==target and e['kind'] in ('flow','blocked')]
        join_y=N[target]['y']-55
        for e in incoming:
            # Reserve one shared final top-entry segment; preserve the old path.
            pts=e['points'];ex=port(target,'t')[0]
            if len(pts)>2:
                pts[-2]=(ex,join_y)
                if len(pts)>3:pts[-3]=(pts[-3][0],join_y)
        e=connect(source,target,label,lane=lane)
        e['points'][-3]=(lane,join_y);e['points'][-2]=(port(target,'t')[0],join_y)

    # A pending check needs a concrete recovery method and a bounded wait.
    N['vdecision']['title']='요청 조건을 검사한 결과는?'
    for e in E:
        if e['source']=='vdecision':
            e['label']={'more':'모든 조건 충족 확인','context2':'틀림·누락 확인됨',
                        'wait_reason':'맞는지 확인 못 함'}[e['target']]
    N['wait_reason'].update(title='무엇이 더 필요한가?')
    for e in E:
        if e['source']=='wait_reason':
            e['label']={'wait':'담당자의 답변·자료','verify_help':'검사\n보완',
                        'wait_expired':'확인 수단 없음'}[e['target']]
    y=bottom('use_wait_control')+130
    reserve(N['wait_expired']['y']-10,y+380)
    node('verification_event','기다린 결과는?',1270,y,w=390,kind='decision')
    for target in ('identity','wait_expired'):cut('use_wait_control',target)
    connect('use_wait_control','verification_event')
    connect('verification_event','identity','응답\n도착',kind='return',lane=1732,side='r')
    connect('verification_event','wait_expired','거절·기한 초과',kind='blocked')
    connect('wait_reason','wait_expired','확인 수단 없음',kind='blocked',lane=1708)
    N['wait_expired']['title']='확인할 수 없어\n해당 작업을 보류함'
    N['more'].update(title='요청한 작업이 모두 끝나고\n완료 조건도 확인됐는가?',x=620,w=560,h=230)
    next(e for e in E if e['source']=='more' and e['target']=='context2')['label']='아니오 · 남은 작업'
    # More than one area can have changed. Revisit the earliest affected stage,
    # so a task edit cannot bypass changed evidence or a changed request.
    N['retry_scope'].update(title='변경의 영향을 받는\n가장 앞 단계는?', h=220)
    for e in E:
        if e['source']=='retry_scope':
            e['label']={'progress':'작업만\n수정','checks_start':'자료·규칙\n변경',
                        'use_communicate0_guard':'목표·범위 변경'}[e['target']]

    # Delivery risk is checked before quality, with separate remediation and
    # unresolved/forbidden outcomes instead of always continuing.
    y=bottom('risk_delivery')+110
    reserve(groups['ai_quality']['y'],y+830)
    node('delivery_risk_result','전달·사용 위험 확인 결과는?',590,y,w=620,kind='decision')
    row=bottom('delivery_risk_result')+150
    node('delivery_risk_fix','전달 전 보완할 내용 정리',80,row,w=430,
         body='피해를 줄일 수정과 빠진 사용 조건을 적습니다.\n고친 뒤에는 결과와 전달 위험을 다시 검사합니다.')
    node('delivery_risk_hold','위험을 해소·확인할 때까지\n전달을 보류함',1200,row,w=480,
         body='해결하지 못한 위험과 확인할 담당자를 남깁니다.',kind='stop')
    cut('risk_delivery','quality')
    connect('risk_delivery','delivery_risk_result')
    connect('delivery_risk_result','quality','확인한 범위에서 허용 가능')
    connect('delivery_risk_result','delivery_risk_fix','수정·대비 필요',kind='blocked')
    connect('delivery_risk_result','delivery_risk_hold','허용 불가·판단 못 함',kind='blocked')
    connect('delivery_risk_fix','context2','',kind='return',lane=538,side='r')

    # Approval and content revision return on opposite sides of the consultation
    # branch. Approval/retry share a short lane beside the actual delivery gate.
    approval_scope=next(g for g in G if g.get('scope_members')==['delivery_approval'])
    dx=100-N['delivery_approval']['x']
    N['delivery_approval']['x']+=dx;approval_scope['x']+=dx
    N['delivery_reply'].update(x=140,w=390)
    connect('delivery_approval','delivery_reply','승인·수정 요청')
    connect('delivery_reply','repair','수정',kind='return',lane=42)
    def approval_return(source,label):
        cut(source,'delivery_guard')
        a,b=port(source,'r' if source in ('delivery_reply','delivery_retry') else 'l'),port('delivery_guard','l')
        E.append(dict(source=source,target='delivery_guard',label=label,kind='return',
            source_port='r' if source in ('delivery_reply','delivery_retry') else 'l',target_port='l',fixed_route=True,
            points=[a,(600,a[1]),(600,b[1]),b],at=((a[0]+600)/2,a[1])))
    approval_return('delivery_reply','승인')
    cut('receipt','delivery_guard')

    # Distinguish missing receipt, rejection, content changes and transport
    # failure. A transport retry has a limit and does not silently send forever.
    y=bottom('receipt')+150
    reserve(N['delivery_repair']['y'],y+760)
    node('delivery_retry','재전달 방법이 확인되고\n재시도 한도 안인가?',100,y,w=410,kind='decision')
    node('delivery_retry_hold','재전달할 수 없어\n전달을 보류함',120,bottom('delivery_retry')+130,w=470,
         body='실패 원인과 마지막 전달 상태를 남깁니다.',kind='stop')
    node('receipt_refused','인수를 거절해\n담당자에게 처리 방향 확인',1180,y,w=510,
         body='거절 이유와 미해결 항목을 기록합니다.\n새 합의 전에는 인수 완료로 처리하지 않습니다.',kind='stop')
    connect('receipt','delivery_retry','전송·열기 실패')
    connect('receipt','receipt_refused','인수 거절',kind='blocked')
    connect('delivery_retry','delivery_retry_hold','아니오·알 수 없음',kind='blocked')
    approval_return('delivery_retry','예')
    for e in E:
        if e['source']=='receipt' and e['target'] in ('wait2','delivery_repair','record_read'):
            e['label']={'wait2':'수령·인수 답변 없음','delivery_repair':'내용 수정 요청',
                        'record_read':'인수·사용 가능 확인'}[e['target']]
    y=bottom('use_wait2_control')+120
    reserve(N['receipt_timeout']['y'],y+370)
    node('receipt_event','기다린 결과는?',1220,y,w=490,kind='decision')
    for target in ('receipt','receipt_timeout'):cut('use_wait2_control',target)
    connect('use_wait2_control','receipt_event')
    connect('receipt_event','receipt','답변·수령 확인 도착',kind='return',lane=1746,side='r')
    connect('receipt_event','receipt_timeout','기한 초과',kind='blocked')
    N['receipt_timeout']['title']='인수 미확인으로 보류\n후속 확인 담당자·기한 기록'
    # Main-path post-delivery review is vertical, while unresolved receipt
    # remains on a side branch and cannot fall into the completion flow.
    connect('receipt','record_read','인수·사용 가능 확인')
    connect('record_read','process_eval','앞에서 남긴 기록')
    connect('process_eval','outcome','일한 과정과 실제 효과 비교')

    # Register a real follow-up, including who owns it and when it starts.
    # Unknown effect timing is not equivalent to "no follow-up needed".
    N['effect_needed'].update(title='남은 효과 확인은?',x=620,w=560,h=170)
    y=bottom('effect_needed')+140
    reserve(N['effect_wait']['y'],y+400)
    node('effect_define','효과 확인 방법·시점 정하기',120,y,w=480,
         body='언제 무엇을 측정해야 효과를 알 수 있는지\n업무 책임자와 정합니다.')
    connect('effect_needed','effect_define','방법·시점 미정')
    connect('effect_define','effect_wait','정한 확인 조건')
    for e in E:
        if e['source']=='effect_needed' and e['target'] in ('effect_wait','learnneed'):
            e['label']={'effect_wait':'방법·시점 정해짐','learnneed':'추가 확인 불필요'}[e['target']]
    y=bottom('effect_wait')+130
    reserve(N['learnneed']['y'],y+600)
    node('effect_registered','항목·담당자·확인 날짜가\n등록됐는가?',1175,y,w=580,kind='decision')
    node('effect_registration_hold','후속 확인 등록을 마칠 때까지\n업무 마감을 보류함',1190,bottom('effect_registered')+150,w=520,
         body='미정 항목을 업무 책임자에게 알리고\n등록할 담당자와 기한을 남깁니다.',kind='stop')
    cut('effect_wait','learnneed')
    connect('effect_wait','effect_registered')
    connect('effect_registered','learnneed','예 · 등록 완료')
    connect('effect_registered','effect_registration_hold','아니오',kind='blocked')
    event=next(e for e in E if e['source']=='effect_wait' and e['target']=='effect_start')
    event['source']='effect_registered';event['label']='등록 완료 · 확인 날짜 도착'
    event['points'][0]=port('effect_registered',event['source_port'])
    event['registration_condition']='registered'
    N['effect_start']['registered_by']='effect_registered'

    # The same missing outcomes occurred outside the cited screenshots:
    # clarification without a reply, failed restoration, and a late-effect
    # check that could close while measurements were still unavailable.
    node('clarification_hold','답변을 받지 못해\n요청 확정을 보류함',1200,N['communicate0']['y'],w=480,
         body='업무 책임자에게 미확정 내용과\n다시 확인할 기한을 남깁니다.',kind='stop')
    # Place the terminal below its source without lengthening the main path.
    N['clarification_hold']['y']=bottom('communicate0')+140
    hold_y=N['clarification_hold']['y']
    reserve(N['case']['y'],bottom('clarification_hold')+130)
    N['clarification_hold']['y']=hold_y
    connect('communicate0','clarification_hold','거절·기한 초과',kind='blocked')
    for e in E:
        if e['source']=='communicate0' and e['target']=='intent':e['label']='답변 도착 · 뜻·범위 반영'
    y=bottom('monitor')+140
    reserve(N['resume_changed']['y'],y+530)
    node('recovery_ok','복구되고 처리 상태도\n확인됐는가?',1175,y,w=580,kind='decision')
    node('recovery_hold','복구·처리 상태를 확인할 때까지\n중단한 작업을 보류함',120,bottom('recovery_ok')+160,w=520,
         body='장애 담당자에게 상태와 미확정 처리를 넘깁니다.\n처리 여부를 모르는 작업은 반복 실행하지 않습니다.',kind='stop')
    cut('monitor','resume_changed');connect('monitor','recovery_ok')
    connect('recovery_ok','resume_changed','예')
    connect('recovery_ok','recovery_hold','아니오·알 수 없음',kind='blocked')
    for key in ('precheck_ok','qualified_test'):
        for e in E:
            if e['source']==key and e['target'] in ('progress','unqualified'):
                e['label']='미충족·확인 못 함'
    y=bottom('effect_check')+130
    reserve(N['effect_record']['y'],y+1050)
    node('effect_measured','효과를 판단할 자료가\n충분히 모였는가?',620,y,w=560,kind='decision')
    node('effect_remeasure','측정 보완·다음 확인 등록',120,bottom('effect_measured')+150,w=480,
         body='빠진 자료와 다음 측정 방법·날짜를 정합니다.\n담당자가 다시 확인하도록 등록합니다.')
    node('effect_measure_hold','효과를 확인할 수 없어\n미확인 상태로 남김',120,bottom('effect_remeasure')+160,w=480,
         body='확인할 수 없는 이유와 영향받는 판단을\n업무 책임자에게 알립니다.',kind='stop')
    node('effect_action','추가 조치가 필요한가?',620,bottom('effect_measured')+530,w=560,kind='decision')
    node('effect_issue','문제·추가 조치 인계',1200,N['effect_action']['y']+280,w=480,
         body='발견한 문제와 필요한 조치를 담당자에게 넘기고\n완료 기준과 확인 기한을 등록합니다.')
    cut('effect_check','effect_record');connect('effect_check','effect_measured')
    connect('effect_measured','effect_action','예')
    connect('effect_measured','effect_remeasure','아니오')
    connect('effect_remeasure','effect_check','등록 시점 도착',kind='return',lane=70)
    connect('effect_remeasure','effect_measure_hold','측정 불가·기한 초과',kind='blocked')
    connect('effect_action','effect_issue','예')
    reserve(N['effect_record']['y'],bottom('effect_issue')+150)
    connect('effect_action','effect_record','아니오')
    connect('effect_issue','effect_record','후속 조치 등록')

    # Whole-job retrospective has consequences as well; an accepted delivery
    # is not permission to close a newly discovered process violation.
    y=bottom('process_eval')+120
    reserve(N['outcome']['y'],y+640)
    node('retrospective_result','인수 후 바로잡을 문제가\n확인됐는가?',600,y,w=600,kind='decision')
    row=bottom('retrospective_result')+140
    node('retrospective_repair','인수 후 시정할 내용 정리',120,row,w=390,
         body='영향받는 결과와 필요한 정정·회수·복구를\n담당자에게 알리고 시정 작업으로 연결합니다.')
    node('retrospective_hold','과정 평가가 끝나지 않아\n업무 마감을 보류함',1200,row,w=480,
         body='확인할 기록과 담당자·기한을 남깁니다.',kind='stop')
    cut('process_eval','outcome');connect('process_eval','retrospective_result')
    connect('retrospective_result','outcome','아니오 · 확인 완료')
    connect('retrospective_result','retrospective_repair','예',kind='blocked')
    connect('retrospective_result','retrospective_hold','확인 못 함',kind='blocked')
    connect('retrospective_repair','context2','',kind='return',lane=538,side='r')

    # Applying an improvement may itself fail after a successful trial.
    y=bottom('improve_apply')+130
    reserve(N['memory2']['y'],y+1140)
    node('improvement_applied','적용 상태와 필수 점검이\n정상인가?',600,y,w=600,kind='decision')
    node('improvement_restore','변경 중단·복구',120,bottom('improvement_applied')+150,w=480,
         body='문제가 있는 수정본의 사용을 멈춥니다.\n승인된 복구 방법으로 이전 상태를 복원합니다.')
    node('improvement_restored','이전 상태로 복구됐는가?',90,bottom('improvement_restore')+130,w=540,kind='decision')
    node('improvement_restore_hold','복구를 확인할 때까지\n영향받는 업무를 중단함',1180,bottom('improvement_restored')+130,w=520,
         body='장애 담당자에게 적용·복구 상태와\n영향받는 업무를 넘깁니다.',kind='stop')
    cut('improve_apply','memory2');connect('improve_apply','improvement_applied')
    connect('improvement_applied','memory2','예')
    connect('improvement_applied','improvement_restore','아니오·확인 못 함',kind='blocked')
    connect('improvement_restore','improvement_restored')
    connect('improvement_restored','memory_unapplied','예')
    connect('improvement_restored','improvement_restore_hold','아니오·확인 못 함',kind='blocked')

    # A prompt but repeatedly wrong reply must not reset its own retry budget.
    # Check the existing deadline and count before every re-request, including
    # after a new reply has failed the identity/target/version check again.
    y=N['identity_reject']['y']
    space(y,330)
    node('identity_retry_allowed','처음 정한 재요청\n기한·횟수 안인가?',1015,y,w=500,kind='decision')
    cut('identity_ok','identity_reject')
    connect('identity_ok','identity_retry_allowed','아니오',kind='blocked')
    connect('identity_retry_allowed','identity_reject','예')
    connect('identity_retry_allowed','identity_timeout','한도 초과·미정',kind='blocked',lane=1640)
    timeout=N['identity_timeout']
    node('identity_timeout','재요청을 끝내고\n해당 작업을 보류함',timeout['x'],timeout['y'],w=timeout['w'],
         body='확보 불가·기한 초과·횟수 초과 이유와\n미해결 항목을 업무 책임자에게 남깁니다.',kind='stop')

    # "Cannot establish quality" differs from finding a concrete defect.
    # Neither case is allowed to reach the delivery permission check directly.
    N['qualityok'].update(title='목적에 맞고 바로 쓸 수\n있다고 확인됐는가?',x=620,w=560)
    node('quality_unknown','품질을 확인할 때까지\n전달을 보류함',1250,bottom('qualityok')+140,w=430,
         body='확인할 항목과 담당자·기한을 남깁니다.',kind='stop')
    connect('qualityok','quality_unknown','확인 못 함',kind='blocked')
    for e in E:
        if e['source']=='qualityok' and e['target'] in ('repair','delivery_guard'):
            e['label']={'repair':'고칠 부분 확인','delivery_guard':'예 · 확인 완료'}[e['target']]

    for e in E:
        if e['kind']=='return' and e['target']=='context2':e['label']=''
    # Remove vacant bands created by local branch reservations; preserve every
    # card, header, junction and horizontal routing band at its full height.
    occupied=[(n['y'],n['y']+n['h']) for n in N.values()]
    occupied += [(a['y']-a.get('size',22),a['y']+8) for a in A]
    occupied += [(g['y'],g['y']+52+32*(len(g.get('title_lines',[g['title']]))-1)) for g in G if g['title']]
    occupied += [(g['y']+g['h']-24,g['y']+g['h']) for g in G if g.get('support_scope')]
    occupied += [(a[1]-34,a[1]+34) for e in E for a,b in zip(e['points'],e['points'][1:]) if a[1]==b[1] and a[0]!=b[0]]
    merged=[]
    for a,b in sorted(occupied):
        if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
        else:merged.append([a,b])
    gaps=[(a[1],b[0]) for a,b in zip(merged,merged[1:]) if b[0]-a[1]>150]
    def compact(y):return y-sum(max(0,min(y,b)-a)*(1-150/(b-a)) for a,b in gaps if y>a)
    for n in N.values():n['y']=compact(n['y'])
    for g in G:
        top,bottom_y=compact(g['y']),compact(g['y']+g['h']);g.update(y=top,h=bottom_y-top)
    for a in A:a['y']=compact(a['y'])
    for e in E:
        e['points']=[(x,compact(y)) for x,y in e['points']]
        if e.get('at'):e['at']=(e['at'][0],compact(e['at'][1]))
    return max(n['y']+n['h'] for n in N.values())+100
