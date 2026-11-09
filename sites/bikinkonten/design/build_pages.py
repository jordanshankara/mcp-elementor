"""BikinKontenAI: Home, Kategori, About, Kontak — Elementor Free native. Palet dari posting Instagram brand (krem, marun, tosca tua, oker); struktur/DNA dari referensi Frameform."""
import json, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent.parent / '_lib'))
import ek
CREAM, CARD, INK, MAROON, TEAL, OCHRE, OCHRE_L, MUTE = '#F0ECE3', '#E6E0D3', '#1B1A19', '#6E1620', '#0B4A50', '#A8601F', '#E7B47A', '#5A5750'
ek.HFAM, ek.HUP = 'Barlow Condensed', False
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = CREAM, INK, MAROON, MUTE, '#9DB5B2', 'Inter'
from ek import *
SITE, AS = 'https://www.bikinkontenai.id', 'https://asosiasi.ai/'
M = json.loads((D / 'media.json').read_text())
def ext(u): return {'url': u, 'is_external': 'on', 'nofollow': ''}
def bg(c): return {'background_background': 'classic', 'background_color': c}
def BP(text, url, ext_=False, **s):
    return BTN(text, url, dark=True, background_color=MAROON, border_color=MAROON, button_text_color=CREAM, button_background_hover_color=TEAL, button_hover_border_color=TEAL, **({'link': ext(url)} if ext_ else {}), **s)
def BO(text, url, light=False, ext_=False, **s):
    c = CREAM if light else INK
    return BTN(text, url, dark=False, button_text_color=c, border_color=c, hover_color=CREAM, button_background_hover_color=MAROON, button_hover_border_color=MAROON, **({'link': ext(url)} if ext_ else {}), **s)
def rowb(children, border=INK, **s):
    st = dict(border_color=border); st.update(s); return ROW(children, **st)
def cell(children, w=None, line=INK, bgc=None, pad=(28,), right=True, **s):
    st = dict(border_color=line)
    if bgc: st.update(bg(bgc))
    st.update(s); return CELL(children, w=w, pad=pad, right=right, **st)
def NUM(n, color=MAROON): return MICRO(f'{n:02d} / 08' if False else f'{n:02d}', color=color)
def RULE(label, color=OCHRE):
    line = lambda: C([], width={'unit': '%', 'size': 28}, width_mobile={'unit': '%', 'size': 14}, border_border='solid', border_width=bw(1, 0, 0, 0), border_color=color)
    return C([line(), MICRO(label, color=color), line()], flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='row', flex_align_items='center', flex_justify_content='center', flex_gap=gap(16), padding=dim(10, 0))
