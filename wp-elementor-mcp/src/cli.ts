#!/usr/bin/env node
// CLI cadangan (kalau MCP belum tersambung): memanggil tool MCP yang sama.
// Contoh: node src/cli.ts elementor_outline '{"site":"toko","page_id":12}'
//         node src/cli.ts --list
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import path from 'node:path';
import { PKG } from './sites.ts';

const [tool, json = '{}'] = process.argv.slice(2);
const client = new Client({ name: 'wpe-cli', version: '1' });
await client.connect(new StdioClientTransport({ command: process.execPath, args: [path.join(PKG, 'src', 'index.ts')], env: process.env as Record<string, string>, stderr: 'inherit' }));
try {
  if (!tool || tool === '--list') {
    const { tools } = await client.listTools();
    tools.forEach((t) => console.log(`${t.name} — ${t.description?.split('.')[0]}`));
  } else {
    const r: any = await client.callTool({ name: tool, arguments: JSON.parse(json) }, undefined, { timeout: 600_000 });
    console.log((r.content ?? []).map((c: any) => c.text).join('\n'));
    if (r.isError) process.exitCode = 1;
  }
} finally { await client.close(); }
