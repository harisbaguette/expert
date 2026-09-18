"""원본과 실제 Markdown 렌더링 결과를 대조한다. 생성 모듈은 호출하지 않는다."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import datetime, gzip, hashlib, json, re
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.검토_기준'
manifest = json.loads((BASE / 'manifest.json').read_text())
md = MarkdownIt('commonmark', {'html': True}).enable('table')

class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_data(self, value):
        self.parts.append(value)

def visible(value):
    parser = Visible()
    parser.feed(value)
    parser.close()
    return re.sub(r'\s+', '', ''.join(parser.parts))

def sha(value):
    return hashlib.sha256(value).hexdigest()

fields = ['판시사항', '판결요지', '참조조문', '참조판례', '판례내용']
checks, links, tables = [], 0, 0
assert len(manifest['files']) == 20
assert len(list(ROOT.glob('*.md'))) == 20
for info in manifest['files']:
    path = ROOT / info['file']
    content = path.read_text()
    assert sha(path.read_bytes()) == info['md_sha256'], path.name
    sources = [(info['source_id'], '', info['raw_sha256'])]
    sources += [(x['source_id'], x['source_id']+'-', x['raw_sha256']) for x in info['supplemental_cases']]
    for sid, prefix, expected_sha in sources:
        raw = gzip.decompress((BASE / '원본' / (sid+'.json.gz')).read_bytes())
        assert sha(raw) == expected_sha, sid
        doc = json.loads(raw)['PrecService']
        for field in fields:
            pattern = re.escape('<!-- 원문시작:'+prefix+field+' -->') + r'(.*?)' + re.escape('<!-- 원문끝:'+prefix+field+' -->')
            match = re.findall(pattern, content, re.S)
            assert len(match) == 1, (path.name, field, '구역 누락/중복')
            original = visible(str(doc.get(field) or ''))
            rendered = visible(md.render(match[0]))
            if not original:
                assert rendered == '해당필드에내용이없습니다.'
            else:
                if original != rendered:
                    at = next((i for i, (a,b) in enumerate(zip(original, rendered)) if a != b), min(len(original),len(rendered)))
                    raise AssertionError((path.name, sid, field, at, original[max(0,at-30):at+60], rendered[max(0,at-30):at+60]))
            checks.append({'file':path.name,'source_id':sid,'field':field,'nonspace_characters':len(original),'preserved':True})
    assert '재료 검토 기준: 79개' in content, path.name
    assert '실제 실행 시험: 미실시' in content, path.name
    assert re.findall(r'^## .+$',content,re.M)==['## 1. 원문','## 2. 해설','## 3. 사용 재료와 보완점'], path.name
    assert content.index('원문시작:판례내용') < content.index('원문시작:판시사항') < content.index('## 2. 해설'), path.name
    assert '이 파일 하나에 설명과 원문이 모두 있습니다' not in content
    assert '00_먼저_보기' not in content
    assert not re.search(r'음했나요|함했나요|봄했나요|나눔했나요', content)

for path in ROOT.glob('*.md'):
    content = path.read_text()
    tokens = md.parse(content)
    count = sum(t.type == 'table_open' for t in tokens)
    assert count == 1, (path.name, '표 렌더링', count)
    tables += count
    all_tokens = list(tokens)
    for token in tokens:
        if token.children:
            all_tokens.extend(token.children)
    for token in all_tokens:
        target = token.attrGet('href') if token.type == 'link_open' else token.attrGet('src') if token.type == 'image' else None
        if not target:
            continue
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        destination = (path.parent / unquote(url.path)) if url.path else path
        assert destination.exists(), (path.name, target, '연결 파일 없음')
        if url.fragment:
            assert f'id="{unquote(url.fragment)}"' in destination.read_text(), (path.name, target, '이동 위치 없음')
        links += 1

snapshot = json.loads((BASE/'작성시점.json').read_text())
for item in snapshot['files']:
    assert sha((ROOT/item['snapshot']).read_bytes()) == item['sha256']

from PIL import Image, ImageChops
with Image.open(BASE/'원본/198440_표장.bmp') as original, Image.open(BASE/'원본/198440_표장.png') as displayed:
    assert original.size == displayed.size
    assert ImageChops.difference(original.convert('RGB'),displayed.convert('RGB')).getbbox() is None

report = {
    'verified_at': datetime.datetime.now().astimezone().isoformat(),
    'result': '통과',
    'case_files':20, 'index_files':0, 'original_cases':22,
    'original_fields_checked':len(checks),
    'original_characters_excluding_whitespace':sum(x['nonspace_characters'] for x in checks),
    'method':'원본 HTML의 표시 문자와 Markdown을 HTML로 렌더링한 표시 문자를 공백 제외 전수 대조. 생성 함수를 재사용하지 않음.',
    'local_links_checked':links, 'tables_rendered':tables,
    'source_hashes_and_snapshot_hashes':'일치', 'trademark_image_pixels':'일치',
    'legal_reasoning_automatically_proved':False,
    'agent_autonomous_execution_tested':False,
    'fields':checks
}
(BASE/'검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='fields'},ensure_ascii=False,indent=2))
