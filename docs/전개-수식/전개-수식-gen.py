# Generates 전개-수식.svg — 수식을 그림 한 장으로. 문서에는 이 그림만 두고 범례도 해설도 붙이지
# 않으므로, 그림만 보고 다 읽혀야 한다.
#   항 6개는 × 로, 항 안의 계통과 재료는 + 로 이어진다. 항을 한 줄로 쌓아 × 다섯 개가 한 축에 선다.
#   재료 줄은 남는 폭을 칩이 나눠 가져 상자 좌우에 꽉 맞춘다.
#   이름·계통·실무 묶음·적용 구분은 본문에서 읽고 materials.md의 공식 대응표와 대조한다.
#   재료 구성과 반복 실행을 함께 보인다. 규칙은 적용 의무의 동시 충족으로 표현한다.
# Run: python3 "docs/전개-수식/전개-수식-gen.py"  (then check the render before committing)
#
# 기준선: 본문 77개 항목 · 9개 계통 · 세부 책임 M01–M57. 한 항목과 한 ID는 일대일이 아니다.

import re
from html import escape
from pathlib import Path

FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

INK = "#16202b"          # 가장 진한 글자
SUB = "#55677a"          # 보조 글자
HEAD_BG = "#1d2b38"      # 항 머리띠
TERM_BG = "#dde6ee"      # 항 몸통 — 계통 카드(흰색)와 명도를 벌린다
TERM_EDGE = "#a7b9c8"
SYS_BG = "#ffffff"       # 계통 상자
SYS_EDGE = "#c3d0db"
CHIP_BG = "#d5e2ec"      # 상시 재료
CHIP_EDGE = "#6d8194"
COND_BG = "#dde7ef"      # 필요한 경우 칸 바닥
COND_EDGE = "#8fa0b0"    # 조건부 재료 (해당 조건이 참이면 필수)
TITLE_BG = "#eef3f8"

FS = 19                  # 재료 글자
PAD = 26                 # 재료 칩 좌우 여백
BH = 38                  # 재료 칩 높이
GAP = 9                  # 재료 사이
OP_W = 22                # + 기호 칸
LINEH = 46               # 재료 줄 간격
SMALL = 17               # 그림 안 최소 글자

MARGIN = 40
TITLE_H = 64             # 맨 위 수식 띠
LOOP_H = 190             # 실제 실행의 피드백 순환
TITLE_FS = 34
BANDGAP = 62             # 항과 항 사이 (× 자리)
TPAD = 20                # 항 상자 안 여백
HDR = 54                 # 항 머리띠 높이
SPAD = 20                # 계통 상자 안 여백
SLBL = 32                # 계통 이름 줄
SYS_GAP = 42             # 계통과 계통 사이 (+ 자리)
CTOP = 14                # 적용 구분 사이 간격
CLBL = 28                # 적용 구분 이름 줄

W = 1446
FULL_W = W - 2 * MARGIN              # 항 카드 폭


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
    return escape(s, quote=True)


# ── 본문 항목과 세부 책임의 공식 대응 ────────────────────────────────
USAGE_LABELS = {
    "상시": "상시 · 업무 내내 적용",
    "단계별": "단계별 · 해당 단계마다 적용",
    "조건부": "조건부 · 필요하면 필수",
}
TERM_SYSTEMS = {
    "환경": ["환경"],
    "지식": ["자료·검색", "지식·경험", "기억·진행 상태"],
    "규칙": ["규칙·권한", "행동 체계"],
    "실무": ["실무"],
    "검증": ["검증·평가"],
    "학습": ["학습·개선"],
}
PLUS = ("o", "+")
ROOT = Path(__file__).resolve().parents[2]
EXPECTED_ITEMS = 77
EXPECTED_IDS = {f"M{i:02d}" for i in range(1, 58)}
SYSTEMS = [group for groups in TERM_SYSTEMS.values() for group in groups]


def section(text, heading):
    if text.count(heading + "\n") != 1:
        raise ValueError(f"절 제목이 없거나 중복됩니다: {heading}")
    return text.split(heading + "\n", 1)[1].split("\n## ", 1)[0]


