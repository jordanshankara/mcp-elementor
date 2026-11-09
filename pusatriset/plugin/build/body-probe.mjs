// Cetak class <body> dan display header desktop/mobile pada lebar tertentu. Pakai: node body-probe.mjs <url> <lebar>
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const [url, w] = process.argv.slice(2);
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: Number(w), height: 900 } })).newPage();
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
console.log(await p.evaluate(() => {
  const d = (s) => { const e = document.querySelector(s); return e ? getComputedStyle(e).display : 'tidak ada'; };
  return 'body: ' + [...document.body.classList].filter((c) => /ast-(desktop|header-break|mobile)/.test(c)).join(' ') + '\nbreak_point js: ' + (window.astra && window.astra.break_point) + '\ndesktop-header: ' + d('#ast-desktop-header') + '\nmobile-header: ' + d('#ast-mobile-header') + '\nmenu: ' + d('.ast-builder-menu-1');
}));
await b.close();
