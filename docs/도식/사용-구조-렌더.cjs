#!/usr/bin/env node
/* Render the exact published SVG and record real text bounds.
 * PUPPETEER_MODULE may point to an existing Puppeteer installation.
 * Usage: node 사용-구조-렌더.cjs [output-directory]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const pp = require(process.env.PUPPETEER_MODULE || 'puppeteer');
const root = path.resolve(__dirname, '../..');
const out = path.resolve(process.argv[2] || '/tmp/expert-usage-render');
fs.mkdirSync(out, {recursive: true});
(async () => {
  const browser = await pp.launch({headless: true});
  try {
    const page = await browser.newPage();
    for (const mode of ['solo', 'orchestration', 'complex']) {
      const source = path.join(root, 'docs/images/expert-definition', `usage-structure-${mode}.svg`);
      const svg = fs.readFileSync(source, 'utf8');
      const width = +svg.match(/width="([\d.]+)"/)[1];
      const height = +svg.match(/height="([\d.]+)"/)[1];
      await page.setViewport({width: Math.ceil(width), height: 1080});
      await page.setContent(`<html><body style="margin:0;background:#19212b">${svg}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate(() => scrollTo(0, 0));
      const geometry = await page.evaluate(() => {
        const rect = e => {const r = e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height};};
        return {
          nodes: [...document.querySelectorAll('.node')].map(e => ({id:e.dataset.id, material:e.dataset.material, shape:rect(e.querySelector('.shape')), texts:[...e.querySelectorAll('text')].map(t => ({text:t.textContent,...rect(t)}))})),
          labels: [...document.querySelectorAll('.edge-label')].map(e => ({id:e.dataset.edge,...rect(e)})),
          annotations: [...document.querySelectorAll('.annotation text,.scope text')].map(e => ({text:e.textContent,...rect(e)})),
          font_available: document.fonts.check('17px "Apple SD Gothic Neo"')
        };
      });
      geometry.svg_sha256 = crypto.createHash('sha256').update(svg).digest('hex');
      geometry.browser = await browser.version();
      geometry.source = path.relative(root, source);
      fs.writeFileSync(path.join(out, `${mode}-geometry.json`), JSON.stringify(geometry,null,2));
      await page.screenshot({path:path.join(out,`${mode}.png`),fullPage:true});
      for (let y=0, i=0; y<height; y+=1000, i++) {
        await page.evaluate(y => scrollTo(0,y),y);
        await page.screenshot({path:path.join(out,`${mode}-detail-${i}.png`)});
      }
      console.log(`${mode}: rendered ${geometry.nodes.length} nodes`);
    }
  } finally {await browser.close();}
})().catch(e => {console.error(e); process.exitCode=1;});
