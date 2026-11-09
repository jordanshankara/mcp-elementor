// Cetak style terhitung properti tertentu untuk elemen (selector) dan 2 induknya. Pakai: node style-probe.mjs <url> <selector> <lebar> prop1,prop2,...
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const [url, sel, w, props] = process.argv.slice(2);
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: Number(w), height: 844 } })).newPage();
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
console.log(await p.evaluate(([s, pr]) => {
  let e = document.querySelector(s); const out = [];
  for (let i = 0; i < 4 && e; i++, e = e.parentElement) {
    const c = getComputedStyle(e);
    out.push(`${e.tagName.toLowerCase()}.${String(e.className).split(' ').slice(0, 2).join('.')}: ` + pr.split(',').map((k) => `${k}=${c.getPropertyValue(k)}`).join(' | '));
  }
  return out.join('\n');
}, [sel, props]));
await b.close();
