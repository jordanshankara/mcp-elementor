// Upload gambar dengan guardrail performa: resize sesuai slot, WebP, buang EXIF, budget ukuran, alt wajib.
import sharp from 'sharp';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import type { Site } from './sites.ts';
import { ROOT } from './sites.ts';
import { wp } from './wp.ts';

export const SLOTS = {
  hero: { maxW: 1920, budget: 200 * 1024, minW: 1280 },
  content: { maxW: 1200, budget: 120 * 1024, minW: 800 },
  card: { maxW: 800, budget: 120 * 1024, minW: 480 },
  icon: { maxW: 400, budget: 50 * 1024, minW: 200 },
} as const;
export type Slot = keyof typeof SLOTS;

const kb = (n: number) => `${Math.round(n / 1024)} KB`;
const mb = (n: number) => (n > 1024 * 1024 ? `${(n / 1024 / 1024).toFixed(1)} MB` : kb(n));

export async function loadSource(source: string): Promise<{ buf: Buffer; name: string }> {
  if (/^https?:\/\//i.test(source)) {
    const r = await fetch(source);
    if (!r.ok) throw new Error(`Gagal mengunduh gambar (${r.status}) dari ${source}`);
    const buf = Buffer.from(await r.arrayBuffer());
    if (buf.length > 40 * 1024 * 1024) throw new Error('Gambar > 40 MB, terlalu besar.');
    return { buf, name: path.basename(new URL(source).pathname) || 'image' };
  }
  const p = path.isAbsolute(source) ? source : path.join(ROOT, source);
  return { buf: await readFile(p), name: path.basename(p) };
}

export interface Optimized { buf: Buffer; mime: string; ext: string; width: number; height: number; report: string; overBudget: boolean }

export async function optimize(input: Buffer, name: string, slot: Slot, keepFormat = false): Promise<Optimized> {
  const meta = await sharp(input, { animated: true }).metadata();
  if (meta.format === 'svg') throw new Error('SVG tidak dioptimasi/diupload (WordPress memblokir SVG secara default dan berisiko keamanan). Pakai PNG/WebP.');
  const cfg = SLOTS[slot];
  const srcW = meta.width ?? cfg.maxW;
  const animated = (meta.pages ?? 1) > 1;
  let width = Math.min(srcW, cfg.maxW);
  const fmt = keepFormat ? (meta.format === 'png' ? 'png' : meta.format === 'gif' ? 'gif' : 'jpeg') : 'webp';

  const encode = async (w: number, q: number) => {
    let img = sharp(input, { animated }).rotate().resize({ width: w, withoutEnlargement: true }); // rotate() = ikuti EXIF lalu buang
    if (fmt === 'webp') img = img.webp({ quality: q, effort: 5, smartSubsample: true, alphaQuality: 90 });
    else if (fmt === 'png') img = img.png({ compressionLevel: 9, palette: q < 80, quality: q });
    else if (fmt === 'gif') img = img.gif();
    else img = img.jpeg({ quality: q, mozjpeg: true, progressive: true });
    const { data, info } = await img.toBuffer({ resolveWithObject: true });
    return { data, info };
  };

  let q = 80;
  let r = await encode(width, q);
  while (r.data.length > cfg.budget && q > 65) { q -= 5; r = await encode(width, q); }
  while (r.data.length > cfg.budget && width > cfg.minW) { width = Math.max(cfg.minW, Math.round(width * 0.85)); r = await encode(width, q); }
  const over = r.data.length > cfg.budget;
  const ext = fmt === 'jpeg' ? 'jpg' : fmt;
  const height = animated ? (r.info.pageHeight ?? r.info.height) : r.info.height;
  const report = `${name} ${mb(input.length)} ${srcW}px ${meta.format} → ${r.info.width}px ${fmt.toUpperCase()} q${q} ${kb(r.data.length)}` +
    (over ? ` ⚠ masih di atas budget ${kb(cfg.budget)} untuk slot ${slot} — beri tahu user (gambar sangat detail).` : ` ✓ (budget ${slot} ${kb(cfg.budget)})`);
  return { buf: r.data, mime: `image/${fmt}`, ext, width: r.info.width, height, report, overBudget: over };
}

function slugify(s: string): string {
  return s.toLowerCase().normalize('NFKD').replace(/[^\w\s-]/g, '').trim().replace(/[\s_]+/g, '-').slice(0, 60) || 'gambar';
}

export async function uploadOptimized(site: Site, x: { source: string; alt: string; slot: Slot; title?: string; keep_format: boolean }) {
  const { buf, name } = await loadSource(x.source);
  const o = await optimize(buf, name, x.slot, x.keep_format);
  const file = `${slugify(x.title ?? x.alt)}.${o.ext}`;
  const m = await wp(site, 'POST', '/wp/v2/media', {
    bodyRaw: o.buf,
    headers: { 'Content-Type': o.mime, 'Content-Disposition': `attachment; filename="${file}"` },
    timeoutMs: 120000,
  });
  await wp(site, 'POST', `/wp/v2/media/${m.id}`, { body: { alt_text: x.alt, title: x.title ?? x.alt } });
  return { id: m.id as number, url: m.source_url as string, width: o.width, height: o.height, report: o.report, suggestedSize: 'full' };
}
