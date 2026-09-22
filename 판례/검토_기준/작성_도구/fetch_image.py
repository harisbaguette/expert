from pathlib import Path
import urllib.request,json,hashlib,datetime
url='https://www.law.go.kr/LSW/flDownload.do?flSeq=36958970'
base=Path(__file__).resolve().parent.parent/'원본'/'198440_표장'
with urllib.request.urlopen(url, timeout=30) as response:
    data=response.read()
    content_type=response.headers.get('Content-Type','')
    final_url=response.url
ext='.png' if data[:8]==b'\x89PNG\r\n\x1a\n' else '.jpg' if data[:3]==b'\xff\xd8\xff' else '.gif' if data[:3]==b'GIF' else '.bmp' if data[:2]==b'BM' else '.webp' if data[:4]==b'RIFF' else None
if ext is None:raise ValueError(f'이미지 응답 확인 필요: type={content_type}, bytes={len(data)}, head={data[:80]!r}')
dest=base.with_suffix(ext);dest.write_bytes(data)
meta={'url':url,'final_url':final_url,'content_type':content_type,'bytes':len(data),'file':dest.name,'sha256':hashlib.sha256(data).hexdigest(),'retrieved_at':datetime.datetime.now().astimezone().isoformat()}
base.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False))
