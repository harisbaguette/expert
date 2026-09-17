#!/usr/bin/env python3
"""세 상황의 재료 조합 순서도. Python 표준 라이브러리만 사용.

도형 좌표와 연결점을 함께 정의한다. 좌표를 비등방 확대하지 않는다.
재료 하나당 도형 하나, 실제 합류는 점으로 표시, 계통 순서로 연결하지 않는다.
"""
from pathlib import Path
from html import escape
import json, re, math, argparse
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'전문가 에이전트 정의.md'
COLORS={'main':('#dbeafe','#719ddd','#17314f'),'note':('#fef9c3','#d2b34e','#713f12'),'back':('#ffedd5','#e3a46b','#7c2d12'),'store':('#e5e7eb','#9ca3af','#1f2937'),'good':('#dcfce7','#55ba7c','#14532d'),'stop':('#fee2e2','#de9393','#7f1d1d')}
def catalog():
    part=DOC.read_text().split('## 계통별 재료')[1].split('## 사용 구조')[0]; out={}
    for line in part.splitlines():
        if not line.startswith('| **') or '✅' not in line:continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        if len(cells)==6:
            name=re.search(r'\*\*(.*?)\*\*',cells[0]).group(1)
            out[name]={'type':cells[4].strip('*'),'meaning':cells[2],'when':cells[5]}
    assert len(out)==79
    return out
CAT=catalog()
def tw(s,size):return sum(size*(1 if ord(c)>=0x2e80 else .32 if c==' ' else .58) for c in s)
def wrap(s,size,limit):
    lines=[]
    for para in s.split('\n'):
        line=''
        for word in para.split():
            if line and tw(line+' '+word,size)>limit:lines.append(line);line=''
            line=(line+' '+word).strip()
            while tw(line,size)>limit:
                n=1
                while n<len(line) and tw(line[:n+1],size)<=limit:n+=1
                lines.append(line[:n]);line=line[n:]
        if line:lines.append(line)
    return lines

def rounded(ps,r=18):
    ps=[p for i,p in enumerate(ps) if i==0 or p!=ps[i-1]]
    d=f'M {ps[0][0]} {ps[0][1]}'
    for a,b,c in zip(ps,ps[1:],ps[2:]):
        l1,l2=math.dist(a,b),math.dist(b,c)
        q=min(r,l1/2,l2/2)
        p1=(b[0]+(a[0]-b[0])*q/l1,b[1]+(a[1]-b[1])*q/l1)
        p2=(b[0]+(c[0]-b[0])*q/l2,b[1]+(c[1]-b[1])*q/l2)
        d+=f' L {p1[0]} {p1[1]} Q {b[0]} {b[1]} {p2[0]} {p2[1]}'
    return d+f' L {ps[-1][0]} {ps[-1][1]}'

