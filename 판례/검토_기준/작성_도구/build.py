from pathlib import Path
import csv, datetime, gzip, hashlib, html, json, re, shutil, sys
from urllib.parse import quote
from html.parser import HTMLParser

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT.parent
ARCHIVE = PROJECT / 'docs/실험 결과/실제 판례 24건 스트레스 검토'
sys.path.insert(0, str(HERE))
from easy_cases import CASES
from simple_notes import NOTES
from beginner_cases import DETAILS, COMMON_ROWS, CASE_ROWS, TESTS, OUTPUTS, READER_QA

BASE = ROOT / '검토_기준'
RAW = BASE / '원본'
RAW.mkdir(exist_ok=True)
rows = {r['ID']: r for r in csv.DictReader((ARCHIVE/'02_24건_대입결과.csv').open(encoding='utf-8-sig'))}
snap = json.loads((BASE/'작성시점.json').read_text())
STAMP = snap['created_at']
CURRENT_REVIEW = json.loads((BASE/'초등독자_전수개정/검토시점.json').read_text())
REVIEW_STAMP = datetime.datetime.fromisoformat(CURRENT_REVIEW['checked_at']).strftime('%Y-%m-%d %H:%M')
CURRENT_LOCATIONS = {
    'D01': [('materials.md',48),('전문가 에이전트 정의 2.md',2877),('전문가 에이전트 정의 2.md',7205)],
    'D02': [('전문가 에이전트 정의.md',469),('전문가 에이전트 정의.md',616)],
    'D03': [('전문가 에이전트 정의.md',594)],
    'D04': [('전문가 에이전트 정의.md',541),('전문가 에이전트 정의.md',690)],
    'D05': [('전문가 에이전트 정의.md',489),('전문가 에이전트 정의.md',641),('전문가 에이전트 정의.md',586)],
    'D06': [('전문가 에이전트 정의 2.md',5143)],
    'D07': [('전문가 에이전트 정의 2.md',7082),('전문가 에이전트 정의 2.md',7089),('전문가 에이전트 정의 2.md',7536)],
    'D08': [('전문가 에이전트 정의 2.md',2987),('전문가 에이전트 정의 2.md',3007)]
}


class TextReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ['br','p','div','li','tr']: self.parts.append('\n')
        if tag.lower()=='img':
            src=dict(attrs).get('src','')
            if src!='/LSA/flDownload.do?flSeq=36958970':raise ValueError('미처리 이미지: '+src)
            self.parts.append('⟦원문이미지36958970⟧')
    def handle_endtag(self, tag):
        if tag.lower() in ['p','div','li','tr']: self.parts.append('\n')
    def handle_data(self, data): self.parts.append(data)

def plain(value):
    p=TextReader();p.feed(str(value or ''));p.close()
    return ''.join(p.parts).replace('\r\n','\n').replace('\r','\n')

def norm(value): return re.sub(r'\s+','',value)
def digest(value):return hashlib.sha256(value).hexdigest()
def link(path):return quote(str(path),safe='/#')
def slug(value):return re.sub(r'[^0-9A-Za-z가-힣]+','_',value).strip('_')
def object_particle(value):
    last=ord(value[-1]);return '을' if 0xAC00<=last<=0xD7A3 and (last-0xAC00)%28 else '를'
def question(task):
    if task.endswith('나눔'): return task[:-2]+'나눴나요?'
    if task.endswith('읽음'): return task[:-2]+'읽었나요?'
    return task+'했나요?'
def finish_document(out):
    text='\n\n'.join(out)+'\n'
    # 표의 행 사이는 빈 줄을 넣지 않는다.
    return re.sub(r'(?m)(\|[^\n]*\|)\n\n(?=\|)',r'\1\n',text)
def escaped(s):
    # 화면에서 원문 문자가 Markdown 문법으로 사라지지 않게 한다.
    return re.sub(r'([\\`*_[\]<>|])',r'\\\1',s)
def render(value):
    src=plain(value)
    # 원래 있던 줄바꿈을 문단으로 표시한다. 단어·구두점·숫자는 바꾸지 않는다.
    chunks=[re.sub(r'[\t \u00a0]+',' ',x).strip() for x in src.split('\n') if x.strip()]
    parts=[]
    for c in chunks:
        if re.fullmatch(r'【[^】]+】',c):parts.append('#### '+escaped(c))
        else:
            # 문단 첫 숫자가 자동 목록으로 변하지 않게 보존한다.
            c=escaped(c)
            c=re.sub(r'^(\d+)([.)])',lambda m:m[1]+'\\'+m[2],c)
            c=re.sub(r'^([#>+\-])(?=\s)',r'\\\1',c)
            parts.append(c)
    result='\n\n'.join(parts)
    return result.replace('⟦원문이미지36958970⟧','![출원 표장 원본](검토_기준/원본/198440_표장.png)')

