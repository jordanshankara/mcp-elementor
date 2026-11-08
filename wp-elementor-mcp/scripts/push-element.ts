// Kirim elemen Elementor BESAR dari berkas JSON lewat tool MCP elementor_structure (guardrail, backup, verifikasi tetap jalan).
// Pakai bila payload terlalu besar untuk diketik di panggilan tool (mis. daftar dokumen).
// Contoh: node scripts/push-element.ts regulasi 543 null 2 ../sites/regulasi/design/library_element.json regulasiai.id
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import fs from 'node:fs';
import path from 'node:path';
import { PKG } from '../src/sites.ts';

const [site, pageId, parent, index, file, domain, reason = 'insert elemen dari berkas'] = process.argv.slice(2);
if (!site || !pageId || !file || !domain) { console.error('pakai: push-element.ts <site> <page_id> <parent_id|null> <index> <berkas.json> <confirm_domain> [alasan]'); process.exit(2); }
const element = JSON.parse(fs.readFileSync(path.resolve(file), 'utf8'));
const client = new Client({ name: 'wpe-push', version: '1' });
await client.connect(new StdioClientTransport({ command: process.execPath, args: [path.join(PKG, 'src', 'index.ts')], env: process.env as Record<string, string>, stderr: 'inherit' }));
const text = (r: any) => (r.content ?? []).map((c: any) => c.text).join('\n');
try {
  const o: any = await client.callTool({ name: 'elementor_outline', arguments: { site, page_id: Number(pageId), max_depth: 0 } });
  const rev = /rev:\s*([0-9a-f]+)/.exec(text(o))?.[1];
  if (!rev) throw new Error('rev tidak ditemukan:\n' + text(o));
  const r: any = await client.callTool({ name: 'elementor_structure', arguments: { site, page_id: Number(pageId), rev, confirm_domain: domain, op: 'insert', parent_id: parent === 'null' ? null : parent, index: Number(index), element, reason } }, undefined, { timeout: 600_000 });
  console.log(text(r));
  if (r.isError) process.exitCode = 1;
} finally { await client.close(); }
