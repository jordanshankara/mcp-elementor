"""BikinKontenAI: Home, Kategori, About, Kontak sebagai elemen Elementor Free native (gaya brutalis oranye/hitam/putih). Hasil: *_sections.json"""
import json, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent.parent / '_lib'))
import ek
ek.PAPER, ek.INK, ek.RED, ek.MUTE, ek.TAPE, ek.MONO = '#FEFEFE', '#050505', '#FF4800', '#555555', '#E6E6E6', 'Space Mono'
from ek import *
WHITE, GREY, LINE = '#FEFEFE', '#E6E6E6', '#2B2B2B'
ORANGE = RED
SITE, AS = 'https://www.bikinkontenai.id', 'https://asosiasi.ai/'
M = json.loads((D / 'media.json').read_text())
def ext(u): return {'url': u, 'is_external': 'on', 'nofollow': ''}
def bg(c): return {'background_background': 'classic', 'background_color': c}
def OBTN(text, url, ext_=False, **s):
    return BTN(text, url, dark=True, background_color=ORANGE, border_color=ORANGE, button_text_color='#FFFFFF', button_background_hover_color=INK, button_hover_border_color=INK, **({'link': ext(url)} if ext_ else {}), **s)
def LBTN(text, url, light=False, **s):
    return BTN(text, url, dark=False, button_text_color='#FFFFFF' if light else INK, border_color='#FFFFFF' if light else INK, **s)
def VLABEL(text, color=INK, bgc=None, w=56, ls=None):
    h = H(text, 13, 13, 13, color=color, tag='div', fam='Space Mono', lh=1, up=False, align='center', _css_classes='bk-v',
          typography_letter_spacing={'unit': 'px', 'size': 2}, typography_text_transform='uppercase', typography_font_weight='500')
    st = dict(width={'unit': 'px', 'size': w}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, justify_content='center', align_items='center',
              padding=dim(0), padding_tablet=dim(14, 20), padding_mobile=dim(12, 20), min_height=px(120), min_height_tablet=px(0), min_height_mobile=px(0), overflow='visible', border_border='solid',
              border_width=bw(0, 1, 0, 0), border_color=LINE if bgc == INK else INK, border_width_tablet=bw(0, 0, 1, 0), border_width_mobile=bw(0, 0, 1, 0))
    if bgc: st.update(bg(bgc))
    return C([h], **st)
def rowb(children, border=INK, **s):
    st = dict(border_color=border); st.update(s); return ROW(children, **st)
def cell(children, w=None, color_border=INK, bgc=None, pad=(28,), right=True, **s):
    st = dict(border_color=color_border); 
    if bgc: st.update(bg(bgc))
    st.update(s); return CELL(children, w=w, pad=pad, right=right, **st)
def NUMTXT(n, color=ORANGE): return MICRO(f'{n:02d} /', color=color)
def ARROW(color=ORANGE, link=None): return W('text-editor', editor=f'<p style="margin:0;font-size:20px">↗</p>', text_color=color, **typo('Space Mono', 20))
def A(el): return el

