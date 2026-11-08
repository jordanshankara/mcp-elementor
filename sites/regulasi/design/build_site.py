"""Generate RegulasiAI design pages (HTML) from copy.json. Text of the brief comes ONLY from copy.json ids (verbatim).
BARU (new, not in brief) strings are in the BARU section and wrapped in <span class="new">.
Usage: python build_site.py  -> p1..p6.html + all.html (for copydiff)"""
import json, html, pathlib

D = pathlib.Path(__file__).parent
txt = {i["id"]: i["text"] for i in json.loads((D / "copy.json").read_text(encoding="utf-8"))["items"]}
def T(n): return html.escape(txt[f"c{n:03d}"])
def N(s): return f'<span class="new">{html.escape(s)}</span>'   # BARU

ICON = {
 "doc": "M7 3h7l4 4v14H7z M14 3v4h4 M9 12h6 M9 16h6",
 "shield": "M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z",
 "scale": "M12 4v16 M7 20h10 M5 7h14 M5 7l-3 7a3 3 0 006 0z M19 7l-3 7a3 3 0 006 0z",
 "globe": "M12 3a9 9 0 100 18 9 9 0 000-18z M3 12h18 M12 3c3 3 3 15 0 18 M12 3c-3 3-3 15 0 18",
 "building": "M4 21h16 M6 21V9l6-4 6 4v12 M10 21v-6h4v6",
 "chart": "M4 20V4 M4 20h16 M8 16v-5 M12 16V8 M16 16v-3",
 "search": "M11 4a7 7 0 100 14 7 7 0 000-14z M21 21l-5-5",
 "arrow": "M5 12h14 M13 6l6 6-6 6",
 "chev": "M6 9l6 6 6-6",
 "check": "M5 12l4 4 10-10",
 "lock": "M6 11h12v9H6z M8 11V8a4 4 0 018 0v3",
 "bot": "M5 8h14v10H5z M12 4v4 M9 13h.01 M15 13h.01",
 "eye": "M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z M12 9a3 3 0 100 6 3 3 0 000-6z",
 "book": "M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3z M5 17a3 3 0 013-3h11",
 "link": "M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1 M14 10a4 4 0 00-5.7 0l-3 3A4 4 0 0011 18.7l1-1",
}
def ico(n, s=22): return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="{ICON[n]}"/></svg>'

