"""buatiklan: logo header (lockup), logo Asosiasi AI di footer, kontak resmi, halaman Kontak (#355). Perlu WPPW."""
import json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '..', '..', '_lib'))
import ek
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = '#ECE7DB', '#0B0B0B', '#D9291C', '#4A463E', '#D8CFB3', 'Inter'
from ek import *
LG = json.load(open(D + '/logos.json')); B = 'https://buatiklanai.id/wp-json'; AS = 'https://asosiasi.ai/'
WA, WAT, EM = 'https://wa.me/628111913553', '+62 8111913553', 'sekretariat@asosiasi.ai'
def wp(m, p, b=None):
    c = ['curl', '-sS', '-m', '90', '-u', 'adminbuatiklan:' + os.environ['WPPW'], '-X', m, '-H', 'Content-Type: application/json', B + p]
    if b is not None: c += ['-d', json.dumps(b)]
    o = subprocess.check_output(c)
    try: return json.loads(o)
    except Exception: return o[:150]
hd = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': ['html-1'], 'above_left_center': [], 'above_center': [], 'above_right_center': [], 'above_right': ['html-2']},
      'primary': {'primary_left': ['logo'], 'primary_left_center': [], 'primary_center': ['menu-1'], 'primary_right_center': [], 'primary_right': ['button-1']}, 'below': {'below_left': [], 'below_left_center': [], 'below_center': [], 'below_right_center': [], 'below_right': []}, 'flag': True}
print(wp('POST', '/claude/v1/theme-option', {'name': 'astra-settings', 'merge': {'header-desktop-items': hd, 'ast-header-responsive-logo-width': {'desktop': 230, 'tablet': 190, 'mobile': 160},
      'display-site-title-responsive': {'desktop': False, 'tablet': False, 'mobile': False}, 'display-site-tagline-responsive': {'desktop': False, 'tablet': False, 'mobile': False}}, 'theme_mods': {'custom_logo': LG['buatiklan']['id']}}))
def blk(i, h): return wp('PUT', f'/wp/v2/widgets/{i}?_fields=id', {'instance': {'raw': {'content': '<!-- wp:html -->\n' + h + '\n<!-- /wp:html -->'}}})
print(blk('block-12', f'<a href="{AS}" target="_blank" rel="noopener"><img src="{LG["asosiasi"]["source_url"]}" alt="Asosiasi AI Indonesia" width="210" style="max-width:210px;height:auto;margin:0 0 14px;display:block"></a>'
    f'<p class="bia-fp">Supported by <a href="{AS}" target="_blank" rel="noopener">Asosiasi AI Indonesia — asosiasi.ai</a></p><p class="bia-fp"><a href="{AS}" target="_blank" rel="noopener">Pelajari Lebih Lanjut di asosiasi.ai →</a></p>'
    f'<p class="bia-fp">WhatsApp: <a href="{WA}" target="_blank" rel="noopener">{WAT}</a><br>Email: <a href="mailto:{EM}">{EM}</a></p><p class="bia-micro">Semua konten bersifat edukasi dan publikasi. Tidak ada penawaran layanan, produk, atau harga.</p>'))
# halaman Kontak
def ln(label, val, url): return C([MICRO(label, color=MUTE), W('text-editor', editor=f'<p style="margin:0"><a href="{url}" target="_blank" rel="noopener" style="color:#0B0B0B">{val}</a></p>', **typo('Anton', 34, 28, 24, lh=1, up=True))], padding=dim(14, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=INK, flex_gap=gap(4))
logo = IMG(LG['asosiasi']['id'], LG['asosiasi']['source_url'], grey=False, width={'unit': 'px', 'size': 260}, align='left')
S = [ROW([C([H('Kontak', 19, 20, 24, tag='h1', unit='vw', lh=.88)], padding=dim(26, 24, 8, 24), padding_mobile=dim(18, 14, 6, 14))], tablet_col=False),
     ROW([CELL([MICRO('Hubungi', color=MUTE), TXT('<p style="margin:0;font-size:20px">Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.</p>', size=20),
                TXT('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', size=15), logo,
                C([BTN('Buka asosiasi.ai →', AS, link={'url': AS, 'is_external': 'on', 'nofollow': ''})], margin=dim(8, 0, 0, 0))], w=55),
          CELL([MICRO('Kontak resmi Asosiasi AI Indonesia', color=MUTE), ln('WhatsApp', WAT, WA), ln('Email', EM, 'mailto:' + EM), ln('Website', 'asosiasi.ai', AS),
                TXT('<p style="margin:12px 0 0">Konsultasi, kolaborasi, dan informasi program diarahkan ke asosiasi.ai. Tidak ada penawaran layanan, produk, atau harga di situs ini.</p>', size=14)], w=45, right=False)], tablet_col=True, border_width=bw(0))]
for s in S: s['settings'].setdefault('background_background', 'classic'); s['settings'].setdefault('background_color', '#ECE7DB')
json.dump(S, open(D + '/kontak_sections.json', 'w'), ensure_ascii=False)
print(subprocess.check_output(['python3', D + '/push_draft.py', '355', D + '/kontak_sections.json'])[:40])
print(wp('POST', '/wp/v2/pages/355?_fields=id,link,title.raw', {'title': 'Kontak', 'meta': {'theme-transparent-header-meta': 'disabled', 'site-post-title': 'disabled', 'ast-site-content-layout': 'full-width-container', 'site-content-layout': 'plain-container', 'site-content-style': 'unboxed', 'site-sidebar-layout': 'no-sidebar'}}))
print(wp('POST', '/claude/v1/purge')); print(wp('POST', '/claude/v1/flush'))
