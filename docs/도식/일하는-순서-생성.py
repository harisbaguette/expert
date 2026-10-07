#!/usr/bin/env python3
"""정의 1 「전문 판단의 신뢰성」 절의 「일하는 순서」 순서도를 그린다.

Mermaid dagre 로는 「뒷받침하지 않음」 되돌아가는 선이 「개념에 없는 관계·규칙」 선을 가로지르는 자리를
없앨 수 없어서(간선 선언 순서 수천 가지를 돌려 봄) 좌표를 직접 잡는다.
- 줄기는 위에서 아래로 한 줄. 되묻기는 왼쪽, 빈 곳 채우기는 오른쪽, 되돌아가는 선은 바깥 여백으로 돌린다.
- 색·도형은 문서 안 다른 Mermaid 순서도(main·stop·back·store·good·note)와 같다.
- 그리고 나서 선끼리 교차, 선이 상자를 뚫는 곳, 이름표 겹침을 스스로 센다. 하나라도 있으면 실패로 끝낸다.

사용법: python3 일하는-순서-생성.py [출력 폴더]   (기본: docs/images/expert-definition)
"""
import math
import os
import sys
from PIL import ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "images", "expert-definition")
NAME = "judgment-work-order"
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FS = 15  # 글자 크기
LH = 23  # 줄 간격
_font = ImageFont.truetype(FONT_PATH, FS, index=0)
_font_lab = ImageFont.truetype(FONT_PATH, 14, index=0)

COLORS = {
    "main": ("#dbeafe", "#7dabe8", "#17314f"),
    "stop": ("#fee2e2", "#f0a3a3", "#7f1d1d"),
    "back": ("#ffedd5", "#f3b183", "#7c2d12"),
    "store": ("#e5e7eb", "#b0b6bf", "#1f2937"),
    "good": ("#dcfce7", "#86d3a3", "#14532d"),
    "note": ("#fef9c3", "#e2c95f", "#713f12"),
}


def tw(s, f=_font):
    return f.getlength(s)


class Node:
    def __init__(self, nid, shape, cls, lines, cx=0, cy=0, minw=0, padx=22, pady=14):
        self.id, self.shape, self.cls, self.lines = nid, shape, cls, lines
        self.padx, self.pady = padx, pady
        self.cx, self.cy = cx, cy
        textw = max(tw(ln) for ln in lines)
        self.slant = 30 if shape == "hex" else 0
        self.w = max(minw, textw + 2 * padx + 2 * self.slant)
        self.h = len(lines) * LH + 2 * pady + (14 if shape == "cyl" else 0)

    @property
    def x(self): return self.cx - self.w / 2
    @property
    def y(self): return self.cy - self.h / 2
    def top(self, dx=0): return (self.cx + dx, self.y)
    def bottom(self, dx=0): return (self.cx + dx, self.y + self.h)
    def left(self, dy=0): return (self.x, self.cy + dy)
    def right(self, dy=0): return (self.x + self.w, self.cy + dy)

    def svg(self):
        f, s, t = COLORS[self.cls]
        x, y, w, h = self.x, self.y, self.w, self.h
        shp = ""
        if self.shape == "rect":
            shp = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{f}" stroke="{s}" stroke-width="1.6"/>'
        elif self.shape == "cap":
            r = min(h / 2, 36)
            shp = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{f}" stroke="{s}" stroke-width="1.6"/>'
        elif self.shape == "hex":
            m = self.slant
            pts = [(x + m, y), (x + w - m, y), (x + w, y + h / 2), (x + w - m, y + h), (x + m, y + h), (x, y + h / 2)]
            shp = '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (" ".join(f"{a:.1f},{b:.1f}" for a, b in pts), f, s)
        elif self.shape == "cyl":
            ry = 9
            shp = (f'<path d="M{x:.1f},{y + ry:.1f} A{w / 2:.1f},{ry} 0 0 1 {x + w:.1f},{y + ry:.1f} L{x + w:.1f},{y + h - ry:.1f} '
                   f'A{w / 2:.1f},{ry} 0 0 1 {x:.1f},{y + h - ry:.1f} Z" fill="{f}" stroke="{s}" stroke-width="1.6"/>'
                   f'<path d="M{x:.1f},{y + ry:.1f} A{w / 2:.1f},{ry} 0 0 0 {x + w:.1f},{y + ry:.1f}" fill="none" stroke="{s}" stroke-width="1.6"/>')
        off = 7 if self.shape == "cyl" else 0
        n = len(self.lines)
        y0 = self.cy + off - (n - 1) * LH / 2
        txt = "".join(
            f'<text x="{self.cx:.1f}" y="{y0 + i * LH:.1f}" text-anchor="middle" dominant-baseline="central" fill="{t}" font-size="{FS}">{esc(ln)}</text>'
            for i, ln in enumerate(self.lines))
        return f'<g id="{self.id}">{shp}{txt}</g>'

    def bbox(self, pad=0):
        return (self.x - pad, self.y - pad, self.x + self.w + pad, self.y + self.h + pad)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ───────────────────────── 상자 ─────────────────────────