def table_cells(line, count):
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if len(cells) != count:
        raise ValueError(f"표는 {count}열이어야 합니다: {cells[0]}")
    return cells


def load_responsibilities(registry):
    records, group = [], ""
    for line in registry.splitlines():
        if line.startswith("## "):
            group = line[3:].split(" — ")[0]
        if not re.match(r"^\| M\d+ ", line):
            continue
        cells = table_cells(line, 5)
        mid, name = cells[0].split(" ", 1)
        usage = re.fullmatch(r"\*\*([^*]+)\*\*<br>(.+)", cells[-1])
        if not usage or usage[1] not in USAGE_LABELS:
            raise ValueError(f"적용 구분·시점 누락 또는 오류: {mid} {name}")
        records.append({"id": mid, "name": name, "group": group,
                        "usage": usage[1], "note": cells[-1]})
    ids = [r["id"] for r in records]
    if len(ids) != len(EXPECTED_IDS) or set(ids) != EXPECTED_IDS:
        raise ValueError("세부 책임의 ID가 M01–M57과 일치하지 않습니다.")
    names = {r["name"] for r in records}
    if len(names) != len(records):
        raise ValueError("세부 책임 이름이 중복됩니다.")
    expected_groups = (set(SYSTEMS) - {"기억·진행 상태"}) | {"기억·상태"}
    if {r["group"] for r in records} != expected_groups:
        raise ValueError("재료의 계통이 9개 계통과 일치하지 않습니다.")
    return records


def load_summary(summary):
    records, group, subgroup = [], "", ""
    for line in section(summary, "## 계통별 재료 ✅").splitlines():
        if line.startswith("### "):
            group = line[4:].removesuffix(" ✅")
            subgroup = ""
        if line.startswith("#### "):
            subgroup = line[5:]
        match = re.match(r"^\|\s*\*\*([^*]+)\*\*(?:\s+✅)?\s*\|", line)
        if not match or not group:
            continue
        cells = table_cells(line, 6)
        usage = re.fullmatch(r"\*\*([^*]+)\*\*", cells[4])
        if not usage or usage[1] not in USAGE_LABELS or not cells[5]:
            raise ValueError(f"본문 적용 구분·시점 오류: {match[1]}")
        records.append({"name": match[1], "group": group, "subgroup": subgroup,
                        "usage": usage[1], "note": cells[5]})
    if len(records) != EXPECTED_ITEMS or len({r["name"] for r in records}) != EXPECTED_ITEMS:
        raise ValueError("본문 항목은 중복 없이 77개여야 합니다.")
    if list(dict.fromkeys(r["group"] for r in records)) != SYSTEMS:
        raise ValueError("본문의 계통·순서가 9개 계통과 일치하지 않습니다.")
    return records


def load_mapping(registry):
    records = []
    for line in section(registry, "## 본문과 세부 책임의 대응").splitlines():
        if not line.startswith("| ") or line.startswith("| 본문 계통 |"):
            continue
        group, name, refs, usage, boundary = table_cells(line, 5)
        ids = re.findall(r"\bM\d+\b", refs)
        if not ids or not set(ids) <= EXPECTED_IDS or usage not in USAGE_LABELS:
            raise ValueError(f"대응표 세부 책임·적용 구분 오류: {name}")
        records.append({"group": group, "name": name, "ids": ids,
                        "usage": usage, "boundary": boundary})
    if len(records) != EXPECTED_ITEMS or len({r["name"] for r in records}) != EXPECTED_ITEMS:
        raise ValueError("대응표 항목은 중복 없이 77개여야 합니다.")
    used_ids = {mid for r in records for mid in r["ids"]}
    if used_ids != EXPECTED_IDS:
        raise ValueError(f"본문에 연결되지 않은 세부 책임: {sorted(EXPECTED_IDS - used_ids)}")
    return records


