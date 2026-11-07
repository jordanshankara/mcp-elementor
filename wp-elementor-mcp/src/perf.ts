// Pengukuran performa ringkas. URL publik → PageSpeed Insights API. Situs lokal → Lighthouse lokal (Chromium Playwright).
import type { Site } from './sites.ts';

interface Res { strategy: string; score: number; lcp: string; cls: string; tbt: string; fcp: string; top: string[] }

function summarize(strategy: string, lhr: any): Res {
  const a = lhr.audits ?? {};
  const top = Object.values<any>(a)
    .filter((x) => x?.details?.type === 'opportunity' && (x.details.overallSavingsMs ?? 0) > 50)
    .sort((x, y) => (y.details.overallSavingsMs ?? 0) - (x.details.overallSavingsMs ?? 0))
    .slice(0, 3)
    .map((x) => `${x.title} (hemat ~${Math.round(x.details.overallSavingsMs)}ms)`);
  // tambahan diagnosa penting walau bukan "opportunity"
  for (const id of ['server-response-time', 'third-party-summary', 'dom-size']) {
    const x = a[id];
    if (x && x.score !== null && x.score < 0.9 && top.length < 4) top.push(`${x.title}${x.displayValue ? ' — ' + x.displayValue : ''}`);
  }
  return {
    strategy,
    score: Math.round((lhr.categories?.performance?.score ?? 0) * 100),
    lcp: a['largest-contentful-paint']?.displayValue ?? '-',
    cls: a['cumulative-layout-shift']?.displayValue ?? '-',
    tbt: a['total-blocking-time']?.displayValue ?? '-',
    fcp: a['first-contentful-paint']?.displayValue ?? '-',
    top,
  };
}

function isLocal(url: string) {
  const h = new URL(url).hostname;
  return h === 'localhost' || h === '127.0.0.1' || h === '[::1]' || h.endsWith('.local') || h.endsWith('.test') || h.endsWith('.localhost');
}

async function psi(url: string, strategy: string, key?: string): Promise<Res> {
  const u = new URL('https://www.googleapis.com/pagespeedonline/v5/runPagespeed');
  u.searchParams.set('url', url);
  u.searchParams.set('strategy', strategy);
  u.searchParams.set('category', 'performance');
  if (key) u.searchParams.set('key', key);
  const r = await fetch(u, { signal: AbortSignal.timeout(120000) });
  const j: any = await r.json();
  if (!r.ok) throw new Error(`PageSpeed API ${r.status}: ${j?.error?.message ?? ''}${r.status === 429 ? ' (kuota habis — isi pagespeed_api_key di config)' : ''}`);
  return summarize(strategy, j.lighthouseResult);
}

async function lighthouseLocal(url: string, strategy: string): Promise<Res> {
  // Chromium diluncurkan oleh Playwright (lebih andal di Windows daripada chrome-launcher), Lighthouse menempel via port debug.
  const { chromium } = await import('playwright');
  const lighthouse = (await import('lighthouse')).default;
  const port = 9300 + Math.floor(Math.random() * 500);
  const browser = await chromium.launch({ args: [`--remote-debugging-port=${port}`] });
  try {
    const flags = { port, output: 'json' as const, logLevel: 'error' as const, onlyCategories: ['performance'] };
    const config = strategy === 'desktop' ? (await import('lighthouse/core/config/desktop-config.js')).default : undefined;
    const r = await lighthouse(url, flags, config);
    return summarize(strategy + ' (lokal)', r!.lhr);
  } finally { await browser.close(); }
}

export async function perfCheck(site: Site, url: string, strategy: 'mobile' | 'desktop' | 'both', key?: string): Promise<string> {
  const list = strategy === 'both' ? ['mobile', 'desktop'] : [strategy];
  const lines: string[] = [`perf ${url}`];
  for (const s of list) {
    const r = isLocal(url) ? await lighthouseLocal(url, s) : await psi(url, s, key);
    lines.push(`${r.strategy}: ${r.score}/100 ${r.score >= 90 ? '✓' : r.score >= 50 ? '△' : '✗'} · LCP ${r.lcp} · CLS ${r.cls} · TBT ${r.tbt} · FCP ${r.fcp}`);
    r.top.forEach((t) => lines.push(`  - ${t}`));
  }
  void site;
  return lines.join('\n');
}
