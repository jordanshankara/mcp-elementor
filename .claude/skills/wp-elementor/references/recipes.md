# Resep

## Ganti teks / tombol
outline → (get bila perlu) → `elementor_update` batch. Untuk repeater (icon-list, tabs): get dulu, kirim array lengkap.

## Ganti gambar (mis. hero)
1. `media_upload` (source=path/URL dari user, slot=hero, alt deskriptif).
2. `elementor_update` → `{"image":{"id":ID,"url":"URL"},"image_size":"full"}`; background section/container: `{"background_background":"classic","background_image":{"id":ID,"url":"URL"},"background_size":"cover"}`.
3. Perubahan besar (hero) → `perf_check` sebelum (sebelum langkah 2) & sesudah.

## Section baru dari section halaman lain (situs sama)
`elementor_structure op=insert copy_from={page_id, element_id} parent_id=null index=N` lalu update teksnya.
Antar situs berbeda: get elemen di situs A → insert sebagai `element` di situs B (id dibuat ulang; gambar harus diupload ulang ke situs B).

## Halaman baru
1. `wp_request POST /wp/v2/pages {title, status:"draft"}` → id.
2. `elementor_outline` halaman baru (kosong) → rev.
3. `elementor_structure insert` per section (atau copy dari halaman template).
4. Beri user link preview; publish (`wp_request POST /wp/v2/pages/ID {status:"publish"}`) setelah OK.
Template halaman kanvas: `wp_request POST /wp/v2/pages/ID {template:"elementor_canvas"}` (tanpa header/footer tema) atau `elementor_header_footer`.

## Menu (Free: menu milik tema)
`wp_request GET /wp/v2/menus fields=id,name` → `GET /wp/v2/menu-items?menus=ID fields=id,title.raw,url,menu_order,parent` → `POST /wp/v2/menu-items/ID {title,url}` / `POST /wp/v2/menu-items {title,url,menus:ID}`.

## Header/footer
- Elementor **Pro**: template Theme Builder di `content_list type=elementor_library` (template_type header/footer) → edit seperti halaman.
- Elementor **Free**: header/footer milik tema. Opsi: menu (di atas), widget area (`/wp/v2/widgets`, `/wp/v2/sidebars`), atau theme mods via plugin tema. Jelaskan batas ini ke user bila diminta "edit header" di situs Free tanpa template.

## Form kontak di Free
Widget `form` = Pro. Gunakan plugin gratis (Contact Form 7 / WPForms Lite) → widget `shortcode` dengan `[contact-form-7 id="…"]`. Instal plugin = konfirmasi user + perf_check.

## Free vs Pro – alternatif
slides → image-carousel · animated-headline → heading · price-table/call-to-action → container+heading+text-editor+button · posts/loop-grid → shortcode plugin gratis / wp-widget-recent-posts · popup → tidak ada (tawarkan section/anchor) · nav-menu → menu tema.

## SEO dasar
- Judul/slug: `wp_request POST /wp/v2/pages/ID {title, slug}` (slug berubah → peringatkan link lama).
- Meta Yoast/RankMath biasanya tidak terekspos REST tanpa konfigurasi; jangan mengarang endpoint — cek dulu `wp_request GET /wp/v2/pages/ID fields=meta`.
- Satu H1 per halaman (heading `header_size: h1`), alt di semua gambar, teks link deskriptif.

## Plugin
List: `wp_request GET /wp/v2/plugins fields=plugin,name,status,version`. Aktif/nonaktif: `POST /wp/v2/plugins/<plugin> {status}` (confirm). Install dari wordpress.org: `POST /wp/v2/plugins {slug, status:"active"}` (confirm + perf_check sebelum/sesudah).

## Optimasi situs (satu langkah per kali, confirm)
`elementor_design perf_get` → kandidat aman: `option elementor_font_display=swap`, `option elementor_optimized_image_loading=1`, experiment `e_font_icon_svg=active`, `e_optimized_markup=active`, `e_element_cache=active`, `e_lazyload=active`, `option elementor_css_print_method=external`. Tiap `perf_set` otomatis visual-check + rollback. Lalu `perf_check`.
Plugin cache (LiteSpeed/WP Rocket/Autoptimize): ubah setting via REST hanya bila plugin menyediakannya; jika tidak, beri user langkah manual. JANGAN minify manual.

## Undo
`elementor_page op=backups` → `op=restore key=… rev=… confirm=true`. Juga ada revisi WordPress (wp-admin → Revisions) dan backup lokal di `backups/<alias>/<page>/`.
