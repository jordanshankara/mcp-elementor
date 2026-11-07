#!/usr/bin/env node
// wp-elementor-mcp: satu MCP server untuk banyak situs WordPress + Elementor (Free/Pro).
// Semua tool wajib `site` (alias persis dari config). Output sengaja ringkas supaya hemat token.
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { loadConfig, getSite, header, domainOf, assertWritable, sitesByTag } from './sites.ts';
import { wp, fetchPublic } from './wp.ts';
import * as E from './elementor.ts';
import { readPage, writePage, restore, siteWidgets } from './ops.ts';
import { uploadOptimized } from './media.ts';
import { perfCheck } from './perf.ts';
import { visualSnapshot, visualCompare } from './visual.ts';

const MAX = 6000;
function out(...parts: (string | string[] | undefined)[]) {
  let t = parts.flat().filter((x) => x !== undefined && x !== '').join('\n');
  if (t.length > MAX) t = t.slice(0, MAX) + `\n…[dipotong ${t.length - MAX} karakter — persempit query/_fields/max_depth]`;
  return { content: [{ type: 'text' as const, text: t }] };
}
function fail(e: unknown) {
  return { isError: true, content: [{ type: 'text' as const, text: (e as Error)?.message ?? String(e) }] };
}
const safe = <A>(fn: (a: A) => Promise<ReturnType<typeof out>>) => async (a: A) => { try { return await fn(a); } catch (e) { return fail(e); } };
const compact = (v: unknown) => JSON.stringify(v);

const server = new McpServer({ name: 'wp-elementor', version: '1.0.0' }, {
  instructions: 'Kelola banyak situs WordPress+Elementor. Selalu sebut `site` (alias persis dari sites_list); jangan menebak situs. Alur edit: elementor_outline → elementor_get (hanya elemen yang perlu) → elementor_update (batch, pakai rev). Verifikasi sudah otomatis. Detail: skill wp-elementor.',
});

const site = z.string().describe('Alias situs persis dari sites_list (mis. "toko"). Wajib; jangan menebak.');
const pageId = z.number().int().positive();
const confirmDomain = z.string().optional().describe('Wajib untuk situs PROD: domain situs persis, mis. "tokoabc.com".');
const rev = z.string().describe('rev dari elementor_outline/elementor_get halaman ini (bukti baca-sebelum-tulis).');

// ---------------- situs ----------------
server.registerTool('sites_list', {
  description: 'Daftar situs terdaftar (alias, domain, env, readonly, tags). Opsional filter tag.',
  inputSchema: { tag: z.string().optional() },
}, safe(async ({ tag }) => {
  const list = tag ? sitesByTag(tag) : Object.values(loadConfig().sites);
  return out(list.map((s) => `${s.alias} · ${domainOf(s)} · ${s.env.toUpperCase()} · ${s.readonly ? 'readonly' : 'write'}${s.tags.length ? ' · #' + s.tags.join(' #') : ''}${s.label ? ' · ' + s.label : ''}${s.notes ? ' · ada catatan' : ''}`), list.length ? '' : '(tidak ada situs)');
}));

server.registerTool('site_health', {
  description: 'Cek koneksi & status situs: versi WP/Elementor/Pro, bridge, auth, cache plugin, fitur performa, jumlah widget.',
  inputSchema: { site },
}, safe(async ({ site: a }) => {
  const s = getSite(a);
  const info = await wp(s, 'GET', '/claude/v1/info');
  const w = await siteWidgets(s);
  const pf = info.perf_features ?? {};
  return out(
    header(s),
    `WP ${info.wp} · PHP ${info.php} · tema ${info.theme} · env-wp ${info.env}`,
    `Elementor ${info.elementor ?? 'TIDAK AKTIF'} · ${info.elementor_pro ? 'Pro ' + info.elementor_pro : 'Free'} · bridge ${info.bridge}`,
    `Login: ${info.user.login} (${info.user.roles.join(',')}) · manage_options=${info.user.can_manage_options}`,
    `Widget tersedia: ${w.widgets.size}${w.promo.size ? ` (+${w.promo.size} placeholder Pro yang TIDAK boleh dipakai)` : ''} · elemen layout: ${[...w.elements].filter((e) => ['section', 'column', 'container', 'e-flexbox', 'e-div-block'].includes(e)).join(',')}`,
    `Cache plugin: ${info.cache_plugins.join(', ') || '-'} · multibahasa: ${info.multilingual ?? '-'} · kit ${info.kit_id}`,
    `Performa: ${Object.entries(pf).map(([k, v]) => `${k}=${v}`).join(' ')}`,
    s.notes ? `Catatan situs: ${s.notes}` : '',
  );
}));

