// Cetak rantai induk (tag.class, lebar x tinggi, display, align/flex) dari elemen pertama yang cocok selector. Pakai: node chain-probe.mjs <url> <selector> [lebar]
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const [url, sel, w = '390'] = process.argv.slice(2);
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: Number(w), height: 844 } })).newPage();
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
console.log(await p.evaluate((s) => {
  let e = document.querySelector(s); const out = [];
  while (e && e.tagName !== 'BODY') {
    const c = getComputedStyle(e), r = e.getBoundingClientRect();
    out.push(`${e.tagName.toLowerCase()}.${String(e.className).split(' ').slice(0, 3).join('.')} ${Math.round(r.width)}x${Math.round(r.height)} disp=${c.display} dir=${c.flexDirection} ai=${c.alignItems} wrap=${c.flexWrap} h=${c.height} minh=${c.minHeight}`);
    e = e.parentElement;
  }
  return out.join('\n');
}, sel));
await b.close();
