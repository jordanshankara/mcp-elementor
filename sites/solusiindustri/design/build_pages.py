"""AISolusiIndustri: Home, Kategori, About, Kontak (Elementor Free native). Referensi: tema korporat industri (Machvex): putih/abu, navy, oranye."""
import json, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent.parent / '_lib'))
import ek
NAVY, NAVY2, ORANGE, GREY, MUTE, WHITE = '#0D1527', '#16213D', '#F47A1F', '#F1F1F1', '#5F6A7D', '#FFFFFF'
ek.HFAM, ek.HUP, ek.BFONT = 'Manrope', False, 'Manrope'
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = WHITE, NAVY, ORANGE, MUTE, GREY, 'Manrope'
import ek2
from ek2 import *
LG = json.loads((D / 'logos.json').read_text())
SITE, AS = 'https://www.aisolusiindustri.id', 'https://asosiasi.ai/'
WA, WAT, EM = 'https://wa.me/628111913553', '+62 8111913553', 'sekretariat@asosiasi.ai'
CATS = [('AI untuk manufaktur', 'ai-untuk-manufaktur', 'fas fa-industry', 'Pemanfaatan AI pada proses produksi dan lini manufaktur.'), ('AI untuk operasional', 'ai-untuk-operasional', 'fas fa-cogs', 'AI dalam perencanaan, penjadwalan, dan operasional harian.'),
        ('AI untuk supply chain', 'ai-untuk-supply-chain', 'fas fa-truck', 'Peramalan, logistik, dan rantai pasok yang dibantu AI.'), ('AI untuk quality control', 'ai-untuk-quality-control', 'fas fa-clipboard-check', 'Inspeksi dan pengendalian kualitas berbasis AI.'),
        ('AI untuk maintenance', 'ai-untuk-maintenance', 'fas fa-tools', 'Pemeliharaan prediktif dan pemantauan kondisi mesin.'), ('AI untuk produktivitas', 'ai-untuk-produktivitas', 'fas fa-chart-line', 'AI sebagai alat bantu produktivitas kerja industri.'),
        ('AI untuk analisis data industri', 'ai-untuk-analisis-data-industri', 'fas fa-database', 'Analisis data sensor, produksi, dan operasional.'), ('Etika dan tata kelola', 'etika-dan-tata-kelola', 'fas fa-balance-scale', 'Tata kelola, tanggung jawab, dan etika penggunaan AI.'),
        ('Tren industri AI', 'tren-industri-ai', 'fas fa-chart-line', 'Perkembangan, riset, dan laporan industri seputar AI.')]
def lg(k, w=None): return IMG(LG[k]['id'], LG[k]['source_url'], grey=False, width={'unit': 'px', 'size': w or 220}, align='left')
def H2(t, color=NAVY, size=40, **s): return H(t, size, size - 8, size - 14, color=color, tag='h2', lh=1.12, **s)
def LBL(t): return W('text-editor', editor=f'<p style="margin:0">{t}</p>', text_color=ORANGE, **typo('Manrope', 13, weight='700', ls=1, up=True))
def band(title, sub=None):
    kids = [BADGE('AISolusiIndustri', '#FFFFFF', bgc='#FFFFFF1A', border='#FFFFFF33'), H(title, 56, 44, 36, color=WHITE, tag='h1', lh=1.05)]
    if sub: kids.append(BODY(f'<p style="margin:0">{sub}</p>', 18, '#C9D1E3'))
    return SEC(kids, None, pv=84, **grad(NAVY, NAVY2, 'linear', 160), shape_divider_bottom='curve', shape_divider_bottom_color=WHITE, shape_divider_bottom_height=px(40))
