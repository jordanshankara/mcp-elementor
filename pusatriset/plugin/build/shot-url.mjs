// Screenshot halaman publik di 3 ukuran + cek overflow horizontal. Pakai: node shot-url.mjs <url> <awalan-nama> [folder]
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const [url, name, dir = 'C:/Users/LENOVO~1/AppData/Local/Temp/claude/c72139456fe3ad00/1683db9e-be5d-404a-9c30-db44ad92af69/scratchpad/live'] = process.argv.slice(2);
fs.mkdirSync(dir, { recursive: true });
const b = await chromium.launch();
for (const [label, w, h] of [['desktop', 1440, 900], ['tablet', 820, 1100], ['mobile', 390, 844]]) {
  const p = await (await b.newContext({ viewport: { width: w, height: h } })).newPage();
  const errs = [];
  p.on('pageerror', (e) => errs.push(String(e).slice(0, 120)));
  const res = await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.addStyleTag({ content: '.surecookie,[class*=cookie]{display:none!important}' }).catch(() => {});
  const info = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight }));
  await p.screenshot({ path: `${dir}/${name}-${label}.png`, fullPage: true });
  console.log(label, res && res.status(), JSON.stringify(info), info.sw > info.cw ? 'OVERFLOW-X' : 'ok', errs.length ? errs.join(' | ') : '');
  await p.close();
}
await b.close();
