"""Pustaka dokumen v2: kartu + sidebar filter + pagination bernomor. Data dari _AI Regulations.xlsx.
Output: library_element.json (semua), library_id.json (Indonesia), library_global.json (tanpa Indonesia).
Jenis/tahun/sumber DIPERKIRAKAN otomatis dari judul + URL (Excel hanya berisi negara, judul, link)."""
import openpyxl, re, json, pathlib
from urllib.parse import urlparse

D = pathlib.Path(__file__).parent
ws = openpyxl.load_workbook(D.parent / "_AI Regulations.xlsx").active
MAP = {"indonesia": ("id", "Indonesia"), "malaysia": ("my", "Malaysia"), "singapore": ("sg", "Singapura"), "korea": ("kr", "Korea Selatan"),
       "china": ("cn", "Tiongkok"), "us": ("us", "Amerika Serikat"), "uk": ("uk", "Inggris"), "france": ("fr", "Prancis"), "italy": ("it", "Italia")}
FLAG = {"id": "bendera-indonesia", "my": "bendera-malaysia", "sg": "bendera-singapura", "kr": "bendera-korea-selatan", "cn": "bendera-tiongkok",
        "us": "bendera-amerika-serikat", "uk": "bendera-inggris", "fr": "bendera-prancis", "it": "bendera-italia"}
BASE = "https://regulasiai.id/wp-content/uploads/2026/11/"

TYPES = [  # urutan = prioritas
    ("Berita & siaran pers", r"press release|siaran pers|media release|\bnews\b|berita|speech|pidato|second reading|statement|briefing|explainer|remarks|解读|答记者问|记者|新闻|조간|보도|experts call|launches|launch of|kolaborasi|membuka kembali|suspends|establishes"),
    ("Rancangan / RUU", r"\bbill\b|rancangan|draft|proposition|proposed|disegno di legge|\bddl\b|h\.r\.|\bs\.\d|house bill|proposta|法案|草案|법률안|consultation"),
    ("Undang-undang & peraturan", r"undang|\buu\b|law\b|\bact\b|regulation|peraturan|loi\b|legge|decree|decreto|provvedimento|public law|executive order|order\b|ordonnance|\bplaw|uscode|条例|办法|规定|法|令|규정|법"),
    ("Pedoman & panduan", r"guideline|guidance|guide\b|pedoman|panduan|advisory|framework|playbook|principles|standard|standar|가이드|안내서|指南|指引|guida|lignes|handbook|templates|memorandum|\bm-2\d"),
    ("Strategi & rencana", r"strateg|roadmap|\bplan\b|blueprint|action plan|peta jalan|programme|program\b|initiative|rencana|pelan|nexus|growth zones|opportunities|nairr|investment"),
]
MEDIA = r"antaranews|thestar|malaymail|etnews|hankyung|segye|mk\.co\.kr|ajunews|nasdaq|newamerica|bsa\.org|utm\.my|korea\.net|rakyatdigital|mohe\.gov\.my/hebahan"

def classify(title, url):
    t = (title + " " + url).lower()
    for name, rx in TYPES:
        if re.search(rx, t, re.I): return name
    return "Dokumen lain"

def year_of(title, url):
    for s in (title, url):
        m = re.findall(r"(?<!\d)(20[12]\d)(?!\d)", s)
        if m: return int(m[0])
    return 0

cur = None; items = []; seen = set()
for row in ws.iter_rows(min_row=2, values_only=True):
    no, neg, _c, jenis, link, nama = (list(row) + [None] * 6)[:6]
    if neg:
        key = str(neg).strip().lower()
        if key.startswith("us"): key = "us"
        cur = MAP.get(key, cur)
    if not link or not str(link).startswith("http") or not cur: continue
    link = str(link).strip()
    title = re.sub(r"\s+", " ", str(nama or "")).strip()
    title = re.sub(r"\.(pdf|txt|docx?)$", "", title, flags=re.I).strip() or urlparse(link).netloc
    if (cur[0], link) in seen: continue
    seen.add((cur[0], link))
    host = urlparse(link).netloc.replace("www.", "")
    src = "Media & analisis" if re.search(MEDIA, link, re.I) else "Lembaga / sumber resmi"
    note = re.sub(r"\s+", " ", str(jenis or "")).strip()
    items.append([cur[0], title[:220], link, host, year_of(title, link), classify(title, link), src, note])

