# Generates 전개-수식.svg — the expansion kept in equation shape, but every material drawn as a
# figure so 필수 (solid filled brick) and 조건부 (dashed empty slot) split at a glance.
# Run: python3 "docs/전개-수식-gen.py"  (then check the render before committing)

FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
FS = 23          # material label
PAD = 32         # box side padding
BH = 48          # box height
GAP = 12         # box .. operator gap
ROW = 66         # row pitch
FILL = "#dde7ef"
LINE = "#46586b"
INK = "#1d2b38"
SUB = "#46586b"
FRAME = "#a8b4bf"


def tw(s, fs=FS):
    """Rough text width: Hangul full width, interpunct half, space thin, ascii ~0.55."""
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


# ── the expansion, row by row.  ("m", name, required?) material · ("o", sym) operator
#    ("[", None) / ("]", None) priority bracket
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

X_TERM = 46          # 항 name left edge
X_EQ = 176           # '=' centre
X_BRACE = 208        # big brace column
X_SYS = 232          # 계통 name left edge
W_SYS = 196          # 계통 name column width
X_BODY = X_SYS + W_SYS
OP_W = 30            # operator slot width


def row_width(row):
    w = 0.0
    for t in row:
        if t[0] == "m":
            w += bw(t[1]) + GAP
        elif t[0] == "o":
            w += OP_W + GAP
        else:
            w += 20 + GAP
    return w


o = []
y = 118

# ── layout pass: assign a y to every row, remember term blocks for the × marks
blocks = []
for name, systems in TERMS:
    start = y
    rows = []
    for sysname, rws in systems:
        sys_top = y
        for r in rws:
            rows.append((y, r))
            y += ROW
        blocks.append(("sys", sysname, sys_top, y - ROW))
        y += 8
    blocks.append(("term", name, start, y - ROW - 8, rows, systems))
    y += 46

H = y + 118
maxw = max(X_BODY + row_width(rw) for _, sysl in TERMS for _, rws in sysl for rw in rws)
W = int(maxw + 60)

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

# title strip
out.append(f'<text x="{X_TERM}" y="56" font-size="30" font-weight="700" fill="{INK}">전개</text>')
out.append(f'<text x="{X_TERM + 92}" y="56" font-size="22" fill="{SUB}">'
           '재료 51개 = 실선 벽돌 43개 + 점선 빈칸 8개</text>')
out.append(f'<line x1="{X_TERM}" y1="76" x2="{W - 46}" y2="76" stroke="{FRAME}" stroke-width="1.6"/>')


def draw_row(x0, y0, row):
    x = x0
    cy = y0 + BH / 2
    mats = [t for t in row if t[0] == "m"]
    only_cond = bool(mats) and all(not t[2] for t in mats)
    if only_cond:
        out.append(f'<text x="{X_BODY - 22}" y="{cy + 7}" text-anchor="end" font-size="20" '
                   f'fill="#94a3b1">필요한 경우</text>')
    for t in row:
        if t[0] == "m":
            _, nm, req = t
            w = bw(nm)
            if req:
                out.append(f'<rect x="{round(x,1)}" y="{y0}" width="{w}" height="{BH}" rx="9" '
                           f'fill="{FILL}" stroke="{LINE}" stroke-width="2.2"/>')
            else:
                out.append(f'<rect x="{round(x,1)}" y="{y0}" width="{w}" height="{BH}" rx="9" '
                           f'fill="#ffffff" stroke="{LINE}" stroke-width="2.2" stroke-dasharray="8 6"/>')
            out.append(f'<text x="{round(x + w / 2,1)}" y="{cy + 8.5}" text-anchor="middle" '
                       f'font-size="{FS}" fill="{INK}">{nm}</text>')
            x += w + GAP
        elif t[0] == "o":
            col = "#94a3b1" if only_cond else SUB
            out.append(f'<text x="{round(x + OP_W / 2,1)}" y="{cy + 9}" text-anchor="middle" '
                       f'font-size="26" fill="{col}">{t[1]}</text>')
            x += OP_W + GAP
        else:  # priority bracket
            br = t[0]
            d = (f'M{round(x+16,1)},{y0 - 6} L{round(x+4,1)},{y0 - 6} L{round(x+4,1)},{y0 + BH + 6} '
                 f'L{round(x+16,1)},{y0 + BH + 6}') if br == "[" else (
                f'M{round(x+4,1)},{y0 - 6} L{round(x+16,1)},{y0 - 6} L{round(x+16,1)},{y0 + BH + 6} '
                f'L{round(x+4,1)},{y0 + BH + 6}')
            out.append(f'<path d="{d}" fill="none" stroke="{SUB}" stroke-width="2.4"/>')
            x += 20 + GAP
    return x


for b in blocks:
    if b[0] == "term":
        _, name, top, bot, rows, systems = b
        mid = (top + bot + BH) / 2
        out.append(f'<text x="{X_TERM}" y="{round(mid + 12,1)}" font-size="34" font-weight="700" fill="{INK}">{name}</text>')
        out.append(f'<text x="{X_EQ}" y="{round(mid + 11,1)}" text-anchor="middle" font-size="30" fill="{SUB}">=</text>')
        if len(systems) > 1:   # big brace across the whole term
            t0, b0 = top - 10, bot + BH + 10
            m = (t0 + b0) / 2
            out.append(f'<path d="M{X_BRACE + 14},{t0} q-10,0 -10,10 L{X_BRACE + 4},{round(m - 12,1)} '
                       f'q0,12 -10,12 q10,0 10,12 L{X_BRACE + 4},{b0 - 10} q0,10 10,10" '
                       f'fill="none" stroke="{SUB}" stroke-width="2.4" stroke-linejoin="round"/>')
        for ry, r in rows:
            draw_row(X_BODY, ry, r)
    else:
        _, sysname, top, bot = b
        if sysname:
            out.append(f'<text x="{X_SYS}" y="{top + 33}" font-size="24" font-weight="700" fill="{SUB}">{sysname}</text>')

