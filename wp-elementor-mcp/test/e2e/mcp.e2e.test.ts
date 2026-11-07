// E2E: jalankan MCP server sungguhan (stdio) melawan 2 WordPress Playground (Elementor FREE).
// Prasyarat: `npm run playground` sedang berjalan (membuat config/sites.playground.json).
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { ROOT, PKG } from '../../src/sites.ts';

const cfgFile = path.join(ROOT, 'config', 'sites.playground.json');
const base = JSON.parse(readFileSync(cfgFile, 'utf8'));
// tambahkan alias readonly yang menunjuk ke test-a untuk menguji guard readonly
const cfg = { sites: { ...base.sites, 'test-a-ro': { ...base.sites['test-a'], readonly: true, env: 'local', tags: [] } } };
const runCfg = path.join(PKG, '.playground', 'sites.e2e.json');
writeFileSync(runCfg, JSON.stringify(cfg));
const A = base.sites['test-a'];
const B = base.sites['test-b'];
const HOME_A = A._pages.home as number;
const HOME_B = B._pages.home as number;
const CTR_A = A._pages.container as number;
const DOMAIN_B = new URL(B.url).host;

let client: Client;
const results: { name: string; ok: boolean; ms: number; chars: number }[] = [];
let totalChars = 0;

async function call(name: string, args: Record<string, unknown>) {
  const r: any = await client.callTool({ name, arguments: args }, undefined, { timeout: 600_000 });
  const text = (r.content ?? []).map((c: any) => c.text).join('\n');
  totalChars += text.length;
  return { text, isError: !!r.isError };
}
const revOf = (t: string) => /rev(?: baru)?: ([0-9a-f]{12})/.exec(t)?.[1] ?? '';
async function outline(site: string, id: number) { const r = await call('elementor_outline', { site, page_id: id }); assert.ok(!r.isError, r.text); return r; }
async function publicHtml(url: string) { const r = await fetch(url + (url.includes('?') ? '&' : '?') + 'nc=' + Date.now()); return r.text(); }

function t(name: string, fn: () => Promise<void>) {
  test(name, async () => {
    const t0 = Date.now(); const c0 = totalChars;
    try { await fn(); results.push({ name, ok: true, ms: Date.now() - t0, chars: totalChars - c0 }); }
    catch (e) { results.push({ name, ok: false, ms: Date.now() - t0, chars: totalChars - c0 }); throw e; }
  });
}

before(async () => {
  client = new Client({ name: 'e2e', version: '1' });
  await client.connect(new StdioClientTransport({ command: process.execPath, args: [path.join(PKG, 'src', 'index.ts')], env: { ...process.env, WPE_SITES: runCfg } as Record<string, string>, stderr: 'ignore' }));
});
after(async () => {
  await client?.close();
  const lines = results.map((r) => `| ${r.ok ? '✅' : '❌'} | ${r.name} | ${(r.ms / 1000).toFixed(1)}s | ${r.chars} |`);
  const md = `# Laporan E2E wp-elementor-mcp\n\nTanggal: ${new Date().toISOString()}\nSitus: test-a (${A.url}, env local), test-b (${B.url}, disimulasikan PROD) — Elementor FREE, tanpa Pro.\n\n| Hasil | Kasus | Waktu | Karakter output tool |\n|---|---|---|---|\n${lines.join('\n')}\n\nTotal: ${results.filter((r) => r.ok).length}/${results.length} lulus. Total output tool: ${totalChars} karakter (~${Math.round(totalChars / 4)} token).\n`;
  writeFileSync(path.join(ROOT, 'reports', 'e2e-report.md'), md);
});

let origRevA = '';

