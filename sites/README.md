# Situs: brief & sumber desain

Satu folder per situs (nama folder = alias di `config/sites.local.json`). Catatan koneksi/teknis per situs tetap di `config/sites/<alias>.md` (dibaca engine MCP). Rahasia (`config/sites.local.json`) tidak ada di repo.

- `BRIEF.md` = brief lengkap. `ADDENDUM.md` = tambahan untuk situs yang SUDAH live (tidak menggantikan brief lama; hanya menambah).
- `design/` = DNA, outline, mockup, generator (bila sudah dikerjakan).

| alias | domain | status | berkas | pekerjaan |
|---|---|---|---|---|
| `regulasi` | regulasiai.id | live | BRIEF + ADDENDUM + design/ | redesain selesai; addendum belum diterapkan |
| `buatiklan` | buatiklanai.id | live | BRIEF + ADDENDUM + design/ | Beranda, header/footer, arsip artikel sudah tayang; addendum belum diterapkan |
| `pusatriset` | pusatriset.ai | belum live | (brief belum ada) | Astra belum dipasang |
| `bikinkonten` | bikinkontenai.id | situs baru | BRIEF + design/ | **dibangun & tayang 2026-11-09** (gaya brutalis oranye/hitam/putih); sisa TODO di `docs/memory/LOG.md` |
| `toolsai` | toolsaigratis.id | belum live | BRIEF | belum dikerjakan |
| `analisadata` | aianalisadata.id | belum live | BRIEF | belum dikerjakan |
| `solusiindustri` | aisolusiindustri.id | situs baru | BRIEF + design/ | **dibangun & tayang 2026-11-09** (putih/navy/oranye, ref. Machvex); foto belum |
| `solusikeamanan` | aisolusikeamanan.id | situs baru | BRIEF + design/ | **dibangun & tayang 2026-11-09** (gelap, Crimson/Sand/Pearl/Obsidian, ref. AgentAI) |
| `institut` | institutnasional.ai | belum live | BRIEF | belum dikerjakan |

## Ketentuan yang sama di semua brief "Revisi Lengkap" (6 situs belum live)
- Struktur halaman: **Home, Artikel, Kategori, About, Kontak** (tidak ada Layanan/Produk/Program/Kursus).
- Identitas: *Inisiasi dari Dian Martin, Ketua Umum Asosiasi AI Indonesia. Supported by Asosiasi AI Indonesia — asosiasi.ai.* Setiap halaman memuat "Supported by Asosiasi AI Indonesia" (footer); nama asosiasi tertaut https://asosiasi.ai.
- Landasan materi: buku *Stay Human, Stay in Charge — Transformasi AI di Korporasi*, riset studi banding 14 yurisdiksi, implementasi industri.
- Semua CTA konsultasi/belajar lanjut/kolaborasi → https://asosiasi.ai. Nomor WhatsApp & email = yang resmi di asosiasi.ai (belum ada di repo; minta ke pemilik).
- Wajib: logo Asosiasi AI, CTA "Pelajari Lebih Lanjut di asosiasi.ai", disclaimer edukasi (bukan penyedia layanan), halaman About memuat identitas inisiator + landasan.
- Artikel wajib punya: kategori, konteks, tag, ringkasan, referensi, CTA. Netral (tidak endorse tools), tanpa janji hasil, klaim bersumber.
- Aturan teknis tetap dari `CLAUDE.md` (Elementor Free native, WebP, Astra, cek 3 ukuran layar).

## Addendum situs live (regulasi, buatiklan) — isi sama
Tambah: identitas + landasan materi; halaman About "Tentang Publikasi Ini"; blok singkat identitas di Home (+ tautan ke About dan asosiasi.ai); teks identitas di footer; field standar artikel/dokumen (Landasan materi, Referensi terperinci, Konteks implementasi, Catatan editorial, Tautan lanjutan ke asosiasi.ai); CTA konsultasi → asosiasi.ai. Tidak ada yang dihapus.

## Data resmi bersama (dari pemilik, 2026-11-09)
- **WhatsApp:** +62 8111913553 (tautan `https://wa.me/628111913553`) · **Email:** sekretariat@asosiasi.ai · **Web:** https://asosiasi.ai/
- **Logo (ada di branch `main`, folder repo):** `logo-asosiasi-ai/` (Logo-AAII-21 lambang+teks, `-Rec-24` horizontal berwarna, `-white-25`, `-Rec-white-26` putih) dan `Logo_Domain_AI/<domain>/` (per situs: `*_logo`, `*_lockup`, `*_lockup_white`, `*_sosmed_*`, `*_youtube_banner`; PNG + SVG). Pakai varian horizontal (Rec) untuk header/footer; ubah ke WebP sebelum diunggah (aturan proyek).
- Situs yang sudah memasang: bikinkonten (header lockup, footer logo putih, About/Home/Kontak), buatiklan (header lockup, footer logo, Kontak #355).

## Alat bersama
`sites/_lib/ek.py` + `ek2.py` (helper elemen Elementor Free: container/kartu/pil/gradien/grid), `sites/_lib/setup_site.py` (halaman, kategori, menu, Astra, widget footer/sidebar, CSS, push Elementor dari `site.json`). Pola per situs: `build_pages.py` → `*_sections.json`, `chrome.css`, `site.json`, `logos.json`.
