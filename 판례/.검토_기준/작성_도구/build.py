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
from simple_notes import NOTES, SIMPLE_ISSUES, RESULTS, STORIES, QA_REPLACEMENTS
from beginner_cases import DETAILS, COMMON_ROWS, ALREADY, CASE_ROWS, TESTS, OUTPUTS

BASE = ROOT / '.검토_기준'
RAW = BASE / '원본'
RAW.mkdir(exist_ok=True)
rows = {r['ID']: r for r in csv.DictReader((ARCHIVE/'02_24건_대입결과.csv').open(encoding='utf-8-sig'))}
snap = json.loads((BASE/'작성시점.json').read_text())
STAMP = snap['created_at']
CURRENT_REVIEW = json.loads((BASE/'초보자_개정/검토시점.json').read_text())
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

ISSUES = {
 'D01': ('79개 재료와 대응표가 맞나요?', '아니오', '본문은 79개인데 상세 대응표는 77개로 적혀 있습니다. 「못 찾음·없음 구분」과 「보고 주체 확인」이 빠진 대응표를 맞춰야 합니다. 두 재료 자체는 정의 문서에 이미 있습니다.', [('materials.md',48),('전문가 에이전트 정의 2.md',1117)]),
 'D02': ('목표가 그대로면 새 증거 확인을 건너뛰어도 되나요?', '아니오', '큰 순서도에는 목표·범위가 안 바뀌면 바로 대안 판단으로 가는 길이 있습니다. 새 증거·법리·권한이 바뀌었는지도 먼저 보고, 필요한 자료 확인과 관련 결과의 재검사로 연결해야 합니다. 이 책임 자체는 「현재 진행 상태」에 이미 있습니다.', [('전문가 에이전트 정의.md',660),('전문가 에이전트 정의 2.md',3605)]),
 'D03': ('사용자가 직접 요청한 긴급 업무도 긴급도 판단이 필요한가요?', '예', '큰 순서도는 신호 입력에서 긴급 판단으로 이어지지만 사용자 요청은 다른 길로 갑니다. 입력 경로와 관계없이 임박한 기한과 즉시 막을 피해를 확인하도록 맞춰야 합니다. 긴급하다는 이유로 권한을 넓히지는 않습니다.', [('전문가 에이전트 정의.md',590)]),
 'D04': ('실행 결과를 성공과 실패 두 개로만 나눠도 되나요?', '아니오', '큰 순서도에는 실패 여부의 두 갈래가 남아 있습니다. 상세 정의에 이미 있는 일부 성공·결과 불명을 연결해야 합니다. 처리 여부를 모르면 원래 요청부터 조회하고, 확인 전에는 다시 실행하지 않습니다.', [('전문가 에이전트 정의.md',690),('전문가 에이전트 정의 2.md',6458)]),
 'D05': ('답변을 기다리는 것만 적으면 후속 처리가 충분한가요?', '아니오', '기다릴 기한·담당·깨울 조건·답이 없을 때의 다음 행동이 필요합니다. 「대기·후속 관리」에 이미 있는 조건을 큰 순서도의 답변 대기에도 연결해야 합니다.', [('전문가 에이전트 정의.md',639),('전문가 에이전트 정의 2.md',5480)]),
 'D06': ('사람에게 일부를 넘겼으면 같은 건의 모든 작업을 멈춰야 하나요?', '아니오', '본문은 영향받지 않는 작업을 계속하라고 합니다. 그런데 시험표는 그 건의 이후 도구 호출을 전부 0건으로 요구합니다. 보류 대상만 막고, 허용된 독립 작업과 상태 확인은 이어 갈 수 있도록 시험 조건을 맞춰야 합니다.', [('전문가 에이전트 정의 2.md',5122),('전문가 에이전트 정의 2.md',5153)]),
 'D07': ('필수 검사를 못 했어도 확신도만 낮추고 통과해도 되나요?', '아니오', '상세 본문은 필수 검사 불가를 통과시키지 말라고 합니다. 검증 순서도에는 검사 못 함에서 채점으로 넘어가는 길이 남아 있습니다. 필수 검사인지 나누고, 필요한 자료 확보·대체 검사·미완료 처리로 이어야 합니다.', [('전문가 에이전트 정의 2.md',7056),('전문가 에이전트 정의 2.md',7292)]),
 'D08': ('바뀐 옛 판례를 모든 상황에서 근거로 쓰지 못하게 막아도 되나요?', '아니오', '「적용 사례」의 설명·시험표는 뒤집힌 해석을 근거로 쓴 수를 0건으로 요구합니다. 통상임금처럼 종전 법리를 적용해야 할 범위가 남는 경우를 구분해야 합니다. 해당 시점·쟁점에 적용할 수 없는 법리를 막도록 조건을 구체화해야 합니다.', [('전문가 에이전트 정의 2.md',2981),('전문가 에이전트 정의 2.md',3001)])
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
    return result.replace('⟦원문이미지36958970⟧','![출원 표장 원본](.검토_기준/원본/198440_표장.png)')

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
    text=(BASE/'초보자_개정/검토정의/전문가 에이전트 정의 2.md').read_text()
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
        out.append(render(html.escape(part)))
        if notes.get(str(j)):
            out.append('<p class="explanation" style="color: #1565c0;">'+html.escape(notes[str(j)])+'</p>')
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
        out += ['![출원 표장](.검토_기준/원본/198440_표장.png)', '표장 이미지: [공식 첨부 파일](https://www.law.go.kr/LSW/flDownload.do?flSeq=36958970).']
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
        out += ['### '+heading, '<p class="explanation" style="color: #1565c0;">'+html.escape(explanation)+'</p>']
    out += ['### 질문으로 확인하기']
    qa=list(c['qa'])
    for at,replacement in QA_REPLACEMENTS.get(c['id'],{}).items():qa[at]=replacement
    if c['id']=='C24':qa=qa[:4]
    if c['id']=='C10':qa=qa[:3]
    for q,a,why in qa:
        out += [f'**{q} → {"YES" if a=="예" else "NO"}**',
                '<p class="explanation" style="color: #1565c0;">'+html.escape(why)+'</p>']
    out += ['---','<a id="materials"></a>','## 3. 사용 재료와 보완점',
            '### 어떤 재료를 어떻게 쓰나',
            '| 사용할 재료 | 이 사건에서 하는 일 | 남겨야 할 결과 |','|---|---|---|']
    assert len(OUTPUTS[c['id']]) == len(c['steps'])
    for (name,_,_),action,result in zip(c['steps'],note['actions'],OUTPUTS[c['id']]):
        out.append(f'| {name} | {action} | {result} |')
    out += ['### 지금 상태와 필요한 변화',
            '| 지금은 어떤 상태인가 | 무엇이 부족한가 | 어떻게 바꿔야 하나 | 바뀌면 어떤 모습인가 | 지금 반영됐나 |',
            '|---|---|---|---|---|']
    doc_status = '해당 정의 반영 YES.<br>이 사건 실제 실행 검증 NO.'
    if c['id']=='C24':
        doc_status = '재료 정의·이 문서 원본 그림 확보 YES.<br>에이전트 실행 검증 NO.'
    for change_row in [(*ALREADY[c['id']],doc_status),
                       (*CASE_ROWS[c['id']],'이 문서에 적용안 작성 YES.<br>구현·실행 완료 확인 NO.'),
                       *(COMMON_ROWS[k] for k in c['issues'])]:
        assert len(change_row)==5
        out.append('| '+' | '.join(value.replace('|','·') for value in change_row)+' |')
    input_case,expected = TESTS[c['id']]
    out += ['### 이 사건으로 무엇을 시험해야 하나',
            '**시험할 입력**',input_case,'**통과하려면**',expected,
            '**실제로 실행해 통과했나? → NO**',
            '판례와 정의 문서를 대조했습니다. 위 입력으로 에이전트가 작동한 결과는 확인하지 않았습니다.',
            '**새 재료가 꼭 필요한가? → NO**',
            '이 사건에서 79개 밖의 새 재료가 꼭 필요하다는 근거는 찾지 못했습니다. 기존 재료에 사건별 확인 항목을 채우고, 표에 적은 연결과 시험을 보완해야 합니다.',
            f'*재료 검토 기준: 79개 · {REVIEW_STAMP} 보관본 · 실제 실행 시험: 미실시*']
    p.write_text(finish_document(out))
    refs={key:[{'file':fn,'line':ln,'snapshot':'초보자_개정/검토정의/'+fn} for fn,ln in CURRENT_LOCATIONS[key]] for key in c['issues']}
    manifest['files'].append({'file':p.name,'review_id':c['id'],'case_number':doc['사건번호'],
        'source_id':sid,'source_path':r['원본경로'],'raw_sha256':digest(raw),
        'md_sha256':digest(p.read_bytes()),'supplemental_cases':extras,'issues':c['issues'],
        'issue_locations':refs,'test_input':r['변형입력'],'expected_response':r['기대반응']})

old_index=ROOT/'00_먼저_보기.md'
if old_index.exists():old_index.unlink()
manifest['layout']='각 파일: 원문 → 해설 → 사용 재료와 보완점. 별도 안내 파일 없음.'
manifest['revised_at']=datetime.datetime.now().astimezone().isoformat()
manifest['beginner_review']=CURRENT_REVIEW
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'판례 {len(names)}개를 원문 → 해설 → 사용 재료 순서로 저장했습니다.')
