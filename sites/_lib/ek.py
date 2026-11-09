"""Pustaka pembantu elemen Elementor Free (container + widget native). Atur palet SEBELUM `from ek import *`: ek.PAPER/INK/RED/MUTE/TAPE/MONO."""
import json, pathlib
HFAM, HUP = 'Anton', True
BFONT = 'Inter'
HW = '800'
PAPER, INK, RED, MUTE, TAPE, MONO = '#ECE7DB', '#0B0B0B', '#D9291C', '#4A463E', '#D8CFB3', 'Inter'
ASOSIASI = 'https://asosiasi.ai'
SITE = 'https://www.buatiklanai.id'
def px(n): return {'unit': 'px', 'size': n}
def dim(t, r=None, b=None, l=None):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': t == r == b == l}
def gap(n): return {'unit': 'px', 'size': n, 'column': str(n), 'row': str(n), 'isLinked': True}
def bw(t=0, r=0, b=0, l=0): return dim(t, r, b, l)
def R(base, key, d=None, t=None, m=None):
    if d is not None: base[key] = d
    if t is not None: base[key + '_tablet'] = t
    if m is not None: base[key + '_mobile'] = m
def C(children, **s):
    st = {'content_width': 'full', 'flex_direction': 'column', 'padding': dim(0), 'flex_gap': gap(0)}
    st.update(s); return {'elType': 'container', 'settings': st, 'elements': children}
def ROW(children, tablet_col=True, **s):
    st = {'flex_direction': 'row', 'flex_direction_tablet': 'column' if tablet_col else 'row', 'flex_direction_mobile': 'column',
          'border_border': 'solid', 'border_width': bw(0, 0, 1, 0), 'border_color': INK, 'flex_align_items': 'stretch'}
    st.update(s); return C(children, **st)
def CELL(children, w=None, pad=(28,), right=True, **s):
    st = {'padding': dim(*pad), 'padding_tablet': dim(24, 24), 'padding_mobile': dim(20, 20),
          'border_border': 'solid', 'border_width': bw(0, 1 if right else 0, 0, 0), 'border_color': INK, 'flex_gap': gap(14),
          'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100},
          'border_width_tablet': bw(0, 0, 1, 0), 'border_width_mobile': bw(0, 0, 1, 0)}
    if w: st['width'] = {'unit': '%', 'size': w}
    st.update(s); return C(children, **st)
def W(wt, **s): return {'elType': 'widget', 'widgetType': wt, 'settings': s}
def typo(fam, size, tablet=None, mobile=None, weight='400', lh=None, ls=None, up=False, unit='px'):
    d = {'typography_typography': 'custom', 'typography_font_family': fam, 'typography_font_weight': weight,
         'typography_font_size': {'unit': unit, 'size': size}}
    if tablet is not None: d['typography_font_size_tablet'] = {'unit': unit, 'size': tablet}
    if mobile is not None: d['typography_font_size_mobile'] = {'unit': unit, 'size': mobile}
    if lh: d['typography_line_height'] = {'unit': 'em', 'size': lh}
    if ls is not None: d['typography_letter_spacing'] = {'unit': 'px', 'size': ls}
    if up: d['typography_text_transform'] = 'uppercase'
    return d
def H(text, size, tablet=None, mobile=None, color=INK, tag='h2', fam=None, lh=.95, up=None, align='left', unit='px', **s):
    fam = fam or HFAM; up = HUP if up is None else up
    d = {'title': text, 'header_size': tag, 'title_color': color, 'align': align}
    d.update(typo(fam, size, tablet, mobile, weight='400' if fam in ('Anton', 'Caveat') else HW, lh=lh, ls=-0.5 if fam == HFAM else 0, up=(up and fam == HFAM), unit=unit)); d.update(s)
    return W('heading', **d)
def SCRIPT(text, size, tablet, mobile, color=INK, rot=-3, tag='h3'):
    return H(text, size, tablet, mobile, color=color, tag=tag, fam='Caveat', lh=1, up=False, _transform_rotate_popover='transform',
             _transform_rotateZ_effect={'unit': 'px', 'size': rot, 'sizes': []})
def MICRO(text, color=INK, align='left', link=None):
    html = f'<a href="{link}" style="color:{RED}">{text}</a>' if link else text
    return W('text-editor', editor=f'<p style="margin:0">{html}</p>', text_color=color, align=align,
             **typo(MONO, 11, weight='500', lh=1.8, ls=2, up=True))
def TXT(html, size=15, color=INK, **s):
    d = {'editor': html, 'text_color': color}; d.update(typo('Inter', size, mobile=15, weight='400', lh=1.6)); d.update(s); return W('text-editor', **d)
def BTN(text, url, dark=True, **s):
    d = {'text': text, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'align': 'left',
         'button_text_color': PAPER if dark else INK, 'background_color': INK if dark else 'transparent',
         'border_border': 'solid', 'border_width': dim(1), 'border_color': INK, 'border_radius': dim(0),
         'text_padding': dim(14, 22), 'hover_color': PAPER, 'button_background_hover_color': RED, 'button_hover_border_color': RED}
    d.update(typo(MONO, 11, weight='500', ls=2, up=True)); d.update(s); return W('button', **d)
def IMG(mid, url, grey=True, rot=0, w=None, **s):
    d = {'image': {'id': mid, 'url': url}, 'image_size': 'large', 'align': 'center', 'width': {'unit': '%', 'size': w or 100}}
    if grey: d.update({'css_filters_css_filter': 'custom', 'css_filters_saturate': px(0), 'css_filters_contrast': px(115)})
    if rot: d.update({'_transform_rotate_popover': 'transform', '_transform_rotateZ_effect': {'unit': 'px', 'size': rot, 'sizes': []}})
    d.update(s); return W('image', **d)
def POLAROID(mid, url, rot, alt=''):
    tape = C([], width={'unit': 'px', 'size': 90}, min_height=px(24), background_background='classic', background_color=TAPE,
             margin=dim(0, 0, -14, 0), _flex_align_self='center', _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': -4, 'sizes': []})
    ph = C([IMG(mid, url, grey=True)], padding=dim(10), background_background='classic', background_color='#F4F1E8',
           border_border='solid', border_width=dim(1), border_color='#D6D0C0',
           _transform_rotate_popover='transform', _transform_rotateZ_effect={'unit': 'px', 'size': rot, 'sizes': []})
    return C([tape, ph], padding=dim(8, 0), flex_gap=gap(0))
def STAMP(l1, l2, l3, size=112):
    return C([H(f'{l1}<br>{l2}<br>{l3}', 10, color=PAPER, tag='div', fam='Inter', align='center', lh=1.5, typography_font_weight='500',
               typography_letter_spacing={'unit': 'px', 'size': 1}, typography_text_transform='uppercase')],
             width={'unit': 'px', 'size': size}, width_tablet={'unit': 'px', 'size': size}, width_mobile={'unit': 'px', 'size': size}, _flex_align_self='flex-start', min_height=px(size), flex_justify_content='center', flex_align_items='center',
             background_background='classic', background_color=RED, border_radius=dim(size // 2),
             border_border='dashed', border_width=dim(2), border_color=PAPER, padding=dim(8))

