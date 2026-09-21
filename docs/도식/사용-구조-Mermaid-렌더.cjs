#!/usr/bin/env node
/* Render native Mermaid without editing its generated SVG.
 * PUPPETEER_MODULE and MERMAID_BUNDLE can use existing local installations.
 * Usage: node 사용-구조-Mermaid-렌더.cjs [output-directory] [solo orchestration complex]
 */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const out = path.resolve(process.argv[2] || '/tmp/expert-usage-mermaid');
fs.mkdirSync(out,{recursive:true});
const pp = require(process.env.PUPPETEER_MODULE || 'puppeteer');
const crypto = require('crypto');

(async () => {
  const browser = await pp.launch({headless:true});
  try {
    const page = await browser.newPage();
    await page.setViewport({width:1920,height:1080});
    await page.setContent('<body style="margin:0;padding:32px;background:#191d25"></body>');
    await page.addScriptTag({path:process.env.MERMAID_BUNDLE || '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/mermaid-markdown-features/markdown-preview-out/index.js'});
    await page.evaluate(async () => {
      await registerMermaidAddons();
      mermaid_default.initialize({startOnLoad:false,securityLevel:'strict'});
    });
    for (const name of (process.argv.length>3?process.argv.slice(3):['solo','orchestration','complex'])) {
      const source = fs.readFileSync(path.join(process.env.MERMAID_SOURCE_DIR || path.join(root,'docs/도식'),`usage-structure-${name}.mmd`),'utf8');
      const result = await page.evaluate(async source => {
        const rendered = await mermaid_default.render('chart',source);
        document.body.innerHTML = rendered.svg;
        await document.fonts.ready;
        const svg = document.querySelector('svg');
        const xml = new XMLSerializer().serializeToString(svg);
        svg.style.width='100%';
        const vb = svg.viewBox.baseVal;
        svg.style.maxWidth=vb.width+'px';
        const inv = svg.getScreenCTM().inverse();
        const point = (x,y) => {const p = new DOMPoint(x,y).matrixTransform(inv);return [p.x,p.y]};
        const rect = e => {const r=e.getBoundingClientRect();const a=point(r.left,r.top),b=point(r.right,r.bottom);return {x:a[0],y:a[1],w:b[0]-a[0],h:b[1]-a[1]}};
        const visible = e => {const c=getComputedStyle(e);return c.visibility!=='hidden'&&c.stroke!=='none'&&c.opacity!=='0'};
        const nodes=[...svg.querySelectorAll('g.node')].map(e=>({id:e.id,key:e.id.replace(/^.*?flowchart-/,'').replace(/-\d+$/,''),text:e.textContent,...rect(e.querySelector(':scope > .label-container')||e),label:[...e.querySelectorAll('b,small,.kind')].map(t=>({text:t.textContent,...rect(t)}))}));
        const groups=[...svg.querySelectorAll('g.cluster')].map(e=>({text:e.querySelector('.cluster-label')?.textContent,...rect(e.querySelector(':scope > rect')),title:e.querySelector('.cluster-label')?rect(e.querySelector('.cluster-label')):null}));
        const labels=[...svg.querySelectorAll('g.edgeLabel')].filter(e=>e.textContent.trim()).map(e=>({text:e.textContent,...rect(e)}));
        const edges=[...svg.querySelectorAll('path.flowchart-link')].filter(visible).map(e=>{
          const l=e.getTotalLength(), points=[],m=e.getScreenCTM();
          for(let s=0;s<=l;s+=Math.min(7,l||1)){const p=e.getPointAtLength(s).matrixTransform(m);points.push(point(p.x,p.y));}
          const p=e.getPointAtLength(l).matrixTransform(m);points.push(point(p.x,p.y));
          return {id:e.id,class:e.getAttribute('class'),style:e.getAttribute('style'),start:getComputedStyle(e).markerStart==='none'?null:getComputedStyle(e).markerStart,end:getComputedStyle(e).markerEnd==='none'?null:getComputedStyle(e).markerEnd,points,...rect(e)};
        });
        return {svg:xml,width:vb.width,height:vb.height,display_scale:svg.getScreenCTM().a,display_height:svg.getBoundingClientRect().height,nodes,groups,labels,edges};
      }, source);
      result.source_sha256=crypto.createHash('sha256').update(source).digest('hex');
      result.browser=await browser.version();
      fs.writeFileSync(path.join(out,`${name}-mermaid.svg`),result.svg);
      delete result.svg;
      fs.writeFileSync(path.join(out,`${name}-mermaid-geometry.json`),JSON.stringify(result,null,2));
      if(!process.env.FAST_RENDER){
      await page.screenshot({path:path.join(out,`${name}-mermaid.png`),fullPage:true});
      for(let y=0,i=0;y<result.display_height;y+=1000,i++){
        await page.evaluate(y=>window.scrollTo(0,y),y);
        await page.screenshot({path:path.join(out,`${name}-mermaid-detail-${i}.png`)});
      }
      await page.evaluate(()=>window.scrollTo(0,0));}
      console.log(name,result.width,result.height,result.nodes.length,result.edges.length,result.display_scale);
    }
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