CSS = """
.rl{font-family:Inter,sans-serif;color:#0B1B3A}.rl *{box-sizing:border-box}
.rl-bar{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid #E6DCC8;border-radius:34px;padding:8px 8px 8px 24px;box-shadow:0 8px 24px rgba(11,27,58,.1);margin-bottom:26px}
.rl-bar input{flex:1;min-width:0;border:0!important;outline:0;background:transparent!important;font:400 16px Inter,sans-serif;color:#0B1B3A;box-shadow:none!important;padding:10px 0!important}
.rl-bar b{background:#C9A24A;color:#0B1B3A;border-radius:22px;padding:11px 22px;font:600 14px Inter,sans-serif}
.rl-wrap{display:grid;grid-template-columns:270px 1fr;gap:28px;align-items:start}
.rl-side{position:sticky;top:20px;background:linear-gradient(170deg,#16305F,#0B1B3A);border-radius:18px;padding:22px;color:#E2E8F0;box-shadow:0 14px 36px rgba(11,27,58,.25)}
.rl-side summary{list-style:none;cursor:pointer;font:500 18px Outfit,sans-serif;color:#fff;display:flex;justify-content:space-between;align-items:center}
.rl-side summary::-webkit-details-marker{display:none}
.rl-side summary:after{content:"";width:8px;height:8px;border-right:2px solid #C9A24A;border-bottom:2px solid #C9A24A;transform:rotate(45deg);margin-right:4px}
.rl-side[open] summary:after{transform:rotate(-135deg)}
.rl-g{margin-top:20px}.rl-g h4{margin:0 0 10px;font:600 11px Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#C9A24A}
.rl-o{display:flex;align-items:center;gap:10px;padding:6px 0;font-size:14px;cursor:pointer;color:#E2E8F0;line-height:1.3}
.rl-o input{accent-color:#C9A24A;width:16px;height:16px;margin:0;flex:none}
.rl-o img{width:22px;height:15px;object-fit:cover;border-radius:2px;flex:none}
.rl-o i{margin-left:auto;font-style:normal;font-size:12px;opacity:.65}
.rl-sel{width:100%;height:42px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#fff;padding:0 10px;font:400 14px Inter,sans-serif}
.rl-sel option{color:#0B1B3A}
.rl-reset{margin-top:20px;width:100%;height:42px;border-radius:21px;border:1px solid rgba(255,255,255,.35)!important;background:transparent!important;color:#fff!important;font:500 14px Inter,sans-serif!important;cursor:pointer}
.rl-reset:hover{background:rgba(255,255,255,.1)!important}
.rl-top{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.rl-count{font-size:15px;color:#445069}.rl-count b{color:#0B1B3A;font-family:Outfit,sans-serif;font-size:20px;font-weight:500}
.rl-sort{display:flex;align-items:center;gap:8px;font-size:13px;color:#445069}
.rl-sort select{height:40px;border-radius:20px;border:1px solid #E6DCC8;background:#fff;padding:0 14px;font:500 13px Inter,sans-serif;color:#0B1B3A}
.rl-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.rl-card{display:flex;flex-direction:column;background:#fff;border:1px solid #E6DCC8;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px rgba(11,27,58,.07);transition:transform .18s,box-shadow .18s;text-decoration:none!important;color:inherit!important}
.rl-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(11,27,58,.18)}
.rl-ch{display:flex;align-items:center;gap:10px;padding:13px 18px;background:linear-gradient(120deg,#16305F,#0B1B3A);border-bottom:3px solid #C9A24A}
.rl-ch img{width:32px;height:21px;object-fit:cover;border-radius:3px;box-shadow:0 0 0 1px rgba(255,255,255,.35)}
.rl-ch span{color:#fff;font:600 13px Inter,sans-serif}
.rl-ch em{margin-left:auto;font-style:normal;background:#C9A24A;color:#0B1B3A;border-radius:12px;padding:3px 10px;font:600 11px Inter,sans-serif;white-space:nowrap}
.rl-cb{padding:18px 20px 14px;flex:1;display:flex;flex-direction:column;gap:12px}
.rl-ct{font:500 18px/1.38 Outfit,sans-serif;color:#0B1B3A;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere;min-height:4.14em}
.rl-cm{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12.5px;color:#445069;margin-top:auto}
.rl-cm span{display:inline-flex;align-items:center;gap:6px;background:#F6F0E4;border-radius:12px;padding:4px 10px;overflow-wrap:anywhere}
.rl-cm .y{background:#EEF1F7;font-weight:600}
.rl-cf{display:flex;align-items:center;justify-content:space-between;padding:12px 20px 16px;color:#8A6A1F;font:600 14px Inter,sans-serif}
.rl-cf svg{transition:transform .18s}.rl-card:hover .rl-cf svg{transform:translateX(4px)}
.rl-pg{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:30px 0 4px}
.rl-pg button{min-width:42px;height:42px;padding:0 12px;border-radius:12px;border:1px solid #E6DCC8!important;background:#fff!important;color:#0B1B3A!important;font:600 14px Inter,sans-serif!important;cursor:pointer}
.rl-pg button:hover:not(:disabled){border-color:#C9A24A!important;background:#F6F0E4!important}
.rl-pg button.on{background:#C9A24A!important;border-color:#C9A24A!important}
.rl-pg button:disabled{opacity:.4;cursor:default}.rl-pg span{display:flex;align-items:center;color:#8C93A3}
.rl-empty{display:none;text-align:center;padding:60px 20px;background:#F6F0E4;border-radius:18px;color:#445069}
@media(max-width:1000px){.rl-wrap{grid-template-columns:1fr}.rl-side{position:static}}
@media(max-width:640px){.rl-grid{grid-template-columns:1fr}.rl-bar{padding-left:16px}.rl-bar b{display:none}.rl-ct{font-size:17px}}
"""

