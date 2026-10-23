// Headless geometry and flow regression checks; run the renderer first.
const fs=require('fs');const path=require('path');
const root=path.resolve(__dirname,'../..');
const qa=process.env.RELIABILITY_QA_DIR||'/tmp/reliability-final-flow';
fs.mkdirSync(qa,{recursive:true});const {chromium}=require('/opt/homebrew/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({headless:true});try{const p=await b.newPage({viewport:{width:1560,height:1000}});await p.setContent(fs.readFileSync(path.join(root,'docs/images/expert-definition/reliability-solution-structure.svg'),'utf8'));await p.evaluate(()=>document.fonts.ready);const r=await p.evaluate(()=>{
 const bounds=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}};
 const overlaps=(a,b,pad=0)=>a.x+pad<b.x+b.w&&a.x+a.w-pad>b.x&&a.y+pad<b.y+b.h&&a.y+a.h-pad>b.y;
 const nodes=[...document.querySelectorAll('.node')].map(e=>({id:e.id.slice(5),...bounds(e),shape:bounds(e.firstElementChild)}));
 const labels=[...document.querySelectorAll('.edge-label')].map(e=>({id:e.dataset.edge,...bounds(e)}));
 const issues={nodeOverlap:[],labelNode:[],labelOverlap:[],edgeNode:[],edgeLabel:[],textOverflow:[]};
 for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++)if(overlaps(nodes[i].shape,nodes[j].shape,2))issues.nodeOverlap.push([nodes[i].id,nodes[j].id]);
 for(const l of labels)for(const n of nodes)if(overlaps(l,n.shape,2))issues.labelNode.push([l.id,n.id]);
 for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)if(overlaps(labels[i],labels[j],2))issues.labelOverlap.push([labels[i].id,labels[j].id]);
 for(const n of nodes){const e=document.getElementById('node-'+n.id);for(const t of e.querySelectorAll('text')){const a=bounds(t),q=n.shape;if(a.x<q.x+5||a.x+a.w>q.x+q.w-5||a.y<q.y||a.y+a.h>q.y+q.h)issues.textOverflow.push([n.id,t.textContent]);}}
 for(const e of document.querySelectorAll('.edge')){const key=e.dataset.from+'>'+e.dataset.to,len=e.getTotalLength(),m=e.getScreenCTM();const hits=new Set(),labelHits=new Set();for(let s=8;s<len-8;s+=5){const a=e.getPointAtLength(s).matrixTransform(m);for(const n of nodes){if(n.id===e.dataset.from||n.id===e.dataset.to)continue;const q=n.shape;if(a.x>q.x+3&&a.x<q.x+q.w-3&&a.y>q.y+3&&a.y<q.y+q.h-3)hits.add(n.id);}for(const l of labels){if(a.x>l.x&&a.x<l.x+l.w&&a.y>l.y&&a.y<l.y+l.h)labelHits.add(l.id);}}
 if(hits.size)issues.edgeNode.push([key,[...hits]]);if(labelHits.size)issues.edgeLabel.push([key,[...labelHits]]);}
  const connectors=[...document.querySelectorAll('.connection')].map(e=>({id:e.id,...bounds(e.firstElementChild)}));
 issues.connectorNode=[];issues.connectorLabel=[];issues.groupTitle=[];
 for(const c of connectors){for(const n of nodes)if(overlaps(c,n.shape,2))issues.connectorNode.push([c.id,n.id]);for(const l of labels)if(overlaps(c,l,2))issues.connectorLabel.push([c.id,l.id]);}
 const titles=[...document.querySelectorAll('.group-title')].map(e=>({id:e.parentNode.id,...bounds(e)}));
 for(const t of titles){for(const n of nodes)if(overlaps(t,n.shape,2))issues.groupTitle.push([t.id,n.id]);for(const l of labels)if(overlaps(t,l,2))issues.groupTitle.push([t.id,l.id]);}
 const sampled=[...document.querySelectorAll('.edge')].map(e=>{const len=e.getTotalLength(),points=[];for(let s=0;s<len;s+=2){const p=e.getPointAtLength(s);points.push([p.x,p.y]);}const p=e.getPointAtLength(len);points.push([p.x,p.y]);return{key:e.dataset.from+'>'+e.dataset.to,points};});
 return{nodes:nodes.length,labels:labels.length,connectors:connectors.length,issues,sampled};});const geometry=JSON.parse(fs.readFileSync(path.join(qa,'geometry.json'),'utf8'));
