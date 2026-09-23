"""Apply the reader-review repairs without changing canonical material names.

The drawing keeps the existing cards/colours. Shared facilities are references;
task edges express actions, choices, waits and the scope of a retry.
"""
import math


def place_usage(N, E, G, A, make, space, port, route, layout, descriptions, support_roles, height):
    """Show distinct managed resources and event-triggered actions.

    Lifecycle availability does not mean an action runs in every workflow step.
    Usage captions name dependencies and their timing at actual use sites.
    """
    def cut(a, b=None):
        E[:] = [e for e in E if not (e['source'] == a and (b is None or e['target'] == b))]

    def link(a, b, sa='b', sb='t', via=None, kind='reference', label=''):
        cut(a, b)
        route(a, b, label, sa, sb, via, kind)

    def add_space(y, amount):
        nonlocal height
        space(y, amount)
        height += amount

    # Reuse real workflow occurrences; the five-card overview is not a step.
    removed = {'foundation_scope', 'global_control', 'global_isolation',
               'global_monitor', 'global_guard', 'global_record'}
    E[:] = [e for e in E if not ({e['source'], e['target']} & (removed | {'foundation'}))]
    for k in removed: N.pop(k, None)
    G[:] = [g for g in G if g['id'] not in {'foundation', 'support_conditions'}]
    supports = ['control', 'isolation', 'monitor', 'guard', 'record']
    first_y = min(N[k]['y'] for k in ['start', 'watch', 'live_start'])
    add_space(first_y, 45-first_y)

    # Create or reuse the job's isolated workspace before gathering its context.
    # Re-entry checks the existing boundary; it does not always create a new job.
    top = N['context_initial']['y']
    isolation = make('isolation', '분리 실행', 640, 0, 520,
                     descriptions['isolation'], condition='작업 공간 준비')
    add_space(top, isolation['h']+60)
    isolation['y'] = top
    cut('signal', 'context_initial')
    link('signal', 'isolation', kind='flow')
    link('isolation', 'context_initial', kind='flow')

    # Monitoring detects faults independently of the job's normal sequence.
    # Its event entry joins the existing recovery/resumption path, not the
    # normal controller checkpoint. This lane concerns the selected job.
    top = N['control']['y']
    event = make('monitor_event', '업무 실행 중\n장애를 감지함', 1250, 0, 430,
                 kind='terminal')
    add_space(top, event['h']+60)
    event['y'] = top
    N['monitor'].update(body=descriptions['monitor'], condition='별도 감시 · 장애 후 복구')
    cut('control', 'monitor')
    link('monitor_event', 'monitor', kind='flow')
    for source in supports:
        N[source]['support_role'] = support_roles[source]
        for field in ['applies_to', 'reference_group', 'scope', 'relation_label']:
            N[source].pop(field, None)

    # A live channel is used only in a live conversation. It is now an actual
    # connected intake step; later conversations name the same channel locally.
    live = N['live']
    live.update(x=1250, y=N['signal']['y'], w=430, h=N['signal']['h'],
                kind='process', body=descriptions['live'])
    N['live_start']['x'] = live['x']+live['w']/2-N['live_start']['w']/2
    for field in ['applies_to', 'reference_group', 'scope']:
        live.pop(field, None)
    cut('live_start', 'signal')
    link('live_start', 'live', kind='flow')
    link('live', 'signal', sa='l', sb='r', kind='flow', label='받은 새 요청')

    # The model is an input to interpretation, not a stage that becomes active
    # only once. Subsequent use sites carry visible, named dependency captions.
    model = N['model']
    model.update(x=1250, y=N['understand']['y'], w=430, h=202,
                 applies_to='understand', relation_label='사용 기능')
    for field in ['reference_group', 'scope']:
        model.pop(field, None)
    link('model', 'understand', sa='l', sb='r')

    # Search tools are adjacent to search, with a reference line. Reading supplied
    # documents remains possible without being forced through a tool invocation.
    search, tools = N['search'], N['global_tools']
    add_space(search['y'], 48)
    search.update(x=150, w=370)
    tools.update(x=580, y=search['y'], w=250, h=search['h'],
                 body=descriptions['global_tools'], applies_to='search', relation_label='필요할 때 사용')
    for field in ['reference_group', 'scope']:
        tools.pop(field, None)
    a, b = port('checks_start'), port('search', 't')
    link('checks_start', 'search', via=[(a[0], b[1]-52), (b[0], b[1]-52)],
         kind='flow', label='필요한 자료 찾기')
    a, b = port('evidence_repair', 'r'), port('search', 't')
    link('evidence_repair', 'search', sa='r', via=[(860, a[1]), (860, b[1]-34), (b[0], b[1]-34)],
         kind='return', label='보완 자료 확보')
    for target in ['now', 'case_ref', 'reference', 'reuse']:
        e = next(e for e in E if e['source'] == 'search' and e['target'] == target)
        e['points'][0] = port('search', 'l')
        e['fixed_route'] = True
    a, b = port('search'), port('absent', 't')
    link('search', 'absent', via=[(a[0], a[1]+18), (840, a[1]+18), (840, b[1]-32), (b[0], b[1]-32)],
         kind='flow', label='추가 확인 필요 없음')
    link('global_tools', 'search', sa='l', sb='r')

    def use(k, source, label, condition):
        if k == source: return
        N[k].setdefault('material_uses', []).append(dict(source=source, material=N[source]['material'],
                                                       label=label, condition=condition))

    for k in ['understand', 'intent', 'goal', 'strategy', 'counter', 'verify', 'quality', 'cause', 'improve']:
        use(k, 'model', '사용: AI 모델', '내용을 이해·판단하거나 작성할 때')
    for k in ['communicate0', 'law_wait', 'rule_wait', 'handoff', 'wait', 'delivery_approval', 'delivery', 'wait2']:
        use(k, 'live', '통화·채팅일 때: 실시간 대화', '실시간으로 말을 주고받을 때만')
    for k in ['now', 'original', 'testenv0', 'testenv', 'capability0', 'capability', 'effect_check']:
        use(k, 'global_tools', '필요 시: 업무 도구·시스템', '조회·측정·시험 도구가 필요할 때만')

    # These dependencies carry distinct times and targets. An unchanged wait is
    # not a recovery, permission check or new decision-recording event.
    for k in ['signal','context2','control']:
        use(k,'control','시작·작업 전환: 실행 제어','업무를 시작·전환·재개할 때')
    for k in ['wait','wait2','effect_wait','improve_queue']:
        use(k,'control','답변·시점 도착: 실행 제어','답변·기한·시작 조건을 받아 대기를 끝낼 때')
    for k in ['context_initial','control','testenv0','testenv']:
        use(k,'isolation','자료·공간 관리: 분리 실행','공간을 준비하거나 자료·실행 자원을 사용할 때')
    for k in ['context_initial','search','original','communicate0','law_wait','rule_wait','handoff','delivery_approval','delivery']:
        use(k,'guard','주고받기 전: 안전장치','정보를 받거나 보내기 전에 허용 여부를 확인')
    for k in ['tools','testenv0','testenv','improve_apply']:
        use(k,'guard','실행 전: 안전장치','실행·재시도·재개 전에 허용 여부를 확인')
    use('context2','guard','조건이 바뀌면: 안전장치','권한·규칙·한도·위험이 바뀌면 영향받는 작업만 재검사')
    for k in ['intent','goal','trust','priority','strategy','plan','progress','verify','process_step','quality','cause']:
        use(k,'record','판단·검사 뒤: 판단 근거 기록','판단·실행·수정·검사 내용이 새로 생겼을 때 기록')
    N['record'].pop('applies_to',None)

    # Name resources once per operation family rather than drawing a web of
    # repeated lines across every alternative in a fan-out.
    family_uses = [
        ('필요에 따라 AI 모델로 내용을 읽고, 업무 도구·시스템으로 자료를 정리합니다.', ['model', 'global_tools']),
        ('풀이·해석에는 AI 모델, 계산에는 업무 도구·시스템을 필요에 따라 씁니다.', ['model', 'global_tools']),
        ('AI 모델로 내용을 설계·작성하고, 필요하면 업무 도구·시스템으로 만듭니다.', ['model', 'global_tools']),
        ('답변·조율에는 AI 모델을 쓰고, 통화·채팅이면 실시간 대화로 주고받습니다.', ['model', 'live']),
        ('기록 변경·거래·설정·게시에는 업무 도구·시스템을 씁니다.', ['global_tools']),
        ('관찰·시험에 필요한 업무 도구·시스템을 씁니다.', ['global_tools']),
    ]
    for i, (text, sources) in enumerate(family_uses):
        g = next(g for g in G if g['id'] == 'opg'+str(i))
        add_space(g['y']+1, 100)
        g.update(usage_caption=text,
                 usage_caption_extra=['자료·공간: 분리 실행  |  실행 전: 안전장치  |  실행 뒤: 판단 근거 기록'],
                 material_uses=[dict(source=s, material=N[s]['material']) for s in sources])
        for source,condition in [('isolation','자료와 실행 공간의 경계 유지'),
                                 ('guard','실행 전에 허용 여부 확인'),
                                 ('record','실행 결과와 판단 근거가 생긴 뒤 기록')]:
            g['material_uses'].append(dict(source=source,material=N[source]['material'],condition=condition))

    # Fit the final copy as well as local-use captions. Descriptions are applied
    # after the earlier layout pass, including cards without usage footers.
    # Grow the canvas instead of reducing the text size.
    for k in sorted((k for k,n in N.items() if n.get('body') or n.get('material_uses')), key=lambda k:N[k]['y']):
        n = N[k]
        z, bs, titles, lines = layout(n)
        # Keep the material name together on narrow cards. The conservative
        # body-text wrap leaves enough room for the caption rendered at 18px.
        captions = []
        for item in n.get('material_uses', []):
            caption = item['label']
            if n['w'] < 350:
                caption = caption.replace(': ', ':\n', 1)
            probe = dict(n, title='', body=caption, material=None, w=n['w'])
            captions.extend(layout(probe)[3])
        if captions:
            n['usage_lines'] = captions
        if n['material']:
            title_rows = n.get('title_lines_reserved', len(titles))
            footer_height = 26 + len(captions)*23 if captions else 24
            required = 35 + title_rows*(z+5) + (8 if lines else 0) + len(lines)*27 + footer_height
        else:
            required = len(titles)*(z+5) + len(lines)*25 + (8 if lines else 0) + 36 + len(captions)*23
        if required > n['h']:
            old_bottom = n['y'] + n['h']
            extra = math.ceil(required-n['h'])
            add_space(old_bottom, extra)
            n['h'] += extra
            n['needed_height'] = n['h']
    # Source cards must fit their new widths, and the two searched-material cards
    # share a row. A size change is applied to the whole row, not just one card.
    row = ['search', 'global_tools', 'original']
    needed = max(35 + len(layout(N[k])[2])*(layout(N[k])[0]+5) + 8 + len(layout(N[k])[3])*27 + 24
                 + (len(N[k].get('usage_lines',[]))*23+14 if N[k].get('usage_lines') else 0) for k in row)
    old_bottom = max(N[k]['y']+N[k]['h'] for k in row)
    if needed > min(N[k]['h'] for k in row):
        add_space(old_bottom, max(0, needed-min(N[k]['h'] for k in row)))
        for k in row:N[k]['h']=N[k]['needed_height']=needed
    rows = [['signal','live'],['progress','record'],['control','monitor'],['plan','state'],
            ['strategy','risk'],['improve','testenv'],['understand','model'],
            ['ethics','principles'],['contract','platform']]
    rows += [[e['target'] for e in E if e['source']=='choose'+str(i)] for i in range(6)]
    for row in rows:
        row_h=max(N[k]['h'] for k in row)
        for k in row:N[k]['h']=N[k]['needed_height']=row_h
    # Height changes may have moved the local model away from its consumer.
    N['model']['y'] = port('understand', 'r')[1] - N['model']['h']/2
    link('model', 'understand', sa='l', sb='r')
    N['global_tools']['y'] = N['search']['y']
    link('global_tools', 'search', sa='l', sb='r')
    for main, companion in [('law_higher','law_higher_apply'), ('law_special','law_special_apply'),
        ('law_clear','law_wait'), ('rule_order','rule_apply'), ('rule_resolved','rule_wait'),
        ('counter_needed','counter'), ('verify','verify_help'), ('strategy_choice','strategy_stop'),
        ('delivery_allowed','delivery_hold'), ('passed','retry_improve')]:
        center=max(N[k]['y']+N[k]['h']/2 for k in [main,companion])
        for k in [main,companion]:N[k]['y']=center-N[k]['h']/2
    # Turn toward the controller above the independent fault entry.
    a,b = port('record'),port('control','t')
    yy = a[1]+32
    link('record','control',via=[(a[0],yy),(b[0],yy)],kind='flow',label='지금 할 일·준비한 자료')
    for source in ['model','global_tools','live',*supports]:
        N[source]['used_by'] = [k for k,n in N.items() if any(u['source']==source for u in n.get('material_uses',[]))]
        N[source]['used_in_groups'] = [g['id'] for g in G if any(u['source']==source for u in g.get('material_uses',[]))]
    return height


