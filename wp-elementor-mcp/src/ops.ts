// Lapisan operasi: baca/tulis halaman Elementor dengan semua guardrail.
// Alur tulis: guard situs → cek rev (baca-sebelum-tulis) → lint performa → validasi widget Free/Pro
//            → backup lokal → POST (bridge membuat backup + revisi + purge cache) → verifikasi (data tersimpan persis
//            + teks baru muncul di render) → jika gagal: restore otomatis.
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync, readdirSync, rmSync } from 'node:fs';
import path from 'node:path';
import type { Site } from './sites.ts';
import { assertWritable, header, ROOT } from './sites.ts';
import { wp } from './wp.ts';
import * as E from './elementor.ts';

export interface Page {
  id: number; type: string; status: string; title: string; link: string; edit_mode: string;
  template_type: string; page_settings: unknown; hash: string; raw: string; data: E.El[]; rev: string;
}

export function revOf(site: Site, id: number, hash: string): string {
  return createHash('sha256').update(`${site.alias}|${new URL(site.url).host}|${id}|${hash}`).digest('hex').slice(0, 12);
}

export async function readPage(site: Site, id: number): Promise<Page> {
  const r = await wp(site, 'GET', `/claude/v1/elementor/${id}`);
  let data: E.El[] = [];
  if (r.data) {
    try { data = JSON.parse(r.data); } catch { throw new Error(`${header(site)} _elementor_data halaman ${id} bukan JSON valid.`); }
  }
  if (!Array.isArray(data)) data = [];
  return { ...r, raw: r.data, data, rev: revOf(site, id, r.hash) };
}

const widgetCache = new Map<string, { at: number; widgets: Set<string>; elements: Set<string>; promo: Set<string>; pro: boolean }>();
export async function siteWidgets(site: Site) {
  const c = widgetCache.get(site.alias);
  if (c && Date.now() - c.at < 10 * 60_000) return c;
  const r = await wp(site, 'GET', '/claude/v1/widgets');
  const v = { at: Date.now(), widgets: new Set<string>(r.widgets), elements: new Set<string>(r.elements), promo: new Set<string>(r.promo ?? []), pro: !!r.pro };
  widgetCache.set(site.alias, v);
  return v;
}

/** Tolak widget/element yang tidak terdaftar di situs (mis. widget Pro di situs Free). */
export async function assertWidgetsAvailable(site: Site, els: E.El[]): Promise<void> {
  const w = await siteWidgets(site);
  const missingW = [...E.widgetTypes(els)].filter((t) => !w.widgets.has(t));
  const missingE = [...E.elTypes(els)].filter((t) => !w.elements.has(t));
  if (missingW.length || missingE.length) {
    const tips = missingW.map((t) => `- ${t}: ${E.proAlternative(t)}`).join('\n');
    const promo = missingW.filter((t) => w.promo.has(t));
    throw new Error(`${header(site)} Tidak tersedia di situs ini${w.pro ? '' : ' (Elementor Free)'}: ${[...missingW, ...missingE].join(', ')}.${promo.length ? ` (${promo.join(', ')} hanya placeholder promosi Pro — render kosong di Free.)` : ''}\n${tips}`);
  }
}

function localBackup(site: Site, id: number, raw: string, reason: string): string {
  const dir = path.join(ROOT, 'backups', site.alias, String(id));
  mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `${new Date().toISOString().replace(/[:.]/g, '-')}.json`);
  writeFileSync(file, JSON.stringify({ site: site.alias, url: site.url, id, reason, raw }));
  const files = readdirSync(dir).sort();
  for (const f of files.slice(0, Math.max(0, files.length - 30))) rmSync(path.join(dir, f));
  return path.relative(ROOT, file);
}

export interface WriteOpts {
  rev: string;
  confirmDomain?: string;
  reason: string;
  dryRun?: boolean;
  verifyTexts?: string[];
  checkWidgetsOf?: E.El[];      // subtree baru yang perlu divalidasi Free/Pro
  allowWarnings?: boolean;
}
export interface WriteResult { ok: boolean; lines: string[]; rev?: string; hash?: string }

