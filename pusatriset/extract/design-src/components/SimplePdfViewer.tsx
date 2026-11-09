"use client";

/// BUILD_PLAN_FINAL §2.7.b, diperbarui PATCH_Perbaikan_PDF_Viewer_Flipbook.md §4.4 — viewer
/// sederhana lewat <object>, PDF viewer bawaan browser (nol dependensi, Ctrl+F & zoom jalan).
/// Dipakai sebagai viewer utama di layar sempit (§2.7.c: "Lebar < 768px -> JANGAN flipbook") DAN
/// sebagai fallback FlipbookViewer kalau PDF > 60 halaman atau gagal dimuat.
///
/// <object data={viewUrl}>, BUKAN <iframe> ATAU blob: URL hasil fetch() manual (versi sebelumnya
/// di file ini) — dua pendekatan itu SAMA-SAMA gagal karena fetch() penuh ke endpoint PDF adalah
/// bentuk request yang paling sering disergap download manager (mis. Internet Download Manager):
/// disergap berarti fetch() menerima respons kosong dari page, blob yang dibuat 0 byte, iframe
/// jadi kosong. <object> membiarkan BROWSER sendiri (bukan JS halaman) yang menangani pemuatan
/// resource-nya lewat mekanisme render PDF native (Range request bertahap, sama seperti pdf.js
/// di FlipbookViewer) — endpoint /file sudah inline + Accept-Ranges: bytes, jadi <object> ini
/// pun tidak akan memicu unduhan. Dukungan PDF <object> lebih konsisten antar browser dibanding
/// <iframe> (patch §4.4).
export function SimplePdfViewer({ viewUrl, downloadUrl, title }: { viewUrl: string; downloadUrl: string; title: string }) {
  return (
    <object
      data={viewUrl}
      type="application/pdf"
      title={`Pratinjau PDF — ${title}`}
      className="h-[80vh] w-full rounded-[14px] border border-warm bg-card-alt"
    >
      {/* §4.4 — "browser tidak mendukung -> Pesan 'Pratinjau tidak tersedia' + tombol unduh" */}
      <div className="flex h-full w-full flex-col items-center justify-center gap-3 p-6 text-center">
        <p className="text-sm text-secondary">Pratinjau tidak tersedia di browser ini.</p>
        <a href={downloadUrl} className="rounded-md bg-brand-700 px-4 py-2 text-sm font-medium text-white hover:bg-brand-900">
          Unduh PDF
        </a>
      </div>
    </object>
  );
}
