"""Metodologi (native penuh), Archive & Dashboard (shortcode plugin) -> elementor/out/*.json"""
import os
from lib import *

OUT = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)

G = {'blue': 'pr-g-blue', 'teal': 'pr-g-teal', 'indigo': 'pr-g-indigo'}  # gradien 3-stop didefinisikan di CSS Tambahan


def gcard(kind, ic, title, desc):
    return box([
        circle_icon(ic, 36, 16, 'rgba(255,255,255,0.15)', '#FFFFFF'),
        heading(title, 14, '600', '#FFFFFF', tag='h3', margin=sp(12, 0, 0, 0), lh=1.43),
        text(f'<p>{desc}</p>', 12, 'rgba(255,255,255,0.8)', 1.625, margin=sp(6, 0, 0, 0)),
    ], pad=sp(20), rad=16, shadow=SHADOW_LG, css=G[kind], grad=(B700, B900, 135))


def glass(children, elem_id=None):
    b = box(children, pad=sp(20), bg='rgba(255,255,255,0.72)', rad=16, shadow=SHADOW,
            border=(1, 'rgba(255,255,255,0.55)', None), css='pr-glass')
    if elem_id: b['settings']['_element_id'] = elem_id
    return b


def h2(t, mt=0):
    return heading(t, 18, '600', PRIMARY, tag='h2', lh=1.55, margin=sp(mt, 0, 0, 0))


def titled(ic, t):
    return box([icon(ic, 16, B700, margin=sp(0)), heading(t, 14, '600', PRIMARY, tag='h3', lh=1.43)],
               direction='row', gap_=8, align='center')


# ---------------- Metodologi
band = box([box([
    circle_icon('fas fa-book-open', 44, 20, B100, B700),
    box([heading('Metodologi', 24, '700', B900, tag='h1', size_m=20, lh=1.33),
         text('<p>Bagaimana PusatRiset.ai mengumpulkan, mengurasi, dan menyajikan riset AI Indonesia &amp; dunia — termasuk batasan dan kebijakan yang kami terapkan.</p>',
              14, SECOND, 1.43, margin=sp(4, 0, 0, 0))], gap_=0),
], direction='row', gap_=12, align='center', wrap='nowrap')],
    inner=False, boxed=768, pad=sp(40, 24), pad_m=sp(40, 16), bg=ALT, border=(1, WARM, 'b'))

BADGES = [('Masih Relevan', '#2F7A4F', '#E1F0E6', 'Temuan masih dianggap relevan/state-of-the-art saat ini.'),
          ('Perlu Pembaruan', '#B98A1E', '#F7EEDA', 'Masih relevan, namun ada keterbatasan yang perlu diperbarui.'),
          ('Sudah Digantikan', '#C9701F', '#F8E3D2', 'Sudah digantikan oleh riset yang lebih baru dan lebih baik.'),
          ('Ditarik', '#B8352E', '#F8DEDC', 'Ditarik oleh penerbit — dibaca dengan kehati-hatian.'),
          ('Riset Fondasi', B700, B100, 'Riset fondasional dengan pengaruh besar dan tahan lama.')]


def chip(label, fg, bg):
    w = heading(label, 12, '500', fg, tag='div', lh=1.33)
    w['settings'].update({'_element_width': 'auto', '_background_background': 'classic', '_background_color': bg,
                          '_padding': sp(2, 8), '_border_radius': radius(999)})
    return w


badge_rows = [box([chip(l, fg, bg), text(f'<p>{d}</p>', 14, SECOND, 1.43)], direction='row', gap_=12, align='center',
                  wrap='nowrap') for l, fg, bg, d in BADGES]
badge_note = box([text('<p>Paper tanpa badge berarti belum ditinjau editor — bukan berarti tidak relevan.</p>', 12, MUTED, 1.33)],
                 pad=sp(10, 0, 0, 0), border=(1, WARM, 't'))

POL = [
    ('fas fa-lock', 'Kebijakan Abstrak & Lisensi', 'Abstrak asli hanya ditampilkan penuh bila lisensi sumber terbuka (mis. CC BY, CC0) atau paper berstatus open access dan sumber mengizinkan. Untuk sumber yang membatasi penggunaan metadata, kami hanya menampilkan ringkasan hasil kurasi editor.', None),
    ('fas fa-globe', 'Kebijakan Inklusi', 'Riset Indonesia yang kami masukkan berasal dari jurnal terindeks DOAJ, SINTA peringkat 1–4, atau melalui tinjauan editorial manual untuk sumber yang belum terindeks formal namun memenuhi standar kualitas dasar.', None),
    ('fas fa-comment-slash', 'Cara Mengajukan Sanggahan', 'Setiap halaman detail riset memiliki tautan "Keberatan dengan konten ini?" pada tab Ringkasan & Relevansi. Sanggahan Anda akan masuk ke antrean tinjauan editor sebelum ada perubahan pada halaman publik.', 'sanggahan'),
]

