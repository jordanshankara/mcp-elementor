"""Bangun dist/pusatriset-data.zip dengan separator '/' (kompatibel WordPress) dan verifikasi hasilnya."""
import os
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'pusatriset-data')
OUT = os.path.normpath(os.path.join(ROOT, '..', 'dist', 'pusatriset-data.zip'))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.exists(OUT):
    os.remove(OUT)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for base, dirs, files in os.walk(SRC):
        dirs.sort()
        for f in sorted(files):
            full = os.path.join(base, f)
            arc = 'pusatriset-data/' + os.path.relpath(full, SRC).replace(os.sep, '/')
            z.write(full, arc)

with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    names = z.namelist()
    assert not any(chr(92) in n for n in names)
    assert 'pusatriset-data/pusatriset-data.php' in names
    print('OK', len(names), 'berkas,', os.path.getsize(OUT), 'byte')
