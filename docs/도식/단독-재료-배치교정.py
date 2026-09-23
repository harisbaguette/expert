"""Keep workflow content intact while separating entries, returns and headers."""
import heapq
import math


def apply(N, E, G, A, space, port, layout, height, measure):
    before = {k: tuple(n[q] for q in ('x', 'y', 'w', 'h')) for k, n in N.items()}
    for key in ('record', 'record_read', 'process_eval'):
        N[key].update(x=640, w=520)
    scope_padding = {}
    for g in G:
        if not g.get('support_scope'):
            continue
        members = [N[k] for k in g['scope_members']]
        scope_padding[g['id']] = (min(n['x'] for n in members)-g['x'],
            min(n['y'] for n in members)-g['y'],
            g['x']+g['w']-max(n['x']+n['w'] for n in members),
            g['y']+g['h']-max(n['y']+n['h'] for n in members))

    # Finish the three entry paths above the common start signal. Joining the
    # start must read downward too, rather than climbing past preparation steps.
    early_y=N['watchtype']['y']+N['watchtype']['h']+100
    change_y=early_y+N['early']['h']+100
    signal_y=max(change_y+N['change']['h'],N['live']['y']+N['live']['h'])+110
    dy=signal_y-N['signal']['y']
    space(N['signal']['y']+.01,dy);height+=dy
    N['early']['y']=early_y;N['change']['y']=change_y;N['signal']['y']=signal_y
    # After improving the checking method, re-enter the earlier verification.
    next(e for e in E if e['source']=='verify_help' and e['target']=='verify')['kind']='return'

    # These side columns have room; the five-card calculation row does not.
    for k in ('law_higher_apply', 'law_special_apply', 'rule_apply',
              'law_wait', 'law_reply', 'law_timeout',
              'rule_wait', 'rule_reply', 'rule_timeout'):
        N[k].update(x=1320, w=350)
    for prefix in ('law', 'rule'):
        N[f'use_{prefix}_wait_guard'].update(x=1345, w=300)
        N[f'use_{prefix}_wait_guard']['title']='문의 내용을 알려도 되는가?'
        N[f'use_{prefix}_wait_guard_hold'].update(x=1345, w=300)
    for k in ('delivery_approval', 'counter'):
        N[k]['w'] = 470

    def refresh_scopes():
        for g in G:
            if g['id'] not in scope_padding:
                continue
            left, top, right, bottom = scope_padding[g['id']]
            members = [N[k] for k in g['scope_members']]
            x=min(n['x'] for n in members)-left
            y=min(n['y'] for n in members)-top
            g.update(x=x, y=y, w=max(n['x']+n['w'] for n in members)+right-x,
                     h=max(n['y']+n['h'] for n in members)+bottom-y)

    # A branch starts at a decision and then travels down into its action.
    # Reserve real space for the entire card and its attached function header.
    staged = [('clear','use_communicate0_guard'), ('law_higher','law_higher_apply'),
              ('law_special','law_special_apply'), ('rule_order','rule_apply'),
              ('allowed','handoff'), ('counter_needed','counter'),
              ('delivery_allowed','delivery_approval'), ('receipt','wait2'),
              ('effect_needed','effect_wait')]
    # Side-by-side successors also need a lower row once their entry is on top.
    for e in E:
        if e['kind'] in ('return','reference') or e['source']=='verify_help':continue
        source,target=e['source'],e['target'];a,b=N[source],N[target]
        if abs(a['y']-b['y'])<400 and b['y']<a['y']+a['h'] and (source,target) not in staged:
            staged.append((source,target))
    staged.sort(key=lambda pair:N[pair[0]]['y'])
    for source, target in staged:
        n=N[target];s=N[source]
        header=max((scope_padding[g['id']][1] for g in G
                    if g.get('scope_members')==[target]), default=0)
        dy=max(0, s['y']+s['h']+header+90-n['y'])
        if dy:
            cut=max(s['y']+s['h'], n['y']+n['h'])+.01
            space(cut, dy)
            n['y']+=dy
            height+=dy
        refresh_scopes()

    # A label needs its own section between the shared fork and the next card
    # or function header. Keep that room instead of drawing it on another edge.
    for e in E:
        if not e['label'] or e['kind'] in ('reference','return'):continue
        source,target=e['source'],e['target'];n=N[target];s=N[source]
        if n['y']<s['y']+s['h']:continue
        if abs((n['x']+n['w']/2)-(s['x']+s['w']/2))>100:continue
        header=max((scope_padding[g['id']][1] for g in G
                    if g.get('scope_members')==[target]), default=0)
        gap=n['y']-header-s['y']-s['h']
        if 0<=gap<145:
            dy=145-gap;space(s['y']+s['h']+.01,dy);height+=dy
            refresh_scopes()

    # Neighbouring cards must have separate bottom exits and top entries.
    exits={e['source'] for e in E if e['kind'] in ('flow','blocked')}
    for key in sorted(exits,key=lambda k:N[k]['y']+N[k]['h']):
        n=N[key];bottom=n['y']+n['h']
        below=[m for k,m in N.items() if k!=key and m['y']>=bottom-.01
               and min(n['x']+n['w'],m['x']+m['w'])>max(n['x'],m['x'])]
        if not below:continue
        gap=min(m['y'] for m in below)-bottom
        if 0<gap<100:
            space(bottom+.01,100-gap);height+=100-gap;refresh_scopes()

    # A stopping branch belongs beside the continuing column. Keeping it on
    # that column made every successful permission check take a rectangular
    # detour around its own terminal.
    for key,x in {
        'use_context_initial_guard_hold':480,
        'use_search_guard_hold':580,
        'use_original_guard_hold':985,
        'use_law_wait_guard_hold':1160,
        'use_rule_wait_guard_hold':1160,
        'use_testenv0_guard_hold':620,
        'use_testenv_guard_hold':620,
    }.items():
        N[key]['x']=x
    for key in ('use_communicate0_guard','communicate0'):
        N[key]['x']+=150
    N['evidence_usable']['x']=N['evidence_use']['x']+N['evidence_use']['w']/2-N['evidence_usable']['w']/2
    N['delivery_approval']['x']=200
    N['delivery_reply']['x']=240
    N['delivery_reply']['y']-=24
    N['delivery_timeout'].update(x=70,w=300)
    N['retry_scope'].update(x=220,w=300)
    N['identity_reject']['x']=1050
    refresh_scopes()

    changed={k for k,n in N.items()
             if tuple(n[q] for q in ('x','y','w','h')) != before[k]}
    headers=[]
    for g in G:
        if g.get('support_scope') or g['id'].startswith('opg'):
            headers.append(dict(x=g['x'], y=g['y'], w=g['w'],
                                h=49+32*(len(g.get('title_lines',[g['title']]))-1), axis='horizontal'))
            for j,line in enumerate(g.get('title_lines',[g['title']])):
                size=20 if line.startswith('(') else 22
                width=measure(line,size)
                headers.append(dict(x=g['x']+22,y=g['y']+37+j*32-size,w=width,h=size+5))

    for g in G:
        if not g['title'] or g.get('support_scope') or g['id'].startswith('opg'):continue
        for j,line in enumerate(g.get('title_lines',[g['title']])):
            size=g.get('title_size',27)
            headers.append(dict(x=g['x']+22,y=g['y']+37+j*32-size,w=measure(line,size),h=size+5))
    for a in A:
        width=measure(a['text'],a['size'])
        headers.append(dict(x=a['x']-(width/2 if a['anchor']=='middle' else 0),y=a['y']-a['size'],w=width,h=a['size']+5))

    def set_ports(source,target,sa,sb):
        e=next(e for e in E if e['source']==source and e['target']==target)
        e.update(source_port=sa,target_port=sb,reroute=True)

    # All execution outcomes leave below and enter above; only returns use sides.
    for e in E:
        if e['kind']=='reference':continue
        if e['kind']!='return':
            if (e['source_port'],e['target_port'])!=('b','t'):
                e.update(source_port='b',target_port='t',reroute=True)
        else:
            s,t=N[e['source']],N[e['target']]
            side='l' if s['x']+s['w']/2<900 else 'r'
            sa=e['source_port'] if e['source_port'] in ('l','r') else side
            sb=e['target_port'] if e['target_port'] in ('l','r') else side
            if (sa,sb)!=(e['source_port'],e['target_port']):
                e.update(source_port=sa,target_port=sb,reroute=True)
    for source,target in [('law_reply','law'),('rule_reply','priority'),
                          ('approval_valid','handoff'),('identity_reject','identity'),
                          ('wait_reason','verify_help')]:
        set_ports(source,target,'l','l')
    set_ports('retry_scope','use_communicate0_guard','l','l')
    set_ports('delivery_reply','repair','l','l')
    set_ports('receipt','delivery_guard','l','l')
    set_ports('resume_changed','state','l','l')
    set_ports('evidence_repair','use_search_guard','r','r')
    set_ports('rule_reply','priority','r','r')
    set_ports('wait_reason','verify_help','r','r')
    set_ports('identity_reject','identity','r','r')
    set_ports('human_return','guard','r','r')

    routed, inside_segment, clean = routing_kernel(N, E, headers, port)

    def fixed(source,target,points):
        e=next(e for e in E if e['source']==source and e['target']==target)
        e.update(points=clean(points),source_port='b',target_port='t',fixed_route=True,at=None)
        e.pop('reroute',None)

    # Reserve clear vertical continuations before the side branches and
    # returns. A short straight flow must not yield its lane to a detour.
    for e in E:
        if e['kind'] not in ('flow','blocked'):continue
        a,b=port(e['source'],'b'),port(e['target'],'t')
        if abs(a[0]-b[0])>.01 or b[1]<=a[1]:continue
        if any(inside_segment(a,b,n,10) for k,n in N.items() if k not in (e['source'],e['target'])):continue
        if any(inside_segment(a,b,h) for h in headers):continue
        fixed(e['source'],e['target'],[a,b])

    # Both required checks branch together after the section headings, so
    # neither incoming line has to weave around a title.
    a=port('checks_start','b')
    for target in ('use_search_guard','use_original_guard'):
        b=port(target,'t')
        fixed('checks_start',target,[a,(a[0],b[1]-52),(b[0],b[1]-52),b])

    # Keep the main entry straight. Side entries join that same trunk; they
    # must not push it into a second, parallel route to the same destination.
    end=port('signal','t')
    fixed('start','signal',[port('start','b'),end])
    for source in ('early','change','live'):
        a=port(source,'b')
        join_y=a[1]+36 if source=='early' else end[1]-50
        fixed(source,'signal',[a,(a[0],join_y),(end[0],join_y),end])

    # Use one side for selecting a task and the other for collecting results.
    # The shared vertical buses are real forks/joins, not unrelated crossings.
    for source,targets,join in [
        ('search',['now','case_ref','reference','reuse'],'absent'),
        ('evidence_use',['knowledge','experience','memory'],'evidence_done')]:
        a=port(source,'b');end=port(join,'t');merge=end[1]-40
        for target in targets:
            b=port(target,'t')
            fixed(source,target,[a,(a[0],a[1]+28),(120,a[1]+28),(120,b[1]-28),(b[0],b[1]-28),b])
            out=port(target,'b')
            fixed(target,join,[out,(out[0],out[1]+28),(840,out[1]+28),(840,merge),(end[0],merge),end])
        # The last result has no intervening card to bypass. It joins straight
        # down while earlier results arrive on the common collection line.
        fixed(targets[-1],join,[port(targets[-1],'b'),end])
        fixed(source,join,[a,(a[0],a[1]+28),(880,a[1]+28),(880,merge),(end[0],merge),end])
    a=port('dispatch','b');end=port('identity','t');merge=end[1]-45
    for i in range(6):
        target='choose'+str(i);b=port(target,'t')
        fixed('dispatch',target,[a,(a[0],b[1]-28),(b[0],b[1]-28),b])
        source='out'+str(i);out=port(source,'b')
        fixed(source,'identity',[out,(out[0],out[1]+28),(1725,out[1]+28),(1725,merge),(end[0],merge),end])
    out=port('out5','b')
    fixed('out5','identity',[out,(out[0],merge),(end[0],merge),end])

    # A confirmed criterion bypasses the side consultation on the main column.
    for source,target in [('law_clear','law_confirmed'),('rule_resolved','rule_confirmed')]:
        a,b=port(source,'b'),port(target,'t')
        fixed(source,target,[a,(a[0],b[1]-40),(b[0],b[1]-40),b])
    # Human results join the same outer results bus, outside operation panels.
    a=port('human_return','b');b=port('identity','t')
    fixed('human_return','identity',[a,(a[0],a[1]+28),(1725,a[1]+28),(1725,b[1]-45),(b[0],b[1]-45),b])

    next(e for e in E if e['source']=='progress' and e['target']=='record')['reroute']=True

    def return_route(source,target,points):
        e=next(e for e in E if e['source']==source and e['target']==target)
        e.update(points=clean(points),fixed_route=True,layout_return_bus=True,at=None)
        e.pop('reroute',None)

    # Keep labels on the three distinct branches near their source. Each
    # branch can then share its destination's return lane without a loop made
    # only to find room for its label at the far end.
    a=port('retry_scope','l')
    for target,lane,stub,dy in [('progress',60,192,-50),('checks_start',52,192,90),
                               ('use_communicate0_guard',24,24,0)]:
        b=port(target,'l')
        return_route('retry_scope',target,[a,(stub,a[1]),(stub,a[1]+dy),
                     (lane,a[1]+dy),(lane,b[1]),b])
    next(e for e in E if e['source']=='retry_scope' and e['target']=='progress')['label']='다음 작업·\n수정'
    for source in ('goal_review','resume_changed','human_return'):
        a,b=port(source,'r'),port('use_context_initial_guard','r')
        return_route(source,'use_context_initial_guard',[a,(1780,a[1]),(1780,b[1]),b])
    a,b=port('human_return','r'),port('use_context_initial_guard','r')
    return_route('human_return','use_context_initial_guard',[
        a,(a[0]+16,a[1]),(a[0]+16,a[1]+160),(1780,a[1]+160),(1780,b[1]),b])
    next(e for e in E if e['source']=='human_return' and e['target']=='use_context_initial_guard')['label']='조건\n변경'

    # Returns to the same destination use one physical trunk. Keep conditions
    # on each incoming branch, before it joins that trunk.
    for target,side,lane,sources in [
        ('progress','l',60,['precheck_ok']),
        ('checks_start','l',52,['strategy_more']),
        ('identity','r',1732,['identity_reject','use_wait_control']),
        ('delivery_guard','l',60,['delivery_reply','receipt']),
        ('repair','l',42,['delivery_repair']),
    ]:
        b=port(target,side)
        for source in sources:
            a=port(source,side)
            return_route(source,target,[a,(lane,a[1]),(lane,b[1]),b])
    for source,target,side,lane in [('law_reply','law','l',946),
        ('rule_reply','priority','r',1766),('wait_reason','verify_help','r',1710)]:
        a,b=port(source,side),port(target,side)
        return_route(source,target,[a,(lane,a[1]),(lane,b[1]),b])
    next(e for e in E if e['source']=='wait_reason' and e['target']=='verify_help')['label']='검사\n보완'
    a,b=port('delivery_reply','l'),port('repair','l')
    return_route('delivery_reply','repair',[
        a,(a[0]-28,a[1]),(a[0]-28,a[1]+70),(42,a[1]+70),(42,b[1]),b])

    # First retain unaffected routes, then route changed branches around them.
    pending=[]
    for e in E:
        start,end=port(e['source'],e['source_port']),port(e['target'],e['target_port'])
        bad=e.get('reroute') or (e['kind']=='return' and not e.get('layout_return_bus')) or math.dist(start,e['points'][0])>.01 or math.dist(end,e['points'][-1])>.01
        bad=bad or any(inside_segment(a,b,h) for h in headers for a,b in zip(e['points'],e['points'][1:]))
        bad=bad or any(inside_segment(a,b,n,8) for k,n in N.items() if k not in (e['source'],e['target']) for a,b in zip(e['points'],e['points'][1:]))
        if bad:pending.append(e)
    kept=[e for e in E if e not in pending]
    # Short forward paths reserve their entries before long return routes.
    pending.sort(key=lambda e:(e['kind']=='return',abs(N[e['source']]['y']-N[e['target']]['y']) if e['target'] in N and e['source'] in N else 0))
    for e in pending:
        routed(e,kept);kept.append(e)
    print('LAYOUT_POLISH',len(pending),'routes;',len(changed),'shifted or widened cards')
    return max(n['y']+n['h'] for n in N.values())+100