def build_home():
    S = []
    # 1 HERO
    hero_l = cell([
        MICRO('Supported by Asosiasi AI Indonesia', color=MUTE),
        H('Pahami AI<br>untuk membuat<br>konten <span style="color:#FF4800">digital.</span>', 9.4, 12, 15, tag='h1', lh=.9, unit='vw', color=INK),
        TXT('<p style="margin:0">BikinKontenAI menghadirkan artikel, panduan, ide, dan studi kasus tentang penggunaan AI dalam pembuatan konten digital.</p>', size=17),
        W('wp-widget-search', wp={'title': ''}, _css_classes='bk-search'),
        C([OBTN('Baca artikel ↗', f'{SITE}/blog/'), LBTN('Jelajahi kategori', f'{SITE}/kategori/')], flex_direction='row', flex_wrap='wrap', flex_gap=gap(10))],
        w=62, pad=(36, 32, 36, 32), flex_gap=gap(22), right=False, **bg(WHITE))
    hero_r = cell([C([IMG(M['hero']['id'], M['hero']['url'], grey=True)], padding=dim(0), **bg(ORANGE), margin=dim(0)),
                   STAMP('Edukasi', 'bukan', 'jasa', size=104)], w=38, pad=(0,), right=False, flex_gap=gap(0), **bg(ORANGE))
    hero_r['settings']['border_width'] = bw(0); hero_r['elements'][1]['settings'].update({'align_self': 'flex-end', 'margin': dim(-60, 24, 20, 0), 'position': 'relative', 'background_color': INK, 'border_color': WHITE})
    S.append(rowb([hero_l, hero_r], tablet_col=True, **bg(WHITE)))
    # 2 KATEGORI band hitam
    CATS = [('Tulisan & copywriting', 'Menyusun naskah, caption, dan copy dengan bantuan AI.', 'ai-untuk-tulisan-dan-copywriting'),
            ('Visual & desain', 'Desain grafis dan foto produk yang dibantu AI.', 'ai-untuk-desain-grafis'),
            ('Video pendek', 'Ide, skrip, dan penyuntingan video pendek.', 'ai-untuk-video-pendek'),
            ('Media sosial', 'Perencanaan dan produksi konten media sosial.', 'ai-untuk-media-sosial')]
    cells = [cell([NUMTXT(i + 1), H(t, 26, 26, 26, color=WHITE, tag='h3', lh=1), TXT(f'<p style="margin:0">{d}</p>', size=12, color='#BBBBBB'),
                   W('text-editor', editor=f'<p style="margin:0"><a href="{SITE}/category/{slug}/" style="color:{ORANGE}">Lihat artikel ↗</a></p>', **typo('Space Mono', 12, weight='500', up=True))],
                  w=25, color_border=LINE, right=(i < 3), **bg(INK)) for i, (t, d, slug) in enumerate(CATS)]
    S.append(rowb([VLABEL('Kategori', color='#FFFFFF', bgc=INK)] + [C(cells, flex_direction='row', flex_direction_tablet='row', flex_direction_mobile='column', flex_wrap='wrap',
                width={'unit': '%', 'size': 95}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, **bg(INK))], border=LINE, tablet_col=True, **bg(INK)))
    # 3 pernyataan besar
    S.append(rowb([cell([H('Konten AI yang bisa dipertanggungjawabkan.', 4.9, 7, 8.6, color=WHITE, tag='h2', lh=.95, unit='vw')], w=62, color_border=LINE, pad=(48, 36), **bg(INK)),
                   cell([TXT('<p style="margin:0;color:#FFFFFF">Berbasis riset, referensi, dan praktik. Bukan jasa, bukan produk.</p>', size=17, color='#FFFFFF'),
                         OBTN('Pelajari lebih lanjut di asosiasi.ai ↗', AS, True)], w=38, right=False, color_border=LINE, pad=(48, 36), justify_content='center', **bg(INK))],
                  border=LINE, tablet_col=True, **bg(INK)))
    # 4 artikel terbaru
    def card(n, bgc, tcol, mcol, k, title, ncol):
        im = IMG(M[k]['id'], M[k]['url'], grey=True, width={'unit': '%', 'size': 100}, height={'unit': 'px', 'size': 240}, object_fit='cover', align='center') if k else None
        kids = [im] if im else []
        kids += [NUMTXT(n, color=ncol), H(title, 30, 28, 26, color=tcol, tag='h3', lh=1, link={'url': f'{SITE}/blog/'}), MICRO('Contoh · segera hadir', color=mcol), MICRO('↗', color=ncol)]
        return cell(kids, w=33.33, bgc=bgc, color_border=INK, pad=(0, 0, 24, 0), flex_gap=gap(10), right=True, **{'padding': dim(0, 0, 24, 0)})
    cards = [card(1, GREY, INK, MUTE, 'c1', 'Judul artikel contoh pertama', ORANGE), card(2, ORANGE, INK, INK, 'c2', 'Judul artikel contoh kedua', INK), card(3, INK, WHITE, '#BBBBBB', 'c3', 'Judul artikel contoh ketiga', ORANGE)]
    for c in cards:
        for e in c['elements'][1:]: e['settings'].setdefault('_padding', dim(0, 22, 0, 22))
        c['elements'][0]['settings']['css_filters_saturate'] = px(0)
    right = C([H('Lihat semua artikel ↗', 13, 13, 13, color='#FFFFFF', tag='div', fam='Space Mono', lh=1, up=False, link={'url': f'{SITE}/blog/'}, _css_classes='bk-v bk-vr',
                 typography_text_transform='uppercase', typography_letter_spacing={'unit': 'px', 'size': 2}, typography_font_weight='500')],
              width={'unit': 'px', 'size': 56}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}, justify_content='center', align_items='center', min_height=px(120), min_height_tablet=px(0), min_height_mobile=px(0), padding_tablet=dim(14, 20), **bg(ORANGE))
    S.append(rowb([VLABEL('Artikel terbaru', color=INK, bgc=WHITE), C(cards, flex_direction='row', flex_direction_tablet='column', flex_direction_mobile='column', width={'unit': '%', 'size': 88}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100}), right], tablet_col=True, **bg(WHITE)))
    # 5 konteks topik
    KT = [('AI untuk tulisan dan copywriting', 'Menempatkan AI sebagai alat bantu menulis, bukan pengganti penulis.'), ('AI untuk visual dan desain', 'Memahami peluang dan batasan visual buatan AI.'), ('Etika dan hak cipta', 'Transparansi, hak cipta, dan potensi misinformasi pada konten AI.')]
    S.append(rowb([cell([NUMTXT(i + 1), H(t, 28, 26, 26, tag='h3', lh=1), TXT(f'<p style="margin:0">{d}</p>', size=14)], w=33.33, right=(i < 2), flex_gap=gap(10), **bg(WHITE)) for i, (t, d) in enumerate(KT)], tablet_col=True, **bg(WHITE)))
    # 6 identitas
    ID = ('Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Materi berlandaskan buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, '
          f'riset studi banding 14 yurisdiksi oleh <a href="{AS}" target="_blank" rel="noopener" style="color:{ORANGE}">Asosiasi AI Indonesia</a>, serta pembelajaran implementasi industri.')
    S.append(rowb([cell([MICRO('Inisiasi', color=MUTE), H('Landasan materi', 40, 34, 32, tag='h2')], w=30, **bg(GREY)),
                   cell([TXT(f'<p style="margin:0">{ID}</p>', size=17)], w=42, **bg(GREY)),
                   cell([OBTN('Pelajari lebih lanjut di asosiasi.ai ↗', AS, True), LBTN('Hubungi Asosiasi AI Indonesia', AS, link=ext(AS))], w=28, right=False, **bg(GREY))],
                  tablet_col=True, border_width=bw(0), **bg(GREY)))
    return S

