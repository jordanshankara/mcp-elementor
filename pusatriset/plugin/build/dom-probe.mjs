// Cetak ringkasan DOM header/footer. Pakai: node dom-probe.mjs <url>
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto(process.argv[2], { waitUntil: 'networkidle' });
console.log(await p.evaluate(() => {
  const q = (s) => document.querySelector(s);
  const out = [];
  out.push('branding: ' + (q('.site-branding')?.outerHTML || 'TIDAK ADA').slice(0, 400));
  out.push('header-row: ' + [...document.querySelectorAll('.ast-primary-header-bar .ast-builder-grid-row > div')].map((d) => d.className + ' [' + d.children.length + ']').join(' | '));
  out.push('footer-primary: ' + (q('.site-primary-footer-wrap')?.outerHTML || 'TIDAK ADA').slice(0, 900));
  out.push('footer-widgets: ' + [...document.querySelectorAll('[class*=footer-widget]')].map((d) => d.className.slice(0, 60) + ' len=' + d.innerHTML.length).join(' | '));
  return out.join('\n');
}));
await b.close();