t('daftar tool lengkap (14) & sites_list + filter tag', async () => {
  const tools = await client.listTools();
  assert.equal(tools.tools.length, 14, tools.tools.map((x) => x.name).join(','));
  const r = await call('sites_list', {});
  assert.match(r.text, /test-a · 127\.0\.0\.1:\d+ · LOCAL · write/);
  assert.match(r.text, /test-b · .* · PROD/);
  const tg = await call('sites_list', { tag: 'satu' });
  assert.match(tg.text, /test-a/); assert.doesNotMatch(tg.text, /test-b/);
});

t('site_health: Elementor FREE + bridge aktif', async () => {
  const r = await call('site_health', { site: 'test-a' });
  assert.ok(!r.isError, r.text);
  assert.match(r.text, /Elementor \d+\.\d+\.\d+ · Free · bridge 1\.0\.0/);
});

t('alias salah ditolak + daftar alias valid', async () => {
  const r = await call('elementor_outline', { site: 'tes-a', page_id: HOME_A });
  assert.ok(r.isError); assert.match(r.text, /tidak dikenal.*test-a/s);
});

t('outline ringkas (bukan JSON penuh) + rev', async () => {
  const r = await outline('test-a', HOME_A);
  assert.match(r.text, /hero1 heading "Selamat Datang di Situs Tes"/);
  assert.match(r.text, /list1 icon-list "Gratis ongkir"/);
  origRevA = revOf(r.text);
  assert.equal(origRevA.length, 12);
  assert.ok(r.text.length < 800, `outline ${r.text.length} karakter`);
});

t('outline halaman container (layout flexbox)', async () => {
  const r = await outline('test-a', CTR_A);
  assert.match(r.text, /ctr1 container/); assert.match(r.text, /cth1 heading "Halaman Container"/);
});

t('elementor_find lintas halaman', async () => {
  const r = await call('elementor_find', { site: 'test-a', query: 'garansi' });
  assert.match(r.text, new RegExp(`#${HOME_A} .*\\n\\s+list1 icon-list icon_list\\[1\\]\\.text`));
});

t('dry_run tidak mengubah apa pun', async () => {
  const r = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev: origRevA, changes: [{ id: 'hero1', settings: { title: 'X' } }], dry_run: true });
  assert.match(r.text, /DRY RUN/);
  assert.equal(revOf((await outline('test-a', HOME_A)).text), origRevA);
});

t('update judul hero → tersimpan, terverifikasi, tampil di HTML publik', async () => {
  const r = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev: origRevA, changes: [{ id: 'hero1', settings: { title: 'Promo 11.11 Diskon 50%' } }] });
  assert.ok(!r.isError, r.text);
  assert.match(r.text, /✓ tersimpan & terverifikasi \(1 teks muncul di render\)/);
  const html = await publicHtml(`${A.url}/?page_id=${HOME_A}`);
  assert.match(html, /Promo 11\.11 Diskon 50%/);
});

t('rev lama ditolak (halaman sudah berubah)', async () => {
  const r = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev: origRevA, changes: [{ id: 'hero1', settings: { title: 'Y' } }] });
  assert.ok(r.isError); assert.match(r.text, /rev tidak cocok/);
});

t('batch update 3 elemen sekaligus', async () => {
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const r = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev, changes: [
    { id: 'hero1', settings: { title: 'Judul Batch' } },
    { id: 'txt1', settings: { editor: '<p>Paragraf batch baru.</p>' } },
    { id: 'btn1', settings: { text: 'Chat WhatsApp', link: { url: 'https://wa.me/6282200000' } } },
  ] });
  assert.ok(!r.isError, r.text);
  assert.match(r.text, /3 teks muncul di render/);
  const g = await call('elementor_get', { site: 'test-a', page_id: HOME_A, element_ids: ['btn1'] });
  assert.match(g.text, /"url":"https:\/\/wa\.me\/6282200000","is_external":"on"/);
});

t('id elemen salah → error jelas, bukan sukses palsu', async () => {
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const r = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev, changes: [{ id: 'tidakada', settings: { title: 'Z' } }] });
  assert.ok(r.isError); assert.match(r.text, /tidak ditemukan/);
  assert.equal(revOf((await outline('test-a', HOME_A)).text), rev);
});