# × between terms — drawn in the left margin, between consecutive term blocks
terms_pos = [b for b in blocks if b[0] == "term"]
for a, c in zip(terms_pos, terms_pos[1:]):
    ymid = (a[3] + BH + c[2]) / 2
    out.append(f'<text x="{X_TERM + 34}" y="{round(ymid + 14,1)}" text-anchor="middle" '
               f'font-size="40" font-weight="700" fill="{SUB}">×</text>')

# legend
ly = H - 96
out.append(f'<rect x="{X_TERM}" y="{ly}" width="64" height="34" rx="7" fill="{FILL}" stroke="{LINE}" stroke-width="2.2"/>')
out.append(f'<text x="{X_TERM + 80}" y="{ly + 25}" font-size="24" fill="{INK}">'
           '실선 벽돌 = 어느 직무든 반드시 있어야 하는 재료 (43개). 하나만 비어도 그 항이 0이 된다</text>')
out.append(f'<rect x="{X_TERM}" y="{ly + 48}" width="64" height="34" rx="7" fill="#ffffff" stroke="{LINE}" '
           'stroke-width="2.2" stroke-dasharray="8 6"/>')
out.append(f'<text x="{X_TERM + 80}" y="{ly + 73}" font-size="24" fill="{INK}">'
           '점선 빈칸 = 그 직무에 필요한 경우에만 채우는 재료 (8개). 없는 직무는 빈칸으로 두고 없다고 적는다</text>')

out.append("</svg>")
path = "docs/전개-수식.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{path}  {W}x{H}")


# ── 같은 데이터로 글자판도 뽑는다 ───────────────────────────────────────────
# 그림을 못 보는 화면과 AI 가 읽는 판. SVG 와 한 데이터에서 나오므로 어긋날 수 없다.
DOC = "전문가 에이전트 정의 2.md"
BEGIN = "<!-- 전개-글자판 시작 — docs/전개-수식-gen.py 가 채운다. 손으로 고치지 말 것 -->"
END = "<!-- 전개-글자판 끝 -->"

W_TERM = 6       # 항 이름 칸
W_SYSN = 15      # 계통 이름 칸
INDENT = W_TERM + 3 + 2 + W_SYSN   # 본문이 시작하는 칸


def dw(s):
    """고정폭 화면에서의 글자 폭 — 한글·중점은 2칸, 나머지 1칸."""
    return sum(2 if ord(ch) > 0x2000 else 1 for ch in s)


def pad(s, w):
    return s + " " * max(0, w - dw(s))


def chip(tok):
    return f"[{tok[1]}]" if tok[2] else f"<{tok[1]}>"


def render_row(row):
    parts = []
    for t in row:
        if t[0] == "m":
            parts.append(chip(t))
        elif t[0] == "o":
            parts.append(t[1])
        else:
            parts.append(t[0])
    return " ".join(parts)


def text_lines():
    out = ["전개 — 재료 51개 = 실선 벽돌 43개 + 점선 빈칸 8개",
           "[재료] 실선 벽돌 = 어느 직무든 반드시 있어야 하는 재료 (43개). 하나만 비어도 그 항이 0이 된다",
           "<재료> 점선 빈칸 = 그 직무에 필요한 경우에만 채우는 재료 (8개). 없는 직무는 빈칸으로 두고 없다고 적는다",
           ""]
    for ti, (term, systems) in enumerate(TERMS):
        if ti:
            out.append(pad("", W_TERM) + " ×")
        braced = len(systems) > 1
        body = []
        for sysname, rows in systems:
            for ri, row in enumerate(rows):
                only_cond = all(t[2] is False for t in row if t[0] == "m") and any(t[0] == "m" for t in row)
                label = "필요한 경우" if only_cond else (sysname if ri == 0 and sysname else "")
                body.append((label, render_row(row)))
        n = len(body)
        mid = (n - 1) // 2
        for bi, (label, text) in enumerate(body):
            head = pad(term, W_TERM) + " = " if bi == 0 else pad("", W_TERM) + "   "
            if braced:
                brace = "⎧ " if bi == 0 else "⎩ " if bi == n - 1 else "⎨ " if bi == mid else "⎪ "
            else:
                brace = ""
            out.append((head + brace + pad(label, W_SYSN) + text).rstrip())
    return out


block = "\n".join([BEGIN, "", "```text"] + text_lines() + ["```", "", END])
doc = open(DOC, encoding="utf-8").read()
if BEGIN in doc and END in doc:
    head, rest = doc.split(BEGIN, 1)
    doc = head + block + rest.split(END, 1)[1]
    open(DOC, "w", encoding="utf-8").write(doc)
    print(f"{DOC}  전개 글자판 갱신")
else:
    print("\n".join(text_lines()))