def POL(mid, url, rot=3):
    frame = C([IMG(mid, url, grey=False)], padding=dim(10), **bg('#FBF9F4'), border_border='solid', border_width=dim(1), border_color='#D6D0C0',
              _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': rot, 'sizes': []})
    tape = C([], width={'unit': 'px', 'size': 92}, min_height=px(24), **bg(TEAL), margin=dim(0, 0, -16, 0), _flex_align_self='center', _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': -5, 'sizes': []})
    back = C([tape, frame], padding=dim(22, 22, 26, 22), **bg(MAROON), flex_gap=gap(0), _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': -2, 'sizes': []})
    return C([back], padding=dim(10, 4))
def CIRCLE(label, bgc, size=240):
    return C([H(label, 46, 40, 40, color=CREAM, tag='div', align='center', lh=1)], width={'unit': 'px', 'size': size}, width_tablet={'unit': 'px', 'size': size}, width_mobile={'unit': 'px', 'size': 200}, min_height=px(size), min_height_mobile=px(200), flex_justify_content='center', flex_align_items='center',
             border_radius=dim(size // 2), **bg(bgc), _flex_align_self='center')
def LBL(text, color):
    return C([MICRO(text, color=color, align='center')], _flex_align_self='center', width={'unit': 'px', 'size': 270}, width_mobile={'unit': '%', 'size': 100}, padding=dim(10, 22), border_border='solid', border_width=dim(2), border_color=color, **bg('#F7F3EC'))

def build_home():
    S = []
    hero_l = cell([
        MICRO('Supported by Asosiasi AI Indonesia', color=MUTE),
        H('Pahami AI untuk Membuat Konten <span style="color:#6E1620">Digital.</span>', 9.2, 12, 15, tag='h1', lh=.9, unit='vw'),
        TXT('<p style="margin:0">BikinKontenAI menghadirkan artikel, panduan, ide, dan studi kasus tentang penggunaan AI dalam pembuatan konten digital.</p>', size=18),
        W('wp-widget-search', wp={'title': ''}, _css_classes='bk-search'),
        C([BP('Baca artikel →', f'{SITE}/blog/'), BO('Jelajahi kategori', f'{SITE}/kategori/')], flex_direction='row', flex_wrap='wrap', flex_gap=gap(10))],
        w=60, pad=(36, 32), flex_gap=gap(22), right=False, **bg(CREAM))
    hero_r = cell([POL(M['hero']['id'], M['hero']['url']), STAMP('Edukasi', 'bukan', 'jasa', size=100)], w=40, pad=(30, 28), right=False, flex_gap=gap(8), flex_justify_content='center', **bg(CREAM))
    hero_r['elements'][1]['settings'].update({'background_color': TEAL, '_flex_align_self': 'flex-end', 'border_color': CREAM, 'margin': dim(-50, 20, 0, 0)})
    S.append(rowb([hero_l, hero_r], tablet_col=True, **bg(CREAM)))
    CATS = [('Tulisan & Copywriting', 'Menyusun naskah, caption, dan copy dengan bantuan AI.', 'ai-untuk-tulisan-dan-copywriting'), ('Visual & Desain', 'Desain grafis dan foto produk yang dibantu AI.', 'ai-untuk-desain-grafis'),
            ('Video Pendek', 'Ide, skrip, dan penyuntingan video pendek.', 'ai-untuk-video-pendek'), ('Media Sosial', 'Perencanaan dan produksi konten media sosial.', 'ai-untuk-media-sosial')]
    cells = [cell([MICRO(f'{i+1:02d}', color=OCHRE_L), H(t, 34, 32, 32, color=CREAM, tag='h3', lh=1), TXT(f'<p style="margin:0">{d}</p>', size=14, color='#D5E0DE'),
                   W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{OCHRE_L}">Lihat artikel →</a></p>', **typo('Inter', 12, weight='600', up=True, ls=1))],
                  w=25, line='#2D6A70', right=(i < 3), **bg(TEAL)) for i, (t, d, slug) in enumerate(CATS)]
    S.append(rowb([cell([RULE('Kategori', OCHRE_L)], w=100, right=False, line='#2D6A70', pad=(18, 28), **bg(TEAL))] , border='#2D6A70', tablet_col=False, **bg(TEAL)))
    S.append(rowb(cells, border='#2D6A70', tablet_col=True, **bg(TEAL)))
    # bagi tugasnya
    A_ = C([CIRCLE('Manusia', MAROON), LBL('Manusia menentukan', MAROON), TXT('<p style="margin:0;text-align:center">Tujuan, sudut pandang, verifikasi, dan gaya personal.</p>', size=16)], width={'unit': '%', 'size': 40}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, flex_align_items='center', flex_gap=gap(16))
    B_ = C([CIRCLE('AI', TEAL, 200), LBL('AI membantu', TEAL), TXT('<p style="margin:0;text-align:center">Eksplorasi ide, kerangka awal, dan variasi visual.</p>', size=16)], width={'unit': '%', 'size': 40}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, flex_align_items='center', flex_gap=gap(16))
    ARW = C([H('→', 72, 56, 44, color=OCHRE, tag='div', align='center', lh=1)], width={'unit': '%', 'size': 10}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, flex_align_items='center', flex_justify_content='center')
    S.append(rowb([cell([H('Bagi Tugasnya. Tetap Pegang Arahnya.', 6.4, 9, 12, tag='h2', lh=.92, unit='vw'),
                         C([A_, ARW, B_], flex_direction='row', flex_direction_tablet='column', flex_direction_mobile='column', flex_justify_content='space-around', flex_align_items='center', flex_gap=gap(18), margin=dim(10, 0, 0, 0)),
                         RULE('Rekomendasi alur kerja')], w=100, right=False, pad=(48, 36), flex_gap=gap(22), **bg(CREAM))], tablet_col=False, **bg(CREAM)))
    # pernyataan
    S.append(rowb([cell([H('Otomatis Belum Tentu Terkendali.', 6.2, 8.5, 11, color=CREAM, tag='h2', lh=.92, unit='vw')], w=62, line='#8A3640', pad=(52, 36), **bg(MAROON)),
                   cell([TXT(f'<p style="margin:0;color:{CREAM}">AI membantu menjalankan proses. Arah konten dan keputusan akhirnya tetap ada di tangan Anda.</p>', size=18, color=CREAM),
                         BTN('Pelajari lebih lanjut di asosiasi.ai →', AS, dark=True, background_color=CREAM, border_color=CREAM, button_text_color=MAROON, button_background_hover_color=INK, link=ext(AS), hover_color=CREAM)],
                        w=38, right=False, line='#8A3640', pad=(52, 36), flex_justify_content='center', **bg(MAROON))], border='#8A3640', tablet_col=True, **bg(MAROON)))
    # artikel terbaru
    def card(n, bgc, tcol, mcol, k, title, ncol):
        kids = [IMG(M[k]['id'], M[k]['url'], grey=False, height={'unit': 'px', 'size': 230}, object_fit='cover')]
        kids += [NUM(n, ncol), H(title, 32, 30, 28, color=tcol, tag='h3', lh=1, link={'url': f'{SITE}/blog/'}), MICRO('Contoh · segera hadir', color=mcol), MICRO('→', color=ncol)]
        c = cell(kids, w=33.33, bgc=bgc, pad=(0, 0, 24, 0), flex_gap=gap(10), right=True, **{'padding': dim(0, 0, 24, 0)})
        for e in c['elements'][1:]: e['settings'].setdefault('_padding', dim(0, 22, 0, 22))
        return c
    cards = [card(1, CARD, INK, MUTE, 'c1', 'Judul Artikel Contoh Pertama', MAROON), card(2, TEAL, CREAM, '#D5E0DE', 'c2', 'Judul Artikel Contoh Kedua', OCHRE_L), card(3, MAROON, CREAM, '#E9C9CD', 'c3', 'Judul Artikel Contoh Ketiga', OCHRE_L)]
    S.append(rowb([cell([RULE('Artikel terbaru', OCHRE), C([], )], w=100, right=False, pad=(18, 28), **bg(CREAM))], tablet_col=False, **bg(CREAM)))
    S.append(rowb([C(cards, flex_direction='row', flex_direction_tablet='column', flex_direction_mobile='column', width={'unit': '%', 'size': 100}),], tablet_col=False, **bg(CREAM)))
    S.append(rowb([cell([BP('Lihat semua artikel →', f'{SITE}/blog/')], w=100, right=False, pad=(22, 28), **bg(CREAM))], tablet_col=False, **bg(CREAM)))
    # konteks
    KT = [('AI untuk Tulisan dan Copywriting', 'Menempatkan AI sebagai alat bantu menulis, bukan pengganti penulis.'), ('AI untuk Visual dan Desain', 'Memahami peluang dan batasan visual buatan AI.'), ('Etika dan Hak Cipta', 'Transparansi, hak cipta, dan potensi misinformasi pada konten AI.')]
    S.append(rowb([cell([NUM(i + 1, OCHRE), H(t, 30, 28, 28, tag='h3', lh=1), TXT(f'<p style="margin:0">{d}</p>', size=15)], w=33.33, right=(i < 2), flex_gap=gap(10), **bg(CREAM)) for i, (t, d) in enumerate(KT)], tablet_col=True, **bg(CREAM)))
    ID = ('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Materi berlandaskan buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
          f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{MAROON}">Asosiasi AI Indonesia</a>, serta pembelajaran implementasi industri.')
    S.append(rowb([cell([MICRO('Inisiasi', color=MUTE), H('Landasan Materi', 44, 36, 34, tag='h2')], w=30, **bg(CARD)), cell([TXT(f'<p style="margin:0">{ID}</p>', size=18)], w=42, **bg(CARD)),
                   cell([BP('Pelajari lebih lanjut di asosiasi.ai →', AS, True), BO('Hubungi Asosiasi AI Indonesia', AS, ext_=True)], w=28, right=False, **bg(CARD))], tablet_col=True, border_width=bw(0), **bg(CARD)))
    return S

def title_row(t): return rowb([C([H(t, 20, 22, 26, tag='h1', unit='vw', lh=.88)], padding=dim(26, 28, 8, 28), padding_mobile=dim(18, 20, 6, 20))], tablet_col=False, **bg(CREAM))
def build_kategori():
    ALL = [('Tulisan dan Copywriting', 'ai-untuk-tulisan-dan-copywriting'), ('Desain Grafis', 'ai-untuk-desain-grafis'), ('Foto Produk', 'ai-untuk-foto-produk'), ('Video Pendek', 'ai-untuk-video-pendek'), ('Presentasi', 'ai-untuk-presentasi'),
           ('Media Sosial', 'ai-untuk-media-sosial'), ('Ide Konten', 'ai-untuk-ide-konten'), ('Etika dan Hak Cipta', 'etika-dan-hak-cipta'), ('Tren Konten AI', 'tren-konten-ai')]
    S = [title_row('Kategori'), rowb([cell([TXT('<p style="margin:0;font-size:20px">Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk konten digital.</p>', size=20)], w=100, right=False, **bg(CREAM))], tablet_col=False, **bg(CREAM))]
    cols = [(CARD, INK, MAROON, INK), (TEAL, CREAM, OCHRE_L, '#2D6A70'), (MAROON, CREAM, OCHRE_L, '#8A3640')]
    for r in range(0, 9, 3):
        S.append(rowb([cell([MICRO(f'{i+1:02d}', color=cols[i % 3][2]), H(ALL[i][0], 36, 32, 30, color=cols[i % 3][1], tag='h3', lh=1, link={'url': f'{SITE}/category/{ALL[i][1]}/'}),
                              MICRO('Lihat artikel →', color=cols[i % 3][2], link=f'{SITE}/category/{ALL[i][1]}/')], w=33.33, right=(i % 3 < 2), flex_gap=gap(12), pad=(36, 28), **bg(cols[i % 3][0])) for i in range(r, r + 3)], tablet_col=True, **bg(CREAM)))
    return S

def build_about():
    LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.', 'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.', 'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
    COPY = ('BikinKontenAI adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI untuk pembuatan konten digital. Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
            f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{MAROON}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
    return [title_row('About'),
            rowb([cell([MICRO('Inisiator', color=MUTE), TXT(f'<p style="margin:0">{COPY}</p>', size=19), C([BP('Pelajari lebih lanjut di asosiasi.ai →', AS, True)], margin=dim(10, 0, 0, 0))], w=58, **bg(CREAM)),
                  cell([MICRO('Landasan materi', color=OCHRE_L)] + [C([TXT(f'<p style="margin:0;color:{CREAM}"><span style="color:{OCHRE_L};font-weight:700">{i+1:02d}</span> &nbsp; {t}</p>', size=16, color=CREAM)], padding=dim(10, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color='#2D6A70') for i, t in enumerate(LAND)] +
                       [TXT(f'<p style="margin:14px 0 0;color:{CREAM}">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', size=15, color=CREAM)], w=42, right=False, line='#2D6A70', **bg(TEAL))], tablet_col=True, **bg(CREAM)),
            rowb([cell([NUM(i + 1, OCHRE), H(t, 32, 30, 28, tag='h3'), TXT(f'<p style="margin:0">{d}</p>')], w=25, right=(i < 3), flex_gap=gap(6), **bg(CARD)) for i, (t, d) in enumerate(
                [('Bersumber', 'Setiap klaim disertai sumber atau referensi.'), ('Netral', 'Tidak mempromosikan tools tertentu.'), ('Bukan Jasa', 'Tanpa penawaran layanan, produk, template, atau kursus.'), ('Beretika', 'Hak cipta, privasi, dan misinformasi diperhatikan.')])], tablet_col=True, flex_wrap='wrap', border_width=bw(0), **bg(CARD))]

def build_kontak():
    return [title_row('Kontak'),
            rowb([cell([MICRO('Hubungi', color=MUTE), TXT('<p style="margin:0;font-size:22px">Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.</p>', size=22),
                        TXT('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', size=15), C([BP('Buka asosiasi.ai →', AS, True)], margin=dim(8, 0, 0, 0))], w=60, **bg(CREAM)),
                  cell([MICRO('Kontak resmi', color=OCHRE_L), TXT(f'<p style="margin:0;color:{CREAM}">Nomor WhatsApp dan email resmi mengikuti kontak di <a href="{AS}" target="_blank" rel="noopener" style="color:{OCHRE_L}">asosiasi.ai</a>.</p>', size=16, color=CREAM),
                        TXT('<p style="margin:0;color:#D5E0DE">Usulan artikel atau ide: gunakan kontak resmi di atas.</p>', size=14, color='#D5E0DE')], w=40, right=False, line='#2D6A70', **bg(TEAL))], tablet_col=True, **bg(CREAM))]

def save(name, S):
    for s in S: s['settings'].setdefault('background_background', 'classic'); s['settings'].setdefault('background_color', CREAM)
    (D / f'{name}_sections.json').write_text(json.dumps(S, ensure_ascii=False)); print(name, len(S))
if __name__ == '__main__':
    save('home', build_home()); save('kategori', build_kategori()); save('about', build_about()); save('kontak', build_kontak())