def catcard(i, name, slug, ic, desc, dark=False):
    fg, mu = (WHITE, '#C9D1E3') if dark else (NAVY, MUTE)
    return CARD([ICON(ic, ORANGE, 30), H(name, 22, 20, 20, color=fg, tag='h3', lh=1.2), BODY(f'<p style="margin:0">{desc}</p>', 14, mu),
                 W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{ORANGE};font-weight:700">Lihat artikel →</a></p>', **typo('Manrope', 14))],
                NAVY2 if dark else WHITE, 16, 26, shadow=None if dark else 'rgba(13,21,39,.08)', border=None if dark else '#E5E7EC')

def build_home():
    S = []
    # hero
    S.append(SEC([BADGE('Referensi AI untuk Industri & Operasional', '#FFFFFF', bgc='#FFFFFF1A', border='#FFFFFF40'),
                  H('Pahami AI untuk <span style="color:#F47A1F">Industri</span> dan Operasional.', 60, 46, 34, color=WHITE, tag='h1', lh=1.08, align='center'),
                  BODY('<p style="margin:0;text-align:center">AISolusiIndustri menghadirkan artikel, panduan, studi kasus, dan tren tentang penggunaan AI dalam industri dan operasional.</p>', 18, '#C9D1E3'),
                  W('wp-widget-search', wp={'title': ''}, _css_classes='ia-search'),
                  C([PILLBTN('Baca Artikel', f'{SITE}/blog/', ORANGE, WHITE), PILLBTN('Jelajahi Kategori', f'{SITE}/kategori/', 'transparent', WHITE, border='#FFFFFF66', hover_bg=ORANGE)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(12), flex_justify_content='center')],
                 None, pv=120, wpx=900, flex_align_items='center', padding=dim(110, 24, 170, 24), padding_mobile=dim(64, 18, 130, 18), **grad(NAVY, NAVY2, 'linear', 160), shape_divider_bottom='curve', shape_divider_bottom_color=WHITE, shape_divider_bottom_height=px(70)))
    # fakta
    FACT = [('14', 'yurisdiksi dalam riset studi banding'), ('5', 'bidang: manufaktur, operasional, supply chain, QC, maintenance'), ('9', 'kategori artikel'), ('Edukasi', 'bukan layanan atau produk')]
    S.append(SEC([ROW2([CARD([H(n, 38, 34, 30, color=ORANGE, tag='div', lh=1), BODY(f'<p style="margin:0">{t}</p>', 14, MUTE)], GREY, 14, 22, w=None, g=6, **{'width': {'unit': '%', 'size': 24}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}}) for n, t in FACT], g=20, flex_justify_content='space-between')],
                 None, pv=0, margin=dim(-110, 0, 0, 0), margin_mobile=dim(-90, 0, 0, 0), z_index=3, padding=dim(0, 24, 20, 24)))
    # about
    ID = ('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Materi berlandaskan buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
          f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{ORANGE}">Asosiasi AI Indonesia</a>, serta pembelajaran implementasi industri.')
    il = W('icon-list', icon_list=[{'_id': f'a{i}', 'text': t, 'selected_icon': {'value': 'fas fa-check-circle', 'library': 'fa-solid'}} for i, t in enumerate(['Berlandaskan riset dan praktik, bukan sekadar opini', 'Netral: tidak mempromosikan tools tertentu', 'Setiap klaim penting disertai sumber atau referensi', 'Bukan penyedia layanan, produk, atau lisensi'])],
           icon_color=ORANGE, text_color=NAVY, **typo('Manrope', 15, weight='500'))
    S.append(SEC([ROW2([C([LBL('Tentang'), H2('Referensi AI Industri yang Berlandaskan Riset dan Praktik'), PILLBTN('Pelajari lebih lanjut di asosiasi.ai', AS, ORANGE, WHITE, ext_=True)], flex_gap=gap(18), **WIDTH(46)),
                          C([BODY(f'<p style="margin:0">{ID}</p>', 17, NAVY), il], flex_gap=gap(18), **WIDTH(50))], g=40, flex_justify_content='space-between')], WHITE))
    # kategori
    grid = RWRAP([catcard(i, *CATS[i], dark=(i in (1, 2))) for i in range(4)], 18, **WIDTH(62), flex_direction='row')
    for c in grid['elements']: c['settings'].update({'width': {'unit': '%', 'size': 48}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}})
    panel = CARD([LBL('Kategori'), H('Jelajahi 9 Kategori Artikel', 34, 30, 28, color=WHITE, tag='h2', lh=1.1), BODY('<p style="margin:0">Manufaktur, operasional, supply chain, quality control, maintenance, dan lainnya — lengkap dengan konteks pembahasan.</p>', 15, '#E8ECF5'), PILLBTN('Lihat Semua Kategori', f'{SITE}/kategori/', ORANGE, WHITE)],
                 NAVY, 20, 32, **grad(NAVY2, NAVY, 'linear', 200), **WIDTH(35), flex_justify_content='flex-end', min_height=px(420))
    S.append(SEC([ROW2([grid, panel], g=24, flex_justify_content='space-between')], GREY))
    # prinsip
    PR = [('fas fa-book-open', 'Bersumber', 'Setiap klaim penting disertai sumber atau referensi.'), ('fas fa-balance-scale', 'Netral', 'Pembahasan tools AI informatif, bukan endorse.'), ('fas fa-ban', 'Bukan Jasa', 'Tidak ada penawaran layanan, produk, atau lisensi.'),
          ('fas fa-user-shield', 'Beretika', 'Etika, privasi, dan potensi misinformasi diperhatikan.'), ('fas fa-flask', 'Berbasis Riset', 'Landasan buku, riset 14 yurisdiksi, dan implementasi industri.'), ('fas fa-project-diagram', 'Kontekstual', 'Setiap artikel punya kategori dan konteks yang jelas.')]
    S.append(SEC([LBL('Prinsip editorial'), H2('Dibangun di Atas Referensi, Bukan Janji'),
                  RWRAP([C([ICON(ic, ORANGE, 28), H(t, 20, 19, 19, color=NAVY, tag='h3', lh=1.2), BODY(f'<p style="margin:0">{d}</p>', 14, MUTE)], flex_gap=gap(8), **{'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}}) for ic, t, d in PR], 24, flex_justify_content='space-between')], WHITE))
    # artikel terbaru
    def ac(i, t):
        return CARD([C([ICON('fas fa-file-alt', ORANGE, 44)], min_height=px(150), flex_justify_content='center', flex_align_items='center', border_radius=dim(12), **grad(NAVY, NAVY2, 'linear', 160)), LBL(f'Contoh · segera hadir'), H(t, 22, 20, 20, color=NAVY, tag='h3', lh=1.2), BODY('<p style="margin:0"><a href="' + SITE + '/blog/" style="color:#F47A1F;font-weight:700">Baca →</a></p>', 14)],
                    WHITE, 16, 18, border='#E5E7EC', shadow='rgba(13,21,39,.06)', **{'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}})
    S.append(SEC([LBL('Artikel terbaru'), H2('Bacaan Terbaru'), RWRAP([ac(i, t) for i, t in enumerate(['Judul artikel contoh pertama', 'Judul artikel contoh kedua', 'Judul artikel contoh ketiga'])], 24, flex_justify_content='space-between'), PILLBTN('Lihat semua artikel', f'{SITE}/blog/', NAVY, WHITE, hover_bg=ORANGE)], GREY))
    # identitas
    S.append(SEC([ROW2([C([lg('asosiasi_putih', 240), H('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 30, 26, 24, color=WHITE, tag='h2', lh=1.15)], flex_gap=gap(20), **WIDTH(48)),
                         C([BODY(f'<p style="margin:0">{ID.replace(ORANGE, "#F9A25F")}</p>', 16, '#D5DBE9'), C([PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai', AS, ORANGE, WHITE, ext_=True), PILLBTN('Hubungi Asosiasi AI Indonesia', AS, 'transparent', WHITE, border='#FFFFFF66', ext_=True, hover_bg=ORANGE)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(10))], flex_gap=gap(18), **WIDTH(48))], g=40, flex_justify_content='space-between')], NAVY))
    return S

def build_kategori():
    cards = [catcard(i, *CATS[i]) for i in range(9)]
    for c in cards: c['settings'].update({'width': {'unit': '%', 'size': 31}, 'width_tablet': {'unit': '%', 'size': 48}, 'width_mobile': {'unit': '%', 'size': 100}})
    return [band('Kategori', 'Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk industri.'), SEC([RWRAP(cards, 24, flex_justify_content='space-between')], WHITE, pv=70)]
def build_about():
    COPY = ('AISolusiIndustri adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI untuk industri dan operasional. Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
            f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{ORANGE}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
    LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.', 'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
    il = W('icon-list', icon_list=[{'_id': f'l{i}', 'text': t, 'selected_icon': {'value': 'fas fa-check-circle', 'library': 'fa-solid'}} for i, t in enumerate(LAND)], icon_color=ORANGE, text_color=WHITE, **typo('Manrope', 15, weight='500'))
    return [band('About', 'Tentang Publikasi Ini'), SEC([ROW2([C([BODY(f'<p style="margin:0">{COPY}</p>', 18, NAVY), lg('asosiasi', 260), PILLBTN('Pelajari Lebih Lanjut di asosiasi.ai', AS, ORANGE, WHITE, ext_=True)], flex_gap=gap(20), **WIDTH(56)),
            CARD([LBL('Landasan materi'), il, BODY('<p style="margin:0">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', 14, '#C9D1E3')], NAVY, 20, 32, **WIDTH(40))], g=36, flex_justify_content='space-between')], WHITE, pv=70)]
def build_kontak():
    def row(ic, label, val, url): return C([C([ICON(ic, ORANGE, 24)], width={'unit': 'px', 'size': 34}, width_mobile={'unit': 'px', 'size': 34}), C([LBL(label), W('text-editor', editor=f'<p style="margin:0"><a href="{url}" target="_blank" rel="noopener" style="color:#FFFFFF">{val}</a></p>', **typo('Manrope', 22, weight='800', lh=1.2))], flex_gap=gap(2))], flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_gap=gap(14), flex_align_items='center', padding=dim(14, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color='#2D3A5C')
    return [band('Kontak', 'Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.'),
            SEC([ROW2([C([BODY('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', 18, NAVY), lg('asosiasi', 260), PILLBTN('Konsultasi melalui Asosiasi AI Indonesia', AS, ORANGE, WHITE, ext_=True)], flex_gap=gap(20), **WIDTH(50)),
                       CARD([row('fab fa-whatsapp', 'WhatsApp', WAT, WA), row('fas fa-envelope', 'Email', EM, 'mailto:' + EM), row('fas fa-globe', 'Website', 'asosiasi.ai', AS), BODY('<p style="margin:10px 0 0">Usulan artikel atau ide: kirim lewat WhatsApp atau email di atas.</p>', 14, '#C9D1E3')], NAVY, 20, 32, **WIDTH(46))], g=36, flex_justify_content='space-between')], WHITE, pv=70)]
def save(name, S):
    (D / f'{name}_sections.json').write_text(json.dumps(S, ensure_ascii=False)); print(name, len(S))
if __name__ == '__main__':
    save('home', build_home()); save('kategori', build_kategori()); save('about', build_about()); save('kontak', build_kontak())
