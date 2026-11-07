# Struktur `_elementor_data`

Array elemen berbentuk pohon. Setiap elemen: `{ id, elType, widgetType?, isInner?, settings, elements[] }`.
Engine membuat `id` otomatis (7 hex) untuk elemen baru — jangan mengarang id.

## V3 klasik
`section` → `column` → `widget` (section dalam column = `isInner: true`).

## Container (flexbox, default situs baru, ada di Free)
`container` → (`container` | `widget`). Setting umum container: `content_width` (boxed|full), `flex_direction` (row|column), `flex_gap`, `padding`, `background_background`, `background_color`, `min_height`.

## V4 atomic (Editor V4)
elType `e-flexbox` / `e-div-block`, widget `e-heading`, `e-paragraph`, `e-button`, `e-image`.
Nilai berbentuk `{ "$$type": "string", "value": "..." }`. Saat update, kirim objek `$$type` UTUH (lihat dulu dengan elementor_get, tiru bentuknya). Style ada di key `styles` (bukan settings) — ubah hanya bila perlu.

## Key widget umum (V3/container)
| Widget | Key utama |
|---|---|
| heading | `title`, `header_size` (h1..h6), `align`, `title_color`, `typography_*` |
| text-editor | `editor` (HTML: `<p>…</p>`), `text_color`, `align` |
| button | `text`, `link` `{url, is_external:"on", nofollow}`, `background_color`, `button_text_color`, `size` |
| image | `image` `{id,url}`, `image_size`, `caption`, `link_to`, `link` |
| icon-list | `icon_list` (array `{_id,text,selected_icon,link}`) — kirim array LENGKAP (array diganti, bukan digabung) |
| icon-box / image-box | `title_text`, `description_text`, `selected_icon` / `image` |
| testimonial | `testimonial_content`, `testimonial_name`, `testimonial_job`, `testimonial_image` |
| spacer / divider | `space` `{unit,size}` / `weight`, `color` |
| shortcode | `shortcode` (mis. form dari plugin gratis) |
| html | `html` (TANPA `<script>` — diblokir guardrail) |
| video | `youtube_url`, `lightbox`, `image_overlay` (wajib untuk performa) |
| icon | `selected_icon` `{value:"fas fa-star", library:"fa-solid"}` |

Ukuran responsif: suffix `_tablet` / `_mobile` (mis. `align_mobile`, `typography_font_size_mobile`).
Satuan: `{ "unit": "px", "size": 24 }`. Warna global: `__globals__: { "title_color": "globals/colors?id=primary" }` — lebih baik daripada warna hex agar konsisten dengan kit.

## Contoh insert (container + heading + button)
```json
{"elType":"container","settings":{"content_width":"boxed","flex_direction":"column","flex_gap":{"unit":"px","size":16,"column":"16","row":"16"}},
 "elements":[
  {"elType":"widget","widgetType":"heading","settings":{"title":"Judul","header_size":"h2"}},
  {"elType":"widget","widgetType":"button","settings":{"text":"Hubungi","link":{"url":"https://wa.me/62..."}}}
 ]}
```
Situs lama tanpa container: bungkus dengan `section` → `column` (`_column_size: 100`).
