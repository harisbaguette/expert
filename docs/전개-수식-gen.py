# Generates 전개-수식.svg — 항마다 한 상자로 묶고, 상자 안은 위가 필수 · 아래가 필요한 경우.
# 계통이 둘 이상인 항 (지식·규칙) 은 상자 안에 계통 상자를 또 둔다.
# Run: python3 "docs/전개-수식-gen.py"  (then check the render before committing)

FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
FS = 23          # 재료 이름 글자 크기
PAD = 32         # 재료 상자 좌우 여백
BH = 48          # 재료 상자 높이
GAP = 12         # 재료 .. 연산자 사이
OP_W = 30        # 연산자 칸 폭
LINEH = 62       # 재료 줄 간격

INK = "#1d2b38"
SUB = "#46586b"
FILL = "#dde7ef"        # 필수 재료 채움
LINE = "#46586b"        # 필수 재료 테두리
TERM_EDGE = "#7b8b9a"   # 항 상자 테두리
TERM_HEAD = "#e6edf3"   # 항 머리띠
SYS_BG = "#f4f8fa"      # 계통 상자 바탕
SYS_EDGE = "#c8d5de"
COND_BG = "#fdf4e6"     # 필요한 경우 자리 바탕
COND_EDGE = "#cfa863"
COND_TXT = "#8a6a34"


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


# ── 전개 내용.  ("m", 이름, 필수?) 재료 · ("o", 기호) 연산자 · ("[", None)/("]", None) 우선순위 괄호
def M(n):
    return ("m", n, True)


def C(n):
    return ("m", n, False)


PLUS = ("o", "+")
ARROW = ("o", "→")
GT = ("o", ">")

TERMS = [
    # (항, [(계통이름, [행, 행...]), ...])
    ("환경", [(None, [
        [M("모델"), PLUS, M("실행 순환"), PLUS, M("저장·이어받기"), PLUS, M("나눠 맡기기")],
        [PLUS, M("작업창"), PLUS, M("시작 신호"), PLUS, M("자료 읽기"), PLUS, M("도구"), PLUS, M("시험 환경")],
        [PLUS, C("실시간 통로"), PLUS, C("그림·영상 생성")],
    ])]),
    ("지식", [
        ("자료·검색", [
            [M("법규·기준"), PLUS, M("해석 자료"), PLUS, M("일반 자료"), PLUS, M("고객·회사 정보")],
            [PLUS, M("출처·시점·판본"), PLUS, M("검색"), PLUS, M("자동 갱신")],
            [PLUS, C("플랫폼·기관 규정"), PLUS, C("현황 자료")],
        ]),
        ("지식·경험", [
            [M("업무 지식"), PLUS, M("감각·사례·암묵지")],
            [PLUS, C("정체성·작풍")],
        ]),
        ("기억·상태", [
            [M("장기 기억"), PLUS, M("작업 기억")],
        ]),
    ]),
    ("규칙", [
        ("규칙·권한", [
            [("[", None), M("절대 원칙"), GT, M("직업 규칙"), GT, C("계약·플랫폼 규칙"), GT, C("회사 규칙"),
             GT, M("개인 취향"), ("]", None)],
            [PLUS, M("권한·명의·위임"), PLUS, M("안전장치"), PLUS, M("책임·손실 한도")],
        ]),
        ("행동 체계", [
            [M("판단 규칙"), PLUS, M("업무 절차·노하우"), PLUS, M("완료 조건"), PLUS, M("먼저 감지하기")],
            [PLUS, M("사람에게 넘기기"), PLUS, M("보고·결과물")],
            [PLUS, C("상대 응대")],
        ]),
    ]),
    ("실무", [("업무 처리 흐름", [
        [M("감지·접수"), ARROW, M("의도 파악"), ARROW, M("문제 정의"), ARROW, M("자료 확인")],
        [ARROW, M("판단·계획"), ARROW, M("처리"), ARROW, M("검증"), ARROW, M("완료·보고"), ARROW, M("남기기")],
    ])]),
    ("검증", [("검증·평가", [
        [M("결과 검증·수정"), PLUS, M("반증·교차 검증"), PLUS, M("위험 누락 검사")],
        [PLUS, M("과정 평가"), PLUS, M("결과물 평가"), PLUS, M("근거 추적·재현")],
    ])]),
    ("학습", [("학습·개선", [
        [M("실패 원인 분석"), PLUS, M("고정 시험"), PLUS, M("자동 학습"), PLUS, M("성과 추적")],
    ])]),
]

