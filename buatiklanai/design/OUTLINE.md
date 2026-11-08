# OUTLINE — BuatIklanAI (buatiklanai.id)

> Tahap 2. Dasar: DNA.md + Brief_BuatIklanAI_id.md. Kanvas desktop 1440, konten 1320 di dalam bingkai hairline. Semua blok dipetakan ke widget Elementor Free.

## Peta situs & struktur konten
**Halaman (Elementor):** Beranda · Panduan (hub) · Studi Kasus (hub) · Tren & Riset (hub) · Etika & Kepatuhan · Glosarium · Tentang · Kirim Artikel.
**Halaman "penyimpan posts" = halaman Artikel** (dan arsip kategori/tag/pencarian) → **blog bawaan WordPress yang dirender Astra**, BUKAN Elementor.
**Taksonomi:** Kategori = 9 topik brief §5 + "Panduan" + "Studi Kasus" (hub Panduan/Studi Kasus/Tren/Etika = arsip kategori yang sama, jadi otomatis terisi). Tag = kata kunci bebas. Unggulan = fitur *sticky post* bawaan WP. (Brief §4.2 dan §5 daftar kategorinya beda; usulan: pakai §5 + Panduan + Studi Kasus.)

## Solusi "posts tanpa widget Posts Pro"
| Kebutuhan | Cara (semua gratis) |
|---|---|
| Daftar artikel + paginasi bernomor | Halaman Posts bawaan WP + **Astra Blog (grid 3 kolom)** diatur lewat Bridge `/theme-option` + CSS Tambahan `/custom-css` agar kartu = gaya DNA (hairline, nomor, kategori merah). Paginasi Astra "Number". |
| Filter kategori | Arsip kategori WP + baris "chip" kategori: widget **Categories (WordPress)** di Elementor/ sidebar Astra, atau daftar tautan native. |
| Pencarian artikel | Widget **Search (WordPress)** bawaan Elementor Free + kolom cari di hero. |
| Tag topik | Widget **Tag Cloud** bawaan. |
| Artikel unggulan | Sticky post (arsip memfilter `sticky`) — atau 3 kartu curated native di Beranda. |
| "Artikel terbaru" di Beranda | 3 opsi: (A) **shortcode `[bia_artikel jumlah=6]` di Bridge 1.4.0** + widget Shortcode Free → otomatis, gaya via CSS Tambahan; (B) **kartu native yang disegarkan lewat MCP** tiap ada artikel baru (tanpa kode, tapi manual); (C) widget Recent Posts bawaan (hanya daftar judul). **Rekomendasi: A**, butuh izin Anda + unggah Bridge sekali lagi. |
| "Artikel populer" | WP tidak menghitung baca → tidak dibuat otomatis. Pakai "Pilihan Editor" (sticky/curated), jangan klaim "populer". |
| Halaman satu artikel | Template single Astra (judul, kategori, penulis, tanggal, ringkasan, isi, **Referensi**) — blok Referensi = bagian akhir isi (aturan editorial brief §6/§10). |
| Newsletter (opsional) | Ditunda sampai ada backend (jangan tombol mati). |

