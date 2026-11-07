# Menambah situs (ke-8, 9, …)

Yang dilakukan USER (menyangkut kredensial, ±3 menit):
1. wp-admin → Users → Add New: buat user `claude-bot` (role **Editor** untuk konten saja; **Administrator** bila perlu urus plugin/settings/performa). Atau pakai user sendiri.
2. Login sebagai user itu → Users → Profile → **Application Passwords** → nama "claude-code" → Add → salin password (format `xxxx xxxx xxxx xxxx xxxx xxxx`).
3. Plugins → Add New → Upload Plugin → `wp-elementor-mcp/dist/claude-bridge.zip` (versi ≥1.3.0) → Install → Activate. (Jika sudah terpasang versi lama: pilih "Replace current with uploaded".) Setelah situs terhubung, jalankan `site_health` dan pastikan `bridge 1.3.0`, lalu baca `references/lessons-redesign.md` sebelum membangun/redesign.
4. Kirim ke Claude: url, username, app password (atau tempel sendiri ke config).

Yang dilakukan CLAUDE:
1. Tambah blok di `config/sites.local.json` (alias pendek huruf kecil, unik):
   `"alias": { "url": "https://domain.com", "user": "claude-bot", "app_password": "xxxx …", "label": "Nama Situs", "env": "prod", "readonly": true, "tags": ["klien-x"] }`
   (Jangan pernah menampilkan app password di chat setelah disimpan.)
2. `site_health alias` → laporkan versi, Free/Pro, bridge, auth.
3. Buat `config/sites/<alias>.md` (5–15 baris: id beranda/kontak dari content_list, warna/font kit dari `elementor_design kit_get keys=[system_colors,system_typography]`).
4. Uji baca: outline beranda. Situs tetap `readonly: true` sampai user mengizinkan tulis → ubah `"readonly": false`.

# Troubleshooting koneksi
| Gejala | Penyebab & solusi |
|---|---|
| 401 incorrect_password | App password salah/terhapus → buat ulang. |
| 401 padahal benar | Hosting (Apache CGI/FastCGI) membuang header. Tambah di `.htaccess` atas: `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1` |
| 401 "Application passwords not available" | Situs tanpa HTTPS atau dimatikan plugin keamanan → aktifkan HTTPS / izinkan Application Passwords. |
| 403 | Role kurang (Editor tidak bisa plugin/settings/kit) atau security plugin. |
| rest_no_route claude/v1 | Bridge belum aktif. |
| Bukan JSON / HTML challenge | Cloudflare/Wordfence/ModSecurity memblokir. Whitelist IP laptop atau rule untuk `/wp-json/` & `?rest_route=`. |
| Teks baru tidak tampil untuk pengunjung | Cache CDN. Bridge sudah purge plugin cache populer; Cloudflare tanpa plugin → user purge manual. |
| Timeout | Hosting lambat; ulangi. Request otomatis di-retry & diantrikan per situs. |

# Update bridge di semua situs
`site_health` menunjukkan versi bridge. Versi baru: `cd wp-elementor-mcp && npm run build-zip` → user upload ulang (Plugins → Add New → Upload → Replace).


## Situs WordPress baru (tanpa Elementor/Astra)
1. Daftarkan di `config/sites.local.json` (alias, url, user, app_password, `readonly:true`), uji `GET /wp/v2/users/me`.
2. Setelah pengguna setuju: `readonly:false`; pasang plugin via `POST /wp/v2/plugins {slug, status:"active"}` (confirm): `elementor`, `classic-editor`.
3. Tema Astra TIDAK bisa lewat REST inti → pengguna unggah Bridge ≥1.3.0, lalu `POST /claude/v1/theme-install {slug:"astra", activate:true}`.
4. Cek `site_health` + 3 standar (Elementor, classic editor, Astra), lalu ikuti `references/lessons-redesign.md`.