N = {}


def add(*a, **k):
    n = Node(*a, **k)
    N[n.id] = n
    return n


CX = 640
add("Q", "cap", "good", ["맡긴 업무 · 판단할 물음"], CX, 0, padx=20, pady=10)
add("P", "rect", "main", ["① 물음 파악 (부품: 개념 · 관계)", "물음의 말을 개념 번호로 바꾸고", "전제가 개념·관계와 맞는지 본다"], CX, 0)
add("dP", "hex", "note", ["전제가 맞고 뜻이 하나인가"], CX, 0, pady=12)
add("T", "rect", "main", ["② 대상 확정 (부품: 개념 · 규칙)", "대상 번호를 하나로 정하고", "상위 개념과 규칙으로 종류를 정한다"], CX, 0)
add("dT", "hex", "note", ["후보 중 하나로 정해지나"], CX, 0, pady=12)
add("R", "rect", "main", ["③ 권한 거르기 (부품: 권한)", "이번 판단에 쓸 수 있는 자료의 범위를 정한다",
                          "모든 단계에서 자료를 찾거나 쓰기 전에 권한을 확인한다"], CX, 0)
add("D", "rect", "main", ["④ 자료 모으기 (부품: 개념 · 관계 · 규칙 · 출처)", "기준 시점에 효력이 있는 판본만 모으고 출처 등급을 단다",
                          "부딪치면 ‘앞선다’ 관계를 따라 고르고,", "점검 목록마다 필요한 증거가 찼는지 본다", "자료 자체가 없는 빈 곳은 표시해 넘긴다"], CX, 0)
add("dD", "hex", "note", ["자료를 모으다 막힌 곳이 있나"], CX, 0, pady=12)
add("I", "rect", "main", ["⑤ 전문 판단 (부품: 관계 · 규칙)", "관계를 따라 사실을 잇고 전문 지식과 조건·예외를 적용한다",
                          "조건·예외가 조문에 정해진 계산은 규칙 엔진이 한다", "반대 근거와 갈리는 해석을 검토해 결론과 처리 방향을 정한다"], CX, 0)
add("dI", "hex", "note", ["판단하다 막힌 곳이 있나"], CX, 0, pady=12)
add("C", "hex", "note", ["⑥ 판단 검사 (부품: 출처 · 권한)", "쓴 자료의 권한을 다시 확인하고 직접 사실은 원문과 대조한다",
                         "계산·규칙 결론은 입력의 출처와 도출 과정을 확인한다", "조건·예외의 적용과 추론이 결론을 뒷받침하나"], CX, 0)