def routing_kernel(N, E, headers, port):
    def inside_segment(a,b,r,pad=0):
        if r.get('axis')=='horizontal':
            if abs(a[0]-b[0])<.01:return False
            pad=0
        x0,y0=r['x']-pad,r['y']-pad;x1=x0+r['w']+2*pad;y1=y0+r['h']+2*pad
        if abs(a[0]-b[0])<.01:
            return x0+.01<a[0]<x1-.01 and max(min(a[1],b[1]),y0)<min(max(a[1],b[1]),y1)-.01
        if abs(a[1]-b[1])<.01:
            return y0+.01<a[1]<y1-.01 and max(min(a[0],b[0]),x0)<min(max(a[0],b[0]),x1)-.01
        return True

    def clean(points):
        result=[]
        for p in points:
            if result and math.dist(result[-1],p)<.01:continue
            while len(result)>1 and ((abs(result[-2][0]-result[-1][0])<.01 and abs(result[-1][0]-p[0])<.01)
                    or (abs(result[-2][1]-result[-1][1])<.01 and abs(result[-1][1]-p[1])<.01)):
                result.pop()
            result.append(p)
        return result

    # Coordinate-compressed orthogonal visibility grid. Rectangles include the
    # full header band, so elbows and labels cannot sit over a function name.
    def routed(e, others):
        start,end=port(e['source'],e['source_port']),port(e['target'],e['target_port'])
        directions={'t':(0,-1),'b':(0,1),'l':(-1,0),'r':(1,0)}
        def stub(p,side):
            dx,dy=directions[side];return (p[0]+dx*28,p[1]+dy*28)
        a,b=stub(start,e['source_port']),stub(end,e['target_port'])
        top=max(4,min(start[1],end[1])-220);bottom=max(start[1],end[1])+220
        obstacles=[n for n in N.values() if n['y']<bottom and n['y']+n['h']>top]
        obstacles+= [h for h in headers if h['y']<bottom and h['y']+h['h']>top]
        xs={24.,60.,90.,1715.,1750.,1780.,a[0],b[0]};ys={top,bottom,a[1],b[1]}
        for n in obstacles:
            xs.update((n['x']-28,n['x']+n['w']+28,n['x']+n['w']/2))
            ys.update((n['y']-28,n['y']+n['h']+28))
        for x,y in e['points']:
            if 6<x<1794:xs.add(x)
            if top<=y<=bottom:ys.add(y)
        xs=sorted(x for x in xs if 6<=x<=1794);ys=sorted(y for y in ys if top<=y<=bottom)
        # Overlapping reservations can put a normal stub in a nearby shape.
        # A shorter perpendicular lead-in remains valid at the same midpoint.
        for role,p,side in [('start',start,e['source_port']),('end',end,e['target_port'])]:
            q=a if role=='start' else b
            if any(inside_segment(p,q,n,10) for n in obstacles if n is not N.get(e['source' if role=='start' else 'target'])):
                dx,dy=directions[side];q=(p[0]+dx*16,p[1]+dy*16)
                if role=='start':a=q
                else:b=q
                xs=sorted(set(xs)|{q[0]});ys=sorted(set(ys)|{q[1]})
        ix={v:i for i,v in enumerate(xs)};iy={v:i for i,v in enumerate(ys)}
        segments=[]
        for other in others:
            for c,d in zip(other['points'],other['points'][1:]):
                if max(c[1],d[1])>=top and min(c[1],d[1])<=bottom:
                    segments.append((c,d,other['kind'],other['source'],other['target'],other['label']))
        cache={}
        def cost(c,d):
            key=tuple(sorted((c,d)))
            if key in cache:return cache[key]
            if any(inside_segment(c,d,n,10) for n in obstacles):
                cache[key]=None;return None
            score=math.dist(c,d)
            for u,v,kind,source,target,label in segments:
                if c[0]==d[0] and u[0]==v[0] and abs(c[0]-u[0])<.01:
                    overlap=min(max(c[1],d[1]),max(u[1],v[1]))-max(min(c[1],d[1]),min(u[1],v[1]))
                elif c[1]==d[1] and u[1]==v[1] and abs(c[1]-u[1])<.01:
                    overlap=min(max(c[0],d[0]),max(u[0],v[0]))-max(min(c[0],d[0]),min(u[0],v[0]))
                else:overlap=0
                related=(source==e['source'] or target==e['target']) and (kind=='return')==(e['kind']=='return')
                if not related:
                    if c[0]==d[0] and u[0]==v[0]:
                        near=abs(c[0]-u[0])<12 and min(max(c[1],d[1]),max(u[1],v[1]))>max(min(c[1],d[1]),min(u[1],v[1]))+.01
                    elif c[1]==d[1] and u[1]==v[1]:
                        near=abs(c[1]-u[1])<12 and min(max(c[0],d[0]),max(u[0],v[0]))>max(min(c[0],d[0]),min(u[0],v[0]))+.01
                    else:near=False
                    if near:cache[key]=None;return None
                if overlap>0:
                    # A shared suffix is an intentional merge, even when each
                    # incoming branch has its own label before the junction.
                    shared=kind==e['kind'] and ((target==e['target']) or
                        (not label and not e['label'] and related))
                    score+=overlap*(0 if shared else 35)
                if c[1]==d[1] and u[0]==v[0] and min(c[0],d[0])<u[0]<=max(c[0],d[0]) and min(u[1],v[1])<c[1]<max(u[1],v[1]):score+=200
                if c[0]==d[0] and u[1]==v[1] and min(u[0],v[0])<c[0]<max(u[0],v[0]) and min(c[1],d[1])<u[1]<=max(c[1],d[1]):score+=200
            cache[key]=score;return score
        first=(ix[a[0]],iy[a[1]],0 if e['source_port'] in ('l','r') else 1)
        distance={first:0};parent={};queue=[(math.dist(a,b),0,first)];last=None
        while queue:
            _,score,state=heapq.heappop(queue)
            if score!=distance.get(state):continue
            x,y,axis=state
            if (xs[x],ys[y])==b:last=state;break
            for dx,dy,newaxis in ((-1,0,0),(1,0,0),(0,-1,1),(0,1,1)):
                nx,ny=x+dx,y+dy
                if not(0<=nx<len(xs) and 0<=ny<len(ys)):continue
                c,d=(xs[x],ys[y]),(xs[nx],ys[ny]);step=cost(c,d)
                if step is None:continue
                total=score+step+(120 if axis!=newaxis else 0)
                nxt=(nx,ny,newaxis)
                if total<distance.get(nxt,float('inf')):
                    distance[nxt]=total;parent[nxt]=state
                    heapq.heappush(queue,(total+abs(d[0]-b[0])+abs(d[1]-b[1]),total,nxt))
        if last is None:raise ValueError(('No clear route',e['source'],e['target'],start,end,a,b,[(n.get('title'),n['x'],n['y'],n['w'],n['h']) for n in obstacles if inside_segment(a,(a[0]+.1,a[1]),n,10) or inside_segment(b,(b[0]+.1,b[1]),n,10)]))
        points=[]
        while True:
            points.append((xs[last[0]],ys[last[1]]))
            if last==first:break
            last=parent[last]
        e.update(points=clean([start,*reversed(points),end]),fixed_route=True,at=None)
        e.pop('reroute',None)

    return routed, inside_segment, clean