CSS = """
:root{--gold:#C9A24A;--golddk:#8A6A1F;--navy:#0B1B3A;--navy2:#16305F;--ivory:#E8DAC0;--ivory2:#F6F0E4;--slate:#445069;--line:#E6DCC8;--muted:#8C93A3;--white:#fff;
--ok:#2f7d5b;--warn:#8A6A1F;--bad:#a4452c;--font-h:'Outfit',sans-serif;--font-t:'Inter',sans-serif}
*{box-sizing:border-box}html,body{margin:0}body{font-family:var(--font-t);color:var(--navy);font-size:16px;line-height:1.5;background:#fff}
.page{position:relative;width:1440px;background:#fff;overflow:hidden}
h1,h2,h3,h4{font-family:var(--font-h);font-weight:500;margin:0}
.wrap{width:1140px;margin:0 auto;position:relative}
a{color:inherit;text-decoration:none}
.new{font-style:normal}
/* strip + header */
.strip{height:40px;background:linear-gradient(90deg,var(--navy),var(--navy2));color:#fff;font-size:12px}
.strip .wrap{display:flex;justify-content:space-between;align-items:center;height:40px}
.strip b{color:var(--gold);font-weight:500;letter-spacing:.02em}
.hdr{height:90px;background:#fff;border-bottom:1px solid var(--line)}
.hdr .wrap{display:flex;align-items:center;justify-content:space-between;height:90px}
.logo{font-family:var(--font-h);font-weight:500;font-size:28px;color:var(--navy);display:flex;align-items:center;gap:10px}
.logo i{width:34px;height:34px;border-radius:10px;background:linear-gradient(150deg,#E0BC6A,#B8892E);display:inline-block}
.nav{display:flex;gap:26px;font-size:14px;font-weight:500;color:var(--slate)}
.nav .on{color:var(--golddk)}
.sbtn{width:46px;height:46px;border-radius:50%;background:var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center}
/* hero */
.hero{background:linear-gradient(150deg,var(--navy2) 0%,var(--navy) 100%);height:600px;color:#fff;border-bottom:4px solid var(--gold)}
.hero .wrap{height:600px}
.hero h1{color:var(--ivory2);position:absolute;left:0;top:70px;width:790px;font-size:56px;line-height:1.14}
.hero .sub{position:absolute;left:0;top:250px;width:640px;font-size:20px;line-height:1.45;opacity:.92}
.searchbar{position:absolute;left:0;top:340px;width:760px;height:68px;background:#fff;border-radius:34px;box-shadow:0 12px 32px rgba(3,21,48,.25);display:flex;align-items:center;padding:0 12px 0 26px;gap:14px;color:#64748b;font-size:16px}
.searchbar span{flex:1}.searchbar em{font-style:normal;width:46px;height:46px;border-radius:50%;background:var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:52px;padding:0 26px;border-radius:26px;font-weight:600;font-size:15px}
.btn.w{background:#fff;color:var(--navy)}.btn.o{border:2px solid rgba(255,255,255,.75);color:#fff}.btn.b{background:var(--gold);color:var(--navy)}.btn.p{background:var(--gold);color:var(--navy)}
.hero .ctas{position:absolute;left:0;top:430px;display:flex;gap:18px}
.glass{position:absolute;left:810px;top:60px;width:330px;height:380px;border-radius:20px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.45);box-shadow:0 8px 32px rgba(0,0,0,.35);padding:24px;color:#fff;display:flex;flex-direction:column;gap:12px}
.glass .tag{color:var(--gold);font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.85}
.glass h4{font-size:19px;line-height:1.3}
.glass .m{font-size:13px;opacity:.9}
.badge{display:inline-block;font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;background:#fff}
.badge.ok{color:var(--ok)}.badge.warn{color:var(--warn)}.badge.bad{color:var(--bad)}.badge.t{background:var(--ivory2);color:var(--golddk)}
.glass .lk{margin-top:auto;font-size:14px;font-weight:600;display:flex;gap:8px;align-items:center}
/* bridge */
.bridge{position:relative;margin-top:-80px;height:200px;background:#fff;border-radius:16px;box-shadow:0 18px 48px rgba(3,21,48,.18);display:flex;align-items:center;justify-content:space-between;padding:0 40px;z-index:3}
.bridge p{margin:0;width:700px;font-size:18px;line-height:1.55;color:var(--slate)}
/* sections */
.sec{padding:50px 0 70px}
.st{font-size:32px;line-height:1.2}
.st::after{content:"";display:block;width:56px;height:4px;border-radius:2px;background:var(--gold);margin-top:12px}
.ss{margin:14px 0 0;color:var(--slate);font-size:16px}
.tint{background:var(--ivory2)}.lav{background:var(--ivory)}
.grid3{display:grid;grid-template-columns:repeat(3,250px);gap:30px 30px;width:810px}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 6px 20px rgba(3,21,48,.06)}
.cat{min-height:165px;padding:24px;display:flex;flex-direction:column;gap:14px}
.cat h4{font-size:18px;line-height:1.3}
.ic{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;flex:none}
.c0{background:var(--gold);color:var(--navy)}.c1{background:var(--navy2)}.c2{background:var(--ivory);color:var(--navy)}.c3{background:var(--navy)}
.side{background:var(--navy);border-radius:14px;padding:12px 24px;color:#fff;width:300px;height:250px}
.side div{display:flex;justify-content:space-between;align-items:center;height:45px;border-bottom:1px solid rgba(255,255,255,.14);font-size:14px}
.side div:last-child{border:0}
/* update */
.dark{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 100%);color:#fff;padding:60px 0 60px}
.dark .st{color:#fff}
.tabsp{background:#fff;color:var(--navy);border-radius:14px;box-shadow:0 18px 48px rgba(0,0,0,.28);padding:20px 24px 14px;width:690px}
.tabs{display:flex;gap:6px;font-size:13px;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:0}
.tabs span{padding:10px 14px;color:var(--slate)}.tabs .on{color:var(--golddk);border-bottom:3px solid var(--gold);margin-bottom:-1px}
.grp{font-family:var(--font-h);font-weight:500;font-size:17px;margin:18px 0 6px}
.row{display:flex;gap:16px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}
.row:last-child{border:0}
.row .ic{width:42px;height:42px}
.row h5{margin:0;font-family:var(--font-h);font-weight:500;font-size:15px;line-height:1.3}
.row .mm{font-size:12px;color:var(--slate);margin-top:2px}
.row .badge{margin-left:auto;white-space:nowrap}
/* topics + countries */
.two{display:flex;gap:30px;margin-top:0}
.topics{border:1px solid var(--line);border-radius:14px;padding:18px 20px;display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;width:490px;margin-top:26px}
.topics div{display:flex;gap:10px;align-items:center;font-size:13px;font-weight:500;height:44px;line-height:1.25}
.topics .ic{width:34px;height:34px}
.ctry{display:grid;grid-template-columns:repeat(5,112px);gap:15px;margin-top:26px}
.ctry div{height:115px;border-radius:12px;background:#fff;border:1px solid var(--line);box-shadow:0 6px 20px rgba(3,21,48,.06);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;text-align:center;font-weight:600;font-size:13px;padding:0 6px;line-height:1.25}
.ctry b{font-family:var(--font-h);font-weight:500;width:40px;height:40px;border-radius:50%;background:var(--ivory2);color:var(--golddk);display:flex;align-items:center;justify-content:center;font-size:14px}
/* cta teaser */
.ctac{width:540px;height:300px;border-radius:16px;background:linear-gradient(150deg,#D8B462,#B8892E);color:var(--navy);padding:40px;box-shadow:0 18px 40px rgba(11,27,58,.25)}
.ctac p{margin:0 0 30px;font-size:17px;line-height:1.55}
.tz{width:570px;height:100px;padding:0 26px;display:flex;align-items:center;gap:20px;margin-bottom:15px}
.tz h4{font-size:19px}.tz p{margin:2px 0 0;font-size:13px;color:var(--slate);line-height:1.4}
.tz .go{margin-left:auto;color:var(--golddk)}
/* footer */
.ftr{background:var(--navy);color:#cbd5e1;padding:44px 0 0;height:360px;font-size:14px}
.ftr .logo{color:#fff}
.fc{display:flex;gap:70px}
.fc h6{margin:0 0 14px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}
.fc a{display:block;margin-bottom:12px}
.ftr .disc{position:absolute;left:0;bottom:36px;font-size:13px;color:var(--muted);border-top:1px solid rgba(255,255,255,.12);width:1140px;padding-top:20px}
/* inner pages */
.band{border-bottom:4px solid var(--gold);height:260px;background:linear-gradient(150deg,var(--navy2),var(--navy));color:#fff}
.band .wrap{padding-top:66px}.band h1{font-size:44px;line-height:1.15}.band p{margin:14px 0 0;width:820px;font-size:18px;opacity:.93}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chip{padding:9px 16px;border-radius:20px;background:var(--ivory2);color:var(--golddk);font-size:14px;font-weight:500;border:1px solid #E3D2A6}
.chip.on{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.filt{display:flex;gap:14px;padding:16px;border-radius:14px;margin:20px 0 30px;align-items:center}
.fld{flex:1;height:50px;border:1px solid var(--line);border-radius:10px;padding:0 14px;display:flex;align-items:center;justify-content:space-between;font-size:14px;color:var(--slate);background:#fff;gap:8px}
.fld small{display:block;font-size:11px;color:#64748b;line-height:1}
.docs{display:flex;flex-direction:column;gap:20px}
.doc{display:flex;overflow:hidden;min-height:140px}
.doc .bar{width:6px;flex:none}
.doc .bd{padding:20px 24px;flex:1}
.doc h3{font-size:20px;line-height:1.3}
.doc .meta{font-size:13px;color:var(--slate);margin:6px 0 8px}
.doc .sm{font-size:14px;color:var(--slate);margin:0 0 12px}
.doc .ft{display:flex;gap:14px;align-items:center;font-size:13px}
.doc .ft a{color:var(--golddk);font-weight:600;display:flex;gap:6px;align-items:center}
.doc .ft span{color:#64748b}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px}
.pill.ok{background:#e6f7f0;color:var(--ok)}.pill.warn{background:#fdf3e1;color:var(--warn)}.pill.bad{background:#fdece4;color:var(--bad)}.pill.t{background:var(--ivory2);color:var(--golddk)}
.pager{display:flex;gap:8px;justify-content:center;margin:34px 0 0}
.pager span{width:40px;height:40px;border-radius:10px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;color:var(--slate)}
.pager .on{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.legend{display:flex;gap:28px;font-size:14px;color:var(--slate);margin-bottom:18px}.legend span{display:flex;gap:8px;align-items:center}.legend svg{color:var(--golddk)}
.lib{display:flex;gap:30px;align-items:flex-start}
.fside{width:300px;background:var(--navy);border-radius:14px;padding:26px 24px;color:#fff;flex:none}
.fside .g{margin-bottom:22px}.fside .g b{display:block;font-family:var(--font-h);font-weight:500;font-size:17px;margin-bottom:10px}
.fside .o{display:flex;gap:10px;align-items:center;font-size:13px;color:#cbd5e1;margin-bottom:8px}
.fside .o i{width:16px;height:16px;border:1.5px solid #64748b;border-radius:4px;display:inline-block}.fside .o i.on{background:var(--gold);border-color:var(--golddk)}
.dl{display:grid;grid-template-columns:230px 1fr;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:26px}
.dl div{padding:12px 20px;border-bottom:1px solid var(--line);font-size:14px}
.dl .k{background:var(--ivory2);color:var(--slate);font-weight:600}.dl div:nth-last-child(-n+2){border-bottom:0}
.cmp{width:1140px;border-collapse:separate;border-spacing:0;border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14px}
.cmp th{background:var(--navy);color:#fff;font-family:var(--font-h);font-weight:500;padding:16px 12px;text-align:center}
.cmp th:first-child{text-align:left;width:270px}
.cmp td{padding:18px 12px;border-top:1px solid var(--line);text-align:center;color:var(--slate)}
.cmp td:first-child{text-align:left;font-weight:600;color:var(--navy);background:var(--ivory2)}
.dot{display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--gold)}.dot.e{background:#fff;border:2px solid var(--line)}
.sum3{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:36px}
.sum3 .card{padding:24px}.sum3 h4{font-size:20px;margin:10px 0 8px}.sum3 p{margin:0;font-size:14px;color:var(--slate)}
.info{display:flex;gap:60px;padding:46px 0;border-bottom:1px solid var(--line)}
.info .l{width:560px}.info .r{flex:1}.info p{margin:16px 0 0;font-size:16px;color:var(--slate);line-height:1.6}
.li{display:flex;gap:14px;align-items:center;padding:13px 0;border-bottom:1px solid var(--line);font-size:15px;font-weight:500}
.li:last-child{border:0}.li .ic{width:34px;height:34px}
.acc .li{justify-content:space-between}.acc .li svg{color:var(--golddk)}
.form{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px;display:grid;grid-template-columns:1fr 1fr;gap:16px;box-shadow:0 6px 20px rgba(3,21,48,.06)}
.form .f{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:var(--slate)}
.form .f.full{grid-column:1/3}
.form .in{height:46px;border:1px solid var(--line);border-radius:10px;background:#f8fafc}.form .in.ta{height:96px}
.form .btn{grid-column:1/3;justify-self:start}
"""

