"""Pembantu tambahan (kartu bundar, section boxed, grid, pil, gradien) di atas ek.py. Panggil setelah mengatur palet ek.*."""
import ek
from ek import *
def bg(c): return {'background_background': 'classic', 'background_color': c}
def grad(c1, c2, kind='linear', angle=180, pos='center center', **extra):
    d = {'background_background': 'gradient', 'background_color': c1, 'background_color_b': c2, 'background_gradient_type': kind}
    if kind == 'linear': d['background_gradient_angle'] = {'unit': 'deg', 'size': angle, 'sizes': []}
    else: d['background_gradient_position'] = pos
    d.update(extra); return d
def WIDTH(w): return {'width': {'unit': '%', 'size': w}, 'width_tablet': {'unit': '%', 'size': 100}, 'width_mobile': {'unit': '%', 'size': 100}}
def SEC(children, bgc=None, pv=84, wpx=1180, **s):
    st = dict(content_width='boxed', boxed_width=px(wpx), padding=dim(pv, 24), padding_tablet=dim(max(48, pv // 1.5), 24), padding_mobile=dim(44, 18), flex_gap=gap(28))
    if bgc: st.update(bg(bgc))
    st.update(s); return C(children, **st)
def FULL(children, bgc=None, **s):  # container penuh tanpa batas isi (isi diatur sendiri)
    st = dict(content_width='full', flex_gap=gap(0)); 
    if bgc: st.update(bg(bgc))
    st.update(s); return C(children, **st)
def RWRAP(children, g=20, **s):
    st = dict(flex_direction='row', flex_direction_tablet='column', flex_direction_mobile='column', flex_gap=gap(g), flex_wrap='wrap', flex_align_items='stretch'); st.update(s); return C(children, **st)
def ROW2(children, g=20, tablet_row=False, **s):
    st = dict(flex_direction='row', flex_direction_tablet='row' if tablet_row else 'column', flex_direction_mobile='column', flex_gap=gap(g), flex_align_items='stretch'); st.update(s); return C(children, **st)
def CARD(children, bgc='#FFFFFF', r=18, pad=26, border=None, shadow=None, w=None, g=12, **s):
    st = dict(padding=dim(pad), padding_mobile=dim(20), border_radius=dim(r), flex_gap=gap(g), **bg(bgc))
    if border: st.update(border_border='solid', border_width=dim(1), border_color=border)
    if shadow: st.update(box_shadow_box_shadow_type='yes', box_shadow_box_shadow={'horizontal': 0, 'vertical': 10, 'blur': 30, 'spread': 0, 'color': shadow})
    if w: st.update(WIDTH(w))
    st.update(s); return C(children, **st)
def PILLBTN(text, url, bgc, fg, border=None, ext_=False, hover_bg=None, **s):
    link = {'url': url, 'is_external': 'on' if ext_ else '', 'nofollow': ''}
    d = dict(text=text, link=link, align='left', background_color=bgc, button_text_color=fg, border_border='solid' if border else '', border_width=dim(1 if border else 0), border_color=border or bgc,
             border_radius=dim(30), text_padding=dim(15, 28), button_background_hover_color=hover_bg or fg, hover_color=bgc if not hover_bg else fg, button_hover_border_color=hover_bg or fg)
    d.update(typo(ek.BFONT, 14, weight='600', ls=0.2)); d.update(s); return W('button', **d)
def BADGE(text, color, bgc=None, border=None):
    st = dict(padding=dim(7, 16), border_radius=dim(30), _css_classes='bd-badge')
    if bgc: st.update(bg(bgc))
    if border: st.update(border_border='solid', border_width=dim(1), border_color=border)
    return C([W('text-editor', editor=f'<p style="margin:0">{text}</p>', text_color=color, **typo(ek.BFONT, 12, weight='600', ls=0.3, lh=1.2))], **st)
def ICON(name, color, size=26, lib=None):
    lib = lib or ('fa-brands' if name.startswith('fab ') else 'fa-solid')
    return W('icon', selected_icon={'value': name, 'library': lib}, primary_color=color, size={'unit': 'px', 'size': size}, align='left')
def BODY(html, size=16, color=None, **s):
    d = {'editor': html, 'text_color': color or ek.INK}; d.update(typo(ek.BFONT, size, mobile=15 if size > 15 else None, weight='400', lh=1.65)); d.update(s); return W('text-editor', **d)