// Sample the actual rounded SVG routes. Spatial buckets keep the comparison local.
const buckets=new Map(),segments=[];
for(let e=0;e<r.sampled.length;e++)for(let i=1;i<r.sampled[e].points.length;i++){
 const a=r.sampled[e].points[i-1],b=r.sampled[e].points[i];if(Math.hypot(b[0]-a[0],b[1]-a[1])<0.01)continue;
 const id=segments.length;segments.push({e,a,b});
 for(let x=Math.floor(Math.min(a[0],b[0])/24);x<=Math.floor(Math.max(a[0],b[0])/24);x++)for(let y=Math.floor(Math.min(a[1],b[1])/24);y<=Math.floor(Math.max(a[1],b[1])/24);y++){const key=x+','+y;if(!buckets.has(key))buckets.set(key,[]);buckets.get(key).push(id);}
}
const compared=new Set(),hits=[],seen=new Set();
function intersect(a,b,c,d){const rx=b[0]-a[0],ry=b[1]-a[1],sx=d[0]-c[0],sy=d[1]-c[1],den=rx*sy-ry*sx;if(Math.abs(den)<1e-8)return;const qx=c[0]-a[0],qy=c[1]-a[1],t=(qx*sy-qy*sx)/den,u=(qx*ry-qy*rx)/den;if(t>=-1e-7&&t<=1+1e-7&&u>=-1e-7&&u<=1+1e-7)return[a[0]+t*rx,a[1]+t*ry];}
function intentionalJunction(i,j,p){
 const a=geometry.edges[i],b=geometry.edges[j];
 if(a.from!==b.from&&a.to!==b.to)return false;
 // Only a shared route waypoint/segment is a join. Merely sharing a node
 // does not exempt two routes that twist across one another elsewhere.
 const shared=a.pts.filter(p=>b.pts.some(q=>Math.hypot(p[0]-q[0],p[1]-q[1])<0.1));
 if(shared.some(q=>Math.hypot(p[0]-q[0],p[1]-q[1])<18))return true;
 for(let k=1;k<a.pts.length;k++)for(let l=1;l<b.pts.length;l++){
  const v=a.pts[k-1],w=a.pts[k],x=b.pts[l-1],y=b.pts[l];
  if(v[0]===w[0]&&x[0]===y[0]&&Math.abs(v[0]-x[0])<0.1&&Math.abs(p[0]-v[0])<0.1&&p[1]>=Math.max(Math.min(v[1],w[1]),Math.min(x[1],y[1]))-0.1&&p[1]<=Math.min(Math.max(v[1],w[1]),Math.max(x[1],y[1]))+0.1)return true;
  if(v[1]===w[1]&&x[1]===y[1]&&Math.abs(v[1]-x[1])<0.1&&Math.abs(p[1]-v[1])<0.1&&p[0]>=Math.max(Math.min(v[0],w[0]),Math.min(x[0],y[0]))-0.1&&p[0]<=Math.min(Math.max(v[0],w[0]),Math.max(x[0],y[0]))+0.1)return true;
 }
 return false;
}
for(const bucket of buckets.values())for(let i=0;i<bucket.length;i++)for(let j=i+1;j<bucket.length;j++){
 const ai=bucket[i],bi=bucket[j],a=segments[ai],b=segments[bi];if(a.e===b.e)continue;const key=Math.min(ai,bi)+':'+Math.max(ai,bi);if(compared.has(key))continue;compared.add(key);const p=intersect(a.a,a.b,b.a,b.b);if(!p||intentionalJunction(a.e,b.e,p))continue;const hitKey=a.e+':'+b.e+':'+Math.round(p[0])+':'+Math.round(p[1]);if(seen.has(hitKey))continue;seen.add(hitKey);hits.push({a:r.sampled[a.e].key,b:r.sampled[b.e].key,x:+p[0].toFixed(2),y:+p[1].toFixed(2)});
}
const bridged=[],unmarked=[];
for(const h of hits){const mark=(geometry.bridges||[]).find(v=>v.drawn&&Math.hypot(h.x-v.x,h.y-v.y)<=v.radius*2&&v.pairs.some(pair=>pair.includes(h.a)&&pair.includes(h.b)));(mark?bridged:unmarked).push(h);}
r.issues.edgeCrossings=unmarked;
r.crossingBridges=(geometry.bridges||[]).length;
r.bridgedIntersections=bridged;