def finish_routes(N, E, G, A, port, measure):
    headers=[]
    for g in G:
        if g.get('support_scope') or g['id'].startswith('opg'):
            headers.append(dict(x=g['x'],y=g['y'],w=g['w'],
                h=49+32*(len(g.get('title_lines',[g['title']]))-1),axis='horizontal'))
    routed, inside, clean = routing_kernel(N,E,headers,port)
    def clashes(e):
        return any(inside(a,b,n,6) for k,n in N.items() if k not in (e['source'],e['target'])
                   for a,b in zip(e['points'],e['points'][1:])) or any(
                   inside(a,b,h) for h in headers for a,b in zip(e['points'],e['points'][1:]))
    pending=[e for e in E if e.get('reroute') or clashes(e)]
    kept=[e for e in E if e not in pending]
    pending.sort(key=lambda e:(e['kind']=='return',abs(N[e['source']]['y']-N[e['target']]['y']) if e['target'] in N else 0))
    for e in pending:
        routed(e,kept);kept.append(e)
    # New paths must also avoid sharing a segment with unrelated routes.
    def overlaps(e,f):
        if (e['source']==f['source'] or e['target']==f['target']) and (e['kind']=='return')==(f['kind']=='return'):
            return False
        for a,b in zip(e['points'],e['points'][1:]):
            for c,d in zip(f['points'],f['points'][1:]):
                for axis in (0,1):
                    other=1-axis
                    if abs(a[axis]-b[axis])<.01 and abs(c[axis]-d[axis])<.01 and abs(a[axis]-c[axis])<.01:
                        if min(max(a[other],b[other]),max(c[other],d[other]))-max(min(a[other],b[other]),min(c[other],d[other]))>1:return True
        return False
    for e in E:
        if any(overlaps(e,f) for f in E if f is not e):
            routed(e,[f for f in E if f is not e])
    print('CLARIFIED_ROUTES',len(pending))