class Chart:
    def __init__(self,mode):
        self.mode=mode;self.W=1380 if mode==1 else 1780;self.y=150
        self.nodes={};self.edges=[];self.labels=[];self.frames=[];self.decor=[];self.failures=[]
    def txt(self,s,x,y,size=16,color='#d4deeb',bold=False,anchor='middle'):
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(s)}</text>'
    def label(self,s,x,y,color='#dae7f7'):
        lines=wrap(s,16,310);w=max([tw(t,16) for t in lines]+[0])+16;h=len(lines)*23
        self.labels.append({'text':s,'x':x-w/2,'y':y-18,'w':w,'h':h+4,'svg':f'<g class="edge-label"><rect x="{x-w/2}" y="{y-18}" width="{w}" height="{h+4}" rx="4" fill="#202020"/>'+''.join(self.txt(t,x,y+i*23,16,color) for i,t in enumerate(lines))+'</g>'})
    def node(self,k,name='',help='',cx=680,y=None,w=330,kind='main',shape='process',material=None):
        y=self.y if y is None else y
        if material:name=material;assert material in CAT
        fs=21 if shape!='decision' else 20
        names=wrap(name,fs,w-46 if shape!='decision' else w*.61)
        helps=wrap(help,17,w-46 if shape!='decision' else w*.61)
        content=len(names)*29+len(helps)*25+(24 if material else 10 if helps else 0)
        h=max(64,content+32)
        if shape=='decision':h=max(176,content*1.7+32)
        n={'id':k,'name':name,'material':material,'type':CAT[material]['type'] if material else None,'help':help,'x':cx-w/2,'y':y,'w':w,'h':h,'shape':shape,'kind':kind}
        self.nodes[k]=n
        x=n['x'];f,s,c=COLORS[kind]
        if shape=='decision':boundary=f'<polygon points="{cx},{y} {x+w},{y+h/2} {cx},{y+h} {x},{y+h/2}"/>'
        else:
            boundary=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if shape=="terminal" else 3}"/>'
            if shape=='call':boundary+=f'<path d="M {x+11} {y} V {y+h} M {x+w-11} {y} V {y+h}" fill="none"/>'
        ty=y+(h-content)/2+23
        words=[]
        for t in names:words.append(self.txt(t,cx,ty,fs,c,True));ty+=29
        if material:words.append(self.txt(CAT[material]['type'],cx,ty-2,12,c));ty+=24
        elif helps:ty+=10
        for t in helps:words.append(self.txt(t,cx,ty,17,c));ty+=25
        n['svg']=f'<g class="node" id="{k}" data-material="{escape(material or "")}" data-shape="{shape}" fill="{f}" stroke="{s}" stroke-width="1.8">{boundary}<g class="node-text" stroke="none">'+''.join(words)+'</g></g>'
        return k
    def m(self,k,name,help='',**kw):return self.node(k,help=help,material=name,**kw)
    def q(self,k,name,**kw):return self.node(k,name,shape='decision',kind='note',**kw)
    def pt(self,k,p):
        n=self.nodes[k];x,y,w,h=n['x'],n['y'],n['w'],n['h']
        return {'t':(x+w/2,y),'b':(x+w/2,y+h),'l':(x,y+h/2),'r':(x+w,y+h/2)}[p]
    def bottom(self,k):return self.nodes[k]['y']+self.nodes[k]['h']
    def after(self,*ks,gap=72):self.y=max(self.bottom(k) for k in ks)+gap
    def path(self,ps,a=None,b=None,dashed=False,arrow=True,label='',label_at=None,relation='flow'):
        self.edges.append({'a':a,'b':b,'points':ps,'dashed':dashed,'arrow':arrow,'relation':relation,'label':label})
        if label:self.label(label,*(label_at or ((ps[0][0]+ps[-1][0])/2,(ps[0][1]+ps[-1][1])/2-10)))
    def edge(self,a,b,ports='bt',via=None,label='',label_at=None,**kw):
        p,q=self.pt(a,ports[0]),self.pt(b,ports[1])
        if via is None:
            if p[0]==q[0] or p[1]==q[1]:via=[]
            elif ports=='bt':via=[(p[0],(p[1]+q[1])/2),(q[0],(p[1]+q[1])/2)]
            else:via=[((p[0]+q[0])/2,p[1]),((p[0]+q[0])/2,q[1])]
        self.path([p,*via,q],a,b,label=label,label_at=label_at,**kw)
    def join(self,ks,target,y=None):
        y=self.nodes[target]['y']-38 if y is None else y;tx=self.pt(target,'t')[0]
        for k in ks:
            p=self.pt(k,'b');self.path([p,(p[0],y),(tx,y)],k,target,arrow=False)
        self.path([(tx,y),self.pt(target,'t')],None,target)
        self.decor.append(f'<circle cx="{tx}" cy="{y}" r="3.7" fill="#77b7fa"/>')
    def frame(self,title,top,bottom,x=90,w=1200,sub=''):
        self.frames.append(f'<g class="section"><rect x="{x}" y="{top}" width="{w}" height="{bottom-top}" rx="12" fill="none" stroke="#b4c0ce" stroke-opacity=".38" stroke-dasharray="3 8"/><g>'+self.txt(title,x+22,top+30,21,'#e2e8f0',True,'start')+(self.txt(sub,x+22,top+58,16,'#adbdcf',False,'start') if sub else '')+'</g></g>')
    def section(self,title,sub=''):
        self.y+=30;top=self.y;self.y+=90 if sub else 66;return top
    def chain(self,prefix,items,prev=None,cx=680,w=330,kind='main'):
        ids=[]
        for i,(name,help) in enumerate(items):
            k=self.m(f'{prefix}{i}',name,help,cx=cx,w=w,kind=kind)
            if ids:self.edge(ids[-1],k)
            elif prev:self.edge(prev,k)
            ids.append(k);self.after(k)
        return ids
    def branch_rows(self,prefix,items,source,title,sub='',dashed=False):
        top=self.section(title,sub);iy=self.y-28;left=185;right=1175;cx=680;ys=[];ids=[]
        p=self.pt(source,'b');self.path([p,(p[0],iy-28),(left,iy-28),(left,iy)],source,None,arrow=False,dashed=dashed)
        for i,(name,condition,result) in enumerate(items):
            k=self.m(f'{prefix}{i}',name,'',cx=cx,w=360,kind='store' if dashed else 'main');n=self.nodes[k];cy=n['y']+n['h']/2
            self.path([(left,cy),self.pt(k,'l')],None,k,dashed=dashed,label=condition,label_at=(335,cy-13),relation='rule-input' if dashed else 'conditional-input')
            self.path([self.pt(k,'r'),(right,cy)],k,None,dashed=dashed,arrow=False,label=result,label_at=(1025,cy-13),relation='result')
            self.decor += [f'<circle cx="{x}" cy="{cy}" r="3.4" fill="#77b7fa"/>' for x in (left,right)]
            ys.append(cy);ids.append(k);self.after(k,gap=58)
        end=self.y-20
        self.path([(left,iy),(left,ys[-1])],source,None,arrow=False,dashed=dashed,relation='bus')
        self.path([(right,ys[0]),(right,end),(680,end)],None,None,arrow=False,dashed=dashed,relation='bus')
        self.frame(title,top,end+24,sub=sub)
        self.y=end+100
        return (680,end),ids
    def from_point(self,p,k):self.path([p,self.pt(k,'t')],None,k)
    def render_connections(self):
        """공유 선은 한 번만 그린다. 분기·합류점을 표시하고 끝점에 방향을 표시한다."""
        result=[]
        for dashed in (False,True):
            edges=[e for e in self.edges if e['dashed']==dashed]
            segments=[(tuple(a),tuple(b)) for e in edges for a,b in zip(e['points'],e['points'][1:]) if a!=b]
            endpoints={p for ab in segments for p in ab}
            graph={};atomic=set()
            for a,b in segments:
                axis=0 if a[1]==b[1] else 1
                assert a[1-axis]==b[1-axis],(a,b)
                cuts=sorted((p for p in endpoints if p[1-axis]==a[1-axis] and min(a[axis],b[axis])<=p[axis]<=max(a[axis],b[axis])),key=lambda p:p[axis])
                for p,q in zip(cuts,cuts[1:]):
                    pair=tuple(sorted((p,q)));atomic.add(pair)
                    graph.setdefault(p,set()).add(q);graph.setdefault(q,set()).add(p)
            used=set();paths=[]
            starts=[p for p,ns in graph.items() if len(ns)!=2]+list(graph)
            for p in starts:
                for q in sorted(graph[p]):
                    pair=tuple(sorted((p,q)))
                    if pair in used:continue
                    points=[p,q];used.add(pair)
                    while len(graph[points[-1]])==2:
                        prev,at=points[-2:];nxt=next(t for t in graph[at] if t!=prev)
                        pair=tuple(sorted((at,nxt)))
                        if pair in used:break
                        used.add(pair);points.append(nxt)
                    paths.append(points)
            color='#9aaec4' if dashed else '#77b7fa'
            dash=' stroke-dasharray="5 6"' if dashed else ''
            for points in paths:
                result.append(f'<path class="edge" d="{rounded(points)}" fill="none" stroke="{color}" stroke-width="1.8"{dash}/>')
            for p,ns in graph.items():
                if len(ns)>2:result.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="3.5" fill="{color}"/>')
            ends=set()
            for e in edges:
                if not e['arrow']:continue
                a,b=next((tuple(a),tuple(b)) for a,b in reversed(list(zip(e['points'],e['points'][1:]))) if a!=b)
                dist=math.dist(a,b);p=(b[0]+(a[0]-b[0])*min(12,dist)/dist,b[1]+(a[1]-b[1])*min(12,dist)/dist)
                if (p,b) in ends:continue
                ends.add((p,b))
                result.append(f'<path d="M {p[0]} {p[1]} L {b[0]} {b[1]}" fill="none" stroke="{color}" stroke-width="1.8" marker-end="url(#arrow)"/>')
        return ''.join(result)

    def save(self,out):
        names={n['material'] for n in self.nodes.values() if n['material']};assert names==set(CAT),set(CAT)-names
        height=math.ceil(self.y+45)
        model={'mode':self.mode,'catalog':CAT,'nodes':{k:{p:v for p,v in n.items() if p!='svg'} for k,n in self.nodes.items()},'edges':self.edges,'labels':[{k:v for k,v in l.items() if k!='svg'} for l in self.labels],'width':self.W,'height':height}
        title=['단독 상황','오케스트레이션','복합 상황'][self.mode-1]
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{height}" viewBox="0 0 {self.W} {height}" role="img" aria-labelledby="title description"><title id="title">{title}: 79개 재료의 사용 조건과 조합</title><desc id="description">실선은 실행과 결과 전달, 점선은 계속 적용되는 책임 또는 규칙 입력. 재료명은 표와 동일하며 한 재료를 한 도형에 표시한다.</desc><metadata id="material-usage-model">{escape(json.dumps(model,ensure_ascii=False))}</metadata><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#77b7fa"/></marker></defs><style>text{{font-family:"Apple SD Gothic Neo","Noto Sans KR",sans-serif}}</style><rect width="100%" height="100%" fill="#202020"/>'
        svg+=''.join(self.frames)
        svg+=self.render_connections()
        svg+=''.join(self.decor)+''.join(n['svg'] for n in self.nodes.values())+''.join(l['svg'] for l in self.labels)+'</svg>'
        slug=['solo','orchestration','complex'][self.mode-1];(out/f'usage-materials-{slug}.svg').write_text(svg)
        return {'mode':slug,'width':self.W,'height':height,'materials':len(names),'nodes':len(self.nodes),'types':dict(Counter(CAT[m]['type'] for m in names))}


