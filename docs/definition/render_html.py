"""Build standalone reading views from Markdown and locally rendered diagrams."""
import base64
import hashlib
import html
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote

from definition_lib import ROOT

HERE = Path(__file__).resolve().parent


def node_environment():
    env = os.environ.copy()
    # Prefer explicitly configured modules. Existing npm cache is a local fallback.
    cache = Path.home() / '.npm/_npx'
    for key, suffix in [('PLAYWRIGHT_MODULE', 'node_modules/playwright'), ('MERMAID_SCRIPT', 'node_modules/mermaid/dist/mermaid.js')]:
        if key not in env:
            found = sorted(cache.glob(f'*/{suffix}')) if cache.exists() else []
            if found:
                env[key] = str(found[0])
    return env


def data_uri(path):
    media = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{media};base64,' + base64.b64encode(path.read_bytes()).decode()


def render_diagrams():
    primary = ROOT / '전문가 에이전트 정의.md'
    source = primary.read_text()
    blocks = re.findall(r'```mermaid\n(.*?)```', source, re.S)
    digest = hashlib.sha256(primary.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='expert-diagrams-') as directory:
        input_path = Path(directory) / 'input.json'
        input_path.write_text(json.dumps({'source_sha256':digest, 'diagrams':blocks}))
        subprocess.run(['node', str(HERE/'render_mermaid.cjs'), str(input_path), str(HERE/'rendered')], env=node_environment(), check=True)
    return json.loads((HERE/'rendered/manifest.json').read_text())


def embed_image(match):
    src = html.unescape(match[1])
    if src.startswith(('data:', 'http:', 'https:')):
        return match[0]
    image_path = ROOT / unquote(src)
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    return 'src="'+data_uri(image_path)+'"'


def diagram_replacer(diagrams):
    items = iter(diagrams)
    def replace(_):
        item = next(items)
        file = HERE/'rendered'/item['file']
        return '\n<figure><div class="diagram"><img alt="업무 정의 흐름도" src="'+data_uri(file)+'" style="width:'+str(item['viewBox'][2])+'px"></div><figcaption><a href="docs/definition/rendered/'+item['file']+'">흐름도 원본 크게 열기</a></figcaption></figure>\n'
    return replace


def render_document(name, manifest):
    md = ROOT / f'{name}.md'
    text = re.sub(r'```mermaid\n.*?```', diagram_replacer(manifest['diagrams']), md.read_text(), flags=re.S)
    body = subprocess.run(['pandoc','--from=gfm+tex_math_dollars','--to=html5','--mathml'], input=text, text=True, capture_output=True, check=True).stdout
    body = re.sub(r'src="([^"]+)"', embed_image, body)
    body = body.replace('<table>', '<div class="table-scroll" tabindex="0"><table>').replace('</table>', '</table></div>')
    body = re.sub(r'<p>(<math display="block".*?</math>)</p>', r'<div class="math-scroll" tabindex="0">\1</div>', body, flags=re.S)
    if '<code class="mermaid"' in body or 'language-mermaid' in body:
        raise ValueError('렌더되지 않은 Mermaid')
    digest = hashlib.sha256(md.read_bytes()).hexdigest()
    style = (HERE/'view.css').read_text()
    result = '<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(name)+'</title><style>'+style+'</style></head><body><!-- source-sha256: '+digest+' --><main>'+body+'</main></body></html>\n'
    (ROOT/f'{name}.html').write_text(result)
    print(f'{name}.html 생성 완료')


def main():
    manifest = render_diagrams()
    for name in ('전문가 에이전트 정의', '진행-계획'):
        render_document(name, manifest)


if __name__ == '__main__':
    main()