def source_load(r):
    sid=Path(r['원본경로']).name.split('_')[0]
    src=ARCHIVE/'재현/원본'/f'{sid}.json.gz'
    data=gzip.decompress(src.read_bytes())
    assert digest(data)==r['원본SHA256'], (r['ID'],'보관 원본 지문 불일치')
    shutil.copyfile(src,RAW/src.name)
    doc=json.loads(data)['PrecService']
    assert doc['사건번호']==r['사건번호']
    return sid,doc,data

def original_sections(doc, prefix=''):
    fields=[('판례내용','fulltext',None),('판시사항','issues','판시사항'),('판결요지','summary','판결요지'),('참조조문','statutes','참조조문'),('참조판례','references','참조판례')]
    out=[]
    for key,anchor,title in fields:
        out += [f'<a id="{prefix}{anchor}"></a>']
        if title: out.append(f'### {title}')
        out += [f'<!-- 원문시작:{prefix}{key} -->', render(doc.get(key,'')) or '해당 필드에 내용이 없습니다.',f'<!-- 원문끝:{prefix}{key} -->']
    return '\n\n'.join(out)

def original_note(rid):
    base='보관된 JSON의 판시사항·판결요지·참조조문·참조판례·판례내용을 모두 옮겼습니다. 아래 원문은 쉬운 말로 고치거나 요약하지 않았고, 제목과 줄바꿈 등 읽는 형식만 정리했습니다. 다수의견뿐 아니라 원본에 들어 있는 다른 의견도 그대로 남겼습니다.'
    base+=' 원본에 없는 소송기록·별지·이미지는 새로 만들어 넣지 않았습니다. 이는 보관된 텍스트의 전문이며, 사건의 증거기록 전부를 확보했다는 뜻은 아닙니다.'
    if rid=='C24':base+=' **본문·판결요지의 표장 자리는 빈칸이지만 판시사항에는 이미지 주소가 있었습니다. 이번에 같은 파일 번호를 공식 LSW 다운로드 경로에서 받아 아래 판시사항에 넣었습니다. 본문의 빈칸 자체를 임의로 고치지는 않았습니다.**'
    if rid in ['C02','C11']:base+=' 본문이 가리키는 별지의 완전성은 별도로 확인해야 합니다. 누락된 별지 내용을 추정해 보충하지 않았습니다.'
    return base

def material_links(case):
    text=(BASE/'초등독자_전수개정/검토정의/전문가 에이전트 정의 2.md').read_text()
    all_names=set(re.findall(r'^#### (.+)$',text,re.M))
    for name,_,_ in case['steps']:assert name in all_names,(case['id'],name)
    return all_names

def annotated_original(doc, sid, prefix=''):
    folder=BASE/'단락_해설'
    parts=json.loads((folder/f'{sid}_paragraphs.json').read_text())
    note_path=folder/f'{sid}_notes.json'
    notes=json.loads(note_path.read_text()) if note_path.exists() else {}
    if notes:assert set(notes)=={str(i) for i in range(len(parts))},sid
    out=[f'<a id="{prefix}fulltext"></a>',f'<!-- 원문시작:{prefix}판례내용 -->']
    for j,part in enumerate(parts):
        tag='h4' if re.fullmatch(r'【[^】]+】',part) else 'p'
        out.append(f'<{tag} class="original" style="color: #82AAFF;">'+html.escape(part)+f'</{tag}>')
        if notes.get(str(j)):
            out.append('<p class="explanation" style="color: #FFD54F;">'+html.escape(notes[str(j)])+'</p>')
    out.append(f'<!-- 원문끝:{prefix}판례내용 -->')
    return '\n\n'.join(out)

manifest={'created_at':STAMP,'selection':'기존 24건 중 20건. C06·C13·C17·C20 제외. 분야를 고르게 포함하기 위한 선정이며 절대 난도 순위가 아님.','case_count':20,'autonomous_execution':'미실시','files':[]}
assert len(CASES)==20 and len({c['id'] for c in CASES})==20
names=[]
for i,c in enumerate(CASES,1):
    r=rows[c['id']]; names.append(f'{i:02d}_{slug(c["title"].split(" — ")[0])}_{slug(r["사건번호"])}.md')

