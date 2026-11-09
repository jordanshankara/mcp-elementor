// Kosongkan cache aset Astra lewat bridge: tulis ulang satu opsi dengan nilai sama (theme-option memanggil astra_clear_all_assets_cache).
// Pakai: node astra-flush.mjs <alias>
import fs from 'node:fs';
const cfg = JSON.parse(fs.readFileSync('E:/1. Code/config/sites.local.json', 'utf8'));
const site = cfg.sites[process.argv[2]];
if (!site) { console.error('alias tidak ada'); process.exit(1); }
const auth = 'Basic ' + Buffer.from(site.user + ':' + String(site.app_password).replace(/\s+/g, ' ')).toString('base64');
const base = site.url.replace(/\/$/, '') + '/wp-json/claude/v1';
const tryFetch = async (url, init) => { for (let i = 1; ; i++) { try { return await fetch(url, init); } catch (e) { if (i >= 5) throw e; await new Promise((r) => setTimeout(r, 3000 * i)); } } };
const r = await tryFetch(base + '/theme-option', { method: 'POST', headers: { Authorization: auth, 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'astra-settings', merge: { 'header-main-sep': 1 } }) });
console.log(r.status, (await r.text()).slice(0, 120));
