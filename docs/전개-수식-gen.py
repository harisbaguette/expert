# Generates 전개-수식.svg — 수식을 그림 한 장으로. 문서에는 이 그림만 두고 범례도 해설도 붙이지
# 않으므로, 그림만 보고 다 읽혀야 한다.
#   항 6개는 × 로, 항 안의 계통과 재료는 + 로 이어진다. 네 밴드로 눕혀 × 다섯 개가 한 축에 선다.
#   필수 재료는 채운 칩, 필요한 경우에만 쓰는 재료는 흰 바탕 점선 칩으로 따로 담는다.
#   규칙·권한의 우선순위는 계단으로, 실무의 순서는 화살표꼴 칩으로 그려 기호 설명이 필요 없게 했다.
# Run: python3 "docs/전개-수식-gen.py"  (then check the render before committing)

FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

INK = "#16202b"          # 가장 진한 글자
SUB = "#55677a"          # 보조 글자
HEAD_BG = "#1d2b38"      # 항 머리띠
TERM_BG = "#dde6ee"      # 항 몸통 — 계통 카드(흰색)와 명도를 벌린다
TERM_EDGE = "#a7b9c8"
SYS_BG = "#ffffff"       # 계통 상자
SYS_EDGE = "#c3d0db"
CHIP_BG = "#d5e2ec"      # 필수 재료
CHIP_EDGE = "#6d8194"
COND_BG = "#dde7ef"      # 필요한 경우 칸 바닥
COND_EDGE = "#8fa0b0"    # 필요한 경우 재료 (점선 = 빈칸으로 둘 수 있다는 뜻)
COND_TXT = "#5b6c7c"
TITLE_BG = "#eef3f8"

FS = 19                  # 재료 글자
PAD = 26                 # 재료 칩 좌우 여백
BH = 38                  # 재료 칩 높이
GAP = 9                  # 재료 사이
OP_W = 22                # + 기호 칸
LINEH = 46               # 재료 줄 간격
STEP = 75                # 우선순위 계단 한 칸
NOTCH = 11               # 흐름 칩 화살촉 깊이
SMALL = 17               # 그림 안 최소 글자

MARGIN = 40
TITLE_H = 64             # 맨 위 수식 띠
TITLE_FS = 34
COLGAP = 46              # 밴드 안 두 카드 사이 (× 자리)
BANDGAP = 62             # 밴드와 밴드 사이 (× 자리)
TPAD = 20                # 항 상자 안 여백
HDR = 54                 # 항 머리띠 높이
SPAD = 20                # 계통 상자 안 여백
SLBL = 32                # 계통 이름 줄
SYS_GAP = 42             # 계통과 계통 사이 (+ 자리)
CTOP = 12                # 필요한 경우 칸 위
CLBL = 26                # 필요한 경우 이름 줄
CBOT = 12

W = 1446
FULL_W = W - 2 * MARGIN              # 전폭 카드
HALF_W = (FULL_W - COLGAP) // 2      # 두 장 나란한 밴드의 카드


def tw(s, fs=FS):
    """글자 폭 어림 — 한글은 한 칸, 중점은 반 칸, 공백은 얇게, 영문은 0.55."""
    w = 0.0
    for ch in s:
        if ch == "·":
            w += fs * 0.5
        elif ch == " ":
            w += fs * 0.35
        elif ord(ch) > 0x2000:
            w += fs * 1.0
        else:
            w += fs * 0.55
    return w


def bw(s):
    return round(tw(s) + PAD, 1)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── 전개 내용.  ("m", 이름, 필수?) 재료 · ("o", 기호) 연산자 · ("[", None)/("]", None) 우선순위 괄호
def M(n):
    return ("m", n, True)


def C(n):
    return ("m", n, False)


PLUS = ("o", "+")
ARROW = ("o", "→")
GT = ("o", ">")

