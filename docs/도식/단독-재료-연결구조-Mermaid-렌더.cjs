#!/usr/bin/env node
/* 단독 상황 Mermaid 블록을 실제 브라우저에서 렌더해 SVG·좌표·스크린샷을 남긴다.
 * 창을 띄우지 않는다(headless). Playwright 를 쓴다 — 이 PC 에 전역 설치돼 있다.
 * 사용법: node 단독-재료-연결구조-Mermaid-렌더.cjs <mmd 파일> <출력 폴더>
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const BUNDLE = process.env.MERMAID_BUNDLE
  || '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/mermaid-markdown-features/markdown-preview-out/index.js';

(async () => {
  const src = path.resolve(process.argv[2]);
  const out = path.resolve(process.argv[3] || '/tmp/solo-mermaid');
  fs.mkdirSync(out, { recursive: true });
  const source = fs.readFileSync(src, 'utf8');

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
    await page.setContent('<body style="margin:0;padding:24px;background:#ffffff"></body>');
    await page.addScriptTag({ path: BUNDLE });
    await page.evaluate(async () => {
      await registerMermaidAddons();
      mermaid_default.initialize({ startOnLoad: false, securityLevel: 'strict' });
    });
    const result = await page.evaluate(async (source) => {
      let rendered;
      try {
        rendered = await mermaid_default.render('chart', source);
      } catch (err) {
        return { error: String(err && err.message || err) };
      }
      document.body.innerHTML = rendered.svg;
      await document.fonts.ready;
      const svg = document.querySelector('svg');
      const xml = new XMLSerializer().serializeToString(svg);
      const vb = svg.viewBox.baseVal;
      svg.style.width = vb.width + 'px';
      svg.style.maxWidth = 'none';
      svg.style.height = vb.height + 'px';
      const inv = svg.getScreenCTM().inverse();
      const pt = (x, y) => { const p = new DOMPoint(x, y).matrixTransform(inv); return [p.x, p.y]; };
      const rect = (e) => {
        const r = e.getBoundingClientRect();
        const a = pt(r.left, r.top), b = pt(r.right, r.bottom);
        return { x: a[0], y: a[1], w: b[0] - a[0], h: b[1] - a[1] };
      };
      const nodes = [...svg.querySelectorAll('g.node')].map((e) => ({
        id: e.id.replace(/^.*?flowchart-/, '').replace(/-\d+$/, ''),
        text: e.textContent,
        ...rect(e.querySelector(':scope > .label-container') || e),
        labels: [...e.querySelectorAll('b, small')].map((t) => ({ text: t.textContent, ...rect(t) })),
      }));
      const clusters = [...svg.querySelectorAll('g.cluster')].map((e) => ({
        id: e.id, text: e.querySelector('.cluster-label')?.textContent || '',
        ...rect(e.querySelector(':scope > rect') || e),
      }));
      const edgeLabels = [...svg.querySelectorAll('g.edgeLabel')]
        .filter((e) => e.textContent.trim()).map((e) => ({ text: e.textContent, ...rect(e) }));
      const edges = [...svg.querySelectorAll('path.flowchart-link')].map((e) => {
        const l = e.getTotalLength(), points = [], m = e.getScreenCTM();
        for (let s = 0; s <= l; s += Math.min(9, l || 1)) {
          const p = e.getPointAtLength(s).matrixTransform(m); points.push(pt(p.x, p.y));
        }
        const p = e.getPointAtLength(l).matrixTransform(m); points.push(pt(p.x, p.y));
        return {
          id: e.id, style: e.getAttribute('style'),
          end: getComputedStyle(e).markerEnd === 'none' ? null : getComputedStyle(e).markerEnd,
          points,
        };
      });
      return { svg: xml, width: vb.width, height: vb.height, nodes, clusters, edgeLabels, edges };
    }, source);

    if (result.error) { console.error('MERMAID ERROR:', result.error); process.exit(2); }
    fs.writeFileSync(path.join(out, 'solo-mermaid.svg'), result.svg);
    const geom = { ...result }; delete geom.svg;
    fs.writeFileSync(path.join(out, 'solo-mermaid-geometry.json'), JSON.stringify(geom, null, 2));
    if (!process.env.FAST_RENDER) {
      await page.setViewportSize({
        width: Math.min(4000, Math.ceil(result.width) + 48),
        height: Math.min(4000, Math.ceil(result.height) + 48),
      });
      await page.screenshot({ path: path.join(out, 'solo-mermaid.png'), fullPage: true });
    }
    console.log(JSON.stringify({
      width: Math.round(result.width), height: Math.round(result.height),
      nodes: result.nodes.length, clusters: result.clusters.length,
      edges: result.edges.length, edgeLabels: result.edgeLabels.length,
      arrowless: result.edges.filter((e) => !e.end).length,
    }));
  } finally { await browser.close(); }
})().catch((e) => { console.error(e); process.exit(1); });
