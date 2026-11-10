"""AIAnalisaData: Home, Kategori, About, Kontak. Referensi: NOVACORE (panel bundar gradien biru muda, indigo + lime, kartu kaca, pil). Elementor Free native."""
import json, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent.parent / '_lib'))
import ek
INK, INDIGO, LIME, DARK, LAV, SKY, MUTE, LINE, WHITE = '#10141F', '#5B50E6', '#D8F25B', '#141A28', '#F2F3FC', '#DCE9FB', '#5B6275', '#E3E6F0', '#FFFFFF'
ek.HFAM, ek.HUP, ek.BFONT, ek.HW = 'Outfit', False, 'Inter', '600'
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = WHITE, INK, INDIGO, MUTE, LAV, 'Inter'
import ek2
from ek2 import *
LG = json.loads((D / 'logos.json').read_text()); MD = json.loads((D / 'media.json').read_text())
SITE, AS = 'https://www.aianalisadata.id', 'https://asosiasi.ai/'
WA, WAT, EM = 'https://wa.me/628111913553', '+62 8111913553', 'sekretariat@asosiasi.ai'
CATS = [('AI untuk analisis data', 'ai-untuk-analisis-data', 'fas fa-chart-pie', 'Memahami pola, tren, dan anomali data dengan bantuan AI.'), ('AI untuk visualisasi data', 'ai-untuk-visualisasi-data', 'fas fa-chart-bar', 'Menyajikan data menjadi grafik yang mudah dipahami.'),
        ('AI untuk dashboard', 'ai-untuk-dashboard', 'fas fa-tachometer-alt', 'Merancang dan membaca dashboard yang informatif.'), ('AI untuk Excel dan Sheets', 'ai-untuk-excel-dan-sheets', 'fas fa-table', 'Rumus, otomasi, dan analisis di spreadsheet.'),
        ('AI untuk business intelligence', 'ai-untuk-business-intelligence', 'fas fa-lightbulb', 'Business intelligence yang dibantu AI.'), ('AI untuk pengambilan keputusan', 'ai-untuk-pengambilan-keputusan', 'fas fa-compass', 'Dari data menjadi keputusan yang bisa dipertanggungjawabkan.'),
        ('AI untuk data cleaning', 'ai-untuk-data-cleaning', 'fas fa-broom', 'Membersihkan dan menyiapkan data sebelum dianalisis.'), ('Etika dan privasi data', 'etika-dan-privasi-data', 'fas fa-user-shield', 'Privasi, bias, dan tata kelola data yang beretika.'),
        ('Tren analisis data AI', 'tren-analisis-data-ai', 'fas fa-arrow-up', 'Perkembangan, riset, dan laporan seputar AI untuk analisis data.')]