## Beranda (1440)
Bingkai hairline mengelilingi seluruh kanvas; setiap sel dibatasi garis 1 px.
1. **Strip atas (Astra header):** logo BuatIklanAI kiri · 3 baris mikro "ARTIKEL / PANDUAN / STUDI KASUS" · menu 5 sel bergaris (Artikel, Panduan, Studi Kasus, Tren & Riset, Tentang) · titik merah (tautan Kirim Artikel). Baris atas kecil: "Dikelola oleh" + logo Asosiasi AI → asosiasi.ai.
2. **Hero:** wordmark **BUATIKLANAI** (Anton ±200 px, selebar bingkai). Bawahnya 3 kolom: kiri = "PAHAMI AI / UNTUK IKLAN / & MARKETING." (Anton 40) + garis + 3 label mikro (ARTIKEL · PANDUAN · STUDI KASUS) + stempel bulat merah; tengah = foto B&W besar miring ±2° beselotip (marketer/layar/papan reklame); kanan = sticky note "referensi, bukan jasa." (Caveat) + teks sub-headline brief + "OLEH ASOSIASI AI INDONESIA" (tertaut) + 2 tombol: **Baca Artikel** (hitam), **Jelajahi Topik** (garis).
3. **Pita pasangan teks (2 baris × 2 sel):** "AI UNTUK" (Anton 120) | "yang bisa diuji" (Caveat 90) ; "IKLAN YANG" (Anton) | "bisa dipercaya." (Caveat) ; sel kecil kanan: BACA / BANDINGKAN / VERIFIKASI / ULANGI.
4. **01 TENTANG** (2 sel): teks deskripsi brief + garis + "EDUKASI, BUKAN JASA." mikro; foto B&W polaroid + sel kanan **02 TOPIK** = daftar 9 kategori (Anton 20, nomor merah, tiap baris tautan ke arsip).
5. **03 ARTIKEL TERBARU** + "LIHAT SEMUA ARTIKEL →": 3 kartu (foto B&W · nomor 001/002/003 · judul Anton · kategori + tahun mikro). Sumber: opsi A/B di atas. Awal: kartu berlabel "contoh".
6. **04 PILIHAN EDITOR / STUDI KASUS** (2 sel): 1 unggulan besar + daftar 3 judul.
7. **Prinsip editorial** (4 sel hairline): Bersumber · Netral · Bukan jasa · Memperhatikan etika (dari brief §7/§8).
8. **CTA:** "LET'S" gaya → "KIRIM IDE" Anton + "artikelmu." Caveat + teks brief §4.9 + tombol **Kirim Usulan** + stempel bulat kecil.
9. **Footer Astra:** strip: BUATIKLANAI · "REFERENSI AI UNTUK PERIKLANAN & DIGITAL MARKETING" · tautan (Tentang, Glosarium, Etika) + logo Asosiasi + © + catatan "Edukasi, bukan jasa".

## Halaman dalam (pola)
- **Artikel (arsip WP/Astra):** pita judul (Anton raksasa "ARTIKEL" + skrip) → baris cari + chip kategori → grid kartu 3 kolom (12/halaman) → paginasi bernomor.
- **Panduan / Studi Kasus / Tren & Riset / Etika:** pita judul + copy brief + arsip kategori (kartu yang sama). Studi Kasus: judul kartu menampilkan ringkas 5 bagian format brief di halaman tunggal.
- **Glosarium:** daftar A-Z accordion native (10 istilah awal brief) dengan sel hairline.
- **Tentang:** latar belakang, tujuan, ruang lingkup, prinsip editorial, pengelola (logo Asosiasi, tertaut).
- **Kirim Artikel:** copy brief §4.9. Form = fitur fungsional → butuh SureForms/OttoKit (izin + akses Google). Sebelum tersambung: tombol nonaktif, tampil email kontak.

## Responsif (satu paket)
Tablet 820: grid 3 → 2 kolom, hero 3 kolom → 1 kolom (foto di bawah judul). HP 390: wordmark 2 baris, semua sel 1 kolom, padding 20-24 px, foto miring dikurangi ke ±1°, menu = hamburger Astra.

## Aset yang dibutuhkan
Logo BuatIklanAI (`Logo_Domain_AI/`, ada di komputer Anda, bukan di repo) + logo Asosiasi AI → WebP; foto Pexels B&W (6-8); stempel bulat WebP; selotip WebP (PNG-transparan tidak boleh → WebP alfa).

## Status situs
Alias `buatiklan` masih **readonly**, belum ada Application Password, Bridge belum terpasang; tema/standar belum dicek. MCP `wp-elementor` tidak tersambung di sesi cloud ini → pemasangan dikerjakan dari Claude Code lokal Anda.