# ── 자리 잡기 ─────────────────────────────────────────────────────────────
MARGIN = 44      # 그림 바깥 여백
TPAD = 22        # 항 상자 안 여백
HDR = 58         # 항 머리띠 높이
SPAD = 18        # 계통 상자 안 여백
SLBL = 38        # 계통 이름 줄 높이
CTOP = 12        # 필요한 경우 자리 위 여백
CLBL = 32        # 필요한 경우 이름 줄 높이
CBOT = 10        # 필요한 경우 자리 아래 여백
XGAP = 54        # 항과 항 사이 (× 자리)


def tok_w(t):
    if t[0] == "m":
        return bw(t[1]) + GAP
    if t[0] == "o":
        return OP_W + GAP
    return 20 + GAP


def flow(tokens, maxw):
    """재료를 주어진 폭 안에서 줄로 흘려 넣는다. 연산자는 다음 줄 머리로 넘어간다."""
    lines, cur, w = [], [], 0.0
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t[0] == "o" and i + 1 < len(tokens) and tokens[i + 1][0] == "m":
            unit, i = [t, tokens[i + 1]], i + 2
        else:
            unit, i = [t], i + 1
        uw = sum(tok_w(x) for x in unit)
        if cur and w + uw > maxw:
            lines.append(cur)
            cur, w = [], 0.0
        cur += unit
        w += uw
    if cur:
        lines.append(cur)
    return lines


def split_rows(rows):
    """행을 필수 묶음과 필요한 경우 묶음으로 가른다."""
    req, cond = [], []
    for r in rows:
        mats = [t for t in r if t[0] == "m"]
        (cond if mats and all(not t[2] for t in mats) else req).extend(r)
    while cond and cond[0][0] == "o":
        cond = cond[1:]
    return req, cond


def stack_h(n):
    """줄 n 개가 차지하는 높이 — 마지막 줄 뒤 여백은 세지 않는다."""
    return n * BH + (n - 1) * (LINEH - BH) if n else 0


def plan_sys(sysname, rows, cw, boxed):
    """계통 하나의 줄 배치와 높이를 미리 잰다."""
    req, cond = split_rows(rows)
    inner = cw - (2 * SPAD if boxed else 0)
    rl = flow(req, inner)
    cl = flow(cond, inner) if cond else []
    h = SPAD if boxed else 0
    if sysname:
        h += SLBL
    h += stack_h(len(rl))
    if cl:
        h += CTOP + CLBL + stack_h(len(cl)) + CBOT
    h += SPAD if boxed else 0
    return {"name": sysname, "req": rl, "cond": cl, "h": h, "boxed": boxed}


# 폭은 데이터의 한 행 가운데 가장 긴 것에 맞춘다 (우선순위 사슬이 제일 길다)
def widest():
    w = 0.0
    for _, systems in TERMS:
        extra = 2 * SPAD if len(systems) > 1 else 0
        for _, rows in systems:
            for row in rows:
                w = max(w, sum(tok_w(t) for t in row) + extra)
    return w


BODY_W = round(widest() + 2 * SPAD)          # 항 상자 안 내용 폭
TERM_W = BODY_W + 2 * TPAD
W = TERM_W + 2 * MARGIN

plans = []
y = MARGIN
for ti, (name, systems) in enumerate(TERMS):
    if ti:
        y += XGAP
    boxed = len(systems) > 1
    sysplans = [plan_sys(sn, rows, BODY_W, boxed) for sn, rows in systems]
    h = HDR + TPAD + sum(p["h"] for p in sysplans) + (len(sysplans) - 1) * 14 + TPAD
    plans.append({"name": name, "y": y, "h": h, "sys": sysplans})
    y += h
H = y + MARGIN

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>']