def build_kategori():
    ALL = [('Tulisan dan copywriting', 'ai-untuk-tulisan-dan-copywriting'), ('Desain grafis', 'ai-untuk-desain-grafis'), ('Foto produk', 'ai-untuk-foto-produk'), ('Video pendek', 'ai-untuk-video-pendek'),
           ('Presentasi', 'ai-untuk-presentasi'), ('Media sosial', 'ai-untuk-media-sosial'), ('Ide konten', 'ai-untuk-ide-konten'), ('Etika dan hak cipta', 'etika-dan-hak-cipta'), ('Tren konten AI', 'tren-konten-ai')]
    S = [rowb([C([H('Kategori', 17, 17, 22, tag='h1', unit='vw', lh=.88)], padding=dim(26, 28, 8, 28), padding_mobile=dim(18, 20, 6, 20))], tablet_col=False, **bg(WHITE)),
         rowb([cell([TXT('<p style="margin:0;font-size:20px">Jelajahi artikel berdasarkan kategori dan konteks pembahasan seputar AI untuk konten digital.</p>', size=20)], w=100, right=False, **bg(WHITE))], tablet_col=False, **bg(WHITE))]
    rows = []
    for r in range(0, 9, 3):
        rows.append(rowb([cell([NUMTXT(i + 1, color=ORANGE), H(ALL[i][0], 34, 30, 28, tag='h3', lh=1, link={'url': f'{SITE}/category/{ALL[i][1]}/'}),
                              MICRO('Lihat artikel ↗', color=ORANGE, link=f'{SITE}/category/{ALL[i][1]}/')], w=33.33, right=(i % 3 < 2), flex_gap=gap(12), pad=(34, 28),
                             **bg(INK if i % 2 else WHITE)) for i in range(r, r + 3)], tablet_col=True, **bg(WHITE)))
    for rr in rows:
        for c in rr['elements']:
            if c['settings'].get('background_color') == INK:
                c['settings']['border_color'] = LINE
                for e in c['elements']:
                    if e['widgetType'] == 'heading': e['settings']['title_color'] = '#FFFFFF'
    return S + rows