TERMS = {
    "환경": [("", [
        [M("모델"), PLUS, M("실행 순환"), PLUS, M("저장·이어받기"), PLUS, M("나눠 맡기기"), PLUS, M("작업창"),
         PLUS, M("시작 신호"), PLUS, M("자료 읽기"), PLUS, M("도구"), PLUS, M("시험 환경")],
        [PLUS, C("실시간 통로"), PLUS, C("문서·그림 만들기")],
    ])],
    "지식": [
        ("자료·검색", [
            [M("법규·기준"), PLUS, M("해석 자료"), PLUS, M("일반 자료"), PLUS, M("고객·회사 정보"),
             PLUS, M("출처·시점·판본"), PLUS, M("검색"), PLUS, M("자동 갱신")],
            [PLUS, C("플랫폼·기관 규정"), PLUS, C("현황 자료")],
        ]),
        ("지식·경험", [
            [M("업무 지식"), PLUS, M("감각·사례·암묵지")],
            [PLUS, C("정체성·작풍")],
        ]),
        ("기억·상태", [
            [M("장기 기억"), PLUS, M("작업 기억")],
        ]),
    ],
    "규칙": [
        ("규칙·권한", [
            [("[", None), M("절대 원칙"), GT, M("직업 규칙"), GT, C("계약·플랫폼 규칙"), GT, C("회사 규칙"),
             GT, M("개인 취향"), ("]", None)],
            [PLUS, M("권한·명의·위임"), PLUS, M("안전장치"), PLUS, M("책임·손실 한도")],
        ]),
        ("행동 체계", [
            [M("판단 규칙"), PLUS, M("업무 절차·노하우"), PLUS, M("완료 조건"), PLUS, M("먼저 감지하기"),
             PLUS, M("사람에게 넘기기"), PLUS, M("보고·결과물")],
            [PLUS, C("상대 응대")],
        ]),
    ],
    "실무": [("업무 처리 흐름", [
        [M("감지·접수"), ARROW, M("의도 파악"), ARROW, M("문제 정의"), ARROW, M("자료 확인"),
         ARROW, M("판단·계획"), ARROW, M("처리"), ARROW, M("검증"), ARROW, M("완료·보고"), ARROW, M("남기기")],
    ])],
    "검증": [("검증·평가", [
        [M("결과 검증·수정"), PLUS, M("반증·교차 검증"), PLUS, M("위험 누락 검사"),
         PLUS, M("과정 평가"), PLUS, M("결과물 평가"), PLUS, M("근거 추적·재현")],
    ])],
    "학습": [("학습·개선", [
        [M("실패 원인 분석"), PLUS, M("고정 시험"), PLUS, M("자동 학습"), PLUS, M("성과 추적")],
    ])],
}

# 네 밴드. 한 밴드에 두 장이면 반폭으로 나란히 놓고 그 사이가 × 자리다.
BANDS = [["환경"], ["지식", "규칙"], ["실무"], ["검증", "학습"]]
ORDER = [n for band in BANDS for n in band]

out = []


# ── 계통 하나를 네 덩이로 가른다 ─────────────────────────────────────────
def segments(rows):
    """chain (우선순위 계단) · chev (흐름 칩) · plus (보통 재료) · cond (필요한 경우)"""
    chain, chev, plus, cond = [], [], [], []
    for r in rows:
        mats = [t for t in r if t[0] == "m"]
        if mats and all(not t[2] for t in mats):
            cond += r
        elif any(t[0] in ("[", "]") for t in r):
            chain += mats
        elif any(t[0] == "o" and t[1] == "→" for t in r):
            chev += mats
        else:
            plus += r
    for grp in (plus, cond):
        while grp and grp[0][0] == "o":
            grp.pop(0)
    return chain, chev, plus, cond


def unit_w(u):
    return sum(bw(t[1]) + GAP if t[0] == "m" else OP_W + GAP for t in u)


def units(tokens):
    """[연산자, 재료] 를 한 묶음으로 — 연산자는 줄 끝이 아니라 다음 줄 머리로 간다."""
    us, i = [], 0
    while i < len(tokens):
        if tokens[i][0] == "o" and i + 1 < len(tokens) and tokens[i + 1][0] == "m":
            us.append([tokens[i], tokens[i + 1]])
            i += 2
        else:
            us.append([tokens[i]])
            i += 1
    return us