server.registerTool('content_list', {
  description: 'Daftar konten ringkas (id · status · judul · slug). type: pages|posts|media|elementor_library atau rest_base lain.',
  inputSchema: { site, type: z.string().default('pages'), search: z.string().optional(), status: z.string().default('any'), per_page: z.number().int().max(100).default(30), page: z.number().int().default(1) },
}, safe(async ({ site: a, type, search, status, per_page, page }) => {
  const s = getSite(a);
  const r = await wp(s, 'GET', `/wp/v2/${type}`, { query: { context: 'edit', search, status: type === 'media' ? undefined : status, per_page, page, _fields: 'id,status,title,slug,lang,template,modified' } });
  return out(header(s), (r as any[]).map((p) => `${p.id} · ${p.status ?? ''} · ${p.title?.raw ?? p.title?.rendered ?? ''} · /${p.slug}${p.lang ? ' · ' + p.lang : ''}`), (r as any[]).length === per_page ? `(mungkin ada lebih; page=${page + 1})` : '');
}));

// ---------------- elementor read ----------------
server.registerTool('elementor_outline', {
  description: 'Struktur halaman Elementor sebagai pohon ringkas: "id tipe \\"cuplikan\\"". Mengembalikan rev untuk menulis. Pakai ini dulu, jangan minta JSON penuh.',
  inputSchema: { site, page_id: pageId, max_depth: z.number().int().min(0).optional(), root_id: z.string().optional() },
}, safe(async ({ site: a, page_id, max_depth, root_id }) => {
  const s = getSite(a);
  const p = await readPage(s, page_id);
  const warn = p.edit_mode !== 'builder' ? '⚠ Halaman ini belum dibangun dengan Elementor (edit_mode bukan builder).' : '';
  return out(`${header(s)} #${p.id} "${p.title}" · ${p.status} · ${p.link}`, `elemen: ${E.countElements(p.data)} · rev: ${p.rev}`, warn, E.outline(p.data, { maxDepth: max_depth, rootId: root_id }));
}));

server.registerTool('elementor_get', {
  description: 'Setting lengkap (tanpa nilai kosong) dari elemen tertentu saja. Pakai untuk tahu nama key sebelum update.',
  inputSchema: { site, page_id: pageId, element_ids: z.array(z.string()).min(1).max(10) },
}, safe(async ({ site: a, page_id, element_ids }) => {
  const s = getSite(a);
  const p = await readPage(s, page_id);
  return out(`${header(s)} #${page_id} rev: ${p.rev}`, element_ids.map((id) => compact(E.getElement(p.data, id))));
}));

server.registerTool('elementor_find', {
  description: 'Cari teks di satu halaman (page_id) atau di banyak halaman/post (tanpa page_id, maks 60 terbaru). Hasil: halaman, id elemen, key, cuplikan.',
  inputSchema: { site, query: z.string().min(2), page_id: pageId.optional(), types: z.array(z.string()).default(['pages', 'posts']) },
}, safe(async ({ site: a, query, page_id, types }) => {
  const s = getSite(a);
  const ids: { id: number; title: string }[] = [];
  if (page_id) ids.push({ id: page_id, title: '' });
  else for (const t of types) {
    const r = await wp(s, 'GET', `/wp/v2/${t}`, { query: { context: 'edit', status: 'any', per_page: 30, orderby: 'modified', _fields: 'id,title' } });
    for (const p of r as any[]) ids.push({ id: p.id, title: p.title?.raw ?? '' });
  }
  const lines: string[] = [header(s)];
  let pagesHit = 0;
  for (const { id, title } of ids.slice(0, 60)) {
    let p; try { p = await readPage(s, id); } catch { continue; }
    if (!p.data.length) continue;
    const m = E.findText(p.data, query, 10);
    if (m.length) { pagesHit++; lines.push(`#${id} "${title || p.title}" rev:${p.rev}`); m.forEach((x) => lines.push(`  ${x.id} ${x.type} ${x.key}: …${x.snippet}…`)); }
  }
  if (!pagesHit) lines.push(`Tidak ditemukan "${query}" di ${Math.min(ids.length, 60)} halaman.`);
  return out(lines);
}));

