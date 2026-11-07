# OUTLINE — RegulasiAI (regulasiai.id), desain website desktop 1440 px

> Tahap 2. Dasar: DNA.md + copy.json (137 teks tampil dari 295 baris brief). Zona px ada di zones.json; wireframe di wire.png (P1 Beranda sudah dilihat; P2-P6 lulus cek otomatis). Satuan px, kanvas 1440 lebar, kontainer konten x150–1290 (1140).

## Ringkasan konsep (3-5 kalimat)
Beranda berjalan seperti portal resmi ala Balad: strip utilitas, header, hero gradien indigo→pink dengan headline + pencarian, kartu putih "jembatan" yang menimpa batas hero, lalu empat section berganti latar (tint biru pucat, gradien navy, putih, lavender pucat) dan footer navy. Halaman dalam memakai pita judul gradien yang sama + satu pola isi per halaman (daftar dokumen, filter, tabel perbandingan, halaman info). Semua blok dipetakan ke widget Elementor Free (container flex, heading, text editor, button, icon box, icon list, image box, tabs, accordion); tidak ada HTML/CSS kustom. Ritme: hero asimetris → grid 3×2 + panel samping → dua kolom tak setara (fitur + panel bertab) → dua kolom (topik + negara) → CTA + teaser → footer.

## Token yang dikunci (diukur dari situs live, bukan ditebak)
- Astra global colors: biru aksi `#086afe`, biru 2 `#257af8`, navy tinta `#031530`, slate `#374c6c`, biru pucat `#ebf5ff`, putih `#ffffff`, abu garis `#e2e8f0`, abu muted `#94a3b8`.
- Gradien hero (dari section buatan pengguna): `#5347E5` → `#E94897`, 150°. Pink hanya aksen kecil (tombol kategori draf, garis aksen judul).
- Font: Outfit 500 (heading), Inter 400/500/600 (badan), dimuat Astra. Kit Elementor masih default (Roboto, `#6EC1E4`): saat build, set kit ke token di atas lebih dulu agar widget mewarisi, bukan menimpa per-elemen.

## Halaman 1 — Beranda (1440 × 3320)
- Fungsi halaman: menjelaskan fungsi situs dan mengarahkan ke pencarian dokumen.
- Zona (y px): strip 0–40 (c029, c227) → header 40–130 (logo c003, menu c043/061/081/104/122/140, tombol cari) → hero 130–730 (h1 c031 56 px; sub c056; kolom cari; tombol c037, c038; kartu pratinjau dokumen) → kartu jembatan 690–890 (c035, tombol c040) → kategori 890–1450 (judul c048; 6 kartu c067–072 3×2; panel navy filter c075–079; tombol pink c073) → Update Terbaru 1450–2010 (c164, c168; tab c170–173; judul isi tab c049/c050; 3 baris dokumen; kartu sorotan) → Topik & Negara 2010–2540 (c051, c138, 11 topik c126–136; c052, 10 ubin negara c087–096) → CTA & teaser 2540–2960 (c144, tombol c039; teaser c175, c187, c204) → footer 2960–3320 (c287, c033, tautan, catatan c290).
- Hierarki baca: 1 headline hero + pencarian; 2 kartu jembatan (deskripsi + tombol pustaka); 3 kategori dokumen; 4 Update Terbaru.
- Aset yang dipakai: tanpa foto. Ikon kategori/topik dari ikon bawaan Elementor (Font Awesome); gradien native; logo teks situs.
- Pemetaan widget Free: hero = container flex kolom gradien; kartu jembatan = container putih + text editor + button; kartu kategori = icon box; panel samping = container navy + icon list; Update Terbaru = Tabs; topik = icon list 2 kolom; ubin negara = container kecil + heading; CTA = container gradien; teaser = image/icon box; footer = container navy + icon list/nav menu.
- Kolom pencarian: butuh solusi non-Pro (belum diputuskan, lihat Risiko).

## Halaman 2 — Regulasi Indonesia
- Fungsi: induk seluruh dokumen Indonesia.
- Zona: pita judul gradien (judul = c061 reuse, sub c065) → chip 7 kategori (c067–073 reuse) → baris filter + pencarian (c075–079 reuse) → 4 kartu dokumen → pagination → footer.
- Hierarki: judul → filter → daftar.
- Aset: tanpa foto; kartu dokumen BARU (contoh).

## Halaman 3 — Regulasi Global
- Fungsi: dokumen negara lain sebagai pembanding.
- Zona: pita judul (c081 reuse, sub c085) → label filter (c098–100) → lencana kartu (c101 "Link ke dokumen asli", c102 "Ringkasan singkat tiap dokumen") → chip 10 negara (c087–096 reuse) → 3 kartu dokumen + ringkasan.
- Hierarki: judul → pilih negara → daftar.

## Halaman 4 — Pustaka Dokumen
- Fungsi: halaman inti seluruh dokumen.
- Zona: pita judul (c140 reuse, sub c144 reuse) → panel navy filter kiri (c157–162) → 3 kartu dokumen kanan → strip label field detail (c146–155).
- Hierarki: filter → hasil → detail field.

## Halaman 5 — Perbandingan Negara
- Fungsi: bandingkan pendekatan antarnegara.
- Zona: pita judul (c104 reuse, sub c108) → kolom label 6 topik (c115–120) + kolom negara (c087–096 reuse) → ringkasan pendekatan per negara.
- Tabel dibuat dari container bersusun (Elementor Free tidak punya widget tabel).