def head(title): return f'<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><title>{title}</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>'

NAV = [43, 61, 81, 104, 122, 140]
def header(on=0):
    nav = "".join(f'<a class="{"on" if i == on else ""}">{T(n)}</a>' for i, n in enumerate(NAV))
    return (f'<div class="strip"><div class="wrap"><b>{T(29)}</b><span>{T(227)}</span></div></div>'
            f'<div class="hdr"><div class="wrap"><div class="logo"><i></i>{T(3)}</div><div class="nav">{nav}</div><div class="sbtn">{ico("search")}</div></div></div>')
def footer():
    c2 = "".join(f"<a>{T(n)}</a>" for n in (61, 81, 104, 122, 140))
    c3 = "".join(f"<a>{T(n)}</a>" for n in (164, 175, 187, 204, 217))
    return (f'<div class="ftr"><div class="wrap" style="height:316px"><div class="fc"><div style="width:300px"><div class="logo"><i></i>{T(3)}</div>'
            f'<p style="margin:16px 0 8px;color:#fff">{T(287)}</p><p style="margin:0;line-height:1.6;font-size:13px">{T(33)}</p></div>'
            f'<div><h6>{N("Regulasi")}</h6>{c2}</div><div><h6>{N("Informasi")}</h6>{c3}</div></div>'
            f'<div class="disc">{T(290)}</div></div></div>')
