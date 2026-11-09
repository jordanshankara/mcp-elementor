"""Pasang logo (header lockup + logo Asosiasi AI) dan kontak resmi (WA, email) — BikinKontenAI. Perlu WPPW."""
import json, os, subprocess
B = 'https://www.bikinkontenai.id/wp-json'; D = os.path.dirname(os.path.abspath(__file__))
LG = json.load(open(D + '/logos.json'))
def wp(m, p, b=None):
    c = ['curl', '-sS', '-m', '90', '-u', 'adminbikinkonten:' + os.environ['WPPW'], '-X', m, '-H', 'Content-Type: application/json', B + p]
    if b is not None: c += ['-d', json.dumps(b)]
    o = subprocess.check_output(c)
    try: return json.loads(o)
    except Exception: return o[:150]
hd = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': [], 'above_left_center': [], 'above_center': [], 'above_right_center': [], 'above_right': []},
      'primary': {'primary_left': ['logo'], 'primary_left_center': [], 'primary_center': ['menu-1'], 'primary_right_center': [], 'primary_right': ['button-1']}, 'below': {'below_left': [], 'below_left_center': [], 'below_center': [], 'below_right_center': [], 'below_right': []}, 'flag': True}
hm = {'popup': {'popup_content': ['mobile-menu']}, 'above': {'above_left': [], 'above_center': [], 'above_right': []}, 'primary': {'primary_left': ['logo'], 'primary_center': [], 'primary_right': ['mobile-trigger']}, 'below': {'below_left': [], 'below_center': [], 'below_right': []}, 'flag': True}
A = {'header-desktop-items': hd, 'header-mobile-items': hm, 'ast-header-responsive-logo-width': {'desktop': 230, 'tablet': 190, 'mobile': 160},
     'display-site-title-responsive': {'desktop': False, 'tablet': False, 'mobile': False}, 'display-site-tagline-responsive': {'desktop': False, 'tablet': False, 'mobile': False}}
print(wp('POST', '/claude/v1/theme-option', {'name': 'astra-settings', 'merge': A, 'theme_mods': {'custom_logo': LG['bikinkonten']['id']}}))
WA, WAT, EM = 'https://wa.me/628111913553', '+62 8111913553', 'sekretariat@asosiasi.ai'
def blk(i, h): return wp('PUT', f'/wp/v2/widgets/{i}?_fields=id', {'instance': {'raw': {'content': '<!-- wp:html -->\n' + h + '\n<!-- /wp:html -->'}}})
logo = LG['asosiasi_putih']['source_url']
print(blk('block-11', '<p class="bia-fh">Supported by</p>'))
print(blk('block-12', f'<a href="https://asosiasi.ai/" target="_blank" rel="noopener"><img src="{logo}" alt="Asosiasi AI Indonesia" width="220" style="max-width:220px;height:auto;margin:0 0 14px;display:block"></a>'
    '<p class="bia-fp"><a href="https://asosiasi.ai/" target="_blank" rel="noopener">Pelajari Lebih Lanjut di asosiasi.ai →</a></p>'
    '<p class="bia-fp"><a href="https://asosiasi.ai/" target="_blank" rel="noopener">Konsultasi melalui Asosiasi AI Indonesia →</a></p>'
    f'<p class="bia-fp">WhatsApp: <a href="{WA}" target="_blank" rel="noopener">{WAT}</a><br>Email: <a href="mailto:{EM}">{EM}</a></p>'
    '<p class="bia-micro">Website ini bersifat edukasi dan publikasi, bukan penyedia layanan.</p>'))
print(wp('POST', '/claude/v1/flush'))