// ---------------- elementor write ----------------
server.registerTool('elementor_update', {
  description: 'Ubah setting satu/banyak elemen (JSON merge-patch: object digabung, null menghapus key). Otomatis: backup, revisi, clear cache, verifikasi tersimpan + teks muncul di render, restore bila gagal. V4: kirim {"$$type":..,"value":..} utuh.',
  inputSchema: {
    site, page_id: pageId, rev, confirm_domain: confirmDomain,
    changes: z.array(z.object({ id: z.string(), settings: z.record(z.string(), z.any()) })).min(1).max(50),
    reason: z.string().default('edit via claude'), dry_run: z.boolean().default(false),
  },
}, safe(async ({ site: a, page_id, rev: r, confirm_domain, changes, reason, dry_run }) => {
  const s = getSite(a);
  const res = await writePage(s, page_id, (d) => E.applyPatches(d, changes), { rev: r, confirmDomain: confirm_domain, reason, dryRun: dry_run, verifyTexts: E.patchTexts(changes) });
  return res.ok ? out(res.lines) : fail(res.lines.join('\n'));
}));

const elementSchema: z.ZodType<any> = z.lazy(() => z.object({
  elType: z.string(), widgetType: z.string().optional(), isInner: z.boolean().optional(),
  settings: z.record(z.string(), z.any()).optional(), elements: z.array(elementSchema).optional(),
}).passthrough());

server.registerTool('elementor_structure', {
  description: 'Ubah struktur: insert (elemen baru/hasil copy), duplicate, move, remove (wajib confirm). copy_from mengambil elemen dari halaman lain di situs yang SAMA. Widget yang tidak ada di situs (mis. Pro di Free) ditolak.',
  inputSchema: {
    site, page_id: pageId, rev, confirm_domain: confirmDomain,
    op: z.enum(['insert', 'duplicate', 'move', 'remove']),
    element_id: z.string().optional().describe('Target untuk duplicate/move/remove'),
    parent_id: z.string().nullable().optional().describe('Container/column tujuan (null = level atas)'),
    index: z.number().int().min(0).optional(),
    element: elementSchema.optional().describe('Untuk insert: elemen baru {elType, widgetType, settings, elements}; id dibuat otomatis'),
    copy_from: z.object({ page_id: pageId, element_id: z.string() }).optional(),
    confirm: z.boolean().default(false), dry_run: z.boolean().default(false), reason: z.string().default('struktur via claude'),
  },
}, safe(async (x) => {
  const s = getSite(x.site);
  let newId = '';
  let check: E.El[] | undefined;
  let source: E.El | undefined;
  if (x.op === 'insert') {
    if (x.copy_from) {
      const src = await readPage(s, x.copy_from.page_id);
      source = E.locate(src.data, x.copy_from.element_id).el;
    } else if (x.element) source = { id: 'new', ...x.element } as E.El;
    else throw new Error('insert butuh `element` atau `copy_from`.');
    check = [source];
  } else if (!x.element_id) throw new Error(`${x.op} butuh element_id.`);
  if (x.op === 'remove' && !x.confirm) throw new Error('Remove adalah operasi destruktif: tanyakan user dulu, lalu ulangi dengan confirm=true.');
  const res = await writePage(s, x.page_id, (d) => {
    switch (x.op) {
      case 'insert': { const r = E.insert(d, x.parent_id ?? null, x.index, source!); newId = r.id; return r.data; }
      case 'duplicate': { const r = E.duplicate(d, x.element_id!); newId = r.id; return r.data; }
      case 'move': return E.move(d, x.element_id!, x.parent_id ?? null, x.index);
      case 'remove': return E.remove(d, x.element_id!);
    }
  }, { rev: x.rev, confirmDomain: x.confirm_domain, reason: x.reason, dryRun: x.dry_run, checkWidgetsOf: check, verifyTexts: source ? E.textsOf(source.settings).slice(0, 2) : undefined });
  return res.ok ? out(res.lines, newId ? `id elemen baru: ${newId}` : '') : fail(res.lines.join('\n'));
}));