def band(title, sub=None):
    return f'<div class="band"><div class="wrap"><h1>{title}</h1>{f"<p>{sub}</p>" if sub else ""}</div></div>'
def doc(title, meta, jenis, status, sm, date, bar="var(--gold)"):
    cls = {"Berlaku": "ok", "Draf": "warn", "Dicabut": "bad"}[status]
    return (f'<div class="card doc"><div class="bar" style="background:{bar}"></div><div class="bd"><h3>{N(title)}</h3>'
            f'<div class="meta">{N(meta)} &nbsp; <span class="pill t">{N(jenis)}</span> <span class="pill {cls}">{N(status)}</span></div>'
            f'<p class="sm">{N(sm)}</p><div class="ft"><a>{ico("link",16)}{T(154)}</a><span>{T(155)}: {N(date)}</span></div></div></div>')

DOCS = [
 ("Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi", "Indonesia · Pemerintah RI · 2022", "Undang-undang", "Berlaku", "Contoh ringkasan singkat; ringkasan tidak menggantikan isi resmi dokumen.", "contoh"),
 ("Surat Edaran Menteri Komunikasi dan Informatika Nomor 9 Tahun 2023 tentang Etika Kecerdasan Artifisial", "Indonesia · Kemkominfo · 2023", "Pedoman", "Berlaku", "Contoh ringkasan singkat; ringkasan tidak menggantikan isi resmi dokumen.", "contoh"),
 ("Strategi Nasional Kecerdasan Artifisial Indonesia 2020–2045", "Indonesia · 2020", "Strategi nasional", "Berlaku", "Contoh ringkasan singkat; ringkasan tidak menggantikan isi resmi dokumen.", "contoh"),
 ("Regulation (EU) 2024/1689 (EU AI Act)", "Uni Eropa · Parlemen Eropa dan Dewan · 2024", "Peraturan", "Berlaku", "Contoh ringkasan singkat; ringkasan tidak menggantikan isi resmi dokumen.", "contoh"),
 ("Model AI Governance Framework, Second Edition", "Singapura · IMDA dan PDPC · 2020", "Pedoman", "Berlaku", "Contoh ringkasan singkat; ringkasan tidak menggantikan isi resmi dokumen.", "contoh"),
 ("Executive Order 14110 tentang AI yang aman dan tepercaya", "Amerika Serikat · Gedung Putih · 2023", "Perintah eksekutif", "Dicabut", "Contoh ringkasan singkat; status contoh, verifikasi ke sumber resmi.", "contoh"),
]
BAR = {"Berlaku": "var(--ok)", "Draf": "var(--warn)", "Dicabut": "var(--bad)"}
def D_(i): d = DOCS[i]; return doc(d[0], d[1], d[2], d[3], d[4], d[5], BAR[d[3]])
def fld(label, val): return f'<div class="fld"><div><small>{label}</small>{val}</div>{ico("chev",16)}</div>'

