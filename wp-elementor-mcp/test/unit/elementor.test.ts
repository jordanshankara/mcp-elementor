import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as E from '../../src/elementor.ts';

const v3 = (): E.El[] => JSON.parse(readFileSync(new URL('../fixtures/v3.json', import.meta.url), 'utf8'));
const v4 = (): E.El[] => JSON.parse(readFileSync(new URL('../fixtures/v4.json', import.meta.url), 'utf8'));

test('outline V3 ringkas dan berisi id+tipe+cuplikan', () => {
  const o = E.outline(v3());
  assert.match(o, /^sec1 section/m);
  assert.match(o, /^    h1 heading "Selamat Datang di Toko Kami"/m);
  assert.match(o, /t1 text-editor "Kami menjual produk & jasa terbaik/);
  assert.match(o, /img1 image "🖼 foto.jpg"/);
  assert.match(o, /il1 icon-list "Gratis ongkir"/);
  assert.ok(o.length < 600, 'outline harus jauh lebih kecil dari JSON');
});

test('outline maxDepth meringkas anak', () => {
  const o = E.outline(v3(), { maxDepth: 0 });
  assert.equal(o.split('\n').length, 2);
  assert.match(o, /sec1 section \(\+4 anak\)/);
});

test('outline V4 atomic membaca $$type value', () => {
  const o = E.outline(v4());
  assert.match(o, /eh1 e-heading "Judul Atomic"/);
  assert.match(o, /ep1 e-paragraph "Paragraf atomic V4"/);
});

test('getElement memangkas setting & tanpa anak', () => {
  const d = v3();
  d[0].elements![0].elements![0].settings!.empty = '';
  const g = E.getElement(d, 'h1');
  assert.equal(g.parent, 'col1');
  assert.equal(g.type, 'heading');
  assert.equal(g.settings.empty, undefined);
  assert.equal(g.settings.title, 'Selamat Datang di Toko Kami');
});

test('findText menemukan teks dalam repeater dan HTML', () => {
  const m = E.findText(v3(), 'garansi');
  assert.equal(m.length, 1);
  assert.equal(m[0].id, 'il1');
  assert.equal(m[0].key, 'icon_list[1].text');
  assert.equal(E.findText(v3(), 'produk & jasa')[0].id, 't1');
  assert.equal(E.findText(v4(), 'atomic V4')[0].id, 'ep1');
});

test('applyPatches merge (object digabung, null hapus) dan immutable', () => {
  const d = v3();
  const n = E.applyPatches(d, [
    { id: 'h1', settings: { title: 'Promo 11.11', title_color: null } },
    { id: 'b1', settings: { link: { url: 'https://wa.me/62822' } } },
  ]);
  const h = E.getElement(n, 'h1').settings;
  assert.equal(h.title, 'Promo 11.11');
  assert.equal(h.title_color, undefined);
  assert.equal(h.header_size, 'h1');
  const b = E.getElement(n, 'b1').settings as any;
  assert.equal(b.link.url, 'https://wa.me/62822');
  assert.equal(b.link.is_external, 'on');
  assert.equal(E.getElement(d, 'h1').settings.title, 'Selamat Datang di Toko Kami', 'data asli tidak berubah');
});

test('patch V4 mengganti {$$type,value} utuh', () => {
  const n = E.applyPatches(v4(), [{ id: 'eh1', settings: { title: { $$type: 'string', value: 'Baru' } } }]);
  assert.deepEqual(E.getElement(n, 'eh1').settings.title, { $$type: 'string', value: 'Baru' });
});

test('id salah -> error jelas, bukan sukses palsu', () => {
  assert.throws(() => E.applyPatches(v3(), [{ id: 'xxx', settings: { title: 'a' } }]), /tidak ditemukan/);
  assert.throws(() => E.applyPatches(v3(), [{ id: 'h1', settings: {} }]), /kosong/);
});

test('duplicate memberi id baru unik untuk semua turunan', () => {
  const { data, id } = E.duplicate(v3(), 'sec1');
  assert.equal(data.length, 3);
  assert.equal(data[1].id, id);
  const ids = [...E.allIds(data)];
  assert.equal(ids.length, new Set(ids).size);
  assert.equal(E.countElements(data), E.countElements(v3()) + 5);
});

test('insert, move, remove', () => {
  let { data, id } = E.insert(v3(), 'col1', 0, { id: 'tmp', elType: 'widget', widgetType: 'heading', settings: { title: 'Baru' } });
  assert.equal(E.getElement(data, id).index, 0);
  data = E.move(data, id, 'col3', 0);
  assert.equal(E.getElement(data, id).parent, 'col3');
  assert.throws(() => E.move(data, 'sec1', 'col1'), /dirinya sendiri/);
  assert.throws(() => E.insert(data, 'h1', 0, { id: 'z', elType: 'widget', widgetType: 'heading' }), /widget/);
  data = E.remove(data, id);
  assert.throws(() => E.getElement(data, id), /tidak ditemukan/);
});

test('widgetTypes & patchTexts', () => {
  assert.deepEqual([...E.widgetTypes(v3())].sort(), ['button', 'heading', 'icon-list', 'image', 'text-editor']);
  assert.deepEqual(E.patchTexts([{ id: 'h1', settings: { title: 'Promo 11.11', title_color: '#fff' } }]), ['Promo 11.11']);
});

test('perfLint: full image, script, font berlebih', () => {
  const d = v3();
  let l = E.perfLint(d);
  assert.ok(l.some((x) => /image_size "full"/.test(x.msg)));
  d.push({ id: 'h9', elType: 'widget', widgetType: 'html', settings: { html: '<script>alert(1)</script>' } });
  d[0].elements![0].elements![1].settings!.typography_font_family = 'Lato';
  d[0].elements![0].elements![2].settings!.typography_font_family = 'Poppins';
  l = E.perfLint(d);
  assert.ok(l.some((x) => x.level === 'block' && /script/.test(x.msg)));
  assert.ok(l.some((x) => /3 keluarga font/.test(x.msg)));
});

test('perfLint: <script> hanya lolos bila ada penanda allow-js (izin pengguna)', () => {
  const mk = (html: string) => [{ id: 'h1', elType: 'widget', widgetType: 'html', settings: { html } }];
  const blocked = (d: any[]) => E.perfLint(d).some((x) => x.level === 'block' && /script/.test(x.msg));
  assert.equal(blocked(mk('<script>1</script>')), true);
  assert.equal(blocked(mk('<!-- allow-js:pencarian-dokumen --><div></div><script>1</script>')), false);
  assert.equal(blocked(mk('<!-- allow-js: --><script>1</script>')), true); // alasan wajib diisi
});

test('normalizeText menyamakan entity & kutip keriting (wptexturize)', () => {
  assert.equal(E.normalizeText('<p>Don&#8217;t &amp; &#8220;Go&#8221;</p>'), `Don't & "Go"`);
});
