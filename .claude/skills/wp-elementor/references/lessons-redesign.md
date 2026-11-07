# Pelajaran dari redesign regulasiai.id (2026-11): BACA sebelum membangun / redesign situs

Setiap butir di sini lahir dari revisi berulang pengguna. Terapkan di awal, jangan menunggu ditegur.

## 0. Urutan kerja yang benar
1. Desain dulu di `html-design-studio` (DNA → outline → HTML), pengguna setuju, BARU pasang ke situs.
2. Pasang ke halaman DRAF/halaman baru dulu; Home/halaman lama diganti lewat `apply_draft` setelah OK (atau langsung bila pengguna bilang "ganti semua").
3. Setiap halaman diverifikasi di TIGA ukuran sebelum dilaporkan: desktop 1440, tablet ~820, HP 390 (browser pane: `resize_window` + JS cek overflow; `visual_check` hanya desktop+HP). Responsif adalah satu paket dengan desktop, bukan tahap tambahan.
4. Lapor jujur apa yang BELUM dicek/diganti. Jangan klaim "sudah rapi" tanpa screenshot.

## 1. Aturan pengguna (keras)
- Tampilan = widget bawaan Elementor Free. Widget HTML HANYA untuk fitur fungsional (pencarian/filter/form) dan hanya dengan izin pengguna. Jangan pernah untuk gaya.
- Gambar/logo WAJIB WebP terkompres. Dilarang PNG/JPG/JPEG di situs. `media_upload` dengan path lokal otomatis mengubah ke WebP (cek hasilnya `.webp`).
- Logo brand situs + logo Asosiasi AI (`E:\1. Code\logo-asosiasi-ai`, brand domain di `E:\1. Code\Logo_Domain_AI`) wajib terpampang jelas. Setiap teks "Asosiasi AI Indonesia" wajib jadi tautan ke `https://asosiasi.ai` (tab baru, `rel="noopener"`).
- Bendera negara wajib bila ada daftar/ubin negara (ambil dari flagcdn → `media_upload` slot icon → WebP). Emoji bendera tidak tampil di Windows.
- Ikon: kecil dan seragam (lingkaran ~35-50 px, ikon 14-22 px), sejajar rapi. Jangan ikon besar dan jangan asal tempel.
- Foto: manfaatkan Pexels API semaksimal mungkin (hero, pita judul, kartu). Kunci API hanya lewat env sekali pakai, JANGAN disimpan di berkas/memori. Pilih foto formal, beri overlay navy, alt deskriptif, kredit fotografer di judul media.
- Daftar dokumen = KARTU (bendera, label jenis, judul, sumber, tahun, tombol) + sidebar filter + pagination BERNOMOR. Dilarang daftar polos dan dilarang "muat lebih banyak". Klik kartu membuka tautan asli di tab baru.
- Data yang diturunkan otomatis (jenis/tahun/sumber dari judul+URL) wajib diberi label "perkiraan otomatis".
- Jangan menyentuh/hapus section buatan pengguna kecuali diminta. Halaman template bawaan boleh diganti bila pengguna bilang boleh (hapus = trash, bukan permanen).

