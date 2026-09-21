#!/usr/bin/env python3
"""Validate the exact diagram model and browser-measured image geometry."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, hashlib, html, importlib.util, itertools, json, re

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('geometry_checks', Path(__file__).with_name('사용-구조-검증.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def run(render_dir):
    d = json.loads((ROOT / 'docs/도식/단독-상황-이미지.json').read_text())
    measured = json.loads((render_dir / 'geometry.json').read_text())
    svg = (ROOT / 'docs/images/expert-definition/solo-one-expert-flow.svg').read_text()
    prefix = (ROOT / '전문가 에이전트 정의.md').read_text().split('## 사용 구조', 1)[0]
    prefix_sha = hashlib.sha256(prefix.encode()).hexdigest()
    assert prefix_sha == d['source_prefix_sha256'] == 'c65318f94f7ff41325f47dd2a3a4feedf56f4fee59deb94a4518b1a389068c0a'
    assert measured['svg_sha256'] == hashlib.sha256(svg.encode()).hexdigest(), 'Stale browser render'
    embedded = json.loads(html.unescape(re.search(r'<metadata id="usage-structure">(.*?)</metadata>', svg, re.S)[1]))
    assert embedded == d
    catalog = {}
    for line in prefix.split('## 계통별 재료', 1)[1].splitlines():
        if line.startswith('| **') and '✅' in line:
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == 6:
                catalog[re.search(r'\*\*(.*?)\*\*', cells[0])[1]] = cells[4].strip('*')
    ns, es = d['nodes'], d['edges']
    objects = ns | {k: v for k, v in d['groups'].items() if 'x' in v}
    material_nodes = [n for n in ns.values() if n['material']]
    assert len(catalog) == 79
    assert set(catalog) == set(d['catalog']) == {n['name'] for n in material_nodes}
    assert Counter(re.findall(r'data-material="([^"]+)"', svg)) == Counter(n['name'] for n in material_nodes)
    for n in material_nodes:
        assert n['usage'] == catalog[n['name']]
        assert n['note'] and n['canonical_condition'] == d['catalog'][n['name']]['condition']
    assert {n['id'] for n in measured['nodes']} == set(ns)
    issues, outgoing = [], defaultdict(list)
    for i, e in enumerate(es):
        assert e['source'] in objects and e['target'] in objects
        if not g.on_boundary(e['points'][0], objects[e['source']]):
            issues.append(['edge-start', i, e['source']])
        if not g.on_boundary(e['points'][-1], objects[e['target']]):
            issues.append(['edge-end', i, e['target']])
        if e['kind'] != 'apply':
            outgoing[e['source']].append(e)
        if e['kind'] in ('return', 'blocked'):
            assert e['label']
        for k, n in ns.items():
            if k not in (e['source'], e['target']) and any(g.intersects_node(a, b, n) for a, b in zip(e['points'], e['points'][1:])):
                issues.append(['edge-node', i, k])
    for k, n in ns.items():
        if n['kind'] == 'decision':
            assert len(outgoing[k]) >= 2 and all(e['label'] for e in outgoing[k]), k
        if n['kind'] in ('terminal', 'stop'):
            assert (k == 'start' and len(outgoing[k]) == 1) or not outgoing[k], k
    for (a, n), (b, m) in itertools.combinations(ns.items(), 2):
        if g.overlap(n, m, 2):
            issues.append(['node-overlap', a, b])
    for (i, e), (j, f) in itertools.combinations(enumerate(es), 2):
        if any(g.crossing(a, b, c, z) for a, b in zip(e['points'], e['points'][1:]) for c, z in zip(f['points'], f['points'][1:])):
            issues.append(['edge-cross', i, j])
    for item in measured['nodes']:
        n = ns[item['id']]
        for t in item['texts']:
            if n['kind'] == 'decision':
                corners = [(t['x'] + 2, t['y'] + 4), (t['x'] + t['w'] - 2, t['y'] + 4),
                           (t['x'] + 2, t['y'] + t['h'] - 3), (t['x'] + t['w'] - 2, t['y'] + t['h'] - 3)]
                if not all(g.inside(c, n, 0) for c in corners):
                    issues.append(['text-diamond', item['id'], t['text']])
            elif t['x'] < n['x'] - 1 or t['x'] + t['w'] > n['x'] + n['w'] + 1 or t['y'] < n['y'] - 1 or t['y'] + t['h'] > n['y'] + n['h'] + 1:
                issues.append(['text-outside-node', item['id'], t['text']])
    for label in measured['labels'] + measured['annotations']:
        lid = label.get('id', label.get('text'))
        if label['x'] < 0 or label['y'] < 0 or label['x'] + label['w'] > d['width'] or label['y'] + label['h'] > d['height']:
            issues.append(['text-outside-image', lid])
        for k, n in ns.items():
            if g.overlap(label, n, 3):
                issues.append(['label-node', lid, k])
        for i, e in enumerate(es):
            if lid != f'e{i}' and any(g.intersects_node(a, b, label) for a, b in zip(e['points'], e['points'][1:])):
                issues.append(['edge-label', i, lid])
    for a, b in itertools.combinations(measured['labels'], 2):
        if g.overlap(a, b, 2):
            issues.append(['label-label', a['id'], b['id']])
    has = lambda a, b: any(e['source'] == a and e['target'] == b for e in es)
    required = [('plan2', 'ability_needed'), ('capable', 'permit'), ('capable', 'plan1'),
                ('repair', 'permit'), ('more', 'delivery0'), ('delivery0', 'delivery1'),
                ('delivery1', 'receipt'), ('receipt', 'outcome'), ('wait_answer', 'check0'),
                ('receipt', 'receipt_wait'), ('receipt_wait', 'receipt'),
                ('test_passed', 'learn1'), ('test_passed', 'remember'), ('remember', 'finish')]
    assert all(has(a, b) for a, b in required)
    assert not has('plan2', 'permit'), 'Capability check bypassed'
    assert '사용하지 않음' in ns['unused']['note']
    result = {
        'scenario': '단독 상황 — 한 건 · 한 전문가',
        'materials': len(catalog), 'material_types': dict(Counter(catalog.values())),
        'nodes': len(ns), 'connections': len(es),
        'dimensions': [d['width'], d['height']],
        'original_document_prefix_preserved': True,
        'source_prefix_sha256': prefix_sha, 'svg_sha256': measured['svg_sha256'],
        'browser': measured['browser'], 'geometry_issues': issues,
        'scope_of_check': 'Canonical coverage, key flow connections and actual rendered geometry; not a guarantee of universal comprehension.',
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('render_dir', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = run(args.render_dir)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['geometry_issues']))
