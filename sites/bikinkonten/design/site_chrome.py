"""Header/footer/menu/kategori BikinKontenAI via REST+Bridge. WPPW di env."""
import json, os, subprocess
B = 'https://www.bikinkontenai.id/wp-json'
def wp(m, p, b=None):
    c = ['curl', '-sS', '-m', '90', '-u', 'adminbikinkonten:' + os.environ['WPPW'], '-X', m, '-H', 'Content-Type: application/json', B + p]
    if b is not None: c += ['-d', json.dumps(b)]
    o = subprocess.check_output(c)
    try: return json.loads(o)
    except Exception: return o[:150]
AS = 'https://asosiasi.ai/'
cats = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'categories.json')))
# menu 7: Artikel(blog 344) · Kategori(818) · About(219) · Kontak(355)
for i, t, oid, n in [(347, 'Artikel', 344, 1), (349, 'Kategori', 818, 2), (351, 'About', 219, 3), (350, 'Kontak', 355, 4)]:
    print('menu', i, wp('PUT', f'/wp/v2/menu-items/{i}?_fields=id,title.raw', dict(title=t, menu_order=n, object='page', object_id=oid, type='post_type'))['title'])
for i in (348, 414): print('del', i, wp('DELETE', f'/wp/v2/menu-items/{i}?force=true&_fields=deleted'))
A = {'global-color-palette': {'palette': ['#6E1620', '#0B4A50', '#1B1A19', '#1B1A19', '#E6E0D3', '#F0ECE3', '#D6D0C0', '#1B1A19', '#1B1A19'], 'flag': False},
     'body-font-family': "'Inter', sans-serif", 'headings-font-family': "'Barlow Condensed', sans-serif", 'headings-text-transform': 'none',
     'header-html-1': '<a class="bk-logo" href="/"><span class="l1">bikinkonten<b>ai</b>.id</span><small>BY ASOSIASI AI INDONESIA</small></a>', 'header-html-2': 'Edukasi, bukan jasa',
     'header-button1-text': 'Pelajari di asosiasi.ai →', 'header-button1-link-option': {'url': AS, 'new_tab': '1', 'link_rel': 'noopener'},
     'footer-copyright-editor': '© [current_year] BikinKontenAI · Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia · Supported by <a href="https://asosiasi.ai/" target="_blank" rel="noopener">Asosiasi AI Indonesia — asosiasi.ai</a>',
     'ast-dynamic-archive-post-custom-title': 'Artikel', 'ast-dynamic-archive-post-banner-title-color': '#050505',
     'ast-dynamic-archive-post-horizontal-alignment': {'desktop': 'left', 'tablet': 'left', 'mobile': 'left'},
     'archive-post-sidebar-layout': 'right-sidebar', 'blog-grid': 2, 'blog-meta': ['category', 'date'], 'blog-excerpt-count': 22}
A['header-desktop-items'] = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': [], 'above_left_center': [], 'above_center': [], 'above_right_center': [], 'above_right': []},
    'primary': {'primary_left': ['html-1'], 'primary_left_center': [], 'primary_center': ['menu-1'], 'primary_right_center': [], 'primary_right': ['button-1']},
    'below': {'below_left': [], 'below_left_center': [], 'below_center': [], 'below_right_center': [], 'below_right': []}, 'flag': True}
A['header-mobile-items'] = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': [], 'above_center': [], 'above_right': []},
    'primary': {'primary_left': ['html-1'], 'primary_center': [], 'primary_right': ['mobile-trigger']}, 'below': {'below_left': [], 'below_center': [], 'below_right': []}, 'flag': True}
print('astra', wp('POST', '/claude/v1/theme-option', {'name': 'astra-settings', 'merge': A, 'nav_menu_locations': {'mobile_menu': 7}}))
def blk(i, h): return wp('PUT', f'/wp/v2/widgets/{i}?_fields=id', {'instance': {'raw': {'content': '<!-- wp:html -->\n' + h + '\n<!-- /wp:html -->'}}})
print(blk('block-7', '<p class="bia-fw">BikinKontenAI</p>'))
print(blk('block-8', '<p class="bia-fp">Pusat publikasi dan referensi AI untuk pembuatan konten digital.</p><p class="bia-fp">Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia.</p><p class="bia-micro">Edukasi, bukan jasa.</p>'))
print(blk('block-9', '<p class="bia-fh">Jelajahi</p><ul class="bia-fl"><li><a href="/blog/">Artikel</a></li><li><a href="/kategori/">Kategori</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Kontak</a></li></ul>'))
print(wp('DELETE', '/wp/v2/widgets/nav_menu-1?force=true&_fields=deleted'))
print(blk('block-10', '<p class="bia-fh">Kategori</p><ul class="bia-fl"><li><a href="/category/ai-untuk-tulisan-dan-copywriting/">Tulisan dan copywriting</a></li><li><a href="/category/ai-untuk-desain-grafis/">Desain grafis</a></li><li><a href="/category/ai-untuk-video-pendek/">Video pendek</a></li><li><a href="/category/ai-untuk-media-sosial/">Media sosial</a></li><li><a href="/category/etika-dan-hak-cipta/">Etika dan hak cipta</a></li></ul>'))
print(wp('DELETE', '/wp/v2/widgets/nav_menu-2?force=true&_fields=deleted'))
print(blk('block-11', '<p class="bia-fh">Supported by</p>'))
print(blk('block-12', '<p class="bia-fp"><a href="https://asosiasi.ai/" target="_blank" rel="noopener">Asosiasi AI Indonesia — asosiasi.ai</a></p><p class="bia-fp"><a href="https://asosiasi.ai/" target="_blank" rel="noopener">Pelajari Lebih Lanjut di asosiasi.ai →</a></p><p class="bia-fp"><a href="https://asosiasi.ai/" target="_blank" rel="noopener">Konsultasi melalui Asosiasi AI Indonesia →</a></p><p class="bia-micro">Website ini bersifat edukasi dan publikasi, bukan penyedia layanan. Tidak ada penawaran layanan atau produk.</p>'))
# sidebar: Cari, Kategori; buang widget bawaan lain
print(blk('block-2', '<!-- wp:heading {"level":2} --><h2 class="wp-block-heading">Cari</h2><!-- /wp:heading --><!-- wp:search {"label":"Cari artikel","showLabel":false,"placeholder":"Cari artikel…","buttonText":"Cari"} /-->'.replace('<!-- wp:html -->','')))
print(wp('PUT', '/wp/v2/widgets/block-6?_fields=id', {'instance': {'raw': {'content': '<!-- wp:heading {"level":2} --><h2 class="wp-block-heading">Kategori</h2><!-- /wp:heading --><!-- wp:categories {"showPostCounts":true} /-->'}}}))
for i in ('block-3', 'block-4', 'block-5'): print(wp('DELETE', f'/wp/v2/widgets/{i}?force=true&_fields=deleted'))
print('css', wp('POST', '/claude/v1/custom-css', {'css': open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome.css')).read()}))
print(wp('POST', '/wp/v2/settings', {'date_format': 'j F Y'}).get('date_format'))
print(wp('POST', '/claude/v1/flush'))