def wrap(us, maxw):
    lines, cur, w = [], [], 0.0
    for u in us:
        uw = unit_w(u)
        if cur and w + uw > maxw:
            lines.append(cur)
            cur, w = [], 0.0
        cur += u
        w += uw
    if cur:
        lines.append(cur)
    return lines


def flow(tokens, maxw):
    """줄 수를 먼저 정하고, 그 줄 수를 지키는 가장 좁은 폭으로 다시 흘린다.
    줄끼리 길이가 고르게 되고 마지막 줄에 칩 하나만 남는 일이 없어진다."""
    us = units(tokens)
    if not us:
        return []
    n = len(wrap(us, maxw))
    if n <= 1:
        return wrap(us, maxw)
    best = wrap(us, maxw)
    lo = max(unit_w(u) for u in us)
    for target in range(int(maxw), int(lo) - 1, -8):
        cand = wrap(us, target)
        if len(cand) != n:
            break
        best = cand
    return best


def flow_chev(chips, maxw):
    """흐름 칩은 서로 맞물려 붙는다. 칩 하나가 밀어내는 폭은 칩 폭에서 물린 깊이를 뺀 만큼."""
    lines, cur, w = [], [], 0.0
    for c in chips:
        adv = bw(c[1]) + NOTCH * 0.6 - NOTCH
        if cur and w + adv + NOTCH > maxw:
            lines.append(cur)
            cur, w = [], 0.0
        cur.append(c)
        w += adv
    if cur:
        lines.append(cur)
    return lines


def stack_h(n):
    return n * BH + (n - 1) * (LINEH - BH) if n else 0


def cond_w(lines):
    return max(sum(bw(t[1]) + GAP if t[0] == "m" else OP_W + GAP for t in ln) for ln in lines) + 28


def plan_sys(sysname, rows, body_w):
    inner = body_w - 2 * SPAD
    chain, chev, plus, cond = segments(rows)
    pl = flow(plus, inner)
    cl = flow(cond, inner - 28) if cond else []
    vl = flow_chev(chev, inner) if chev else []
    h = SPAD + (SLBL if sysname else 0)
    if chain:
        h += len(chain) * (BH + 7) - 7 + (24 if pl else 6)
    if vl:
        h += stack_h(len(vl)) + (14 if pl else 0)
    if pl:
        h += stack_h(len(pl))
    if cl:
        h += CTOP + CLBL + stack_h(len(cl)) + CBOT
    h += SPAD
    return {"name": sysname, "chain": chain, "chev": vl, "plus": pl, "cond": cl, "h": h}


def plan_term(name, body_w):
    sysp = [plan_sys(sn, rows, body_w) for sn, rows in TERMS[name]]
    h = HDR + TPAD + sum(p["h"] for p in sysp) + (len(sysp) - 1) * SYS_GAP + TPAD
    return {"name": name, "sys": sysp, "h": h, "body_w": body_w}


# ── 자리 잡기 ────────────────────────────────────────────────────────────
cards, bands = {}, []
y = MARGIN + TITLE_H + BANDGAP
for band in BANDS:
    tw_ = FULL_W if len(band) == 1 else HALF_W
    ps = [plan_term(n, tw_ - 2 * TPAD) for n in band]
    bh = max(p["h"] for p in ps)
    for i, p in enumerate(ps):
        p["x"] = MARGIN + i * (HALF_W + COLGAP)
        p["y"], p["w"], p["bh"] = y, tw_, bh
        cards[p["name"]] = p
    bands.append({"y": y, "h": bh, "n": len(ps)})
    y += bh + BANDGAP
H = y - BANDGAP + MARGIN

out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT}">')
out.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')


def op_circle(cx, cy, sym, big):
    r = 23 if big else 15
    fill, stroke, col, fs = (HEAD_BG, HEAD_BG, "#ffffff", 26) if big else ("#ffffff", SYS_EDGE, SUB, 19)
    out.append(f'<circle cx="{round(cx,1)}" cy="{round(cy,1)}" r="{r}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="2"/>')
    out.append(f'<text x="{round(cx,1)}" y="{round(cy + fs * 0.35,1)}" text-anchor="middle" '
               f'font-size="{fs}" font-weight="700" fill="{col}">{sym}</text>')


