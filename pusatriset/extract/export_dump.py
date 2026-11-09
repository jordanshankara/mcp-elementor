"""Ekspor dump mysqldump (gz) -> JSONL per tabel (semua kolom, tipe asli). Streaming, tanpa MySQL.
Tabel berisi data pribadi/internal TIDAK diekspor: users (password_hash), audit_logs, app_settings, submissions, disputes.
Pakai: python export_dump.py <dump.sql.gz> <folder_keluar>"""
import gzip, re, sys, json, os, collections

BS = chr(92)  # backslash (ditulis lewat chr() supaya tidak ambigu)
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
SKIP = {"users", "audit_logs", "app_settings", "submissions", "disputes"}
cre = re.compile(rb"^CREATE TABLE `([^`]+)`")
ins = re.compile(rb"^INSERT INTO `([^`]+)` VALUES ")
STR = "'(?:[^'" + BS + BS + "]|" + BS + BS + ".|'')*'"
tok = re.compile("(" + STR + ")|(NULL)|(-?[0-9]+(?:[.][0-9]+)?(?:[eE][-+]?[0-9]+)?)|(0x[0-9a-fA-F]+)|([(),;])")
ESC = {"n": "\n", "r": "\r", "t": "\t", "0": "\0", "Z": "\x1a", "b": "\b"}
esc = re.compile(BS + BS + "(.)|''", re.S)


def unq(s):  # s termasuk tanda kutip pembuka/penutup
    s = s[1:-1]
    return esc.sub(lambda m: "'" if m.group(0) == "''" else ESC.get(m.group(1), m.group(1)), s)


def num(s):
    return float(s) if ("." in s or "e" in s or "E" in s) else int(s)


cols = {}
cur = None
counts = collections.Counter()
files = {}


def handle(line):
    m = ins.match(line)
    if not m:
        return
    t = m.group(1).decode()
    if t in SKIP:
        return
    fh = files.get(t)
    if not fh:
        fh = files[t] = open(os.path.join(outdir, t + ".jsonl"), "w", encoding="utf-8", newline="\n")
    c = cols[t]
    row = []
    depth = 0
    for mm in tok.finditer(line.decode("utf-8", "replace"), m.end()):
        s, nl, n, hx, p = mm.groups()
        if p == "(":
            depth = 1
            row = []
        elif p == ")":
            if depth:
                fh.write(json.dumps(dict(zip(c, row)), ensure_ascii=False, separators=(",", ":")) + "\n")
                counts[t] += 1
            depth = 0
        elif p in (",", ";"):
            pass
        elif depth:
            row.append(unq(s) if s is not None else (None if nl else (num(n) if n is not None else hx)))


with gzip.open(src, "rb") as f:
    for line in f:
        m = cre.match(line)
        if m:
            cur = m.group(1).decode()
            cols[cur] = []
            continue
        if cur and line.startswith(b"  `"):
            cols[cur].append(line.decode().split("`")[1])
        elif line.startswith(b") ENGINE"):
            cur = None
        elif line.startswith(b"INSERT INTO"):
            handle(line)

for fh in files.values():
    fh.close()
json.dump({"source": os.path.basename(src), "tables": {t: counts[t] for t in sorted(counts)}, "skipped_personal": sorted(SKIP)},
          open(os.path.join(outdir, "_manifest.json"), "w"), indent=1)
for t in sorted(counts):
    print(f"{t:34} {counts[t]:>9}")