fs.writeFileSync(path.join(qa,'sampled-paths.json'),JSON.stringify(r.sampled));
delete r.sampled;
const source=fs.readFileSync(path.join(root,'docs/도식/reliability-solution-structure.mmd'),'utf8');
const logical=[...source.matchAll(/^\s*(\w+) -->(?:\|[^|]*\|)? (\w+)$/gm)].map(m=>[m[1],m[2]]);
const adj=new Map();for(const[a,b]of logical){if(!adj.has(a))adj.set(a,[]);adj.get(a).push(b);}
const reachable=(from,to,blocked=[])=>{const seen=new Set(blocked),todo=[from];while(todo.length){const n=todo.pop();if(seen.has(n))continue;if(n===to)return true;seen.add(n);todo.push(...(adj.get(n)||[]));}return false;};
const undirected=new Map();for(const[a,b]of logical){for(const[v,w]of[[a,b],[b,a]]){if(!undirected.has(v))undirected.set(v,[]);undirected.get(v).push(w);}}
const connected=new Set(),todo=['START'];while(todo.length){const n=todo.pop();if(connected.has(n))continue;connected.add(n);todo.push(...(undirected.get(n)||[]));}
const onNode=(p,n)=>p[0]>=n.x-2&&p[0]<=n.x+n.w+2&&p[1]>=n.y-2&&p[1]<=n.y+n.h+2;
const checks={
 oneConnectedDiagram:Object.keys(geometry.nodes).every(n=>connected.has(n)),
 allEdgesEndAtTheirActualNodes:geometry.edges.every(e=>onNode(e.pts[0],geometry.nodes[e.from])&&onNode(e.pts.at(-1),geometry.nodes[e.to])),
 noDetachedConnectors:geometry.connections.length===0,
 recordingStartsWithWork:['G20','G21','G22'].every(n=>adj.get('START').includes(n)),
 emergencyAvailableFromStart:adj.get('START').includes('E1'),
 fourOrFewerMarkedCrossings:geometry.bridges.length<=4&&geometry.bridges.every(b=>b.drawn),
 all28Tools:Array.from({length:28},(_,i)=>i+1).every(n=>Object.values(geometry.nodes).some(v=>v.html.match(/<b>[\d ·]+<\/b>/g)?.some(t=>t.replace(/<[^>]*>/g,'').split(/\D+/).map(Number).includes(n)))),
 executionRequiresCheck:!reachable('START','X16',['CHECK']),
 humanReviewRequiresRecheck:!reachable('HJ','X16',['CHECK']),
 approvalDoesNotSkipPolicy:!reachable('HX','X16',['X18']),
 newEvidencePassesMaterialGate:!reachable('RBEGIN','A21',['RSAFE']),
 allFiveInspectionsReachJoin:['K11','K12','K17','K22','K28'].every(n=>reachable(n,'KJOIN')),
 holdOnlyReports:!reachable('HOLD','X16')&&reachable('HOLD','OUT'),
 unknownResultDoesNotRetryExecution:!reachable('HRX','X16'),
 decisionShapes:Object.values(geometry.nodes).filter(n=>n.kind==='note').every(n=>n.shape==='{')
};
r.semanticChecks=checks;
fs.writeFileSync(path.join(qa,'audit.json'),JSON.stringify(r,null,2));console.log(JSON.stringify(r,null,2));
if(Object.values(r.issues).some(a=>a.length)||Object.values(checks).some(v=>!v))process.exitCode=1;}finally{await b.close();}})();
