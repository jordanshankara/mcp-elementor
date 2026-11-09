// Kirim ARRAY section top-level dari berkas JSON ke halaman, satu per satu (index berurutan), lewat tool MCP elementor_structure.
// Guardrail, backup, rev, dan verifikasi tetap jalan. `--replace` menghapus dulu SEMUA section top-level halaman (backup otomatis tiap tulis).
// Contoh: node scripts/push-sections.ts pusatriset 15 ../pusatriset/elementor/out/home.json pusatriset.ai
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import fs from 'node:fs';
import path from 'node:path';
import { PKG } from '../src/sites.ts';

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const replace = process.argv.includes('--replace');
const [site, pageId, file, domain] = args;
if (!site || !pageId || !file || !domain) { console.error('pakai: push-sections.ts <site> <page_id> <berkas.json (array)> <confirm_domain> [--replace]'); process.exit(2); }
const sections = JSON.parse(fs.readFileSync(path.resolve(file), 'utf8'));
if (!Array.isArray(sections)) { console.error('berkas harus berupa array section'); process.exit(2); }
const client = new Client({ name: 'wpe-push-sections', version: '1' });
await client.connect(new StdioClientTransport({ command: process.execPath, args: [path.join(PKG, 'src', 'index.ts')], env: process.env as Record<string, string>, stderr: 'inherit' }));
const text = (r: any) => (r.content ?? []).map((c: any) => c.text).join('\n');
const call = (name: string, a: any) => client.callTool({ name, arguments: a }, undefined, { timeout: 600_000 }) as Promise<any>;
const outline = async (depth = 0) => {
  const o = await call('elementor_outline', { site, page_id: Number(pageId), max_depth: depth });
  const rev = /rev:\s*([0-9a-f]+)/.exec(text(o))?.[1];
  if (!rev) throw new Error('rev tidak ditemukan:\n' + text(o));
  return { rev, raw: text(o) };
};
try {
  if (replace) {
    // baris top-level outline = tanpa indentasi: '<id7> container'
    const ids = (await outline(1)).raw.split(String.fromCharCode(10)).map((l) => /^([0-9a-f]{7})\s/.exec(l)?.[1]).filter(Boolean) as string[];
    console.log('hapus section top-level:', ids.join(','));
    for (const id of ids) {
      const { rev } = await outline();
      const r = await call('elementor_structure', { site, page_id: Number(pageId), rev, confirm: true, confirm_domain: domain, op: 'remove', element_id: id, reason: 'ganti isi halaman (--replace)' });
      if (r.isError) { console.error(text(r)); process.exit(1); }
    }
  }
  for (let i = 0; i < sections.length; i++) {
    const { rev } = await outline();
    const r = await call('elementor_structure', { site, page_id: Number(pageId), rev, confirm_domain: domain, op: 'insert', parent_id: null, index: i, element: sections[i], reason: `section ${i + 1}/${sections.length}` });
    console.log(`#${i + 1}:`, text(r).split('\n').slice(0, 3).join(' | '));
    if (r.isError) { process.exitCode = 1; break; }
  }
} finally { await client.close(); }