def validate_summary(records, mapping):
    """일대다·다대일 대응을 허용하고 본문 이름·계통·구분·순서를 검사한다."""
    for record, mapped in zip(records, mapping, strict=True):
        if any(record[key] != mapped[key] for key in ("name", "group", "usage")):
            raise ValueError(f"본문과 대응표의 이름·계통·구분·순서 불일치: {record['name']} / {mapped['name']}")
        record["ids"] = mapped["ids"]
        record["boundary"] = mapped["boundary"]


REGISTRY = (ROOT / "docs/materials.md").read_text(encoding="utf-8")
RESPONSIBILITIES = load_responsibilities(REGISTRY)
MATERIALS = load_summary((ROOT / "전문가 에이전트 정의.md").read_text(encoding="utf-8"))
validate_summary(MATERIALS, load_mapping(REGISTRY))
TERMS = {
    term: [(group, [r for r in MATERIALS if r["group"] == group]) for group in groups]
    for term, groups in TERM_SYSTEMS.items()
}
ORDER = list(TERMS)
out = []


def material_tokens(records):
    tokens = []
    for record in records:
        if tokens:
            tokens.append(PLUS)
        tokens.append(("m", record["name"], record["usage"], record))
    return tokens


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


def stack_h(n):
    return n * BH + (n - 1) * (LINEH - BH) if n else 0




def plan_sys(group, records, body_w):
    inner = body_w - 2 * SPAD
    name = "" if group in {"환경", "실무"} else group
    blocks = []
    keys = list(dict.fromkeys((r["subgroup"], r["usage"]) for r in records))
    for subgroup, usage in keys:
        selected = [r for r in records if (r["subgroup"], r["usage"]) == (subgroup, usage)]
        lines = flow(material_tokens(selected), inner - 28)
        blocks.append({"usage": usage, "subgroup": subgroup, "lines": lines,
                       "h": CLBL + stack_h(len(lines)) + 12})
    h = SPAD + (SLBL if name else 0)
    h += sum(block["h"] for block in blocks) + CTOP * (len(blocks) - 1)
    if group == "규칙·권한":
        h += 38
    h += SPAD
    return {"name": name, "blocks": blocks, "h": h}


def plan_term(name, body_w):
    sysp = [plan_sys(sn, rows, body_w) for sn, rows in TERMS[name]]
    h = HDR + TPAD + sum(p["h"] for p in sysp) + (len(sysp) - 1) * SYS_GAP + TPAD
    return {"name": name, "sys": sysp, "h": h, "body_w": body_w}


# ── 자리 잡기 ────────────────────────────────────────────────────────────
cards = {}
y = MARGIN + TITLE_H + BANDGAP
for name in ORDER:
    p = plan_term(name, FULL_W - 2 * TPAD)
    p["y"] = y
    cards[name] = p
    y += p["h"] + BANDGAP
LOOP_Y = y - BANDGAP + 28
H = LOOP_Y + LOOP_H + MARGIN

out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT}" role="img" aria-labelledby="formula-title formula-desc">')
out.append(f'<title id="formula-title">전문 AI 에이전트 구성 전개식 — '
           f'{len(TERMS)}개 항·{len(SYSTEMS)}개 계통·{len(MATERIALS)}개 항목</title>')
out.append('<desc id="formula-desc">환경 × 지식 × 규칙 × 실무 × 검증 × 학습. '
           f'본문의 {len(MATERIALS)}개 항목을 세부 책임 {len(RESPONSIBILITIES)}개와 대응한다. '
           '상시는 진행 전반에, 단계별은 해당 단계마다 적용한다. '
           '단계별도 자료·전제·결과가 바뀌면 반복한다. '
           '조건부는 필요할 때 적용하며, 조건이 참이면 필수다. '
           '실무는 진행·후속 관리, 자료 가공, 계산·분석·판정, 구상·표현·제작, '
           '대화·협의, 업무 시스템 조작, 납품·인계, 관찰·시험·연습의 여덟 묶음이다. '
           '규칙은 적용 범위와 해석을 확인해 함께 충족하며, 상황·조건부 전략·실행·외부 검증을 순환한다. '
           '재료의 개수는 전문가 성능을 보장하지 않는다.</desc>')
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
lead = "구성 개념식  ="
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


