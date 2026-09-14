// Browser checks of generated local views; screenshots support human review.
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const crypto = require('node:crypto');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../..');
const out = path.join(__dirname, 'rendered');
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
async function checkViews(page) {
  const results=[];
  for (const name of ['전문가 에이전트 정의', '진행-계획']) {
    for (const width of [1280, 390]) {
      await page.setViewportSize({ width, height:1000 });
      await page.goto(pathToFileURL(path.join(root, name+'.html')).href);
      await page.evaluate(() => document.fonts.ready);
      const check = await page.evaluate(() => ({
        documentWidth: document.documentElement.scrollWidth, viewport: innerWidth,
        brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).length,
        diagrams: document.querySelectorAll('.diagram').length,
        tables: document.querySelectorAll('table').length,
        headingIdsUnique: (()=>{ const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.length===new Set(ids).size; })()
      }));
      if (check.documentWidth > width || check.brokenImages || !check.headingIdsUnique) throw new Error(JSON.stringify({name,width,check}));
      results.push({name,width,...check});
      if (name === '전문가 에이전트 정의') {
        const h = page.locator('h2').filter({hasText:'계통별 재료'});
        await h.scrollIntoViewIfNeeded();
        await page.screenshot({path:path.join(out,`materials-${width}.png`)});
      }
    }
  }
  return results;
}

async function checkFormula(page) {
  await page.setViewportSize({width:1446,height:1000});
  const formula=path.join(root,'docs/전개-수식/전개-수식.svg');
  await page.goto('about:blank');
  await page.setContent('<!doctype html><body style="margin:0">'+fs.readFileSync(formula,'utf8')+'</body>');
  const formulaBounds=await page.evaluate(()=>{const svg=document.querySelector('svg');const box=svg.getBBox();const v=svg.viewBox.baseVal;return {x:box.x,y:box.y,width:box.width,height:box.height,viewWidth:v.width,viewHeight:v.height};});
  if (formulaBounds.x<0 || formulaBounds.y<0 || formulaBounds.x+formulaBounds.width>formulaBounds.viewWidth+1 || formulaBounds.y+formulaBounds.height>formulaBounds.viewHeight+1) throw new Error('Formula outside viewBox');
  await page.locator('svg').screenshot({path:path.join(out,'formula.png')});
  return formulaBounds;
}

async function checkDiagrams(page) {
  const manifest=JSON.parse(fs.readFileSync(path.join(out,'manifest.json')));
  const svgChecks=[];
  for (const d of manifest.diagrams) {
    await page.setViewportSize({width:Math.ceil(d.viewBox[2]),height:1000});
    await page.setContent('<!doctype html><body style="margin:0">'+fs.readFileSync(path.join(out,d.file),'utf8')+'</body>');
    const labels=await page.evaluate(()=> [...document.querySelectorAll('foreignObject')].map(e=>{
      const content=e.firstElementChild, r=content?.getBoundingClientRect(), box=e.getBoundingClientRect();
      return {width:r?.width||0,height:r?.height||0,boxWidth:box.width,boxHeight:box.height};
    }));
    const clipped=labels.filter(l=>l.width>l.boxWidth+2 || l.height>l.boxHeight+2).length;
    if(clipped) throw new Error(`${d.file}: ${clipped} clipped labels`);
    svgChecks.push({file:d.file,labels:labels.length,clippedLabels:clipped});
    if(['diagram-4.svg','diagram-5.svg','diagram-6.svg','diagram-7.svg'].includes(d.file)) {
      await page.locator('svg').screenshot({path:path.join(out,d.file.replace('.svg','.png'))});
    }
  }
  return svgChecks;
}

async function main() {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_EXECUTABLE || chromium.executablePath() });
  const errors = [];
  try {
    const page = await browser.newPage({ viewport: { width:1280, height:1000 }, deviceScaleFactor:1 });
    await page.route('http://**/*', r => r.abort());
    await page.route('https://**/*', r => r.abort());
    page.on('pageerror', e => errors.push(String(e)));
    const results=await checkViews(page);
    const formulaBounds=await checkFormula(page);
    const svgChecks=await checkDiagrams(page);
    const report={kind:'local browser layout checks; screenshots require human inspection',browser:browser.version(),viewports:results,formula:formulaBounds,mermaid:svgChecks,pageErrors:errors,sha256:{definition_html:sha(path.join(root,'전문가 에이전트 정의.html')),progress_html:sha(path.join(root,'진행-계획.html')),formula_svg:sha(path.join(root,'docs/전개-수식/전개-수식.svg'))}};
    fs.writeFileSync(path.join(out,'visual-check.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({views:results.length,diagrams:svgChecks.length,errors:errors.length}));
  } finally {await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
