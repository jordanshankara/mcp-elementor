"""Pasang situs WP baru dari config JSON: halaman, kategori, menu, Astra (header/footer), widget footer/sidebar, CSS, lalu dorong halaman Elementor.
Pakai:  WPPW=... python3 setup_site.py <dir-situs>/design/site.json     (JSON: host, user, base, pages, cats, menu, astra, footer, css, ...)"""
import json, os, subprocess, sys, pathlib, random
cfgp = pathlib.Path(sys.argv[1]); D = cfgp.parent; C = json.loads(cfgp.read_text())
B = f"https://{C['host']}/wp-json"
def wp(m, p, b=None, t=120):
    c = ['curl', '-sS', '-m', str(t), '-u', f"{C['user']}:{os.environ['WPPW']}", '-X', m, '-H', 'Content-Type: application/json', B + p]
    if b is not None: c += ['-d', json.dumps(b)]
    o = subprocess.check_output(c)
    try: return json.loads(o)
    except Exception: return o[:200]
def ids(els):
    for e in els:
        e['id'] = '%07x' % random.getrandbits(28)
        if e['elType'] == 'widget': e.setdefault('elements', [])
        ids(e.get('elements', []))
def push(pid, name):
    random.seed(11); data = json.load(open(D / f'{name}_sections.json')); ids(data)
    cur = wp('GET', f'/claude/v1/elementor/{pid}')
    r = wp('POST', f'/claude/v1/elementor/{pid}', {'data': json.dumps(data, ensure_ascii=False), 'hash': cur['hash'], 'reason': 'bangun halaman ' + name}); return r.get('ok')
step = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'settings', 'cats', 'pages', 'menu', 'astra', 'widgets', 'css', 'push', 'fixw'}
META = {'theme-transparent-header-meta': 'disabled', 'site-post-title': 'disabled', 'ast-site-content-layout': 'full-width-container', 'site-content-layout': 'plain-container', 'site-content-style': 'unboxed', 'site-sidebar-layout': 'no-sidebar', 'ast-featured-img': 'disabled'}
state = json.loads((D / 'state.json').read_text()) if (D / 'state.json').exists() else {}
if 'settings' in step:
    print('settings', wp('POST', '/wp/v2/settings', {'language': 'id_ID', 'date_format': 'j F Y', 'title': C.get('title') or None, 'description': C.get('tagline') or None, 'posts_per_page': 12}).get('language'))
if 'cats' in step:
    state['cats'] = {}
    for n in C['cats']:
        r = wp('POST', '/wp/v2/categories?_fields=id,slug', {'name': n})
        if isinstance(r, dict) and 'id' not in r and r.get('data', {}).get('term_id'): r = {'id': r['data']['term_id'], 'slug': ''}
        state['cats'][n] = r; print('cat', n, r)
if 'pages' in step:
    state['pages'] = {}
    for key, pg in C['pages'].items():
        if pg.get('id'):
            r = wp('POST', f"/wp/v2/pages/{pg['id']}?_fields=id,link", {'title': pg['title'], 'slug': pg.get('slug'), 'status': 'publish', 'meta': META if pg.get('elementor', True) else {}})
        else:
            r = wp('POST', '/wp/v2/pages?_fields=id,link', {'title': pg['title'], 'slug': pg.get('slug'), 'status': 'publish', 'meta': META if pg.get('elementor', True) else {}})
        state['pages'][key] = r.get('id'); print('page', key, r)
    for dead in C.get('trash_pages', []): print('trash', dead, wp('DELETE', f'/wp/v2/pages/{dead}?_fields=id,status').get('status'))
    for dead in C.get('trash_posts', []): print('trash post', dead, wp('DELETE', f'/wp/v2/posts/{dead}?_fields=id,status').get('status'))
    print('reading', wp('POST', '/wp/v2/settings', {'show_on_front': 'page', 'page_on_front': state['pages']['home'], 'page_for_posts': state['pages']['artikel']}).get('page_on_front'))