JS = r"""
(function(){var root=document.currentScript.closest('.rl');if(!root)return;
var D=JSON.parse(root.querySelector('.rl-data').textContent),ALLOW=root.getAttribute('data-allow').split(','),
FL=JSON.parse(root.getAttribute('data-flags')),CN=JSON.parse(root.getAttribute('data-cn')),SHOWC=root.getAttribute('data-chips')==='1',
PER=12,st={q:'',c:[],t:'',y:'',s:'',sort:'',p:1};
D=D.filter(function(d){return ALLOW.indexOf(d[0])>-1});
var $=function(s){return root.querySelector(s)};
function esc(x){return String(x).replace(/[&<>"]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]})}
function uniq(a){return a.filter(function(v,i){return a.indexOf(v)===i})}
var types=uniq(D.map(function(d){return d[5]})).sort(),years=uniq(D.map(function(d){return d[4]}).filter(Boolean)).sort(function(a,b){return b-a}),srcs=uniq(D.map(function(d){return d[6]})).sort();
function cnt(f){return D.filter(f).length}
function buildSide(){var h='';
if(SHOWC){h+='<div class="rl-g"><h4>Negara</h4>'+ALLOW.map(function(c){return '<label class="rl-o"><input type="checkbox" data-k="c" value="'+c+'"><img src="'+FL[c]+'" alt=""><span>'+CN[c]+'</span><i>'+cnt(function(d){return d[0]===c})+'</i></label>'}).join('')+'</div>'}
h+='<div class="rl-g"><h4>Jenis dokumen <small style="text-transform:none;letter-spacing:0;opacity:.6;font-weight:400">(perkiraan otomatis)</small></h4><select class="rl-sel" data-k="t"><option value="">Semua jenis</option>'+types.map(function(t){return '<option>'+esc(t)+'</option>'}).join('')+'</select></div>';
h+='<div class="rl-g"><h4>Tahun</h4><select class="rl-sel" data-k="y"><option value="">Semua tahun</option>'+years.map(function(y){return '<option>'+y+'</option>'}).join('')+'</select></div>';
h+='<div class="rl-g"><h4>Sumber</h4><select class="rl-sel" data-k="s"><option value="">Semua sumber</option>'+srcs.map(function(s){return '<option>'+esc(s)+'</option>'}).join('')+'</select></div>';
h+='<button type="button" class="rl-reset">Reset filter</button>';
$('.rl-fb').innerHTML=h}
function match(d){var q=st.q.toLowerCase().split(/\s+/).filter(Boolean),hay=(d[1]+' '+CN[d[0]]+' '+d[3]+' '+d[5]+' '+d[4]).toLowerCase();
return q.every(function(w){return hay.indexOf(w)>-1})&&(!st.c.length||st.c.indexOf(d[0])>-1)&&(!st.t||d[5]===st.t)&&(!st.y||String(d[4])===st.y)&&(!st.s||d[6]===st.s)}
var ARROW='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
function card(d){return '<a class="rl-card" href="'+esc(d[2])+'" target="_blank" rel="noopener noreferrer"><div class="rl-ch"><img src="'+FL[d[0]]+'" alt=""><span>'+CN[d[0]]+'</span><em>'+esc(d[5])+'</em></div><div class="rl-cb"><div class="rl-ct">'+esc(d[1])+'</div><div class="rl-cm"><span>'+esc(d[3])+'</span>'+(d[4]?'<span class="y">'+d[4]+'</span>':'')+(d[7]?'<span>'+esc(d[7])+'</span>':'')+'</div></div><div class="rl-cf"><span>Buka dokumen</span>'+ARROW+'</div></a>'}
function pager(n){var pg=Math.ceil(n/PER),h='';if(pg<=1){$('.rl-pg').innerHTML='';return}
function b(p,l,dis,on){return '<button type="button" data-p="'+p+'"'+(dis?' disabled':'')+(on?' class="on"':'')+'>'+l+'</button>'}
h+=b(st.p-1,'‹',st.p===1);var last=0;
for(var i=1;i<=pg;i++){if(i===1||i===pg||Math.abs(i-st.p)<=1){if(last&&i-last>1)h+='<span>…</span>';h+=b(i,i,false,i===st.p);last=i}}
h+=b(st.p+1,'›',st.p===pg);$('.rl-pg').innerHTML=h}
function run(){var m=D.filter(match);
if(st.sort==='az')m.sort(function(a,b){return a[1].localeCompare(b[1])});else if(st.sort==='yr')m.sort(function(a,b){return b[4]-a[4]});
var pg=Math.max(1,Math.ceil(m.length/PER));if(st.p>pg)st.p=pg;
$('.rl-grid').innerHTML=m.slice((st.p-1)*PER,st.p*PER).map(card).join('');
$('.rl-count').innerHTML='<b>'+m.length+'</b> dokumen ditemukan';$('.rl-empty').style.display=m.length?'none':'block';$('.rl-grid').style.display=m.length?'grid':'none';
pager(m.length)}
function go(){st.p=1;run()}
$('.rl-q').addEventListener('input',function(e){st.q=e.target.value;go()});
$('.rl-fb').addEventListener('change',function(e){var k=e.target.getAttribute('data-k');if(k==='c'){st.c=[].slice.call(root.querySelectorAll('input[data-k=c]:checked')).map(function(i){return i.value})}else if(k){st[k]=e.target.value}go()});
$('.rl-fb').addEventListener('click',function(e){if(e.target.classList.contains('rl-reset')){st.c=[];st.t=st.y=st.s='';[].forEach.call(root.querySelectorAll('input[data-k=c]'),function(i){i.checked=false});[].forEach.call(root.querySelectorAll('select[data-k]'),function(s){s.value=''});go()}});
$('.rl-sort select').addEventListener('change',function(e){st.sort=e.target.value;go()});
$('.rl-pg').addEventListener('click',function(e){var p=e.target.getAttribute&&e.target.getAttribute('data-p');if(p){st.p=+p;run();root.scrollIntoView({behavior:'smooth',block:'start'})}});
buildSide();
if(window.innerWidth>1000){$('.rl-side').setAttribute('open','')}
try{var q=new URLSearchParams(location.search).get('q');if(q){st.q=q;$('.rl-q').value=q}}catch(e){}
run()})();
"""

