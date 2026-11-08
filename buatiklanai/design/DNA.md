# DNA — BuatIklanAI (buatiklanai.id), mode A (dari nol, absorb referensi)

> Tahap 1. Referensi = gambar "FRAMEFORM" (portofolio motion designer). Dipakai sebagai DNA tata letak & karakter, BUKAN isi (tidak ada robot/kamera/konten Frameform). Warna dibaca dari gambar (perkiraan visual).

## 1. Brief satu kalimat
Pusat publikasi & referensi AI untuk periklanan/digital marketing (Asosiasi AI Indonesia), bahasa Indonesia, desktop 1440 + tablet 820 + HP 390, untuk marketer, pemilik brand, kreator, mahasiswa; tampilan "majalah cetak / lembar kontak" yang berani, ganjil, dan autentik.

## 2. Batasan keras (aturan proyek + brief)
- Native Elementor Free (container, heading, text editor, button, image, icon list, divider, counter, accordion, tabs, widget WordPress bawaan Free: Search, Categories, Tag Cloud, Recent Posts). TANPA widget Pro (Posts/Loop Grid/Form/Theme Builder). HTML widget hanya fitur fungsional dengan izin.
- Gambar/logo WebP saja. Logo BuatIklanAI + logo Asosiasi AI wajib tampil; setiap teks "Asosiasi AI Indonesia" tertaut https://asosiasi.ai.
- Header/footer = Astra (via Bridge), bukan Elementor.
- Brief §8: tidak menawarkan jasa/produk, tidak menjanjikan hasil, tidak mempromosikan tools, klaim wajib bersumber. Tidak ada statistik karangan; artikel contoh diberi label "contoh".
- Tiga standar situs: Elementor, classic editor, Astra.

## 3. DNA referensi (diukur)
| Aspek | Referensi | Terjemahan untuk BuatIklanAI |
|---|---|---|
| Kertas | krem hangat ≈ `#E8E4D9`, tekstur kertas halus | latar "kertas" `#ECE7DB`; tekstur lewat gambar WebP tipis (opsional) |
| Tinta | hitam pekat ≈ `#0A0A0A` | `#0B0B0B` |
| Sinyal | SATU merah ≈ `#D4281F` (robot, stempel) | satu merah iklan `#D9291C` — dipakai hemat: tombol, stempel, 1 kata judul, garis |
| Judul | sans ultra-padat, tebal, huruf kapital, raksasa (nama brand selebar layar) | **Anton** (Google Font), kapital, tracking -0.01em; judul hero ≈ 200 px desktop / 72 px HP |
| Tulisan tangan | skrip kursif miring sebagai "suara" kedua ("THAT SPEAKS", "NEXT.") | **Caveat** 700, miring sedikit; dipakai hanya untuk 1 frasa per section |
| Label mikro | sans kecil kapital, tracking lebar (≈ 9-10 px) | **Inter** 500, 11 px, kapital, letter-spacing 0.18em |
| Teks badan | sans netral 13-14 px, kolom sempit | Inter 400, 15-16 px (aksesibilitas), kolom ≤ 52ch |
| Struktur | grid garis tipis (hairline 1 px hitam) membagi sel; nomor section 01-04 kecil di kiri; bingkai tipis di pinggir kanvas | container ber-`border` 1 px hitam, tanpa radius, tanpa bayangan |
| Foto | hitam-putih, grain; SATU elemen berwarna (merah) | semua foto di-grayscale ke WebP (bukan filter CSS); aksen merah lewat elemen grafis |
| Elemen "ganjil" | foto ditempel selotip & agak miring; sticky note berisi tulisan tangan; stempel bulat bertulisan melingkar; baris teks miring besar kontras dengan teks tegak | foto polaroid + selotip (rotasi ±2°), sticky note, stempel bulat "AI · IKLAN · EDUKASI", pasangan teks tegak-Anton + skrip-Caveat |
| Footer | strip tipis: nama · slogan kapital kecil · tautan sosial | footer Astra bergaya strip hairline |

Apa yang membuatnya autentik: (1) satu merah + hitam + kertas, tidak ada gradien/ bayangan; (2) skala ekstrem (raksasa vs mikro); (3) garis tipis sebagai arsitektur; (4) sentuhan tangan (selotip, sticky, skrip) yang tidak simetris.

## 4. Adaptasi tema (agar bukan salinan)
- Metafora: **lembar kontak/pasteboard biro iklan** — papan layout, brief ditempel, stempel "TERVERIFIKASI SUMBER".
- Wordmark raksasa: "BUATIKLANAI" selebar layar (Anton), pecah dua baris di HP: BUAT / IKLAN·AI.
- Pasangan judul: "AI UNTUK IKLAN" (Anton) + "yang bisa dipertanggungjawabkan." (Caveat).
- Merah dipakai juga sebagai kode kategori kecil (titik/nomor), bukan warna latar luas.

## 5. Risiko / yang perlu diputuskan
- Font Anton & Caveat dari Google Fonts: dimuat lewat Astra (Customizer) / kontrol tipografi Elementor; cek performa (hanya 2 keluarga, subset latin).
- Rotasi elemen (foto miring) = kontrol Transform Elementor; diverifikasi nyata di editor Free sebelum dipakai. Fallback: gambar polaroid sudah dimiringkan di WebP.
- Stempel bulat bertulisan melingkar = gambar WebP hasil render (bukan SVG/teks).
- Foto: Pexels via env sekali pakai (kunci tidak disimpan), jadi grayscale WebP, kredit di judul media.