def build(mode):
    c=Chart(mode)
    c.decor.append(c.txt(['한 건 · 한 전문가','한 건 · 총괄과 여러 전문가','맞물린 여러 건 · 전체 총괄과 건별 팀'][mode-1],c.W/2,40,27,'#f1f5f9',True))
    c.decor.append(c.txt('재료명은 굵게 · 실선은 실행·결과 전달 · 점선은 전 구간 적용·규칙 입력',c.W/2,76,17))
    c.decor.append(c.txt('상시는 책임 유지 · 단계별은 해당 단계에 · 조건부는 화살표의 조건에 해당하면 사용',c.W/2,105,16))
    start=c.node('start','요청·변경·재개 신호 도착',kind='good',shape='terminal');c.after(start)
    inp=c.chain('input',[('시작 신호','새 업무 또는 기다리던 업무에 신호를 연결'),('업무별 정보','대상·기한·요청 내용·현재 조건을 모음'),('지시·의도 파악','무엇을 원하는지와 허용한 범위를 확인'),('문제·목표·완료 조건','해결할 문제와 완료를 증명할 결과를 정함'),('성과 추적','어떤 성과를 언제 확인할지 정함')],start)
    last=inp[-1]
    if mode>1:
        t=c.section('총괄이 역할·입력·결과를 연결','동시에 할 수 있는 일은 나누고, 의존하는 일은 선행 결과가 확인된 뒤 배정')
        items=[('대안·전략 판단','분담 방법·우선순위·필요한 전문성을 비교')]
        if mode==3:items += [('비용·위험 한도','모든 건의 사용·진행·예약분을 합산해 공동 자원·한도를 배정')]
        items += [('업무 절차·실행 계획','담당별 입력·결과와 선후 관계를 정함'+(' · 서로 기다리는 관계는 분해·순서 조정' if mode==3 else '')),('나눠 맡기기','작업·자료·권한·기한·반환 형식을 담당별로 전달')]
        dispatch=c.chain('dispatch',items,last);last=dispatch[-1];c.frame('총괄이 역할·입력·결과를 연결',t,c.y-20,sub='동시에 할 수 있는 일은 나누고, 의존하는 일은 선행 결과가 확인된 뒤 배정')
        c.y+=65
        if mode==3:
            lead_a=c.m('lead_a','나눠 맡기기','건 A 총괄 → A의 전문가들에게 분담',cx=680)
            lead_b=c.m('lead_b','나눠 맡기기','건 B 총괄 → B의 전문가들에게 분담',cx=1560,w=300)
            jy=c.y-32;p=c.pt(last,'b');c.path([p,(680,jy)],last,None,arrow=False)
            for k in (lead_a,lead_b):q=c.pt(k,'t');c.path([(680,jy),(q[0],jy),q],last,k)
            c.after(lead_a,lead_b);last=lead_a;otherprev=lead_b
        else:otherprev=last
    else:
        unused=c.m('unused','나눠 맡기기','이 상황에서는 미사용\n한 전문가가 직접 처리',cx=1080,w=300,kind='store',y=c.nodes[last]['y'])
        c.edge(last,unused,ports='rl',dashed=True,arrow=False,relation='scope')
    # Expand one actual expert lane; other experts retain distinct input and output lanes.
    expert_top=c.y
    entry=c.node('expert_entry','한 전문가의 재료 조합' if mode==1 else '전문가 A의 재료 조합' if mode==2 else '건 A · 각 전문가의 재료 조합',help='자기 목표·자료·권한으로 판단·실행·검증',shape='call',w=430)
    if mode==2:
        fork_y=c.y-35;p=c.pt(last,'b');c.path([p,(680,fork_y)],last,None,arrow=False)
        c.path([(680,fork_y),c.pt(entry,'t')],last,entry)
    else:c.edge(last,entry)
    if mode>1:
        other=c.node('other_expert','전문가 B · 독립 실행' if mode==2 else '건 B · 전문가별 독립 실행',help='왼쪽과 같은 재료 조합을\n자기 목표·자료·권한으로 사용\n다른 전문가와 상태를 섞지 않음',cx=1560,w=300,shape='call')
        if mode==2:c.path([(680,fork_y),(1560,fork_y),c.pt(other,'t')],last,other)
        else:c.edge(otherprev,other)
    c.after(entry,gap=65)
    # Ongoing operating relations are scoped, not steps in the solid execution path.
    t=c.section('실행 내내 유지되는 책임','아래 다섯 재료는 단계 순서가 아니라 전 구간의 실행·기록·복구를 뒷받침')
    a=c.m('control','실행 제어','판단·도구·분기를 호출하고 결과·오류를 연결',cx=345,w=380,kind='store')
    b=c.m('isolation','분리 실행','작업·자료·자원을 분리하고 허용 범위만 공유',cx=1015,w=380,kind='store')
    c.edge(a,b,ports='rl',dashed=True,label='작업별 실행',label_at=(680,c.nodes[a]['y']+65),relation='scope')
    c.after(a,b)
    rec=c.m('record','판단 근거 기록','선택·판단·실행·검증의 입력과 이유를 기록',cx=345,w=380,kind='store')
    ops=c.m('ops','운영 감시·복구','별도 감시자가 지연·장애를 격리하고 저장 상태로 복구',cx=1015,w=380,kind='store')
    c.edge(a,rec,dashed=True,relation='scope');c.edge(b,ops,dashed=True,relation='scope');c.after(rec,ops)
    state=c.m('ongoing_state','현재 진행 상태','담당·완료·대기·승인·취소·미확인을 유지',kind='store',w=390)
    for k in (rec,ops):c.edge(k,state,dashed=True,relation='scope')
    c.after(state,gap=45);c.frame('실행 내내 유지되는 책임',t,c.y,sub='아래 다섯 재료는 단계 순서가 아니라 전 구간의 실행·기록·복구를 뒷받침')
    # Solid main path bypasses the ongoing responsibility frame.
    c.y+=100
    facts=c.m('facts','정보·자료 이해','받은 자료의 사실·주장·추정과 맥락을 구별',cx=420,w=350)
    mem=c.m('memory','장기 기억','관련된 이전 결정·약속·교훈을 불러옴',cx=940,w=350,kind='store')
    p=c.pt(entry,'l');q=c.pt(facts,'t');routey=c.y-35
    c.path([p,(100,p[1]),(100,routey),(940,routey),c.pt(mem,'t')],entry,mem)
    c.path([(420,routey),q],entry,facts)
    c.decor.append(f'<circle cx="420" cy="{routey}" r="3.4" fill="#77b7fa"/>')
    c.after(facts,mem)
    ctx=c.m('context','현재 작업 정보','이번 자료·관련 기억·진행 상태를 필요한 만큼 구성',cx=345,w=380)
    knowledge=c.m('knowledge','업무 지식','원리·방법·적용 조건',cx=790,w=280)
    experience=c.m('experience','실전 경험·감각','핵심 단서·예외·함정',cx=1100,w=280)
    c.join((facts,mem),ctx)
    c.after(ctx,knowledge,experience)
    model=c.m('model','AI 모델','현재 정보에 지식·경험을 함께 써서 판단하고 내용을 생성',w=390)
    c.join((ctx,knowledge,experience),model);c.after(model)
    # Search branch.
    q=c.q('search_q','근거가 더 필요한가?');c.edge(model,q);c.after(q)
    search=c.m('search','정보·자료 찾기','부족한 근거·지식·방법을 원문까지 확인',cx=1010,w=340)
    c.edge(q,search,label='예',label_at=(970,c.nodes[search]['y']-20));c.after(search)
    empty=c.m('empty','못 찾음·없음 구분','빈 조회·없음 판단 때 검색 한계·접근 불가·확인된 없음을 구별',cx=1010,w=340)
    c.edge(search,empty,label='빈 조회 또는 없음 판단',label_at=(1010,c.nodes[empty]['y']-24));c.after(empty,gap=110)
    ev=c.m('evidence','근거의 신뢰성·적합성','새 근거와 기존 근거의 출처·한계·적합성을 확인',cx=420,w=350)
    version=c.m('version','자료의 시점·버전','대상 시점에 맞는 판본·확인 시각을 확인',cx=940,w=350)
    py=c.nodes[ev]['y']-37
    c.path([c.pt(q,'l'),(185,c.pt(q,'l')[1]),(185,py-36),(680,py-36)],q,None,arrow=False,label='아니오 · 기존 근거',label_at=(315,c.pt(q,'l')[1]+42))
    c.path([c.pt(search,'r'),(1245,c.pt(search,'r')[1]),(1245,py-36),(680,py-36)],search,None,arrow=False,label='찾음',label_at=(1245,c.bottom(search)+43))
    c.path([c.pt(empty,'b'),(1010,py-36),(680,py-36)],empty,None,arrow=False)
    c.path([(680,py-36),(680,py)],None,None,arrow=False)
    for k in (ev,version):p=c.pt(k,'t');c.path([(680,py),(p[0],py),p],None,k)
    c.after(ev,version)
    extraq=c.q('extra_q','추가로 필요한 자료가 있는가?');c.join((ev,version),extraq)
    c.after(extraq)
    entries=[('적용 사례','적용 과정 비교','비슷한 조건·차이'),('참고 자료','원리·방법 참고','설명·작업 근거'),('재사용 자료','서식·부품 활용','권한·호환이 맞는 재료'),('현재 값·상태 확인','현재 값이 중요','조회 값·확인 시각'),('먼저 알아채기','상황 감시를 맡음','새 문제·기회·긴급도'),('변경 감시·반영','변화를 계속 추적','변경 내용·영향받는 일')]
    p,_=c.branch_rows('source_',entries,extraq,'필요한 자료를 함께 더함','각 조건에 해당하는 가지를 사용 · 위아래는 실행 순서가 아님')
    enriched=c.m('enriched','현재 작업 정보','추가 정보·변경·확인 한계를 이번 판단에 반영',w=390);c.from_point(p,enriched)
    a=c.pt(extraq,'l');b=c.pt(enriched,'l');c.path([a,(120,a[1]),(120,b[1]),b],extraq,enriched,label='아니오 · 기존 정보 사용',label_at=(300,a[1]+42));c.after(enriched)
    # Rules are a bank of applicable sources with explicit hierarchy, not a temporal sequence.
    rulesrc=c.m('rule_source','규칙·기준 원문','대상·지역·시점·설정 권한에 맞는 원문 확보');c.edge(enriched,rulesrc);c.after(rulesrc)
    rules=[('법·의무 기준','먼저 법적 적용 관계','상하·위임·특별·개정·경과'),('직업 윤리·의무','그 안에서 우선 ①','직업의 필수 의무'),('에이전트 기본 원칙','그 안에서 우선 ①','원칙·승인된 보호 기준'),('계약·합의 조건','그다음 ②','유효한 계약·합의'),('플랫폼·제출처 규정','그다음 ②','플랫폼·제출처 필수 규정'),('조직 규칙','그다음 ③','조직의 필수 규칙'),('사용자 지정 규칙','그다음 ④','사용자가 추가한 필수 조건'),('표현 방식·스타일','표현 기준이 필요할 때','⑤ 기본 방식·스타일')]
    p,_=c.branch_rows('rule_',rules,rulesrc,'적용할 규칙을 함께 대조 · 번호는 충돌 시 위계','문서 이름보다 의무의 근거·설정 권한을 따름 · 기본 스타일보다 높은 의무를 먼저 지킴',dashed=True)
    priority=c.m('priority','규칙의 적용·우선순위','적용 규칙은 함께 지킴 · 충돌하는 조항만 위계로 조정\n하위 조건도 충돌하지 않으면 유지',w=410);c.from_point(p,priority);c.after(priority)
    rq=c.q('rule_q','적용 조건·충돌이 해결됐는가?');c.edge(priority,rq);c.after(rq)
    humanrule=c.m('rule_human','사람에게 넘기기','근거·대안을 갖춰 해석·예외 권한자에게 결정 요청',cx=1020,w=350,kind='back')
    c.edge(rq,humanrule,label='아니오',label_at=(990,c.nodes[humanrule]['y']-23));c.after(humanrule)
    rulewho=c.m('rule_who','보고 주체 확인','답변자의 권한과 결정 범위를 확인',cx=1020,w=350,kind='back');c.edge(humanrule,rulewho);c.after(rulewho)
    resolved=c.q('rule_reply','유효한 결정으로 해결됐는가?',cx=1020,w=350);c.edge(rulewho,resolved)
    a=c.pt(resolved,'r');b=c.pt(priority,'r');c.path([a,(1245,a[1]),(1245,b[1]),b],resolved,priority,label='예 · 조건 반영 후 다시 대조',label_at=(1120,b[1]-38))
    c.after(resolved)
    rfail=c.node('rule_hold','충돌 미해결 · 해당 작업 보류',help='이유·남은 책임을 반환',cx=1020,w=350,kind='stop');c.edge(resolved,rfail,label='아니오',label_at=(1020,c.nodes[rfail]['y']-22));c.failures.append(rfail);c.after(rfail)
    plan=c.chain('plan',[('문제·목표·완료 조건','확인한 근거·규칙으로 목표와 완료 증거를 확정'),('대안·전략 판단','정보·지식·경험으로 대안의 효과·비용·위험을 비교'),('업무 절차·실행 계획','어떤 재료의 결과를 다음 어떤 재료가 받을지 정함'),('빠진 위험 확인','계획·변경·실행·전달에서 빠진 조건과 피해를 점검')])
    a=c.pt(rq,'l');b=c.pt(plan[0],'l');c.path([a,(185,a[1]),(185,b[1]),b],rq,plan[0],label='예 · 적용 조건 확정',label_at=(320,a[1]+42))
    # Capability and permissions; local fail paths join one outcome return rail.
    aq=c.q('ability_q','이번 범위의 능력이 검증됐는가?');c.edge(plan[-1],aq);c.after(aq)
    env=c.m('ability_env','시험 환경','별도 시험 공간·조건이 필요하면 준비',cx=1020,w=350)
    c.edge(aq,env,label='아니오 · 별도 환경 필요',label_at=(1000,c.nodes[env]['y']-23));c.after(env)
    test=c.m('ability_test','업무 능력 시험','첫 투입·범위 밖·능력 변경·시험 신뢰 상실이면 시험',cx=1020,w=350);c.edge(env,test)
    a=c.pt(aq,'r');b=c.pt(test,'r');c.path([a,(1245,a[1]),(1245,b[1]),b],aq,test,label='아니오 · 별도 환경 불필요',label_at=(1080,c.bottom(test)+33));c.after(test)
    passed=c.q('ability_pass','이번 업무를 수행할 수 있는가?',cx=1020,w=350);c.edge(test,passed);c.after(passed)
    afail=c.node('ability_hold','미검증 범위는 투입하지 않음',help='부족한 능력·미완료 상태 반환',cx=1020,w=350,kind='stop');c.edge(passed,afail,label='아니오',label_at=(1020,c.nodes[afail]['y']-22));c.failures.append(afail);c.after(afail,gap=110)
    auth=c.m('authority','업무 권한','대상·행동·내용·기간의 위임과 동의',cx=420,w=350)
    limit=c.m('limit','비용·위험 한도','사용량+진행분+예약분과 실행·대기의 위험',cx=940,w=350)
    gy=c.nodes[auth]['y']-40
    for src,label in ((aq,'예 · 검증된 범위'),(passed,'예 · 시험 통과')):
        a=c.pt(src,'l');c.path([a,(185 if src==aq else 750,a[1]),(185 if src==aq else 750,gy-36),(680,gy-36)],src,None,arrow=False,label=label,label_at=(345 if src==aq else 665,c.pt(src,'l')[1]+40))
    c.path([(680,gy-36),(680,gy)],None,None,arrow=False)
    for k in (auth,limit):p=c.pt(k,'t');c.path([(680,gy),(p[0],gy),p],None,k)
    c.after(auth,limit)
    safety=c.m('safety','안전장치','매 실행·위임·재시도·재개 전\n규칙·권한·승인·한도를 함께 검사',w=410);c.join((auth,limit),safety);c.after(safety)
    allow=c.q('allowed','이번 행동을 실행할 수 있는가?');c.edge(safety,allow);c.after(allow)
    h=c.m('human','사람에게 넘기기','되돌릴 수 없는 일·승인 조건·판단 불가·한도 초과·자격자 전속',cx=1020,w=350,kind='back');c.edge(allow,h,label='사람의 결정·작업 필요',label_at=(985,c.nodes[h]['y']-22));c.after(h)
    wait=c.m('human_wait','대기·후속 관리','AI가 준비·비교·검증을 마친 뒤 필요한 결정·작업과 기한을 관리',cx=1020,w=350,kind='back');c.edge(h,wait);c.after(wait)
    who=c.m('human_who','보고 주체 확인','답변자·권한·대상·승인 내용을 대조',cx=1020,w=350,kind='back');c.edge(wait,who);c.after(who)
    hq=c.q('human_reply','유효한 답변을 받았는가?',cx=1020,w=350);c.edge(who,hq)
    a=c.pt(hq,'l');b=c.pt(wait,'l');c.path([a,(770,a[1]),(770,b[1]),b],hq,wait,label='아직 대기 · 기한 안',label_at=(640,a[1]-15))
    a=c.pt(hq,'r');b=c.pt(safety,'r');c.path([a,(1245,a[1]),(1245,b[1]),b],hq,safety,label='예 · 원래 행동을 다시 검사',label_at=(1100,b[1]-40));c.after(hq)
    hfail=c.node('human_hold','금지·거절·취소·기한 종료',help='해당 행동을 실행하지 않고 상태 반환',cx=1020,w=350,kind='stop');c.edge(hq,hfail,label='아니오 · 기한 종료·거절',label_at=(1020,c.nodes[hfail]['y']-23));c.failures.append(hfail)
    a=c.pt(allow,'l');b=c.pt(hfail,'l');c.path([a,(430,a[1]),(430,b[1]),b],allow,hfail,label='금지 · 우회 실행 금지',label_at=(440,a[1]+118));c.after(hfail)
    action_context=c.m('action_context','현재 작업 정보','확인한 자료·조건 + 직전 재료의 검증 결과',w=390)
    a=c.pt(allow,'l');b=c.pt(action_context,'l');c.path([a,(185,a[1]),(185,b[1]),b],allow,action_context,label='허용 · 바로 실행',label_at=(205,a[1]+50));c.after(action_context)
    progress=c.m('progress','작업 진행·연결','입력이 준비된 재료를 연결\n한 재료의 결과를 다음 재료의 입력으로 사용',w=410);c.edge(action_context,progress);c.after(progress)
    toolq=c.q('tool_q','외부 도구·시스템이 필요한가?');c.edge(progress,toolq);c.after(toolq)
    tool=c.m('tool','업무 도구·시스템','요청 형식을 맞춰 연결하고 실제 결과·오류·처리 상태를 받음',cx=1020,w=350);c.edge(toolq,tool,label='예',label_at=(990,c.nodes[tool]['y']-24));c.after(tool)
    select=c.q('select','이번에 필요한 작업은?');c.edge(tool,select)
    a=c.pt(toolq,'l');b=c.pt(select,'l');c.path([a,(185,a[1]),(185,b[1]),b],toolq,select,label='아니오',label_at=(320,a[1]+42));c.after(select)
    actions=[('자료 선별·분류','고를·분류할 자료','선별 자료·분류'),('자료 정리·결합','오류·중복·누락 자료','정리·결합한 자료'),('형식·구조 변환','형식 변경 필요','다음 도구의 입력'),('계산','값·식이 필요','계산값·단위'),('분석','차이·관계·원인 해석','해석·근거·한계'),('기준 적용·판정','요건·자격 판정','판정·적용 근거'),('예측','앞으로의 결과 예상','예상·가정·불확실성'),('조건 안에서 최선 찾기','제약 안에서 선택','유리한 안·절충점'),('결과물 설계','구성·작동 구상','구성·형태·설계'),('내용 재구성','요약·번역·표현 변경','목적에 맞춘 내용'),('결과물 만들기·수정','구현·보완이 필요','완성·수정한 결과물'),('사람과 소통','질문·설명·응대','답변·이해 확인'),('협상·조율','요구·역할이 다름','합의·남은 쟁점'),('기록 입력·수정','기록 반영 필요','실제 반영 기록'),('신청·거래 처리','신청·거래·취소','처리 내역·상태'),('설정·작동 제어','설정·상태 조정','변경 상태·이력'),('게시·배포','공개·제공 필요','공개 판본·범위'),('관찰·측정','새 관찰 값 필요','측정값·관찰 기록'),('실험','조건의 효과 비교','비교 결과·조건'),('시뮬레이션','가정·모의 대응','모의 결과·한계'),('실시간 대화','즉시 대화 필요','소통의 연결·전송'),('시험 환경','별도 시험 조건 필요','실험·모의·시험 조건'),('AI 모델','판단·답변만 필요','판단·생성한 내용')]
    p,_=c.branch_rows('action_',actions,select,'조건이 맞는 재료를 하나 또는 여럿 조합','필요한 가지를 함께 사용 · 결과를 확인한 뒤 다음 재료가 필요하면 다시 선택')
    verify=c.chain('verify',[('보고 주체 확인','누가 맡은 결과인지, 분담·판본·대외 명의 확인'),('결과 검증·재검증','입력·근거·완료 조건과 대조 · 변경되면 영향받은 결과도 확인'),('반대 근거·다시 확인','중요한 판단은 다른 근거·방법으로 반증'),('일하는 과정 평가','각 단계의 방법·절차·권한 사용을 평가'),('결과 품질 평가','사용 목적·기능·정확성·이해·편의를 확인')])
    c.from_point(p,verify[0])
    status=c.q('result_status','검증 결과는?');c.edge(verify[-1],status);c.after(status)
    fix=c.m('fix','업무 절차·실행 계획','새 근거·규칙을 반영해 문제 있는 재료 조합만 수정',cx=335,w=330,kind='back')
    unknown=c.m('unknown','현재 값·상태 확인','외부 작업이 실제로 처리됐는지 조회',cx=1020,w=350,kind='back')
    c.edge(status,fix,label='문제 있음',label_at=(350,c.nodes[fix]['y']-20));c.edge(status,unknown,label='미확인',label_at=(1020,c.nodes[unknown]['y']-20))
    a=c.pt(fix,'l');b=c.pt(safety,'l');c.path([a,(70,a[1]),(70,b[1]),b],fix,safety,label='수정 후 실행 전 조건 재검사',label_at=(310,b[1]+43))
    c.after(fix,unknown)
    uwait=c.m('unknown_wait','대기·후속 관리','기한 안에서 확인 · 상태 확인 전 중복 실행 금지',cx=1020,w=350,kind='back');c.edge(unknown,uwait);c.after(uwait)
    uq=c.q('unknown_q','실제 처리 상태가 확인됐는가?',cx=1020,w=350);c.edge(uwait,uq)
    a=c.pt(uq,'l');b=c.pt(unknown,'l');c.path([a,(770,a[1]),(770,b[1]),b],uq,unknown,label='아직 미확인 · 기한 안',label_at=(640,a[1]-15))
    a=c.pt(uq,'r');b=c.pt(verify[0],'r');c.path([a,(1245,a[1]),(1245,b[1]),b],uq,verify[0],label='예 · 실제 결과를 재검증',label_at=(1110,b[1]-38));c.after(uq)
    uf=c.node('unknown_hold','확인 기한 종료 · 미확인 반환',help='실행 성공으로 보고하지 않음',cx=1020,w=350,kind='stop');c.edge(uq,uf,label='아니오 · 기한 종료',label_at=(1020,c.nodes[uf]['y']-20));c.failures.append(uf);c.after(uf)
    more=c.q('more','이 결과를 사용할 다음 재료가 필요한가?',w=400)
    a=c.pt(status,'b');b=c.pt(more,'t');c.path([a,b],status,more,label='문제없음',label_at=(680,a[1]+130))
    a=c.pt(more,'l');b=c.pt(safety,'l');c.path([a,(70,a[1]),(70,b[1]),b],more,safety,label='예 · 결과를 다음 입력으로',label_at=(320,a[1]+40))
    c.after(more)
    output=c.node('expert_output','담당 작업의 결과·상태 반환',help='결과·근거·판본·완료/미완료·남은 책임',w=470,kind='store')
    c.edge(more,output,label='아니오 · 담당 작업 완료',label_at=(680,c.nodes[output]['y']-24))
    rail=1320
    for f in c.failures:
        a=c.pt(f,'r');c.path([a,(rail,a[1])],f,None,arrow=False)
        c.decor.append(f'<circle cx="{rail}" cy="{a[1]}" r="3.4" fill="#77b7fa"/>')
    c.path([(rail,c.pt(c.failures[0],'r')[1]),(rail,c.pt(output,'r')[1]),c.pt(output,'r')],None,output,label='보류·중단·미확인도 상태를 반환',label_at=(1110,c.pt(output,'r')[1]-25))
    c.after(output,gap=110)
    c.frame('한 전문가가 쓰는 재료 조합' if mode==1 else '총괄·전문가 모두 자기 입력으로 이 조합을 각각 사용',expert_top-57,c.y-35,x=80,w=1285)
    # Per-worker result check and true orchestration merge.
    if mode>1:
        a=c.m('result_a','결과 검증·재검증','A의 결과·근거·판본·처리 상태 확인',cx=680,w=350)
        b=c.m('result_b','결과 검증·재검증','B의 결과·근거·판본·처리 상태 확인',cx=1560,w=300)
        c.edge(output,a);c.edge(other,b,label='B의 독립 실행 결과',label_at=(1560,c.nodes[b]['y']-40));c.after(a,b)
        collect=c.m('collect','나눠 맡기기','총괄이 담당별 결과·상태를 모음\n누락·중복·이견·실패를 구별',w=430)
        c.join((a,b),collect);c.after(collect)
        ready=c.q('ready','필수 결과가 모두 검증됐는가?',w=380);c.edge(collect,ready);c.after(ready)
        pending=c.m('pending','대기·후속 관리','미확인·지연이면 담당 상태 조회와 기한 관리',cx=335,w=330,kind='back')
        c.edge(ready,pending,label='아니오 · 미확인·지연',label_at=(335,c.nodes[pending]['y']-23))
        a=c.pt(pending,'l');b=c.pt(collect,'l');c.path([a,(120,a[1]),(120,b[1]),b],pending,collect,label='조회·답변·기한 도달',label_at=(330,b[1]+40))
        c.after(pending)
        repair=c.m('reassign','대안·전략 판단','이견·실패·누락 또는 기한 종료이면 근거를 비교하고 방법·분담을 조정',cx=1080,w=350,kind='back')
        a=c.pt(ready,'r');b=c.pt(repair,'t');c.path([a,(1080,a[1]),b],ready,repair,label='아니오 · 오류·이견·기한 종료',label_at=(1080,b[1]-22))

        c.after(repair)
        retry=c.q('retry_q','기한·한도 안에서 보완 가능한가?',cx=1080,w=350);c.edge(repair,retry)
        a=c.pt(retry,'r');b=c.pt(dispatch[0],'r');c.path([a,(1745,a[1]),(1745,b[1]),b],retry,dispatch[0],label='예 · 완료분 유지하고 재배정',label_at=(1500,a[1]-15))
        c.after(retry)
        incomplete=c.node('incomplete','미완료·이유·남은 책임을 전달',cx=1080,w=350,kind='stop')
        c.edge(retry,incomplete,label='아니오',label_at=(1080,c.nodes[incomplete]['y']-22));c.after(incomplete)
        nextq=c.q('dependent_q','검증 결과를 받을 후속 작업이 남았는가?',w=410)
        a=c.pt(ready,'b');b=c.pt(nextq,'t');c.path([a,b],ready,nextq,label='예 · 필수 결과 확보',label_at=(680,a[1]+135));c.after(nextq)
        follow=c.m('follow','나눠 맡기기','검증된 선행 결과·근거·판본을 후속 담당의 입력으로 전달',cx=335,w=330)
        c.edge(nextq,follow,label='예 · 선행 결과 준비됨',label_at=(345,c.nodes[follow]['y']-23))
        a=c.pt(follow,'l');b=c.pt(dispatch[0],'l');c.path([a,(35,a[1]),(35,b[1]),b],follow,dispatch[0],label='후속 담당이 자기 재료 조합으로 처리',label_at=(335,c.bottom(follow)+31));c.after(follow)
        last=nextq
        if mode==3:
            change=c.q('cross_change','다른 건에 영향을 주는 변경이 있는가?',w=410)
            a=c.pt(nextq,'r');b=c.pt(change,'t');c.path([a,(1300,a[1]),(1300,b[1]-36),(b[0],b[1]-36),b],nextq,change,label='아니오 · 후속 작업 없음',label_at=(1105,a[1]-15));c.after(change)
            impact=c.chain('impact',[('변경 감시·반영','건 A의 원문·결과 변경이 이를 사용한 건 B에 미치는 영향 확인'),('자료의 시점·버전','옛 결과와 새 결과를 구별해 잘못된 재사용 차단'),('결과 검증·재검증','변경된 결과와 그 결과에 의존한 다른 건을 함께 재검증')],cx=335,w=330,kind='back')
            c.edge(change,impact[0],label='예 · 영향받는 건만',label_at=(335,c.nodes[impact[0]]['y']-20))
            a=c.pt(impact[-1],'l');b=c.pt(dispatch[0],'l');c.path([a,(35,a[1]),(35,b[1]),b],impact[-1],dispatch[0],label='영향 범위 재배정',label_at=(335,c.bottom(impact[-1])+31));last=change
        final=c.m('integration','결과 검증·재검증','총괄이 부분 결과를 결합해 전체 목표·누락·중복·모순을 확인',w=430)
        a=c.pt(last,'r');b=c.pt(final,'r');c.path([a,(1300,a[1]),(1300,b[1]),b],last,final,label='아니오 · 통합할 결과 확보',label_at=(1105,b[1]-25));c.after(final)
    else:final=output
    quality=c.m('whole_quality','결과 품질 평가','전체 결과가 받는 사람의 목적에 맞게 바로 쓰일 수 있는지 확인',w=430);c.edge(final,quality);c.after(quality)
    fq=c.q('final_q','전체 완료 조건과 품질을 충족했는가?',w=420);c.edge(quality,fq);c.after(fq)
    ffix=c.m('final_fix','대안·전략 판단','미달 부분을 기한·한도 안에서 보완할 수 있는지 판단',cx=335,w=330,kind='back');c.edge(fq,ffix,label='아니오',label_at=(335,c.nodes[ffix]['y']-20));c.after(ffix)
    can=c.q('can_fix','보완할 수 있는가?',cx=335,w=330);c.edge(ffix,can)
    target=dispatch[0] if mode>1 else 'context'
    a=c.pt(can,'l');b=c.pt(target,'l');c.path([a,(35,a[1]),(35,b[1]),b],can,target,label='예 · 미달 부분 보완',label_at=(260,c.bottom(can)+31));c.after(can)
    deliver=c.m('deliver','납품 준비','결과·원본·근거·사용법·남은 책임을 갖춤\n미완료면 상태·이유·한계를 명시',w=440)
    c.edge(can,deliver,label='아니오 · 미완료로 전달',label_at=(700,c.nodes[deliver]['y']-26))
    if mode>1:
        a=c.pt(incomplete,'r');b=c.pt(deliver,'r');c.path([a,(1340,a[1]),(1340,b[1]),b],incomplete,deliver,label='미완료 상태로 인계',label_at=(1110,b[1]+35))
    a=c.pt(fq,'r');b=c.pt(deliver,'r');c.path([a,(1180,a[1]),(1180,b[1]),b],fq,deliver,label='예 · 전체 기준 통과',label_at=(1060,a[1]-17));c.after(deliver)
    hand=c.m('handover','전달·인수 확인','수령·사용 조건·남은 책임의 인계를 확인',w=410);c.edge(deliver,hand);c.after(hand)
    receipt=c.q('receipt_q','수령·사용 상태가 확인됐는가?',w=400);c.edge(hand,receipt);c.after(receipt)
    rw=c.m('receipt_wait','대기·후속 관리','수신·사용 문제를 확인하고 기한 안에 재전달·후속 조치',cx=1050,w=350,kind='back');c.edge(receipt,rw,label='아니오 · 응답 대기·전달 문제',label_at=(1040,c.nodes[rw]['y']-23))
    a=c.pt(rw,'r');b=c.pt(hand,'r');c.path([a,(1300,a[1]),(1300,b[1]),b],rw,hand,label='재전달·답변 후 다시 확인',label_at=(1130,b[1]-33));c.after(rw)
    closed=c.m('closed','현재 진행 상태','완료·인수와 미완료·거절·인수 실패를 구별하고 후속 책임 유지',w=440)
    a=c.pt(receipt,'l');b=c.pt(closed,'l');c.path([a,(185,a[1]),(185,b[1]),b],receipt,closed,label='예 · 확인됨',label_at=(320,a[1]+42))
    c.edge(rw,closed,label='거절·기한 종료',label_at=(980,c.nodes[closed]['y']-20));c.after(closed)
    # Learning is last and follows observed results, including failures.
    top=c.section('결과에서 학습 · 검증된 개선만 다음 업무에 적용')
    perf=c.m('performance','성과 추적','약속한 시점의 실제 성과·후속 문제를 확인',w=410);c.edge(closed,perf);c.after(perf)
    memory=c.m('learn_memory','장기 기억','판단·실행·평가 기록과 성과 중 재사용할 결정·약속·교훈을 보관·정정',w=430);c.edge(perf,memory);c.after(memory)
    causeq=c.q('cause_q','재사용할 성과·분석할 문제가 있는가?',w=420);c.edge(memory,causeq);c.after(causeq)
    cause=c.m('cause','성공·실패 원인 분석','재사용할 성과·원인 불명·영향이 큰 문제·반복 오류의 원인과 적용 조건 분석',cx=1020,w=350);c.edge(causeq,cause,label='예',label_at=(1020,c.nodes[cause]['y']-22));c.after(cause)
    iq=c.q('improve_q','개선할 점·새로 필요한 능력이 있는가?',w=420);c.edge(cause,iq)
    a=c.pt(causeq,'l');b=c.pt(iq,'t');c.path([a,(185,a[1]),(185,b[1]-36),(680,b[1]-36),b],causeq,iq,label='아니오',label_at=(320,a[1]+42));c.after(iq)
    imp=c.m('improve','능력 개선·확장','지식·판단 요령·방법·도구를 보완',cx=1020,w=350);c.edge(iq,imp,label='예',label_at=(1020,c.nodes[imp]['y']-22));c.after(imp)
    ie=c.m('improve_env','시험 환경','별도 공간·조건이 필요하면 준비 · 미통과 판본의 실제 투입 차단',cx=1020,w=350);c.edge(imp,ie,label='별도 환경 필요',label_at=(1020,c.nodes[ie]['y']-22));c.after(ie)
    it=c.m('improve_test','업무 능력 시험','개선 효과와 기존 능력을 함께 시험',cx=1020,w=350);c.edge(ie,it)
    a=c.pt(imp,'r');b=c.pt(it,'r');c.path([a,(1245,a[1]),(1245,b[1]),b],imp,it,label='별도 환경 불필요',label_at=(1110,c.bottom(it)+33));c.after(it)
    ip=c.q('improve_pass','개선 효과·기존 능력 모두 통과했는가?',cx=1020,w=350);c.edge(it,ip);c.after(ip)
    adopt=c.m('adopt','업무 지식','검증된 내용과 적용 조건을 반영',cx=1020,w=350);c.edge(ip,adopt,label='예',label_at=(1020,c.nodes[adopt]['y']-22));c.after(adopt)
    am=c.m('adopt_memory','장기 기억','검증 근거·판본·교훈을 다음 판단에 제공',cx=1020,w=350);c.edge(adopt,am);c.after(am)
    finish=c.node('finish','이번 처리를 마침',help='남은 책임은 계속 관리\n후속 신호가 오면 해당 건을 이어서 처리',shape='terminal',kind='good',w=460)
    c.edge(am,finish)
    a=c.pt(ip,'r');b=c.pt(finish,'r');c.path([a,(1245,a[1]),(1245,b[1]),b],ip,finish,label='아니오 · 기존 검증본 유지',label_at=(1110,b[1]-27))
    a=c.pt(iq,'l');b=c.pt(finish,'l');c.path([a,(185,a[1]),(185,b[1]),b],iq,finish,label='아니오 · 개선 생략',label_at=(310,a[1]+42));c.after(finish,gap=45)
    c.frame('결과에서 학습 · 검증된 개선만 다음 업무에 적용',top,c.y)
    return c

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'docs/images/expert-definition');args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    print(json.dumps([build(mode).save(args.out) for mode in (1,2,3)],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
