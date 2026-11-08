"""Header/footer/menu Astra untuk BuatIklanAI lewat REST + Bridge. Jalankan dengan WPPW di env."""
import json, os, subprocess
def wp(m, p, b=None):
    c = ['curl', '-sS', '-m', '90', '-u', 'adminbuatiklan:' + os.environ['WPPW'], '-X', m, '-H', 'Content-Type: application/json', 'https://buatiklanai.id/wp-json' + p]
    if b is not None: c += ['-d', json.dumps(b)]
    o = subprocess.check_output(c)
    try: return json.loads(o)
    except Exception: return o[:200]
cfg = [(347, 'Artikel', dict(object='page', object_id=344, type='post_type'), 1), (351, 'Panduan', dict(object='category', object_id=20, type='taxonomy'), 2),
       (350, 'Studi Kasus', dict(object='category', object_id=21, type='taxonomy'), 3), (348, 'Tren & Riset', dict(object='category', object_id=19, type='taxonomy'), 4),
       (349, 'Tentang', dict(object='page', object_id=219, type='post_type'), 5)]
for i, t, o, n in cfg: print('menu', i, wp('PUT', f'/wp/v2/menu-items/{i}?_fields=id,title.raw', dict(title=t, menu_order=n, **o)))
print('menu del 414', wp('DELETE', '/wp/v2/menu-items/414?force=true&_fields=deleted'))
A = {'global-color-palette': {'palette': ['#D9291C', '#0B0B0B', '#0B0B0B', '#0B0B0B', '#ECE7DB', '#ECE7DB', '#E4DFD2', '#0B0B0B', '#0B0B0B'], 'flag': False},
     'body-font-family': "'Inter', sans-serif", 'headings-font-family': "'Anton', sans-serif", 'headings-text-transform': 'uppercase',
     'header-html-1': 'Dikelola oleh <a href="https://asosiasi.ai" target="_blank" rel="noopener">Asosiasi AI Indonesia</a>', 'header-html-2': 'Referensi, bukan jasa',
     'header-button1-text': 'Baca artikel', 'header-button1-link-option': {'url': '/blog/', 'new_tab': '', 'link_rel': ''},
     'footer-copyright-editor': '© [current_year] BuatIklanAI · Edukasi, bukan jasa · Dikelola oleh <a href="https://asosiasi.ai" target="_blank" rel="noopener">Asosiasi AI Indonesia</a>'}
A['header-desktop-items'] = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': ['html-1'], 'above_left_center': [], 'above_center': [], 'above_right_center': [], 'above_right': ['html-2']},
      'primary': {'primary_left': ['logo'], 'primary_left_center': [], 'primary_center': ['menu-1'], 'primary_right_center': [], 'primary_right': ['button-1']},
      'below': {'below_left': [], 'below_left_center': [], 'below_center': [], 'below_right_center': [], 'below_right': []}, 'flag': True}
A['header-mobile-items'] = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': ['html-1'], 'above_center': [], 'above_right': []},
      'primary': {'primary_left': ['logo'], 'primary_center': [], 'primary_right': ['mobile-trigger']}, 'below': {'below_left': [], 'below_center': [], 'below_right': []}, 'flag': True}
print('astra', wp('POST', '/claude/v1/theme-option', {'name': 'astra-settings', 'merge': A, 'nav_menu_locations': {'mobile_menu': 6}}))
def blk(i, html): return wp('PUT', f'/wp/v2/widgets/{i}?_fields=id', {'instance': {'raw': {'content': '<!-- wp:html -->\n' + html + '\n<!-- /wp:html -->'}}})
print(blk('block-7', '<p class="bia-fw">BuatIklanAI</p>'))
print(blk('block-8', '<p class="bia-fp">Pusat publikasi dan referensi AI untuk periklanan, digital marketing, dan komunikasi brand.</p><p class="bia-micro">Edukasi, bukan jasa.</p>'))
print(blk('block-9', '<p class="bia-fh">Jelajahi</p><ul class="bia-fl"><li><a href="/blog/">Artikel</a></li><li><a href="/category/panduan/">Panduan</a></li><li><a href="/category/studi-kasus/">Studi Kasus</a></li><li><a href="/category/tren-dan-laporan-industri/">Tren dan riset</a></li><li><a href="/about/">Tentang</a></li></ul>'))
print(wp('DELETE', '/wp/v2/widgets/nav_menu-1?force=true&_fields=deleted'))
print(blk('block-10', '<p class="bia-fh">Topik</p><ul class="bia-fl"><li><a href="/category/ai-untuk-riset-pasar/">Riset pasar</a></li><li><a href="/category/ai-untuk-iklan-digital/">Iklan digital</a></li><li><a href="/category/ai-untuk-seo-dan-geo/">SEO dan GEO</a></li><li><a href="/category/ai-untuk-media-sosial/">Media sosial</a></li><li><a href="/category/etika-dan-kepatuhan/">Etika dan kepatuhan</a></li></ul>'))
print(wp('DELETE', '/wp/v2/widgets/nav_menu-2?force=true&_fields=deleted'))
print(blk('block-11', '<p class="bia-fh">Dikelola oleh</p>'))
print(blk('block-12', '<p class="bia-fp"><a href="https://asosiasi.ai" target="_blank" rel="noopener">Asosiasi AI Indonesia</a></p><p class="bia-micro">Semua konten bersifat edukasi dan publikasi. Tidak ada penawaran jasa atau produk.</p>'))
print('css', wp('POST', '/claude/v1/custom-css', {'css': open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome.css')).read()}))
print('flush', wp('POST', '/claude/v1/flush'))
