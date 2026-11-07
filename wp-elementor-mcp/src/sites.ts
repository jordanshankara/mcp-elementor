// Registry situs: satu file config untuk 7, 9, 20+ situs. Situs dipilih lewat alias; tidak ada default & tidak ada tebakan.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export interface Site {
  alias: string;
  url: string;          // https://domain.com (tanpa slash akhir)
  user: string;
  app_password: string;
  label?: string;
  env: 'prod' | 'staging' | 'local';
  readonly: boolean;
  tags: string[];
  notes?: string;       // path catatan per situs (config/sites/<alias>.md)
}
export interface Config { sites: Record<string, Site>; pagespeed_api_key?: string; file: string }

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..'); // E:\1. Code
export const PKG = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export function configPath(): string {
  return process.env.WPE_SITES ? path.resolve(process.env.WPE_SITES) : path.join(ROOT, 'config', 'sites.local.json');
}

let cache: { mtime: number; cfg: Config } | null = null;

export function loadConfig(): Config {
  const file = configPath();
  if (!existsSync(file)) throw new Error(`File config belum ada: ${file}. Salin config/sites.example.json menjadi sites.local.json lalu isi.`);
  const { mtimeMs } = require_stat(file);
  if (cache && cache.mtime === mtimeMs) return cache.cfg;
  const raw = JSON.parse(readFileSync(file, 'utf8'));
  const sites: Record<string, Site> = {};
  for (const [alias, s] of Object.entries<any>(raw.sites ?? {})) {
    if (!/^[a-z0-9][a-z0-9-]{0,30}$/.test(alias)) throw new Error(`Alias "${alias}" tidak valid (pakai huruf kecil, angka, strip).`);
    if (!s.url || !s.user || !s.app_password) throw new Error(`Situs "${alias}" wajib punya url, user, app_password.`);
    const env = (s.env ?? 'prod') as Site['env'];
    if (!['prod', 'staging', 'local'].includes(env)) throw new Error(`env situs "${alias}" harus prod|staging|local.`);
    sites[alias] = {
      alias,
      url: String(s.url).replace(/\/+$/, ''),
      user: String(s.user),
      app_password: String(s.app_password).replace(/\s+/g, ''),
      label: s.label,
      env,
      readonly: s.readonly !== false, // default: readonly sampai diaktifkan
      tags: Array.isArray(s.tags) ? s.tags.map(String) : [],
      notes: existsSync(path.join(ROOT, 'config', 'sites', `${alias}.md`)) ? path.join(ROOT, 'config', 'sites', `${alias}.md`) : undefined,
    };
  }
  const cfg: Config = { sites, pagespeed_api_key: raw.pagespeed_api_key || process.env.PAGESPEED_API_KEY, file };
  cache = { mtime: mtimeMs, cfg };
  return cfg;
}

import { statSync } from 'node:fs';
function require_stat(f: string) { return statSync(f); }

export function domainOf(site: Site): string {
  return new URL(site.url).host.replace(/^www\./, '');
}

export function header(site: Site): string {
  return `[${site.alias} · ${domainOf(site)} · ${site.env.toUpperCase()}${site.readonly ? ' · READONLY' : ''}]`;
}

/** Ambil situs berdasar alias PERSIS. Salah ketik => error berisi daftar alias valid. */
export function getSite(alias: string): Site {
  const { sites } = loadConfig();
  const s = sites[alias];
  if (!s) {
    const list = Object.values(sites).map((x) => `${x.alias} (${domainOf(x)})`).join(', ') || '(belum ada situs)';
    throw new Error(`Situs "${alias}" tidak dikenal. Alias valid: ${list}. Jangan menebak — tanyakan ke user bila ragu.`);
  }
  return s;
}

export function sitesByTag(tag: string): Site[] {
  return Object.values(loadConfig().sites).filter((s) => s.tags.includes(tag));
}

/** Guard penulisan: readonly, dan untuk prod wajib confirm_domain yang cocok. */
export function assertWritable(site: Site, confirmDomain?: string): void {
  if (site.readonly) throw new Error(`${header(site)} Situs ini READONLY. Ubah "readonly": false di config hanya bila user mengizinkan.`);
  if (site.env === 'prod') {
    const want = domainOf(site);
    const got = (confirmDomain ?? '').replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '').toLowerCase();
    if (got !== want) throw new Error(`${header(site)} Situs PROD: wajib isi confirm_domain="${want}" (diterima: "${confirmDomain ?? ''}"). Ini kunci ganda anti salah situs.`);
  }
}