def apply(N, E, G, A, make, space, port, route, layout):
    def cut(a, b=None):
        E[:] = [e for e in E if not (e['source'] == a and (b is None or e['target'] == b))]

    def delete(k):
        E[:] = [e for e in E if k not in (e['source'], e['target'])]
        N.pop(k, None)

    def link(a, b, label='', sa='b', sb='t', via=None, kind='flow'):
        cut(a, b)
        route(a, b, label, sa, sb, via, kind)

    def outer(a, b, x, label='', sa='l', sb='l', kind='return'):
        start, end = port(a, sa), port(b, sb)
        link(a, b, label, sa, sb, [(x, start[1]), (x, end[1])], kind)

    def size(k):
        n = N[k]
        z, bs, titles, body = layout(n)
        if n['material']:
            n.pop('title_lines_reserved', None)
            h = 32 + len(titles) * (z + 5) + 10 + len(body) * 27 + 22
        else:
            h = len(titles) * (z + 5) + len(body) * 25 + (8 if body else 0) + 28
            if n['kind'] in ('decision', 'decisionwide'):
                h = max(h, 160 if len(titles) < 3 else 220)
        n['h'] = n['needed_height'] = max(90, math.ceil(h))

    def body(k, text, condition=None):
        N[k]['body'] = text
        if condition is not None:
            N[k]['condition'] = condition

    def add_after(before, key, title, x, w=520, body='', kind='process', condition=None, gap=64):
        y = N[before]['y'] + N[before]['h'] + gap
        n = make(key, title, x, 0, w, body, kind, condition)
        h = n['h']
        space(y, h + gap)
        n['y'] = y
        return n

    # Shared facilities apply from the first input, including research, retries,
    # external effects and follow-up changes. They are not activation steps.
    delete('model_initial')
    cut('context_initial')
    link('context_initial', 'understand')
    cut('context', 'model'); cut('model')
    link('context', 'goal_review')
    cut('live'); cut('live_start', 'live')
    N['live_start']['title'] = '실시간 대화로\n새 요청을 받음'
    N['start']['title'] = '새 요청을 받거나\n업무 조건이 바뀜'
    link('live_start', 'signal')
    body('signal', '새 요청과 조건 변경을 해당 업무에 연결합니다.\n기다리던 답변은 아래의 해당 대기 단계로 전달합니다.')
    facilities = [
        ('model', 'AI 모델', '정보를 이해하고 판단하며 내용을 만듭니다.\n아래에서 이해·판단·생성이 필요할 때마다 씁니다.'),
        ('global_control', '실행 제어', '작업 순서와 결과 합류를 관리합니다.\n답변·시간 알림은 기다리던 해당 단계로 보냅니다.'),
        ('global_tools', '업무 도구·시스템', '검색·조회·편집 등에 필요한 도구를 연결합니다.\n요청을 보내고 결과·오류·진행 상태를 받습니다.'),
        ('global_guard', '안전장치', '처음 자료를 받을 때부터 권한·규칙·한도를 확인합니다.\n조사·질문·시험·재개·개선에도 같은 기준을 적용합니다.'),
        ('global_monitor', '운영 감시·복구', '업무 내내 오류·지연·중단을 살핍니다.\n복구하면 아래의 재개 조건 확인으로 연결합니다.'),
        ('global_isolation', '분리 실행', '업무를 시작할 때부터 자료와 실행 공간을 구분합니다.\n허용된 공유만 열고 다른 작업에 영향을 주지 않게 합니다.'),
        ('global_record', '판단 근거 기록', '조사·판단·실행·검사의 입력과 결과를 계속 기록합니다.\n선택한 이유와 수정·재개한 이유도 남깁니다.'),
        ('live', '실시간 대화', '통화·채팅의 입력과 출력을 주고받습니다.\n새 요청과 기다리던 답변을 구분해 전달합니다.'),
    ]
    space(0, 800)
    for i, (k, title, text) in enumerate(facilities):
        n = make(k, title, 85 + (i % 4) * 415, 105 + (i // 4) * 270, 385, text, 'reference')
        n.update(applies_to='ALL_WORK', reference_group='foundation', scope='all_information_and_actions')
    height = max(N[k]['h'] for k, _, _ in facilities)
    for i, (k, _, _) in enumerate(facilities):
        N[k].update(y=100 + (i // 4) * (height + 32), h=height)
    foundation_bottom = max(N[k]['y'] + N[k]['h'] for k, _, _ in facilities) + 24
    G.append(dict(id='foundation', x=65, y=35, w=1670, h=foundation_bottom-35,
                  title='업무 내내 쓰는 기반 · 아래의 조사·실행·대기·후속 작업 전체에 적용', desc=''))
    make('foundation_scope', '모든 단계에 공통으로 적용', 640, foundation_bottom+45, 520,
         '현재 권한·규칙·한도 안에서 처리합니다.\n점선은 적용 관계이며, 작업 순서를 뜻하지 않습니다.', 'reference')
    N['foundation_scope'].update(applies_to='ALL_WORK', scope='all_information_and_actions')
    link('foundation', 'foundation_scope', kind='reference')
    # Named per-operation occurrences now have a concrete local purpose.
    body('tools', '이번 작업에 쓸 도구와 입력을 준비합니다.\n도구가 필요 없으면 모델로 처리합니다.', '이번 작업 준비')
    body('control', '선택한 작업의 입력·작업 공간·기록이 준비됐는지 확인합니다.\n이번 실행과 그 결과 처리를 연결합니다.', '이번 실행 준비')
    body('isolation', '이번 작업의 자료와 실행 공간을 준비합니다.\n기존 공간을 쓸 수 있으면 그대로 사용합니다.', '이번 작업 공간')
    body('record', '선택한 작업·대상·입력과 이유를 기록합니다.\n실행·수정·검사 결과도 같은 기록에 덧붙입니다.', '이번 작업 기록')

    # Optional items form an inclusive selection: every selected result is
    # required, or the explicitly labelled no-selection path is taken.
    for a, b in [('search', 'absent'), ('evidence_use', 'evidence_done')]:
        e = next(e for e in E if e['source'] == a and e['target'] == b)
        e['label'] = '추가 확인\n필요 없음'
        if a == 'evidence_use':e['label'] = '추가 확인 필요 없음'
        e['fixed_route'] = True
        e.pop('label_in_body', None)
    N['search'].update(control_role='select_required_items', selected_targets=['now', 'case_ref', 'reference', 'reuse'])
    N['absent'].update(control_role='all_selected_complete', selection_source='search')
    N['evidence_use'].update(control_role='select_required_items', selected_targets=['knowledge', 'experience', 'memory'])
    N['evidence_done'].update(control_role='all_selected_complete', selection_source='evidence_use')
    for a in A:
        if a['text'] == '모은 결과를 확인': a['text'] = '고른 항목을 모두 확인한 뒤 합류'
    body('evidence_done', '고른 지식·경험·기록을 모두 확인한 뒤 합류합니다.\n확인한 자료와 아직 모르는 점을 함께 남깁니다.')
    body('absent', '찾아본 범위와 한계를 남깁니다.\n없다고 할 근거가 있을 때만 없음으로 적습니다.')
    body('version', '이번 일이 다루는 시점에 맞는 자료와 버전을 고릅니다.\n어느 원본을 언제 확인했는지도 남깁니다.')
    body('knowledge', '이번 판단에 쓸 원리와 방법을 찾습니다.\n적용 조건과 예외도 확인합니다.', '원리·방법을 참고할 때')
    N['experience']['condition'] = '비슷한 경험을 참고할 때'
    N['memory']['condition'] = '이전 기록이 필요할 때'
    for k in ['knowledge', 'experience', 'memory']:
        next(e for e in E if e['source'] == 'evidence_use' and e['target'] == k)['label'] = N[k]['condition']
    body('evidence_repair', '추가 자료를 찾거나 요청하고 기한을 정합니다.\n확보할 때까지 해당 판단을 보류합니다.')
    next(e for e in E if e['source']=='evidence_repair' and e['target']=='search')['label']='보완 자료 확보'
    old = N['evidence_use']['y']
    space(old, 225)
    make('evidence_hold', '근거를 확보하지 못해\n해당 판단을 보류함', 590, old, 260,
         '이유와 다시 확인할 조건을 남깁니다.', 'stop')
    link('evidence_repair', 'evidence_hold', '확보 불가·기한 초과')

    # Legal hierarchy is a reference diagram, not four mandatory searches.
    hierarchy = ['law_constitution', 'law_statute', 'law_decree', 'law_ministry']
    for k in hierarchy:
        E[:] = [e for e in E if k not in (e['source'], e['target'])]
    top = N['law_constitution']['y']
    make('law_date', '대상 시점과 적용 조건 확인', 985, top, 670,
         '언제부터 적용되는지 확인합니다.\n이전 일에 예전 규칙을 적용하는 조건도 확인합니다.')
    hy = top + N['law_date']['h'] + 80
    for i, k in enumerate(hierarchy):
        N[k].update(x=990+i*170, y=hy, w=155, h=110, needed_height=110, kind='reference',
                    title=['헌법', '법률', '대통령령', '총리령·부령'][i], body='',
                    applies_to='law_higher', reference_group='law_hierarchy')
    G.append(dict(id='law_hierarchy', x=970, y=hy-55, w=720, h=190,
                  title='한국 중앙정부 법령 예 · 왼쪽이 상위', desc=''))
    for a,b in zip(hierarchy,hierarchy[1:]): link(a,b,sa='r',sb='l',kind='reference')
    for a in A:
        if a['text']=='한국 중앙정부 법령 예': a['text']=''
    cut('law', 'law_constitution')
    link('law', 'law_date')
    start,end=port('law_date','r'),port('law_higher','r')
    link('law_date','law_higher','해당 법령의 관계 확인','r','r',[(1710,start[1]),(1710,end[1])])
    link('law_hierarchy','law_higher',kind='reference')
    body('law_new', '확인한 적용 시점과 경과조치를 바탕으로\n새 법이 이번 일에 적용되는지 판단합니다.')
    N['law_new']['title']='새 법을 적용할지 판단'
    body('rule_compare', '왜 지켜야 하는지, 누가 정할 권한이 있는지,\n이번 일에 어디까지 적용되는지 비교합니다.')
    for k in ['law_reply','rule_reply']:
        body(k,'답한 사람의 결정 권한을 확인합니다.\n그 결정이 법과 규칙에 맞는지 다시 대조합니다.')

    # Check risk after the actual target/input is known, and conditions after
    # an outage before resuming an old plan.
    n=add_after('control','risk_exec','빠진 위험 확인',640,body='이번 작업의 대상·입력·도구에서 생길 위험을 확인합니다.\n바뀐 조건과 필요한 대비를 실행 전에 반영합니다.',condition='구체적인 실행 전')
    cut('control','guard');link('control','risk_exec');link('risk_exec','guard')
    N['monitor']['title']='운영 감시·복구'
    body('monitor','저장한 진행 상태와 실제 처리 상태를 확인합니다.\n중단된 동안 바뀐 조건도 함께 확인합니다.','장애 후 복구')
    n=make('resume_changed','중단된 동안\n조건이 바뀌었는가?',1285,0,360,kind='decision')
    n['y']=port('monitor','b')[1]+60
    cut('monitor','state')
    link('monitor','resume_changed')
    outer('resume_changed','state',1770,'아니오','r','r')
    # A changed condition uses the same affected-scope routing as a changed result.

    # Distinguish a completed human action from an approval to perform it.
    before=next(g['y'] for g in G if g['id']=='opg0')
    space(before,290)
    make('human_return','받은 답변은\n어떤 내용인가?',1285,before,360,kind='decision')
    body('identity0','답한 사람이 맞는지, 결정하거나 수행할 권한이 있는지 봅니다.\n답변의 대상·버전이 요청과 같은지도 확인합니다.')
    N['approval_valid']['title']='상대·권한·대상·버전이\n모두 맞는가?'
    cut('approval_valid','guard');link('approval_valid','human_return','예')
    outer('human_return','guard',1210,'실행 승인','l','r')
    start,end=port('human_return','b'),port('identity','r')
    link('human_return','identity','사람이 처리한 결과','b','r',[(start[0],start[1]+45),(1750,start[1]+45),(1750,end[1])])
    outer('human_return','context_initial',1780,'목표·범위 변경','r','r')

    # One selected operation goes straight to its family. The six panels are
    # a dispatch palette, not six sequential yes/no classifications.
    for i in range(6): delete('type'+str(i))
    top=next(g['y'] for g in G if g['id']=='opg0')
    space(top,250)
    make('dispatch','지금 선택한\n작업은?',120,top,360,kind='decision')
    link('tools','dispatch')
    labels=['자료 정리','계산·판단','설계·제작','대화·조율','외부 변경·공개','관찰·시험']
    for i,label in enumerate(labels):
        a,b=port('dispatch','l'),port('choose'+str(i),'l')
        link('dispatch','choose'+str(i),label,'l','l',[(85,a[1]),(85,b[1])])
        N['choose'+str(i)].update(selection='one_operation_per_pass',dispatches='operation_selected_at_progress')
    N['dispatch'].update(control_role='exclusive_dispatch',selection='one_operation_per_pass')
    body('progress','계획과 현재 상태를 보고 지금 할 작업 하나를 고릅니다.\n대상·입력·도구와 다음에 이어질 작업을 정합니다.')

    # External effects need checked content/parameters as well as permission.
    before=N['tools']['y']
    space(before,330)
    make('precheck','결과 검증·재검증',640,before,520,
         '외부로 보낼 내용과 변경할 대상·값을 실행 전에 확인합니다.\n중요한 결론은 반대 근거도 검토하고 승인된 버전과 대조합니다.',condition='외부 행동 전')
    make('precheck_ok','이번 실행에 쓸 내용·값이\n확인됐는가?',720,port('precheck','b')[1]+55,360,kind='decision')
    extra=port('precheck_ok','b')[1]+70-N['tools']['y']
    if extra>0:space(N['tools']['y'],extra)
    cut('allowed','tools');link('allowed','precheck','실행 가능')
    link('precheck','precheck_ok');link('precheck_ok','tools','예·해당 없음')
    outer('precheck_ok','progress',580,'아니오·입력 보완','l','l')

    # Per-stage process review precedes acceptance of that stage's result.
    before=N['state_result']['y']
    space(before,265)
    make('process_step','일하는 과정 평가',640,before,520,
         '이번 단계에서 필요한 자료·절차·승인을 지켰는지 확인합니다.\n잘못된 과정과 영향을 받은 결과를 고칠 일로 남깁니다.',condition='단계 완료 확인')
    cut('verify','state_result');link('verify','process_step');link('process_step','state_result')
    N['identity_ok']['title']='요청한 상대의 결과이며\n대상·버전도 맞는가?'

    # Verification uncertainty is not always a missing reply; a timer must
    # have an explicit outcome even when nothing arrives.
    body('wait','답변이 필요한 상대에게 요청하고 기한을 정합니다.\n도착한 결과와 기한 초과를 구분해 처리합니다.')
    make('verify_help','검사 방법·근거 보완',1250,N['verify']['y'],430,
         '확인할 근거와 검사 방법을 보완합니다.\n확보할 수 없으면 이유와 한계를 결과에 남깁니다.')
    link('verify_help','verify',sa='l',sb='r')
    before=N['more']['y']
    space(before,275)
    make('wait_reason','확인하지 못한\n이유는?',1285,before,360,kind='decision')
    cut('vdecision','wait');link('vdecision','wait_reason','아직 확인 못 함','r','t')
    # Keep waiting next to the cause decision rather than above it.
    N['wait']['y']=port('wait_reason','b')[1]+65
    extra=port('wait','b')[1]+60-N['more']['y']
    if extra>0:space(N['more']['y'],extra)
    link('wait_reason','wait','답변 미도착')
    outer('wait_reason','verify_help',1730,'근거·검사 보완','r','r')
    make('wait_expired','기한 내 확인하지 못해\n해당 작업을 보류함',1250,port('wait','b')[1]+65,430,
         '담당자에게 알리고 다시 시작할 조건을 남깁니다.','stop')
    extra=port('wait_expired','b')[1]+60-N['more']['y']
    if extra>0:space(N['more']['y'],extra)
    link('wait','wait_expired','기한 초과·확보 불가')

    # Resume only the affected scope. Ordinary next steps and local corrections
    # retain the established goal, plan and unchanged evidence/rules.
    body('context2','앞선 결과와 수정할 내용을 현재 정보에 반영합니다.\n바뀐 범위를 구분해 필요한 단계부터 이어 갑니다.')
    before=N['pack']['y']
    space(before,285)
    make('retry_scope','어디부터\n다시 확인할까?',120,before,390,kind='decision')
    cut('context2','checks_start');link('context2','retry_scope')
    outer('retry_scope','progress',60,'다음 작업·결과 수정')
    outer('retry_scope','checks_start',40,'자료·규칙 변경')
    outer('retry_scope','communicate0',20,'목표·범위 변경')
    outer('resume_changed','context2',1790,'예·변경 내용 반영','r','r',kind='flow')
    N['more']['title']='요청한 작업과 결과가\n모두 완료됐는가?'

    # Place approval on the same side as rework, so a requested modification
    # has a short explicit route back to correction rather than mere permission.
    cut('delivery_allowed','delivery_approval');cut('delivery_allowed','delivery_hold');cut('delivery_approval')
    N['delivery_approval'].update(x=120,w=390)
    N['delivery_hold'].update(x=1250,w=430)
    body('delivery_approval','필요한 승인을 요청하고 답변을 확인합니다.\n답한 사람의 권한과 대상·버전을 대조합니다.')
    link('delivery_allowed','delivery_approval','확인 필요','l','r',kind='blocked')
    link('delivery_allowed','delivery_hold','전달 불가','r','l',kind='blocked')
    before=N['delivery']['y'];space(before,285)
    make('delivery_reply','내용·범위를 바꾸라는\n요청이 있는가?',120,before,390,kind='decision')
    link('delivery_approval','delivery_reply')
    outer('delivery_reply','repair',85,'예·수정 후 재검사')
    outer('delivery_reply','delivery_guard',595,'아니오·승인 확인','r','l')

    # Register future-effect checks and then continue closing the current work.
    body('outcome','지금 확인할 수 있는 성과를 기록합니다.\n나중에 확인할 효과가 있는지도 구분합니다.')
    body('effect_wait','나중에 확인할 효과의 담당자와 날짜를 등록합니다.\n현재 업무 정리는 계속 진행합니다.','후속 확인 등록')
    cut('outcome','learnneed');cut('effect_wait','outcome')
    make('effect_needed','나중에 확인할\n효과가 있는가?',720,N['effect_wait']['y'],360,kind='decision')
    cut('outcome','effect_wait');link('outcome','effect_needed')
    link('effect_needed','effect_wait','예','r','l')
    link('effect_needed','learnneed','아니오')
    a,b=port('effect_wait','b'),port('learnneed','r')
    link('effect_wait','learnneed','등록 완료','b','r',[(a[0],b[1])])
    N['effect_wait'].update(registers='future_effect_check',does_not_block_current_completion=True)

    # Close this job after recording the improvement task. Running that task
    # is a later, separately triggered flow, still inside the same drawing.
    before=N['testenv']['y'];space(before,740)
    make('improve_queue','대기·후속 관리',640,before,520,
         '개선할 내용·담당자·시작 조건을 등록합니다.\n개선 시험을 기다리지 않고 이번 업무를 정리합니다.',condition='개선 과제 등록')
    make('job_memory','장기 기억',640,port('improve_queue','b')[1]+60,520,
         '이번 일의 사실·결정·교훈과 남은 약속을 저장합니다.\n등록한 성과 확인과 개선 과제도 함께 남깁니다.')
    old_finish=N['finish']['y']
    N['finish'].update(x=640,w=520,y=port('job_memory','b')[1]+60,title='이번 업무 처리 끝')
    body('finish','등록한 후속 일은 정해 둔 조건에 따라 별도로 이어 갑니다.')
    cut('improveneed','testenv');link('improveneed','improve_queue','예')
    link('improve_queue','job_memory');link('job_memory','finish')
    for k in ['memory_direct','memory_reuse']:
        cut(k,'finish');outer(k,'finish',1740,sa='r',sb='r',kind='flow')
    make('improve_start','등록한 개선 과제의\n시작 조건이 됨',120,N['testenv']['y']-180,390,kind='terminal')
    link('improve_start','testenv')
    a,b=port('improve_queue','l'),port('improve_start','l')
    link('improve_queue','improve_start','등록한 과제','l','l',[(85,a[1]),(85,b[1])],kind='reference')
    N['improve_start']['activation']='registered_improvement_due'
    make('improve_finish','개선 작업 처리 끝',640,old_finish,520,
         '적용 여부와 다음 확인 시점을 남깁니다.','terminal')
    for k in ['memory2','memory_unapplied']:
        cut(k,'finish')
        if k=='memory2':link(k,'improve_finish')
        else:outer(k,'improve_finish',1710,sa='r',sb='r',kind='flow')
    before=N['improve_apply']['y'];space(before,250)
    make('improve_allowed','시험한 버전을 실제로\n적용해도 되는가?',720,before,360,kind='decision')
    cut('passed','improve_apply');link('passed','improve_allowed','예')
    link('improve_allowed','improve_apply','권한·조건 충족')
    a,b=port('improve_allowed','r'),port('memory_unapplied','t')
    link('improve_allowed','memory_unapplied','확인 필요·적용 불가','r','t',[(b[0],a[1])],kind='blocked')
    body('improve_apply','현재 권한·규칙·한도를 확인한 시험 통과 버전만 적용합니다.\n적용 후 성과와 문제가 생기는지도 확인합니다.','허용된 개선 적용')
    N['improve_allowed']['checks']=['passed_test_version','current_authority','current_rules','current_limits']

    # A scheduled effects check is a real independent start, not an unfinished
    # branch of the delivery. Record its outcome and follow-up tasks locally.
    y=port('improve_finish','b')[1]+160
    make('effect_start','등록한 성과 확인\n시점이 됨',640,y,520,kind='terminal')
    make('effect_check','성과 추적',640,port('effect_start','b')[1]+60,520,
         '등록한 항목으로 실제 효과와 뒤늦게 생긴 문제를 확인합니다.\n이전 결과와 비교하고 후속 조치가 필요한지 판단합니다.')
    make('effect_record','대기·후속 관리',640,port('effect_check','b')[1]+60,520,
         '확인 결과를 기록하고 필요한 후속 일의 담당·기한을 정합니다.\n조치가 필요 없으면 후속 확인을 마칩니다.')
    make('effect_end','이번 성과 확인 끝',640,port('effect_record','b')[1]+60,520,kind='terminal')
    link('effect_start','effect_check');link('effect_check','effect_record');link('effect_record','effect_end')
    N['effect_start'].update(activation='registered_effect_check_due',registered_by='effect_wait')
    outer('effect_wait','effect_start',1760,'등록된 시점에 별도 시작','r','r',kind='reference')

    # Clean stale captions and metadata from replaced occurrences.
    A[:]=[a for a in A if a['text']]
    # Enlarge changed descriptions before routing. Insert space after the old
    # bottom so existing neighbouring stages keep their separation.
    for k in sorted(N, key=lambda k:N[k]['y']):
        n=N[k];old=n['h'];bottom=n['y']+old
        size(k)
        needed=n['h'];n['h']=max(old,needed)
        if needed>old:space(bottom,needed-old)
    # The common isolation card already covers initial and later work spaces.
    # Avoid another activation step and leave a clear return inlet to selection.
    delete('isolation')
    N['control']['completion_sources']=['record']
    body('control','선택한 작업의 입력·작업 공간·기록이 준비됐는지 확인합니다.\n이번 실행과 그 결과 처리를 연결합니다.','이번 실행 준비')

    # Reference priorities occupy the formerly empty left column, while the
    # rule-resolution flow can immediately follow legal applicability.
    rank=next(g for g in G if g['id']=='rank')
    evidence=next(g for g in G if g['id']=='evidence')
    rules=next(g for g in G if g['id']=='rules')
    rank_old_y=rank['y'];priority_old_y=N['priority']['y']
    rank_new_y=port('evidence_done','b')[1]+120
    dx=135-rank['x'];dy=rank_new_y-rank_old_y
    rank.update(x=135,y=rank_new_y)
    for n in N.values():
        if n.get('priority_rank'):n['x']+=dx;n['y']+=dy
    for a in A:
        if a['text'].startswith(('이 도식의 업무 기준 순서','같은 1순위','같은 2순위')) or a['text'] in ['1','2','3','4','5']:
            a['x']+=dx;a['y']+=dy
    shift=priority_old_y-(port('law_confirmed','b')[1]+120)
    tail={'priority','rule_conflict','rule_compare','rule_order','rule_apply','rule_exception','rule_candidate','rule_resolved','rule_wait','rule_reply','rule_confirmed'}
    for k in tail:N[k]['y']-=shift
    for e in E:
        if e['source'] in tail or e['target'] in tail:
            e['points']=[(x,y-shift if y>=priority_old_y else y) for x,y in e['points']]
            e['at']=None
    space(N['checks_join']['y'],-shift)
    evidence['h']=port('evidence_done','b')[1]+50-evidence['y']
    rules['h']=port('rule_confirmed','b')[1]+65-rules['y']
    a,b=port('rank','r'),port('priority','l')
    link('rank','priority','충돌 시 적용할 순서','r','l',[(885,a[1]),(885,b[1])],kind='reference')

    # Rebuild moved routes from actual midpoints, not old intermediate points.
    rail=N['checks_join']['y']-50
    for k,side,x in [('rule_confirmed','b',None),('evidence_done','l',105)]:
        a,b=port(k,side),port('checks_join','t')
        via=[(a[0],rail),(b[0],rail)] if x is None else [(x,a[1]),(x,rail),(b[0],rail)]
        link(k,'checks_join','',side,'t',via)
    N['identity_reject']['y']=port('identity_ok','r')[1]-N['identity_reject']['h']/2
    minimum=port('identity_ok','b')[1]+90
    if N['counter_needed']['y']<minimum:space(N['counter_needed']['y'],minimum-N['counter_needed']['y'])
    link('identity_ok','identity_reject','아니오','r','l',kind='blocked')
    link('identity_ok','counter_needed','예')
    N['context2']['y']=port('more','l')[1]-N['context2']['h']/2
    link('more','context2','아니오·다음 작업','l','r')
    N['retry_scope'].update(x=120,w=390)
    a,b=port('context2','b'),port('retry_scope','r')
    yy=N['retry_scope']['y']-75
    link('context2','retry_scope',via=[(a[0],yy),(560,yy),(560,b[1])],sb='r')
    outer('repair','context2',580,'고칠 내용 반영','r','r')
    a,b=port('retry_scope','t'),port('progress','l');yy=a[1]-38
    link('retry_scope','progress','다음 작업·수정','t','l',[(a[0],yy),(60,yy),(60,b[1])],kind='return')
    outer('retry_scope','checks_start',40,'자료·규칙 변경')
    a,b=port('retry_scope','b'),port('communicate0','l');yy=a[1]+42
    link('retry_scope','communicate0','목표·범위 변경','b','l',[(a[0],yy),(20,yy),(20,b[1])],kind='return')
    outer('precheck_ok','progress',60,'입력 보완')
    cut('resume_changed','context2')
    a,b=port('resume_changed','b'),port('context_initial','r');yy=a[1]+35
    link('resume_changed','context_initial','조건 변경','b','r',[(a[0],yy),(1780,yy),(1780,b[1])],kind='return')
    # Approval and completed results leave different sides of the selector.
    a,b=port('approval_valid','b'),port('human_return','l');yy=N['human_return']['y']-68
    link('approval_valid','human_return','예','b','l',[(a[0],yy),(1250,yy),(1250,b[1])])
    a,b=port('human_return','t'),port('guard','r');yy=a[1]-32
    link('human_return','guard','실행 승인','t','r',[(a[0],yy),(1735,yy),(1735,b[1])],kind='return')
    outer('human_return','context_initial',1780,'조건 변경','r','r')
    a,b=port('wait','b'),port('identity','r');yy=a[1]+40
    link('wait','identity','새 결과 도착','b','r',[(a[0],yy),(1750,yy),(1750,b[1])],kind='return')
    # Connect law applicability above the hierarchy's example, then use the
    # reference only as a relationship input to the conflict decision.
    a,b=port('law_date','l'),port('law_higher','l')
    link('law_date','law_higher',sa='l',sb='l',via=[(935,a[1]),(935,b[1])])
    a,b=port('delivery_approval','b'),port('delivery_reply','r');yy=N['delivery_reply']['y']-75
    link('delivery_approval','delivery_reply',via=[(a[0],yy),(560,yy),(560,b[1])],sb='r')
    a,b=port('delivery_reply','t'),port('delivery_guard','l');yy=a[1]-35
    link('delivery_reply','delivery_guard','승인','t','l',[(a[0],yy),(85,yy),(85,b[1])],kind='return')
    outer('delivery_reply','repair',85,'수정')
    a,b=port('wait_reason','b'),port('verify_help','r');yy=a[1]+33
    link('wait_reason','verify_help','검사 보완','b','r',[(a[0],yy),(1730,yy),(1730,b[1])],kind='return')
    for a in A:
        if a['text'] in ['1','2','3','4','5']:a['x']=132
        if a['text'].startswith(('같은 1순위','같은 2순위')):
            a['text']=a['text'].replace('아래에서 조정','오른쪽에서 조정')
    outer('foundation_scope','signal',600,sa='l',sb='l',kind='reference')
    N['effect_needed']['y']=port('effect_wait','l')[1]-N['effect_needed']['h']/2
    link('effect_needed','effect_wait','예','r','l')
    a,b=port('effect_wait','b'),port('learnneed','t');yy=b[1]-45
    link('effect_wait','learnneed','등록 완료',via=[(a[0],yy),(b[0],yy)])
    if N['improve_apply']['y']-port('improve_allowed','b')[1]<100:
        space(N['improve_apply']['y'],100-(N['improve_apply']['y']-port('improve_allowed','b')[1]))
    link('improve_allowed','improve_apply','허용됨')
    for n in N.values():
        if n.get('control_role') in ('current_result_with_optional_followup',): n.pop('control_role')

    # Every explicit wait also has a no-reply outcome. An unanswered request
    # must not be mistaken for an approval or force an endless retry.
    for prefix, next_key in [('law','law_confirmed'),('rule','rule_confirmed')]:
        wait, reply, end = prefix+'_wait', prefix+'_reply', prefix+'_timeout'
        y=port(reply,'b')[1]+60
        n=make(end,'확인 기한이 지나\n해당 작업을 보류함',1420,y,250,kind='stop')
        needed=port(end,'b')[1]+60-N[next_key]['y']
        if needed>0:space(N[next_key]['y'],needed)
        body(wait,'권한 있는 담당자에게 확인을 요청하고 기한을 정합니다.\n답변 전에는 관련 작업을 보류합니다.')
        a,b=port(wait,'b'),port(end,'l');yy=a[1]+35
        link(wait,end,'기한 초과','b','l',[(a[0],yy),(1380,yy),(1380,b[1])],kind='blocked')
    # Approval timeout shares the existing stop result with an explicit denial.
    y=port('identity0','b')[1]+65
    make('handoff_timeout','거절되거나 기한이 지나\n해당 작업을 보류함',1250,y,430,kind='stop')
    a,b=port('handoff','b'),port('handoff_timeout','l');yy=a[1]+40
    link('handoff','handoff_timeout','거절·기한 초과','b','l',[(a[0],yy),(1215,yy),(1215,b[1])],kind='blocked')
    a,b=port('identity0','r'),port('approval_valid','t');yy=b[1]-45
    link('identity0','approval_valid',sa='r',via=[(1700,a[1]),(1700,yy),(b[0],yy)])
    body('handoff','사람의 승인·판단·직접 수행이 필요한 일을 넘깁니다.\n준비한 자료와 요청 기한을 함께 보냅니다.')
    y=port('delivery_approval','b')[1]+60
    make('delivery_timeout','거절되거나 기한이 지나\n전달을 보류함',120,y,390,kind='stop')
    needed=port('delivery_timeout','b')[1]+90-N['delivery_reply']['y']
    if needed>0:space(N['delivery_reply']['y'],needed)
    a,b=port('delivery_allowed','l'),port('delivery_approval','t');yy=b[1]-45
    link('delivery_allowed','delivery_approval','확인 필요','l','t',[(590,a[1]),(590,yy),(b[0],yy)],kind='blocked')
    outer('delivery_approval','delivery_reply',560,'승인·수정 요청','r','r',kind='flow')
    link('delivery_approval','delivery_timeout','거절·기한 초과',kind='blocked')
    body('delivery_approval','승인을 요청하고 답변 기한을 정합니다.\n답한 사람의 권한과 대상·버전을 확인합니다.')
    y=port('wait2','b')[1]+60
    make('receipt_timeout','인수 확인을 받지 못해\n후속 확인으로 남김',1250,y,430,
         '미확인 상태와 담당자·다음 확인일을 기록합니다.','stop')
    needed=port('receipt_timeout','b')[1]+65-N['record_read']['y']
    if needed>0:space(N['record_read']['y'],needed)
    link('wait2','receipt_timeout','기한 초과',kind='blocked')
    a,b=port('receipt','b'),port('record_read','l');yy=a[1]+35
    link('receipt','record_read','인수 확인','b','l',[(a[0],yy),(1210,yy),(1210,b[1])])
    body('wait2','상대에게 인수 확인을 요청하고 기한을 정합니다.\n답이 오면 확인하고, 기한이 지나면 미확인으로 남깁니다.')
    # If no viable inspection is available, stop this stage instead of cycling
    # through a research action that has no way to produce evidence.
    link('wait_reason','wait_expired','검증 불가','l','l',[(1210,port('wait_reason','l')[1]),(1210,port('wait_expired','l')[1])],kind='blocked')
    body('verify_help','확인에 필요한 근거와 검사 방법을 보완합니다.\n보완한 내용으로 결과를 다시 검사합니다.')
    N['improve_start']['registered_by']='improve_queue'

    # Leave room for the two outcomes beneath each wait. Labels sit after
    # their branch point, so no label hides another outcome's line.
    for k in ['law_wait','rule_wait']:
        body(k,'담당자에게 기준을 확인하고\n답변 기한을 정합니다.')
        size(k)
    for a,b,label in [('handoff','identity0','답변'),('rule_wait','rule_reply','답변'),
                      ('wait_reason','wait','답변 대기'),('more','context2','다음 작업'),
                      ('retry_scope','checks_start','자료\n규칙'),('wait','identity','결과 도착')]:
        next(e for e in E if e['source']==a and e['target']==b)['label']=label
    # Local correction returns enter below the approval return without sharing
    # a segment carrying two opposite meanings.
    outer('delivery_repair','repair',60,'수정')
    a,b=port('delivery_reply','l'),port('repair','l')
    link('delivery_reply','repair','예','l','l',[(60,a[1]),(60,b[1])],kind='return')
    N['delivery_reply']['title']='내용·범위의\n수정 요청인가?'
    a,b=port('delivery_reply','t'),port('delivery_guard','l');yy=a[1]-35
    link('delivery_reply','delivery_guard','아니오·승인','t','l',[(a[0],yy),(85,yy),(85,b[1])],kind='return')
    a,b=port('receipt','r'),port('delivery_guard','r')
    yy=N['receipt']['y']-55
    link('receipt','delivery_guard','전달 실패·재시도','r','r',[(1160,a[1]),(1160,yy),(1750,yy),(1750,b[1])],kind='return')
    next(e for e in E if e['source']=='receipt' and e['target']=='wait2')['label']='대기'
    for k, extra in [('identity0',35),('rule_reply',35),('wait',50)]:
        space(N[k]['y'],extra)
    for i in range(6):N['choose'+str(i)]['h']=160
    rows=[['ethics','principles'],['contract','platform']]
    rows += [[e['target'] for e in E if e['source']=='choose'+str(i)] for i in range(6)]
    for row in rows:
        reserve=max(len(layout(N[k])[2]) for k in row)
        old_bottom=max(port(k,'b')[1] for k in row)
        heights=[]
        for k in row:
            n=N[k];n['title_lines_reserved']=reserve
            z,_,_,lines=layout(n)
            heights.append(max(n['h'],32+reserve*(z+5)+10+len(lines)*27+22))
        height=max(heights);y=N[row[0]]['y']
        if y+height>old_bottom:space(old_bottom,y+height-old_bottom)
        for k in row:N[k]['h']=height
    for main, companion in [
        ('law_higher','law_higher_apply'),('law_special','law_special_apply'),
        ('law_clear','law_wait'),('rule_order','rule_apply'),('rule_resolved','rule_wait'),
        ('counter_needed','counter'),('verify','verify_help'),
        ('strategy_choice','strategy_stop'),('delivery_allowed','delivery_hold'),
        ('passed','retry_improve')]:
        N[companion]['y']=port(main,'r')[1]-N[companion]['h']/2

    # Empty bands left by removed activation/classification nodes add no
    # meaning. Compress only bands without cards, captions or group titles.
    occupied=[(n['y'],n['y']+n['h']) for n in N.values()]
    occupied += [(a['y']-a.get('size',22),a['y']+8) for a in A]
    occupied += [(g['y'],g['y']+48) for g in G if g['title']]
    occupied += [(a[1]-24,a[1]+24) for e in E for a,b in zip(e['points'],e['points'][1:])
                 if a[1]==b[1] and a[0]!=b[0]]
    merged=[]
    for a,b in sorted(occupied):
        if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
        else:merged.append([a,b])
    gaps=[(a[1],b[0]) for a,b in zip(merged,merged[1:]) if b[0]-a[1]>110]
    def compact(y):
        return y-sum(max(0,min(y,b)-a)*(1-110/(b-a)) for a,b in gaps if y>a)
    for n in N.values():n['y']=compact(n['y'])
    for g in G:
        top,bottom=compact(g['y']),compact(g['y']+g['h'])
        g.update(y=top,h=bottom-top)
    for a in A:a['y']=compact(a['y'])
    for e in E:
        e['points']=[(x,compact(y)) for x,y in e['points']]
        if e.get('at'):e['at']=(e['at'][0],compact(e['at'][1]))
    return max(n['y']+n['h'] for n in N.values())+100


def draw_usage(N, E, G, A, make, space, port, route, layout, height):
    """Replace prose footnotes with calls in the flow and local resource links."""
    def reserve(y, amount):
        nonlocal height
        space(y, amount)
        height += amount

    def link(a, b, label='', sa='b', sb='t', via=None, kind='flow'):
        route(a, b, label, sa, sb, via, kind)
        E[-1]['fixed_route'] = True
        return E[-1]

    # Compare the laws that actually apply; a country's example hierarchy is
    # not an input to this workflow.
    example_ids = {'law_constitution', 'law_statute', 'law_decree', 'law_ministry'}
    example_top = min(N[k]['y'] for k in example_ids)
    E[:] = [e for e in E if not ({e['source'], e['target']} & (example_ids | {'law_hierarchy'}))
            and (e['source'], e['target']) != ('law_date', 'law_higher')]
    for k in example_ids:
        del N[k]
    G[:] = [g for g in G if g['id'] != 'law_hierarchy']
    make('law_rank', '적용할 법의 상하 관계 확인', 985, example_top, 670,
         '이번 일에 적용되는 법 중\n무엇이 상위법인지 확인합니다.')
    link('law_date', 'law_rank')
    link('law_rank', 'law_higher')
    original_ids = set(N)

    def small(k, source, x, y, w=240, kind='process', title=None, owner=None):
        n = make(k, title or N[source]['title'], x, y, w, kind=kind)
        # These are calls/references to an already defined material, not another
        # full definition card. The original material names and bodies stay put.
        n.update(material=None, usage_material=N[source]['material'], usage_source=source,
                 usage_step=kind != 'reference', usage_owner=owner)
        n.pop('term', None); n.pop('system', None)
        z, _, titles, _ = layout(n)
        n['h'] = n['needed_height'] = max(76, len(titles)*(z+5)+28)
        if kind == 'reference': n['applies_to'] = owner
        return n

    # Delete every usage footer. Size the original cards for their descriptions.
    for n in N.values():
        n.pop('usage_lines', None)
        if n.get('material_uses'):
            z, _, titles, lines = layout(n)
            if n['material']:
                n['h'] = 35+n.get('title_lines_reserved',len(titles))*(z+5)+8+len(lines)*27+24
            else:
                n['h'] = max(90,len(titles)*(z+5)+len(lines)*25+(8 if lines else 0)+28)
            n['needed_height'] = n['h']
    for row in [['signal','live'],['search','global_tools','original'],['understand','model'],
                ['progress','record'],['plan','state'],['control','monitor'],
                ['strategy','risk'],['improve','testenv']]:
        h=max(N[k]['h'] for k in row)
        for k in row:N[k]['h']=N[k]['needed_height']=h

    def after(owner, source, event=''):
        key='use_'+owner+'_'+source
        n=N[owner];w=min(n['w'],300);bottom=n['y']+n['h']
        c=small(key,source,n['x']+(n['w']-w)/2,0,w,owner=owner)
        gap=84 if event or owner=='identity_ok' else 48
        reserve(bottom,c['h']+gap+48);c['y']=bottom+gap
        for e in E:
            if e['source']==owner and e['kind']!='reference':
                e.setdefault('logical_source',owner);e['source']=key
                e['source_port']='b'
        link(owner,key,event)
        return key

    guard_questions = {
        'context_initial': '이 자료를\n사용해도 되는가?',
        'search': '이 자료를\n찾아봐도 되는가?',
        'original': '이 원문을\n열어 봐도 되는가?',
        'communicate0': '질문할 내용을\n상대에게 알려도\n되는가?',
        'law_wait': '문의 내용을\n알려도\n되는가?',
        'rule_wait': '문의 내용을\n알려도\n되는가?',
        'testenv0': '이 자료·도구로\n시험해도 되는가?',
        'testenv': '이 자료·도구로\n시험해도 되는가?',
    }

    def guard_before(owner):
        key='use_'+owner+'_guard';n=N[owner];top=n['y'];cx=n['x']+n['w']/2
        gate=small(key,'guard',cx-min(300,n['w']*.85)/2,0,min(300,n['w']*.85),
                   kind='decisionwide',title=guard_questions[owner],owner=owner)
        gate['h']=gate['needed_height']=150
        stopkey=key+'_hold'
        stop=make(stopkey,'허용을 확인 못해\n작업을 보류함',n['x'],0,min(250,n['w']*.8),kind='stop')
        stop.update(usage_step=True,usage_owner=owner)
        amount=gate['h']+84+stop['h']+64
        reserve(top,amount);gate['y']=top;stop['y']=top+gate['h']+84
        for e in E:
            if e['target']==owner and e['kind']!='reference':
                e.setdefault('logical_target',owner);e['target']=key
        # Put the stop to the left of the central success line, on its own row.
        stop['w']=min(250,n['w']*.72)
        z,_,titles,_=layout(stop);stop['h']=max(90,len(titles)*(z+5)+28)
        stop['x']=n['x']
        # The success route goes around the stop on the right and joins below it.
        a=port(key,'r');b=port(owner,'t');xx=n['x']+n['w']-4;yy=b[1]-28
        link(key,owner,'예','r','t',[(xx,a[1]),(xx,yy),(b[0],yy)])
        a=port(key);b=port(stopkey,'t');yy=a[1]+44
        link(key,stopkey,'아니오·알 수 없음','b','t',[(a[0],yy),(b[0],yy)],kind='blocked')
        return key

    presentations={}
    # Existing checks already control these uses. Reuse them instead of adding
    # another check between a successful check and the action it permits.
    existing={
        ('context_initial','isolation'):'isolation',
        ('control','isolation'):'isolation',
        ('handoff','guard'):'guard',('tools','guard'):'guard',
        ('delivery','guard'):'delivery_guard',('delivery_approval','guard'):'delivery_guard',
        ('context2','guard'):'guard',('improve_apply','guard'):'improve_allowed',
        ('progress','record'):'record',('understand','model'):'model',
    }
    presentations.update(existing)
    # Calls occur after decisions/inspections, and before the next original step.
    for owner in ['intent','goal','trust','priority','strategy','plan','process_step','quality','cause']:
        presentations[(owner,'record')]=after(owner,'record')
    presentations[('verify','record')]=presentations[('process_step','record')]
    for owner in ['signal','context2','wait','wait2']:
        label='답변·기한 도착' if owner in ('wait','wait2') else ''
        presentations[(owner,'control')]=after(owner,'control',label)
    # A future callback starts at its event, never in the registration path.
    presentations[('effect_wait','control')]=after('effect_start','control')
    presentations[('improve_queue','control')]=after('improve_start','control')
    for owner in ['context_initial','search','original','communicate0','law_wait','rule_wait','testenv0','testenv']:
        presentations[(owner,'guard')]=guard_before(owner)

    # One execution record is shared by the six alternative operation families.
    operation_record=after('identity_ok','record')
    # Only the accepted-result branch records an operation. Rejected reports
    # return to their sender without passing through the record call.
    for e in E:
        if e['source']==operation_record and e['target']=='identity_reject':
            e['source']='identity_ok';e['source_port']='r'
    next(e for e in E if e['source']=='identity_ok' and e['target']==operation_record)['label']='예'
    for e in E:
        if e['source']==operation_record and e['target']=='counter_needed':e['label']=''

    # References are short named boxes with a dotted connection. Try a clear
    # side position first; otherwise reserve a small band below the main card.
    def intersects(a,b,r,pad=3):
        x0,x1=r['x']-pad,r['x']+r['w']+pad;y0,y1=r['y']-pad,r['y']+r['h']+pad
        if abs(a[0]-b[0])<.01:return x0<a[0]<x1 and max(min(a[1],b[1]),y0)<min(max(a[1],b[1]),y1)
        if abs(a[1]-b[1])<.01:return y0<a[1]<y1 and max(min(a[0],b[0]),x0)<min(max(a[0],b[0]),x1)
        return True
    def crosses(a,b,c,d):
        if abs(a[1]-b[1])<.01 and abs(c[0]-d[0])<.01:
            return min(a[0],b[0])<c[0]<max(a[0],b[0]) and min(c[1],d[1])<a[1]<max(c[1],d[1])
        if abs(a[0]-b[0])<.01 and abs(c[1]-d[1])<.01:return crosses(c,d,a,b)
        return False
    def overlap(a,b,pad=8):
        return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>-pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>-pad
    def ref(owner,source,condition=''):
        key='ref_'+owner+'_'+source;n=N[owner];w=250
        title=N[source]['title']+ ('\n('+condition+')' if condition else '')
        r=small(key,source,0,-1000,w,kind='reference',title=title,owner=owner)
        candidates=[]
        for width in [250,220,200]:
            r['w']=width;z,_,titles,_=layout(r);r['h']=max(76,len(titles)*(z+5)+28)
            w=width
            for side in ['r','l']:
                for gap in [50,80,120]:
                    x=n['x']+n['w']+gap if side=='r' else n['x']-gap-w
                    box=dict(x=x,y=n['y']+(n['h']-r['h'])/2,w=w,h=r['h'])
                    if x<90 or x+w>1710:continue
                    if any(k not in (key,owner) and overlap(box,v) for k,v in N.items()):continue
                    start=(x if side=='r' else x+w,box['y']+box['h']/2);end=port(owner,side)
                    if any(k not in (key,owner) and intersects(start,end,v) for k,v in N.items()):continue
                    if any(intersects(a,b,box) for e in E for a,b in zip(e['points'],e['points'][1:])):continue
                    if any(crosses(start,end,a,b) for e in E for a,b in zip(e['points'],e['points'][1:])):continue
                    candidates.append((gap+(250-w)/2,side,box))
        if candidates:
            _,side,box=min(candidates,key=lambda a:a[0]);r.update(box)
            link(key,owner,sa='l' if side=='r' else 'r',sb=side,kind='reference')
        else:
            bottom=n['y']+n['h'];w=min(250,n['w']*.44)
            r['w']=w;z,_,titles,_=layout(r);r['h']=r['needed_height']=max(76,len(titles)*(z+5)+28)
            reserve(bottom,r['h']+140)
            side='r' if n['x']>=1200 else 'l'
            r.update(x=n['x']+n['w']-w if side=='r' else n['x'],y=bottom+90)
            a=port(key,side);b=port(owner,side);xx=n['x']+n['w']+20 if side=='r' else n['x']-20
            link(key,owner,sa=side,sb=side,via=[(xx,a[1]),(xx,b[1])],kind='reference')
        return key
    for owner in sorted(original_ids,key=lambda k:(N[k]['y'],N[k]['x'],k)):
        for use in N[owner].get('material_uses',[]):
            source=use['source'];pair=(owner,source)
            if pair not in presentations:
                cond='통화·채팅일 때' if source=='live' else '필요할 때' if source=='global_tools' else ''
                presentations[pair]=ref(owner,source,cond)
            use['visual_node']=presentations[pair]
            use.pop('label',None)

    # The operation family is an actual scope: isolation is its boundary, and
    # resource references connect to the operation area, not to the selector.
    for i in range(6):
        g=next(g for g in G if g['id']=='opg'+str(i))
        g.pop('usage_caption',None);g.pop('usage_caption_extra',None)
        g.update(title='이번 업무의 작업 공간',usage_material='분리 실행',usage_source='isolation')
        operations=[e['target'] for e in E if e['source']=='choose'+str(i)]
        members=[N[k] for k in operations]
        sources=[u['source'] for u in g['material_uses'] if u['source'] in ('model','global_tools','live')]
        ref_y=port('choose'+str(i))[1]+48
        reserve(min(n['y'] for n in members),max(0,ref_y+180-min(n['y'] for n in members)))
        scope=dict(id='resources_'+str(i),title='',x=min(n['x'] for n in members)-12,
                   y=min(n['y'] for n in members)-16,w=max(n['x']+n['w'] for n in members)-min(n['x'] for n in members)+24,
                   h=max(n['y']+n['h'] for n in members)-min(n['y'] for n in members)+32,
                   border_style='dotted',resource_scope=True)
        G.append(scope)
        for e in E:
            if e['source']=='choose'+str(i) and e['target'] in operations:
                a,b=port(e['source']),port(e['target'],'t');yy=scope['y']-28
                e.update(source_port='b',target_port='t',points=[a,(a[0],yy),(b[0],yy),b],fixed_route=True)
        for j,source in enumerate(sources):
            k='ref_opg'+str(i)+'_'+source
            side='l' if j==0 else 'r'
            x=g['x']+24 if side=='l' else g['x']+g['w']-304
            r=small(k,source,x,ref_y,280,kind='reference',owner='out'+str(i),
                    title=N[source]['title']+('\n(통화·채팅일 때)' if source=='live' else '\n(필요할 때)'))
            xx=scope['x']-24 if side=='l' else scope['x']+scope['w']+24
            a=port(k,side);b=(scope['x'] if side=='l' else scope['x']+scope['w'],scope['y']+scope['h']/2)
            edge=link(k,operations[0],sa=side,sb=side,via=[(xx,a[1]),(xx,b[1])],kind='reference')
            edge['target']=scope['id'];edge['points'][-1]=b;edge['reference_scope']=True
            for u in g['material_uses']:
                if u['source']==source:u['visual_node']=k
        for use in g['material_uses']:
            if use['source']=='isolation':use['visual_group']=g['id']
            elif use['source']=='guard':use['visual_node']='guard'
            elif use['source']=='record':use['visual_node']=operation_record
    # Return lanes stay outside the expanded calls and their failure branches.
    next(e for e in E if e['source']=='clear' and e['target']=='use_communicate0_guard')['label']='예'
    e=next(e for e in E if e['source']=='communicate0' and e['target']=='intent')
    a,b=port('communicate0','r'),port('intent','l')
    e.update(source_port='r',target_port='l',points=[a,(610,a[1]),(610,b[1]),b],fixed_route=True)
    N['state']['y']=port('use_plan_record','r')[1]-N['state']['h']/2
    e=next(e for e in E if e['source']=='use_plan_record' and e['target']=='state')
    a,b=port('use_plan_record','r'),port('state','l')
    e.update(source_port='r',target_port='l',points=[a,(1200,a[1]),(1200,b[1]),b],fixed_route=True)
    e=next(e for e in E if e['source']=='use_wait2_control' and e['target']=='receipt')
    a,b=port('use_wait2_control','r'),port('receipt','t');yy=b[1]-36
    e.update(source_port='r',target_port='t',points=[a,(1715,a[1]),(1715,yy),(b[0],yy),b],fixed_route=True)
    e=next(e for e in E if e['source']=='law_wait' and e['target']=='law_timeout')
    a,b=port('law_wait'),port('law_timeout','l');yy=N['law_reply']['y']-130
    e.update(points=[a,(a[0],yy),(1380,yy),(1380,b[1]),b],fixed_route=True)
    # Keep complete paths in the original metadata for equivalence checks.
    for main, companion in [('clear','communicate0'),('law_higher','law_higher_apply'),('law_special','law_special_apply'),
            ('law_clear','law_wait'),('rule_order','rule_apply'),('rule_resolved','rule_wait'),
            ('counter_needed','counter'),('verify','verify_help'),('strategy_choice','strategy_stop'),
            ('delivery_allowed','delivery_hold'),('passed','retry_improve')]:
        entry='use_'+companion+'_guard'
        if entry in N:companion=entry
        target_y=N[companion]['y']+N[companion]['h']/2-N[main]['h']/2
        delta=target_y-N[main]['y'];N[main]['y']=target_y
        for n in N.values():
            if n.get('usage_owner')==main and n['kind']=='reference':n['y']+=delta
    # The two required preparation branches start at the same visual level.
    row=['use_search_guard','use_original_guard'];top=min(N[k]['y'] for k in row)
    for k in row:
        delta=top-N[k]['y'];N[k]['y']=top;N[k+'_hold']['y']+=delta
        e=next(e for e in E if e['source']==k and e['target']==k+'_hold')
        a,b=port(k),port(k+'_hold','t');yy=a[1]+44
        e['points']=[a,(a[0],yy),(b[0],yy),b]
        owner=N[k]['usage_owner'];n=N[owner]
        e=next(e for e in E if e['source']==k and e['target']==owner)
        a,b=port(k,'r'),port(owner,'t');xx=n['x']+n['w']-4;yy=b[1]-28
        e['points']=[a,(xx,a[1]),(xx,yy),(b[0],yy),b];e['at']=(xx,(a[1]+yy)/2)
    # Supporting functions enclose the work where they are used. They are not
    # extra workflow steps or detached reference cards.
    model_definition = N['model']
    model_owners = [k for k,n in N.items()
                    if any(u['source']=='model' for u in n.get('material_uses',[]))]
    model_cards = {k for k,n in N.items() if k=='model' or n.get('usage_source')=='model'}
    E[:] = [e for e in E if not ({e['source'],e['target']} & model_cards)]
    for k in model_cards: del N[k]
    reserve(N['goal']['y'],80)
    reserve(N['quality']['y'],40)
    reserve(N['cause']['y'],40)

    def enclose_model(key, members, conditional=False, existing=None):
        boxes=[N[k] for k in members]
        left=min(n['x'] for n in boxes)-24
        top=min(n['y'] for n in boxes)-(84 if conditional else 64)
        right=max(n['x']+n['w'] for n in boxes)+24
        bottom=max(n['y']+n['h'] for n in boxes)+24
        scope=existing if existing is not None else dict(id=key)
        scope.update(x=left,y=top,w=right-left,h=bottom-top,
                     title='AI 모델'+(' (필요할 때)' if conditional else ''),
                     title_size=23,border_style='solid',model_scope=True,support_scope=True,
                     scope_members=members,usage_source='model',usage_material='AI 모델',
                     scope_sources=['model'],
                     conditional=conditional)
        if existing is None:G.append(scope)
        return scope

    first=enclose_model('model',['understand','intent'])
    first.update(material='AI 모델',system=model_definition['system'],term=model_definition['term'],
                 definition_body=model_definition['body'],used_by=model_definition['used_by'],
                 used_in_groups=model_definition['used_in_groups'])
    for owner in model_owners:
        key='model' if owner in ('understand','intent') else 'ai_'+owner
        if key!='model':enclose_model(key,[owner])
        use=next(u for u in N[owner]['material_uses'] if u['source']=='model')
        use.pop('visual_node',None);use['visual_group']=key
    for i in range(4):
        family=next(g for g in G if g['id']=='opg'+str(i))
        area=next(g for g in G if g['id']=='resources_'+str(i))
        members=[e['target'] for e in E if e['source']=='choose'+str(i)]
        # Leave a title band below the outside tool/channel reference boxes.
        reserve(min(N[k]['y'] for k in members),80)
        enclose_model(area['id'],members,conditional=True,existing=area)
        for e in E:
            if e['source']=='choose'+str(i) and e['target'] in members:
                a,b=port(e['source']),port(e['target'],'t');yy=min(N[k]['y'] for k in members)-24
                e['points']=[a,(a[0],yy),(b[0],yy),b]
        use=next(u for u in family['material_uses'] if u['source']=='model')
        use.pop('visual_node',None);use['visual_group']=area['id']

    # Apply the same visual grammar to communication, tools and isolation,
    # including the small support cards beside deferred/future work.
    tool_definition=N['global_tools']
    tool_definition['used_by'].append('search')
    N['search'].setdefault('material_uses',[]).append(dict(
        source='global_tools',material='업무 도구·시스템',
        condition='검색·조회 도구가 필요할 때만',visual_group='global_tools'))
    support_sources={'live','global_tools','isolation'}
    support_cards={k for k,n in N.items() if k=='global_tools' or
                   (n['kind']=='reference' and n.get('usage_source') in support_sources)}
    E[:]=[e for e in E if not ({e['source'],e['target']} & support_cards)]
    for k in support_cards:del N[k]

    labels={'model':'AI 모델 (필요할 때)',
            'global_tools':'업무 도구·시스템 (필요할 때)',
            'live':'실시간 대화 (통화·채팅일 때)',
            'isolation':'실제 업무와 분리한 시험 공간'}

    def set_scope_labels(scope,sources):
        # Keep conditions with the function they qualify; wrap a narrow header
        # instead of squeezing it into the card's explanation.
        lines=[];limit=(scope['w']-44)/23
        for source in sources:
            title=labels[source]
            if (scope['w']<800 or len(title)>limit) and ' (' in title:
                name,condition=title.split(' (',1)
                lines.extend([name,'('+condition])
            else:lines.append(title)
        scope.update(title='\n'.join(lines),title_lines=lines,title_size=23,
                     scope_sources=sources,support_scope=True,border_style='solid')
        return 84+32*(len(lines)-1)

    pending=[]
    for owner,n in N.items():
        sources=[u['source'] for u in n.get('material_uses',[])
                 if u['source'] in support_sources and
                 (u.get('visual_node') in support_cards or owner=='search' and u['source']=='global_tools')]
        if not sources:continue
        # Isolation is the unconditional boundary of a test; tools remain
        # conditional inside the same precisely bounded work area.
        sources.sort(key=lambda s:(s!='isolation',s))
        key='global_tools' if owner=='search' else 'support_'+owner
        scope=dict(id=key,x=n['x']-24,w=n['w']+48,scope_members=[owner])
        header=set_scope_labels(scope,sources)
        pending.append((owner,scope,header))

    # Reserve only the extra header room a preceding card actually needs.
    # Shifting at the preceding card's bottom preserves existing aligned rows.
    for owner,scope,header in sorted(pending,key=lambda item:N[item[0]]['y']):
        n=N[owner]
        obstacles=[v for k,v in N.items() if k!=owner]
        obstacles += [dict(x=a['x'],y=a['y']-a.get('size',22),
                           w=len(a['text'])*a.get('size',22),h=a.get('size',22)+8) for a in A]
        above=[v for v in obstacles if v['y']+v['h']<=n['y']+.01
               and min(v['x']+v['w'],scope['x']+scope['w'])>max(v['x'],scope['x'])]
        if above:
            bottom=max(v['y']+v['h'] for v in above)
            extra=header+64-(n['y']-bottom)
            if extra>0:reserve(bottom+.01,extra)
    for owner,scope,header in pending:
        n=N[owner];scope.update(y=n['y']-header,h=n['h']+header+24)
        if owner=='search':
            scope.update(material=tool_definition['material'],system=tool_definition['system'],
                         term=tool_definition['term'],definition_body=tool_definition['body'],
                         used_by=tool_definition['used_by'],used_in_groups=tool_definition['used_in_groups'])
        G.append(scope)
        for use in n['material_uses']:
            if use['source'] in scope['scope_sources']:
                use.pop('visual_node',None);use['visual_group']=scope['id']

    for i in range(6):
        family=next(g for g in G if g['id']=='opg'+str(i))
        area=next(g for g in G if g['id']=='resources_'+str(i))
        members=[e['target'] for e in E if e['source']=='choose'+str(i)]
        sources=[u['source'] for u in family['material_uses'] if u['source'] in ('model','global_tools','live')]
        left=min(N[k]['x'] for k in members)-24;right=max(N[k]['x']+N[k]['w'] for k in members)+24
        area.update(x=left,w=right-left,scope_members=members)
        header=set_scope_labels(area,sources)+20
        top=min(N[k]['y'] for k in members)-header
        area.update(y=top,h=max(N[k]['y']+N[k]['h'] for k in members)+24-top)
        for use in family['material_uses']:
            if use['source'] in sources:
                use.pop('visual_node',None);use['visual_group']=area['id']
        for e in E:
            if e['source']=='choose'+str(i) and e['target'] in members:
                a,b=port(e['source']),port(e['target'],'t');yy=min(N[k]['y'] for k in members)-24
                e['points']=[a,(a[0],yy),(b[0],yy),b]

    # Added room in a neighbouring branch must not stretch an AI header.
    for scope in G:
        if scope.get('model_scope') and not scope.get('resource_scope'):
            enclose_model(scope['id'],scope['scope_members'],existing=scope)

    # The isolated trial continues through the actual test, not just the step
    # that creates the test environment.
    scope=next(g for g in G if g['id']=='support_testenv0')
    scope['scope_members']=['testenv0','capability0']
    scope['h']=N['capability0']['y']+N['capability0']['h']+24-scope['y']
    G[:]=[g for g in G if g['id']!='support_capability0']
    for use in N['capability0']['material_uses']:
        if use['source']=='global_tools':use['visual_group']=scope['id']

    tools_scope=next(g for g in G if g['id']=='support_testenv')
    header=set_scope_labels(tools_scope,['global_tools'])
    tools_scope.update(y=N['testenv']['y']-header,h=N['testenv']['h']+header+24)
    children=[g for g in G if g['id'] in ('support_testenv','ai_improve','support_capability')]
    left=min(g['x'] for g in children)-24;top=min(g['y'] for g in children)-64
    right=max(g['x']+g['w'] for g in children)+24;bottom=max(g['y']+g['h'] for g in children)+24
    G.append(dict(id='isolated_improvement',title='실제 업무와 분리한 시험 공간',title_size=23,
                  x=left,y=top,w=right-left,h=bottom-top,border_style='solid',
                  support_scope=True,scope_sources=['isolation'],scope_members=['testenv','improve','capability']))
    for owner,key in [('capability0','support_testenv0'),('testenv','isolated_improvement'),
                      ('improve','isolated_improvement'),('capability','isolated_improvement')]:
        use=next((u for u in N[owner].get('material_uses',[]) if u['source']=='isolation'),None)
        if use is None:
            use=dict(source='isolation',material='분리 실행',condition='실제 업무와 분리한 시험 공간에서 작업하는 동안')
            N[owner].setdefault('material_uses',[]).append(use)
            N['isolation']['used_by'].append(owner)
        use.pop('visual_node',None);use['visual_group']=key

    e=next(e for e in E if e['source']=='goal_review' and e['target']=='risk')
    a,b=port('goal_review'),port('risk','t');yy=N['strategy']['y']-96
    e['points']=[a,(a[0],yy),(b[0],yy),b]
    e=next(e for e in E if e['source']=='counter' and e['target']=='verify')
    a,b=port('counter'),port('verify','t');yy=N['verify']['y']-104
    e['points']=[a,(a[0],yy),(b[0],yy),b]
    e=next(e for e in E if e['source']=='wait_reason' and e['target']=='verify_help')
    a,b=port('wait_reason'),port('verify_help','r');yy=a[1]+32
    e['points']=[a,(a[0],yy),(1730,yy),(1730,b[1]),b]
    e=next(e for e in E if e['source']=='use_wait2_control' and e['target']=='receipt')
    a,b=port('use_wait2_control','r'),port('receipt','t')
    # Cross below the communication header, above the receipt decision.
    yy=b[1]-16
    e['points']=[a,(1715,a[1]),(1715,yy),(b[0],yy),b]

    for k,n in N.items():
        if k not in original_ids:n['usage_added']=True
    # Remove vacant bands left by replaced footers and staggered insertions.
    # Preserve every card and horizontal routing/label band.
    occupied=[(n['y'],n['y']+n['h']) for n in N.values()]
    occupied += [(a['y']-a.get('size',22),a['y']+8) for a in A]
    occupied += [(g['y'],g['y']+48+32*(len(g.get('title_lines',[g['title']]))-1)) for g in G if g['title']]
    occupied += [(g['y']+g['h']-24,g['y']+g['h']) for g in G if g.get('support_scope')]
    occupied += [(a[1]-28,a[1]+28) for e in E for a,b in zip(e['points'],e['points'][1:]) if a[1]==b[1] and a[0]!=b[0]]
    merged=[]
    for a,b in sorted(occupied):
        if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
        else:merged.append([a,b])
    gaps=[(a[1],b[0]) for a,b in zip(merged,merged[1:]) if b[0]-a[1]>110]
    def compact(y):return y-sum(max(0,min(y,b)-a)*(1-110/(b-a)) for a,b in gaps if y>a)
    for n in N.values():n['y']=compact(n['y'])
    for g in G:
        top,bottom=compact(g['y']),compact(g['y']+g['h']);g.update(y=top,h=bottom-top)
    for a in A:a['y']=compact(a['y'])
    for e in E:
        e['points']=[(x,compact(y)) for x,y in e['points']]
        if e.get('at'):e['at']=(e['at'][0],compact(e['at'][1]))
    return max(n['y']+n['h'] for n in N.values())+100