t('rev dari situs A ditolak di situs B (page id sama tidak bisa tertukar)', async () => {
  const revA = revOf((await outline('test-a', HOME_A)).text);
  assert.equal(HOME_A, HOME_B, 'page id sengaja sama di kedua situs');
  const r = await call('elementor_update', { site: 'test-b', page_id: HOME_B, rev: revA, confirm_domain: DOMAIN_B, changes: [{ id: 'hero1', settings: { title: 'SALAH SITUS' } }] });
  assert.ok(r.isError); assert.match(r.text, /rev tidak cocok/);
  assert.doesNotMatch(await publicHtml(`${B.url}/?page_id=${HOME_B}`), /SALAH SITUS/);
});

t('situs PROD wajib confirm_domain yang cocok', async () => {
  const rev = revOf((await outline('test-b', HOME_B)).text);
  const no = await call('elementor_update', { site: 'test-b', page_id: HOME_B, rev, changes: [{ id: 'hero1', settings: { title: 'Prod' } }] });
  assert.ok(no.isError); assert.match(no.text, /wajib isi confirm_domain/);
  const wrong = await call('elementor_update', { site: 'test-b', page_id: HOME_B, rev, confirm_domain: 'tokolain.com', changes: [{ id: 'hero1', settings: { title: 'Prod' } }] });
  assert.ok(wrong.isError);
  const ok = await call('elementor_update', { site: 'test-b', page_id: HOME_B, rev, confirm_domain: DOMAIN_B, changes: [{ id: 'hero1', settings: { title: 'Judul Situs B' } }] });
  assert.ok(!ok.isError, ok.text);
  assert.match(ok.text, /^\[test-b · 127\.0\.0\.1:\d+ · PROD\]/);
});

t('situs readonly menolak semua penulisan', async () => {
  const rev = revOf((await outline('test-a-ro', HOME_A)).text);
  const r = await call('elementor_update', { site: 'test-a-ro', page_id: HOME_A, rev, changes: [{ id: 'hero1', settings: { title: 'RO' } }] });
  assert.ok(r.isError); assert.match(r.text, /READONLY/);
});

t('widget Pro (form) ditolak di Elementor Free + saran alternatif', async () => {
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const r = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'insert', parent_id: 'col1', element: { elType: 'widget', widgetType: 'form', settings: {} } });
  assert.ok(r.isError); assert.match(r.text, /Tidak tersedia di situs ini \(Elementor Free\): form/); assert.match(r.text, /shortcode/);
});

t('guardrail: <script> kustom ditolak', async () => {
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const r = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'insert', parent_id: 'col1', element: { elType: 'widget', widgetType: 'html', settings: { html: '<script>alert(1)</script>' } } });
  assert.ok(r.isError); assert.match(r.text, /script/);
});

t('insert widget Free (heading) → tampil; duplicate section; remove wajib confirm', async () => {
  let rev = revOf((await outline('test-a', HOME_A)).text);
  const ins = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'insert', parent_id: 'col2', index: 0, element: { elType: 'widget', widgetType: 'heading', settings: { title: 'Keunggulan Kami', header_size: 'h2' } } });
  assert.ok(!ins.isError, ins.text);
  const newId = /id elemen baru: (\w+)/.exec(ins.text)![1];
  assert.match(await publicHtml(`${A.url}/?page_id=${HOME_A}`), /Keunggulan Kami/);
  rev = revOf(ins.text);
  const dup = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'duplicate', element_id: 'sec2' });
  assert.ok(!dup.isError, dup.text);
  rev = revOf(dup.text);
  const noConfirm = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'remove', element_id: newId });
  assert.ok(noConfirm.isError); assert.match(noConfirm.text, /destruktif/);
  const rm = await call('elementor_structure', { site: 'test-a', page_id: HOME_A, rev, op: 'remove', element_id: newId, confirm: true });
  assert.ok(!rm.isError, rm.text);
});