def chip(x, y, name, usage, record, ext=0.0):
    w = bw(name) + ext
    fill = CHIP_BG if usage == "상시" else "#ffffff"
    stroke = COND_EDGE if usage == "조건부" else CHIP_EDGE
    dash = ' stroke-dasharray="5 4"' if usage == "조건부" else ""
    out.append(f'<g data-material="{esc(name)}" data-system="{esc(record["group"])}" '
               f'data-subgroup="{esc(record["subgroup"])}" data-usage="{usage}" '
               f'data-responsibilities="{" ".join(record["ids"])}">')
    out.append(f'<title>{esc(name)} · {usage} · {esc(record["note"])}\n'
               f'{"·".join(record["ids"])}: {esc(record["boundary"])}</title>')
    out.append(f'<rect x="{round(x,1)}" y="{round(y,1)}" width="{w}" height="{BH}" rx="8" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>')
    out.append(f'<text x="{round(x + w / 2,1)}" y="{round(y + BH / 2 + 7,1)}" text-anchor="middle" '
               f'font-size="{FS}" fill="{INK}">{esc(name)}</text>')
    out.append('</g>')
    return w


def justify(toks, width):
    """남는 폭을 칩이 고루 나눠 가져 줄이 좌우에 꽉 찬다."""
    chips = [t for t in toks if t[0] == "m"]
    base = sum(bw(t[1]) for t in chips) + OP_W * (len(toks) - len(chips)) + GAP * (len(toks) - 1)
    return max(0.0, width - base) / len(chips) if chips else 0.0


def draw_line(x, y, toks, width=None):
    ext = justify(toks, width) if width else 0.0
    for t in toks:
        if t[0] == "m":
            x += chip(x, y, t[1], t[2], t[3], ext=ext) + GAP
        else:
            out.append(f'<text x="{round(x + OP_W / 2,1)}" y="{round(y + BH / 2 + 7,1)}" '
                       f'text-anchor="middle" font-size="21" fill="{SUB}">{esc(t[1])}</text>')
            x += OP_W + GAP



def draw_sys(p, x, y, body_w):
    top, cx, inner = y, x + SPAD, body_w - 2 * SPAD
    out.append(f'<rect x="{x}" y="{round(y,1)}" width="{body_w}" height="{round(p["h"],1)}" rx="10" '
               f'fill="{SYS_BG}" stroke="{SYS_EDGE}" stroke-width="1.5"/>')
    y += SPAD
    if p["name"]:
        out.append(f'<text x="{cx}" y="{round(y + 20,1)}" font-size="21" font-weight="700" '
                   f'fill="{INK}">{esc(p["name"])}</text>')
        y += SLBL
    for index, block in enumerate(p["blocks"]):
        if index:
            y += CTOP
        block_y = y
        usage = block["usage"]
        if usage == "조건부":
            out.append(f'<rect x="{cx}" y="{round(y,1)}" width="{inner}" '
                       f'height="{block["h"]}" rx="9" fill="{COND_BG}"/>')
        prefix = "+ " if index else ""
        label = prefix + (block["subgroup"] + " — " if block["subgroup"] else "") + USAGE_LABELS[usage]
        out.append(f'<text x="{cx + 14}" y="{round(y + 19,1)}" font-size="{SMALL}" '
                   f'font-weight="700" fill="{SUB}">{esc(label)}</text>')
        y += CLBL
        for line in block["lines"]:
            draw_line(cx + 14, y, line, inner - 28)
            y += LINEH
        y = block_y + block["h"]
    if p["name"] == "규칙·권한":
        note_y = top + p["h"] - 20
        out.append(f'<text x="{cx}" y="{note_y}" font-size="{SMALL}" fill="{SUB}">'
                   '관할·대상·해석 근거 확인 → 적용 의무·권한·한도를 함께 충족</text>')
    return top + p["h"]