add("A", "cap", "good", ["검증한 전문 판단", "결론 · 적용 조건 · 근거 · 처리 방향",
                         "미확인 사항과 판단 범위를 밝히고,", "뒷받침할 수 없는 결론은 내지 않는다"], CX, 0)
add("ASK", "rect", "stop", ["틀린 전제는 바로잡고", "전제·뜻·대상을 확인할 수 없으면", "맡긴 사람에게 되묻는다"], 140, 0)
add("DEC", "rect", "stop", ["대안마다 ⑤ 판단·⑥ 검사를 마친다", "근거와 대안을 붙여", "사람에게 결정을 요청한다"], 0, 0)
add("GAP", "rect", "back", ["빈 곳 채우기", "업무 지식이 개념·관계를 보태고 사람이 승인한다", "승인 전에는 빈 곳을 밝혀 답하거나 삼간다"], 0, 0)
add("ONT", "cyl", "store", ["판단의 공통 기준", "개념 · 관계 · 규칙 · 출처 · 권한"], 0, 0)
add("dO", "hex", "note", ["대상·범위가 바뀌었나"], 0, 0, pady=12)

# 줄기: 위에서 아래로 일정한 간격으로 쌓는다.
SPINE = ["Q", "P", "dP", "T", "dT", "R", "D", "dD", "I", "dI", "C", "A"]
GAPY = 58
yy = 20
for k, nid in enumerate(SPINE):
    n = N[nid]
    n.cy = yy + n.h / 2
    yy += n.h + GAPY

# 오른쪽 상자는 줄기 오른쪽 끝에서 간격을 두고 놓는다.
spine_right = max(N[k].x + N[k].w for k in SPINE)
RIGHT_X0 = spine_right + 120
N["GAP"].cx = RIGHT_X0 + N["GAP"].w / 2
N["GAP"].cy = N["dI"].cy
N["ONT"].cx = N["GAP"].cx
N["ONT"].cy = N["GAP"].cy + N["GAP"].h / 2 + 62 + N["ONT"].h / 2
N["dO"].cx = N["GAP"].cx
N["dO"].cy = N["ONT"].cy + N["ONT"].h / 2 + 58 + N["dO"].h / 2
# 왼쪽 상자: 첫 판단 옆, 결정 요청은 ⑤ 옆
N["DEC"].cy = N["I"].cy
N["DEC"].cx = 40 + N["DEC"].w / 2
N["ASK"].cy = N["dP"].cy
N["ASK"].cx = 30 + N["ASK"].w / 2

# ───────────────────────── 선 ─────────────────────────
E = []  # dict(id, pts, label(lines), at)


def edge(eid, pts, label=None, at=None, dash=False, color="#333"):
    E.append(dict(id=eid, pts=pts, label=label, at=at, dash=dash, color=color))


q, p, dp, t, dt, r, d, dd, i, di, c, a, ask, dec, gap, ont, do = (N[k] for k in (
    "Q", "P", "dP", "T", "dT", "R", "D", "dD", "I", "dI", "C", "A", "ASK", "DEC", "GAP", "ONT", "dO"))


def beside(node_a, node_b, dx=50):
    """세로선 옆에 이름표를 둔다."""
    return ("pt", (node_a.cx + dx, (node_a.bottom()[1] + node_b.top()[1]) / 2))


# 줄기(곧은 세로선)
edge("Q-P", [q.bottom(), p.top()])
edge("P-dP", [p.bottom(), dp.top()])
edge("dP-T", [dp.bottom(), t.top()], label=["맞고 하나임"], at=beside(dp, t, 58))
edge("T-dT", [t.bottom(), dt.top()])
edge("dT-R", [dt.bottom(), r.top()], label=["정해짐"], at=beside(dt, r, 40))
edge("R-D", [r.bottom(), d.top()])
edge("D-dD", [d.bottom(), dd.top()])
edge("dD-I", [dd.bottom(), i.top()], label=["막힘 없음"], at=beside(dd, i, 44))
edge("I-dI", [i.bottom(), di.top()])
edge("dI-C", [di.bottom(), c.top()], label=["막힘 없음"], at=beside(di, c, 44))
edge("C-A", [c.bottom(), a.top()], label=["뒷받침함"], at=beside(c, a, 46))

