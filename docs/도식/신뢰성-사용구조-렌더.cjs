const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/homebrew/lib/node_modules/playwright');
const root = path.resolve(__dirname, '../..');
const base = path.join(root, 'docs/images/expert-definition/judgment-reliability-usage');
const out = process.argv[2] || '/tmp/judgment-reliability-review';

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1800, height: 1200 }, deviceScaleFactor: 1 });
    await page.setContent('<body style="margin:0;background:white">' + fs.readFileSync(base + '.svg', 'utf8') + '</body>');
    await page.evaluate(() => document.fonts.ready);
    const geometry = await page.evaluate(() => {
      const rect = el => { const r = el.getBoundingClientRect(); return { x:r.x, y:r.y, w:r.width, h:r.height }; };
      return {
        nodes: [...document.querySelectorAll('.node')].map(el => ({
          id:el.dataset.id, ...rect(el.querySelector('.shape')),
          texts:[...el.querySelectorAll('text')].map(t => ({ text:t.textContent, ...rect(t) })),
        })),
        labels:[...document.querySelectorAll('.edge-label')].map(el => ({ id:el.dataset.id, ...rect(el) })),
        sections:[...document.querySelectorAll('.section')].map(el=>rect(el)),
        arrows:document.querySelectorAll('.edge[marker-end]').length,
        portalLinks:[...document.querySelectorAll('.portal a')].map(el=>el.getAttribute('href')),
      };
    });
    fs.writeFileSync(path.join(out, 'geometry.json'), JSON.stringify(geometry, null, 2));
    await page.screenshot({ path:base + '.png', fullPage:true });
    await page.addStyleTag({ content:'body > svg {width:1080px;height:auto;display:block}' });
    await page.setViewportSize({ width:1080, height:1200 });
    const height = await page.evaluate(()=>document.body.scrollHeight);
    for (let y=0, i=0; y<height; y+=1100, i++) {
      await page.evaluate(y=>scrollTo(0,y),y);
      await page.screenshot({ path:path.join(out,`view-${String(i).padStart(2,'0')}.png`) });
    }
    console.log(JSON.stringify({ png:base + '.png', nodes:geometry.nodes.length, arrows:geometry.arrows, previews:Math.ceil(height/1100) }));
  } finally { await browser.close(); }
})().catch(error=>{ console.error(error); process.exit(1); });
