// Screenshot halaman situs WP uji untuk dibandingkan dengan baseline. Pakai: node shot.mjs <outDir> <url:nama>...
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require('../../../wp-elementor-mcp/node_modules/playwright');
const out = path.resolve(process.argv[2]);
fs.mkdirSync(out, { recursive: true });
const jobs = process.argv.slice(3).map((a) => { const i = a.lastIndexOf('='); return [a.slice(i + 1), a.slice(0, i)]; });
const VIEWS = [['desktop', { width: 1440, height: 900 }], ['tablet', { width: 820, height: 1100 }], ['mobile', { width: 390, height: 844 }]];
const browser = await chromium.launch();
for (const [vn, vp] of VIEWS) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.log('pageerror', String(e).slice(0, 120)));
  for (const [name, url] of jobs) {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(400);
    const el = await page.$('.pr-scope');
    const file = path.join(out, `${name}-${vn}.png`);
    if (el) await el.screenshot({ path: file }); else await page.screenshot({ path: file, fullPage: true });
    console.log(vn, name, 'ok');
  }
  await ctx.close();
}
await browser.close();
