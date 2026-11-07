// REST client per situs: Basic auth (Application Password), retry dengan jeda, antrian berurutan per situs,
// dan pesan error yang langsung menunjukkan penyebab umum (401/403/bridge belum terpasang/WAF).
import type { Site } from './sites.ts';
import { header } from './sites.ts';

export class WpError extends Error {
  status: number; code: string;
  constructor(msg: string, status: number, code = '') { super(msg); this.status = status; this.code = code; }
}

const queues = new Map<string, Promise<unknown>>();
function enqueue<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const prev = queues.get(key) ?? Promise.resolve();
  const next = prev.catch(() => {}).then(fn);
  queues.set(key, next);
  return next;
}

export interface ReqOpts { query?: Record<string, string | number | boolean | undefined>; body?: unknown; timeoutMs?: number; raw?: boolean; headers?: Record<string, string>; bodyRaw?: Buffer | Uint8Array }

export function restUrl(site: Site, path: string, query?: ReqOpts['query']): string {
  const p = path.startsWith('/') ? path : '/' + path;
  // pakai ?rest_route= supaya tetap jalan walau permalink "plain" / .htaccess bermasalah
  const u = new URL(site.url + '/');
  u.searchParams.set('rest_route', p.split('?')[0]);
  const inline = p.includes('?') ? new URLSearchParams(p.split('?')[1]) : null;
  inline?.forEach((v, k) => u.searchParams.set(k, v));
  for (const [k, v] of Object.entries(query ?? {})) if (v !== undefined) u.searchParams.set(k, String(v));
  return u.toString();
}

export function authHeader(site: Site): string {
  return 'Basic ' + Buffer.from(`${site.user}:${site.app_password}`).toString('base64');
}

export async function wp<T = any>(site: Site, method: string, path: string, opts: ReqOpts = {}): Promise<T> {
  return enqueue(site.alias, async () => {
    const url = restUrl(site, path, opts.query);
    let lastErr: unknown;
    for (let attempt = 0; attempt < 3; attempt++) {
      if (attempt) await new Promise((r) => setTimeout(r, 800 * attempt * attempt));
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 45000);
      try {
        const res = await fetch(url, {
          method,
          signal: ctrl.signal,
          headers: {
            Authorization: authHeader(site),
            Accept: 'application/json',
            'User-Agent': 'wp-elementor-mcp/1.0',
            ...(opts.body !== undefined ? { 'Content-Type': 'application/json' } : {}),
            ...opts.headers,
          },
          body: opts.bodyRaw ? new Uint8Array(opts.bodyRaw) : (opts.body !== undefined ? JSON.stringify(opts.body) : undefined),
        });
        const text = await res.text();
        if ((res.status === 429 || res.status >= 502) && attempt < 2) { lastErr = new WpError(`HTTP ${res.status}`, res.status); continue; }
        let json: any;
        try { json = text ? JSON.parse(text) : null; } catch {
          throw new WpError(`${header(site)} Balasan bukan JSON (HTTP ${res.status}). Kemungkinan diblokir firewall/security plugin (Wordfence, Cloudflare, ModSecurity) atau REST API dimatikan. Awal balasan: ${text.slice(0, 160).replace(/\s+/g, ' ')}`, res.status, 'not_json');
        }
        if (!res.ok) throw explain(site, res.status, json, path);
        return (opts.raw ? { status: res.status, headers: Object.fromEntries(res.headers), json } : json) as T;
      } catch (e: any) {
        if (e instanceof WpError) throw e;
        lastErr = e;
        if (attempt === 2) break;
      } finally { clearTimeout(t); }
    }
    const m = (lastErr as Error)?.name === 'AbortError' ? 'timeout' : (lastErr as Error)?.message;
    throw new WpError(`${header(site)} Gagal menghubungi ${site.url}: ${m}`, 0, 'network');
  });
}

function explain(site: Site, status: number, json: any, path: string): WpError {
  const code = json?.code ?? '';
  const msg = json?.message ?? '';
  const h = header(site);
  if (status === 401) return new WpError(`${h} 401 ${code}: ${msg}. Cek user & Application Password di config. Jika benar, hosting mungkin membuang header Authorization → tambahkan ke .htaccess: SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1`, status, code);
  if (status === 403) return new WpError(`${h} 403 ${code}: ${msg}. User "${site.user}" tidak punya izin untuk ${path} (perlu role lebih tinggi) atau diblokir security plugin.`, status, code);
  if (status === 404 && code === 'rest_no_route' && path.startsWith('/claude/')) return new WpError(`${h} Plugin "Claude Bridge" belum terpasang/aktif. Upload wp-elementor-mcp/dist/claude-bridge.zip lewat Plugins → Add New → Upload, lalu aktifkan.`, status, code);
  if (status === 409 && code === 'conflict') return new WpError(`${h} BENTROK: ${msg}`, status, code);
  return new WpError(`${h} HTTP ${status} ${code}: ${msg || JSON.stringify(json).slice(0, 300)}`, status, code);
}

/** Ambil HTML publik (tanpa auth) dengan cache-buster. */
export async function fetchPublic(url: string): Promise<{ status: number; html: string }> {
  const u = new URL(url);
  u.searchParams.set('nocache', String(Date.now()));
  const res = await fetch(u, { headers: { 'User-Agent': 'wp-elementor-mcp/1.0', 'Cache-Control': 'no-cache' } });
  return { status: res.status, html: await res.text() };
}