server.registerTool('elementor_page', {
  description: 'Versi & draft: backups (daftar), restore (key+rev, wajib confirm), draft_copy (duplikat halaman jadi draft untuk edit besar), apply_draft (salin isi draft page_id ke target_id; wajib confirm + rev target).',
  inputSchema: {
    site, page_id: pageId, op: z.enum(['backups', 'restore', 'draft_copy', 'apply_draft']),
    key: z.string().optional(), rev: z.string().optional(), target_id: pageId.optional(),
    confirm_domain: confirmDomain, confirm: z.boolean().default(false),
  },
}, safe(async (x) => {
  const s = getSite(x.site);
  if (x.op === 'backups') {
    const r = await wp(s, 'GET', `/claude/v1/elementor/${x.page_id}/backups`);
    return out(header(s), (r as any[]).map((b) => `${b.key} · ${b.time} · ${b.bytes}B · ${b.reason}`), (r as any[]).length ? '' : '(belum ada backup)');
  }
  if (x.op === 'draft_copy') {
    assertWritable(s, x.confirm_domain);
    const r = await wp(s, 'POST', `/claude/v1/elementor/${x.page_id}/draft-copy`);
    return out(header(s), `Draft dibuat: #${r.id} · preview: ${r.preview}`, 'Edit draft ini, minta user cek preview, lalu apply_draft (page_id=draft, target_id=asli) setelah user setuju.');
  }
  if (!x.confirm) throw new Error(`${x.op} mengubah halaman tayang: tanyakan user dulu, lalu ulangi dengan confirm=true.`);
  if (!x.rev) throw new Error('rev wajib (dari elementor_outline halaman target).');
  if (x.op === 'restore') {
    if (!x.key) throw new Error('key backup wajib.');
    return out((await restore(s, x.page_id, x.key, x.rev, x.confirm_domain)).lines);
  }
  if (!x.target_id) throw new Error('target_id wajib untuk apply_draft.');
  const draft = await readPage(s, x.page_id);
  const res = await writePage(s, x.target_id, () => draft.data, { rev: x.rev, confirmDomain: x.confirm_domain, reason: `apply draft #${x.page_id}` });
  if (res.ok) await wp(s, 'DELETE', `/wp/v2/${draft.type === 'page' ? 'pages' : 'posts'}/${x.page_id}`).catch(() => {});
  return res.ok ? out(res.lines, `Draft #${x.page_id} dipindah ke trash.`) : fail(res.lines.join('\n'));
}));

