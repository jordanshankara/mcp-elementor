"""AISolusiKeamanan: Home, Kategori, About, Kontak. Referensi: AgentAI (gelap, panel bundar, kaca, pil, glow merah) + palet Crimson Depth / Warm Sand / Soft Pearl / Obsidian Black."""
import json, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent.parent / '_lib'))
import ek
OBS, OBS2, LINE, CRIM, CRIM_L, SAND, PEARL, MUTE = '#161616', '#1E1E1E', '#2E2E2E', '#710014', '#C4283F', '#B38F6F', '#F2F1ED', '#A9A59E'
ek.HFAM, ek.HUP, ek.BFONT, ek.HW = 'Instrument Sans', False, 'Inter', '500'
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = OBS, PEARL, CRIM, MUTE, LINE, 'Inter'
import ek2
from ek2 import *
import latest
LATEST = latest.load(D)
LG = json.loads((D / 'logos.json').read_text())
MD = json.loads((D / 'media.json').read_text())
def PHOTO(k, h=220, r=24, **s): return IMG(MD[k]['id'], MD[k]['url'], grey=False, width={'unit': '%', 'size': 100}, image_border_radius=dim(r), **FIT(h), css_filters_css_filter='custom', css_filters_brightness=px(88), css_filters_saturate=px(85), **s)
SITE, AS = 'https://aisolusikeamanan.id', 'https://asosiasi.ai/'
WA, WAT, EM = 'https://wa.me/628111913553', '+62 8111913553', 'sekretariat@asosiasi.ai'
CATS = [('AI untuk deteksi ancaman', 'ai-untuk-deteksi-ancaman'), ('AI untuk keamanan siber', 'ai-untuk-keamanan-siber'), ('AI untuk perlindungan data', 'ai-untuk-perlindungan-data'), ('AI untuk deteksi fraud', 'ai-untuk-deteksi-fraud'),
        ('AI untuk phishing dan malware', 'ai-untuk-phishing-dan-malware'), ('AI untuk SOC', 'ai-untuk-soc'), ('AI untuk tata kelola risiko', 'ai-untuk-tata-kelola-risiko'), ('Etika dan kepatuhan', 'etika-dan-kepatuhan'), ('Tren keamanan AI', 'tren-keamanan-ai')]
def lg(k, w=220): return IMG(LG[k]['id'], LG[k]['source_url'], grey=False, width={'unit': 'px', 'size': w}, align='left')
def HS(t, size=56, color=PEARL, tag='h2', lh=1.05, **s): return H(t, size, int(size * .78), int(size * .6), color=color, tag=tag, lh=lh, typography_font_weight='500', typography_letter_spacing={'unit': 'px', 'size': -(size * 0.03)}, **s)
def GLASS(children, r=26, pad=26, w=None, **s):
    return CARD(children, OBS2, r, pad, border=LINE, w=w, **grad('#242424', '#161616', 'linear', 160), **s)
def DOT(text): return BADGE(f'<span style="color:{CRIM_L}">●</span>&nbsp; {text}', PEARL, bgc='#FFFFFF0D', border='#FFFFFF22')
def band(title, sub=None):
    kids = [DOT('AISolusiKeamanan'), HS(title, 80, tag='h1', lh=1)]
    if sub: kids.append(BODY(f'<p style="margin:0">{sub}</p>', 18, '#CFCBC3'))
    return SEC(kids, None, pv=96, wpx=1180, **grad(OBS, CRIM, 'radial', pos='top right', background_color_stop={'unit': '%', 'size': 0}, background_color_b_stop={'unit': '%', 'size': 0}))
def glow(): return {'background_background': 'gradient', 'background_color': '#4A0010', 'background_color_b': OBS, 'background_gradient_type': 'radial', 'background_gradient_position': 'top right', 'background_color_stop': {'unit': '%', 'size': 0}, 'background_color_b_stop': {'unit': '%', 'size': 62}}