## Halaman 6 — Panduan, Glosarium, Sumber, Tentang, Kontak (halaman info, 5 blok)
- Fungsi: bantuan, istilah, sumber, profil, pengiriman dokumen.
- Zona: Tentang (c217 reuse, c219, c221–225, c008) → Panduan (c175 reuse, c179, c181–185) → Glosarium (c187 reuse, c202, c191–200 sebagai Accordion) → Sumber (c204 reuse, c215, c208–213) → Kontak (c227 reuse, c231, label formulir c233–238).
- Kategori Topik (c122) dan Update Terbaru (c164) memakai pola P2/Beranda; bukan halaman terpisah di wireframe.

## Anggaran tinggi
| Halaman | Zona (tinggi px) | Jumlah | Tinggi halaman |
|---|---|---|---|
| 1 Beranda | strip 40 + header 90 + hero 600 (jembatan menimpa 40) + kategori 560 + update 560 + topik/negara 530 + CTA 420 + footer 360 | 3.160 + overlap 160 | 3.320 |
| 2 Regulasi Indonesia | header 130 + pita 260 + chip/filter 170 + 4 kartu 620 + pager/jeda 120 + footer 360 | 1.660 | 1.660 (kanvas 3.320, sisa kosong) |
| 3 Regulasi Global | 130 + 260 + filter 175 + 3 kartu 600 + jeda 135 + 360 | 1.660 | 1.660 |
| 4 Pustaka Dokumen | 130 + 260 + isi 810 + jeda 200 + 360 | 1.760 | 1.760 |
| 5 Perbandingan | 130 + 260 + tabel 380 + ringkasan 280 + jeda 90 + 360 | 1.500 | 1.500 |
| 6 Halaman info | 130 + pita 200 + 5 blok 1.850 + footer 360 | 2.540 | 2.540 |

## Pemetaan teks
- copy.json = hanya teks yang tampil di situs (137 id). Penanda markdown dibuang (`**`, `>`, `-`, `###`), label brief ("Nama Website:", "Target Pengguna:") dibuang, nomor bagian brief ("4.2") dibuang; teks asli tersimpan di kolom `orig` dan seluruh baris brief di `copy_full.json`.
- Tidak ditampilkan (catatan internal brief, 158 baris): ringkasan proyek, "Bukan:", fokus, tujuan website (c019–025), "Tujuan:" tiap halaman, daftar format konten, tabel struktur data (c254–265, dipakai sebagai acuan field kartu), tone of voice (c267–273), bio sosmed (c275–287 kecuali c287), catatan penting (c289, c291–295: aturan kerja, bukan teks situs). Duplikat: c055, c058–059 sama dengan c031, c037–038.
- Id yang dipakai ulang di beberapa halaman (menu, footer, judul halaman, chip) dipetakan sekali; zona ulang diberi label "reuse".
- BARU (belum dari brief, ditulis saat build; wajib berlabel "contoh"): placeholder kolom cari ("Cari peraturan, kebijakan, pedoman…"); judul/lembaga/tahun pada kartu dokumen contoh (usulan dokumen nyata: UU No. 27/2022 PDP, Surat Edaran Menkominfo No. 9/2023 etika AI, Strategi Nasional KA 2020–2045, EU AI Act, Singapore Model AI Governance Framework, harus diverifikasi ke sumber resmi sebelum tampil); label lencana status (Berlaku/Draf/Dicabut dari brief); isi sel perbandingan negara dan ringkasan per negara.
- Tidak dibuat: statistik/angka jumlah dokumen (belum ada data nyata).

## Risiko Elementor Free (harus diputuskan bersama pengguna sebelum build)
- Pencarian + filter dokumen: Search Form dan Posts/Loop Grid adalah Pro → perlu plugin gratis (taksonomi + filter) tanpa HTML widget.
- Formulir kirim dokumen: widget Form adalah Pro → perlu plugin formulir gratis; cek yang terpasang di regulasi.
- Data dokumen: custom post type + taksonomi (negara, topik, jenis, status), bukan halaman satu-satu.

## Tinjauan diri terhadap DNA
| Butir uji DNA | Terpenuhi oleh |
|---|---|
| Harus 1 (ritme section, kontainer 1140) | P1: latar berganti tint → gradien navy → putih → lavender → navy; padding section 50–90 px; semua zona di x150–1290 |
| Harus 2 (hero gradien + headline + cari + 2 CTA) | zona h1 c031, sub c056, search, cta1 c037, cta2 c038 |
| Harus 3 (pola judul + subjudul + garis aksen) | s2/s3/s4 title + sub di semua section; P2–P5 pita judul + sub-judul |
| Harus 4 (kartu putih konsisten; panel gelap untuk fitur) | cat1–6, kartu dokumen, ubin negara; panel `side`, `tabs_panel`, footer navy |
| Harus 5 (tiap elemen = widget Free) | pemetaan widget Free per halaman di atas; zona `ui` BARU diwujudkan dari container+heading |
| Jangan 1 (HTML/CSS kustom) | tidak ada zona HTML; semua gradien/border/bayangan = kontrol container |
| Jangan 2 (Pro) | risiko Pro ditulis, bukan disembunyikan; putusan sebelum build |
| Jangan 3 (foto politik/stok, statistik) | tanpa foto; tanpa angka; contoh dokumen berlabel |
| Jangan 4 (merah-navy Balad, kampanye) | gradien indigo→pink + biru Astra; tanpa donasi/join us |
| Jangan 5 (kartu identik, glass blur) | ritme variasi 3×2 + panel, tab, 5×2 ubin, teaser; kaca hanya transparansi + border + bayangan |
