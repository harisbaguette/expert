#!/usr/bin/env node
/* 정의 2의 Mermaid 순서도를 VS Code 미리보기와 같은 엔진으로 그려 선 겹침을 잰다.
 * 쓰는 법: node docs/도식/정의2-순서도-검증.cjs [그림 번호 쉼표목록] [--png 저장폴더]
 * 환경 변수: PLAYWRIGHT_MODULE(기본 playwright), CHROME_PATH, MERMAID_BUNDLE
 * 잰 것: 선끼리 교차, 선이 남의 상자를 지남, 글이 상자·다른 글·다른 선과 겹침, 나란히 겹친 선(이 넷이 0이 아니면 종료 코드 1), 시작 상자가 맨 위인지(참고만)
 */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const doc = path.join(root, '전문가 에이전트 정의 2.md');
const bundle = process.env.MERMAID_BUNDLE || '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/mermaid-markdown-features/markdown-preview-out/index.js';
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pw;
try { pw = require(process.env.PLAYWRIGHT_MODULE || 'playwright'); } catch (e) { pw = require('/opt/homebrew/lib/node_modules/playwright'); }
const { chromium } = pw;

const args = process.argv.slice(2);
const pngIdx = args.indexOf('--png');
const pngDir = pngIdx >= 0 ? path.resolve(args.splice(pngIdx, 2)[1]) : null;
const only = args[0] ? args[0].split(',').map(Number) : null;

const blocks = [];
{
  const lines = fs.readFileSync(doc, 'utf8').split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].startsWith('```mermaid')) continue;
    let j = i + 1;
    while (!lines[j].startsWith('```')) j++;
    blocks.push({ line: i + 2, src: lines.slice(i + 1, j).join('\n') + '\n' });
    i = j;
  }
}

async function measure(src) {
  const el = document.getElementById('o');
  let out;
  try { out = await mermaid_default.render('g' + Math.random().toString(36).slice(2), src); } catch (e) { return { error: String(e).slice(0, 200) }; }
  el.innerHTML = out.svg;
  const svg = el.querySelector('svg');
  const nodes = {};
  svg.querySelectorAll('g.node').forEach(g => {
    const id = (g.id.match(/flowchart-(.+)-\d+$/) || [])[1] || g.id;
    const b = g.getBoundingClientRect();
    nodes[id] = { x: b.x, y: b.y, w: b.width, h: b.height };
  });
  const edges = [];
  svg.querySelectorAll('path.flowchart-link').forEach(p => {
    const m0 = p.id.replace(/^.*?-L_/, '').replace(/_\d+$/, '');
    let ls = '', le = '';
    for (const k in nodes) if (m0.startsWith(k + '_') && nodes[m0.slice(k.length + 1)] !== undefined) { ls = k; le = m0.slice(k.length + 1); break; }
    const L = p.getTotalLength(), n = Math.max(8, Math.ceil(L / 3)), m = p.getScreenCTM(), pts = [];
    for (let i = 0; i <= n; i++) { const q = p.getPointAtLength(L * i / n); const s = new DOMPoint(q.x, q.y).matrixTransform(m); pts.push([s.x, s.y]); }
    edges.push({ ls, le, pts, id: p.id });
  });
  const labels = [];
  svg.querySelectorAll('g.edgeLabel').forEach(g => {
    const t = g.textContent.trim(); if (!t) return;
    const b = g.getBoundingClientRect();
    labels.push({ t, x: b.x, y: b.y, w: b.width, h: b.height, id: (g.querySelector('[data-id]') || { getAttribute: () => '' }).getAttribute('data-id') });
  });
  const r0 = svg.getBoundingClientRect();
  return { w: r0.width, h: r0.height, nodes, edges, labels };
}