def draw_line(x0, y0, toks, cond):
    x = x0
    cy = y0 + BH / 2
    for t in toks:
        if t[0] == "m":
            _, nm, req = t
            w = bw(nm)
            if req:
                out.append(f'<rect x="{round(x,1)}" y="{y0}" width="{w}" height="{BH}" rx="9" '
                           f'fill="{FILL}" stroke="{LINE}" stroke-width="2.2"/>')
            else:
                out.append(f'<rect x="{round(x,1)}" y="{y0}" width="{w}" height="{BH}" rx="9" '
                           f'fill="#ffffff" stroke="{COND_EDGE}" stroke-width="2.2" stroke-dasharray="8 6"/>')
            out.append(f'<text x="{round(x + w / 2,1)}" y="{round(cy + 8.5,1)}" text-anchor="middle" '
                       f'font-size="{FS}" fill="{INK}">{nm}</text>')
            x += w + GAP
        elif t[0] == "o":
            col = COND_TXT if cond else SUB
            out.append(f'<text x="{round(x + OP_W / 2,1)}" y="{round(cy + 9,1)}" text-anchor="middle" '
                       f'font-size="26" fill="{col}">{t[1]}</text>')
            x += OP_W + GAP
        else:
            d = (f'M{round(x+16,1)},{round(y0-7,1)} L{round(x+4,1)},{round(y0-7,1)} '
                 f'L{round(x+4,1)},{round(y0+BH+7,1)} L{round(x+16,1)},{round(y0+BH+7,1)}') if t[0] == "[" else (
                f'M{round(x+4,1)},{round(y0-7,1)} L{round(x+16,1)},{round(y0-7,1)} '
                f'L{round(x+16,1)},{round(y0+BH+7,1)} L{round(x+4,1)},{round(y0+BH+7,1)}')
            out.append(f'<path d="{d}" fill="none" stroke="{SUB}" stroke-width="2.4"/>')
            x += 20 + GAP


def draw_sys(p, x, y, cw):
    """계통 하나를 그린다. 돌려주는 값은 다음 y."""
    top = y
    if p["boxed"]:
        out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{p["h"]}" rx="11" '
                   f'fill="{SYS_BG}" stroke="{SYS_EDGE}" stroke-width="2"/>')
        y += SPAD
        cx = x + SPAD
        inner = cw - 2 * SPAD
    else:
        cx = x
        inner = cw
    if p["name"]:
        out.append(f'<text x="{cx}" y="{round(y + 25,1)}" font-size="23" font-weight="700" '
                   f'fill="{SUB}">{p["name"]}</text>')
        y += SLBL
    for ln in p["req"]:
        draw_line(cx, y, ln, False)
        y += LINEH
    if p["cond"]:
        y += CTOP
        bh = CLBL + stack_h(len(p["cond"])) + CBOT
        out.append(f'<rect x="{cx}" y="{round(y,1)}" width="{inner}" height="{round(bh,1)}" rx="10" '
                   f'fill="{COND_BG}" stroke="{COND_EDGE}" stroke-width="1.8" stroke-dasharray="7 5"/>')
        out.append(f'<text x="{round(cx + 16,1)}" y="{round(y + 24,1)}" font-size="21" font-weight="700" '
                   f'fill="{COND_TXT}">필요한 경우에만</text>')
        y += CLBL
        for ln in p["cond"]:
            draw_line(cx + 16, y, ln, True)
            y += LINEH
        y += CBOT
    return top + p["h"]


for pi, p in enumerate(plans):
    x, y0, h = MARGIN, p["y"], p["h"]
    out.append(f'<rect x="{x}" y="{y0}" width="{TERM_W}" height="{h}" rx="16" '
               f'fill="#ffffff" stroke="{TERM_EDGE}" stroke-width="2.8"/>')
    out.append(f'<path d="M{x},{y0 + HDR} L{x},{y0 + 16} q0,-16 16,-16 L{x + TERM_W - 16},{y0} '
               f'q16,0 16,16 L{x + TERM_W},{y0 + HDR} Z" fill="{TERM_HEAD}"/>')
    out.append(f'<line x1="{x}" y1="{y0 + HDR}" x2="{x + TERM_W}" y2="{y0 + HDR}" '
               f'stroke="{TERM_EDGE}" stroke-width="2.8"/>')
    out.append(f'<text x="{x + TPAD}" y="{y0 + 41}" font-size="31" font-weight="700" fill="{INK}">{p["name"]}</text>')
    sy = y0 + HDR + TPAD
    for si, sp in enumerate(p["sys"]):
        if si:
            sy += 14
        sy = draw_sys(sp, x + TPAD, sy, BODY_W)
    if pi + 1 < len(plans):
        ym = y0 + h + XGAP / 2
        out.append(f'<text x="{round(W / 2,1)}" y="{round(ym + 15,1)}" text-anchor="middle" '
                   f'font-size="42" font-weight="700" fill="{SUB}">×</text>')

out.append("</svg>")
path = "docs/전개-수식.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{path}  {W}x{H}")
