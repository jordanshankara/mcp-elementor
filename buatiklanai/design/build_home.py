"""Bangun Beranda BuatIklanAI sebagai elemen Elementor (container + widget Free native). Hasil: home_sections.json (daftar elemen level atas)."""
import json, pathlib
D = pathlib.Path(__file__).parent
PAPER, INK, RED, MUTE, TAPE = '#ECE7DB', '#0B0B0B', '#D9291C', '#4A463E', '#D8CFB3'
ASOSIASI = 'https://asosiasi.ai'
SITE = 'https://www.buatiklanai.id'
def px(n): return {'unit': 'px', 'size': n}
def dim(t, r=None, b=None, l=None):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': t == r == b == l}
def gap(n): return {'unit': 'px', 'size': n, 'column': str(n), 'row': str(n), 'isLinked': True}
def bw(t=0, r=0, b=0, l=0): return dim(t, r, b, l)
def R(base, key, d=None, t=None, m=None):
    if d is not None: base[key] = d
    if t is not None: base[key + '_tablet'] = t
    if m is not None: base[key + '_mobile'] = m
def C(children, **s):
    st = {'content_width': 'full', 'flex_direction': 'column', 'padding': dim(0), 'flex_gap': gap(0)}
    st.update(s); return {'elType': 'container', 'settings': st, 'elements': children}
def ROW(children, tablet_col=True, **s):
    st = {'flex_direction': 'row', 'flex_direction_tablet': 'column' if tablet_col else 'row', 'flex_direction_mobile': 'column',
          'border_border': 'solid', 'border_width': bw(0, 0, 1, 0), 'border_color': INK, 'align_items': 'stretch'}
    st.update(s); return C(children, **st)
def CELL(children, w=None, pad=(28,), right=True, **s):
    st = {'padding': dim(*pad), 'padding_tablet': dim(24, 24), 'padding_mobile': dim(20, 20),
          'border_border': 'solid', 'border_width': bw(0, 1 if right else 0, 0, 0), 'border_color': INK, 'flex_gap': gap(14),
          'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100},
          'border_width_tablet': bw(0, 0, 1, 0), 'border_width_mobile': bw(0, 0, 1, 0)}
    if w: st['width'] = {'unit': '%', 'size': w}
    st.update(s); return C(children, **st)
def W(wt, **s): return {'elType': 'widget', 'widgetType': wt, 'settings': s}
def typo(fam, size, tablet=None, mobile=None, weight='400', lh=None, ls=None, up=False, unit='px'):
    d = {'typography_typography': 'custom', 'typography_font_family': fam, 'typography_font_weight': weight,
         'typography_font_size': {'unit': unit, 'size': size}}
    if tablet is not None: d['typography_font_size_tablet'] = {'unit': unit, 'size': tablet}
    if mobile is not None: d['typography_font_size_mobile'] = {'unit': unit, 'size': mobile}
    if lh: d['typography_line_height'] = {'unit': 'em', 'size': lh}
    if ls is not None: d['typography_letter_spacing'] = {'unit': 'px', 'size': ls}
    if up: d['typography_text_transform'] = 'uppercase'
    return d
def H(text, size, tablet=None, mobile=None, color=INK, tag='h2', fam='Anton', lh=.95, up=True, align='left', unit='px', **s):
    d = {'title': text, 'header_size': tag, 'title_color': color, 'align': align}
    d.update(typo(fam, size, tablet, mobile, lh=lh, ls=-0.5 if fam == 'Anton' else 0, up=up and fam == 'Anton', unit=unit)); d.update(s)
    return W('heading', **d)
def SCRIPT(text, size, tablet, mobile, color=INK, rot=-3, tag='h3'):
    return H(text, size, tablet, mobile, color=color, tag=tag, fam='Caveat', lh=1, up=False, _transform_rotate_popover='transform',
             _transform_rotateZ_effect={'unit': 'px', 'size': rot, 'sizes': []})
