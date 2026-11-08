# HANDOFF: melanjutkan proyek ini di perangkat lain

Terakhir diperbarui: 2026-11-07. Bahasa kerja dengan pemilik: **Indonesia**. Pemilik detail soal desain, benci revisi berulang, dan lebih suka rencana rinci lalu eksekusi mandiri. Lapor jujur apa yang BELUM dicek.

## 1. Apa proyek ini
Mengelola 9 situs WordPress + Elementor (Free) milik pemilik dari Claude Code, tanpa browser:
- **`wp-elementor-mcp/`**: MCP server (Node/TS, 14 tool) + plugin WordPress **Claude Bridge** (`bridge-plugin/`, versi terbaru 1.3.0) + skrip (`scripts/`).
- **`.claude/skills/wp-elementor/`**: skill kerja (alur, guardrail, **`references/lessons-redesign.md` = pelajaran penting, baca dulu**).
- **`CLAUDE.md`**: aturan proyek (standar wajib, native-first, logo, responsif).
- **`sites/`**: brief + sumber desain per situs (lihat `sites/README.md`) situs regulasiai.id (DNA, outline, HTML mock, generator).
- **`docs/memory/`**: salinan memori Claude (lihat §8). **`config/`**: contoh config; `sites.local.json` RAHASIA (tidak ada di repo).

## 2. Setup di perangkat baru
1. Node ≥ 22.18, Git, Claude Code (atau desktop app). Python 3 + `pip install openpyxl pillow` (untuk generator).
2. `git clone https://github.com/jordanshankara/mcp-elementor.git` lalu `cd mcp-elementor/wp-elementor-mcp && npm install`.
3. Buat `config/sites.local.json` dari `config/sites.example.json` (format: `url`, `user`, `app_password`, `label`, `env`, `readonly`, `tags`). **Password aplikasi diminta dari pemilik/dibuat ulang; JANGAN dikomit, JANGAN ditampilkan di chat.**
4. `.mcp.json` di root sudah menunjuk `wp-elementor-mcp/src/index.ts`; buka Claude Code di folder repo, setujui server MCP `wp-elementor`.
5. Aset yang TIDAK ada di repo (gambar/biner): `logo-asosiasi-ai/`, `Logo_Domain_AI/` (logo), `sites/regulasi/_AI Regulations.xlsx` (data dokumen, ADA di repo), laporan screenshot (`reports/`), backup halaman (`backups/`). Minta pemilik menyalin logo bila perlu; build logo → upload `media_upload` (WebP).
6. Bangun ulang plugin bridge bila perlu: `cd wp-elementor-mcp && node scripts/build-zip.ts` → `dist/claude-bridge.zip` (tidak di repo).
7. Tes: `npm test` (14 tes) dan `npm run typecheck`.

## 3. Daftar situs (alias → domain). Status per 2026-11-07
| alias | domain | status |
|---|---|---|
| **regulasi** | regulasiai.id | TERHUBUNG, mode tulis, sudah di-redesign penuh (lihat §4) |
| **pusatriset** | pusatriset.ai | TERDAFTAR, mode tulis. Elementor 4.3.6 + Classic Editor AKTIF. **Menunggu pengguna mengunggah Bridge 1.3.0** → lalu pasang Astra via `POST /claude/v1/theme-install {slug:"astra",activate:true}`. Tema aktif masih Twenty Twenty-Five |
| bikinkonten, buatiklan, toolsai, analisadata, solusiindustri, solusikeamanan, institut | bikinkontenai.id, buatiklanai.id, toolsaigratis.id, aianalisadata.id, aisolusiindustri.id, aisolusikeamanan.id, institutnasional.ai | readonly; belum ada Application Password sah + Bridge. Urutan berikutnya: bikinkonten |
Standar wajib tiap situs: (1) Elementor builder, (2) classic page / Gutenberg nonaktif, (3) tema Astra.

