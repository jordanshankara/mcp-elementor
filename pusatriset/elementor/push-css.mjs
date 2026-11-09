// Kirim elementor/custom.css ke CSS Tambahan situs lewat bridge (/claude/v1/custom-css). Kredensial dari config/sites.local.json (tidak dicetak).
// Pakai: node push-css.mjs <alias>
import fs from 'node:fs';
const cfg = JSON.parse(fs.readFileSync('E:/1. Code/config/sites.local.json', 'utf8'));
const site = cfg.sites[process.argv[2]];
if (!site) { console.error('alias tidak ada'); process.exit(1); }
const auth = 'Basic ' + Buffer.from(site.user + ':' + String(site.app_password).replace(/\s+/g, ' ')).toString('base64');
const base = site.url.replace(/\/$/, '') + '/wp-json/claude/v1';
const css = fs.readFileSync(new URL('./custom.css', import.meta.url), 'utf8');
const tryFetch = async (url, init) => { for (let i = 1; ; i++) { try { return await fetch(url, init); } catch (e) { if (i >= 5) throw e; await new Promise((r) => setTimeout(r, 3000 * i)); } } };
const r = await tryFetch(base + '/custom-css', { method: 'POST', headers: { Authorization: auth, 'Content-Type': 'application/json' }, body: JSON.stringify({ css: Buffer.from(css).toString('utf8'), append: false }) });
console.log(r.status, (await r.text()).slice(0, 200));
const f = await tryFetch(base + '/flush', { method: 'POST', headers: { Authorization: auth } });
console.log('flush', f.status);