# 되묻기(왼쪽): 두 판단의 왼쪽 꼭짓점에서 나간다
edge("dP-ASK", [dp.left(), ask.right()], label=["전제 틀림·미확인", "뜻이 갈림"], at=("pt", ((dp.left()[0] + ask.right()[0]) / 2, dp.cy)))
edge("dT-ASK", [dt.left(), (ask.cx + 40, dt.cy), ask.bottom(40)], label=["후보가 갈리지 않음"], at=("pt", ((dt.left()[0] + ask.cx + 40) / 2 + 20, dt.cy)))
edge("ASK-P", [ask.top(-40), (ask.cx - 40, p.left(-30)[1]), p.left(-30)])

# 빈 곳 채우기(오른쪽)
edge("dD-GAP", [dd.right(), (gap.cx, dd.cy), gap.top()], label=["개념·관계가 비는", "점검 항목"], at=("pt", (dd.right()[0] + 110, dd.cy)))
edge("dI-GAP", [di.right(), gap.left()], label=["개념에 없는", "관계·규칙"], at=("pt", ((di.right()[0] + gap.left()[0]) / 2, di.cy)))

# 결정 요청(왼쪽): 정할 수 없는 충돌은 대안별 판단·검사를 마쳐 넘기고, 결정을 받으면 전문 판단으로 돌아간다.
edge("dD-DEC", [dd.left(), (dec.cx, dd.cy), dec.top()], label=["정할 수 없는 충돌"], at=("pt", ((dd.left()[0] + dec.cx) / 2 + 30, dd.cy)))
edge("dI-DEC", [di.left(), (dec.cx, di.cy), dec.bottom()], label=["정할 수 없는 충돌"], at=("pt", ((di.left()[0] + dec.cx) / 2 + 30, di.cy)))
edge("DEC-I", [dec.right(), i.left()], label=["결정을 받음"], at=("pt", ((dec.right()[0] + i.left()[0]) / 2, i.cy)))
edge("GAP-ONT", [gap.bottom(), ont.top()])
edge("ONT-dO", [ont.bottom(), do.top()])

# 되돌아감(오른쪽 바깥 여백): 안쪽 줄은 자료 모으기로, 바깥 줄은 물음 파악으로
lane_d = max(gap.x + gap.w, ont.x + ont.w, do.x + do.w) + 46
lane_p = lane_d + 46
bottom_y = do.bottom()[1] + 42
edge("dO-D", [do.right(), (lane_d, do.cy), (lane_d, d.right(-40)[1]), d.right(-40)],
     label=["유지", "관련 자료 재확인"], at=("pt", ((d.right(-40)[0] + lane_d) / 2 + 40, d.right(-40)[1])))
edge("dO-P", [do.bottom(0), (do.cx, bottom_y), (lane_p, bottom_y), (lane_p, p.right()[1]), p.right()],
     label=["바뀜"], at=("pt", ((p.right()[0] + lane_p) / 2 + 40, p.right()[1])))
# 판단 검사 → 자료 모으기 (왼쪽 바깥 여백)
lane_c = 22
edge("C-D", [c.left(), (lane_c, c.cy), (lane_c, d.left()[1]), d.left()], label=["뒷받침하지 않음", "판단 못 함"], at=("pt", ((lane_c + c.left()[0]) / 2, c.cy)))

# ───────────────────────── 선 그리기 ─────────────────────────
R = 26  # 모서리 둥글기