# ── 맨 위 수식 띠 — 여기서 쓰는 × 는 그림 속 × 와 같은 모양이어야 기호가 한 번에 배운다
CIRC = "①②③④⑤⑥"
lead = "전문 AI 에이전트  ="
names = [f"{CIRC[i]} {n}" for i, n in enumerate(ORDER)]
XR, XPAD = 15, 14
tfs = TITLE_FS
while True:
    wsum = tw(lead, tfs) + 20 + sum(tw(n, tfs) for n in names) + 5 * (2 * XR + 2 * XPAD) + 5 * 16
    if wsum <= FULL_W - 40 or tfs <= 24:
        break
    tfs -= 1
ty = MARGIN + TITLE_H / 2
out.append(f'<rect x="{MARGIN}" y="{MARGIN}" width="{FULL_W}" height="{TITLE_H}" rx="12" '
           f'fill="{TITLE_BG}" stroke="{SYS_EDGE}" stroke-width="1.5"/>')
tx = (W - wsum) / 2
out.append(f'<text x="{round(tx,1)}" y="{round(ty + tfs * 0.36,1)}" font-size="{tfs}" '
           f'font-weight="800" fill="{INK}">{lead}</text>')
tx += tw(lead, tfs) + 20
for i, n in enumerate(names):
    if i:
        tx += 8 + XPAD
        out.append(f'<circle cx="{round(tx + XR,1)}" cy="{round(ty,1)}" r="{XR}" fill="{HEAD_BG}"/>')
        out.append(f'<text x="{round(tx + XR,1)}" y="{round(ty + 7,1)}" text-anchor="middle" '
                   f'font-size="20" font-weight="700" fill="#ffffff">×</text>')
        tx += 2 * XR + XPAD + 8
    out.append(f'<text x="{round(tx,1)}" y="{round(ty + tfs * 0.36,1)}" font-size="{tfs}" '
               f'font-weight="800" fill="{INK}">{n}</text>')
    tx += tw(n, tfs)


def chip(x, y, name, req, dash=True):
    w = bw(name)
    if req:
        out.append(f'<rect x="{round(x,1)}" y="{round(y,1)}" width="{w}" height="{BH}" rx="8" '
                   f'fill="{CHIP_BG}" stroke="{CHIP_EDGE}" stroke-width="1.5"/>')
    else:
        out.append(f'<rect x="{round(x,1)}" y="{round(y,1)}" width="{w}" height="{BH}" rx="8" '
                   f'fill="#ffffff" stroke="{COND_EDGE}" stroke-width="1.5" '
                   f'stroke-dasharray="{"5 4" if dash else "none"}"/>')
    out.append(f'<text x="{round(x + w / 2,1)}" y="{round(y + BH / 2 + 7,1)}" text-anchor="middle" '
               f'font-size="{FS}" fill="{INK}">{esc(name)}</text>')
    return w


def draw_flow_line(x, y, chips, last, first=True, extra=0.0):
    """화살표꼴 칩을 맞물려 그린다 — 기호 없이 순서가 읽힌다. 첫 칩과 맨 끝은 평평하게 막는다."""
    for ci, c in enumerate(chips):
        end = last and ci == len(chips) - 1
        head = first and ci == 0
        w = bw(c[1]) + NOTCH * 0.6 + extra
        x0, y1 = round(x, 1), round(y + BH, 1)
        xm, ym = round(x + w, 1), round(y + BH / 2, 1)
        tip = (f'L{round(x + w - NOTCH,1)},{round(y,1)} L{xm},{ym} L{round(x + w - NOTCH,1)},{y1} '
               if not end else f'L{xm},{round(y,1)} L{xm},{y1} ')
        back = f'L{x0},{y1} Z' if head else f'L{x0},{y1} L{round(x0 + NOTCH,1)},{ym} Z'
        d = f'M{x0},{round(y,1)} ' + tip + back
        out.append(f'<path d="{d}" fill="{CHIP_BG}" stroke="{CHIP_EDGE}" stroke-width="1.5" '
                   'stroke-linejoin="round"/>')
        out.append(f'<text x="{round(x + w / 2 + NOTCH / 2,1)}" y="{round(y + BH / 2 + 7,1)}" '
                   f'text-anchor="middle" font-size="{FS}" fill="{INK}">{esc(c[1])}</text>')
        x += w - NOTCH