CODES = ["ID", "US", "EU", "GB", "SG", "KR", "JP", "CN", "CA", "AU"]

# ---------------- P1 ----------------
cats = [(67, "building", "c0"), (68, "scale", "c1"), (69, "lock", "c2"), (70, "chart", "c3"), (71, "globe", "c0"), (72, "doc", "c1")]
cat_html = "".join(f'<div class="card cat"><div class="ic {c}">{ico(i)}</div><h4>{T(n)}</h4></div>' for n, i, c in cats)
side_html = "".join(f'<div><span>{T(n)}</span>{ico("arrow",16)}</div>' for n in range(75, 80))
topic_icons = ["scale", "lock", "bot", "eye", "shield", "scale", "building", "building", "chart", "doc", "eye"]
topics_html = "".join(f'<div><span class="ic {"c0" if i % 2 == 0 else "c3"}">{ico(topic_icons[i],17)}</span>{T(126 + i)}</div>' for i in range(11))
ctry_html = "".join(f'<div><b>{N(CODES[i])}</b>{T(87 + i)}</div>' for i in range(10))
def rows(items):
    return "".join(f'<div class="row"><span class="ic c{k % 4}">{ico("doc",20)}</span><div><h5>{N(d[0])}</h5><div class="mm">{N(d[1])}</div></div><span class="pill {"ok" if d[3]=="Berlaku" else "bad"}">{N(d[3])}</span></div>' for k, d in enumerate(items))
