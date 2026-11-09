// Hasilkan includes/icons.php dari paket lucide-react yang sama dengan aplikasi lama (ikon identik).
import fs from 'node:fs';
import path from 'node:path';

const dir = 'F:/0. Code/pusatriset/node_modules/lucide-react/dist/esm/icons';
const want = {
  BrainCircuit: ['brain-circuit'], Search: ['search'], FileStack: ['file-stack'], Flag: ['flag'], Building2: ['building-2'], Sparkles: ['sparkles'],
  TrendingUp: ['trending-up'], Flame: ['flame'], BarChart3: ['chart-no-axes-column', 'bar-chart-3', 'chart-column'], BookMarked: ['book-marked'],
  Languages: ['languages'], UserCheck: ['user-check'], Quote: ['quote'], FileText: ['file-text'], LayoutGrid: ['layout-grid'], LibraryBig: ['library-big'],
  SearchX: ['search-x'], Globe2: ['globe-2', 'earth'], CalendarRange: ['calendar-range'], Tags: ['tags'], Award: ['award'], SlidersHorizontal: ['sliders-horizontal'],
  LineChart: ['chart-line', 'line-chart'], PieChart: ['chart-pie', 'pie-chart'], BookOpenCheck: ['book-open-check'], MapPin: ['map-pin'], Trophy: ['trophy'],
  BookOpen: ['book-open'], FileCheck: ['file-check'], Database: ['database'], Eye: ['eye'], Lock: ['lock'], Globe: ['globe'],
  MessageSquareWarning: ['message-square-warning'], AlertTriangle: ['triangle-alert', 'alert-triangle'], ShieldCheck: ['shield-check'],
  GraduationCap: ['graduation-cap'], Cpu: ['cpu'], Menu: ['menu'], X: ['x'],
};
const BS = String.fromCharCode(92);
const esc = (s) => String(s).split(BS).join(BS + BS).split("'").join(BS + "'");
let out = "<?php\n// DIHASILKAN oleh build/gen-icons.mjs dari lucide-react (jangan diedit manual).\nreturn [\n";
const missing = [];
for (const [name, cands] of Object.entries(want)) {
  let found = null;
  for (const c of cands) { const f = path.join(dir, c + '.mjs'); if (fs.existsSync(f)) { found = f; break; } }
  if (!found) { missing.push(name); continue; }
  let src = fs.readFileSync(found, 'utf8');
  for (let hop = 0; hop < 3 && src.indexOf('const __iconData = ') < 0; hop++) {
    const mm = src.match(new RegExp("from '(?:[.]/)([a-z0-9-]+)[.]mjs'"));
    if (!mm) break;
    src = fs.readFileSync(path.join(dir, mm[1] + '.mjs'), 'utf8');
  }
  if (src.indexOf('const __iconData = ') < 0) { missing.push(name + '(format)'); continue; }
  const start = src.indexOf('const __iconData = ') + 'const __iconData = '.length;
  const end = src.indexOf('};', start) + 1;
  const data = new Function('return ' + src.slice(start, end))();
  const inner = data.node.map(([tag, attrs]) => '<' + tag + ' ' + Object.entries(attrs).filter(([k]) => k !== 'key').map(([k, v]) => k + '="' + v + '"').join(' ') + '/>').join('');
  out += "  '" + name + "' => '" + esc(inner) + "',\n";
}
out += '];\n';
fs.writeFileSync('E:/1. Code/pusatriset/plugin/pusatriset-data/includes/icons.php', out);
console.log('ikon:', Object.keys(want).length - missing.length, 'hilang:', missing.join(',') || '-');
