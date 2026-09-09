# Generates 전개-끼움판.svg — the same 51 materials, but 필수 and 조건부 are split by PLACE:
# the body board holds the 43 that every job needs, and the 8 conditional ones sit apart in a
# tray that says when each gets plugged in.  Empty dashed slots (numbered) mark where they go.
# Run: python3 "docs/전개-끼움판-gen.py"  (then check the render before committing)

FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
FS = 23
PAD = 32
BH = 48
GAP = 12
ROWP = 60          # chip row pitch
FILL = "#dde7ef"
LINE = "#46586b"
INK = "#1d2b38"
SUB = "#46586b"
FRAME = "#a8b4bf"
DIM = "#7b8b9c"
NUM = "①②③④⑤⑥⑦⑧"


def tw(s, fs=FS):
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


# ── data ────────────────────────────────────────────────────────────────────
# chip = (name, slot_no or None)   slot_no set ⇒ conditional, drawn as an empty dashed slot
TERMS = {
    "환경": [(None, ["모델", "실행 순환", "저장·이어받기", "나눠 맡기기", "작업창", "시작 신호",
                     "자료 읽기", "도구", "시험 환경", ("실시간 통로", 1), ("그림·영상 생성", 2)])],
    "지식": [("자료·검색", ["법규·기준", "해석 자료", "일반 자료", "고객·회사 정보", "출처·시점·판본",
                           "검색", "자동 갱신", ("플랫폼·기관 규정", 3), ("현황 자료", 4)]),
             ("지식·경험", ["업무 지식", "감각·사례·암묵지", ("정체성·작풍", 5)]),
             ("기억·상태", ["장기 기억", "작업 기억"])],
    "규칙": [("규칙·권한", {"chain": ["절대 원칙", "직업 규칙", ("계약·플랫폼 규칙", 6), ("회사 규칙", 7),
                                     "개인 취향"],
                            "side": ["권한·명의·위임", "안전장치", "책임·손실 한도"]}),
             ("행동 체계", ["판단 규칙", "업무 절차·노하우", "완료 조건", "먼저 감지하기",
                           "사람에게 넘기기", "보고·결과물", ("상대 응대", 8)])],
    "실무": [("업무 처리 흐름", ["0 감지·접수", "1 의도 파악", "2 문제 정의", "3 자료 확인", "4 판단·계획",
                               "5 처리", "6 검증", "7 완료·보고", "8 남기기"])],
    "검증": [("검증·평가", ["결과 검증·수정", "반증·교차 검증", "위험 누락 검사", "과정 평가",
                          "결과물 평가", "근거 추적·재현"])],
    "학습": [("학습·개선", ["실패 원인 분석", "고정 시험", "자동 학습", "성과 추적"])],
}
COLUMNS = [["환경", "실무"], ["지식", "검증"], ["규칙", "학습"]]

# 끼움 부품 8 — (번호, 이름, 언제 끼우나, 들어갈 자리)
TRAY = [
    (1, "실시간 통로", "음성·화상·채팅·방송처럼 초 단위로 주고받는 일일 때", "환경"),
    (2, "그림·영상 생성", "결과물이 글이 아닐 때 (그림·영상·음성·도면)", "환경"),
    (3, "플랫폼·기관 규정", "올리거나 납품하거나 승인받는 곳이 있을 때", "지식 · 자료·검색"),
    (4, "현황 자료", "날마다 바뀌는 바깥 값이 판단에 들어갈 때", "지식 · 자료·검색"),
    (5, "정체성·작풍", "채널·작가·브랜드의 고유한 목소리가 있는 일일 때", "지식 · 지식·경험"),
    (6, "계약·플랫폼 규칙", "계약·플랫폼이 회사 밖에서 나를 묶을 때", "규칙 · 규칙·권한"),
    (7, "회사 규칙", "회사 정책·전결권·승인 조건에 매인 일일 때", "규칙 · 규칙·권한"),
    (8, "상대 응대", "상대가 사람이고 그 자리에서 성과가 갈릴 때", "규칙 · 행동 체계"),
]

COL_W = 508
COL_GAP = 24
MARGIN = 30
W = MARGIN * 2 + COL_W * 3 + COL_GAP * 2

out = []


