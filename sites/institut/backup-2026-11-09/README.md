# Backup publik institutnasional.ai — 2026-11-09 (SEBELUM dirombak)

Diambil TANPA login (REST publik + HTML tampilan). Isi: `site-info.json`, `pages/` (konten + teks per halaman), `html/` (HTML render semua halaman + beranda), `posts.json` (5 artikel), `categories.json`, `tags.json`, `media.json` (89 berkas), `types.json`, `users.json`.

## Halaman (urutan penting)
| id | slug | judul | catatan |
|---|---|---|---|
| 423 | home-copy | Home – Copy | **halaman depan yang tayang** (`/`), ±43 KB Elementor |
| 66 | institut-ai-nasional | Home | beranda lama/duplikat (`/institut-ai-nasional/`) |
| 64 | about-us | About Us | **isinya masih berguna** (naskah Tentang, Visi, Misi) — teks di `pages/64-about-us.txt` |
| 60 | faculties | Faculty | bertentangan dengan brief |
| 62 | contact-us | Contact Us | form (Contact Form 7) |
| 58 | blog | Blog | halaman posts |

## Yang TIDAK ada di backup ini (butuh login/Bridge)
`_elementor_data` asli tiap halaman, pengaturan Customizer/tema bosa, menu, widget, formulir Contact Form 7, pengaturan Yoast SEO, WooCommerce, ElementsKit/Essential Addons, daftar plugin lengkap, database. **Sebelum merombak: lakukan backup penuh** (mis. UpdraftPlus/hosting) dan/atau jalankan backup Bridge (`/claude/v1/elementor/<id>` + `/backups`) setelah kredensial & Bridge tersedia.

## Temuan penting (konten lama vs brief baru)
Konten lama memosisikan situs sebagai **lembaga pendidikan & riset** ("1.500+ alumni", "10+ program studi", "50+ tenaga pengajar", program/kurikulum, testimoni pejabat, "Call us", alamat Jakarta Selatan, mitra "Di Dukung Oleh", tema bosa + WooCommerce add-on). Brief baru: BUKAN lembaga pendidikan formal/penyedia kursus/pelatihan; tanpa klaim tanpa sumber; struktur Home, Artikel, Kategori, About, Kontak. Perlu keputusan pemilik sebelum merombak.