for i,c in enumerate(CASES):
    r=rows[c['id']];sid,doc,raw=source_load(r);material_links(c)
    note=NOTES[c['id']]
    assert len(note['actions'])==len(c['steps'])
    date=doc['선고일자']; pretty=f'{date[:4]}-{date[4:6]}-{date[6:8]}'
    official=f'https://www.law.go.kr/LSW/precInfoP.do?precSeq={sid}'
    p=ROOT/names[i]
    short_title=c['title'].split(' — ')[0]
    out=[f'# {i+1:02d}. {short_title}',
         f'{doc["법원명"]} {pretty} · {doc["사건번호"]} · [출처]({official})',
         '[최종 종합 해설](#easy) · [사용 재료](#materials)',
         '---','<a id="original"></a>','## 1. 원문과 단락별 해설',annotated_original(doc,sid)]
    if c['id']=='C24':
        out += ['![출원 표장](검토_기준/원본/198440_표장.png)', '표장 이미지: [공식 첨부 파일](https://www.law.go.kr/LSW/flDownload.do?flSeq=36958970).']
    extras=[]
    if c['id']=='C15':
        for extra in ['600537','600539']:
            sp=ARCHIVE/'재현/원본'/f'{extra}.json.gz'
            rawextra=gzip.decompress(sp.read_bytes());edoc=json.loads(rawextra)['PrecService']
            shutil.copyfile(sp,RAW/sp.name)
            out += [f'<a id="supplement-{extra}"></a>',f'### 관련 판결 원문 — {edoc["사건번호"]}',
                    f'대법원 2024-12-19 · [출처](https://www.law.go.kr/LSW/precInfoP.do?precSeq={extra})',annotated_original(edoc,extra,f'{extra}-')]
            extras.append({'source_id':extra,'case_number':edoc['사건번호'],'raw_sha256':digest(rawextra)})
    out += ['---','<a id="easy"></a>','## 2. 최종 종합 해설']
    for heading, explanation in DETAILS[c['id']]:
        out += ['### '+heading, '<p class="explanation" style="color: #FFD54F;">'+html.escape(explanation)+'</p>']
    out += ['### 질문으로 확인하기']
    qa=READER_QA[c['id']]
    assert len(qa)==4
    for q,a,why in qa:
        assert a in ('예','아니오'), (c['id'],q,a)
        out += [f'**{q} → {"YES" if a=="예" else "NO"}**',
                '<p class="explanation" style="color: #FFD54F;">'+html.escape(why)+'</p>']
    out += ['---','<a id="materials"></a>','## 3. 사용 재료와 보완점',
            '### 어떤 재료를 어떻게 쓰나',
            '| 사용할 재료 | 이 사건에서 하는 일 | 남겨야 할 결과 |','|---|---|---|']
    assert len(OUTPUTS[c['id']]) == len(c['steps'])
    for (name,_,_),action,result in zip(c['steps'],note['actions'],OUTPUTS[c['id']]):
        out.append(f'| {name} | {action} | {result} |')
    out += ['### 지금 상태와 필요한 변화',
            '| 지금은 어떤 상태인가 | 무엇이 부족한가 | 어떻게 바꿔야 하나 | 바꾸면 어떻게 되나 | 어디까지 끝났나 |',
            '|---|---|---|---|---|']
    doc_status = '이 파일에 적용 방법 작성? YES.<br>이 사건으로 AI 실행 시험 완료? NO.'
    if c['id']=='C24':
        doc_status = '이 파일에 원본 그림 추가? YES.<br>AI가 누락을 찾는 실행 시험 완료? NO.'
    for change_row in [(*CASE_ROWS[c['id']],doc_status),
                       *(COMMON_ROWS[k] for k in c['issues'])]:
        assert len(change_row)==5
        out.append('| '+' | '.join(value.replace('|','·') for value in change_row)+' |')
    input_case,expected = TESTS[c['id']]
    out += ['### 이 사건으로 무엇을 시험해야 하나',
            '**시험할 입력**',input_case,'**통과하려면**',expected,
            '**실제로 실행해 통과했나? → NO**',
            '위 상황을 AI에 주고 실제 답변과 처리 결과를 확인하는 시험은 아직 하지 않았습니다.',
            '**새 재료가 꼭 필요한가? → NO**',
            '이 사건을 문서로 검토한 범위에서는 기존 79개 재료로 다룰 수 있습니다. 각 재료에 이 사건의 확인 항목을 넣고, 위 표의 순서도·설명·시험을 고쳐야 합니다. 실제로 제대로 처리하는지는 별도 시험이 필요합니다.',
            f'*재료 검토 기준: 79개 · {REVIEW_STAMP} 보관본 · 실제 실행 시험: 미실시*']
    p.write_text(finish_document(out))
    refs={key:[{'file':fn,'line':ln,'snapshot':'초등독자_전수개정/검토정의/'+fn} for fn,ln in CURRENT_LOCATIONS[key]] for key in c['issues']}
    manifest['files'].append({'file':p.name,'review_id':c['id'],'case_number':doc['사건번호'],
        'source_id':sid,'source_path':r['원본경로'],'raw_sha256':digest(raw),
        'md_sha256':digest(p.read_bytes()),'supplemental_cases':extras,'issues':c['issues'],
        'issue_locations':refs,'test_input':input_case,'expected_response':expected})

old_index=ROOT/'00_먼저_보기.md'
if old_index.exists():old_index.unlink()
manifest['layout']='각 파일: 원문 → 해설 → 사용 재료와 보완점. 별도 안내 파일 없음.'
manifest['revised_at']=datetime.datetime.now().astimezone().isoformat()
manifest['beginner_review']=CURRENT_REVIEW
manifest['original_color']='#82AAFF'
manifest['explanation_color']='#FFD54F'
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'판례 {len(names)}개를 원문 → 해설 → 사용 재료 순서로 저장했습니다.')