function score(r) {
  const E = r.edges;
  const o = (p, q, s) => (q[0] - p[0]) * (s[1] - p[1]) - (q[1] - p[1]) * (s[0] - p[0]);
  const seg = (a, b, c, d) => o(c, d, a) * o(c, d, b) < 0 && o(a, b, c) * o(a, b, d) < 0;
  const inN = (p, n, pad) => p[0] > n.x - pad && p[0] < n.x + n.w + pad && p[1] > n.y - pad && p[1] < n.y + n.h + pad;
  const ov = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
  const cross = [], thru = [], lab = [], par = [];
  for (let i = 0; i < E.length; i++) for (let j = i + 1; j < E.length; j++) {
    const a = E[i], b = E[j];
    const shared = [a.ls, a.le].filter(x => x === b.ls || x === b.le).map(k => r.nodes[k]);
    let hit = false;
    for (let s = 0; s < a.pts.length - 1 && !hit; s++) for (let t = 0; t < b.pts.length - 1; t++)
      if (seg(a.pts[s], a.pts[s + 1], b.pts[t], b.pts[t + 1]) && !shared.some(n => inN(a.pts[s], n, 14))) { hit = true; break; }
    if (hit) cross.push(`${a.ls}>${a.le} x ${b.ls}>${b.le}`);
    if (a.ls !== b.ls && a.le !== b.le) {
      let len = 0;
      for (let s = 0; s < a.pts.length - 1; s += 2) for (let t = 0; t < b.pts.length - 1; t += 2)
        if (Math.abs(a.pts[s][0] - b.pts[t][0]) < 4 && Math.abs(a.pts[s][1] - b.pts[t][1]) < 4) { len += 6; break; }
      if (len >= 60) par.push(`${a.ls}>${a.le} || ${b.ls}>${b.le}`);
    }
  }
  for (const e of E) for (const k in r.nodes) {
    if (k === e.ls || k === e.le) continue;
    if (e.pts.some(p => inN(p, r.nodes[k], -4))) thru.push(`${e.ls}>${e.le} thru ${k}`);
  }
  for (let i = 0; i < r.labels.length; i++) {
    const L = r.labels[i];
    for (const k in r.nodes) if (ov(L, r.nodes[k])) lab.push(`${L.t} ~ 상자 ${k}`);
    for (let j = i + 1; j < r.labels.length; j++) if (ov(L, r.labels[j])) lab.push(`${L.t} ~ ${r.labels[j].t}`);
    for (const e of E) {
      if (L.id && e.id.includes(L.id)) continue;
      if (e.pts.some(p => p[0] > L.x + 2 && p[0] < L.x + L.w - 2 && p[1] > L.y + 2 && p[1] < L.y + L.h - 2)) lab.push(`${L.t} ~ 선 ${e.ls}>${e.le}`);
    }
  }
  const inn = {}; for (const k in r.nodes) inn[k] = 0; for (const e of E) inn[e.le]++;
  const starts = Object.keys(r.nodes).filter(k => inn[k] === 0);
  const minY = Math.min(...Object.values(r.nodes).map(n => n.y));
  const startOff = starts.filter(k => r.nodes[k].y - minY > 6);
  return { cross, thru, lab, par, startOff };
}

(async () => {
  const browser = await chromium.launch({ executablePath: chrome });
  const page = await browser.newPage({ viewport: { width: 3000, height: 1200 } });
  await page.setContent('<html><body style="margin:0;background:#fff"><div id="o"></div></body></html>');
  await page.addScriptTag({ path: bundle });
  await page.evaluate(async () => { await registerMermaidAddons(); mermaid_default.initialize({ startOnLoad: false, securityLevel: 'strict' }); });
  if (pngDir) fs.mkdirSync(pngDir, { recursive: true });
  let bad = 0;
  for (let i = 0; i < blocks.length; i++) {
    if (only && !only.includes(i + 1)) continue;
    const r = await page.evaluate(measure, blocks[i].src);
    const name = String(i + 1).padStart(2, '0');
    if (r.error) { console.log(`${name} (줄 ${blocks[i].line}) 그리기 실패: ${r.error}`); bad++; continue; }
    const s = score(r);
    const flaw = s.cross.length + s.thru.length + s.lab.length + s.par.length;
    if (flaw) bad++;
    console.log(`${name} (줄 ${blocks[i].line}) ${Math.round(r.w)}x${Math.round(r.h)} 교차 ${s.cross.length} · 상자 관통 ${s.thru.length} · 글 겹침 ${s.lab.length} · 나란히 겹침 ${s.par.length} · 시작이 위가 아님(참고) ${s.startOff.length}`);
    for (const k of ['cross', 'thru', 'lab', 'par', 'startOff']) if (s[k].length) console.log('   ', k, s[k].join(' | '));
    if (pngDir) await (await page.$('#o svg')).screenshot({ path: path.join(pngDir, `${name}.png`) });
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
