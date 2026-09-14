// Render local Mermaid sources without network access. See README for dependencies.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

async function renderDiagram(page, code, i, output) {
  const svg = await page.evaluate(async ({ code, i }) => {
    const result = await mermaid.render(`diagram${i}`, code);
    const container = document.createElement('div');
    container.innerHTML = result.svg;
    return new XMLSerializer().serializeToString(container.querySelector('svg'));
  }, { code: code, i });
  const file = `diagram-${i + 1}.svg`;
  fs.writeFileSync(path.join(output, file), svg);
  const viewBox = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  return { file, viewBox };
}

async function main() {
  const [input, output] = process.argv.slice(2);
  const sources = JSON.parse(fs.readFileSync(input, 'utf8'));
  const mermaidPath = process.env.MERMAID_SCRIPT || require.resolve('mermaid/dist/mermaid.js');
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_EXECUTABLE || chromium.executablePath() });
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
    await page.route('http://**/*', route => route.abort());
    await page.route('https://**/*', route => route.abort());
    await page.setContent('<!doctype html><meta charset="utf-8"><body></body>');
    await page.addScriptTag({ path: mermaidPath });
    await page.evaluate(() => mermaid.initialize({
      startOnLoad: false, securityLevel: 'strict', theme: 'base',
      themeVariables: { fontFamily: '-apple-system, Apple SD Gothic Neo, sans-serif', fontSize: '16px', primaryColor: '#eff6ff', primaryTextColor: '#16202b', primaryBorderColor: '#64748b', lineColor: '#64748b', secondaryColor: '#f0fdf4', tertiaryColor: '#fff7ed' },
      flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'linear', nodeSpacing: 35, rankSpacing: 50, wrappingWidth: 240 }
    }));
    const diagrams = [];
    for (let i = 0; i < sources.diagrams.length; i++) {
      diagrams.push(await renderDiagram(page, sources.diagrams[i], i, output));
    }
    fs.writeFileSync(path.join(output, 'manifest.json'), JSON.stringify({ source_sha256: sources.source_sha256, diagram_count: diagrams.length, diagrams }, null, 2) + '\n');
    console.log(`Mermaid ${diagrams.length}개 렌더 완료`);
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