def chip(x, y, name, slot=None):
    """slot=None → solid brick; otherwise dashed empty slot carrying its number."""
    label = name if slot is None else f"{NUM[slot - 1]} {name}"
    w = bw(label)
    if slot is None:
        out.append(f'<rect x="{round(x,1)}" y="{y}" width="{w}" height="{BH}" rx="9" '
                   f'fill="{FILL}" stroke="{LINE}" stroke-width="2.2"/>')
        out.append(f'<text x="{round(x + w / 2,1)}" y="{y + 32.5}" text-anchor="middle" '
                   f'font-size="{FS}" fill="{INK}">{label}</text>')
    else:
        out.append(f'<rect x="{round(x,1)}" y="{y}" width="{w}" height="{BH}" rx="9" '
                   f'fill="#ffffff" stroke="{DIM}" stroke-width="2.2" stroke-dasharray="8 6"/>')
        out.append(f'<text x="{round(x + w / 2,1)}" y="{y + 32.5}" text-anchor="middle" '
                   f'font-size="{FS}" fill="{DIM}">{label}</text>')
    return w


def wrap(chips, inner_w):
    """Greedy row packing; returns list of rows, each a list of (chip, width)."""
    rows, cur, curw = [], [], 0.0
    for c in chips:
        nm, slot = (c, None) if isinstance(c, str) else c
        label = nm if slot is None else f"{NUM[slot - 1]} {nm}"
        w = bw(label)
        if cur and curw + GAP + w > inner_w:
            rows.append(cur)
            cur, curw = [], 0.0
        cur.append(((nm, slot), w))
        curw += w + (GAP if len(cur) > 1 else 0)
    if cur:
        rows.append(cur)
    return rows


def term_height(name):
    h = 62                                  # header + rule line
    for sysname, chips in TERMS[name]:
        if sysname:
            h += 34
        if isinstance(chips, dict):
            h += len(chips["chain"]) * ROWP
        else:
            h += len(wrap(chips, COL_W - 48)) * ROWP
        h += 10
    return h + 8


def draw_term(x, y, name):
    h = term_height(name)
    out.append(f'<rect x="{x}" y="{y}" width="{COL_W}" height="{h}" rx="12" fill="#ffffff" '
               f'stroke="{FRAME}" stroke-width="2.2"/>')
    out.append(f'<text x="{x + 22}" y="{y + 46}" font-size="36" font-weight="700" fill="{INK}">{name}</text>')
    out.append(f'<line x1="{x + 22}" y1="{y + 58}" x2="{x + COL_W - 22}" y2="{y + 58}" '
               f'stroke="{FRAME}" stroke-width="1.6"/>')
    cy = y + 62
    inner = COL_W - 48
    for sysname, chips in TERMS[name]:
        if sysname:
            out.append(f'<text x="{x + 22}" y="{cy + 26}" font-size="24" font-weight="700" fill="{SUB}">{sysname}</text>')
            cy += 34
        if isinstance(chips, dict):
            cw = max(bw(c if isinstance(c, str) else f"{NUM[c[1]-1]} {c[0]}") for c in chips["chain"])
            sw = max(bw(c) for c in chips["side"])
            lx = x + (COL_W - (cw + 16 + sw)) / 2
            for j, c in enumerate(chips["chain"]):
                nm, slot = (c, None) if isinstance(c, str) else c
                label = nm if slot is None else f"{NUM[slot-1]} {nm}"
                chip(lx + (cw - bw(label)) / 2, cy + j * ROWP, nm, slot)
                if j < len(chips["chain"]) - 1:
                    out.append(f'<text x="{round(lx + cw / 2,1)}" y="{cy + j * ROWP + BH + 14}" '
                               f'text-anchor="middle" font-size="20" fill="{SUB}">∨</text>')
            for j, c in enumerate(chips["side"]):
                chip(lx + cw + 16 + (sw - bw(c)) / 2, cy + j * ROWP, c)
            out.append(f'<text x="{x + 156}" y="{cy - 8}" font-size="20" fill="{DIM}">'
                       f'왼쪽 줄 위아래 = 부딪힐 때 이기는 순서</text>')
            cy += len(chips["chain"]) * ROWP + 10
            continue
        for row in wrap(chips, inner):
            tot = sum(w for _, w in row) + GAP * (len(row) - 1)
            cx = x + (COL_W - tot) / 2
            for (nm, slot), w in row:
                chip(cx, cy, nm, slot)
                cx += w + GAP
            cy += ROWP
        cy += 10
    return h