json.dump(state, open(D / 'state.json', 'w'), indent=1)
if 'menu' in step:
    m = wp('POST', '/wp/v2/menus?_fields=id', {'name': 'Menu Utama'}); mid = m.get('id') or m.get('data', {}).get('term_id'); print('menu', m)
    for i, (title, key) in enumerate(C['menu']):
        print(' item', title, wp('POST', '/wp/v2/menu-items?_fields=id', {'title': title, 'menus': mid, 'menu_order': i + 1, 'object': 'page', 'object_id': state['pages'][key], 'type': 'post_type', 'status': 'publish'}))
    state['menu'] = mid; json.dump(state, open(D / 'state.json', 'w'), indent=1)
if 'astra' in step:
    A = dict(C['astra']); mid = state.get('menu')
    print('astra', wp('POST', '/claude/v1/theme-option', {'name': 'astra-settings', 'merge': A, 'nav_menu_locations': {'primary': mid, 'mobile_menu': mid, 'footer_menu': mid, 'secondary_menu': mid}, 'theme_mods': {'custom_logo': C['custom_logo']}}))
if 'widgets' in step:
    for sb, blocks in C['footer'].items():
        for html in blocks:
            r = wp('POST', '/wp/v2/widgets?_fields=id,sidebar', {'id_base': 'block', 'sidebar': sb, 'instance': {'raw': {'content': '<!-- wp:html -->\n' + html + '\n<!-- /wp:html -->'}}})
            if r.get('sidebar') != sb: r = wp('PUT', f"/wp/v2/widgets/{r['id']}?_fields=id,sidebar", {'sidebar': sb})
            print('widget', sb, r)
    if C.get('sidebar'):
        for w in wp('GET', '/wp/v2/widgets?sidebar=sidebar-1&_fields=id'): wp('DELETE', f"/wp/v2/widgets/{w['id']}?force=true")
        for html in C['sidebar']:
            r = wp('POST', '/wp/v2/widgets?_fields=id,sidebar', {'id_base': 'block', 'sidebar': 'sidebar-1', 'instance': {'raw': {'content': html}}})
            if r.get('sidebar') != 'sidebar-1': r = wp('PUT', f"/wp/v2/widgets/{r['id']}?_fields=id,sidebar", {'sidebar': 'sidebar-1'})
            print('sidebar', r)
if 'css' in step:
    print('css', wp('POST', '/claude/v1/custom-css', {'css': (D / C['css']).read_text()}))
    print(wp('POST', '/claude/v1/flush'))
if 'push' in step:
    for key, pg in C['pages'].items():
        if pg.get('elementor', True) and (D / f'{key}_sections.json').exists(): print('push', key, state['pages'][key], push(state['pages'][key], key))
    print(wp('POST', '/claude/v1/purge'))

if 'fixw' in step:  # widget sering kembali ke wp_inactive_widgets setelah flush/push: pasang ulang ke sidebar yang benar
    sbs = wp('GET', '/wp/v2/sidebars?_fields=id,widgets'); inactive = [w for x in sbs if x['id'] == 'wp_inactive_widgets' for w in x['widgets']]
    order = sorted(inactive, key=lambda w: int(w.split('-')[-1]))
    targets = [f'footer-widget-{i+1}' for i in range(len(C['footer']))]
    foot_ids = order[:sum(len(v) for v in C['footer'].values())]; side_ids = order[len(foot_ids):]
    for w, sb in zip(foot_ids, targets): print('fixw', w, sb, wp('PUT', f'/wp/v2/widgets/{w}?_fields=id,sidebar', {'sidebar': sb}).get('sidebar'))
    for w in side_ids: print('fixw', w, 'sidebar-1', wp('PUT', f'/wp/v2/widgets/{w}?_fields=id,sidebar', {'sidebar': 'sidebar-1'}).get('sidebar'))
    print([(x['id'], len(x['widgets'])) for x in wp('GET', '/wp/v2/sidebars?_fields=id,widgets')])