server.registerTool('elementor_design', {
  description: 'Level situs: kit_get / kit_update (warna & tipografi global — berdampak ke SEMUA halaman, wajib confirm), perf_get / perf_set (fitur performa Elementor Free; otomatis visual check & rollback bila tampilan berubah/JS error).',
  inputSchema: {
    site, op: z.enum(['kit_get', 'kit_update', 'perf_get', 'perf_set']),
    keys: z.array(z.string()).optional().describe('kit_get: hanya key ini (hemat)'),
    settings: z.record(z.string(), z.any()).optional(), hash: z.string().optional(),
    name: z.string().optional(), state: z.enum(['active', 'inactive', 'default']).optional(),
    option: z.string().optional(), value: z.any().optional(),
    check_urls: z.array(z.string()).optional().describe('perf_set: halaman untuk visual check (default: beranda)'),
    confirm_domain: confirmDomain, confirm: z.boolean().default(false),
  },
}, safe(async (x) => {
  const s = getSite(x.site);
  if (x.op === 'kit_get') {
    const r = await wp(s, 'GET', '/claude/v1/kit');
    const st = x.keys?.length ? Object.fromEntries(x.keys.map((k) => [k, r.settings?.[k]])) : r.settings;
    return out(header(s), `kit #${r.kit_id} hash:${r.hash}`, compact(x.keys?.length ? st : E.prune(st)));
  }
  if (x.op === 'perf_get') return out(header(s), compact(await wp(s, 'GET', '/claude/v1/experiments')));
  assertWritable(s, x.confirm_domain);
  if (!x.confirm) throw new Error(`${x.op} berdampak ke seluruh situs: tanyakan user dulu, lalu ulangi dengan confirm=true.`);
  if (x.op === 'kit_update') {
    if (!x.settings || !x.hash) throw new Error('kit_update butuh settings + hash (dari kit_get).');
    const r = await wp(s, 'POST', '/claude/v1/kit', { body: { settings: x.settings, hash: x.hash } });
    await fetchPublic(s.url + '/').catch(() => {}); // warm-up CSS global
    return out(header(s), `✓ kit diperbarui. hash baru ${r.hash}. Sarankan visual_check di 3 halaman utama.`);
  }
  // perf_set dengan pengaman visual
  const cur = await wp(s, 'GET', '/claude/v1/experiments');
  const curVal = x.option ? cur?.[x.option.replace(/^elementor_/, '')] : cur?.[x.name ?? ''];
  if (curVal !== undefined && String(curVal) === String(x.option ? x.value : x.state)) {
    return out(header(s), `Tidak ada perubahan: ${x.option ?? x.name} sudah "${curVal}".`);
  }
  const urls = x.check_urls?.length ? x.check_urls : [s.url + '/'];
  const label = `perf-${Date.now()}`;
  for (const u of urls) await visualSnapshot(s, u, label);
  const body = x.option ? { option: x.option, value: x.value } : { name: x.name, state: x.state };
  const r = await wp(s, 'POST', '/claude/v1/experiments', { body });
  await wp(s, 'POST', '/claude/v1/purge').catch(() => {});
  // warm-up: Elementor membuat ulang file CSS saat halaman pertama kali dibuka setelah purge
  for (const u of urls) for (let i = 0; i < 2; i++) await fetchPublic(u).catch(() => {});
  const lines = [header(s), `diubah: ${x.option ?? x.name} → ${x.option ? compact(x.value) : x.state} (sebelumnya ${compact(r.previous)})`];
  let bad = false;
  for (const u of urls) {
    const c = await visualCompare(s, u, label);
    lines.push(`${u}: ${c.summary}`);
    if (!c.same) bad = true;
  }
  if (bad) {
    const back = x.option ? { option: x.option, value: r.previous } : { name: x.name, state: r.previous ?? 'default' };
    await wp(s, 'POST', '/claude/v1/experiments', { body: back });
    await wp(s, 'POST', '/claude/v1/purge').catch(() => {});
    lines.push('✗ Tampilan berubah / ada error baru → setting DIKEMBALIKAN otomatis.');
    return fail(lines.join('\n'));
  }
  lines.push('✓ Tampilan identik & tanpa error JS baru.');
  return out(lines);
}));

