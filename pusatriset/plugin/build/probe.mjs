import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:8765/katalog/', { waitUntil: 'networkidle' });
console.log(JSON.stringify(await p.evaluate(() => {
  const cb = document.querySelector('input[type=checkbox][name=subfield]');
  const cs = getComputedStyle(cb), lab = cb.parentElement, ls = getComputedStyle(lab);
  const box = document.querySelector('.max-h-48');
  const a = document.querySelector('article a');
  return { cb: cb.getBoundingClientRect().toJSON(), margin: cs.margin, width: cs.width, pad: cs.padding, labW: lab.getBoundingClientRect().width, boxW: box.clientWidth, boxScroll: box.scrollHeight, boxCl: box.clientHeight, font: ls.fontFamily.slice(0, 40), fs: ls.fontSize, aDeco: getComputedStyle(a).textDecorationLine, aW: getComputedStyle(a).fontWeight };
}), null, 1));
await b.close();