p1 = (head("RegulasiAI - Beranda") + '<div class="page">' + header(0) +
 f'<div class="hero"><div class="wrap"><h1>{T(31)}</h1><div class="sub">{T(56)}</div>'
 f'<div class="searchbar">{ico("search")}<span>{N("Cari peraturan, kebijakan, pedoman…")}</span><em>{ico("arrow",20)}</em></div>'
 f'<div class="ctas"><a class="btn w">{T(37)}</a><a class="btn o">{T(38)}</a></div>'
 f'<div class="glass"><div class="tag">{N("Contoh tampilan")}</div><h4>{N(DOCS[1][0])}</h4><div class="m">{N(DOCS[1][1])}</div>'
 f'<div><span class="badge ok">{N("Berlaku")}</span> &nbsp; <span class="badge t">{N("Pedoman")}</span></div>'
 f'<div class="lk">{T(154)} {ico("arrow",16)}</div></div></div></div>'
 f'<div class="wrap"><div class="bridge"><p>{T(35)}</p><a class="btn b">{T(40)}</a></div></div>'
 f'<div class="sec tint" style="margin-top:-120px;padding-top:170px"><div class="wrap"><h2 class="st">{T(48)}</h2>'
 f'<div class="two" style="margin-top:34px"><div class="grid3">{cat_html}</div><div><div class="side">{side_html}</div><a class="btn p" style="margin-top:25px;width:300px;border-radius:14px;height:70px">{T(73)}</a></div></div></div></div>'
 f'<div class="dark"><div class="wrap two"><div style="width:420px;padding-right:20px"><h2 class="st">{T(164)}</h2><p style="margin:22px 0 28px;opacity:.88;line-height:1.55">{T(168)}</p>'
 f'<div class="glass" style="position:static;width:400px;height:230px"><div class="tag">{N("Contoh tampilan")}</div><h4>{N(DOCS[3][0])}</h4><div class="m">{N(DOCS[3][1])}</div><div class="lk">{T(154)} {ico("arrow",16)}</div></div></div>'
 f'<div class="tabsp"><div class="tabs"><span class="on">{T(170)}</span><span>{T(171)}</span><span>{T(172)}</span><span>{T(173)}</span></div>'
 f'<div class="grp">{T(49)}</div>{rows(DOCS[0:2])}<div class="grp">{T(50)}</div>{rows(DOCS[3:5])}</div></div></div>'
 f'<div class="sec"><div class="wrap two"><div style="width:490px"><h2 class="st">{T(51)}</h2><p class="ss">{T(138)}</p><div class="topics">{topics_html}</div></div>'
 f'<div style="width:620px;margin-left:0"><h2 class="st">{T(52)}</h2><div class="ctry">{ctry_html}</div></div></div></div>'
 f'<div class="sec lav"><div class="wrap two" style="align-items:flex-start"><div class="ctac"><p>{T(144)}</p><a class="btn w">{T(39)}</a></div>'
 f'<div>' + "".join(f'<div class="card tz"><span class="ic c{k}">{ico(ic)}</span><div><h4>{T(t)}</h4><p>{T(d)}</p></div><span class="go">{ico("arrow")}</span></div>' for k, (t, d, ic) in enumerate([(175, 179, "book"), (187, 202, "doc"), (204, 215, "link")])) +
 f'</div></div></div>' + footer() + '</div></body></html>')

