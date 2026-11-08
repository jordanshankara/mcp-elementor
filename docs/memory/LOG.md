# LOG memori proyek (kronologis, terbaru di atas)

Log kerja lintas sesi/perangkat. Tidak berisi rahasia. Pemilik: berbahasa Indonesia, detail soal desain, benci revisi berulang, lebih suka rencana rinci lalu eksekusi mandiri, ingin laporan jujur tentang yang BELUM dicek. Sesi ini dijalankan dari **claude.ai/code di HP (sesi cloud)**.


## 2026-11-08 (lanjutan) — izin jaringan semua situs & audit publik awal
- `update_environment` disetujui: Allowed domains kini memuat apex + `www.` untuk bikinkontenai.id, aisolusikeamanan.id, toolsaigratis.id, aianalisadata.id, aisolusiindustri.id, institutnasional.ai, pusatriset.ai, regulasiai.id (+ buatiklanai.id). Semua terjangkau (HTTP 200).
- **Audit publik (tanpa login)**: 
  - `bikinkonten`: WP + Elementor + Astra-style starter (sama dengan buatiklan sebelum diredesain), namespace `claude/v1` (Bridge SUDAH terpasang), `elementor/v1`, `sureforms/v1`. Masih template starter: menu Beranda/Tentang/Penawaran/Donasi/Blog/Kontak; heading "Tutorial Praktis, Koleksi Alat, Pelatihan Gratis, Mentorship, Kompetisi Kreatif, Kursus Video, Template Kreatif, Bergabunglah Bersama Kami"; footer berisi telepon 083145916630 & email jordanshankara@gmail.com (data bukan asosiasi.ai); 3 post contoh "Your awesome post title goes here"; halaman starter Shop/Checkout/Dashboard(SureCart)/Offering/Donate/Sample; 8 gambar JPEG (dilarang, harus WebP); TIDAK ada Dian Martin / Supported by / asosiasi.ai / WhatsApp / disclaimer edukasi. Kategori: General, Uncategorized saja. Halaman brief (Artikel, Kategori, About, Kontak) belum sesuai.
  - `aisolusikeamanan`, `toolsai`, `analisadata`, `solusiindustri`: WordPress kosong, tema Twenty Twenty-Five, tanpa Elementor, tanpa Bridge, 1 halaman (Sample) + 1 post contoh.
  - `institut`: tema **bosa** (bukan Astra) + Elementor (ada `elementor/v1`), tanpa Bridge; halaman: home-copy, blog, faculties, contact-us, about-us, institut-ai-nasional; 5 post. Perlu migrasi ke Astra + dibersihkan (ada halaman "faculties" yang bertentangan brief).
  - `pusatriset`: tema terdeteksi **Astra** (berarti sudah terpasang/diganti pemilik), `claude/v1` (Bridge aktif) + `elementor/v1`; hanya Sample Page; konten belum dibangun.
  - `regulasi`: Astra + Elementor + Bridge + SureForms; halaman: informasi, perbandingan-negara, pustaka-dokumen, regulasi-global, regulasi-indonesia, testing, home; `asosiasi.ai` tertaut (3 kali) tapi "Supported by"/Dian Martin belum ada.
- **bikinkonten TERHUBUNG** (user `adminbikinkonten`, audit privat dilakukan; lihat `config/sites/bikinkonten.md`): bridge 1.3.0, Elementor Free, Astra, administrator; Classic Editor tidak terpasang; 39 JPEG + 1 PNG; 63 elemen starter di Home; palet biru bawaan. Mode config lokal readonly sampai pemilik mengizinkan tulis.
- Belum ada kredensial untuk 6 situs selain buatiklan → audit privat (site_health, plugin, pengaturan) menunggu username + Application Password.

---

## 2026-11-08 (sesi cloud, branch `claude/clever-hypatia-6agnmk`)

### A. Pemahaman proyek & lingkungan
- Repo: github.com/jordanshankara/mcp-elementor. Satu commit awal 32dd226 (2026-11-07), lalu 9 commit sesi ini (lihat §H).
- **MCP `wp-elementor` TIDAK tersambung di sesi cloud** (CONNECTION_CLOSED; tidak ada node_modules/sites.local.json). Cara kerja yang dipakai: jalankan engine sendiri lewat CLI:
  ```
  cd wp-elementor-mcp && npm install
  export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_NO_WARNINGS=1
  node src/cli.ts <tool> '<json>'          # mis. site_health, elementor_outline, elementor_page
  ```
  `NODE_USE_ENV_PROXY=1` WAJIB (fetch Node tidak memakai proxy sandbox secara default). `config/sites.local.json` dibuat di container (gitignored, rahasia, ephemeral) untuk alias `buatiklan`.
