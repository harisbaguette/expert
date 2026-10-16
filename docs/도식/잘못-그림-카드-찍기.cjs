let pw; try{pw=require('playwright')}catch(e){pw=require('/opt/homebrew/lib/node_modules/playwright')}
(async()=>{const b=await pw.chromium.launch();const p=await b.newPage({deviceScaleFactor:2,viewport:{width:600,height:900}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(300);
for(let i=0;i<4;i++){await (await p.$('#c'+i)).screenshot({path:process.argv[3]+'/c'+i+'@2x.png'});}
await b.close();})();
