# Situs: brief & sumber desain

Satu folder per situs (nama folder = alias di `config/sites.local.json`). Catatan koneksi/teknis per situs tetap di `config/sites/<alias>.md` (dibaca engine MCP). Rahasia (`config/sites.local.json`) tidak ada di repo.

- `BRIEF.md` = brief lengkap. `ADDENDUM.md` = tambahan untuk situs yang SUDAH live (tidak menggantikan brief lama; hanya menambah).
- `design/` = DNA, outline, mockup, generator (bila sudah dikerjakan).

| alias | domain | status | berkas | pekerjaan |
|---|---|---|---|---|
| `regulasi` | regulasiai.id | live | BRIEF + ADDENDUM + design/ | redesain selesai; addendum belum diterapkan |
| `buatiklan` | buatiklanai.id | live | BRIEF + ADDENDUM + design/ | Beranda, header/footer, arsip artikel sudah tayang; addendum belum diterapkan |
| `pusatriset` | pusatriset.ai | belum live | (brief belum ada) | Astra belum dipasang |
| `bikinkonten` | bikinkontenai.id | belum live | BRIEF | belum dikerjakan |
| `toolsai` | toolsaigratis.id | belum live | BRIEF | belum dikerjakan |
| `analisadata` | aianalisadata.id | belum live | BRIEF | belum dikerjakan |
| `solusiindustri` | aisolusiindustri.id | belum live | BRIEF | belum dikerjakan |
| `solusikeamanan` | aisolusikeamanan.id | belum live | BRIEF | belum dikerjakan |
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