export async function writePage(site: Site, id: number, mutate: (data: E.El[]) => E.El[], o: WriteOpts): Promise<WriteResult> {
  assertWritable(site, o.confirmDomain);
  const page = await readPage(site, id);
  if (page.rev !== o.rev) {
    throw new Error(`${header(site)} rev tidak cocok untuk halaman ${id}. Rev harus berasal dari elementor_outline/elementor_get halaman INI di situs INI, dan halaman belum berubah sejak dibaca. Baca ulang lalu ulangi.`);
  }
  const next = mutate(page.data);
  const lints = E.perfLint(next);
  const before = new Set(E.perfLint(page.data).map((l) => l.msg));
  const fresh = lints.filter((l) => !before.has(l.msg));
  const blocks = fresh.filter((l) => l.level === 'block');
  if (blocks.length) throw new Error(`${header(site)} Ditolak guardrail:\n` + blocks.map((b) => '- ' + b.msg).join('\n'));
  if (o.checkWidgetsOf?.length) await assertWidgetsAvailable(site, o.checkWidgetsOf);

  const json = JSON.stringify(next);
  const lines: string[] = [header(site) + ` halaman ${id} "${page.title}"`];
  if (o.dryRun) {
    lines.push(`DRY RUN — tidak ada yang ditulis. Elemen: ${E.countElements(page.data)} → ${E.countElements(next)}.`);
    fresh.forEach((l) => lines.push(`⚠ ${l.msg}`));
    return { ok: true, lines, rev: page.rev };
  }
  const local = localBackup(site, id, page.raw, o.reason);
  const res = await wp(site, 'POST', `/claude/v1/elementor/${id}`, { body: { data: json, hash: page.hash, reason: o.reason } });

  // ---- verifikasi: jangan percaya "success" ----
  const problems: string[] = [];
  const after = await readPage(site, id);
  if (after.raw !== json) problems.push('data yang tersimpan berbeda dengan yang dikirim');
  if (o.verifyTexts?.length) {
    const r = await wp(site, 'GET', `/claude/v1/elementor/${id}/render`);
    const html = E.normalizeText(r.html ?? '').toLowerCase();
    for (const t of o.verifyTexts) {
      const needle = t.toLowerCase().slice(0, 60);
      if (!html.includes(needle)) problems.push(`teks "${t.slice(0, 40)}" tidak muncul di hasil render`);
    }
  }
  if (problems.length) {
    // restore otomatis
    try {
      await wp(site, 'POST', `/claude/v1/elementor/${id}/backups`, { body: { key: res.backup, hash: after.hash } });
      lines.push(`✗ GAGAL VERIFIKASI → sudah di-restore otomatis ke versi sebelumnya.`);
    } catch (e: any) {
      lines.push(`✗ GAGAL VERIFIKASI dan restore otomatis gagal (${e.message}). Backup lokal: ${local}`);
    }
    problems.forEach((p) => lines.push('  - ' + p));
    return { ok: false, lines };
  }
  lines.push(`✓ tersimpan & terverifikasi${o.verifyTexts?.length ? ` (${o.verifyTexts.length} teks muncul di render)` : ''}. backup: ${res.backup}`);
  fresh.forEach((l) => lines.push(`⚠ ${l.msg}`));
  lines.push(`rev baru: ${after.rev}`);
  return { ok: true, lines, rev: after.rev, hash: after.hash };
}

export async function restore(site: Site, id: number, key: string, rev: string, confirmDomain?: string): Promise<WriteResult> {
  assertWritable(site, confirmDomain);
  const page = await readPage(site, id);
  if (page.rev !== rev) throw new Error(`${header(site)} rev tidak cocok. Baca ulang halaman ${id} dulu.`);
  localBackup(site, id, page.raw, 'before-restore');
  const res = await wp(site, 'POST', `/claude/v1/elementor/${id}/backups`, { body: { key, hash: page.hash } });
  const after = await readPage(site, id);
  return { ok: true, lines: [header(site) + ` halaman ${id} di-restore dari ${key}. hash ${after.hash.slice(0, 8)} (backup sebelum restore: ${res.backup})`, `rev baru: ${after.rev}`], rev: after.rev, hash: after.hash };
}
