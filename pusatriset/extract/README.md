# Ekstraksi PusatRiset.ai lama (Next.js + MySQL) → bahan konversi ke WordPress/Elementor

Sumber: `F:\0. Code\pusatriset` (aplikasi Next.js 16 + Prisma + MySQL/MariaDB). Dump yang dipakai: `docs/handover/pusatriset-20260824.sql.gz`.

## 1. Data (sudah diekstrak, terverifikasi)
`extract/data/*.jsonl` (satu baris = satu record, semua kolom, tipe asli; **tidak masuk git**, ±175 MB). Dibuat oleh `export_dump.py` (streaming, tanpa MySQL).

| Tabel | Baris | Catatan |
|---|---:|---|
| papers | 35.621 | inti katalog (judul, abstrak, tanggal, origin, tier, kuartil SJR, lisensi, kebijakan abstrak) |
| authors / paper_authors | 89.976 / 136.967 | |
| author_affiliations / institutions | 156.526 / 7.260 | afiliasi per paper |
| paper_identifiers | 70.631 | DOI, arXiv, OpenAlex |
| paper_titles / paper_topics | 35.618 / 35.616 | judul dwibahasa; domain→field→subfield→topic |
| citation_stats | 35.609 | sitasi total, per tahun (JSON), FWCI, persentil, retraksi |
| paper_affiliation_countries | 47.877 | |
| summaries / paper_relations / relevance_scores | 74 / 30 / 1 | konten kurasi |
| policy_tags / search_synonyms / search_terms / approved_venues / venue_arxiv_categories | 6 / 47 / 8.613 / 9 / 2 | |
| paper_files / paper_versions / paper_merges / paper_policy_tags / institution_name_variants | 0 | kosong |

**Verifikasi:** semua angka identik dengan `verifikasi-A2-sebelum-20260824.txt` (papers 35.621, summaries 74, paper_authors 136.967, relations 30, origin local 22.319 / international 13.302, indexed 35.621, policy full 35.599 / summary_only 22).

**Sengaja TIDAK diekspor (data pribadi/internal):** `users` (5 akun, ada `password_hash`), `audit_logs`, `app_settings`, `submissions`, `disputes` (berisi email pengirim).
Catatan data: 34.512 paper punya abstrak; kuartil SJR: Q1 7.669, Q2 1.024, Q3 234, Q4 44, tak terindeks 26.650; tahun terbit sampai 2026. `paper_files` kosong → belum ada publikasi sendiri.

## 2. Desain (sumber disalin apa adanya)
`extract/design-src/` = salinan verbatim halaman publik + komponen + `globals.css` (44 berkas): Home, Archive/Katalog, Dashboard, Metodologi, detail Riset, Header, Footer, kartu, filter, badge, grafik, viewer jurnal. Admin (`/admin/*`) tidak ikut (netral, akan diganti layar admin WordPress).

Token desain (dari `globals.css`): latar `#F7F9FC`, kartu `#FFFFFF`, kartu-alt `#EEF3FA`, garis `#E2E8F0`; biru `#0C2D4A` (900) / `#14508A` (700) / `#E3EEF7` (100); teal `#14B8A6`/`#0F766E`; indigo `#6366F1`/`#3730A3`; teks `#0F172A` / `#475569` / `#64748B`; badge relevansi hijau `#2F7A4F`, kuning `#B98A1E`, jingga `#C9701F`, merah `#B8352E`. Font: Geist (sans), Geist Mono, Source Serif 4. Komponen khas: kartu KPI gradien (teal/biru/indigo), `glass-card` (blur 14px), kartu paper dengan garis gradien saat hover, header sticky blur, footer 3 kolom, grafik area/batang/donat.

## 3. Rekomendasi penyimpanan 35 ribuan aset (bukan per post)
**Tabel khusus di database WordPress yang sama + plugin "PusatRiset Data" (REST + shortcode).**
- Tabel `wp_pr_*` meniru skema lama (papers, authors, paper_authors, institutions, affiliations, identifiers, topics, citation_stats, summaries, relations, policy_tags, synonyms, search_terms). **UUID lama dipertahankan** → tautan lama `/riset/<uuid>` tetap hidup.
- Pencarian: index FULLTEXT (judul+abstrak+penulis) + sinonim + saran "mungkin maksud Anda" (port `search.ts`), filter sama persis dengan Archive lama (asal, tahun, subbidang, badge, kuartil, akses terbuka).
- Tampilan: shortcode `[pr_catalog]`, `[pr_paper]`, `[pr_dashboard]`, `[pr_recent]`, dirender di server (cepat, ramah SEO, bisa diakses tanpa JS, formulir GET seperti aslinya). Grafik = SVG sisi server.
- Menambah data kemudian: layar admin WordPress (tambah/edit paper, ringkasan), impor CSV/JSON/OpenAlex yang **upsert** berdasar DOI/OpenAlex ID (tanpa duplikat), versi skema bermigrasi rapi.
- Impor awal: skrip membaca JSONL dan mengirim per 500 baris ke endpoint REST plugin (dapat dilanjutkan, idempoten) — tidak terkendala batas unggah phpMyAdmin.

Ditolak: (a) 35 ribu post/CPT + postmeta → 300 ribu+ baris meta, admin lambat, filter lemah; (b) JSON statis → >70 MB, filter/pencarian tidak mungkin; (c) API eksternal → bukan WordPress native.

## 4. Peta halaman lama → WordPress
| Lama | Baru |
|---|---|
| `/` (hero, KPI, fitur, terbaru, terpopuler, CTA) | Halaman Elementor native (hero/KPI/fitur/CTA) + shortcode untuk statistik & daftar terbaru |
| `/katalog` | Halaman Elementor: header judul + `[pr_catalog]` |
| `/dashboard` | Halaman Elementor: header + KPI + `[pr_dashboard]` (grafik) |
| `/metodologi` | Halaman Elementor native penuh (statik) |
| `/riset/[id]` | Rewrite `/riset/<uuid>` → template `[pr_paper]` (tab Data Asli / Ringkasan, riset serupa, BibTeX) |
| Header/Footer | Header/footer Astra (via Bridge) |
| `/admin/*` | Layar admin WordPress (plugin) |

## 5. Verifikasi desain: baseline
Database MariaDB lokal (`D:\xampp`, terpisah: `pusatriset_baseline`) dipulihkan dari dump yang sama; aplikasi lama dijalankan lokal untuk menangkap screenshot semua halaman sebagai pembanding "tidak boleh berubah". Lihat `extract/baseline/`.
