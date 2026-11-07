// Fungsi murni untuk memanipulasi struktur `_elementor_data` (V3 section/column/widget dan V4 container/atomic).
// Tidak ada I/O di sini supaya mudah di-unit-test.

export type Settings = Record<string, unknown>;
export interface El {
  id: string;
  elType: string;
  widgetType?: string;
  isInner?: boolean;
  settings?: Settings;
  elements?: El[];
  [k: string]: unknown;
}

export class ElementorError extends Error {}

// ---------- traversal ----------
export function walk(
  data: El[],
  fn: (el: El, depth: number, parent: El | null, index: number) => void | false,
  depth = 0,
  parent: El | null = null,
): void {
  data.forEach((el, i) => {
    if (fn(el, depth, parent, i) === false) return;
    if (Array.isArray(el.elements)) walk(el.elements, fn, depth + 1, el);
  });
}

export function typeOf(el: El): string {
  return el.elType === 'widget' ? (el.widgetType ?? 'widget') : el.elType;
}

interface Loc { el: El; parent: El | null; siblings: El[]; index: number; depth: number }
export function locate(data: El[], id: string): Loc {
  let found: Loc | null = null;
  const visit = (arr: El[], parent: El | null, depth: number) => {
    for (let i = 0; i < arr.length && !found; i++) {
      const el = arr[i];
      if (el.id === id) { found = { el, parent, siblings: arr, index: i, depth }; return; }
      if (Array.isArray(el.elements)) visit(el.elements, el, depth + 1);
    }
  };
  visit(data, null, 0);
  if (!found) throw new ElementorError(`Elemen "${id}" tidak ditemukan di halaman ini. Jalankan elementor_outline untuk melihat id yang valid.`);
  return found;
}

// ---------- text helpers ----------
const ENT: Record<string, string> = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', hellip: '...', ndash: '-', mdash: '-', rsquo: "'", lsquo: "'", rdquo: '"', ldquo: '"' };
export function normalizeText(s: string): string {
  return s
    .replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&([a-z]+);/gi, (m, n) => ENT[n.toLowerCase()] ?? m)
    .replace(/[‘’‚′]/g, "'")
    .replace(/[“”„″]/g, '"')
    .replace(/[–—]/g, '-')
    .replace(/…/g, '...')
    .replace(/[\s ]+/g, ' ')
    .trim();
}

const TEXT_KEYS = ['title', 'editor', 'text', 'html', 'caption', 'description_text', 'title_text', 'testimonial_content', 'alert_title', 'tab_title', 'inner_text', 'content', 'label', 'paragraph'];
const SKIP_KEY = /(^_|color|typography|font|size|width|height|margin|padding|border|radius|shadow|background|align|position|z_index|css|motion|animation|classes|^hide_|_mobile$|_tablet$|^gap|^flex|^grid|^custom_css)/i;

/** Ambil nilai string dari setting (mendukung V4 `{ $$type, value }`). */
function unwrap(v: unknown): unknown {
  if (v && typeof v === 'object' && '$$type' in (v as object) && 'value' in (v as object)) return unwrap((v as { value: unknown }).value);
  return v;
}

