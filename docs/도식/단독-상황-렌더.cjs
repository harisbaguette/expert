const fs=require('fs'),path=require('path'),crypto=require('crypto');
const pp=require(process.env.PUPPETEER_MODULE||'puppeteer');
const root=path.resolve(__dirname,'../..');
const dir=process.argv[2]||'/tmp/solo-flow-review';fs.mkdirSync(dir,{recursive:true});
(async()=>{const browser=await pp.launch({headless:true});try{
 const page=await browser.newPage();
 const src=path.join(root,'docs/images/expert-definition/solo-one-expert-flow.svg');
 const svg=fs.readFileSync(src,'utf8');const width=+svg.match(/width="([\d.]+)"/)[1];const height=+svg.match(/height="([\d.]+)"/)[1];
 await page.setViewport({width,height:1080,deviceScaleFactor:1});
 await page.setContent('<body style="margin:0;background:#fff">'+svg+'</body>');
 await page.evaluate(()=>document.fonts.ready);
 const measured=await page.evaluate(()=>{const r=e=>{const a=e.getBoundingClientRect();return{x:a.x,y:a.y,w:a.width,h:a.height}};
 return{nodes:[...document.querySelectorAll('.node')].map(n=>({id:n.dataset.id,material:n.dataset.material,shape:r(n.querySelector('.shape')),texts:[...n.querySelectorAll('text')].map(t=>({text:t.textContent,...r(t)}))})),
 labels:[...document.querySelectorAll('.edge-label')].map(e=>({id:e.dataset.edge,...r(e)})),
 annotations:[...document.querySelectorAll('.annotation text,.scope text')].map(e=>({text:e.textContent,...r(e)}))};});
 measured.browser=await browser.version();measured.svg_sha256=crypto.createHash('sha256').update(svg).digest('hex');
 fs.writeFileSync(path.join(dir,'geometry.json'),JSON.stringify(measured,null,2));
 if(!process.env.FAST_RENDER){await page.screenshot({path:path.join(dir,'solo-one-expert-flow.png'),fullPage:true});
 for(let y=0,i=0;y<height;y+=1000,i++){await page.evaluate(y=>scrollTo(0,y),y);await page.screenshot({path:path.join(dir,`detail-${i}.png`)});}}
 console.log(JSON.stringify({width,height,nodes:measured.nodes.length,dir}));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
