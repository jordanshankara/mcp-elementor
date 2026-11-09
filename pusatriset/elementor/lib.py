"""Helper pembangun elemen Elementor (container flex/grid + widget native) untuk halaman PusatRiset.
Warna & ukuran mengikuti token Tailwind aplikasi lama (lihat plugin/build/build-css.mjs)."""
import json

# --- token desain aplikasi lama
B900, B700, B100 = '#0C2D4A', '#14508A', '#E3EEF7'
PAGE, CARD, ALT, WARM = '#F7F9FC', '#FFFFFF', '#EEF3FA', '#E2E8F0'
PRIMARY, SECOND, MUTED = '#0F172A', '#475569', '#64748B'
TEAL, TEALD, INDIGO, INDIGOD = '#14B8A6', '#0F766E', '#6366F1', '#3730A3'
FONT = 'Geist'
SHADOW = {'horizontal': 0, 'vertical': 1, 'blur': 3, 'spread': 0, 'color': 'rgba(15,23,42,0.08)'}
SHADOW_LG = {'horizontal': 0, 'vertical': 10, 'blur': 15, 'spread': -3, 'color': 'rgba(0,0,0,0.1)'}


def px(n): return {'unit': 'px', 'size': n}
def em(n): return {'unit': 'em', 'size': n}
def pct(n): return {'unit': '%', 'size': n}


def sp(t=0, r=None, b=None, l=None, unit='px'):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': t == r == b == l}


def gap(n): return {'unit': 'px', 'size': n, 'column': str(n), 'row': str(n)}


def radius(n): return {'unit': 'px', 'top': str(n), 'right': str(n), 'bottom': str(n), 'left': str(n), 'isLinked': True}


def el(elType, settings=None, elements=None, **kw):
    d = {'elType': elType, 'settings': settings or {}, 'elements': elements or []}
    d.update(kw)
    return d


def box(children, *, inner=True, direction='column', gap_=0, pad=None, pad_t=None, pad_m=None, bg=None, grad=None,
        border=None, rad=None, shadow=None, width=None, boxed=None, align=None, justify=None, wrap=None, css=None,
        min_h=None, margin=None, extra=None, overlay=None):
    """Container flexbox. boxed=px -> isi dibatasi lebar itu (content_width boxed), selain itu full."""
    s = {'flex_direction': direction, 'flex_gap': gap(gap_), 'content_width': 'boxed' if boxed else 'full',
         'padding': pad if pad is not None else sp(0)}
    if boxed: s['boxed_width'] = px(boxed)
    if pad_t is not None: s['padding_tablet'] = pad_t
    if pad_m is not None: s['padding_mobile'] = pad_m
    if bg: s.update({'background_background': 'classic', 'background_color': bg})
    if grad:  # (warna1, warna2, sudut)
        s.update({'background_background': 'gradient', 'background_gradient_type': 'linear', 'background_color': grad[0],
                  'background_color_b': grad[1], 'background_gradient_angle': {'unit': 'deg', 'size': grad[2]},
                  'background_color_stop': pct(0), 'background_color_b_stop': pct(100)})
    if border:  # (lebar, warna, sisi) sisi: None=semua, 'b'=bawah, 't'=atas, 'tb'
        w, col, side = border
        t = w if side in (None, 't', 'tb') else 0
        r_ = w if side is None else 0
        b = w if side in (None, 'b', 'tb') else 0
        l = w if side is None else 0
        s.update({'border_border': 'solid', 'border_width': sp(t, r_, b, l), 'border_color': col})
    if rad is not None: s['border_radius'] = radius(rad)
    if shadow: s.update({'box_shadow_box_shadow_type': 'yes', 'box_shadow_box_shadow': shadow})
    if width is not None: s['width'] = width
    if align: s['flex_align_items'] = align
    if justify: s['flex_justify_content'] = justify
    if wrap: s['flex_wrap'] = wrap
    if css: s['css_classes'] = css
    if min_h: s['min_height'] = px(min_h)
    if margin: s['margin'] = margin
    if extra: s.update(extra)
    return el('container', s, children, isInner=inner)