// ---------------- WordPress umum ----------------
const DESTRUCTIVE = /^\/wp\/v2\/(plugins|themes|users|settings)|\/wp\/v2\/[^/]+\/\d+.*$/;
server.registerTool('wp_request', {
  description: 'REST WordPress umum untuk admin dashboard (posts, pages, media, menus, menu-items, plugins, users, settings, taxonomies). GET bebas; tulis butuh situs writable; DELETE / plugins / themes / users / settings wajib confirm. Selalu isi fields untuk GET supaya hemat.',
  inputSchema: {
    site, method: z.enum(['GET', 'POST', 'PUT', 'PATCH', 'DELETE']), path: z.string().describe('mis. /wp/v2/posts atau /wp/v2/plugins/akismet/akismet'),
    query: z.record(z.string(), z.union([z.string(), z.number(), z.boolean()])).optional(), body: z.any().optional(),
    fields: z.string().optional().describe('daftar field dipisah koma → _fields'), confirm_domain: confirmDomain, confirm: z.boolean().default(false),
  },
}, safe(async (x) => {
  const s = getSite(x.site);
  if (x.path.startsWith('/claude/v1/elementor') && x.method !== 'GET') throw new Error('Tulis data Elementor hanya lewat elementor_update/elementor_structure (punya guardrail).');
  const write = x.method !== 'GET';
  if (write) {
    assertWritable(s, x.confirm_domain);
    const needsConfirm = x.method === 'DELETE' || /^\/wp\/v2\/(plugins|themes|users|settings)/.test(x.path) || (x.body && typeof x.body === 'object' && 'status' in x.body && ['trash', 'draft', 'private'].includes(String((x.body as any).status)));
    if (needsConfirm && !x.confirm) throw new Error('Operasi ini berisiko (hapus / plugin / tema / user / settings / unpublish). Tanyakan user dulu, lalu ulangi dengan confirm=true.');
  }
  void DESTRUCTIVE;
  const query = { ...(x.query ?? {}), ...(x.fields ? { _fields: x.fields } : {}), ...(x.method === 'GET' && !('context' in (x.query ?? {})) ? { context: 'edit' } : {}) };
  const r = await wp(s, x.method, x.path, { query, body: x.body });
  const hint = x.method === 'GET' && !x.fields ? '\n(tip: isi `fields` supaya output lebih kecil)' : '';
  return out(header(s) + ` ${x.method} ${x.path}`, compact(r) + hint);
}));

server.registerTool('media_upload', {
  description: 'Upload gambar (file lokal atau URL) dengan optimasi otomatis: resize sesuai slot, WebP, buang EXIF, budget ukuran (hero ≤200KB, lain ≤120KB), alt wajib. Balikan id+url+ukuran untuk dipasang di widget.',
  inputSchema: {
    site, source: z.string().describe('Path file lokal atau URL http(s)'), alt: z.string().min(3),
    slot: z.enum(['hero', 'content', 'card', 'icon']).default('content'), title: z.string().optional(),
    keep_format: z.boolean().default(false).describe('true = jangan konversi ke WebP (mis. SVG/logo khusus)'),
    confirm_domain: confirmDomain,
  },
}, safe(async (x) => {
  const s = getSite(x.site);
  assertWritable(s, x.confirm_domain);
  const r = await uploadOptimized(s, x);
  return out(header(s), r.report, `id: ${r.id} · url: ${r.url} · ${r.width}x${r.height}`, `Pasang di widget image: {"image":{"id":${r.id},"url":"${r.url}"},"image_size":"${r.suggestedSize}"}`);
}));

server.registerTool('perf_check', {
  description: 'Ukur performa halaman (PageSpeed Insights untuk URL publik; Lighthouse lokal untuk situs local). Output ringkas: skor mobile/desktop, LCP, CLS, TBT, 3 penyebab terbesar. Pakai hanya untuk perubahan besar.',
  inputSchema: { site, url: z.string().optional().describe('Default: beranda situs'), strategy: z.enum(['mobile', 'desktop', 'both']).default('both') },
}, safe(async (x) => {
  const s = getSite(x.site);
  return out(header(s), await perfCheck(s, x.url ?? s.url + '/', x.strategy, loadConfig().pagespeed_api_key));
}));

server.registerTool('visual_check', {
  description: 'Regresi visual tanpa Claude in Chrome (Playwright headless, mobile 390px + desktop 1440px): snapshot (simpan baseline) lalu compare (beda pixel %, error JS baru, request gagal). Mengembalikan angka saja; gambar di folder reports/.',
  inputSchema: { site, url: z.string(), op: z.enum(['snapshot', 'compare']), label: z.string().default('baseline') },
}, safe(async (x) => {
  const s = getSite(x.site);
  if (x.op === 'snapshot') return out(header(s), await visualSnapshot(s, x.url, x.label));
  const c = await visualCompare(s, x.url, x.label);
  return out(header(s), c.summary, c.files);
}));

await server.connect(new StdioServerTransport());