def lg(k, w=220): return IMG(LG[k]['id'], LG[k]['source_url'], grey=False, width={'unit': 'px', 'size': w}, align='left')
def PH(k, h=300, r=22, **s): return IMG(MD[k]['id'], MD[k]['url'], grey=False, width={'unit': '%', 'size': 100}, image_border_radius=dim(r), **FIT(h), **s)
def HX(t, size=56, color=INK, tag='h2', lh=1.06, **s): return H(t, size, int(size * .78), int(size * .6), color=color, tag=tag, lh=lh, typography_letter_spacing={'unit': 'px', 'size': -(size * 0.025)}, **s)
def acc(t): return f'<span style="color:{INDIGO}">{t}</span>'
def TAG(t): return BADGE(f'<span style="color:{INDIGO}">●</span>&nbsp; {t}', INK, bgc='#FFFFFFCC', border=LINE)
def LAVC(children, w=None, r=24, pad=26, **s): return CARD(children, LAV, r, pad, w=w, **s)
def GL(children, w=None, r=22, pad=22, **s): return CARD(children, '#FFFFFF', r, pad, border='#FFFFFF', shadow='rgba(60,70,140,.10)', w=w, **s)
def PANEL(children, **s): return CARD(children, SKY, 34, 44, **grad('#CFE2FB', '#F7FAFF', 'linear', 170), **s)
def catline(name, slug, ic, desc, dark=False):
    fg, mu = (WHITE, '#B9C0D6') if dark else (INK, MUTE)
    return (CARD if dark else GL)([ICON(ic, LIME if dark else INDIGO, 26), H(name, 19, 18, 18, color=fg, tag='h3', lh=1.2), BODY(f'<p style="margin:0">{desc}</p>', 13, mu),
        W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{LIME if dark else INDIGO};font-weight:600">Pelajari →</a></p>', **typo('Inter', 13))], *(['#141A28', 22, 22] if dark else []), g=10)
def bars():
    hs = [26, 38, 30, 54, 66, 84]
    return C([C([], width={'unit': 'px', 'size': 14}, width_mobile={'unit': 'px', 'size': 14}, width_tablet={'unit': 'px', 'size': 14}, min_height=px(h), min_height_mobile=px(h), border_radius=dim(5), **grad(INDIGO if i < 5 else LIME, '#9C95F2' if i < 5 else '#EDFB9A', 'linear', 0)) for i, h in enumerate(hs)], flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_align_items='flex-end', flex_gap=gap(8), min_height=px(90), flex_wrap='nowrap', css_classes='ad-bars')
def band(title, sub=None):
    kids = [TAG('AIAnalisaData'), HX(title, 72, tag='h1', lh=1)]
    if sub: kids.append(BODY(f'<p style="margin:0">{sub}</p>', 18, MUTE))
    return SEC([PANEL(kids, g=18, padding=dim(64, 48), padding_mobile=dim(36, 22))], WHITE, pv=24, padding_mobile=dim(18, 14))

def build_home():
    S = []
    left = C([TAG('Referensi AI untuk analisis data'), HX('Pahami AI untuk ' + acc('Analisis Data.'), 70, tag='h1', lh=1.0),
              BODY('<p style="margin:0">AIAnalisaData menghadirkan artikel, panduan, studi kasus, dan tren tentang penggunaan AI dalam analisis data dan pengambilan keputusan.</p>', 17.5, MUTE),
              W('wp-widget-search', wp={'title': ''}, _css_classes='ad-search'),
              C([PILLBTN('Baca Artikel →', f'{SITE}/blog/', LIME, INK), PILLBTN('Jelajahi Kategori', f'{SITE}/kategori/', 'transparent', INK, border=INK)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12))], flex_gap=gap(20), **WIDTH(56))
    right = C([PH('hero', 470, 28), GL([MICRO('Kategori artikel', color=MUTE), H('9', 46, 40, 36, color=INK, tag='div', lh=1), bars(), BODY('<p style="margin:0">dari analisis data hingga etika & privasi</p>', 12, MUTE)], r=20, pad=20, g=6, width={'unit': 'px', 'size': 190}, width_mobile={'unit': '%', 'size': 100}, margin=dim(-150, 14, 0, 0), margin_mobile=dim(-90, 12, 0, 12), _flex_align_self='flex-end')], flex_gap=gap(0), **WIDTH(40))
    strip = ROW2([catline(*CATS[i]) for i in range(4)] + [CARD([ICON('fas fa-database', LIME, 26), H('Di mana data bertemu <span style="color:#D8F25B">keputusan.</span>', 22, 20, 20, color=WHITE, tag='h3', lh=1.15)], DARK, 22, 22, g=12)], g=14, flex_wrap='wrap', flex_justify_content='space-between', margin=dim(26, 0, 0, 0))
    for c in strip['elements']: c['settings'].update({'width': {'unit': '%', 'size': 19}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}})
    strip['settings']['flex_direction_tablet'] = 'row'; strip['settings']['flex_wrap'] = 'wrap'
    S.append(SEC([PANEL([ROW2([left, right], g=24, flex_justify_content='space-between', flex_align_items='center'), strip], padding=dim(48, 44), padding_mobile=dim(28, 18))], WHITE, pv=24, wpx=1260, padding_mobile=dim(14, 12)))
    # about
    S.append(SEC([ROW2([C([TAG('Tentang'), HX('Referensi AI untuk ' + acc('analisis data') + ' yang berlandaskan riset dan ' + acc('praktik') + '.', 46, tag='h2', lh=1.1)], flex_gap=gap(16), **WIDTH(58)),
                        C([BODY('<p style="margin:0">Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', 16, MUTE),
                           W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/about/" style="color:{INK};font-weight:600">Pelajari lebih lanjut tentang publikasi ini →</a></p>', **typo('Inter', 15))], flex_gap=gap(14), **WIDTH(36))], g=40, flex_justify_content='space-between', flex_align_items='flex-end')], WHITE, pv=70))
    # fakta
    def fc(children, bgc, w=24, **s): return CARD(children, bgc, 24, 26, g=8, **{'width': {'unit': '%', 'size': w}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}, **s)
    facts = [fc([ICON('fas fa-globe', INDIGO, 22), MICRO('Riset studi banding', color=MUTE), H('14', 50, 44, 40, color=INK, tag='div', lh=1), BODY('<p style="margin:0">yurisdiksi dikaji oleh Asosiasi AI Indonesia</p>', 14, MUTE)], LAV),
             fc([ICON('fas fa-chart-line', INK, 22), MICRO('Kategori artikel', color='#4E5A12'), H('9', 50, 44, 40, color=INK, tag='div', lh=1), BODY('<p style="margin:0">dari data cleaning hingga etika privasi</p>', 14, '#4E5A12')], LIME),
             C([PH('photo2', 250, 24), C([MICRO('Edukasi', color=WHITE), BODY('<p style="margin:0;color:#fff">bukan layanan atau produk</p>', 13, WHITE)], padding=dim(14, 18), border_radius=dim(16), margin=dim(-70, 0, 0, 14), **bg(INDIGO), width={'unit': 'px', 'size': 190})], flex_gap=gap(0), **{'width': {'unit': '%', 'size': 23}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}),
             fc([ICON('fas fa-book-open', INDIGO, 22), MICRO('Format konten', color=MUTE), H('5', 50, 44, 40, color=INK, tag='div', lh=1), BODY('<p style="margin:0">artikel, panduan, studi kasus, tren, dan etika</p>', 14, MUTE)], LAV)]
    S.append(SEC([RWRAP(facts, 18, flex_justify_content='space-between')], WHITE, pv=10))
    # kategori
    grid = RWRAP([catline(*CATS[i], dark=False) for i in range(4, 9)], 16, flex_justify_content='space-between', **WIDTH(62))
    for c in grid['elements']: c['settings'].update({'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}})
    grid['elements'].append(CARD([ICON('fas fa-arrow-right', INK, 26), H('Lihat semua 9 kategori', 22, 20, 20, color=INK, tag='h3', lh=1.2), PILLBTN('Jelajahi Kategori', f'{SITE}/kategori/', INK, LIME)], LIME, 22, 22, g=12, **{'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}))
    S.append(SEC([PANEL([ROW2([C([TAG('Kategori'), HX('Kategori artikel untuk setiap tahap ' + acc('analisis.'), 44, tag='h2', lh=1.08), BODY('<p style="margin:0">Dari menyiapkan data, membuat visualisasi dan dashboard, hingga mengambil keputusan dan menjaga etika.</p>', 15.5, MUTE),
                                      PILLBTN('Baca Artikel →', f'{SITE}/blog/', LIME, INK)], flex_gap=gap(16), **WIDTH(32)), grid], g=24, flex_justify_content='space-between')], padding=dim(40, 36), padding_mobile=dim(26, 16))], WHITE, pv=40, wpx=1260, padding_mobile=dim(14, 12)))
    # prinsip + foto
    rows = [('fas fa-book-open', 'Bersumber', 'Setiap klaim penting disertai sumber atau referensi.'), ('fas fa-balance-scale', 'Netral', 'Pembahasan tools bersifat informatif, bukan endorse.'), ('fas fa-user-shield', 'Beretika', 'Etika, privasi data, dan potensi misinformasi diperhatikan.')]
    S.append(SEC([ROW2([C([PH('case', 360, 26)], **WIDTH(40)), C([TAG('Prinsip editorial'), HX('Insight yang bisa ' + acc('dipertanggungjawabkan.'), 40, tag='h2', lh=1.1)] +
                  [GL([C([ICON(ic, INDIGO, 22)], width={'unit': 'px', 'size': 40}), C([H(t, 18, 17, 17, color=INK, tag='h3', lh=1.2), BODY(f'<p style="margin:0">{d}</p>', 13.5, MUTE)], flex_gap=gap(2), width={'unit': '%', 'size': 85}, width_tablet={'unit': '%', 'size': 85}, width_mobile={'unit': '%', 'size': 80})], r=18, pad=16, g=14, flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_align_items='center') for ic, t, d in rows], flex_gap=gap(14), **WIDTH(52))], g=34, flex_justify_content='space-between', flex_align_items='center')], WHITE, pv=70))
    # artikel contoh
    def ac(i, t): return CARD([PH(f'c{i+1}', 170, 18), MICRO('Contoh · segera hadir', color=INDIGO), H(t, 21, 20, 20, color=INK, tag='h3', lh=1.2), BODY(f'<p style="margin:0"><a href="{SITE}/blog/" style="color:{INDIGO};font-weight:600">Baca →</a></p>', 13.5)], LAV, 24, 16, g=10, **{'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}})
    S.append(SEC([TAG('Artikel terbaru'), HX('Bacaan terbaru', 44, tag='h2'), RWRAP([ac(i, t) for i, t in enumerate(['Judul artikel contoh pertama', 'Judul artikel contoh kedua', 'Judul artikel contoh ketiga'])], 20, flex_justify_content='space-between'), PILLBTN('Lihat semua artikel →', f'{SITE}/blog/', LIME, INK)], WHITE, pv=40))
    # identitas + CTA
    ID = ('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Materi berlandaskan buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
          f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{INDIGO}">Asosiasi AI Indonesia</a>, serta pembelajaran implementasi industri.')
    S.append(SEC([CARD([ROW2([C([lg('asosiasi', 230), HX('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 30, tag='h2', lh=1.15)], flex_gap=gap(18), **WIDTH(46)),
                              C([BODY(f'<p style="margin:0">{ID}</p>', 15.5, MUTE), C([PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai →', AS, LIME, INK, ext_=True), PILLBTN('Hubungi Asosiasi AI Indonesia', AS, 'transparent', INK, border=INK, ext_=True)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(10))], flex_gap=gap(16), **WIDTH(48))], g=36, flex_justify_content='space-between')], LAV, 30, 44, padding_mobile=dim(26, 18))], WHITE, pv=20))
    S.append(SEC([CARD([HX('Siap memahami data dengan lebih ' + acc('bertanggung jawab?'), 44, tag='h2', lh=1.1), BODY('<p style="margin:0">Konsultasi, kolaborasi, dan informasi program diarahkan ke Asosiasi AI Indonesia.</p>', 16, MUTE),
                       C([PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai →', AS, INK, LIME, ext_=True), PILLBTN('Konsultasi melalui Asosiasi AI Indonesia', AS, 'transparent', INK, border=INK, ext_=True)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12))],
                      LIME, 32, 54, g=16, **grad('#E4F77E', '#E3E4FB', 'linear', 120), padding_mobile=dim(28, 20))], WHITE, pv=30, padding_bottom_=0))
    return S

def build_kategori():
    cards = [catline(*CATS[i]) for i in range(9)]
    for c in cards: c['settings'].update({'width': {'unit': '%', 'size': 31.5}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}})
    return [band('Kategori', 'Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk analisis data.'), SEC([RWRAP(cards, 20, flex_justify_content='space-between')], WHITE, pv=50)]
def build_about():
    COPY = ('AIAnalisaData adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI untuk analisis data, visualisasi, dashboard, dan pengambilan keputusan berbasis data. Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
            f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{INDIGO}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
    LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.', 'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
    il = W('icon-list', icon_list=[{'_id': f'l{i}', 'text': t, 'selected_icon': {'value': 'fas fa-check-circle', 'library': 'fa-solid'}} for i, t in enumerate(LAND)], icon_color=INDIGO, text_color=INK, **typo('Inter', 15))
    return [band('About', 'Tentang Publikasi Ini'), SEC([ROW2([C([BODY(f'<p style="margin:0">{COPY}</p>', 18, INK), lg('asosiasi', 260), PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai →', AS, LIME, INK, ext_=True)], flex_gap=gap(20), **WIDTH(56)),
            LAVC([MICRO('Landasan materi', color=INDIGO), il, BODY('<p style="margin:0">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', 14, MUTE)], w=40, pad=32)], g=36, flex_justify_content='space-between')], WHITE, pv=50)]
def build_kontak():
    def row(ic, label, val, url): return C([C([ICON(ic, INDIGO, 22)], width={'unit': 'px', 'size': 34}, width_mobile={'unit': 'px', 'size': 34}), C([MICRO(label, color=MUTE), W('text-editor', editor=f'<p style="margin:0"><a href="{url}" target="_blank" rel="noopener" style="color:{INK}">{val}</a></p>', **typo('Outfit', 26, 24, 22, weight='600', lh=1.2))], flex_gap=gap(2))],
                                     flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_gap=gap(14), flex_align_items='center', padding=dim(14, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=LINE)
    return [band('Kontak', 'Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.'),
            SEC([ROW2([C([BODY('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', 18, INK), lg('asosiasi', 260), PILLBTN('Konsultasi melalui Asosiasi AI Indonesia →', AS, LIME, INK, ext_=True)], flex_gap=gap(20), **WIDTH(50)),
                       LAVC([row('fab fa-whatsapp', 'WhatsApp', WAT, WA), row('fas fa-envelope', 'Email', EM, 'mailto:' + EM), row('fas fa-globe', 'Website', 'asosiasi.ai', AS), BODY('<p style="margin:10px 0 0">Usulan artikel atau ide: kirim lewat WhatsApp atau email di atas.</p>', 14, MUTE)], w=46, pad=32)], g=36, flex_justify_content='space-between')], WHITE, pv=50)]
def save(name, S): (D / f'{name}_sections.json').write_text(json.dumps(S, ensure_ascii=False)); print(name, len(S))
if __name__ == '__main__':
    save('home', build_home()); save('kategori', build_kategori()); save('about', build_about()); save('kontak', build_kontak())