t('restore backup tertua → halaman kembali PERSIS seperti semula (rev sama)', async () => {
  const list = await call('elementor_page', { site: 'test-a', page_id: HOME_A, op: 'backups' });
  const keys = [...list.text.matchAll(/(_claude_bk_\w+)/g)].map((m) => m[1]);
  assert.ok(keys.length >= 5, list.text);
  const oldest = keys[keys.length - 1];
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const r = await call('elementor_page', { site: 'test-a', page_id: HOME_A, op: 'restore', key: oldest, rev, confirm: true });
  assert.ok(!r.isError, r.text);
  assert.equal(revOf((await outline('test-a', HOME_A)).text), origRevA);
  assert.match(await publicHtml(`${A.url}/?page_id=${HOME_A}`), /Selamat Datang di Situs Tes/);
});

t('draft_copy → edit draft → apply_draft ke halaman asli', async () => {
  const d = await call('elementor_page', { site: 'test-a', page_id: HOME_A, op: 'draft_copy' });
  assert.ok(!d.isError, d.text);
  const draftId = Number(/Draft dibuat: #(\d+)/.exec(d.text)![1]);
  const drev = revOf((await outline('test-a', draftId)).text);
  const e = await call('elementor_update', { site: 'test-a', page_id: draftId, rev: drev, changes: [{ id: 'hero1', settings: { title: 'Versi Redesign' } }] });
  assert.ok(!e.isError, e.text);
  assert.doesNotMatch(await publicHtml(`${A.url}/?page_id=${HOME_A}`), /Versi Redesign/);
  const trev = revOf((await outline('test-a', HOME_A)).text);
  const ap = await call('elementor_page', { site: 'test-a', page_id: draftId, op: 'apply_draft', target_id: HOME_A, rev: trev, confirm: true });
  assert.ok(!ap.isError, ap.text);
  assert.match(await publicHtml(`${A.url}/?page_id=${HOME_A}`), /Versi Redesign/);
});

t('wp_request: GET ringkas dengan fields; DELETE tanpa confirm ditolak', async () => {
  const g = await call('wp_request', { site: 'test-a', method: 'GET', path: '/wp/v2/pages', fields: 'id,title.raw' });
  assert.ok(!g.isError, g.text); assert.match(g.text, /Beranda Tes/);
  const d = await call('wp_request', { site: 'test-a', method: 'DELETE', path: `/wp/v2/pages/${CTR_A}` });
  assert.ok(d.isError); assert.match(d.text, /confirm=true/);
  const w = await call('wp_request', { site: 'test-a', method: 'POST', path: `/claude/v1/elementor/${HOME_A}`, body: {} });
  assert.ok(w.isError); assert.match(w.text, /hanya lewat elementor_update/);
});

t('media_upload: foto 6000px berat → WebP ≤200KB, alt & dimensi terisi', async () => {
  const W = 6000, H = 4000;
  const raw = Buffer.alloc(W * H * 3);
  for (let i = 0; i < raw.length; i++) raw[i] = (i * 7 + ((i / 3000) | 0) * 13 + (Math.random() * 60) | 0) & 255;
  const file = path.join(PKG, '.playground', 'foto-besar.jpg');
  await sharp(raw, { raw: { width: W, height: H, channels: 3 } }).jpeg({ quality: 95 }).toFile(file);
  const r = await call('media_upload', { site: 'test-a', source: file, alt: 'Foto produk unggulan', slot: 'hero' });
  assert.ok(!r.isError, r.text);
  assert.match(r.text, /6000px jpeg → 1\d{3}px WEBP/);
  assert.match(r.text, /\b1\d{3}x\d{3,4}\b/, 'dimensi dilaporkan');
  const id = Number(/id: (\d+)/.exec(r.text)![1]);
  const kbSize = Number(/WEBP q\d+ (\d+) KB/.exec(r.text)![1]);
  assert.ok(kbSize <= 200, r.text);
  const m = await call('wp_request', { site: 'test-a', method: 'GET', path: `/wp/v2/media/${id}`, fields: 'alt_text,mime_type,source_url' });
  assert.match(m.text, /"alt_text":"Foto produk unggulan"/); assert.match(m.text, /image\/webp/);
  // file yang tersaji publik memang ≤200KB & lebar sesuai slot
  const url = /"source_url":"([^"]+)"/.exec(m.text)![1].replace(/\\\//g, '/');
  const pub = Buffer.from(await (await fetch(url)).arrayBuffer());
  assert.ok(pub.length <= 200 * 1024, `ukuran publik ${pub.length}`);
  const meta = await sharp(pub).metadata();
  assert.equal(meta.format, 'webp'); assert.ok(meta.width! <= 1920 && meta.width! >= 1280, String(meta.width));
});

