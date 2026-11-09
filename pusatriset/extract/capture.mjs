// Tangkap screenshot baseline halaman publik aplikasi lama (localhost:3100) — pembanding "desain tidak boleh berubah".
// Pakai: node capture.mjs <folderKeluar> [baseUrl]
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require('../../wp-elementor-mcp/node_modules/playwright');
const out = path.resolve(process.argv[2] || 'baseline');
const base = process.argv[3] || 'http://localhost:3100';
fs.mkdirSync(out, { recursive: true });
const PAGES = [
  ['home', '/'],
  ['katalog', '/katalog'],
  ['katalog-cari', '/katalog?q=privacy'],
  ['katalog-filter', '/katalog?origin=local&quartile=q1&yearFrom=2023'],
  ['dashboard', '/dashboard'],
  ['metodologi', '/metodologi'],
  ['riset-ringkasan', '/riset/01b0e219-559a-410d-9675-b8d6286b820d?tab=ringkasan'],
  ['riset-data', '/riset/0079b4f4-ed83-44a4-9080-056455683a42'],
  ['riset-relasi', '/riset/1ba3b1ce-a7ed-481f-8bc9-61dca17d631c'],
  ['riset-summary-only', '/riset/08456c97-1a72-47c6-963b-ac68c011ade8'],
];
const VIEWS = [['desktop', { width: 1440, height: 900 }], ['tablet', { width: 820, height: 1100 }], ['mobile', { width: 390, height: 844 }]];
const browser = await chromium.launch();
const report = [];
for (const [vn, vp] of VIEWS) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', (e) => errs.push(String(e).slice(0, 120)));
  for (const [name, url] of PAGES) {
    try {
      const r = await page.goto(base + url, { waitUntil: 'networkidle', timeout: 60000 });
      await page.waitForTimeout(600);
      const file = path.join(out, `${name}-${vn}.png`);
      await page.screenshot({ path: file, fullPage: true });
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      report.push(`${vn} ${name} ${r?.status()} h=${h}`);
    } catch (e) { report.push(`${vn} ${name} GAGAL ${String(e).slice(0, 80)}`); }
  }
  if (errs.length) report.push(`${vn} error JS: ${errs.join(' | ')}`);
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(out, '_laporan.txt'), report.join('\n'));
console.log(report.join('\n'));
