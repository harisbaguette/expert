const fs=require('fs'),path=require('path'),crypto=require('crypto');
const usePlaywright=Boolean(process.env.PLAYWRIGHT_MODULE);
const pp=usePlaywright?require(process.env.PLAYWRIGHT_MODULE).chromium:require(process.env.PUPPETEER_MODULE||'puppeteer');
const root=path.resolve(__dirname,'../..');
const dir=process.argv[2]||'/tmp/solo-material-relations';fs.mkdirSync(dir,{recursive:true});
(async()=>{const browser=await pp.launch({headless:true});try{
 const page=await browser.newPage();
 const setViewport=size=>usePlaywright?page.setViewportSize(size):page.setViewport(size);
 const svg=fs.readFileSync(path.join(root,'docs/images/expert-definition/solo-material-relations.svg'),'utf8');
 const width=+svg.match(/width="([\d.]+)"/)[1],height=+svg.match(/height="([\d.]+)"/)[1];
 await setViewport({width,height:1000});
 await page.setContent('<body style="margin:0;background:white">'+svg+'</body>');
 await page.evaluate(()=>document.fonts.ready);
 const measured=await page.evaluate(()=>{const rect=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}};
 return{scopes:[...document.querySelectorAll('.scope-border')].map(n=>({id:n.dataset.id,...rect(n)})),
 scope_headers:[...document.querySelectorAll('.scope-header-band')].map(n=>({scope:n.dataset.scope,...rect(n)})),
 nodes:[...document.querySelectorAll('.node,.material')].map(n=>({id:n.dataset.id,shape:rect(n.querySelector('.shape')),texts:[...n.querySelectorAll(':scope > text')].map(t=>({text:t.textContent,role:t.getAttribute('class'),...rect(t)}))})),
 labels:[...document.querySelectorAll('.edge-label')].map(e=>({id:e.dataset.edge,...rect(e)})),
 bridges:[...document.querySelectorAll('.edge-bridge')].map(e=>({over:e.dataset.over,under:e.dataset.under,...rect(e)})),
 arrowheads:[...document.querySelectorAll('.arrowhead')].map(e=>({id:e.dataset.edge,...rect(e)})),
 system_labels:[...document.querySelectorAll('.system-label')].map(e=>({id:e.parentElement.dataset.id,text:e.textContent,...rect(e)})),
 illustration_count:document.querySelectorAll('image,use,img').length,
 annotations:[...document.querySelectorAll('text.annotation,.scope > text')].map(e=>({text:e.textContent,...rect(e)}))};});
 measured.svg_sha256=crypto.createHash('sha256').update(svg).digest('hex');measured.browser=await browser.version();
 fs.writeFileSync(path.join(dir,'geometry.json'),JSON.stringify(measured,null,2));
 if(!process.env.FAST_RENDER){
  await page.screenshot({path:path.join(dir,'solo-material-relations.png'),fullPage:true});
  await page.addStyleTag({content:'body > svg {width:1100px;height:auto;display:block}'});
  await setViewport({width:1100,height:1000});
  for(let y=0,i=0;y<height*1100/width;y+=900,i++){
   await page.evaluate(y=>scrollTo(0,y),y);await page.screenshot({path:path.join(dir,`normal-${i}.png`)});
  }
 }
 console.log(JSON.stringify({width,height,dir}));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