# ── layout: three columns, terms stacked per column ─────────────────────────
BODY_TOP = 132
col_x = [MARGIN + i * (COL_W + COL_GAP) for i in range(3)]
col_bottom = []
placed = {}
for i, names in enumerate(COLUMNS):
    yy = BODY_TOP
    for nm in names:
        placed[nm] = (col_x[i], yy)
        yy += term_height(nm) + 30
    col_bottom.append(yy - 30)

BODY_BOTTOM = max(col_bottom)
TRAY_TOP = BODY_BOTTOM + 54
TRAY_ROW = 84
TRAY_H = 74 + 4 * TRAY_ROW + 96
H = TRAY_TOP + TRAY_H + 30

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

# ── header of the body board
out.append(f'<text x="{MARGIN}" y="56" font-size="34" font-weight="700" fill="{INK}">본체 — 어느 직무든 있어야 하는 재료 43개</text>')
out.append(f'<text x="{MARGIN}" y="92" font-size="24" fill="{SUB}">'
           '실선 벽돌은 직무를 갈아 끼워도 그대로 남는다. 하나만 비어도 그 항이 0이 되어 에이전트가 서지 않는다</text>')
out.append(f'<line x1="{MARGIN}" y1="110" x2="{W - MARGIN}" y2="110" stroke="{INK}" stroke-width="2.6"/>')

for nm in placed:
    x, y = placed[nm]
    draw_term(x, y, nm)

# × marks between the three columns, at the height of the first row of terms
xmid_y = BODY_TOP + term_height("환경") / 2
for i in range(2):
    out.append(f'<text x="{col_x[i] + COL_W + COL_GAP / 2}" y="{round(xmid_y + 18,1)}" text-anchor="middle" '
               f'font-size="52" font-weight="700" fill="{SUB}">×</text>')

# ── the tray
out.append(f'<rect x="{MARGIN}" y="{TRAY_TOP}" width="{W - MARGIN * 2}" height="{TRAY_H}" rx="14" '
           f'fill="#fafbfc" stroke="{DIM}" stroke-width="2.4" stroke-dasharray="12 8"/>')
out.append(f'<text x="{MARGIN + 26}" y="{TRAY_TOP + 50}" font-size="34" font-weight="700" fill="{INK}">'
           '끼움 부품 — 그 직무의 세상에 있을 때만 채우는 재료 8개</text>')
out.append(f'<text x="{MARGIN + 26}" y="{TRAY_TOP + 86}" font-size="24" fill="{SUB}">'
           '위 본체의 같은 번호 빈칸에 들어간다. 없는 직무는 빈칸으로 두고 "이 직무에 없음" 이라 적는다. '
           '있어야 하는데 빠지면 필수와 똑같이 그 항이 0이다</text>')

tw_col = (W - MARGIN * 2 - 52) / 2
for k, (no, nm, when, where) in enumerate(TRAY):
    cx = MARGIN + 26 + (k % 2) * (tw_col + 4)
    cy = TRAY_TOP + 116 + (k // 2) * TRAY_ROW
    out.append(f'<circle cx="{round(cx + 20,1)}" cy="{cy + 24}" r="20" fill="{FILL}" stroke="{LINE}" stroke-width="2.2"/>')
    out.append(f'<text x="{round(cx + 20,1)}" y="{cy + 32}" text-anchor="middle" font-size="22" '
               f'font-weight="700" fill="{INK}">{no}</text>')
    out.append(f'<text x="{round(cx + 52,1)}" y="{cy + 20}" font-size="25" font-weight="700" fill="{INK}">{nm}</text>')
    out.append(f'<text x="{round(cx + 52,1)}" y="{cy + 50}" font-size="22" fill="{SUB}">{when}</text>')
    out.append(f'<text x="{round(cx + tw_col - 14,1)}" y="{cy + 20}" text-anchor="end" font-size="21" '
               f'fill="{DIM}">{where}</text>')

py = TRAY_TOP + TRAY_H - 32
out.append(f'<text x="{MARGIN + 26}" y="{py}" font-size="22" fill="{SUB}">'
           '짝지어 다니는 것 — ⑥ 계약·플랫폼 규칙과 ⑦ 회사 규칙은 둘 다 빌 수 없다 (나를 묶는 것이 회사든 계약이든 하나는 있다) · '
           '③ 플랫폼·기관 규정이 있으면 ⑥ 도 있다</text>')

svg += out + ["</svg>"]
path = "docs/전개-끼움판.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print(f"{path}  {W}x{H}")
