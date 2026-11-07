# DNA — RegulasiAI (regulasiai.id), desain website, mode A (dari nol, absorb referensi)

> Tahap 1. Ukuran dari gambar referensi yang ditampilkan 736 px lebar (skala ≈ 1920 px ÷ 736 = 2,6). Angka bertanda ≈ dibaca dari gambar; ukur pasti dengan `scripts/palette.py` bila berkas gambar asli tersedia.

## 1. Brief satu kalimat
Desain baru (mode A, absorb) beranda + kerangka halaman website pusat dokumen regulasi AI "RegulasiAI" (Asosiasi AI Indonesia), bahasa Indonesia, desktop 1440–1920 px + mobile 390 px, untuk bisnis, pemerintah, akademisi, legal/compliance, developer, mahasiswa; keluarga tata letak mengikuti portal pemerintah/kota (template Balad), bukan isinya.

## 2. Batasan keras (dari permintaan pengguna)
- Teks resmi dari `Brief_RegulasiAI_id.md` (tagline, headline, sub-headline, CTA, copywriting tiap halaman) dipakai apa adanya; teks baru (label UI, placeholder, contoh judul dokumen) ditandai BARU di OUTLINE.md dan dilaporkan.
- Hasil akhir harus dibangun NATIVE di Elementor Free 4.x: container (flex), heading, text editor, button, icon box, icon list, image, counter, tabs, accordion. DILARANG: widget HTML, `<style>`/CSS kustom, widget Pro (form, posts/loop grid, search form pro, dst.), backdrop-blur pada container klasik.
- Situs wajib memenuhi 3 standar: Elementor builder, classic page (Gutenberg nonaktif), tema Astra.
- Tidak ada klaim hukum definitif; selalu arahkan ke dokumen asli (tone brief bagian 7); ada catatan "bukan penyedia layanan hukum" (brief bagian 9).
- Dikerjakan bertahap: DNA dulu (tahap ini), outline menyusul setelah dilihat pengguna.

## 3. Brand DNA
| Hal | Nilai |
|---|---|
| Palet (hex + peran) | PALET PENGGUNA 2026-11-06 "Regal Heritage" (menggantikan biru Astra dan indigo→pink): Midnight Navy `#0B1B3A` (latar gelap, teks, footer), Royal Gold `#C9A24A` (aksen, tombol, ikon; teks di atas emas selalu navy), Ivory Stone `#E8DAC0` (latar section hangat). Turunan: navy 2 `#16305F` (ujung gradien hero), emas tua `#8A6A1F` (teks emas di atas putih/ivory), ivory muda `#F6F0E4`, garis `#E6DCC8`, slate `#445069`. Hex dibaca dari gambar palet (perkiraan visual); ganti bila pengguna memberi hex resmi. Gradien hero: navy 2 → navy 150° + garis emas 4 px. Warna status fungsional: Berlaku `#2f7d5b`, Draf `#8A6A1F`, Dicabut `#a4452c`. Kit Elementor masih default (Roboto, `#6EC1E4`): set ke token ini saat build. |
| Font (heading / body) | DIUKUR dari situs live: Outfit 500 (heading), Inter 400/500/600 (badan), dimuat Astra. Variasi lewat bobot. |
| Logo | Teks "Regulasi AI Indonesia" putih di header gradien (situs live). Berkas logo belum ada; jangan membuat logo baru tanpa persetujuan. |
| Foto | Tidak ada foto kegiatan dari pengguna. Situs repositori dokumen: tanpa foto stok/AI; hero memakai medan gradien brand (native). Bila nanti ada foto asli, warna asli, tanpa tint. |
| Tone | Formal tapi mudah dipahami, netral, berbasis dokumen resmi, tidak promosi berlebihan, tidak menghakimi. |

## 4. Peran referensi
| Referensi | Peran | AMBIL | JANGAN AMBIL |
|---|---|---|---|
| Gambar template "Balad city" (portal kota/pemerintah, 1 halaman panjang) | Tata letak/komposisi + suasana (portal resmi, tepercaya, padat informasi tapi rapi) | urutan section, grid kontainer ≈1140 px, ritme latar antar section, kartu putih di atas latar berwarna, panel samping gelap, judul section + garis aksen kecil, strip utilitas atas, footer 4 kolom + bar hak cipta | foto politik/bendera/gedung kongres, tema pemilu & donasi, konten (walikota, berita, acara, nomor darurat), warna merah-navy aslinya, badge "Join us" bergaya kampanye |
| `Brief_RegulasiAI_id.md` | Sumber konten & struktur halaman | semua copywriting, 12 halaman, fitur, struktur data dokumen, tone | gaya visual apa pun (brief tidak punya) |
| Section buatan pengguna di halaman Testing (container+heading native, gradien indigo→pink) | Palet + cara membangun (native) | hex gradien, cara container bersarang bergradien + kartu putih transparan | lebar `boxed_width` (tidak berefek pada container bersarang; pakai Width) |

