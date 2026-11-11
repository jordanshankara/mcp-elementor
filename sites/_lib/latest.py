"""Ambil N artikel terbit terbaru (REST publik) -> latest.json untuk kartu 'Artikel terbaru' di Home.
Pakai: python3 latest.py <host> <folder-design> [n]   (NODE_USE_ENV_PROXY tidak perlu; pakai curl)"""
import json, subprocess, sys, pathlib, html, re
BULAN = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember']
def fmt(d): y, m, dd = d[:10].split('-'); return f'{int(dd)} {BULAN[int(m)-1]} {y}'
def fetch(host, n=3):
    u = f'https://{host}/wp-json/wp/v2/posts?per_page={n}&_embed=wp:featuredmedia&_fields=id,link,title,date,featured_media,_embedded'
    out = []
    for p in json.loads(subprocess.check_output(['curl', '-sS', '-m', '40', u])):
        m = (p.get('_embedded', {}).get('wp:featuredmedia') or [{}])[0]; sz = (m.get('media_details') or {}).get('sizes', {})
        img = (sz.get('large') or sz.get('medium_large') or {}).get('source_url') or m.get('source_url')
        out.append({'title': html.unescape(re.sub('<[^>]+>', '', p['title']['rendered'])), 'url': p['link'], 'date': fmt(p['date']), 'id': m.get('id') or 0, 'img': img})
    return out
def load(design_dir):
    f = pathlib.Path(design_dir) / 'latest.json'
    return json.loads(f.read_text()) if f.exists() else []
if __name__ == '__main__':
    host, d = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    r = fetch(host, n); (pathlib.Path(d) / 'latest.json').write_text(json.dumps(r, ensure_ascii=False, indent=1)); print(host, len(r), [x['title'][:40] for x in r])
