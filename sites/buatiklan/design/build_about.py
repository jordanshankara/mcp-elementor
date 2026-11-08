"""Halaman About 'Tentang Publikasi Ini' (addendum). Hasil: about_sections.json"""
import json, pathlib
import build_home as B
from build_home import *
LAND = ['Buku <em>“Stay Human, Stay in Charge — Transformasi AI di Korporasi”</em> karya Dian Martin, Ketua Umum Asosiasi AI Indonesia.',
        'Riset dan buku studi banding terhadap 14 yurisdiksi yang dilakukan oleh Asosiasi AI Indonesia.',
        'Pembelajaran dari implementasi industri.', 'Sumber pendukung yang relevan dan dapat diverifikasi.']
COPY = ('BuatIklanAI adalah inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia, sebagai wadah publikasi dan referensi tentang penggunaan AI dalam periklanan dan digital marketing. '
        'Materi publikasi berlandaskan pada buku <em>Stay Human, Stay in Charge — Transformasi AI di Korporasi</em>, riset studi banding 14 yurisdiksi oleh '
        f'<a href="{ASOSIASI}" target="_blank" rel="noopener" style="color:{RED}">Asosiasi AI Indonesia</a>, serta pembelajaran dari implementasi industri. '
        'Website ini menyediakan publikasi dan edukasi, bukan layanan atau produk.')
A = []
A.append(ROW([C([H('Tentang publikasi ini', 9.2, 9.2, 11, tag='h1', unit='vw', lh=.88)], padding=dim(26, 24, 12, 24), padding_mobile=dim(18, 14, 8, 14))], tablet_col=False))
A.append(ROW([
    CELL([MICRO('Inisiator', color=MUTE), TXT(f'<p style="margin:0">{COPY}</p>', size=18),
          C([BTN('Pelajari Lebih Lanjut di asosiasi.ai →', ASOSIASI + '/', link={'url': ASOSIASI + '/', 'is_external': 'on', 'nofollow': ''})], margin=dim(10, 0, 0, 0))], w=58),
    CELL([MICRO('Landasan materi', color=MUTE)] + [C([TXT(f'<p style="margin:0"><span style="color:{RED};font:500 11px Inter;letter-spacing:.1em">{i+1:02d}</span> &nbsp; {t}</p>', size=16)],
          padding=dim(10, 0), border_border='solid', border_width=bw(0, 0, 1, 0), border_color=INK) for i, t in enumerate(LAND)] +
         [TXT('<p style="margin:14px 0 0">Publikasi disusun berdasarkan riset dan praktik, bukan sekadar opini atau rangkuman tren.</p>', size=15)], w=42, right=False)], tablet_col=True))
A.append(ROW([CELL([MICRO(f'{i+1:02d}', color=RED), H(t, 30, 28, 28, tag='h3'), TXT(f'<p style="margin:0">{d}</p>')], w=25, right=(i < 3), flex_gap=gap(6))
              for i, (t, d) in enumerate([('Bersumber', 'Setiap klaim disertai referensi.'), ('Netral', 'Tidak mempromosikan tools tertentu.'),
                                          ('Bukan jasa', 'Tanpa penawaran produk, layanan, atau harga.'), ('Beretika', 'Hak cipta, privasi, dan misinformasi diperhatikan.')])],
             tablet_col=True, flex_wrap='wrap', border_width=bw(0)))
for s in A: s['settings'].setdefault('background_background', 'classic'); s['settings'].setdefault('background_color', PAPER)
(pathlib.Path(__file__).parent / 'about_sections.json').write_text(json.dumps(A, ensure_ascii=False))
print(len(A), 'sections')