def grid(children, cols=(1, 1, 1), gap_=16, inner=True, **kw):
    """Container grid: cols=(desktop, tablet, mobile)."""
    n = len(children)
    rows = tuple(-(-n // c) for c in cols)  # jumlah baris eksplisit (Elementor default 2 baris -> ruang kosong)
    extra = {'container_type': 'grid', 'grid_columns_grid': {'unit': 'fr', 'size': cols[0]},
             'grid_rows_grid': {'unit': 'fr', 'size': rows[0]}, 'grid_rows_grid_tablet': {'unit': 'fr', 'size': rows[1]},
             'grid_rows_grid_mobile': {'unit': 'fr', 'size': rows[2]},
             'grid_columns_grid_tablet': {'unit': 'fr', 'size': cols[1]}, 'grid_columns_grid_mobile': {'unit': 'fr', 'size': cols[2]},
             'grid_gaps': gap(gap_), 'grid_auto_flow': 'row'}
    extra.update(kw.pop('extra', {}) or {})
    return box(children, inner=inner, extra=extra, **kw)


def grid_tpl(children, tpl, tpl_t='1fr', tpl_m='1fr', gap_=40, inner=True, **kw):
    """Grid dengan kolom kustom (mis. 1.1fr 0.9fr) lewat CSS: Elementor memakai pengulangan 'fr' sederhana, jadi pakai flex bila rasio tak sama."""
    return grid(children, **kw)


def heading(text, size, weight='700', color=PRIMARY, tag='h2', align=None, size_t=None, size_m=None, lh=None, link=None,
            margin=None, transform=None, spacing=None, align_t=None, align_m=None, font=FONT, css=None):
    s = {'title': text, 'header_size': tag, 'title_color': color, 'typography_typography': 'custom',
         'typography_font_family': font, 'typography_font_size': px(size), 'typography_font_weight': weight}
    if size_t: s['typography_font_size_tablet'] = px(size_t)
    if size_m: s['typography_font_size_mobile'] = px(size_m)
    if lh: s['typography_line_height'] = em(lh)
    if transform: s['typography_text_transform'] = transform
    if spacing is not None: s['typography_letter_spacing'] = {'unit': 'px', 'size': spacing}
    if align: s['align'] = align
    if align_t: s['align_tablet'] = align_t
    if align_m: s['align_mobile'] = align_m
    if link: s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    if margin: s['_margin'] = margin
    if css: s['_css_classes'] = css
    return el('widget', s, widgetType='heading')


def text(html, size, color=SECOND, lh=1.5, weight='400', align=None, size_t=None, size_m=None, margin=None, align_t=None,
         align_m=None, max_w=None, font=FONT):
    s = {'editor': html, 'text_color': color, 'typography_typography': 'custom', 'typography_font_family': font,
         'typography_font_size': px(size), 'typography_font_weight': weight, 'typography_line_height': em(lh)}
    if size_t: s['typography_font_size_tablet'] = px(size_t)
    if size_m: s['typography_font_size_mobile'] = px(size_m)
    if align: s['align'] = align
    if align_t: s['align_tablet'] = align_t
    if align_m: s['align_mobile'] = align_m
    if margin: s['_margin'] = margin
    if max_w: s.update({'_element_width': 'initial', '_element_custom_width': px(max_w)})
    return el('widget', s, widgetType='text-editor')


def icon(cls, size, color, lib='fa-solid', align='center', margin=None):
    s = {'selected_icon': {'value': cls, 'library': lib}, 'primary_color': color, 'size': px(size), 'align': align,
         'view': 'default'}
    if margin: s['_margin'] = margin
    return el('widget', s, widgetType='icon')


def shortcode(code):
    return el('widget', {'shortcode': code}, widgetType='shortcode')


def button(label, url, bg, color, size=14, weight='500', pad=None, rad=6, align=None, ext=False):
    s = {'text': label, 'link': {'url': url, 'is_external': 'on' if ext else '', 'nofollow': '', 'custom_attributes': 'rel|noopener' if ext else ''},
         'background_color': bg, 'button_text_color': color, 'typography_typography': 'custom', 'typography_font_family': FONT,
         'typography_font_size': px(size), 'typography_font_weight': weight, 'border_border': 'solid', 'border_width': sp(0),
         'border_color': 'rgba(0,0,0,0)', 'border_radius': radius(rad), 'text_padding': pad or sp(12, 24),
         'hover_color': color}
    if align: s['align'] = align
    return el('widget', s, widgetType='button')


def image(img_id, url, width=None, link=None, ext=False, align=None, alt=''):
    s = {'image': {'id': img_id, 'url': url, 'alt': alt}, 'image_size': 'full'}
    if width: s['width'] = px(width)
    if align: s['align'] = align
    if link: s.update({'link_to': 'custom', 'link': {'url': link, 'is_external': 'on' if ext else '', 'nofollow': '', 'custom_attributes': 'rel|noopener' if ext else ''}})
    return el('widget', s, widgetType='image')


def circle_icon(cls, size_box, size_icon, bg, color):
    """Lingkaran berisi ikon (seperti 'flex h-9 w-9 items-center justify-center rounded-full')."""
    return box([icon(cls, size_icon, color)], inner=True, width=px(size_box), min_h=size_box, bg=bg, rad=999,
               align='center', justify='center',
               extra={'_flex_size': 'none', 'width_tablet': px(size_box), 'width_mobile': px(size_box)})


def dump(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)