def draw_line(x, y, toks):
    for t in toks:
        if t[0] == "m":
            x += chip(x, y, t[1], t[2]) + GAP
        else:
            out.append(f'<text x="{round(x + OP_W / 2,1)}" y="{round(y + BH / 2 + 7,1)}" '
                       f'text-anchor="middle" font-size="21" fill="{SUB}">{esc(t[1])}</text>')
            x += OP_W + GAP


def draw_stairs(cx, y, chain):
    """우선순위는 계단으로. 왼쪽 점선이 계단을 따라 꺾여 내려가 위가 세다는 것을 보인다."""
    n = len(chain)
    ch = n * (BH + 7) - 7
    pts, xs = [], []
    for i in range(n):
        xs.append(cx + 46 + i * STEP)
    ax = xs[0] - 16
    d = f"M{round(ax,1)},{round(y + BH / 2,1)}"
    for i in range(1, n):
        d += f" V{round(y + i * (BH + 7) + BH / 2,1)} H{round(xs[i] - 16,1)}"
        ax = xs[i] - 16
    out.append(f'<path d="{d}" fill="none" stroke="{SUB}" stroke-width="2" stroke-dasharray="4 4" '
               'stroke-linejoin="round"/>')
    tipy = y + BH / 2
    tx0 = xs[0] - 16
    out.append(f'<path d="M{round(tx0 - 6,1)},{round(tipy + 8,1)} L{round(tx0,1)},{round(tipy - 2,1)} '
               f'L{round(tx0 + 6,1)},{round(tipy + 8,1)}" fill="none" stroke="{SUB}" stroke-width="2" '
               'stroke-linejoin="round" stroke-linecap="round"/>')
    right = 0.0
    for i, c in enumerate(chain):
        w = chip(xs[i], y + i * (BH + 7), c[1], c[2])
        right = max(right, xs[i] + w)
        pts.append(xs[i])
    # 계단 오른쪽 빈자리에 뜻을 적는다 — 그림 밖 범례를 두지 않으므로 여기서 밝힌다
    out.append(f'<text x="{round(xs[0] + bw(chain[0][1]) + 20,1)}" y="{round(y + BH / 2 + 6,1)}" '
               f'font-size="{SMALL}" font-weight="700" fill="{SUB}">위 규칙이 아래를 이긴다</text>')
    return ch, right


def draw_sys(p, x, y, body_w):
    top, cx, inner = y, x + SPAD, body_w - 2 * SPAD
    out.append(f'<rect x="{x}" y="{round(y,1)}" width="{body_w}" height="{round(p["h"],1)}" rx="10" '
               f'fill="{SYS_BG}" stroke="{SYS_EDGE}" stroke-width="1.5"/>')
    y += SPAD
    if p["name"]:
        out.append(f'<text x="{cx}" y="{round(y + 20,1)}" font-size="21" font-weight="700" '
                   f'fill="{INK}">{esc(p["name"])}</text>')
        y += SLBL
    if p["chain"]:
        ch, _ = draw_stairs(cx, y, p["chain"])
        if p["plus"]:
            out.append(f'<text x="{round(cx + 6,1)}" y="{round(y + ch + 17,1)}" '
                       f'font-size="21" fill="{SUB}">+</text>')
            y += ch + 24
        else:
            y += ch + 6
    if p["chev"]:
        for li, ln in enumerate(p["chev"]):
            used = sum(bw(c[1]) + NOTCH * 0.6 - NOTCH for c in ln) + NOTCH
            draw_flow_line(cx, y, ln, li == len(p["chev"]) - 1, li == 0,
                           max(0.0, (inner - used) / len(ln)))
            y += LINEH
        y += -LINEH + BH + (14 if p["plus"] else 0)
    if p["plus"]:
        for ln in p["plus"]:
            draw_line(cx, y, ln)
            y += LINEH
        y += -LINEH + BH
    if p["cond"]:
        y += CTOP
        bh = CLBL + stack_h(len(p["cond"])) + CBOT
        out.append(f'<rect x="{cx}" y="{round(y,1)}" width="{round(cond_w(p["cond"]),1)}" '
                   f'height="{round(bh,1)}" rx="9" fill="{COND_BG}"/>')
        out.append(f'<text x="{round(cx + 14,1)}" y="{round(y + 19,1)}" font-size="{SMALL}" '
                   f'font-weight="700" fill="{COND_TXT}">+ 필요한 경우에만</text>')
        y += CLBL
        for ln in p["cond"]:
            draw_line(cx + 14, y, ln)
            y += LINEH
    return top + p["h"]


