#!/usr/bin/env python3
"""Validate native Mermaid coverage, edge meanings and browser-measured geometry.

This checks the native rendering, independently of the preserved SVG images.
Crossing checks use short sampled segments; they do not replace visual review.
"""
import json,math,itertools,collections,sys,re,html,hashlib,argparse,importlib.util
from pathlib import Path

def overlap(a,b,pad=2):return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>pad and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>pad
def inside(p,n,pad=3):
 if n.get('key') in ['permit','human_valid','ready','verdict','wait_result','nextwork','received','learn_needed','test_passed'] and n['w']>n['h']*.8 and n['w']<n['h']*1.2:
  return abs((p[0]-n['x']-n['w']/2)/(n['w']/2))+abs((p[1]-n['y']-n['h']/2)/(n['h']/2))<.95
 return n['x']+pad<p[0]<n['x']+n['w']-pad and n['y']+pad<p[1]<n['y']+n['h']-pad
def cross(a,b,c,d):
 dx,dy=b[0]-a[0],b[1]-a[1];ex,ey=d[0]-c[0],d[1]-c[1];det=dx*ey-dy*ex
 if abs(det)<.0001:return None
 u=((c[0]-a[0])*ey-(c[1]-a[1])*ex)/det;v=((c[0]-a[0])*dy-(c[1]-a[1])*dx)/det
 if .0001<u<.9999 and .0001<v<.9999:return [a[0]+u*dx,a[1]+u*dy]
def audit(m):
 issues=[]
 for a,b in itertools.combinations(m['nodes'],2):
  if overlap(a,b):issues.append(['node-node',a['key'],b['key']])
 for a in m['labels']:
  for b in m['nodes']:
   if overlap(a,b):issues.append(['label-node',a['text'],b['key']])
 for g in m['groups']:
  t=g['title']
  if t and g['text'] and (t['x']<g['x']-1 or t['x']+t['w']>g['x']+g['w']+1):issues.append(['title-out',g['text']])
 for a,b in itertools.combinations(m['labels'],2):
  if overlap(a,b):issues.append(['label-label',a['text'],b['text']])
 for n in m['nodes']:
  for t in n['label']:
   if t['x']<n['x']-1 or t['y']<n['y']-1 or t['x']+t['w']>n['x']+n['w']+1 or t['y']+t['h']>n['y']+n['h']+1:issues.append(['text-out',n['key'],t['text']])
 for e in m['edges']:
  for n in m['nodes']:
   if ('_'+n['key']+'_') in e['id']:continue
   if sum(inside(p,n) for p in e['points'])>2:issues.append(['edge-node',e['id'],n['key']])
  for g in m['groups']:
   if g['text'] and sum(inside(p,g['title'],1) for p in e['points'])>2:issues.append(['edge-title',e['id'],g['text']])
 # Pair only segments in the same spatial cell.
 bins=collections.defaultdict(list);hits={}
 for ei,e in enumerate(m['edges']):
  for a,b in zip(e['points'],e['points'][1:]):
   keys=[(x,y) for x in range(math.floor(min(a[0],b[0])/64),math.floor(max(a[0],b[0])/64)+1) for y in range(math.floor(min(a[1],b[1])/64),math.floor(max(a[1],b[1])/64)+1)]
   for key in keys:
    for fi,c,d in bins[key]:
     if ei==fi:continue
     p=cross(a,b,c,d)
     if p:hits[(min(ei,fi),max(ei,fi))]=p
    bins[key].append((ei,a,b))
 for (i,j),p in hits.items():issues.append(['edge-cross',m['edges'][i]['id'],m['edges'][j]['id'],p])
 return issues


ROOT=Path(__file__).resolve().parents[2]
MODES=('solo','orchestration','complex')

def compact(text):
    return re.sub(r'\s+','',html.unescape(re.sub(r'<[^>]+>','',text)))