/** Semua string teks yang "kelihatan" di setting elemen (bukan style). */
export function textsOf(settings: Settings | undefined, maxDepth = 3): string[] {
  const out: string[] = [];
  const visit = (v: unknown, key: string, d: number, textKey: boolean) => {
    v = unwrap(v);
    if (d > maxDepth || SKIP_KEY.test(key)) return;
    if (typeof v === 'string') {
      const t = normalizeText(v);
      if (!t || /^(https?:|#|\d+(px|%|em|rem)?$)/i.test(t) || !/[a-z]/i.test(t)) return;
      // nilai enum seperti "full_width", "classic", "yes" hanya diabaikan di key non-teks
      if (!textKey && !TEXT_KEYS.includes(key) && /^[a-z0-9_-]+$/.test(t)) return;
      out.push(t);
    } else if (Array.isArray(v)) v.forEach((x) => visit(x, key, d + 1, textKey));
    else if (v && typeof v === 'object') for (const [k, x] of Object.entries(v)) visit(x, k, d + 1, textKey || TEXT_KEYS.includes(k));
  };
  if (!settings) return out;
  // prioritaskan key teks umum
  for (const k of TEXT_KEYS) if (k in settings) visit(settings[k], k, 0, true);
  for (const [k, v] of Object.entries(settings)) if (!TEXT_KEYS.includes(k)) visit(v, k, 0, false);
  return out;
}

function snippet(el: El, len = 40): string {
  const s = el.settings ?? {};
  const t = textsOf(s)[0];
  if (t) return t.length > len ? t.slice(0, len - 1) + '…' : t;
  const img = unwrap(s.image) as { url?: string } | undefined;
  const url = (img && typeof img === 'object' && typeof img.url === 'string' ? img.url : undefined)
    ?? (typeof (unwrap(s.background_image) as { url?: string })?.url === 'string' ? (unwrap(s.background_image) as { url: string }).url : undefined);
  if (url) return '🖼 ' + url.split('/').pop();
  return '';
}

// ---------- read views ----------
/** Outline ringkas: satu baris per elemen. */
export function outline(data: El[], opts: { maxDepth?: number; rootId?: string } = {}): string {
  const lines: string[] = [];
  const roots = opts.rootId ? [locate(data, opts.rootId).el] : data;
  walk(roots, (el, depth) => {
    if (opts.maxDepth !== undefined && depth > opts.maxDepth) return false;
    const sn = snippet(el);
    const n = el.elements?.length ?? 0;
    const kids = n && opts.maxDepth !== undefined && depth === opts.maxDepth ? ` (+${countElements(el.elements!)} anak)` : '';
    lines.push(`${'  '.repeat(depth)}${el.id} ${typeOf(el)}${sn ? ` "${sn}"` : ''}${kids}`);
  });
  return lines.join('\n');
}

export function countElements(data: El[]): number {
  let n = 0;
  walk(data, () => { n++; });
  return n;
}
export function maxDepth(data: El[]): number {
  let m = 0;
  walk(data, (_el, d) => { if (d + 1 > m) m = d + 1; });
  return m;
}

function isEmpty(v: unknown): boolean {
  if (v === '' || v === null || v === undefined) return true;
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === 'object') {
    const o = v as Record<string, unknown>;
    if ('$$type' in o) return isEmpty(o.value);
    const vals = Object.values(o);
    if (vals.length === 0) return true;
    // unit objects like {unit:'px', size:''}
    if ('unit' in o && 'size' in o && (o.size === '' || o.size === null)) return true;
    return vals.every(isEmpty);
  }
  return false;
}
export function prune(settings: Settings = {}): Settings {
  const out: Settings = {};
  for (const [k, v] of Object.entries(settings)) if (!isEmpty(v)) out[k] = v;
  return out;
}

/** Satu elemen tanpa anak-anaknya; setting kosong dibuang. */
export function getElement(data: El[], id: string): { id: string; type: string; parent: string | null; index: number; children: string[]; settings: Settings; extra?: Record<string, unknown> } {
  const { el, parent, index } = locate(data, id);
  const { id: _i, elType: _t, widgetType: _w, settings, elements, isInner: _n, ...rest } = el;
  const extra = Object.keys(rest).length ? rest : undefined;
  return { id: el.id, type: typeOf(el), parent: parent?.id ?? null, index, children: (elements ?? []).map((c) => c.id), settings: prune(settings), ...(extra ? { extra } : {}) };
}

export interface Match { id: string; type: string; key: string; snippet: string }
export function findText(data: El[], query: string, limit = 30): Match[] {
  const q = normalizeText(query).toLowerCase();
  const out: Match[] = [];
  walk(data, (el) => {
    if (out.length >= limit) return false;
    const visit = (v: unknown, path: string, d: number) => {
      v = unwrap(v);
      if (d > 4 || out.length >= limit) return;
      if (typeof v === 'string') {
        const t = normalizeText(v);
        const i = t.toLowerCase().indexOf(q);
        if (i >= 0) out.push({ id: el.id, type: typeOf(el), key: path, snippet: t.slice(Math.max(0, i - 20), i + q.length + 30) });
      } else if (Array.isArray(v)) v.forEach((x, j) => visit(x, `${path}[${j}]`, d + 1));
      else if (v && typeof v === 'object') for (const [k, x] of Object.entries(v)) visit(x, path ? `${path}.${k}` : k, d + 1);
    };
    for (const [k, v] of Object.entries(el.settings ?? {})) visit(v, k, 0);
  });
  return out;
}

// ---------- writes (immutable: selalu mengembalikan salinan) ----------
const clone = <T>(x: T): T => structuredClone(x);

function isPlainObject(v: unknown): v is Record<string, unknown> {
  return !!v && typeof v === 'object' && !Array.isArray(v);
}
/** JSON merge-patch: object digabung, array diganti, null menghapus key. */
export function mergePatch(target: unknown, patch: unknown): unknown {
  if (!isPlainObject(patch)) return clone(patch);
  // V4: patch berupa {$$type,value} menggantikan seluruh nilai
  if ('$$type' in patch) return clone(patch);
  const out: Record<string, unknown> = isPlainObject(target) ? { ...target } : {};
  for (const [k, v] of Object.entries(patch)) {
    if (v === null) delete out[k];
    else out[k] = mergePatch(out[k], v);
  }
  return out;
}

export interface Patch { id: string; settings: Settings }
export function applyPatches(data: El[], patches: Patch[]): El[] {
  const next = clone(data);
  for (const p of patches) {
    const { el } = locate(next, p.id);
    if (!isPlainObject(p.settings) || Object.keys(p.settings).length === 0) throw new ElementorError(`Patch untuk "${p.id}" kosong.`);
    el.settings = mergePatch(Array.isArray(el.settings) ? {} : el.settings ?? {}, p.settings) as Settings;
  }
  return next;
}

export function newId(existing: Set<string>): string {
  let id: string;
  do id = Math.floor(Math.random() * 0xfffffff).toString(16).padStart(7, '0'); while (existing.has(id));
  existing.add(id);
  return id;
}
export function allIds(data: El[]): Set<string> {
  const s = new Set<string>();
  walk(data, (el) => { s.add(el.id); });
  return s;
}
/** Beri id baru ke elemen + semua turunannya (dipakai untuk duplicate/insert/copy). */
export function reId(el: El, ids: Set<string>): El {
  const c = clone(el);
  walk([c], (e) => {
    e.id = newId(ids);
    if (!Array.isArray(e.elements)) e.elements = [];
    if (e.settings === undefined || Array.isArray(e.settings)) e.settings = {};
  });
  return c;
}

export function insert(data: El[], parentId: string | null, index: number | undefined, element: El): { data: El[]; id: string } {
  const next = clone(data);
  const ids = allIds(next);
  const el = reId(element, ids);
  const target = parentId ? locate(next, parentId).el : null;
  if (target && target.elType === 'widget') throw new ElementorError('Tidak bisa menyisipkan ke dalam widget; pilih container/column.');
  const arr = target ? (target.elements ??= []) : next;
  arr.splice(index === undefined ? arr.length : Math.max(0, Math.min(index, arr.length)), 0, el);
  return { data: next, id: el.id };
}

export function duplicate(data: El[], id: string): { data: El[]; id: string } {
  const next = clone(data);
  const loc = locate(next, id);
  const copy = reId(loc.el, allIds(next));
  loc.siblings.splice(loc.index + 1, 0, copy);
  return { data: next, id: copy.id };
}

export function remove(data: El[], id: string): El[] {
  const next = clone(data);
  const loc = locate(next, id);
  loc.siblings.splice(loc.index, 1);
  return next;
}

export function move(data: El[], id: string, parentId: string | null, index?: number): El[] {
  const next = clone(data);
  const loc = locate(next, id);
  if (parentId) {
    let inside = false;
    walk([loc.el], (e) => { if (e.id === parentId) inside = true; });
    if (inside) throw new ElementorError('Tidak bisa memindahkan elemen ke dalam dirinya sendiri.');
  }
  loc.siblings.splice(loc.index, 1);
  const target = parentId ? locate(next, parentId).el : null;
  if (target && target.elType === 'widget') throw new ElementorError('Tujuan adalah widget; pilih container/column.');
  const arr = target ? (target.elements ??= []) : next;
  arr.splice(index === undefined ? arr.length : Math.max(0, Math.min(index, arr.length)), 0, loc.el);
  return next;
}

/** Tipe widget yang dipakai di subtree (untuk validasi Free/Pro). */
export function widgetTypes(els: El[]): Set<string> {
  const s = new Set<string>();
  walk(els, (e) => { if (e.elType === 'widget' && e.widgetType) s.add(e.widgetType); });
  return s;
}
export function elTypes(els: El[]): Set<string> {
  const s = new Set<string>();
  walk(els, (e) => { if (e.elType !== 'widget') s.add(e.elType); });
  return s;
}

/** String teks baru dari patch (untuk verifikasi render). */
export function patchTexts(patches: Patch[]): string[] {
  const out: string[] = [];
  for (const p of patches) out.push(...textsOf(p.settings));
  return out.filter((t) => t.length >= 3);
}

// ---------- guardrail performa ----------
const PRO_HINT: Record<string, string> = {
  form: 'Pakai widget "shortcode" berisi form dari plugin gratis (WPForms Lite / Contact Form 7).',
  posts: 'Pakai widget bawaan tema / shortcode, atau "text-editor" berisi daftar link.',
  'loop-grid': 'Loop Grid hanya Pro. Alternatif: widget "shortcode" dari plugin daftar post gratis.',
  slides: 'Pakai widget "image-carousel" (Free).',
  'animated-headline': 'Pakai widget "heading" (Free).',
  'price-table': 'Bangun dengan container + heading + text-editor + button (Free).',
  'call-to-action': 'Bangun dengan container + heading + text-editor + button (Free).',
  'nav-menu': 'Menu biasanya milik tema di Free; kelola via wp_request /wp/v2/menu-items.',
  popup: 'Popup hanya Pro.',
};
export function proAlternative(type: string): string {
  return PRO_HINT[type] ?? 'Gunakan kombinasi widget Free: container, heading, text-editor, image, button, icon-list.';
}

export interface Lint { level: 'warn' | 'block'; msg: string }
export function perfLint(data: El[], opts: { maxNest?: number; maxElements?: number } = {}): Lint[] {
  const out: Lint[] = [];
  const maxNest = opts.maxNest ?? 4;
  const maxEls = opts.maxElements ?? 800;
  const n = countElements(data);
  if (n > maxEls) out.push({ level: 'warn', msg: `Halaman punya ${n} elemen (> ${maxEls}). DOM besar memperlambat; pertimbangkan memecah/menyederhanakan.` });
  // nesting layout (container/section/column), bukan widget
  let deepest = 0; let deepId = '';
  walk(data, (el, d) => {
    if (el.elType !== 'widget' && d + 1 > deepest) { deepest = d + 1; deepId = el.id; }
  });
  if (deepest > maxNest + 1) out.push({ level: 'warn', msg: `Nesting layout ${deepest} level (di ${deepId}). Ideal ≤ ${maxNest}; kurangi wrapper.` });
  const fonts = new Set<string>();
  walk(data, (el) => {
    const s = el.settings ?? {};
    for (const [k, v] of Object.entries(s)) {
      if (/font_family$/.test(k) && typeof v === 'string' && v) fonts.add(v);
    }
    const html = typeof s.html === 'string' ? s.html : '';
    // Pengecualian sempit (izin pengguna 2026-11-06 untuk fitur fungsional, mis. pencarian dokumen):
    // widget html boleh memuat <script> HANYA bila membawa penanda <!-- allow-js:<alasan> -->.
    if (/<script\b/i.test(html) && !/<!--\s*allow-js:\s*[^\s>-][^>]*-->/i.test(html)) out.push({ level: 'block', msg: `Elemen ${el.id} berisi <script>. JS kustom dilarang oleh guardrail (risiko rusak & lambat). Hanya diizinkan dengan penanda <!-- allow-js:alasan --> atas izin pengguna.` });
    if (el.widgetType === 'image') {
      const size = s.image_size;
      if (size === 'full') out.push({ level: 'warn', msg: `Gambar ${el.id} memakai image_size "full". Pilih "large"/"medium_large" kecuali benar-benar full-width.` });
    }
    const img = (s.image ?? s.background_image) as { url?: string } | undefined;
    if (img?.url && /\.gif(\?|$)/i.test(img.url)) out.push({ level: 'warn', msg: `Elemen ${el.id} memakai GIF. Ganti ke WebP/video.` });
  });
  if (fonts.size > 2) out.push({ level: 'warn', msg: `Halaman memakai ${fonts.size} keluarga font lokal (${[...fonts].join(', ')}). Maks 2; gunakan font global kit.` });
  return out;
}