Satu kalimat DNA baru: "portal dokumen resmi ala template kota Balad (section berirama, kartu putih, panel gelap) dengan warna indigo→pink RegulasiAI dan dibangun hanya dari widget Elementor Free."

## 5. DNA referensi (diukur)
- Grid & margin: kontainer konten x 150–587 dari 736 = 59% lebar ≈ 1140 px pada 1920; header, hero, footer lebar penuh; kolom 12 (news 4×3, departemen 3 kolom ikon + 1 panel samping, events 5:7, bawah 6:6).
- Jenis blok & proporsi (kosakata, 10 blok):
  1. Strip utilitas atas (tinggi ≈15/736 ≈ 39 px), warna ungu gelap + tombol merah di kanan.
  2. Header putih (≈58/736 ≈ 150 px): logo tengah, menu bawah, pencarian + tombol "donate" merah kecil.
  3. Hero bidang penuh (≈270/736 ≈ 700 px): foto + overlay duotone, judul besar kiri, subjudul miring, 1 tombol pil merah.
  4. Kartu "jembatan" yang menimpa batas hero dan band indigo di bawahnya (foto kiri + teks sambutan kanan), menyambungkan dua section.
  5. Section judul + subjudul kecil + garis merah pendek (dipakai di semua section).
  6. Grid kartu putih berfoto atas (berita 4 kolom): label kategori berwarna di pojok foto, meta kecil, judul 2 baris, cuplikan, baris penulis.
  7. Grid kartu ikon bulat berwarna (departemen 3×2) + panel samping gelap berisi akordeon dan tombol merah.
  8. Section latar gradien gelap penuh (acara): fitur foto besar kiri + panel putih bertab kanan berisi daftar.
  9. Daftar ikon bulat navy dalam kotak berbingkai tipis + kartu foto potret.
  10. Kartu CTA merah (formulir langganan) + tiga kartu angka besar; footer hitam 4 kolom + kartu sosial navy + bar merah hak cipta.
- Skala tipografi ≈ (di 1920 px): judul hero 56–64 px bold putih; judul section 28–32 px bold; judul kartu 15–16 px semibold; meta/label 11–12 px; badan 14–15 px; angka besar 40 px.
- Kepadatan & ritme ruang putih: padding vertikal section ≈ 85–95 px (≈33–36/736), jarak antarkartu ≈ 30 px; latar berselang-seling terang → tint pink-lavender → gradien gelap → putih → lavender pucat → hitam, sehingga tiap section punya identitas warna sendiri.
- Apa yang membuatnya elegan: (1) ritme latar section penuh yang berganti warna; (2) kartu putih konsisten (radius kecil, bayangan lembut) di atas latar berwarna; (3) hierarki seragam: judul + subjudul + garis aksen di setiap section, satu aksen merah untuk aksi.
- Yang BEDA antar section (variasi tata letak): hero asimetris; grid 4 kolom seragam; grid 3×2 + sidebar; dua kolom tidak setara (fitur besar + panel bertab); dua kolom setara; baris CTA+angka; footer 4 kolom.

## 6. Niat per elemen
| Elemen | Untuk apa ada | Tingkat fidelitas |
|---|---|---|
| Hero dengan headline + search bar | Mengarahkan pengguna langsung ke pencarian dokumen (fungsi inti brief 4.1) | Sedang: tata letak final; search bar harus nyata bisa dipakai (butuh solusi non-Pro, lihat risiko) |
| Kartu kategori dokumen / topik / negara | Memudahkan telusur lewat topik & negara | Sedang-tinggi: isi nyata dari brief (11 topik, 10 negara) |
| Daftar "Regulasi terbaru" (Indonesia / global) | Menunjukkan koleksi hidup | Tinggi: contoh dokumen harus ditandai BARU/contoh; jangan memalsukan dokumen resmi |
| Panel samping status dokumen (berlaku/draf/dicabut) | Membantu membaca status | Sedang |
| Kartu angka (jumlah dokumen, negara) | Hanya bila angkanya nyata | Tidak dibuat bila angka belum ada (anti statistik karangan) |
| Footer + catatan "bukan layanan hukum" | Kepatuhan tone & brief bagian 9 | Tinggi |