DISC = '#B98A1E'
disc = box([
    box([icon('fas fa-exclamation-triangle', 16, DISC, margin=sp(0)), heading('Disclaimer', 14, '600', DISC, tag='h3', lh=1.43)],
        direction='row', gap_=8, align='center'),
    text('<p>Ringkasan dan label relevansi di situs ini dibantu oleh kecerdasan buatan dan ditinjau oleh editor manusia sebelum tayang, namun tetap dapat mengandung kesalahan interpretasi. Selalu rujuk ke sumber asli untuk keputusan yang bersifat kritis.</p>',
         12, DISC, 1.625, margin=sp(6, 0, 0, 0)),
], pad=sp(20), bg='#F7EEDA', rad=14, border=(1, 'rgba(185,138,30,0.3)', None), margin=sp(40, 0, 0, 0))

sumber = box([h2('Sumber Data'), grid([
    gcard('blue', 'fas fa-globe-asia', 'Riset Internasional', 'Bersumber dari venue tier-1 (mis. NeurIPS, ICML, ICLR, ACL) dan preprint arXiv (cs.AI, cs.LG).'),
    gcard('teal', 'fas fa-map-marker-alt', 'Riset Indonesia', 'Bersumber dari jurnal terindeks SINTA atau DOAJ, serta repositori institusi. Metadata diperkaya menggunakan OpenAlex bila tersedia.'),
], cols=(2, 1, 1), gap_=16, margin=sp(12, 0, 0, 0))])
sumber['settings']['_element_id'] = 'sumber-data'

tier = box([h2('Sistem Tier Venue'), grid([
    gcard('indigo', 'fas fa-trophy', 'Tier 1', 'Konferensi/jurnal papan atas dengan reputasi internasional mapan.'),
    gcard('blue', 'fas fa-book-open', 'Tier 2', 'Jurnal terindeks (SINTA 1–2, DOAJ) atau preprint repository (arXiv).'),
    gcard('teal', 'fas fa-file-alt', 'Tier 3', 'Sumber lain yang lolos tinjauan editorial minimal.'),
], cols=(3, 1, 1), gap_=16, margin=sp(12, 0, 0, 0))], margin=sp(40, 0, 0, 0))

sumbu = box([h2('Dua Sumbu Editorial'),
             text('<p>Setiap riset melewati dua lapis kurasi independen sebelum tayang ke publik. Draf yang belum ditinjau tidak pernah tampil, meski datanya sudah ada di database.</p>',
                  14, SECOND, 1.625, margin=sp(8, 0, 0, 0)),
             grid([glass([titled('fas fa-database', 'Status Metadata'),
                          text('<p>Apakah riset ini layak diindeks sama sekali.</p>', 12, SECOND, 1.625, margin=sp(6, 0, 0, 0))]),
                   glass([titled('fas fa-eye', 'Status Interpretasi'),
                          text('<p>Apakah ringkasan, relasi, dan tag kebijakan sudah ditinjau editor sebelum tayang ke publik.</p>', 12, SECOND, 1.625, margin=sp(6, 0, 0, 0))])],
                  cols=(2, 1, 1), gap_=16, margin=sp(12, 0, 0, 0))], margin=sp(40, 0, 0, 0))

badge = box([h2('Arti Setiap Badge'),
             box([glass(badge_rows + [badge_note])], margin=sp(12, 0, 0, 0))], margin=sp(40, 0, 0, 0))
badge['settings']['_element_id'] = 'badge'
badge['elements'][1]['elements'][0]['settings']['flex_gap'] = gap(10)

pol = grid([glass([titled(ic, t), text(f'<p>{d}</p>', 12, SECOND, 1.625, margin=sp(6, 0, 0, 0))], elem_id=eid)
            for ic, t, d, eid in POL], cols=(1, 1, 1), gap_=16, margin=sp(40, 0, 0, 0))

body = box([sumber, tier, sumbu, badge, pol, disc], inner=False, boxed=768, pad=sp(40, 24), pad_m=sp(40, 16))
dump([band, body], os.path.join(OUT, 'metodologi.json'))

# ---------------- Archive & Dashboard: seluruh isi dari shortcode plugin (hero bawaan memuat form cari/filter)
for name, code in (('katalog', '[pr_katalog hero="1"]'), ('dashboard', '[pr_dashboard hero="1"]')):
    dump([box([shortcode(code)], inner=False, extra={'content_width': 'full'})], os.path.join(OUT, name + '.json'))
print('ok')