def MICRO(text, color=INK, align='left', link=None):
    html = f'<a href="{link}" style="color:{RED}">{text}</a>' if link else text
    return W('text-editor', editor=f'<p style="margin:0">{html}</p>', text_color=color, align=align,
             **typo('Inter', 11, weight='500', lh=1.8, ls=2, up=True))
def TXT(html, size=15, color=INK, **s):
    d = {'editor': html, 'text_color': color}; d.update(typo('Inter', size, mobile=15, weight='400', lh=1.6)); d.update(s); return W('text-editor', **d)
def BTN(text, url, dark=True, **s):
    d = {'text': text, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'align': 'left',
         'button_text_color': PAPER if dark else INK, 'background_color': INK if dark else 'transparent',
         'border_border': 'solid', 'border_width': dim(1), 'border_color': INK, 'border_radius': dim(0),
         'text_padding': dim(14, 22), 'hover_color': PAPER, 'button_background_hover_color': RED, 'button_hover_border_color': RED}
    d.update(typo('Inter', 11, weight='500', ls=2, up=True)); d.update(s); return W('button', **d)
def IMG(mid, url, grey=True, rot=0, w=None, **s):
    d = {'image': {'id': mid, 'url': url}, 'image_size': 'large', 'align': 'center', 'width': {'unit': '%', 'size': w or 100}}
    if grey: d.update({'css_filters_css_filter': 'custom', 'css_filters_saturate': px(0), 'css_filters_contrast': px(115)})
    if rot: d.update({'_transform_rotate_popover': 'transform', '_transform_rotateZ_effect': {'unit': 'px', 'size': rot, 'sizes': []}})
    d.update(s); return W('image', **d)
