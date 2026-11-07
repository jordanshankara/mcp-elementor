// Membuat dist/claude-bridge.zip untuk di-upload lewat wp-admin → Plugins → Add New → Upload.
import { mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { PKG } from '../src/sites.ts';

const src = path.join(PKG, 'bridge-plugin');
const out = path.join(PKG, 'dist', 'claude-bridge.zip');
mkdirSync(path.dirname(out), { recursive: true });
rmSync(out, { force: true });
const py = `import zipfile,os,sys
src,out=sys.argv[1],sys.argv[2]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for root,_,files in os.walk(os.path.join(src,'claude-bridge')):
    for f in files:
      p=os.path.join(root,f); z.write(p, os.path.relpath(p, src).replace(os.sep,'/'))
print(out)`;
for (const bin of ['python', 'python3', 'py']) {
  try { console.log(execFileSync(bin, ['-I', '-c', py, src, out], { encoding: 'utf8' }).trim()); process.exit(0); } catch {}
}
console.error('Python tidak ditemukan. Zip manual folder bridge-plugin/claude-bridge (folder harus ada di dalam zip).');
process.exit(1);
