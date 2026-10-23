// The Mermaid file owns wording, groups, colors and directed relationships.
// This compact, reproducible layout replaces only Mermaid's global auto-layout.
// Run: node docs/도식/reliability-solution-structure-render.cjs
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/homebrew/lib/node_modules/playwright');
const root = path.resolve(__dirname, '../..');
const base = path.join(root, 'docs/images/expert-definition/reliability-solution-structure');
const source = fs.readFileSync(path.join(__dirname, 'reliability-solution-structure.mmd'), 'utf8');
const bundle = process.env.MERMAID_BUNDLE || '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/mermaid-markdown-features/markdown-preview-out/index.js';
const W = 1560, FONT = 22, LH = 30;
const palette = {};
for (const match of source.matchAll(/^\s*classDef (\w+) (.+)$/gm)) {
 const value = key => match[2].match(new RegExp('(?:^|,)' + key + ':(#[0-9a-f]+)'))?.[1];
 palette[match[1]] = [value('fill'), value('stroke'), value('color')];
}
const nodes = {}, groups = {}, edges = [], linkStyles = {};
let currentGroup = null;
for (const line of source.split('\n')) {
  let m;
  if ((m=line.match(/^\s*subgraph (\w+)\["(.+)"\]/))) { currentGroup=m[1]; groups[currentGroup]={id:currentGroup,title:m[2],members:[]}; }
  else if (line.trim()==='end') currentGroup=null;
  else if ((m=line.match(/^\s*(\w+)(\(\[|\[\[|\{|\[)"(.+)"(?:\]\)|\]\]|\}|\]):::(\w+)/))) {
    nodes[m[1]]={id:m[1],shape:m[2],html:m[3],kind:m[4],group:currentGroup};
    if(currentGroup)groups[currentGroup].members.push(m[1]);
  } else if ((m=line.match(/^\s*(\w+) (-->(?:\|([^|]*)\|)?|~~~) (\w+)\s*$/))) edges.push({from:m[1],to:m[4],label:m[3]||'',hidden:m[2]==='~~~'});
  else if ((m=line.match(/^\s*linkStyle ([\d,]+) (.+)$/))) for (const i of m[1].split(','))linkStyles[i]=m[2];
}
for(let i=0;i<edges.length;i++) {
  const style=linkStyles[i]||'';
  edges[i].color=(style.match(/stroke:(#[\da-f]+)/)||[])[1]||'#60a5fa';
  edges[i].dash=(style.match(/stroke-dasharray:([\d ]+)/)||[])[1]||'';
  edges[i].key=edges[i].from+'>'+edges[i].to;
}
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try {
  const page=await browser.newPage({viewport:{width:W,height:1000},deviceScaleFactor:1});
  await page.setContent('<body style="margin:0;background:white"></body>');
  await page.addScriptTag({path:bundle});
  const measured=await page.evaluate(async({source,nodes})=>{
   await registerMermaidAddons();
   mermaid_default.initialize({startOnLoad:false,securityLevel:'strict'});
   await mermaid_default.parse(source);
   const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
   const sizes={};
   // Measure using the same locally available Korean font used by the SVG.
   for(const n of Object.values(nodes)) {
    sizes[n.id]={};
    let activeBold=false;
    for(const p of n.html.split(/<br\s*\/?\s*>/i)) {
     const bold=activeBold||p.includes('<b>'),text=p.replace(/<[^>]+>/g,'');
     activeBold=bold&&!p.includes('</b>');
     ctx.font=`${bold?700:400} 22px "Apple SD Gothic Neo", "Noto Sans CJK KR", sans-serif`;
     for(const c of text) sizes[n.id][(bold?'b':'n')+c]=ctx.measureText(c).width;
    }
   }
   return sizes;
  },{source,nodes});
  function linesFor(n,w) {
   const lines=[];
   let activeBold=false;
   for(const p of n.html.split(/<br\s*\/?\s*>/i)) {
    const bold=activeBold||p.includes('<b>'),text=p.replace(/<[^>]+>/g,'');
    activeBold=bold&&!p.includes('</b>');
    let line='',len=0;
    // Prefer word boundaries; split a long technical name only if unavoidable.
    const chunks=text.match(/\S+\s*|\s+/g)||[''];
    for(const word of chunks) {
     const width=[...word].reduce((a,c)=>a+(measured[n.id][(bold?'b':'n')+c]||11),0);
     if(line && len+width>w) {lines.push({text:line.trim(),bold});line='';len=0;}
     for(const c of word) {
      const cw=measured[n.id][(bold?'b':'n')+c]||11;
      if(line && len+cw>w) {lines.push({text:line.trim(),bold});line='';len=0;}
      if(!line && c===' ')continue;
      line+=c;len+=cw;
     }
    }
    if(line)lines.push({text:line.trim(),bold});
   }
   return lines;
  }
  function place(id,x,y,w,h=0) {
   const n=nodes[id];if(!n)throw Error('missing node '+id);
   n.lines=linesFor(n,w-(n.shape==='{'?w*0.48:32));
   Object.assign(n,{x,y,w,h:Math.max(h,(n.lines.length*LH+32)*(n.shape==='{'?1.75:1))});return n;
  }
  const bottom=n=>n.y+n.h, right=n=>n.x+n.w, midX=n=>n.x+n.w/2, midY=n=>n.y+n.h/2;
  function row(ids,x,y,width,gap=36) {
   const w=(width-gap*(ids.length-1))/ids.length;
   const arr=ids.map((id,i)=>place(id,x+i*(w+gap),y,w));
   const h=Math.max(...arr.map(n=>n.h));for(const n of arr)n.h=h;return y+h;
  }
  function group(id,x,y,w,end) {Object.assign(groups[id],{x,y,w,h:end-y});return groups[id];}
  const routes={};
  function route(from,to,pts,labelAt) {const key=from+'>'+to;if(routes[key])throw Error('duplicate route '+key);routes[key]={pts,labelAt};}
  const at=(id,side,offset=0)=>{
   const n=nodes[id]||groups[id];
   const inset=n.shape==='{'?(n.w/2)*Math.abs(offset)/(n.h/2):0;
   return side==='T'?[midX(n)+offset,n.y]:side==='B'?[midX(n)+offset,bottom(n)]:side==='L'?[n.x+inset,midY(n)+offset]:[right(n)-inset,midY(n)+offset];
  };
  function down(a,b,labelAt){route(a,b,[at(a,'B'),at(b,'T')],labelAt);}
  function across(a,b,labelAt){route(a,b,[at(a,'R'),at(b,'L')],labelAt);}
  // The preparation band is separate from the per-case processing path.
  let e=row(['P1','P15','P14','P13','P12'],88,76,1350,25);
  let py=e+92;
  place('P26',85,py,440);place('PUPDATE',650,py,350);place('W26',1080,py,350);
  const ph=Math.max(nodes.P26.h,nodes.PUPDATE.h,nodes.W26.h);for(const id of ['P26','PUPDATE','W26'])nodes[id].h=ph;
  let pb=Math.max(bottom(nodes.W26),bottom(nodes.P26),bottom(nodes.PUPDATE));
  group('PREP',65,26,1390,pb+90);
  for(const id of ['P1','P15','P14','P13','P12'])route(id,'P26',[at(id,'B'),[midX(nodes[id]),e+42],[305,e+42],at('P26','T')]);
  route('W26','PUPDATE',[at('W26','L'),at('PUPDATE','R')]);
  route('PUPDATE','P26',[at('PUPDATE','L'),at('P26','R')],[585,py-24]);
  place('START',530,bottom(groups.PREP)+100,400);
  route('P26','START',[at('P26','B'),[305,bottom(groups.PREP)+45],[730,bottom(groups.PREP)+45],at('START','T')],[475,bottom(groups.PREP)+20]);
  let y=bottom(nodes.START)+65;
  e=row(['C11','C13'],530,y+64,880,85);
  e=row(['C23','C16'],530,e+100,880,85);
  place('SCOPE',720,e+86,500);
  group('SCOPEL',500,y,940,bottom(nodes.SCOPE)+26);
  down('START','C11');across('C11','C13');
  let branchY=nodes.C23.y-50;
  route('C13','C23',[at('C13','B'),[midX(nodes.C13),branchY],[midX(nodes.C23),branchY],at('C23','T')],[760,branchY-24]);
  down('C13','C16',[1305,branchY]);
  let joinY=nodes.SCOPE.y-42;
  for(const id of ['C23','C16'])route(id,'SCOPE',[at(id,'B'),[midX(nodes[id]),joinY],[970,joinY],at('SCOPE','T')],[midX(nodes[id])+(id==='C23'?-105:110),joinY-24]);
  function handoff(id,decision,w=320){
   place(id,65,0,w);nodes[id].y=midY(nodes[decision])-nodes[id].h*0.72;return nodes[id];
  }
  handoff('OUTSCOPE','SCOPE');
  place('NOTAKE',65,bottom(nodes.OUTSCOPE)+100,320);
  route('SCOPE','OUTSCOPE',[at('SCOPE','L'),[385,midY(nodes.SCOPE)]],[560,midY(nodes.SCOPE)-24]);
  route('OUTSCOPE','C11',[[385,nodes.OUTSCOPE.y+40],[450,nodes.OUTSCOPE.y+40],[450,midY(nodes.C11)],at('C11','L')],[455,midY(nodes.C11)-24]);
  down('OUTSCOPE','NOTAKE',[325,bottom(nodes.OUTSCOPE)+47]);
  y=bottom(groups.SCOPEL)+100;
  e=row(['D8','D9','D10'],520,y+64,900,42);
  place('D19',834,e+96,272);place('D23',1148,e+96,272);
  e=Math.max(bottom(nodes.D19),bottom(nodes.D23));
  place('DREADY',720,e+90,500);
  group('DOORL',500,y,940,bottom(nodes.DREADY)+26);
  route('SCOPE','D8',[at('SCOPE','B'),[970,y+30],[midX(nodes.D8),y+30],at('D8','T')],[1010,y]);
  across('D8','D9');across('D9','D10');
  branchY=nodes.D19.y-48;
  route('D10','D19',[at('D10','B'),[midX(nodes.D10),branchY],[midX(nodes.D19),branchY],at('D19','T')]);
  route('D10','D23',[at('D10','B'),[midX(nodes.D10),branchY],[midX(nodes.D23),branchY],at('D23','T')]);
  joinY=nodes.DREADY.y-45;
  for(const id of ['D19','D23'])route(id,'DREADY',[at(id,'B'),[midX(nodes[id]),joinY],[970,joinY],at('DREADY','T')]);
  handoff('HD','DREADY');
  place('W23',65,Math.max(bottom(nodes.NOTAKE)+75,groups.DOORL.y+90),320);
  route('W23','HD',[at('W23','B'),at('HD','T')],[320,bottom(nodes.W23)+45]);
  route('DREADY','HD',[at('DREADY','L'),[385,midY(nodes.DREADY)]],[565,midY(nodes.DREADY)-25]);
  route('HD','D8',[[385,nodes.HD.y+40],[450,nodes.HD.y+40],[450,midY(nodes.D8)],at('D8','L')],[470,midY(nodes.D8)-25]);
  y=bottom(groups.DOORL)+110;
  place('RBEGIN',720,y+64,500);
  e=row(['R7','R2','R6'],520,bottom(nodes.RBEGIN)+94,900,42);
  place('R3',520,e+70,272);place('R4',834,e+70,272);
  e=Math.max(bottom(nodes.R3),bottom(nodes.R4));
  e=row(['R18','R5'],655,e+110,765,85);
  place('RSAFE',670,e+90,600);
  place('RREADY',720,bottom(nodes.RSAFE)+75,500);
  group('SRCL',500,y,940,bottom(nodes.RREADY)+26);
  down('DREADY','RBEGIN',[1010,groups.SRCL.y+20]);
  branchY=nodes.R7.y-47;
  for(const id of ['R7','R2','R6'])route('RBEGIN',id,[at('RBEGIN','B'),[970,branchY],[midX(nodes[id]),branchY],at(id,'T')]);
  route('RBEGIN','R3',[at('RBEGIN','L'),[510,midY(nodes.RBEGIN)],[510,midY(nodes.R3)],at('R3','L')]);
  down('R2','R4');
  joinY=nodes.R18.y-55;
  for(const id of ['R3','R4','R6'])route(id,'R18',[at(id,'B'),[midX(nodes[id]),joinY],[midX(nodes.R18),joinY],at('R18','T')]);
  route('R7','R18',[at('R7','R'),[810,midY(nodes.R7)],[810,joinY],[midX(nodes.R18),joinY],at('R18','T')]);
  across('R18','R5');
  route('R5','RSAFE',[at('R5','B'),[midX(nodes.R5),nodes.RSAFE.y-45],[970,nodes.RSAFE.y-45],at('RSAFE','T')]);
  down('RSAFE','RREADY');
  handoff('HRD','RREADY');
  route('RREADY','HRD',[at('RREADY','L'),[385,midY(nodes.RREADY)]],[555,midY(nodes.RREADY)-25]);
  route('HRD','RSAFE',[[385,nodes.HRD.y+35],[450,nodes.HRD.y+35],[450,midY(nodes.RSAFE)],at('RSAFE','L')],[560,midY(nodes.RSAFE)-26]);
  y=bottom(groups.SRCL)+150;
  e=row(['A21','A13'],520,y+70,586,42);
  place('CALC',1148,y+70,272);
  e=Math.max(e,bottom(nodes.CALC));
  e=row(['A27','A12'],834,e+100,586,100);
  group('AIL',500,y,940,e+26);
  place('W6',65,y+10,320);place('W24',65,bottom(nodes.W6)+70,320);
  down('W6','W24',[335,bottom(nodes.W6)+35]);
  route('RREADY','A21',[at('RREADY','B'),[970,y+40],[midX(nodes.A21),y+40],at('A21','T')],[1000,y+12]);
  across('A21','A13');across('A13','CALC');
  branchY=nodes.A27.y-50;
  route('CALC','A27',[at('CALC','B'),[midX(nodes.CALC),branchY],[midX(nodes.A27),branchY],at('A27','T')],[1080,branchY-25]);
  down('CALC','A12',[1325,branchY]);
  route('A12','A27',[at('A12','L'),at('A27','R')],[1127,midY(nodes.A27)-25]);
  y=bottom(groups.AIL)+110;
  place('KSTART',670,y+64,600);
  e=row(['K28','K11','K22'],520,bottom(nodes.KSTART)+96,900,42);
  e=row(['K12','K17'],520,e+100,586,42);
  place('KJOIN',670,e+100,600);
  place('CHECK',720,bottom(nodes.KJOIN)+75,500);
  group('CHKL',500,y,940,bottom(nodes.CHECK)+26);
  down('A27','KSTART');
  branchY=nodes.K28.y-48;
  for(const id of ['K28','K11','K22'])route('KSTART',id,[at('KSTART','B'),[970,branchY],[midX(nodes[id]),branchY],at(id,'T')]);
  route('KSTART','K12',[at('KSTART','L'),[510,midY(nodes.KSTART)],[510,midY(nodes.K12)],at('K12','L')]);
  branchY=nodes.K17.y-50;
  route('K28','K17',[at('K28','B'),[midX(nodes.K28),branchY],[midX(nodes.K17),branchY],at('K17','T')],[800,branchY-26]);
  down('K11','K17',[1080,branchY]);
  joinY=nodes.KJOIN.y-50;
  for(const id of ['K17','K22','K12'])route(id,'KJOIN',[at(id,'B'),[midX(nodes[id]),joinY],[970,joinY],at('KJOIN','T')]);
  down('KJOIN','CHECK');
  handoff('HJ','CHECK');
  route('CHECK','HJ',[at('CHECK','L'),[385,midY(nodes.CHECK)]],[610,midY(nodes.CHECK)-40]);
  y=bottom(groups.CHKL)+110;
  place('X18',670,y+64,600);
  place('XREADY',720,bottom(nodes.X18)+75,500);
  e=row(['X16','X7'],520,bottom(nodes.XREADY)+95,900,100);
  place('XSTATE',720,e+90,500);
  group('ACTL',500,y,940,bottom(nodes.XSTATE)+26);
  down('CHECK','X18',[1010,groups.ACTL.y+20]);down('X18','XREADY');
  route('XREADY','X16',[at('XREADY','B'),[970,nodes.X16.y-48],[midX(nodes.X16),nodes.X16.y-48],at('X16','T')],[1010,nodes.X16.y-50]);
  across('X16','X7');
  route('X7','XSTATE',[at('X7','B'),[midX(nodes.X7),nodes.XSTATE.y-45],[970,nodes.XSTATE.y-45],at('XSTATE','T')]);
  handoff('HX','XREADY');
  route('XREADY','HX',[at('XREADY','L',30),[385,midY(nodes.XREADY)+30]],[560,midY(nodes.XREADY)+58]);
  route('HX','X18',[[385,nodes.HX.y+35],[450,nodes.HX.y+35],[450,midY(nodes.X18)],at('X18','L')],[555,midY(nodes.X18)-26]);
  handoff('HRX','XSTATE');
  route('XSTATE','HRX',[at('XSTATE','L'),[385,midY(nodes.XSTATE)]],[560,midY(nodes.XSTATE)-26]);
  route('HRX','X7',[[385,nodes.HRX.y+35],[450,nodes.HRX.y+35],[450,bottom(nodes.X16)+20],[970,bottom(nodes.X16)+20],[970,midY(nodes.X7)],at('X7','L')],[720,bottom(nodes.X16)+43]);
  y=Math.max(bottom(groups.ACTL)+110,bottom(nodes.HRX)+200);
  place('F17',670,y+70,600);
  place('HOLD',65,midY(nodes.F17)-130,320,260);
  place('FINAL',720,Math.max(bottom(nodes.F17)+150,bottom(nodes.HOLD)+230),500);
  handoff('HR','FINAL');
  place('OUT',770,Math.max(bottom(nodes.FINAL),bottom(nodes.HR))+90,400);
  down('XSTATE','F17',[1100,nodes.F17.y-40]);down('F17','FINAL');
  route('FINAL','HR',[at('FINAL','L'),[385,midY(nodes.FINAL)]],[550,midY(nodes.FINAL)-26]);
  route('HR','F17',[[385,nodes.HR.y+35],[450,nodes.HR.y+35],[450,midY(nodes.F17)+50],[670,midY(nodes.F17)+50]],[560,midY(nodes.F17)+25]);
  route('HOLD','F17',[at('HOLD','R'),at('F17','L')],[530,midY(nodes.F17)-27]);
  down('FINAL','OUT',[1010,bottom(nodes.FINAL)+45]);
  // Refusals from distinct human tasks merge explicitly into one hold record.
  for(const id of ['HD','HRD','HJ','HX','HRX'])route(id,'HOLD',[at(id,'B'),[225,bottom(nodes[id])+72],[35,bottom(nodes[id])+72],[35,nodes.HOLD.y+35],[65,nodes.HOLD.y+35]],[315,bottom(nodes[id])+38]);
  route('HR','HOLD',[at('HR','T'),at('HOLD','B')],[315,(nodes.HR.y+bottom(nodes.HOLD))/2]);
  y=bottom(nodes.OUT)+95;
  e=row(['G21','G22','G20','G24'],88,y+64,1350,42);
  group('LOGL',65,y,1390,e+105);
  route('G20','G24',[at('G20','B'),[midX(nodes.G20),e+62],[midX(nodes.G24),e+62],at('G24','B')],[1125,e+32]);
  y=bottom(groups.LOGL)+65;
  e=row(['E1','E2'],88,y+64,660,40);
  place('EWAIT',800,y+64,290);
  place('E3',1170,y+64,260);place('E4',1170,bottom(nodes.E3)+75,260);
  group('EMERGL',65,y,1390,Math.max(e,bottom(nodes.E4))+26);
  across('E1','E2');across('E2','EWAIT');
  route('EWAIT','E3',[at('EWAIT','R'),at('E3','L')],[1130,midY(nodes.EWAIT)-25]);
  route('EWAIT','E4',[at('EWAIT','B'),[midX(nodes.EWAIT),midY(nodes.E4)],at('E4','L')],[1050,midY(nodes.E4)-27]);
  // Every return remains a continuous directed path; no detached connectors.
  const connections=[], entries=[];
  route('W24','PUPDATE',[at('W24','B',-75),[150,bottom(nodes.W24)+60],[8,bottom(nodes.W24)+60],[8,pb+52],[825,pb+52],at('PUPDATE','B')],[92,bottom(nodes.W24)+28]);
  const ay=midY(nodes.A21);
  route('W24','A21',[at('W24','R'),[450,midY(nodes.W24)],[450,ay],[480,ay],at('A21','L')],[463,ay-28]);
  route('HJ','A21',[[385,nodes.HJ.y+40],[450,nodes.HJ.y+40],[450,midY(nodes.W24)],[450,ay],[480,ay],at('A21','L')],[417,nodes.HJ.y+12]);
  route('CHECK','A21',[at('CHECK','R',-28),[1490,midY(nodes.CHECK)-28],[1490,groups.AIL.y+40],[970,groups.AIL.y+40],[midX(nodes.A21),groups.AIL.y+40],at('A21','T')],[1335,midY(nodes.CHECK)-72]);
  route('CHECK','RBEGIN',[at('CHECK','R',28),[1525,midY(nodes.CHECK)+28],[1525,midY(nodes.RBEGIN)],at('RBEGIN','R')],[1350,midY(nodes.CHECK)+78]);
  route('XREADY','A21',[at('XREADY','L',-30),[480,midY(nodes.XREADY)-30],[480,ay],at('A21','L')],[580,midY(nodes.XREADY)-76]);
  route('START','G20',[at('START','R'),[1550,midY(nodes.START)],[1550,groups.LOGL.y+40],[midX(nodes.G20),groups.LOGL.y+40],at('G20','T')],[1250,midY(nodes.START)-27]);
  for(const id of ['G21','G22'])route('START',id,[at('START','R'),[1550,midY(nodes.START)],[1550,groups.LOGL.y+40],[midX(nodes.G20),groups.LOGL.y+40],[midX(nodes[id]),groups.LOGL.y+40],at(id,'T')]);
  route('START','E1',[at('START','R'),[1550,midY(nodes.START)],[1550,groups.LOGL.y+40],[1550,groups.EMERGL.y-30],[midX(nodes.E1),groups.EMERGL.y-30],at('E1','T')],[780,groups.EMERGL.y-56]);
  // Validate that the visual source has not silently lost or invented edges.
  const visible=edges.filter(e=>!e.hidden), keys=new Set(visible.map(e=>e.key));
  for(const e of visible)if(!routes[e.key])throw Error('unrouted edge '+e.key);
  for(const key of Object.keys(routes))if(!keys.has(key))throw Error('extra edge '+key);
  for(const n of Object.values(nodes))if(n.x===undefined)throw Error('unplaced node '+n.id);
  const bridges=[];
  function crossing(a,b,c,d) {
   const rx=b[0]-a[0],ry=b[1]-a[1],sx=d[0]-c[0],sy=d[1]-c[1],den=rx*sy-ry*sx;
   if(Math.abs(den)<1e-8)return;
   const qx=c[0]-a[0],qy=c[1]-a[1],t=(qx*sy-qy*sx)/den,u=(qx*ry-qy*rx)/den;
   if(t>1e-6&&t<1-1e-6&&u>1e-6&&u<1-1e-6)return[a[0]+t*rx,a[1]+t*ry];
  }
  for(let i=0;i<visible.length;i++)for(let j=i+1;j<visible.length;j++){
   const a=visible[i],b=visible[j],ap=routes[a.key].pts,bp=routes[b.key].pts;
   for(let m=1;m<ap.length;m++)for(let n=1;n<bp.length;n++){
    const p=crossing(ap[m-1],ap[m],bp[n-1],bp[n]);if(!p)continue;
    const over=ap[m-1][1]===ap[m][1]?a:b;
    let mark=bridges.find(v=>v.over===over.key&&Math.hypot(v.x-p[0],v.y-p[1])<1);
    if(!mark){mark={over:over.key,x:p[0],y:p[1],pairs:[],radius:12};bridges.push(mark);}
    mark.pairs.push([a.key,b.key]);
   }
  }
  const H=bottom(groups.EMERGL)+30;
  let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="title desc"><title id="title">해결책 구조</title><desc id="desc">원문의 해결책 28개, 그룹과 색상을 유지하고 읽는 폭에 맞춰 배치한 순서도. 한 건의 처리, 사람의 결정, 재검토와 공통 통제를 구분한다.</desc><style>text{font-family:"Apple SD Gothic Neo","Noto Sans CJK KR",sans-serif;fill:#17314f;font-size:22px} .edge-label text{font-size:20px;fill:#475569} .node text{dominant-baseline:middle} .group-title{font-size:24px;fill:#64748b}</style><rect width="100%" height="100%" fill="white"/><defs>`;
  for(const color of new Set([...visible,...entries].map(e=>e.color)))svg+=`<marker id="arrow${color.slice(1)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${color}"/></marker>`;
  svg+='</defs>';
  for(const g of Object.values(groups))svg+=`<g class="group" id="group-${g.id}"><rect x="${g.x}" y="${g.y}" width="${g.w}" height="${g.h}" fill="none" stroke="#94a3b8" stroke-width="1.3" stroke-dasharray="2 7"/><text class="group-title" x="${g.x+18}" y="${g.y+32}">${esc(g.title)}</text></g>`;
  // Rounded orthogonal routes retain the soft original curves without big loops.
  function pathD(points,key=''){
   points=points.filter((p,i)=>!i||p[0]!==points[i-1][0]||p[1]!==points[i-1][1]);
   let current=points[0],d=`M ${current.join(' ')}`;
   function line(end){
    const marks=bridges.filter(v=>v.over===key&&Math.abs(current[1]-end[1])<0.1&&Math.abs(v.y-end[1])<0.1&&v.x>Math.min(current[0],end[0])+v.radius&&v.x<Math.max(current[0],end[0])-v.radius).sort((a,b)=>(a.x-b.x)*Math.sign(end[0]-current[0]));
    for(const v of marks){const direction=Math.sign(end[0]-current[0]),l=[v.x-direction*v.radius,v.y],r=[v.x+direction*v.radius,v.y];d+=` L ${l.join(' ')} Q ${v.x} ${v.y-v.radius*2} ${r.join(' ')}`;v.drawn=true;v.d=`M ${l.join(' ')} Q ${v.x} ${v.y-v.radius*2} ${r.join(' ')}`;}
    d+=` L ${end.join(' ')}`;current=end;
   }
   for(let i=1;i<points.length-1;i++){
    const a=points[i-1],b=points[i],c=points[i+1],ab=Math.hypot(b[0]-a[0],b[1]-a[1]),bc=Math.hypot(c[0]-b[0],c[1]-b[1]);
    const r=Math.min(12,ab/2,bc/2),p=[b[0]-(b[0]-a[0])*r/ab,b[1]-(b[1]-a[1])*r/ab],q=[b[0]+(c[0]-b[0])*r/bc,b[1]+(c[1]-b[1])*r/bc];
    line(p);d+=` Q ${b.join(' ')} ${q.join(' ')}`;current=q;
   }
   line(points.at(-1));return d;
  }
  for(const e of [...visible,...entries]){const r=routes[e.key]||e;svg+=`<path class="edge" id="edge-${e.from}-${e.to}" data-from="${e.from}" data-to="${e.to}" d="${pathD(r.pts,e.key)}" fill="none" stroke="${e.color}" stroke-width="2.6" ${e.dash?`stroke-dasharray="${e.dash}"`:''} marker-end="url(#arrow${e.color.slice(1)})"/>`;}
  for(const v of bridges){
   if(!v.drawn)throw Error('bridge not drawn '+JSON.stringify(v));
   const edge=visible.find(e=>e.key===v.over);
   svg+=`<g class="line-bridge" data-over="${v.over}"><path d="${v.d}" fill="none" stroke="white" stroke-width="7.5"/><path d="${v.d}" fill="none" stroke="${edge.color}" stroke-width="2.6"/></g>`;
  }
  for(const c of connections) {
   svg+=`<g class="connection" id="connection-${c.id}" data-target="${c.to}"><circle cx="${c.x}" cy="${c.y}" r="22" fill="white" stroke="#64748b" stroke-width="1.8"/><text x="${c.x}" y="${c.y}" dominant-baseline="middle" text-anchor="middle" style="font-weight:700">${c.letter}</text></g>`;
   if(c.entry)svg+=`<text x="${c.x}" y="${c.y-40}" text-anchor="middle" style="font-size:20px;fill:#475569">${c.title}</text>`;
  }

  for(const n of Object.values(nodes)){
   const [fill,stroke,color]=palette[n.kind];let shape;
   if(n.shape==='{')shape=`<polygon points="${midX(n)},${n.y} ${right(n)},${midY(n)} ${midX(n)},${bottom(n)} ${n.x},${midY(n)}"`;
   else shape=`<rect x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" rx="${n.shape==='(['?n.h/2:0}"`;
   svg+=`<g class="node" id="node-${n.id}">${shape} fill="${fill}" stroke="${stroke}" stroke-width="1.6"/>`;
   if(n.shape==='[[')svg+=`<path d="M ${n.x+10} ${n.y} V ${bottom(n)} M ${right(n)-10} ${n.y} V ${bottom(n)}" fill="none" stroke="${stroke}" stroke-width="1.6"/>`;
   const startY=n.y+(n.h-(n.lines.length-1)*LH)/2;
   n.lines.forEach((l,i)=>svg+=`<text x="${midX(n)}" y="${startY+i*LH}" text-anchor="middle" style="fill:${color};font-weight:${l.bold?700:400}">${esc(l.text)}</text>`);
   svg+='</g>';
  }
  for(const e of visible){
   if(!e.label)continue;
   const p=routes[e.key].labelAt;if(!p)throw Error('label not placed '+e.key);
   const lines=e.label.split(/<br\s*\/?\s*>/i);
   const vertical=p[2]==='vertical';
   svg+=`<g class="edge-label" data-edge="${e.key}" transform="translate(${p[0]},${p[1]})${vertical?' rotate(-90)':''}">`;
   lines.forEach((t,i)=>svg+=`<text x="0" y="${(i-(lines.length-1)/2)*27}" text-anchor="middle" dominant-baseline="middle">${esc(t)}</text>`);
   svg+='</g>';
  }
  svg+='</svg>';
  await page.setContent('<body style="margin:0;background:#fff">'+svg+'</body>');
  await page.evaluate(()=>document.fonts.ready);
  const finalSvg=await page.locator('svg').evaluate(e=>new XMLSerializer().serializeToString(e));
  fs.writeFileSync(base+'.svg',finalSvg);
  await page.screenshot({path:base+'.png',fullPage:true});
  const qa=process.env.RELIABILITY_QA_DIR||'/tmp/reliability-final-flow';fs.mkdirSync(qa,{recursive:true});
  fs.writeFileSync(path.join(qa,'geometry.json'),JSON.stringify({width:W,height:H,nodes,groups,connections,bridges,edges:[...visible.map(e=>({...e,...routes[e.key]})),...entries]},null,2));
  // Inspect at a normal document preview width; do not manipulate a user window.
  await page.setViewportSize({width:1194,height:1000});
  await page.setContent(`<body style="margin:0;padding:24px 46px;background:#202020"><img style="display:block;width:1100px;height:auto;background:white" src="data:image/svg+xml;base64,${Buffer.from(finalSvg).toString('base64')}"/></body>`);
  await page.locator('img').evaluate(img=>img.decode());
  await page.screenshot({path:path.join(qa,'preview-1100.png'),fullPage:true});
  console.log(JSON.stringify({width:W,height:H,nodes:Object.keys(nodes).length,edges:visible.length,bodyAt1100:FONT*1100/W,labelAt1100:20*1100/W,png:base+'.png'}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