def make(allow, name, show_chips=True):
    sub = [i for i in items if i[0] in allow]
    codes = [c for c, _ in MAP.values() if c in allow]
    data = json.dumps(sub, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    flags = json.dumps({c: BASE + FLAG[c] + ".webp" for c in codes})
    cn = json.dumps({c: n for c, n in MAP.values() if c in allow}, ensure_ascii=False)
    out = (f'<!-- allow-js:pencarian-dokumen (izin pengguna 2026-11-06) -->'
           f'<div class="rl" data-allow="{",".join(codes)}" data-flags=\'{flags}\' data-cn=\'{cn}\' data-chips="{1 if show_chips else 0}">'
           f'<div class="rl-bar"><input class="rl-q" type="search" placeholder="Cari judul dokumen, negara, jenis, atau sumber…" aria-label="Cari dokumen"><b>Cari</b></div>'
           f'<div class="rl-wrap"><details class="rl-side"><summary>Filter</summary><div class="rl-fb"></div></details>'
           f'<div class="rl-main"><div class="rl-top"><div class="rl-count"></div><label class="rl-sort">Urutkan<select><option value="">Urutan awal</option><option value="az">Judul A–Z</option><option value="yr">Tahun terbaru</option></select></label></div>'
           f'<div class="rl-grid"></div><div class="rl-empty">Tidak ada dokumen yang cocok. Ubah kata kunci atau reset filter.</div><div class="rl-pg"></div></div></div>'
           f'<script type="application/json" class="rl-data">{data}</script><style>{CSS}</style><script>{JS}</script></div>')
    side = {"unit": "px", "top": "40", "right": "20", "bottom": "50", "left": "20", "isLinked": False}
    el = {"elType": "container", "settings": {"content_width": "boxed", "boxed_width": {"unit": "px", "size": 1140, "sizes": []}, "flex_direction": "column",
          "padding": {"unit": "px", "top": "50", "right": "0", "bottom": "70", "left": "0", "isLinked": False}, "padding_tablet": side, "padding_mobile": side,
          "background_background": "classic", "background_color": "#FFFFFF"},
          "elements": [{"elType": "widget", "widgetType": "html", "settings": {"html": out}}]}
    (D / name).write_text(json.dumps(el, ensure_ascii=False), encoding="utf-8")
    types = {}
    for i in sub: types[i[5]] = types.get(i[5], 0) + 1
    print(name, len(sub), "dokumen", len(out), "byte", types)

allc = set(c for c, _ in MAP.values())
make(allc, "library_element.json")
make({"id"}, "library_id.json", show_chips=False)
make(allc - {"id"}, "library_global.json")