t('visual_check: tanpa perubahan = SAMA; ubah warna = terdeteksi BERBEDA', async () => {
  const url = `${A.url}/?page_id=${HOME_A}`;
  const s = await call('visual_check', { site: 'test-a', url, op: 'snapshot', label: 'e2e' });
  assert.ok(!s.isError, s.text);
  const same = await call('visual_check', { site: 'test-a', url, op: 'compare', label: 'e2e' });
  console.log(same.text);
  assert.match(same.text, /✓ SAMA/, same.text);
  const rev = revOf((await outline('test-a', HOME_A)).text);
  const u = await call('elementor_update', { site: 'test-a', page_id: HOME_A, rev, changes: [{ id: 'hero1', settings: { title_color: '#FF0000' } }] });
  assert.ok(!u.isError, u.text);
  const diff = await call('visual_check', { site: 'test-a', url, op: 'compare', label: 'e2e' });
  assert.match(diff.text, /✗ BERBEDA/, diff.text);
});

t('elementor_design perf_get + kit_get ringkas', async () => {
  const p = await call('elementor_design', { site: 'test-a', op: 'perf_get' });
  assert.ok(!p.isError, p.text); assert.match(p.text, /css_print_method/);
  const k = await call('elementor_design', { site: 'test-a', op: 'kit_get', keys: ['system_colors'] });
  assert.ok(!k.isError, k.text); assert.match(k.text, /hash:/);
  const n = await call('elementor_design', { site: 'test-a', op: 'perf_set', option: 'elementor_font_display', value: 'swap' });
  assert.ok(n.isError); assert.match(n.text, /confirm=true/);
});

t('perf_set dengan pengaman visual: setting aman dipertahankan', async () => {
  const url = `${A.url}/?page_id=${HOME_A}`;
  const noop = await call('elementor_design', { site: 'test-a', op: 'perf_set', option: 'elementor_font_display', value: 'swap', check_urls: [url], confirm: true });
  assert.match(noop.text, /Tidak ada perubahan/, noop.text);
  // Element Caching (fitur performa Free) — harus identik secara visual
  const r = await call('elementor_design', { site: 'test-a', op: 'perf_set', option: 'elementor_element_cache_ttl', value: '24', check_urls: [url], confirm: true });
  console.log(r.text);
  assert.ok(!r.isError || /DIKEMBALIKAN otomatis/.test(r.text), r.text);
  assert.match(r.text, /Tampilan identik|DIKEMBALIKAN otomatis/);
});

t('perf_check (Lighthouse lokal) memberi skor ringkas', async () => {
  const r = await call('perf_check', { site: 'test-a', url: `${A.url}/?page_id=${HOME_A}`, strategy: 'mobile' });
  assert.ok(!r.isError, r.text); assert.match(r.text, /mobile \(lokal\): \d+\/100/);
  console.log(r.text);
});
