# Generates work-flow.svg — the one-glance overview of the work flow (straight spine + return arcs).
# Run: python3 docs/work-flow-gen.py  (then check the render before committing)
NS = "http://" + "www.w3.org/2000/svg"
W = 1440
H = 485
BW = 132
BH = 64
GAP = 14
X0 = 100
Y = 215
steps = [("0 감지·접수", "받을지 정한다"), ("1 의도 파악", "끝을 정한다"), ("2 문제 정의", "풀 문제를 짚는다"),
         ("3 자료 확인", "사실을 가른다"), ("4 판단·계획", "끝까지 그려 본다"), ("5 처리", "결과물을 만든다"),
         ("6 검증", "실제 상태를 본다"), ("7 완료·보고", "그대로 쓰게 낸다"), ("8 남기기", "다음 건에 남긴다")]


def cx(i):
    return X0 + i * (BW + GAP) + BW / 2


top = Y - BH / 2
bot = Y + BH / 2
FONT = 'font-family="Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR, sans-serif"'
o = [f'<svg xmlns="{NS}" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>']
o.append('<defs>'
         '<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#334155"/></marker>'
         '<marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b45309"/></marker>'
         '<marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#dc2626"/></marker>'
         '</defs>')
o.append(f'<rect width="{W}" height="{H}" fill="white"/>')
o.append(f'<text x="{W - 10}" y="{H - 8}" text-anchor="end" font-size="12" fill="#475569">실선 = 앞으로 가는 길 · 주황 점선 = 되돌아가는 길 · 빨강 = 사람에게 넘기거나 급한 길</text>')

# start circle and spine
sx = 36
o.append(f'<circle cx="{sx}" cy="{Y}" r="24" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>'
         f'<text x="{sx}" y="{Y + 5}" text-anchor="middle" font-size="14" fill="#14532d">시작</text>')
o.append(f'<line x1="{sx + 24}" y1="{Y}" x2="{cx(0) - BW / 2 - 2}" y2="{Y}" stroke="#334155" stroke-width="2" marker-end="url(#a)"/>')
for i, (a, b) in enumerate(steps):
    x = cx(i) - BW / 2
    o.append(f'<rect x="{x}" y="{top}" width="{BW}" height="{BH}" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>')
    o.append(f'<text x="{cx(i)}" y="{Y - 4}" text-anchor="middle" font-size="15" font-weight="700" fill="#17314f">{a}</text>')
    o.append(f'<text x="{cx(i)}" y="{Y + 18}" text-anchor="middle" font-size="13" fill="#17314f">{b}</text>')
    if i < 8:
        o.append(f'<line x1="{x + BW}" y1="{Y}" x2="{x + BW + GAP - 2}" y2="{Y}" stroke="#334155" stroke-width="2" marker-end="url(#a)"/>')


def lab(x, y, t, col, size=12.5):
    w = len(t) * size * 0.95 + 10
    o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="18" rx="3" fill="white"/>')
    o.append(f'<text x="{x}" y="{y + 3}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')


def arc(f, t, h, label, so, to, above, k=None):
    fx, tx = cx(f) + so, cx(t) + to
    if above:
        y0, c, yend = top, top - h * 1.3, top - 2
    else:
        y0, c, yend = bot, bot + h * 1.3, bot + 2
    o.append(f'<path d="M{fx},{y0} C{fx},{c} {tx},{c} {tx},{yend}" fill="none" stroke="#b45309" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#r)"/>')
    # label near the source end for long arcs so neighbouring labels do not pile up at the apex
    if k is None:
        k = 0.5 if abs(f - t) == 1 else 0.28
    u = 1 - k
    lx = u ** 3 * fx + 3 * u * u * k * fx + 3 * u * k * k * tx + k ** 3 * tx
    ly = u ** 3 * y0 + 3 * u * u * k * c + 3 * u * k * k * c + k ** 3 * yend
    lab(lx, ly - 12 if above else ly + 12, label, "#92400e")


# returns above the spine (longer arcs start further toward the target, land further away)
arc(2, 1, 40, "문제가 달라졌다", -30, 20, True)
arc(4, 2, 72, "방식이 틀렸다", -35, 10, True)
arc(5, 4, 34, "같은 실패 두 번", -35, 0, True)
arc(6, 5, 40, "처리가 틀렸다", 25, 0, True)
arc(6, 4, 82, "판단이 틀렸다", -5, 30, True, k=0.72)
arc(6, 3, 110, "자료가 틀렸다", -35, 0, True, k=0.5)
arc(7, 5, 145, "고쳐 달라", -25, 30, True)
# long returns below the spine
arc(7, 1, 168, "범위가 바뀌었다", 40, 0, False)
arc(8, 0, 208, "기억은 다음 건의 0으로 이어진다", 40, -30, False)

# human hand-off box below 4-5
hx = (cx(4) + cx(5)) / 2 - 20
hy = bot + 60
hw = 300
hh = 74
o.append(f'<rect x="{hx - hw / 2}" y="{hy}" width="{hw}" height="{hh}" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>')
o.append(f'<text x="{hx}" y="{hy + 22}" text-anchor="middle" font-size="14" font-weight="700" fill="#7f1d1d">사람에게 넘기기 — 다섯 경우에만 멈춘다</text>')
o.append(f'<text x="{hx}" y="{hy + 42}" text-anchor="middle" font-size="12.5" fill="#7f1d1d">되돌릴 수 없는 행동 · 승인 조건 · 판단이 안 섬</text>')
o.append(f'<text x="{hx}" y="{hy + 60}" text-anchor="middle" font-size="12.5" fill="#7f1d1d">한도 초과 · 자격자 전속 행위</text>')
for i in (4, 5):
    o.append(f'<line x1="{cx(i)}" y1="{bot}" x2="{cx(i)}" y2="{hy - 2}" stroke="#dc2626" stroke-width="1.8" marker-end="url(#s)"/>')
lab(hx + 20, bot + 30, "걸리면", "#7f1d1d")

# emergency box above 0-1
ex = cx(0) + 30
ey = top - 128
ew = 220
eh = 66
o.append(f'<rect x="{ex - ew / 2}" y="{ey}" width="{ew}" height="{eh}" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>')
o.append(f'<text x="{ex}" y="{ey + 20}" text-anchor="middle" font-size="14" font-weight="700" fill="#7f1d1d">긴급 경로</text>')
o.append(f'<text x="{ex}" y="{ey + 39}" text-anchor="middle" font-size="12.5" fill="#7f1d1d">피해가 분마다 커지면 1~3 건너뛰고</text>')
o.append(f'<text x="{ex}" y="{ey + 56}" text-anchor="middle" font-size="12.5" fill="#7f1d1d">되돌릴 수 있는 첫 조치부터</text>')
o.append(f'<path d="M{sx},{Y - 24} C{sx},{ey + eh / 2} {sx},{ey + eh / 2} {ex - ew / 2 - 2},{ey + eh / 2}" fill="none" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#s)"/>')
o.append(f'<line x1="{cx(1) - 40}" y1="{ey + eh + 2}" x2="{cx(1) - 40}" y2="{top - 2}" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#s)"/>')
lab(cx(1) - 40 - 50, top - 30, "피해가 멎으면", "#7f1d1d")

o.append('</svg>')
import os
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work-flow.svg'), 'w', encoding='utf-8').write('\n'.join(o))
print('written')
