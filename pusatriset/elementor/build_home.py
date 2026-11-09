"""Beranda PusatRiset: daftar section TOP-LEVEL (boxed 1152px = max-w-6xl) -> elementor/out/home.json (array)."""
import os
from lib import *

OUT = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)
KAT, DASH = '/katalog/', '/dashboard/'

PAD_SEC_T = sp(0, 24)   # padding horizontal tablet
PAD_SEC_M = sp(0, 16)

# ---------------- 1. HERO
pill = el('widget', {
    'icon_list': [{'_id': 'pill0001', 'text': 'Kurasi manusia, bukan cuma AI mentah', 'selected_icon': {'value': 'fas fa-magic', 'library': 'fa-solid'}}],
    'icon_color': B700, 'text_color': B700, 'icon_size': px(13), 'text_indent': px(6),
    'icon_typography_typography': 'custom', 'icon_typography_font_family': FONT, 'icon_typography_font_size': px(12), 'icon_typography_font_weight': '600',
    '_element_width': 'auto', '_background_background': 'classic', '_background_color': B100, '_padding': sp(4, 12), '_border_radius': radius(999)},
    widgetType='icon-list')

hero_left = box([
    box([pill], direction='row', justify='flex-start', align='center', extra={'flex_justify_content_tablet': 'center', 'flex_justify_content_mobile': 'center'}),
    heading('Pusat kurasi riset AI Indonesia & dunia', 48, '700', B900, tag='h1', size_t=36, size_m=30, lh=1.25,
            align='left', align_t='center', align_m='center', margin=sp(16, 0, 0, 0)),
    text('<p>Temukan riset kecerdasan buatan dengan ringkasan terkurasi, relevansi untuk Indonesia, dan sumber asli yang bisa dipertanggungjawabkan — abstrak asli, makna nyata.</p>',
         18, SECOND, 1.556, size_m=16, align='left', align_t='center', align_m='center', margin=sp(16, 0, 0, 0)),
    box([shortcode('[pr_cari]')], margin=sp(32, 0, 0, 0)),
], width=pct(55), extra={'width_tablet': pct(100), 'width_mobile': pct(100)})

hero_right = box([shortcode('[pr_hero_art]')], width=pct(45), css='pr-art-col',
                 extra={'width_tablet': pct(100), 'width_mobile': pct(100)})

hero = box([box([hero_left, hero_right], direction='row', gap_=40, align='center', wrap='nowrap',
                extra={'flex_direction_tablet': 'column', 'flex_direction_mobile': 'column', 'flex_gap_tablet': gap(40)})],
           inner=False, boxed=1152, pad=sp(80, 24), pad_t=sp(64, 24), pad_m=sp(64, 16), bg=ALT,
           border=(1, WARM, 'b'), css='pr-dots')

# ---------------- 2. KPI
kpi = box([shortcode('[pr_kpi]')], inner=False, boxed=1152, pad=sp(40, 24), pad_t=sp(40, 24), pad_m=sp(40, 16))

# ---------------- 3. KENAPA
FEATURES = [
    ('fas fa-quote-left', 'Abstrak Asli, Bukan Karangan', 'Setiap klaim ditelusuri balik ke abstrak sumber — kami tidak pernah mengarang angka atau temuan yang tidak tertulis di sana.'),
    ('fas fa-language', 'Relevansi untuk Indonesia', 'Bukan sekadar terjemahan — tiap riset dinilai konkret: sektor apa di Indonesia yang bisa memakainya, dan kenapa penting.'),
    ('fas fa-user-check', 'Ditinjau Editor Manusia', 'AI cuma membantu draf awal. Setiap ringkasan yang tayang sudah melewati tinjauan editor sebelum publik membacanya.'),
    ('fas fa-bookmark', 'Transparan Soal Sumber', 'Tier venue, lisensi, dan status metadata ditampilkan apa adanya — Anda tahu persis seberapa bisa diandalkan sumbernya.'),
]
feat_cards = [box([
    circle_icon(ic, 36, 18, B100, B700),
    heading(t, 14, '600', PRIMARY, tag='h3', margin=sp(12, 0, 0, 0), lh=1.43),
    text(f'<p>{d}</p>', 12, SECOND, 1.625, margin=sp(6, 0, 0, 0)),
], pad=sp(20), bg='rgba(255,255,255,0.72)', rad=16, shadow=SHADOW,
    border=(1, 'rgba(255,255,255,0.55)', None), css='pr-glass') for ic, t, d in FEATURES]

why = box([
    heading('Kenapa PusatRiset.ai', 12, '600', B700, tag='div', align='center', transform='uppercase', spacing=0.6),
    heading('Bukan agregator riset biasa', 24, '700', B900, tag='h2', align='center', margin=sp(8, 0, 0, 0), lh=1.33),
    grid(feat_cards, cols=(4, 2, 1), gap_=20, margin=sp(32, 0, 0, 0)),
], inner=False, boxed=1152, pad=sp(56, 24), pad_t=sp(56, 24), pad_m=sp(56, 16), bg=ALT, border=(1, WARM, 'tb'), css='pr-why')


def list_section(title, icon_cls, code, last=False):
    head = box([
        box([icon(icon_cls, 20, B700, margin=sp(0)), heading(title, 18, '600', B900, tag='h2', lh=1.55)],
            direction='row', gap_=8, align='center'),
        heading('Lihat semua →', 14, '500', B700, tag='div', link=KAT, css='pr-lihat'),
    ], direction='row', justify='space-between', align='center', margin=sp(0, 0, 16, 0), css='pr-lihat-row')
    return box([head, shortcode(code)], inner=False, boxed=1152,
               pad=sp(56 if not last else 0, 24, 64, 24), pad_t=sp(56 if not last else 0, 24, 64, 24), pad_m=sp(56 if not last else 0, 16, 64, 16))


terbaru = list_section('Riset Terbaru', 'fas fa-chart-line', '[pr_terbaru]')
populer = list_section('Riset Terpopuler', 'fas fa-fire', '[pr_populer]', last=True)

# ---------------- 6. CTA
cta = box([
    box([circle_icon('fas fa-chart-bar', 56, 28, 'rgba(255,255,255,0.10)', '#FFFFFF')], align='center'),
    heading('Lihat tren riset AI Indonesia vs dunia', 24, '600', '#FFFFFF', tag='h2', size_m=20, align='center', margin=sp(16, 0, 0, 0), lh=1.33),
    text('<p>Bandingkan pertumbuhan riset per tahun dan per subbidang lewat Dashboard — lihat area yang masih jarang diteliti di Indonesia dibanding tren global.</p>',
         14, 'rgba(255,255,255,0.8)', 1.43, align='center', margin=sp(8, 0, 0, 0), max_w=576),
    box([button('Buka Dashboard', DASH, '#FFFFFF', B900, 14, '500', sp(12, 24), 6)], align='center', margin=sp(24, 0, 0, 0)),
], inner=False, boxed=896, align='center', pad=sp(56, 24), pad_m=sp(56, 16), bg=B900, css='pr-dots-w')

sections = [hero, kpi, why, terbaru, populer, cta]
dump(sections, os.path.join(OUT, 'home.json'))
print('home.json', len(sections), 'section')