def build_about():
    LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.',
            'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.', 'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
    COPY = ('BikinKontenAI adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI untuk pembuatan konten digital. '
            'Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, riset studi banding 14 yurisdiksi oleh '
            f'<a href="{AS}" target="_blank" rel="noopener" style="color:{ORANGE}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
    S = [rowb([C([H('About', 22, 22, 28, tag='h1', unit='vw', lh=.88)], padding=dim(26, 28, 8, 28), padding_mobile=dim(18, 20, 6, 20))], tablet_col=False, **bg(WHITE)),
         rowb([cell([MICRO('Inisiator', color=MUTE), TXT(f'<p style="margin:0">{COPY}</p>', size=19), C([OBTN('Pelajari lebih lanjut di asosiasi.ai ↗', AS, True)], margin=dim(10, 0, 0, 0))], w=58, **bg(WHITE)),
               cell([MICRO('Landasan materi', color='#BBBBBB')] + [C([TXT(f'<p style="margin:0;color:#FFFFFF"><span style="color:{ORANGE};font:500 12px Space Mono">{i+1:02d}</span> &nbsp; {t}</p>', size=16, color='#FFFFFF')], padding=dim(10, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=LINE) for i, t in enumerate(LAND)] +
                    [TXT('<p style="margin:14px 0 0;color:#FFFFFF">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', size=15, color='#FFFFFF')], w=42, right=False, color_border=LINE, **bg(INK))], tablet_col=True, **bg(WHITE)),
         rowb([cell([NUMTXT(i + 1), H(t, 30, 28, 28, tag='h3'), TXT(f'<p style="margin:0">{d}</p>')], w=25, right=(i < 3), flex_gap=gap(6), **bg(GREY)) for i, (t, d) in enumerate(
             [('Bersumber', 'Setiap klaim disertai sumber atau referensi.'), ('Netral', 'Tidak mempromosikan tools tertentu.'), ('Bukan jasa', 'Tanpa penawaran layanan, produk, template, atau kursus.'), ('Beretika', 'Hak cipta, privasi, dan misinformasi diperhatikan.')])],
              tablet_col=True, flex_wrap='wrap', border_width=bw(0), **bg(GREY))]
    return S

def build_kontak():
    S = [rowb([C([H('Kontak', 22, 22, 28, tag='h1', unit='vw', lh=.88)], padding=dim(26, 28, 8, 28), padding_mobile=dim(18, 20, 6, 20))], tablet_col=False, **bg(WHITE)),
         rowb([cell([MICRO('Hubungi', color=MUTE), TXT('<p style="margin:0;font-size:20px">Hubungi Asosiasi AI Indonesia untuk informasi lebih lanjut, kolaborasi, atau konsultasi.</p>', size=20),
                     TXT('<p style="margin:0">Semua permintaan konsultasi, kolaborasi, atau informasi program diarahkan ke asosiasi.ai.</p>', size=15),
                     C([OBTN('Buka asosiasi.ai ↗', AS, True)], margin=dim(8, 0, 0, 0))], w=60, **bg(WHITE)),
               cell([MICRO('Kontak resmi', color='#BBBBBB'), TXT('<p style="margin:0;color:#FFFFFF">Nomor WhatsApp dan email resmi mengikuti kontak di <a href="https://asosiasi.ai/" target="_blank" rel="noopener" style="color:#FF4800">asosiasi.ai</a>.</p>', size=16, color='#FFFFFF'),
                     TXT('<p style="margin:0;color:#BBBBBB">Usulan artikel atau ide: gunakan kontak resmi di atas.</p>', size=14, color='#BBBBBB')], w=40, right=False, color_border=LINE, **bg(INK))], tablet_col=True, **bg(WHITE))]
    return S

def save(name, S):
    for s in S: s['settings'].setdefault('background_background', 'classic'); s['settings'].setdefault('background_color', WHITE)
    (D / f'{name}_sections.json').write_text(json.dumps(S, ensure_ascii=False)); print(name, len(S))
if __name__ == '__main__':
    save('home', build_home()); save('kategori', build_kategori()); save('about', build_about()); save('kontak', build_kontak())