# ── 항 카드 ──────────────────────────────────────────────────────────────
for i, name in enumerate(ORDER):
    p = cards[name]
    x, y0, tw_, bh = MARGIN, p["y"], FULL_W, p["h"]
    out.append(f'<rect x="{x}" y="{y0}" width="{tw_}" height="{round(bh,1)}" rx="14" '
               f'fill="{TERM_BG}" stroke="{TERM_EDGE}" stroke-width="2"/>')
    out.append(f'<path d="M{x},{y0 + HDR} L{x},{y0 + 14} q0,-14 14,-14 L{x + tw_ - 14},{y0} '
               f'q14,0 14,14 L{x + tw_},{y0 + HDR} Z" fill="{HEAD_BG}"/>')
    out.append(f'<text x="{x + TPAD}" y="{round(y0 + HDR / 2 + 10,1)}" font-size="26" '
               f'font-weight="700" fill="#ffffff">{CIRC[i]}  {name}</text>')
    sy = y0 + HDR + TPAD
    for si, sp in enumerate(p["sys"]):
        if si:
            ox, oy = x + tw_ / 2, sy + SYS_GAP / 2
            out.append(f'<path d="M{ox},{round(sy,1)} L{ox},{round(sy + SYS_GAP,1)}" '
                       f'stroke="{SYS_EDGE}" stroke-width="2"/>')
            op_circle(ox, oy, "+", False)
            sy += SYS_GAP
        sy = draw_sys(sp, x + TPAD, sy, p["body_w"])

# ── 항과 항을 잇는 × 다섯 개 — 한 세로축에 세운다
cx = W / 2
for a, b in zip(ORDER, ORDER[1:]):
    y0 = cards[a]["y"] + cards[a]["h"]
    y1 = cards[b]["y"]
    out.append(f'<path d="M{cx},{round(y0,1)} L{cx},{round(y1,1)}" stroke="{TERM_EDGE}" '
               'stroke-width="2"/>')
    op_circle(cx, (y0 + y1) / 2, "×", True)

# ── 실제 업무 순환: 상황 변화에 따른 실행·검증·재검토 ────────────────
out.append(f'<rect x="{MARGIN}" y="{LOOP_Y}" width="{FULL_W}" height="{LOOP_H}" '
           f'rx="12" fill="{TITLE_BG}" stroke="{SYS_EDGE}"/>')
out.append(f'<text x="{MARGIN + 24}" y="{LOOP_Y + 35}" font-size="23" '
           f'font-weight="700" fill="{INK}">사건이 진행되는 동안 반복</text>')
loop_labels = ["상황 갱신", "대안·조건부 전략", "권한·제약·전문 검토", "실행·외부 결과", "반증·성과 확인"]
node_w = (FULL_W - 100) / 5
node_y = LOOP_Y + 58
for index, label in enumerate(loop_labels):
    node_x = MARGIN + 24 + index * (node_w + 13)
    out.append(f'<rect x="{node_x}" y="{node_y}" width="{node_w}" height="48" '
               f'rx="8" fill="{CHIP_BG}" stroke="{CHIP_EDGE}"/>')
    out.append(f'<text x="{node_x + node_w / 2}" y="{node_y + 31}" text-anchor="middle" '
               f'font-size="19" fill="{INK}">{esc(label)}</text>')
    if index < 4:
        out.append(f'<text x="{node_x + node_w + 2}" y="{node_y + 30}" '
                   f'font-size="17" fill="{SUB}">→</text>')
left = MARGIN + 24 + node_w / 2
right = MARGIN + 24 + 4 * (node_w + 13) + node_w / 2
base_y = node_y + 77
out.append(f'<path d="M{right},{node_y + 48} V{base_y} H{left} V{node_y + 48} '
           f'm-6,8 l6,-8 l6,8" fill="none" stroke="{CHIP_EDGE}" stroke-width="2"/>')
out.append(f'<text x="{W / 2}" y="{base_y + 28}" text-anchor="middle" font-size="19" '
           f'fill="{SUB}">새 증거·상대 반응·이견·다른 건으로 번지는 손해 → 영향받는 판단과 작업 재검토</text>')
out.append("</svg>")
path = Path(__file__).with_name("전개-수식.svg")
with path.open("w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"{path}  {W}x{H}")