# ── 항 카드 ──────────────────────────────────────────────────────────────
for i, name in enumerate(ORDER):
    p = cards[name]
    x, y0, tw_, bh = p["x"], p["y"], p["w"], p["bh"]
    out.append(f'<rect x="{x}" y="{y0}" width="{tw_}" height="{round(bh,1)}" rx="14" '
               f'fill="{TERM_BG}" stroke="{TERM_EDGE}" stroke-width="2"/>')
    out.append(f'<path d="M{x},{y0 + HDR} L{x},{y0 + 14} q0,-14 14,-14 L{x + tw_ - 14},{y0} '
               f'q14,0 14,14 L{x + tw_},{y0 + HDR} Z" fill="{HEAD_BG}"/>')
    out.append(f'<text x="{x + TPAD}" y="{round(y0 + HDR / 2 + 10,1)}" font-size="26" '
               f'font-weight="700" fill="#ffffff">{CIRC[i]}  {name}</text>')
    sy = y0 + HDR + TPAD + (bh - p["h"]) / 2
    for si, sp in enumerate(p["sys"]):
        if si:
            ox, oy = x + tw_ / 2, sy + SYS_GAP / 2
            out.append(f'<path d="M{ox},{round(sy,1)} L{ox},{round(sy + SYS_GAP,1)}" '
                       f'stroke="{SYS_EDGE}" stroke-width="2"/>')
            op_circle(ox, oy, "+", False)
            sy += SYS_GAP
        sy = draw_sys(sp, x + TPAD, sy, p["body_w"])

# ── 항과 항을 잇는 × 다섯 개 — 밴드 사이는 세로, 밴드 안은 가로. 한 축에 세운다
for bi, b in enumerate(bands):
    if b["n"] == 2:
        cx, cy = W / 2, b["y"] + b["h"] / 2
        out.append(f'<path d="M{round(MARGIN + HALF_W,1)},{round(cy,1)} '
                   f'L{round(MARGIN + HALF_W + COLGAP,1)},{round(cy,1)}" stroke="{TERM_EDGE}" '
                   'stroke-width="2"/>')
        op_circle(cx, cy, "×", True)
    if bi:
        cx = W / 2
        prev = bands[bi - 1]
        y0 = prev["y"] + prev["h"]
        cy = (y0 + b["y"]) / 2
        seg = []
        for yy, yend, n in ((y0, cy, prev["n"]), (b["y"], cy, b["n"])):
            if n == 1:
                seg.append(f'M{round(cx,1)},{round(yy,1)} L{round(cx,1)},{round(yend,1)}')
            else:
                ym = (yy + yend) / 2
                for hx in (MARGIN + HALF_W / 2, MARGIN + HALF_W + COLGAP + HALF_W / 2):
                    seg.append(f'M{round(hx,1)},{round(yy,1)} L{round(hx,1)},{round(ym,1)} '
                               f'L{round(cx,1)},{round(ym,1)} L{round(cx,1)},{round(yend,1)}')
        out.append(f'<path d="{" ".join(seg)}" fill="none" stroke="{TERM_EDGE}" stroke-width="2" '
                   'stroke-linejoin="round"/>')
        op_circle(cx, cy, "×", True)

out.append("</svg>")
path = "docs/전개-수식.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{path}  {W}x{H}")