def rounded(pts, r=R):
    """꺾이는 자리를 둥글게 깎은 꺾은선 → (SVG path, 촘촘히 뽑은 점)"""
    d_ = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    samples = [pts[0]]
    cur = pts[0]
    for k in range(1, len(pts) - 1):
        p0, p1, p2 = cur, pts[k], pts[k + 1]
        v1 = (p1[0] - p0[0], p1[1] - p0[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        rr = min(r, l1 / 2, l2 / 2)
        a_ = (p1[0] - v1[0] / l1 * rr, p1[1] - v1[1] / l1 * rr)
        b_ = (p1[0] + v2[0] / l2 * rr, p1[1] + v2[1] / l2 * rr)
        d_.append(f"L{a_[0]:.1f},{a_[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {b_[0]:.1f},{b_[1]:.1f}")
        samples.append(a_)
        for s in range(1, 8):
            u = s / 8
            samples.append(((1 - u) ** 2 * a_[0] + 2 * u * (1 - u) * p1[0] + u * u * b_[0],
                            (1 - u) ** 2 * a_[1] + 2 * u * (1 - u) * p1[1] + u * u * b_[1]))
        samples.append(b_)
        cur = b_
    d_.append(f"L{pts[-1][0]:.1f},{pts[-1][1]:.1f}")
    samples.append(pts[-1])
    return " ".join(d_), samples


def seg_point(pts, at):
    kind, v = at
    if kind == "pt":
        return v
    # mid: 첫 선분 가운데(오프셋 v)
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    return ((x1 + x2) / 2, (y1 + y2) / 2 + v)


labels = []
paths = []
for e in E:
    dpath, samples = rounded(e["pts"])
    e["samples"] = samples
    paths.append(dpath)
    if e["label"]:
        cx_, cy_ = seg_point(e["pts"], e["at"])
        wl = max(tw(ln, _font_lab) for ln in e["label"]) + 12
        hl = len(e["label"]) * 18 + 6
        labels.append(dict(id=e["id"], lines=e["label"], x=cx_ - wl / 2, y=cy_ - hl / 2, w=wl, h=hl))

# ───────────────────────── 검사 ─────────────────────────
def orient(a, b, c_):
    return (b[0] - a[0]) * (c_[1] - a[1]) - (b[1] - a[1]) * (c_[0] - a[0])


def seg_cross(a, b, c_, d_):
    return orient(a, b, c_) * orient(a, b, d_) < 0 and orient(c_, d_, a) * orient(c_, d_, b) < 0


def inside(pt, bb, m=0):
    return bb[0] + m < pt[0] < bb[2] - m and bb[1] + m < pt[1] < bb[3] - m


problems = []
for x in range(len(E)):
    for y in range(x + 1, len(E)):
        sa, sb = E[x]["samples"], E[y]["samples"]
        for k in range(len(sa) - 1):
            hit = False
            for m in range(len(sb) - 1):
                if seg_cross(sa[k], sa[k + 1], sb[m], sb[m + 1]):
                    problems.append(f"선 교차: {E[x]['id']} × {E[y]['id']} @ {sa[k][0]:.0f},{sa[k][1]:.0f}")
                    hit = True
                    break
            if hit:
                break
ends = {e["id"]: e["id"].split("-") for e in E}
for e in E:
    a_id, b_id = e["id"].split("-")
    for nid, n in N.items():
        bb = n.bbox()
        cnt = sum(1 for s in e["samples"] if inside(s, bb, 2))
        if cnt and nid not in (a_id, b_id):
            problems.append(f"선이 상자를 지남: {e['id']} → {nid}")
# 선이 제 상자 안으로 파고들지 않는지(끝점 근처 몇 개는 허용)
for e in E:
    for nid in e["id"].split("-"):
        bb = N[nid].bbox()
        cnt = sum(1 for s in e["samples"][1:-1] if inside(s, bb, 3))
        if cnt > 0 and N[nid].shape != "hex":
            problems.append(f"선이 제 상자를 뚫음: {e['id']} → {nid} ({cnt})")
for L in labels:
    bb = (L["x"], L["y"], L["x"] + L["w"], L["y"] + L["h"])
    for nid, n in N.items():
        b2 = n.bbox()
        if bb[0] < b2[2] and bb[2] > b2[0] and bb[1] < b2[3] and bb[3] > b2[1]:
            problems.append(f"이름표가 상자와 겹침: {L['id']} × {nid}")
    for e in E:
        if e["id"] == L["id"]:
            continue
        for k in range(len(e["samples"]) - 1):
            s1, s2 = e["samples"][k], e["samples"][k + 1]
            for corner in [(bb[0], bb[1], bb[2], bb[1]), (bb[2], bb[1], bb[2], bb[3]), (bb[2], bb[3], bb[0], bb[3]), (bb[0], bb[3], bb[0], bb[1])]:
                if seg_cross(s1, s2, (corner[0], corner[1]), (corner[2], corner[3])):
                    problems.append(f"이름표가 다른 선과 겹침: {L['id']} × {e['id']}")
                    break
            else:
                if inside(s1, bb):
                    problems.append(f"이름표가 다른 선과 겹침: {L['id']} × {e['id']}")
                    break
                continue
            break
for k, L1 in enumerate(labels):
    for L2 in labels[k + 1:]:
        if L1["x"] < L2["x"] + L2["w"] and L1["x"] + L1["w"] > L2["x"] and L1["y"] < L2["y"] + L2["h"] and L1["y"] + L1["h"] > L2["y"]:
            problems.append(f"이름표끼리 겹침: {L1['id']} × {L2['id']}")

# ───────────────────────── SVG ─────────────────────────
allx = [n.x for n in N.values()] + [n.x + n.w for n in N.values()] + [s[0] for e in E for s in e["samples"]]
ally = [n.y for n in N.values()] + [n.y + n.h for n in N.values()] + [s[1] for e in E for s in e["samples"]]
MARG = 20
minx, maxx, miny, maxy = min(allx) - MARG, max(allx) + MARG, min(ally) - MARG, max(ally) + MARG
W, H = maxx - minx, maxy - miny

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="{minx:.1f} {miny:.1f} {W:.1f} {H:.1f}" role="img" '
       f'font-family="\'Apple SD Gothic Neo\',\'Noto Sans KR\',\'Malgun Gothic\',sans-serif">',
       '<title>일하는 순서 여섯 단계: 물음 파악, 대상 확정, 권한 거르기, 자료 모으기, 전문 판단, 판단 검사</title>',
       f'<rect x="{minx:.1f}" y="{miny:.1f}" width="{W:.1f}" height="{H:.1f}" fill="white"/>',
       '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
       '<path d="M0,0 L10,5 L0,10 Z" fill="#333"/></marker></defs>']
for e, dpath in zip(E, paths):
    svg.append(f'<path id="e-{e["id"]}" d="{dpath}" fill="none" stroke="{e["color"]}" stroke-width="1.6" marker-end="url(#ar)"/>')
for n in N.values():
    svg.append(n.svg())
for L in labels:
    svg.append(f'<rect x="{L["x"]:.1f}" y="{L["y"]:.1f}" width="{L["w"]:.1f}" height="{L["h"]:.1f}" fill="#ececec" fill-opacity="0.92" rx="2"/>')
    for k, ln in enumerate(L["lines"]):
        svg.append(f'<text x="{L["x"] + L["w"] / 2:.1f}" y="{L["y"] + 3 + 9 + k * 18:.1f}" text-anchor="middle" dominant-baseline="central" fill="#333" font-size="14">{esc(ln)}</text>')
svg.append("</svg>")

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, NAME + ".svg"), "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print(f"크기 {W:.0f}×{H:.0f}  상자 {len(N)}  선 {len(E)}  이름표 {len(labels)}")
if problems:
    print("문제:")
    for pr in problems:
        print(" -", pr)
    sys.exit(1)
print("교차 0 · 상자 뚫음 0 · 이름표 겹침 0")