## 2. Header & footer di Elementor FREE = tema Astra (BUKAN Elementor)
- Elementor Free tidak punya Theme Builder; `[elementor-template]` juga Pro. Jangan menyalin header/footer manual ke tiap halaman.
- Atur lewat bridge ≥1.2.0: `GET/POST /claude/v1/theme-option` (opsi `astra-settings`, merge level atas + backup 1 versi; `theme_mods` custom_logo & nav_menu_locations), `/claude/v1/custom-css` (CSS Tambahan), `/claude/v1/flush`. Konten footer = widget blok: `POST /wp/v2/widgets` ke sidebar `footer-widget-N`.
- Kunci Astra yang terbukti: `header-desktop-items` / `header-mobile-items` (mobile-trigger = hamburger), `header-html-1/2`, `header-button1-text` & `-link-option`, `footer-desktop-items` (widget-1..3, copyright), `footer-copyright-editor`, `global-color-palette` (palet global = cara terbaik mewarnai tema), `transparent-header-enable`, `mobile-header-breakpoint`, `ast-header-responsive-logo-width`, `display-site-title-responsive`.
- Jebakan: `header-logo-color` (mis. #fefefe) mengubah logo jadi putih → kosongkan. Header transparan menimpa isi halaman → matikan. Widget footer yang dibuat sebelum sidebarnya terdaftar masuk `wp_inactive_widgets` → buat setelah settings tersimpan, lalu pindahkan (`POST /wp/v2/widgets/<id> {sidebar}`). Beberapa kunci warna Astra tidak berpengaruh → pakai CSS Tambahan (selektor `.ast-above-header-bar`, `.main-header-menu-toggle`, `.site-primary-footer-wrap[data-section=...]` dengan `!important`).
- Pengaturan header bisa ter-reset (mis. baris atas hilang) bila Customizer disimpan pengguna → verifikasi ulang setelah perubahan besar; ubah header hanya lewat bridge.
- Menu: item halaman harus diset `object_id`+`object:"page"`+`type:"post_type"` (mengganti `url` saja tidak ubah tautan).

## 3. Halaman Elementor di tema Astra
- Meta halaman agar tidak terjepit 1200px: `ast-site-content-layout=full-width-container`, `site-content-layout=page-builder`, `site-content-style=unboxed`, `site-sidebar-layout=no-sidebar`; template `elementor_header_footer`. Kosongkan meta `ast-main-header-display`/`footer-sml-layout` agar header/footer Astra tampil.
- Container bersarang punya padding bawaan 10px → set padding 0, kalau tidak baris ber-lebar px akan terlipat. `boxed_width` diabaikan pada container bersarang → pakai `width` (px) + `width_tablet`/`width_mobile` (%).
- Setiap container top-level boxed wajib punya `padding_tablet` & `padding_mobile` sisi 20-24px (padding 0 membuat teks menempel ke tepi layar). Baris dengan anak berlebar px → `flex_wrap: wrap` + `width_tablet: 100%`.
- icon-box: kosongkan `description_text` (bawaan "Lorem ipsum"); `position_mobile/position_tablet: left` agar ikon tetap di kiri teks; ukuran ikon via `icon_size` + `icon_padding`.
- Tombol: Astra menambah border biru → set `border_border: solid`, `border_width` 0, `border_color` transparan. Warna tombol/teks selalu eksplisit.
- Tabel lebar di text-editor → bungkus `<div style="overflow-x:auto">` dan beri `min-width` (kalau tidak, halaman HP melebar).
- Hero beroverlay foto: `background_image` + `background_overlay_background: classic` + `background_overlay_color` + `background_overlay_opacity`.
- Kartu menimpa hero: container luar transparan dengan margin atas negatif + gradien `hard stop` agar latar di bawahnya menyambung.
- Gambar via `media_upload`; pasang `image_size` "full" hanya bila memang lebar penuh (peringatan perf).

## 4. Fitur fungsional (HTML widget + JS) — izin pengguna 2026-11-06
- Guardrail memblokir `<script>`. Pengecualian sempit: widget html boleh memuat script bila mengandung penanda `<!-- allow-js:<alasan> -->` dengan ALASAN TERISI (penanda kosong tetap diblokir; dilindungi unit test `perfLint: <script> hanya lolos bila ada penanda allow-js`). Minta izin pengguna dulu dan sebut alasannya.
- Status tes: `npm test` (14 tes) + `npm run typecheck` lulus. Belum ada tes otomatis untuk bridge PHP 1.2.0 dan `scripts/push-element.ts` (terbukti hanya lewat pemakaian live di regulasi); `npm run e2e` belum dijalankan setelah perubahan ini. Jalankan `npm test` setiap mengubah `src/`.
- Payload besar (mis. 100+ dokumen) jangan diketik di panggilan tool: bangun JSON elemen dengan skrip Python (`regulasi/design/build_library.py` jadi contoh) lalu `node wp-elementor-mcp/scripts/push-element.ts <site> <page_id> <parent|null> <index> <berkas.json> <domain> [alasan]` (tetap lewat MCP: backup, rev, verifikasi).
- Pola pustaka: data JSON di `<script type=application/json>`, kartu dirender JS, filter (negara berbendera, jenis, tahun, sumber), cari, urut, pagination 12/halaman, dukungan `?q=` dari kolom cari Beranda. Uji nyata di browser: klik halaman, filter, cari, reset.
- Form kirim dokumen: jangan aktifkan tombol sebelum backend (mis. SureForms+OttoKit→Google Sheets) tersambung; jangan terima kiriman yang hilang.

## 5. Pengaman & izin
- Publikasi halaman (`status: publish`) via `wp_request` diblokir mode otomatis sampai pengguna menyetujui di chat. Tanyakan sekali, lalu terbitkan.
- `wp_request` POST/PUT memuat `status` draft/trash → butuh `confirm:true`. SELALU isi `fields` pada POST/GET `wp_request` (tanpa itu balasan halaman ±5 KB per panggilan).
- Koneksi sempat "fetch failed" tetapi operasi kadang SUDAH terjadi → cek ulang (outline) sebelum mengulang.
- Tool `elementor_update` memakai `changes[].id` (bukan `element_id`); `visual_check` memakai `op`+`url`+`label`; `elementor_outline` memakai `page_id`.
- Rev berubah setelah menyimpan meta halaman/aksi lain → baca ulang outline (max_depth 0) sebelum menulis.

## 6. Plugin yang sering tersedia di situs Astra Starter
- Header-Footer-Elementor ("Ultimate Addons"): CPT `elementor-hf` tidak terekspos REST → tidak bisa dibuat lewat MCP; pakai Astra builder.
- SureForms + OttoKit (SureTriggers): form & integrasi Google Sheets. SureCookie: banner cookie (menutupi screenshot; bukan bug).