# ---------------- P2 ----------------
p2 = (head("RegulasiAI - Regulasi Indonesia") + '<div class="page">' + header(1) + band(T(61), T(65)) +
 f'<div class="sec" style="padding-bottom:60px"><div class="wrap"><div class="chips">' + "".join(f'<span class="chip{" on" if i==0 else ""}">{T(67+i)}</span>' for i in range(7)) + '</div>'
 f'<div class="card filt">{fld(T(76), N("Semua"))}{fld(T(75), N("Semua tahun"))}{fld(T(77), N("Semua lembaga"))}{fld(T(78), N("Semua status"))}<div class="fld" style="flex:1.3">{ico("search",18)}<span style="flex:1;margin-left:6px">{T(79)}</span></div></div>'
 f'<div class="docs">{D_(0)}{D_(1)}{D_(2)}{D_(5)}</div><div class="pager"><span class="on">1</span><span>2</span><span>3</span><span>›</span></div></div></div>' + footer() + '</div></body></html>')

# ---------------- P3 ----------------
p3 = (head("RegulasiAI - Regulasi Global") + '<div class="page">' + header(2) + band(T(81), T(85)) +
 f'<div class="sec" style="padding-bottom:60px"><div class="wrap"><div class="card filt" style="margin-top:0">{fld(T(98), N("Semua negara"))}{fld(T(99), N("Semua tahun"))}{fld(T(100), N("Semua topik"))}</div>'
 f'<div class="legend"><span>{ico("link",18)}{T(101)}</span><span>{ico("doc",18)}{T(102)}</span></div>'
 f'<div class="chips" style="margin-bottom:30px">' + "".join(f'<span class="chip{" on" if i==2 else ""}">{T(87+i)}</span>' for i in range(10)) + '</div>'
 f'<div class="docs">{D_(3)}{D_(4)}{D_(5)}</div></div></div>' + footer() + '</div></body></html>')

# ---------------- P4 ----------------
def grp(label, opts): return f'<div class="g"><b>{T(label)}</b>' + "".join(f'<div class="o"><i class="{"on" if k==0 else ""}"></i>{N(o)}</div>' for k, o in enumerate(opts)) + '</div>'
dl_keys = list(range(146, 156)); dl_vals = [DOCS[3][0], "Uni Eropa", "Parlemen Eropa dan Dewan", "2024", "Peraturan", "Berlaku", "Tata kelola AI", "Contoh ringkasan singkat", "Sumber resmi (contoh)", "contoh"]
dl_html = "".join(f'<div class="k">{T(k)}</div><div>{N(v)}</div>' for k, v in zip(dl_keys, dl_vals))
p4 = (head("RegulasiAI - Pustaka Dokumen") + '<div class="page">' + header(5) + band(T(140), T(144)) +
 f'<div class="sec" style="padding-bottom:60px"><div class="wrap"><div class="lib"><div class="fside">{grp(157,["Semua","Indonesia","Uni Eropa"])}{grp(158,["2024","2023","2022"])}{grp(159,["Peraturan","Pedoman","Strategi"])}{grp(160,["Etika AI","Privasi","AI generatif"])}{grp(161,["Berlaku","Draf","Dicabut"])}{grp(162,["Kementerian","Badan pengatur","Organisasi internasional"])}</div>'
 f'<div style="flex:1"><div class="docs">{D_(0)}{D_(3)}{D_(4)}</div><div class="dl">{dl_html}</div></div></div></div></div>' + footer() + '</div></body></html>')

