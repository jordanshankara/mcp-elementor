// Impor JSONL ke situs lewat REST plugin PusatRiset Data (idempoten REPLACE INTO; aman diulang / dilanjutkan).
// Pakai: node import-remote.mjs <alias> [tabel,tabel,...] [--status]
// Kredensial dibaca dari config/sites.local.json (rahasia, tidak pernah dicetak).
import fs from 'node:fs';
import readline from 'node:readline';

const cfg = JSON.parse(fs.readFileSync('E:/1. Code/config/sites.local.json', 'utf8'));
const alias = process.argv[2];
const site = cfg.sites[alias];
if (!site) { console.error('alias tidak ada'); process.exit(1); }
const auth = 'Basic ' + Buffer.from(site.user + ':' + String(site.app_password).replace(/\s+/g, ' ')).toString('base64');
const api = site.url.replace(/\/$/, '') + '/wp-json/pusatriset/v1';
const DATA = 'E:/1. Code/pusatriset/extract/data/';
const STATE = 'E:/1. Code/pusatriset/extract/data/_import_state.json';
const ORDER = ['approved_venues', 'policy_tags', 'search_synonyms', 'search_terms', 'institutions', 'authors', 'papers', 'paper_titles', 'paper_identifiers', 'paper_authors', 'author_affiliations', 'paper_affiliation_countries', 'paper_topics', 'citation_stats', 'summaries', 'paper_relations', 'relevance_scores', 'venue_arxiv_categories'];

async function call(path, method, body) {
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      const r = await fetch(api + path, { method, headers: { Authorization: auth, 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
      const t = await r.text();
      if (r.ok) return JSON.parse(t);
      if (r.status < 500 && r.status !== 429) throw new Error(r.status + ' ' + t.slice(0, 200));
    } catch (e) { if (attempt === 5) throw e; }
    await new Promise((res) => setTimeout(res, 1500 * attempt));
  }
}

if (process.argv.includes('--status')) { console.log(JSON.stringify(await call('/status', 'GET'), null, 1)); process.exit(0); }

const only = process.argv[3] && !process.argv[3].startsWith('--') ? process.argv[3].split(',') : ORDER;
const state = fs.existsSync(STATE) ? JSON.parse(fs.readFileSync(STATE, 'utf8')) : {};
state[alias] = state[alias] || {};
for (const t of only) {
  const f = DATA + t + '.jsonl';
  if (!fs.existsSync(f)) { console.log('lewati', t); continue; }
  const done = state[alias][t] || 0;
  const batchSize = t === 'papers' || t === 'summaries' ? 150 : 600;
  // Pecah baris HANYA di \n (readline juga memecah di U+2028/U+2029 yang sah di dalam teks JSON).
  const rl = (async function* () {
    let buf = '';
    for await (const chunk of fs.createReadStream(f, 'utf8')) {
      buf += chunk;
      let p;
      while ((p = buf.indexOf('\n')) >= 0) { yield buf.slice(0, p); buf = buf.slice(p + 1); }
    }
    if (buf) yield buf;
  })();
  let i = 0, batch = [], sent = 0; const t0 = Date.now();
  const flush = async () => { if (!batch.length) return; await call('/import', 'POST', { table: t, rows_b64: Buffer.from(JSON.stringify(batch)).toString('base64') }); i += 0; sent += batch.length; state[alias][t] = (state[alias][t] || 0) + batch.length; fs.writeFileSync(STATE, JSON.stringify(state)); batch = []; };
  for await (const line of rl) {
    if (!line.trim()) continue;
    i++;
    if (i <= done) continue; // sudah terkirim
    batch.push(JSON.parse(line));
    if (batch.length >= batchSize) { await flush(); process.stdout.write(`\r${t} ${done + sent}`); }
  }
  await flush();
  console.log(`\r${t} selesai ${done + sent} baris (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
}
await call('/flush', 'POST');
console.log(JSON.stringify((await call('/status', 'GET')).counts));
