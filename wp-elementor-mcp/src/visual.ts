// Regresi visual headless (tanpa Claude in Chrome): screenshot mobile+desktop, pixel diff, error JS, request gagal.
// Yang dikembalikan ke Claude hanya angka; file PNG disimpan di reports/.
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';
import type { Site } from './sites.ts';
import { ROOT } from './sites.ts';

const VIEWPORTS = [{ name: 'mobile', width: 390, height: 844 }, { name: 'desktop', width: 1440, height: 900 }];
const MAX_H = 8000;

function dirFor(site: Site, url: string) {
  const slug = (new URL(url).pathname.replace(/\/+$/, '').replace(/[^\w-]+/g, '_') || 'home').slice(0, 60);
  const d = path.join(ROOT, 'reports', site.alias, slug);
  mkdirSync(d, { recursive: true });
  return d;
}

interface Capture { errors: string[]; failed: string[] }

async function capture(url: string, outPrefix: string): Promise<Capture> {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch();
  const errors = new Set<string>();
  const failed = new Set<string>();
  try {
    for (const vp of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
      const page = await ctx.newPage();
      page.on('console', (m) => { if (m.type() === 'error') errors.add(m.text().slice(0, 200)); });
      page.on('pageerror', (e) => errors.add('JS: ' + e.message.slice(0, 200)));
      page.on('response', (r) => {
        const t = r.request().resourceType();
        if (r.status() >= 400 && ['stylesheet', 'script', 'font', 'image', 'document'].includes(t)) failed.add(`${r.status()} ${t} ${r.url().split('?')[0].slice(-120)}`);
      });
      page.on('requestfailed', (r) => { const t = r.resourceType(); if (['stylesheet', 'script', 'font'].includes(t)) failed.add(`FAIL ${t} ${r.url().split('?')[0].slice(-120)}`); });
      const u = new URL(url); u.searchParams.set('nocache', String(Date.now()));
      await page.goto(u.toString(), { waitUntil: 'networkidle', timeout: 90000 }).catch(async () => { await page.waitForLoadState('load').catch(() => {}); });
      await page.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}' }).catch(() => {});
      // muat gambar lazy dengan scroll, lalu kembali ke atas
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } window.scrollTo(0, 0); });
      await page.waitForTimeout(700);
      const h = Math.min(await page.evaluate(() => document.documentElement.scrollHeight), MAX_H);
      await page.screenshot({ path: `${outPrefix}-${vp.name}.png`, clip: { x: 0, y: 0, width: vp.width, height: h }, fullPage: true });
      await ctx.close();
    }
  } finally { await browser.close(); }
  return { errors: [...errors], failed: [...failed] };
}

export async function visualSnapshot(site: Site, url: string, label: string): Promise<string> {
  const d = dirFor(site, url);
  const c = await capture(url, path.join(d, label));
  writeFileSync(path.join(d, `${label}.json`), JSON.stringify(c));
  return `snapshot "${label}" disimpan (${VIEWPORTS.map((v) => v.name).join('+')}). error JS: ${c.errors.length}, request gagal: ${c.failed.length}${c.errors.length || c.failed.length ? '\n' + [...c.errors, ...c.failed].slice(0, 5).join('\n') : ''}`;
}

function diffPng(a: string, b: string, out: string): { pct: number; heightDelta: number } {
  const A = PNG.sync.read(readFileSync(a));
  const B = PNG.sync.read(readFileSync(b));
  const w = Math.min(A.width, B.width);
  const h = Math.min(A.height, B.height);
  const crop = (img: PNG) => {
    if (img.width === w && img.height === h) return img.data;
    const buf = Buffer.alloc(w * h * 4);
    for (let y = 0; y < h; y++) img.data.copy(buf, y * w * 4, y * img.width * 4, y * img.width * 4 + w * 4);
    return buf;
  };
  const D = new PNG({ width: w, height: h });
  const n = pixelmatch(crop(A), crop(B), D.data, w, h, { threshold: 0.1 });
  writeFileSync(out, PNG.sync.write(D));
  return { pct: (n / (w * h)) * 100, heightDelta: B.height - A.height };
}

/** Compare dengan 1x ambil ulang bila berbeda (menyaring gangguan sesaat: server lambat, request timeout, font telat). */
export async function visualCompare(site: Site, url: string, label: string, tolerancePct = 0.1) {
  const first = await compareOnce(site, url, label, tolerancePct);
  if (first.same) return first;
  const second = await compareOnce(site, url, label, tolerancePct);
  return second.same ? { ...second, summary: second.summary + ' (diambil ulang 1x)' } : second;
}

async function compareOnce(site: Site, url: string, label: string, tolerancePct: number) {
  const d = dirFor(site, url);
  const baseMeta = path.join(d, `${label}.json`);
  if (!existsSync(baseMeta)) throw new Error(`Belum ada snapshot "${label}" untuk ${url}. Jalankan op=snapshot dulu.`);
  const base: Capture = JSON.parse(readFileSync(baseMeta, 'utf8'));
  const after = await capture(url, path.join(d, `${label}-after`));
  const parts: string[] = [];
  let same = true;
  const files: string[] = [];
  for (const vp of VIEWPORTS) {
    const r = diffPng(path.join(d, `${label}-${vp.name}.png`), path.join(d, `${label}-after-${vp.name}.png`), path.join(d, `${label}-diff-${vp.name}.png`));
    parts.push(`${vp.name}: beda ${r.pct.toFixed(3)}%${r.heightDelta ? `, tinggi ${r.heightDelta > 0 ? '+' : ''}${r.heightDelta}px` : ''}`);
    if (r.pct > tolerancePct || Math.abs(r.heightDelta) > 2) same = false;
    files.push(path.relative(ROOT, path.join(d, `${label}-diff-${vp.name}.png`)));
  }
  const newErr = after.errors.filter((e) => !base.errors.includes(e));
  const newFail = after.failed.filter((e) => !base.failed.includes(e));
  if (newErr.length || newFail.length) same = false;
  const summary = `${same ? '✓ SAMA' : '✗ BERBEDA'} · ${parts.join(' · ')} · error JS baru: ${newErr.length} · request gagal baru: ${newFail.length}` +
    (newErr.length || newFail.length ? '\n' + [...newErr, ...newFail].slice(0, 5).join('\n') : '');
  return { same, summary, files: 'diff: ' + files.join(', ') };
}
