"""Analisis dump mysqldump (gz) secara streaming: daftar tabel, jumlah baris perkiraan, ukuran data per tabel."""
import gzip, re, sys, json, collections
src = sys.argv[1]
rows = collections.Counter(); size = collections.Counter(); creates = {}
cur = None
ins = re.compile(rb"^INSERT INTO `([^`]+)` VALUES ")
cre = re.compile(rb"^CREATE TABLE `([^`]+)`")
with gzip.open(src, "rb") as f:
    for line in f:
        m = ins.match(line)
        if m:
            t = m.group(1).decode()
            size[t] += len(line)
            rows[t] += line.count(b"),(") + 1
            continue
        m = cre.match(line)
        if m: cur = m.group(1).decode(); creates[cur] = []
        elif cur and line.startswith(b"  `"):
            creates[cur].append(line.split(b"`")[1].decode())
        elif line.startswith(b") ENGINE"): cur = None
out = {t: {"rows_approx": rows[t], "mb": round(size[t] / 1048576, 1), "cols": creates.get(t, [])} for t in sorted(creates)}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
for t, v in sorted(out.items(), key=lambda kv: -kv[1]["mb"]): print(f'{t:34} {v["rows_approx"]:>9} baris {v["mb"]:>8} MB')