def build_home():
    S = []
    FACT = [('14', 'yurisdiksi studi banding'), ('9', 'kategori artikel'), ('Edukasi', 'bukan layanan atau produk')]
    left = C([DOT('Referensi AI untuk keamanan siber & data'),
              HS('Pahami AI untuk <span style="color:#C4283F">Keamanan Siber</span> dan Data.', 76, tag='h1', lh=1.0),
              BODY('<p style="margin:0">AISolusiKeamanan menghadirkan artikel, panduan, studi kasus, dan tren tentang penggunaan AI dalam keamanan siber dan perlindungan data.</p>', 18, '#CFCBC3'),
              W('wp-widget-search', wp={'title': ''}, _css_classes='sk-search'),
              C([PILLBTN('Baca Artikel', f'{SITE}/blog/', CRIM, PEARL, hover_bg=CRIM_L), PILLBTN('Jelajahi Kategori', f'{SITE}/kategori/', '#FFFFFF14', PEARL, border='#FFFFFF2E', hover_bg=CRIM)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12)),
              ROW2([GLASS([H(n, 34, 30, 28, color=PEARL, tag='div', lh=1, typography_font_weight='500'), BODY(f'<p style="margin:0">{t}</p>', 12.5, MUTE)], 18, 18, g=4, **{'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 31}, 'width_mobile': {'unit': '%', 'size': 100}}) for n, t in FACT], g=12, tablet_row=True, flex_justify_content='space-between', margin=dim(18, 0, 0, 0))],
             flex_gap=gap(22), **WIDTH(58))
    orb = C([C([], width={'unit': 'px', 'size': 300}, min_height=px(300), border_radius=dim(150), **grad('#B0112B', '#2A0008', 'radial', pos='center center', background_color_stop={'unit': '%', 'size': 0}, background_color_b_stop={'unit': '%', 'size': 72}), box_shadow_box_shadow_type='yes', box_shadow_box_shadow={'horizontal': 0, 'vertical': 0, 'blur': 120, 'spread': 10, 'color': 'rgba(196,40,63,.45)'}),
             GLASS([MICRO('Kategori artikel', color=MUTE), H('9', 64, 56, 48, color=PEARL, tag='div', lh=1, typography_font_weight='500'), BODY('<p style="margin:0">Deteksi ancaman, perlindungan data, fraud, phishing dan malware, SOC, tata kelola risiko, etika, dan tren.</p>', 13.5, '#CFCBC3')], 22, 22, g=6, **WIDTH(70), _flex_align_self='flex-end')],
            **WIDTH(40), flex_align_items='center', flex_gap=gap(-40))
    S.append(SEC([ROW2([left, orb], g=30, flex_justify_content='space-between', flex_align_items='center')], None, pv=110, **glow(), padding_mobile=dim(56, 18)))
    # pernyataan
    S.append(SEC([H('Kami menyajikan <span style="color:#C4283F">referensi</span> tentang AI untuk keamanan siber — dari <span style="color:#C4283F">deteksi ancaman</span> dan perlindungan data hingga <span style="color:#C4283F">tata kelola risiko</span> — berlandaskan riset dan praktik.', 44, 34, 28, color=PEARL, tag='h2', lh=1.18, typography_font_weight='500')], OBS, pv=90, wpx=1080))
    # dua panel
    ID = ('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Materi berlandaskan buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
          f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{SAND}">Asosiasi AI Indonesia</a>, serta pembelajaran implementasi industri.')
    pl = GLASS([DOT('Landasan materi'), HS('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 38, tag='h2', lh=1.1), BODY(f'<p style="margin:0">{ID}</p>', 15.5, '#CFCBC3'), lg('asosiasi_putih', 230),
                C([PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai', AS, CRIM, PEARL, ext_=True, hover_bg=CRIM_L)], flex_direction='row')], 30, 38, g=18, **WIDTH(56), flex_justify_content='space-between')
    pr = C([C([PHOTO('hero', 230, 26), MICRO('Foto: Tima Miroshnichenko / Pexels', color=MUTE)], flex_gap=gap(6)), GLASS([MICRO('Riset studi banding', color=MUTE), H('14+', 84, 64, 52, color=PEARL, tag='div', lh=1, typography_font_weight='500'), BODY('<p style="margin:0">yurisdiksi dikaji oleh Asosiasi AI Indonesia sebagai landasan publikasi.</p>', 14, '#CFCBC3')], 28, 30, g=6),
            GLASS([H('“Stay Human, Stay in Charge.”', 30, 26, 24, color=PEARL, tag='div', lh=1.15, typography_font_weight='500'), BODY('<p style="margin:0">Transformasi AI di Korporasi — buku Dian Martin, Ketua Umum Asosiasi AI Indonesia.</p>', 14, MUTE)], 28, 30, g=10)], flex_gap=gap(20), **WIDTH(40))
    S.append(SEC([ROW2([pl, pr], g=20, flex_justify_content='space-between')], OBS, pv=40))
    # kategori
    items = [GLASS([MICRO(f'{i+1:02d}', color=SAND), H(n, 25, 24, 24, color=PEARL, tag='h3', lh=1.15, typography_font_weight='500', link={'url': f'{SITE}/category/{slug}/'}),
                    W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{CRIM_L}">Lihat artikel →</a></p>', **typo('Inter', 13, weight='600'))], 22, 24, g=10,
                   **{'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}) for i, (n, slug) in enumerate(CATS)]
    S.append(SEC([DOT('Kategori'), HS('Kategori Artikel', 60, tag='h2'), BODY('<p style="margin:0">Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk keamanan digital.</p>', 17, '#CFCBC3'), RWRAP(items, 20, flex_justify_content='space-between')], OBS, pv=90))
    # artikel terbaru
    def ac(t, k): return GLASS([PHOTO(k, 160, 16), MICRO('Contoh · segera hadir', color=SAND), H(t, 26, 24, 24, color=PEARL, tag='h3', lh=1.15, typography_font_weight='500'),
                              W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/blog/" style="color:{CRIM_L}">Baca →</a></p>', **typo('Inter', 13, weight='600'))], 22, 18, g=12, **{'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}})
    def ac2(p): return GLASS([POSTIMG(p, 170, 16, '#2A0008'), MICRO(p['date'], color=SAND), H(p['title'], 24, 22, 22, color=PEARL, tag='h3', lh=1.2, typography_font_weight='500', link={'url': p['url']}),
                              W('text-editor', editor=f'<p style="margin:0"><a href="{p["url"]}" style="color:{CRIM_L}">Baca →</a></p>', **typo('Inter', 13, weight='600'))], 22, 18, g=12, **{'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}})
    S.append(SEC([DOT('Artikel terbaru'), HS('Bacaan Terbaru', 56, tag='h2'), RWRAP([ac2(p) for p in LATEST] if LATEST else [ac(t, f'c{i+1}') for i, t in enumerate(['Judul artikel contoh pertama', 'Judul artikel contoh kedua', 'Judul artikel contoh ketiga'])], 20, flex_justify_content='space-between'), PILLBTN('Lihat semua artikel', f'{SITE}/blog/', '#FFFFFF14', PEARL, border='#FFFFFF2E', hover_bg=CRIM)], OBS, pv=60))
    # CTA
    S.append(SEC([CARD([HS('Pelajari lebih lanjut di <span style="color:#B38F6F">asosiasi.ai</span>', 52, tag='h2'), BODY('<p style="margin:0">Konsultasi, kolaborasi, dan informasi program diarahkan ke Asosiasi AI Indonesia.</p>', 17, '#E6D9D9'),
                       C([PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai', AS, PEARL, CRIM, ext_=True, hover_bg=SAND), PILLBTN('Konsultasi melalui Asosiasi AI Indonesia', AS, 'transparent', PEARL, border='#FFFFFF66', ext_=True, hover_bg=CRIM_L)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12))],
                      CRIM, 32, 56, g=18, **grad('#8A0A22', '#3A0009', 'linear', 150))], OBS, pv=50, padding_mobile=dim(30, 18)))
    return S

def build_kategori():
    items = [GLASS([MICRO(f'{i+1:02d}', color=SAND), H(n, 28, 26, 26, color=PEARL, tag='h3', lh=1.15, typography_font_weight='500', link={'url': f'{SITE}/category/{slug}/'}),
                    W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{CRIM_L}">Lihat artikel →</a></p>', **typo('Inter', 13, weight='600'))], 22, 26, g=10,
                   **{'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}) for i, (n, slug) in enumerate(CATS)]
    return [band('Kategori', 'Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk keamanan digital.'), SEC([RWRAP(items, 20, flex_justify_content='space-between')], OBS, pv=70)]
def build_about():
    COPY = ('AISolusiKeamanan adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI untuk keamanan siber, data, dan risiko digital. Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
            f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{SAND}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
    LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.', 'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
    il = W('icon-list', icon_list=[{'_id': f'l{i}', 'text': t, 'selected_icon': {'value': 'fas fa-check-circle', 'library': 'fa-solid'}} for i, t in enumerate(LAND)], icon_color=CRIM_L, text_color=PEARL, **typo('Inter', 15, weight='400'))
    return [band('About', 'Tentang Publikasi Ini'), SEC([ROW2([C([BODY(f'<p style="margin:0">{COPY}</p>', 18, '#E6E3DC'), lg('asosiasi_putih', 250), PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai', AS, CRIM, PEARL, ext_=True, hover_bg=CRIM_L)], flex_gap=gap(22), **WIDTH(56)),
            GLASS([MICRO('Landasan materi', color=SAND), il, BODY('<p style="margin:0">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', 14, MUTE)], 26, 32, **WIDTH(40))], g=36, flex_justify_content='space-between')], OBS, pv=70)]
def build_kontak():
    def row(ic, label, val, url): return C([C([ICON(ic, CRIM_L, 22)], width={'unit': 'px', 'size': 34}, width_mobile={'unit': 'px', 'size': 34}), C([MICRO(label, color=SAND), W('text-editor', editor=f'<p style="margin:0"><a href="{url}" target="_blank" rel="noopener" style="color:{PEARL}">{val}</a></p>', **typo('Instrument Sans', 30, 26, 24, weight='600', lh=1.15))], flex_gap=gap(2))], flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_gap=gap(14), flex_align_items='center', padding=dim(14, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=LINE)
    return [band('Kontak', 'Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.'),
            SEC([ROW2([C([BODY('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', 18, '#E6E3DC'), lg('asosiasi_putih', 250), PILLBTN('Konsultasi melalui Asosiasi AI Indonesia', AS, CRIM, PEARL, ext_=True, hover_bg=CRIM_L)], flex_gap=gap(22), **WIDTH(50)),
                       GLASS([row('fab fa-whatsapp', 'WhatsApp', WAT, WA), row('fas fa-envelope', 'Email', EM, 'mailto:' + EM), row('fas fa-globe', 'Website', 'asosiasi.ai', AS), BODY('<p style="margin:10px 0 0">Usulan artikel atau ide: kirim lewat WhatsApp atau email di atas.</p>', 14, MUTE)], 26, 32, **WIDTH(46))], g=36, flex_justify_content='space-between')], OBS, pv=70)]
def save(name, S): (D / f'{name}_sections.json').write_text(json.dumps(S, ensure_ascii=False)); print(name, len(S))
if __name__ == '__main__':
    save('home', build_home()); save('kategori', build_kategori()); save('about', build_about()); save('kontak', build_kontak())
