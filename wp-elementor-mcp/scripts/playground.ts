// Menjalankan 2 (atau lebih) WordPress Playground lokal untuk tes: WP + Elementor FREE + Claude Bridge.
// Hasil: config/sites.playground.json (format sama dengan sites.local.json). Biarkan proses ini berjalan selama tes.
// Pemakaian: node scripts/playground.ts [jumlah=2] [portAwal=9401]
import { spawn, type ChildProcess } from 'node:child_process';
import { mkdirSync, rmSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { PKG, ROOT } from '../src/sites.ts';

const count = Number(process.argv[2] ?? 2);
const port0 = Number(process.argv[3] ?? 9401);
const names = ['test-a', 'test-b', 'test-c', 'test-d'].slice(0, count);
const cli = path.join(PKG, 'node_modules', '@wp-playground', 'cli', 'cli.js');
const procs: ChildProcess[] = [];

async function startOne(name: string, port: number) {
  const out = path.join(PKG, '.playground', name);
  rmSync(out, { recursive: true, force: true });
  mkdirSync(out, { recursive: true });
  const args = [
    cli, 'server', `--port=${port}`, '--php=8.3', '--wp=latest', '--verbosity=normal',
    // 1 worker: dengan >1 worker tiap worker punya salinan filesystem sendiri → file CSS Elementor yang dibuat
    // di worker A tidak terlihat dari worker B (artefak Playground, tidak terjadi di hosting sungguhan).
    '--workers=1',
    `--blueprint=${path.join(PKG, 'playground', 'blueprint.json')}`,
    // Elementor FREE dari wordpress.org (di-download sekali ke .playground/cache oleh scripts/fetch-elementor)
    '--mount-dir', path.join(PKG, '.playground', 'cache', 'elementor'), '/wordpress/wp-content/plugins/elementor',
    '--mount-dir', path.join(PKG, 'bridge-plugin', 'claude-bridge'), '/wordpress/wp-content/plugins/claude-bridge',
    '--mount-dir', out, '/claude-out',
  ];
  // Folder sementara Playground (±200 MB/situs) diarahkan ke dalam proyek supaya tidak memenuhi drive C:.
  const tmp = path.join(PKG, '.playground', 'tmp', name);
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  const p = spawn(process.execPath, args, { stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, TEMP: tmp, TMP: tmp, TMPDIR: tmp } });
  procs.push(p);
  const log: string[] = [];
  p.stdout!.on('data', (d) => log.push(String(d)));
  p.stderr!.on('data', (d) => log.push(String(d)));
  p.on('exit', (c) => { if (c) console.error(`[${name}] keluar dengan kode ${c}\n${log.join('').slice(-2000)}`); });
  const file = path.join(out, 'site.json');
  const t0 = Date.now();
  while (!existsSync(file)) {
    if (Date.now() - t0 > 600_000) throw new Error(`[${name}] timeout menunggu setup.\n${log.join('').slice(-2000)}`);
    if (p.exitCode !== null) throw new Error(`[${name}] gagal start.\n${log.join('').slice(-3000)}`);
    await new Promise((r) => setTimeout(r, 1000));
  }
  // tunggu server benar-benar melayani
  const url = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 120; i++) {
    try { const r = await fetch(url + '/?rest_route=/'); if (r.ok) break; } catch {}
    await new Promise((r) => setTimeout(r, 1000));
  }
  const s = JSON.parse(readFileSync(file, 'utf8'));
  console.log(`[${name}] siap di ${url} (WP ${s.wp}, Elementor ${s.elementor}) dalam ${Math.round((Date.now() - t0) / 1000)}s`);
  return { name, url, ...s };
}

const results = [];
for (let i = 0; i < names.length; i++) results.push(await startOne(names[i], port0 + i));

const cfg = {
  sites: Object.fromEntries(results.map((r, i) => [r.name, {
    url: r.url, user: r.user, app_password: r.app_password, label: `Playground ${r.name}`,
    env: i === 0 ? 'local' : 'prod',            // test-b disimulasikan sebagai PROD untuk menguji confirm_domain
    readonly: false, tags: i === 0 ? ['grup-tes', 'satu'] : ['grup-tes'],
    _pages: { home: r.home, container: r.container },
  }])),
};
mkdirSync(path.join(ROOT, 'config'), { recursive: true });
writeFileSync(path.join(ROOT, 'config', 'sites.playground.json'), JSON.stringify(cfg, null, 2));
console.log('READY config/sites.playground.json');

const stop = () => { procs.forEach((p) => p.kill()); process.exit(0); };
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
setInterval(() => {}, 1 << 30);