# ---------------- P5 ----------------
cols = [87, 88, 89, 90, 91]
marks = [[1, 1, 0, 1, 1], [1, 0, 1, 1, 1], [0, 1, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]]
cmp_html = f'<table class="cmp"><tr><th></th>' + "".join(f'<th>{T(c)}</th>' for c in cols) + '</tr>' + "".join(
    f'<tr><td>{T(115+r)}</td>' + "".join(f'<td><span class="dot{"" if m else " e"}"></span></td>' for m in marks[r]) + '</tr>' for r in range(6)) + '</table>'
sums = [("Indonesia", "Kombinasi undang-undang, surat edaran etika AI, dan strategi nasional (contoh)."), ("Uni Eropa", "Kerangka lintas negara anggota dengan pendekatan berbasis tingkat risiko (contoh)."), ("Singapura", "Pedoman tata kelola sukarela untuk sektor swasta (contoh).")]
p5 = (head("RegulasiAI - Perbandingan Negara") + '<div class="page">' + header(3) + band(T(104), T(108)) +
 f'<div class="sec" style="padding-bottom:70px"><div class="wrap"><div style="margin-bottom:18px;font-size:13px;color:var(--slate)">{N("Contoh tampilan: isi sel belum final")}</div>{cmp_html}'
 f'<div class="sum3">' + "".join(f'<div class="card"><span class="ic c{k}">{ico("globe",20)}</span><h4>{N(a)}</h4><p>{N(b)}</p></div>' for k, (a, b) in enumerate(sums)) + '</div></div></div>' + footer() + '</div></body></html>')

# ---------------- P6 ----------------
def li(items, icn=None, accord=False): return ''.join(f'<div class="li">' + (f'<span class="ic c{k%4}">{ico(icn)}</span>' if icn else '') + f'<span style="flex:1">{T(n)}</span>' + (ico("chev", 18) if accord else '') + '</div>' for k, n in enumerate(items))
def info(title_n, copy_n, items, icn=None, accord=False, extra=''):
    return f'<div class="info"><div class="l"><h2 class="st">{T(title_n)}</h2><p>{T(copy_n)}</p>{extra}</div><div class="r{" acc" if accord else ""}">{li(items, icn, accord)}</div></div>'
form_labels = [233, 234, 235, 236, 237, 238]
form = ('<div class="form">' + "".join(f'<div class="f{" full" if n==238 else ""}">{T(n)}<div class="in{" ta" if n==238 else ""}"></div></div>' for n in form_labels) + f'<a class="btn b">{N("Kirim")}</a></div>')
p6 = (head("RegulasiAI - Halaman Informasi") + '<div class="page">' + header(0) + band(T(217)) .replace('</div></div>', f'</div></div>', 1) +
 f'<div class="wrap">' +
 f'<div class="info"><div class="l"><p style="margin-top:0">{T(219)}</p><p>{T(8)}</p></div><div class="r">{li(range(221,226),"check")}</div></div>' +
 info(175, 179, range(181, 186), "check") + info(187, 202, range(191, 201), None, True) + info(204, 215, range(208, 214), "link") +
 f'<div class="info" style="border:0"><div class="l"><h2 class="st">{T(227)}</h2><p>{T(231)}</p></div><div class="r">{form}</div></div></div>' + footer() + '</div></body></html>')

pages = {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6}
for k, v in pages.items(): (D / f"{k}.html").write_text(v, encoding="utf-8")
body = "".join(v.split("<body>")[1].split("</body>")[0] for v in pages.values())
(D / "all.html").write_text(head("RegulasiAI - semua halaman") + body + "</body></html>", encoding="utf-8")
print("ok", {k: len(v) for k, v in pages.items()})