## 7. Daftar larangan
Umum: lihat references/anti-patterns.md. Khusus proyek ini:
- KEPUTUSAN PENGGUNA 2026-11-06 (menggantikan larangan HTML mutlak): tampilan/tata letak tetap 100% native Elementor. Widget HTML BOLEH hanya untuk FITUR fungsional (pencarian + filter dokumen, kolom input kirim dokumen). Formulir kirim dokumen cukup input sederhana yang disimpan ke spreadsheet (bukan formulir resmi/Pro). Risiko Free lain dinyatakan "clear" oleh pengguna. Desain dikerjakan dulu di sini (html-design-studio), lalu dipasang ke situs lewat /wp-elementor.
- Widget HTML untuk gaya/visual, CSS kustom, widget Pro untuk tampilan (pengguna kecewa saat HTML dipakai; fokus: dapat diedit orang lain di editor).
- Backdrop-blur/glass pada container klasik Elementor Free (tidak ada kontrolnya); kaca hanya transparansi + border + bayangan.
- Foto politik, bendera, atau foto stok/AI sebagai pengganti kegiatan nyata; tidak ada tint pada foto.
- Statistik/angka karangan, dokumen resmi palsu; contoh dokumen wajib berlabel contoh.
- Klaim hukum definitif, kata promosi berlebihan, gaya kampanye/donasi (tombol "Join us", "Donate").
- Meniru warna merah-navy Balad; palet memakai indigo `#5347E5` → pink `#E94897`.
- Mengubah copywriting brief; menambah slogan yang tidak diminta.
- Menyentuh atau menghapus section buatan pengguna di halaman Testing.

## 8. Uji DNA
Hasil harus terasa seperti: portal resmi yang tepercaya dan rapi seperti template kota Balad, berirama warna per section, tetapi bernuansa indigo→pink RegulasiAI dan murni dari widget Elementor Free. Bukan seperti: blog/portal berita, situs konsultasi hukum, landing page kursus, atau situs kampanye politik.

Harus (5):
1. Urutan section berirama: latar berganti (terang, tint, gradien, putih) dengan padding ≈ 90 px, kontainer ≈ 1140 px.
2. Hero gradien brand + headline brief + search bar + 2 CTA brief ("Cari Dokumen", "Lihat Regulasi Indonesia").
3. Setiap section memakai pola judul + subjudul kecil + garis aksen pendek, sama di semua halaman.
4. Kartu putih konsisten (radius, bayangan lembut) untuk dokumen, topik, negara; panel gelap/gradien untuk fitur & perbandingan.
5. Setiap elemen dapat dipetakan ke satu widget/pengaturan bawaan Elementor Free (dicatat di OUTLINE.md per blok).

Jangan (5):
1. Widget HTML atau CSS kustom.
2. Widget Pro atau fitur yang tidak ada di Free tanpa solusi tertulis.
3. Foto politik/stok, tint foto, statistik karangan.
4. Merah-navy Balad atau konten kampanye (donasi, "join us").
5. Kartu identik berulang tanpa variasi skala/posisi; glass blur palsu.

## 9. Risiko Elementor Free yang harus diputuskan di OUTLINE (bukan ditanyakan sekarang)
- Search bar & filter dokumen (negara/tahun/topik/jenis/status): widget Search Form dan Posts/Loop Grid adalah Pro; butuh pendekatan non-Pro (plugin pustaka dokumen/taksonomi + shortcode) dan harus lolos aturan "tanpa HTML widget".
- Formulir "Kirim Dokumen": widget Form adalah Pro; butuh plugin formulir gratis (cek apa yang sudah terpasang di regulasi).
- Tabel perbandingan negara: Elementor Free tidak punya widget tabel; opsi: container bersusun (native) atau plugin tabel.
- Data dokumen (struktur brief bagian 6): kemungkinan custom post type + taksonomi; perlu keputusan terpisah dengan pengguna.

## 10. Pelajaran (isi setiap ada koreksi pengguna; jangan dihapus)
- 2026-11-05: jangan memakai widget HTML/CSS kustom sebagai jalan pintas; bangun dari kontrol bawaan Elementor Free agar mudah diedit orang lain; jangan defensif, terima faktanya lalu perbaiki.
- 2026-11-05: `boxed_width` diabaikan pada container bersarang; pakai kontrol Width (px) + Width mobile (%).
- 2026-11-05: editor Elementor pengguna bisa menimpa tulisan MCP dengan data lama; minta reload editor sebelum mengedit.