## 4. regulasiai.id (situs selesai pertama)
- **Palet "Regal Heritage"**: navy `#0B1B3A`, emas `#C9A24A`, ivory `#E8DAC0`; turunan navy2 `#16305F`, emas tua `#8A6A1F`, ivory muda `#F6F0E4`, garis `#E6DCC8`, slate `#445069`. Font Outfit (judul) + Inter (teks). Hex dibaca dari gambar palet pengguna (perkiraan).
- **Halaman:** Home #275 (Beranda baru), Regulasi Indonesia #541, Regulasi Global #542, Pustaka Dokumen #543, Perbandingan Negara #544, Informasi #545 (Tentang/Panduan/Glosarium/Sumber/Kontak). Testing #526 (milik pengguna, jangan disentuh). Halaman template lama dibuang ke trash.
- **Pustaka dokumen** (218 dokumen dari `_AI Regulations.xlsx`): widget HTML + JS (izin pengguna, penanda `<!-- allow-js:... -->`), kartu + sidebar filter + pagination bernomor 12/halaman, `?q=` dari kolom cari hero. Dibangun oleh `sites/sites/regulasi/design/build_library.py` → `library_*.json` → `node wp-elementor-mcp/scripts/push-element.ts regulasi <page_id> null <index> <json> regulasiai.id "<alasan>"`. Jenis/tahun/sumber = **perkiraan otomatis** dari judul+URL (diberi label).
- **Header/footer = Astra Customizer via Bridge** (BUKAN Elementor): `/claude/v1/theme-option` (astra-settings), `/custom-css`, `/flush`; footer = widget blok di `footer-widget-1..3`. Menu "Main Menu" (id 3). Logo situs (custom_logo) = logo RegulasiAI WebP; strip atas: "Dikelola oleh" + logo Asosiasi AI → https://asosiasi.ai. Setiap teks "Asosiasi AI Indonesia" wajib tertaut ke https://asosiasi.ai.
- **Media** (WebP, di server): foto Pexels (hero, pita judul, kartu update), 13 bendera, logo brand & asosiasi, favicon. API Pexels dipakai sekali lewat env, **kunci tidak disimpan**.
- **Belum selesai:** form Kirim Dokumen (tombol nonaktif; rencana SureForms + OttoKit → Google Sheets, butuh akses Google pengguna); data contoh "contoh" di Update Terbaru & Perbandingan Negara; cek visual HP/tablet halaman lain menyeluruh; Kategori Topik belum punya halaman; template library Elementor #563/#565 (header/footer lama) tidak terpakai (boleh dihapus).
- Sumber desain: `sites/regulasi/design/` (DNA.md, OUTLINE.md, `build_site.py` → p1..p6.html, `copy.json`). Proses desain memakai skill `html-design-studio` (DNA → outline → desain, lalu pasang ke situs lewat skill `wp-elementor`).

## 5. Aturan keras pemilik (ringkas; rincian di `lessons-redesign.md`)
- Tampilan = widget bawaan Elementor Free. HTML widget HANYA fitur fungsional dengan izin (pencarian/filter/form). Dilarang untuk gaya.
- Gambar/logo wajib **WebP** terkompres (dilarang PNG/JPG). Logo brand situs + logo Asosiasi AI wajib terpampang. Bendera negara wajib untuk daftar negara.
- Ikon kecil, seragam, rapi. Daftar = kartu + filter + **pagination bernomor** (bukan "muat lebih banyak").
- Header/footer = Astra. Elementor Pro dilarang (jangan pakai widget Pro).
- Semua halaman dicek di **desktop, tablet, HP** sebelum dilaporkan selesai.
- Publikasi halaman via `wp_request` diblokir mode otomatis sampai pengguna menyetujui di chat.
- Konfirmasi sebelum operasi destruktif/tingkat situs. Tanyakan situs bila tidak disebut.

## 6. Cara kerja (ringkas)
`sites_list` → pilih alias persis → `elementor_outline` (rev) → `elementor_get` seperlunya → `elementor_update`/`elementor_structure` (batch, pakai `rev` + `confirm_domain` situs PROD) → `visual_check` + cek tablet/HP di browser pane. Gunakan `fields` pada `wp_request`. Payload besar → `push-element.ts`.

## 7. Keamanan: TINDAK LANJUT wajib
- Password admin 8 situs (dulu ditempel di chat) dan Application Password pusatriset.ai pernah terlihat di percakapan → **buat ulang/cabut**. Kunci API Pexels juga pernah ditempel di chat → rotasi di dashboard Pexels.
- Repo ini TIDAK berisi rahasia: `config/sites.local.json`, `sites.playground.json`, `backups/`, `reports/`, gambar, zip, `node_modules/` ada di `.gitignore`.

## 8. Memori Claude (log lintas sesi)
Memori asli ada di `~/.claude/projects/<proyek>/memory/` (tidak ikut git). Salinannya ada di `docs/memory/` (`MEMORY.md` indeks, `wp-elementor-project.md`, `elementor-native-first.md`). Di perangkat baru: salin isi `docs/memory/` ke folder memori proyek Claude Code, atau cukup baca file ini + skill (isinya sudah memuat semuanya).

## 9. Langkah berikutnya yang disarankan
1. pusatriset.ai: pengguna unggah Bridge 1.3.0 → pasang Astra → set up header/footer, logo "Pusat Riset AI Indonesia" (`Logo_Domain_AI/Pusat Riset AI Indonesia`), brief & desain via `html-design-studio`.
2. regulasi: sambungkan form Kirim Dokumen ke Google Sheets; ganti data "contoh"; cek ulang visual tablet/HP seluruh halaman; hapus template #563/#565.
3. Hubungkan 6 situs lain satu per satu (Application Password + Bridge 1.3.0), terapkan 3 standar + pelajaran redesign.
4. Tambah tes untuk Bridge PHP & `push-element.ts`; jalankan `npm run e2e`.
