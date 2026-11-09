// Bangun assets/css/pr.css: Tailwind v4 (theme + utilities !important, dipindai dari PHP plugin) + preflight TERSKOP (.pr-scope)
// + @font-face dari build lama + kelas kustom globals.css lama. Dijalankan dengan Node dari folder mana pun.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const OLD = 'F:/0. Code/pusatriset';
const PLUG = 'E:/1. Code/pusatriset/plugin/pusatriset-data';
const require = createRequire(OLD + '/package.json');
const postcss = require('postcss');
const tailwind = require('@tailwindcss/postcss');

const TW = OLD + '/node_modules/tailwindcss';
const input = `
@layer theme, base, components, utilities;
@import "${TW}/theme.css" layer(theme);
@import "${TW}/utilities.css" layer(utilities) important;
@source "${PLUG}/includes/*.php";

@theme inline {
  --color-page: var(--bg-page);
  --color-card: var(--bg-card);
  --color-card-alt: var(--bg-card-alt);
  --color-warm: var(--border-warm);
  --color-brand-900: var(--brand-blue-900);
  --color-brand-700: var(--brand-blue-700);
  --color-brand-100: var(--brand-blue-100);
  --color-primary: var(--text-primary);
  --color-secondary: var(--text-secondary);
  --color-muted-warm: var(--text-muted);
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
  --font-serif: var(--font-source-serif);
}
`;

const out = await postcss([tailwind({ base: PLUG })]).process(input, { from: PLUG + '/build/in.css' });
let css = out.css;

// Preflight terskop: prefix semua selektor dengan .pr-scope (html/body/:host -> .pr-scope itu sendiri).
const pre = fs.readFileSync(TW + '/preflight.css', 'utf8');
const root = postcss.parse(pre);
const scoped = [];
root.walkRules((rule) => {
  if (rule.parent && rule.parent.type === 'atrule' && /keyframes/.test(rule.parent.name)) return;
  rule.selectors = rule.selectors.map((s) => {
    s = s.trim();
    if (s === 'html' || s === ':host' || s === 'body') return '.pr-scope';
    // .pr-scope.pr-scope = spesifisitas (0,2,x) agar menang atas aturan tema seperti ".entry-content p".
    if (s === '*' || s.startsWith('::') || s.startsWith('*')) return s.split(',').map((x) => '.pr-scope.pr-scope ' + x.trim()).join(',');
    return '.pr-scope.pr-scope ' + s;
  });
});
root.walkAtRules('layer', (a) => { if (a.nodes) a.replaceWith(a.nodes); else a.remove(); });
const preflight = root.toString();

// @font-face: salin dari CSS terkompilasi aplikasi lama, ganti path media.
const old = fs.readFileSync(OLD + '/.next/static/chunks/0ylx8wmm6xuqh.css', 'utf8');
const fonts = (old.match(/@font-face\{[^}]*\}/g) || []).map((f) => f.replace(/url\(\.\.\/media\//g, 'url(../media/')).join('\n');

const custom = `
.pr-scope{
  --font-geist-sans:Geist,"Geist Fallback",ui-sans-serif,system-ui,sans-serif;
  --font-geist-mono:"Geist Mono","Geist Mono Fallback",ui-monospace,monospace;
  --font-source-serif:"Source Serif 4","Source Serif 4 Fallback",serif;
  --background:#ffffff;--foreground:#0f172a;
  --bg-page:#F7F9FC;--bg-card:#FFFFFF;--bg-card-alt:#EEF3FA;--border-warm:#E2E8F0;
  --shadow-card:0 1px 3px rgba(15,23,42,.08),0 1px 2px rgba(15,23,42,.04);
  --brand-blue-900:#0C2D4A;--brand-blue-700:#14508A;--brand-blue-100:#E3EEF7;
  --brand-teal:#14B8A6;--brand-teal-dark:#0F766E;--brand-indigo:#6366F1;--brand-indigo-dark:#3730A3;
  --text-primary:#0F172A;--text-secondary:#475569;--text-muted:#64748B;
  --badge-still-relevant:#2F7A4F;--badge-needs-update:#B98A1E;--badge-superseded:#C9701F;--badge-retracted:#B8352E;--badge-foundational:var(--brand-blue-700);
  --badge-still-relevant-fg:var(--badge-still-relevant);--badge-needs-update-fg:var(--badge-needs-update);--badge-superseded-fg:var(--badge-superseded);--badge-retracted-fg:var(--badge-retracted);--badge-foundational-fg:var(--badge-foundational);
  --badge-still-relevant-bg:#E1F0E6;--badge-needs-update-bg:#F7EEDA;--badge-superseded-bg:#F8E3D2;--badge-retracted-bg:#F8DEDC;--badge-foundational-bg:var(--brand-blue-100);
  display:block;
  font-family:var(--font-geist-sans);
  font-feature-settings:normal;font-variation-settings:normal;
  line-height:1.5;-webkit-text-size-adjust:100%;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
}
.pr-scope a{color:inherit !important;text-decoration:none !important}
.pr-scope .gradient-card-teal{background:linear-gradient(135deg,#2dd4bf 0%,var(--brand-teal-dark) 55%,var(--brand-blue-900) 100%)}
.pr-scope .gradient-card-blue{background:linear-gradient(135deg,var(--brand-blue-700) 0%,var(--brand-blue-900) 100%)}
.pr-scope .gradient-card-indigo{background:linear-gradient(135deg,#818cf8 0%,var(--brand-indigo-dark) 55%,var(--brand-blue-900) 100%)}
.pr-scope .glass-card{background:color-mix(in srgb,var(--bg-card) 72%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid color-mix(in srgb,white 55%,transparent)}
.pr-scope .summary-content h2{margin-top:1em;margin-bottom:.4em;font-size:1.15em;font-weight:700}
.pr-scope .summary-content h3{margin-top:.9em;margin-bottom:.35em;font-size:1.05em;font-weight:600}
.pr-scope .summary-content p{margin-bottom:.75em;line-height:1.7}
.pr-scope .summary-content ul{margin-bottom:.75em;padding-left:1.25em;list-style:disc}
.pr-scope .summary-content ol{margin-bottom:.75em;padding-left:1.25em;list-style:decimal}
.pr-scope .summary-content li{margin-bottom:.25em}
.pr-scope .summary-content strong{font-weight:700}
.pr-scope .summary-content em{font-style:italic}
.pr-scope .summary-content u{text-decoration:underline}
.pr-scope details>summary::-webkit-details-marker{display:none}
`;

const final = '/* DIHASILKAN oleh plugin/build/build-css.mjs — jangan diedit manual */\n' + fonts + '\n' + css + '\n' + preflight + '\n' + custom;
fs.mkdirSync(PLUG + '/assets/css', { recursive: true });
fs.writeFileSync(PLUG + '/assets/css/pr.css', final);
console.log('pr.css', (final.length / 1024).toFixed(1) + ' KB');