- **Jaringan sandbox**: host harus diizinkan di environment ("Default Cloud Environment" → Allowed domains). Sudah ditambahkan: `buatiklanai.id`, `www.buatiklanai.id`. Situs WP memakai `www.` (site_url) → butuh kedua host. Tambah host baru lewat `update_environment` (butuh persetujuan kartu di app) atau pengaturan environment di app.
- **Push GitHub** sempat 403 ("Claude doesn't have GitHub access"); beres setelah pemilik menghubungkan ulang GitHub / memasang Claude GitHub App (https://claude.ai/connect-github). Sekarang push ke branch di atas berhasil.
- Pekerjaan langsung ke situs dilakukan lewat: (1) CLI engine MCP (guardrail, rev, backup) dan (2) `curl` ke REST WP + endpoint Bridge `/claude/v1/*` (skrip Python di `sites/buatiklan/design/`). Klasifier otomatis sempat menolak perubahan header global sampai pemilik menyetujui eksplisit di chat.
- Bridge 1.3.0 dibangun ulang (`node wp-elementor-mcp/scripts/build-zip.ts` → `dist/claude-bridge.zip`, tidak di repo) dan dikirim ke pemilik. Pemilik mengunggahnya ke pusatriset.ai dan buatiklanai.id (buatiklanai.id terkonfirmasi: bridge 1.3.0 aktif).

### B. Studi repo `jordanshankara/pusatrisetai` (BUKAN WordPress)
- Aplikasi Next.js (App Router) + Prisma + MySQL/MariaDB (23 tabel): katalog riset AI (OpenAlex), klasifikasi origin lokal/internasional, kuartil SJR, ringkasan editor manual (fitur LLM dihapus total), pencarian 4-lapis, publikasi sendiri + viewer PDF flipbook, RBAC admin/editor. 187 berkas, update terakhir 2026-08-26; status "semua selesai kecuali deploy".
- **Database TIDAK ada di GitHub**: hanya skema (`docs/pusatriset-schema.sql`). Dump data 35.621 paper (`docs/handover/pusatriset-20260824.sql.gz`) hanya di komputer pemilik (di-gitignore; berisi password_hash staf → jangan lewat chat).
- Desain publik (Tailwind): palet `#F7F9FC`, brand-900 `#0C2D4A`, brand-700 `#14508A`, brand-100 `#E3EEF7`, teal `#14B8A6`, indigo `#6366F1`; font Geist + Source Serif 4; halaman Home/Katalog/Detail/Dashboard/Metodologi.
- Keterbatasan konversi ke Elementor Free native: ilustrasi hero SVG, grafik Dashboard, Katalog dengan filter/pagination DB, viewer PDF flipbook, 35k paper → butuh widget HTML+JS (izin) atau tetap di app Next.js. **Konversi ditunda**; pemilik mengalihkan ke buatiklanai.id. Pertanyaan terbuka: sumber data (dump/CSV dari pemilik vs re-ingest OpenAlex) dan boleh/tidak HTML+JS fungsional.

### C. buatiklanai.id (alias `buatiklan`) — DIKERJAKAN & TAYANG
Referensi desain dari pemilik: gambar "FRAMEFORM" (portofolio motion designer; gaya majalah/lembar kontak, "bizarre & authentic"). DNA diadaptasi, bukan disalin.

**Tahap & berkas** (`sites/buatiklan/design/`): `DNA.md`, `OUTLINE.md`, `home.html` (mockup statis), `build_home.py` (generator Beranda → `home_sections.json`), `build_about.py` (→ `about_sections.json`), `push_draft.py <page_id> <json>` (tulis `_elementor_data` lewat Bridge dengan hash+backup, id elemen dibuat otomatis), `site_chrome.py` (menu+Astra+widget footer+CSS), `chrome.css` (SELURUH CSS Tambahan situs — sumber kebenaran), `media.json`, `posts.json`.

**Desain (kunci):** kertas `#ECE7DB`, tinta `#0B0B0B`, satu merah `#D9291C`; font Anton (judul kapital), Caveat 700 (tulisan tangan, satu frasa per section), Inter (label mikro kapital + badan). Struktur sel hairline 1 px, nomor section 01–04, foto B&W ber-selotip & miring ±2°, sticky note, stempel bulat merah (container bulat berborder dashed), tanpa gradien/bayangan. Foto = gambar milik situs sendiri (media 997, 884, 981, 949, 943) dijadikan B&W via CSS filter native image widget.

**Keadaan situs (per 2026-11-08):**
- WP 7.1.4, PHP 7.4.34 (tua), Elementor 4.3.6 **Free**, tema Astra, Bridge 1.3.0, Classic Editor aktif, kit #274 (masih bawaan). Plugin aktif: classic-editor, claude-bridge, elementor, suretriggers (OttoKit), sigmize, astra-sites, surecookie, sureform, surerank, header-footer-elementor. Tidak aktif: akismet, hello, surecart. User login: `adminbuatiklan` (administrator). Application Password JANGAN dicatat (pernah ditempel di chat → **cabut/buat ulang**).
- **Home #275**: DIGANTI total (backup `_claude_bk_*` di postmeta; draf uji #1032 sudah di-trash). Isi: wordmark BUATIKLANAI (Anton 19.5vw), hero 3 sel (headline, foto polaroid, sticky note + sub-headline + tombol), pasangan teks "AI untuk / yang bisa diuji" & "Iklan yang / bisa dipercaya.", Tentang+Topik (9 kategori tertaut), Artikel Terbaru (3 kartu dari artikel nyata: 980, 947, 939; kartu native, MANUAL — tidak otomatis), 4 prinsip, blok identitas inisiator (addendum). **Bagian "Kirim ide/Kirim artikel" DIHAPUS atas permintaan pemilik**; tidak ada halaman `/kirim-artikel/`.
- **About #219** (slug `about`, judul "Tentang Publikasi Ini"): teks addendum persis + daftar Landasan materi + 4 prinsip + tombol "Pelajari Lebih Lanjut di asosiasi.ai". Meta layout = full-width, header transparan dimatikan.
- **Blog #344** = halaman Posts (Astra), diredesain via CSS+Astra: banner "ARTIKEL" raksasa + intro brief, kartu hairline, gambar B&W, sidebar kanan (Cari + Kategori; widget Tag dihapus karena kosong), paginasi bernomor, tombol "Baca →". Arsip kategori memakai gaya sama; intro khusus Panduan/Studi Kasus/Tren/Etika dari brief; state kosong "Belum ada artikel di bagian ini. Segera hadir." Halaman satu artikel: judul Anton besar, foto B&W, teks Inter 17px.
- **Menu utama (menu 6)**: Artikel(347→page 344) · Panduan(351→cat 20) · Studi Kasus(350→cat 21) · Tren & Riset(348→cat 19) · Tentang(349→page 219). Item "Kontak"(414) dihapus dari menu (halaman tetap ada). `mobile_menu` diarahkan ke menu 6.
- **Header Astra** (global): baris atas hitam "Dikelola oleh Asosiasi AI Indonesia" (tertaut) + "Referensi, bukan jasa"; baris utama logo-teks (judul situs "Buat Iklan AI Indonesia", Anton) + menu bersel hairline + tombol "Baca artikel". Footer: 4 kolom (merek+tagline+identitas Dian Martin, Jelajahi, Topik, Supported by Asosiasi AI Indonesia — asosiasi.ai + CTA "Pelajari Lebih Lanjut di asosiasi.ai"), copyright berisi identitas addendum. Widget footer = blok HTML `block-7..12`; widget `nav_menu-1/2` (starter) dihapus; sidebar: `block-2` (Cari), `block-6` (Kategori); `block-3/4/5` dihapus.
- **Astra settings yang diubah**: `global-color-palette` (paper/ink/merah), `body-font-family` Inter, `headings-font-family` Anton + uppercase, `header-desktop-items`/`header-mobile-items`, `header-html-1/2`, `header-button1-*`, `footer-copyright-editor`, `ast-dynamic-archive-post-custom-title`="Artikel", banner title color/align, `archive-post-sidebar-layout`=right-sidebar, `blog-grid`=2, `blog-meta`=[category,date]. Backup 1 versi otomatis oleh Bridge (`claude_bridge_backup_astra-settings`).
- **Kategori dibuat** (ID): 11 riset pasar · 12 ide & pembuatan konten · 13 iklan digital · 14 SEO & GEO · 15 media sosial · 16 visual/foto/video · 17 analisis performa · 18 etika & kepatuhan · 19 tren & laporan industri · 20 Panduan · 21 Studi Kasus.
- **20 artikel (17 publish + 3 draf) dikategorikan** (isi/judul/tanggal/status tidak diubah): semua "Cara …" → Panduan(20) + satu topik (SEO→14, iklan TikTok/Instagram→15, positioning/USP/persona/journey→11, selain itu→13; draf "Cara Membuat" kosong→12); "AI Kill Switch"→18. "Uncategorized" tidak dipakai lagi.
- **Pengaturan situs**: bahasa WP diubah ke `id_ID`, format tanggal `j F Y`.
- Artikel lama yang menyebut nama tools (Quattr, HubSpot, Fliki, GravityWrite, Branding5, Replug, Simplified Riley, Besthunt) bertentangan dengan aturan netral brief → **dibiarkan** (keputusan pemilik belum final: opsi "jadikan draf" ditawarkan).
- Halaman starter lama masih ada & belum disentuh: Offering, Donate, Shop(+SureCart), Checkout, Dashboard, Contact (berisi alamat San Diego palsu dari template), Sample Page.

**Belum / TODO buatiklan:** logo BuatIklanAI & logo Asosiasi AI (pemilik bilang ada, TIDAK ketemu di Media Library/container/repo; minta lokasi); judul situs di header masih "Buat Iklan AI Indonesia" (belum diubah); standar field artikel addendum (Landasan materi, Referensi terperinci, Konteks implementasi, Catatan editorial, Tautan lanjutan ke asosiasi.ai) — rencana: template di repo + dipasang di artikel baru, artikel lama tidak diubah (menunggu OK); halaman Kontak dengan WhatsApp/email resmi asosiasi.ai (data belum ada); Studi Kasus & Tren & Riset masih kosong; rapikan/hapus halaman starter; "Artikel unggulan/populer" tidak otomatis (WP tidak menghitung baca; pakai sticky/curated).

### D. Brief & addendum baru (SEMUA MUTLAK — instruksi pemilik)
Disimpan rapi di repo: `sites/<alias>/BRIEF.md` / `ADDENDUM.md` (lihat `sites/README.md`).
- **Sudah live → ADDENDUM** (tambahan, tidak menghapus): `regulasi`, `buatiklan`. Isi: identitas "Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia / Supported by Asosiasi AI Indonesia — asosiasi.ai"; landasan materi (buku *Stay Human, Stay in Charge — Transformasi AI di Korporasi*, riset studi banding 14 yurisdiksi, implementasi industri); halaman About "Tentang Publikasi Ini"; blok identitas di Home; teks footer; standar field artikel/dokumen; CTA konsultasi → https://asosiasi.ai/; WA & email = sama dengan asosiasi.ai; tanpa penawaran layanan/produk/harga.
- **Belum live → BRIEF Revisi Lengkap** (6): `bikinkonten`(bikinkontenai.id), `toolsai`(toolsaigratis.id), `analisadata`(aianalisadata.id), `solusiindustri`(aisolusiindustri.id), `solusikeamanan`(aisolusikeamanan.id), `institut`(institutnasional.ai). Struktur: **Home, Artikel, Kategori, About, Kontak** (tanpa Layanan/Produk/Program/Kursus); "Supported by Asosiasi AI Indonesia" di setiap halaman/footer; logo Asosiasi wajib; CTA "Pelajari Lebih Lanjut di asosiasi.ai" & "Konsultasi melalui Asosiasi AI Indonesia"; disclaimer edukasi; Kontak berisi WA+email resmi asosiasi.ai + form usulan artikel; artikel wajib kategori+konteks+tag+ringkasan+referensi+CTA.
- `pusatriset`: BELUM ada brief.
- Keputusan pemilik yang berubah: awalnya "Tentang & Glosarium tidak usah" (khusus buatiklan), lalu "addendum & brief baru adalah mutlak" → About WAJIB (sudah dibuat di buatiklan). Glosarium tidak dibuat.

### E. Struktur repo (dirapikan 2026-11-08)
`regulasi/` → `sites/regulasi/`, `buatiklanai/` → `sites/buatiklan/` (+ BRIEF.md/ADDENDUM.md), `_AI Regulations.xlsx` → `sites/regulasi/`. Folder baru: `sites/{bikinkonten,toolsai,analisadata,solusiindustri,solusikeamanan,institut,pusatriset}/`. Catatan koneksi per situs tetap di `config/sites/<alias>.md` (dibaca engine). `build_library.py` path xlsx sudah diperbaiki (218 dokumen = 16 + 202, teruji).

### F. Pelajaran teknis baru (tambah ke lessons-redesign.md bila perlu)
1. **Google Fonts dari Elementor tidak ter-enqueue** di situs ini (SureCookie guard/optimasi) → judul jatuh ke serif. Solusi: `@import url(fonts.googleapis.com…)` di CSS Tambahan (+ set font di Astra). Verifikasi dengan screenshot, jangan percaya `typography_font_family` saja.
2. **`POST /claude/v1/custom-css` MENGGANTI seluruh CSS** → selalu kirim isi penuh `chrome.css`.
3. `theme-option` GET: parameter `name=astra-settings` (opsional `keys=a,b`). POST: `{name, merge:{...}, nav_menu_locations:{...}}`; backup 1 versi otomatis.
4. `elementor_page apply_draft` HANYA menyalin `_elementor_data`, **tidak** meta halaman → set meta Astra di halaman target (mis. `theme-transparent-header-meta: disabled`, `site-post-title: disabled`, layout full-width/unboxed/no-sidebar). Draf hasil `draft_copy` menyalin meta halaman asal.
5. Preview draf tanpa login: terbitkan draf dengan **password halaman** (post_password), isi lewat Playwright, lalu hapus/trash. Application Password tidak bisa dipakai untuk render frontend.
6. Screenshot Playwright: scroll bertahap dulu (gambar lazy-load), tunggu font; banner cookie SureCookie menutupi tangkapan (bukan bug).
7. Header Astra "layout-2" banner: `#masthead` position absolute → arsip/kategori perlu `.blog #masthead,.archive #masthead,.search #masthead{position:relative!important}`.
8. Elementor 4.3.6 Free mendukung native: rotasi (`_transform_rotateZ_effect`), CSS filter image (`css_filters_css_filter:custom` + `css_filters_saturate`), border/radius/dashed, ukuran font `vw`. Guardrail memperingatkan ">2 font keluarga" (diabaikan; sengaja Anton+Inter+Caveat).
9. Widget footer/sidebar diubah via `PUT /wp/v2/widgets/<id> {instance:{raw:{content:"<!-- wp:html -->…"}}}`; widget `nav_menu` lebih mudah dihapus lalu diganti blok HTML tautan. Menu item: `PUT /wp/v2/menu-items/<id>` dengan `object`, `object_id`, `type` (post_type|taxonomy).
10. Kontainer legacy: `width` px pada container bersarang butuh `width_tablet/width_mobile`; stempel bulat harus set `width_mobile` + `align_self:flex-start` (kalau tidak melebar jadi pil di HP).
11. WP REST mengembalikan 20 artikel termasuk draf bila `status=any&context=edit`.

### G. Keamanan (WAJIB tindak lanjut)
Application Password buatiklan (user `adminbuatiklan`) dan pusatriset, password admin 8 situs, kunci Pexels pernah ditempel di chat → **cabut/buat ulang**. Repo tidak berisi rahasia (`config/sites.local.json` gitignored; tidak di-commit).

### H. Commit sesi ini (branch `claude/clever-hypatia-6agnmk`)
060c733 DNA+outline+mockup buatiklan · a06e14b generator Beranda · 3df3e65 header/footer/menu · 9f4f4d2 Beranda tayang & hapus CTA Kirim · 5716efc redesain arsip/artikel · b39e402 kategori & state kosong · a205480 rapikan repo `sites/` + 8 brief · 6c166b7 fix path xlsx · 4c956a6 addendum buatiklan · (commit berikutnya: memory log ini). Belum ada PR (tidak diminta).

### I. Langkah berikutnya (urut termudah)
1. **regulasi** (addendum): butuh username + Application Password regulasiai.id + host `regulasiai.id`/`www.` di allowed hosts + Bridge 1.3.0. Terapkan: blok identitas Home, halaman About "Tentang Publikasi Ini", footer (Astra), field standar dokumen, CTA asosiasi.ai. Ingat: pustaka dokumen = widget HTML+JS (allow-js), header/footer = Astra, jangan sentuh halaman Testing #526.
2. **6 situs baru** satu per satu: kredensial → site_health → pasang Astra (`POST /claude/v1/theme-install {slug:"astra",activate:true}`) + Elementor + Classic Editor → DNA/outline/mockup → bangun draf → cek 3 layar → tayang (konfirmasi). Mulai `bikinkonten`.
3. **Data bersama** dari pemilik: logo Asosiasi AI (+ logo tiap brand), nomor WhatsApp & email resmi asosiasi.ai, teks naskah buku/riset (detail "mengikuti naskah resmi tim").
4. buatiklan: template field artikel + keputusan artikel bernama tools + halaman Kontak (menunggu WA/email) + rapikan halaman starter + judul situs.
5. pusatriset: tunggu brief; keputusan strategi (WP front vs app Next.js) & sumber data.
6. Tes: tambah tes Bridge PHP & `push-element.ts`; `npm run e2e`.