def run(geometry):
    model=json.loads((ROOT/'docs/도식/사용-구조-원본.json').read_text())
    doc=(ROOT/'전문가 에이전트 정의.md').read_text()
    prefix,usage=doc.split('## 사용 구조',1)
    blocks=re.findall(r'```mermaid\n(.*?)```',usage,re.S)
    assert len(blocks)==3
    assert '<details' not in usage and '<summary' not in usage
    sections=re.split(r'^### ',usage,flags=re.M)[1:]
    assert len(sections)==3
    result=[]
    for mode,block,section in zip(MODES,blocks,sections):
        image=f'](docs/images/expert-definition/usage-structure-{mode}.svg)'
        assert section.count(image)==1 and section.index(image)<section.index('```mermaid')
        assert not section[section.index(image)+len(image):section.index('```mermaid')].strip()
        source=(ROOT/f'docs/도식/usage-structure-{mode}.mmd').read_text()
        assert block==source,(mode,'embedded Mermaid differs')
        d=model['diagrams'][mode]
        assert d['source_prefix_sha256']==hashlib.sha256(prefix.encode()).hexdigest()
        declarations={}
        for line in source.splitlines():
            match=re.match(r'^\s*(\w+)(?:\[|\{|\(\[).*?"(.*?)".*?:::(\w+)\s*$',line)
            if match:declarations[match[1]]=(match[2],match[3])
            fork=re.match(r'^\s*(\w+)@\{ shape: fork \}$',line)
            if fork:declarations[fork[1]]=('', 'fork')
        assert set(declarations)==set(d['nodes']),(mode,'missing or extra nodes')
        material_names=[]
        for key,n in d['nodes'].items():
            label,kind=declarations[key]
            assert kind==n['kind'],(mode,key,'changed shape meaning')
            if n['kind']=='fork':continue
            bold=re.findall(r'<b>(.*?)</b>',label)
            assert [compact(x) for x in bold]==[compact(n['name'])]
            assert compact(n['note']) in compact(label),(mode,key,'condition lost')
            if n['material']:
                assert n['usage'] in label
                material_names.append(n['name'])
        assert set(material_names)==set(model['catalog']) and len(set(material_names))==79
        relations=re.findall(r'^\s*%% relation (\d+): (\w+) -> (\w+); (\w+)\n([^\n]+)',source,re.M)
        assert len(relations)==len(d['edges'])
        measured=json.loads((geometry/f'{mode}-mermaid-geometry.json').read_text())
        assert measured['source_sha256']==hashlib.sha256(source.encode()).hexdigest(),(mode,'stale render')
        assert {n['key'] for n in measured['nodes']}==set(d['nodes'])
        assert len(measured['edges'])==len(relations)
        start=next(n for n in measured['nodes'] if n['key']=='start')
        assert start['y']<=min(n['y'] for n in measured['nodes'])+1
        colors={'flow':'#71aeff','data':'#71aeff','return':'#ffd452','blocked':'#ff8d91','apply':'#94a6b9'}
        for index,(i,a,b,kind,line) in enumerate(relations):
            original=d['edges'][int(i)]
            assert (a,b,kind)==(original['source'],original['target'],original['kind'])
            tokens=line.split();left,right=tokens[0],tokens[-1]
            rendered=measured['edges'][index]
            assert re.match(r'^chart-L_'+re.escape(left)+'_'+re.escape(right)+r'_\d+$',rendered['id']), (mode,i,'render order mismatch')
            assert colors[kind] in rendered['style']
            assert {left,right}=={a,b},(mode,i,'original endpoint changed')
            if kind=='apply':assert not rendered['start'] and not rendered['end']
            elif '<-->' in line:
                assert re.search(r'^\s*linkStyle '+str(index)+r' [^\n]*marker-end:none',source,re.M)
                assert rendered['start'] and not rendered['end']
                assert (left,right)==(b,a),(mode,i,'return arrow reversed')
            else:
                assert rendered['end'] and not rendered['start']
                assert (left,right)==(a,b),(mode,i,'forward arrow reversed')
        issues=audit(measured)
        assert not issues,(mode,issues)
        result.append({'scenario':mode,'materials':79,'material_nodes':len(material_names),'nodes':len(measured['nodes']),'visible_connections':len(measured['edges']),'all_conditions_preserved':True,'all_relation_records_preserved':True,'source_sha256':measured['source_sha256'],'renderer':'Mermaid + ELK, VS Code bundled renderer','browser':measured['browser'],'native_width':measured['width'],'native_height':measured['height'],'inspection_viewport_width':1920,'inspection_scale':measured['display_scale'],'geometry_issues':issues})
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--geometry',type=Path,required=True)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    results=run(args.geometry)
    if args.report:args.report.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))
