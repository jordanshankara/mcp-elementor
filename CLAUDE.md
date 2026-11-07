# Project: pengelola website WordPress + Elementor

- Semua pekerjaan website (edit Elementor, admin WordPress, gambar, performa) WAJIB lewat skill `wp-elementor` dan MCP server `wp-elementor` — bukan Claude in Chrome / browser.
- Situs terdaftar di `config/sites.local.json` (rahasia, jangan ditampilkan/di-commit). Pilih situs lewat alias persis; kalau user tidak menyebut situs, TANYAKAN.
- Konfirmasi user sebelum operasi destruktif / tingkat situs / massal. Redesign → draft_copy dulu.
- Hemat token: outline → get seperlunya → update batch. Verifikasi sudah otomatis.
- Standar wajib tiap situs: (1) Elementor builder, (2) classic page / Gutenberg nonaktif, (3) tema Astra.
- Native-first: tampilan dari widget Elementor Free; HTML widget hanya fitur fungsional dengan izin pengguna. Semua gambar/logo WebP terkompres (dilarang PNG/JPG).
- Logo brand situs + logo Asosiasi AI wajib tampil; setiap teks "Asosiasi AI Indonesia" ditautkan ke https://asosiasi.ai. Header/footer = tema Astra (via bridge), bukan Elementor.
- Setiap halaman wajib dicek di desktop, tablet, dan HP sebelum dilaporkan selesai. Detail & jebakan: `.claude/skills/wp-elementor/references/lessons-redesign.md`.
- Engine & tes: `wp-elementor-mcp/` (`npm test`, `npm run playground` + `npm run e2e`).