def POLAROID(mid, url, rot, alt=''):
    tape = C([], width={'unit': 'px', 'size': 90}, min_height=px(24), background_background='classic', background_color=TAPE,
             margin=dim(0, 0, -14, 0), align_self='center', _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': -4, 'sizes': []})
    ph = C([IMG(mid, url, grey=True)], padding=dim(10), background_background='classic', background_color='#F4F1E8',
           border_border='solid', border_width=dim(1), border_color='#D6D0C0',
           _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': rot, 'sizes': []})
    return C([tape, ph], padding=dim(8, 0), flex_gap=gap(0))
def STAMP(l1, l2, l3, size=112):
    return C([H(f'{l1}<br>{l2}<br>{l3}', 10, color=PAPER, tag='div', fam='Inter', align='center', lh=1.5, typography_font_weight='500',
               typography_letter_spacing={'unit': 'px', 'size': 1}, typography_text_transform='uppercase')],
             width={'unit': 'px', 'size': size}, width_tablet={'unit': 'px', 'size': size}, width_mobile={'unit': 'px', 'size': size}, align_self='flex-start', min_height=px(size), justify_content='center', align_items='center',
             background_background='classic', background_color=RED, border_radius=dim(size // 2),
             border_border='dashed', border_width=dim(2), border_color=PAPER, padding=dim(8))

IMGS = json.loads((D / 'media.json').read_text())
M = lambda k: (IMGS[k]['id'], IMGS[k]['url'])
def CARD(no, title, cat, url, k):
    mid, u = M(k)
    return CELL([W('image', image={'id': mid, 'url': u}, image_size='large', link_to='custom', link={'url': url},
                   css_filters_css_filter='custom', css_filters_saturate=px(0), css_filters_contrast=px(115),
                   image_border_radius=dim(0)),
                 MICRO(f'{no} · {cat}', color=MUTE),
                 H(title, 30, 28, 26, tag='h3', link={'url': url}, lh=1.0),
                 MICRO('Baca →', color=RED, link=url)],
                w=None, pad=(22,), right=True, flex_gap=gap(10), **{'width': {'unit': '%', 'size': 33.33}})
S = []
# 1 — wordmark
S.append(ROW([C([H('BuatIklanAI', 19.5, 19, 19, tag='h1', unit='vw', lh=.82, align='left', typography_letter_spacing={'unit': 'px', 'size': -1})],
                padding=dim(18, 24, 6, 24), padding_mobile=dim(14, 14, 4, 14), overflow='hidden')],
             tablet_col=False, background_background='classic', background_color=PAPER))
# 2 — hero
S.append(ROW([
    CELL([H('Pahami AI<br>untuk iklan<br>&amp; marketing.', 42, 38, 34, tag='h2', lh=.98),
          C([], border_border='solid', border_width=bw(2, 0, 0, 0), border_color=INK, width={'unit': 'px', 'size': 34}),
          MICRO('Artikel<br>Panduan<br>Studi kasus'),
          STAMP('AI · Iklan', 'Edukasi', 'Bersumber')], w=26, flex_gap=gap(18)),
    CELL([POLAROID(*M('hero'), rot=2)], w=44, pad=(30, 28)),
    CELL([C([H('referensi,<br>bukan jasa.', 34, 30, 30, color=INK, tag='div', fam='Caveat', lh=1, up=False)],
            background_background='classic', background_color=TAPE, padding=dim(14, 18), width={'unit': 'px', 'size': 190},
            align_self='flex-end', _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': 5, 'sizes': []}),
          TXT('<p style="margin:0">Artikel, panduan, tren, dan studi kasus penggunaan AI dalam komunikasi pemasaran.</p>'),
          MICRO(f'Oleh <a href="{ASOSIASI}" target="_blank" rel="noopener" style="color:{RED}">Asosiasi AI Indonesia</a>'),
          C([BTN('Baca Artikel →', f'{SITE}/blog/'), BTN('Jelajahi Topik', '#topik', dark=False)], flex_direction='row', flex_wrap='wrap', flex_gap=gap(8))],
         w=30, right=False)], tablet_col=True))
# 3 — pasangan teks
def PAIR(big, script, color):
    return ROW([CELL([H(big, 120, 80, 48, tag='h2', lh=.92)], w=55, pad=(20, 28), justify_content='center'),
                CELL([SCRIPT(script, 96, 64, 44, color=color)], w=45, pad=(20, 28), right=False, justify_content='center')], tablet_col=False,
               flex_direction_tablet='row', flex_direction_mobile='row', flex_wrap='nowrap')
S.append(PAIR('AI untuk', 'yang bisa diuji', INK))
S.append(PAIR('Iklan yang', 'bisa dipercaya.', RED))
# 4 — tentang + topik
TOP = [('riset-pasar', 'ai-untuk-riset-pasar', 'AI untuk riset pasar'), ('konten', 'ai-untuk-ide-dan-pembuatan-konten', 'AI untuk ide dan pembuatan konten'),
       ('iklan', 'ai-untuk-iklan-digital', 'AI untuk iklan digital'), ('seo', 'ai-untuk-seo-dan-geo', 'AI untuk SEO dan GEO'),
       ('sosmed', 'ai-untuk-media-sosial', 'AI untuk media sosial'), ('visual', 'ai-untuk-visual-foto-dan-video', 'AI untuk visual, foto, dan video'),
       ('performa', 'ai-untuk-analisis-performa', 'AI untuk analisis performa'), ('etika', 'etika-dan-kepatuhan', 'Etika dan kepatuhan'),
       ('tren', 'tren-dan-laporan-industri', 'Tren dan laporan industri')]
topic_rows = [C([W('text-editor', editor=f'<p style="margin:0"><span style="color:{RED};font:500 11px Inter;letter-spacing:.1em">{i+1:02d}</span> &nbsp; <a href="{SITE}/category/{slug}/" style="color:{INK}">{name}</a></p>',
                   **typo('Inter', 17, lh=1.3))], padding=dim(9, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=INK)
              for i, (_, slug, name) in enumerate(TOP)]
S.append(ROW([
    CELL([MICRO('01', color=MUTE)], w=6, pad=(28, 14), pad_tablet=None) if False else CELL([MICRO('01', color=MUTE)], w=6, pad=(28, 14)),
    CELL([H('Tentang', 28, 28, 28, tag='h2'),
          TXT('<p style="margin:0">BuatIklanAI adalah pusat publikasi dan referensi tentang AI untuk periklanan, digital marketing, dan komunikasi brand.</p>'),
          C([], border_border='solid', border_width=bw(2, 0, 0, 0), border_color=INK, width={'unit': 'px', 'size': 34}),
          MICRO('Edukasi, bukan jasa.')], w=28),
    CELL([POLAROID(*M('about'), rot=-2)], w=30, pad=(30, 28)),
    CELL([MICRO('02', color=MUTE), H('Topik', 28, 28, 28, tag='h2')] + topic_rows, w=36, right=False, _element_id='topik')], tablet_col=True))
# 5 — artikel terbaru
posts = json.loads((D / 'posts.json').read_text())
S.append(ROW([
    CELL([MICRO('03', color=MUTE)], w=6, pad=(28, 14)),
    C([ROW([CELL([H('Artikel terbaru', 28, 28, 28, tag='h2')], w=70, right=False, pad=(22, 22), border_width=bw(0), border_width_tablet=bw(0), border_width_mobile=bw(0)),
            CELL([BTN('Lihat semua artikel →', f'{SITE}/blog/', dark=False)], w=30, right=False, pad=(22, 22), border_width=bw(0), border_width_tablet=bw(0), border_width_mobile=bw(0))],
           tablet_col=False, flex_direction_mobile='column', border_width=bw(0, 0, 1, 0)),
       C([CARD(f'{i+1:03d}', p['title'], p['cat'], p['url'], p['img']) for i, p in enumerate(posts)], flex_direction='row', flex_direction_tablet='column', flex_direction_mobile='column')],
      width={'unit': '%', 'size': 94}, width_tablet={'unit': '%', 'size': 100}, width_mobile={'unit': '%', 'size': 100})], tablet_col=True))
# 6 — prinsip
PR = [('Bersumber', 'Setiap klaim disertai referensi.'), ('Netral', 'Tidak mempromosikan tools tertentu.'),
      ('Bukan jasa', 'Tanpa penawaran produk atau layanan.'), ('Beretika', 'Hak cipta, privasi, dan misinformasi diperhatikan.')]
S.append(ROW([CELL([MICRO(f'{i+1:02d}', color=RED), H(t, 30, 28, 28, tag='h3'), TXT(f'<p style="margin:0">{d}</p>')], w=25, right=(i < 3), flex_gap=gap(6))
              for i, (t, d) in enumerate(PR)], tablet_col=True, flex_wrap='wrap'))
# 7 — CTA
S.append(ROW([
    CELL([MICRO('04', color=MUTE)], w=6, pad=(28, 14)),
    CELL([C([H('Kirim ide', 84, 60, 44, tag='h2', lh=.95), SCRIPT('artikelmu.', 84, 60, 44, color=RED, rot=-4)], flex_direction='row', flex_wrap='wrap',
            align_items='center', flex_gap=gap(14))], w=48),
    CELL([TXT('<p style="margin:0">Punya ide artikel, riset, atau studi kasus seputar AI untuk periklanan? Kirimkan usulan Anda.</p>'),
          BTN('Kirim usulan →', f'{SITE}/kirim-artikel/')], w=34),
    CELL([STAMP('Edukasi', 'bukan', 'jasa', size=104)], w=12, right=False, align_items='center')], tablet_col=True, border_width=bw(0)))
for s in S: s['settings'].setdefault('background_background', 'classic'); s['settings'].setdefault('background_color', PAPER)
(D / 'home_sections.json').write_text(json.dumps(S, ensure_ascii=False))
print(len(S), 'sections', len(json.dumps(S)), 'bytes')
