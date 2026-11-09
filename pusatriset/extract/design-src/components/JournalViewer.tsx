"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { SimplePdfViewer } from "./SimplePdfViewer";

/// BUILD_PLAN_FINAL §2.7.c — "Import dinamis next/dynamic + ssr:false" (pdfjs-dist & react-pageflip
/// butuh Canvas/DOM, tidak bisa jalan di server). Bundle flipbook (pdfjs-dist + react-pageflip)
/// HANYA diunduh browser kalau memang dipakai (desktop) — di HP komponen ini tidak pernah diimpor.
const FlipbookViewer = dynamic(() => import("./FlipbookViewer").then((m) => m.FlipbookViewer), {
  ssr: false,
  loading: () => (
    <div className="flex h-[80vh] w-full items-center justify-center rounded-[14px] border border-warm bg-card-alt">
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-brand-700 border-t-transparent" />
    </div>
  ),
});

const MOBILE_BREAKPOINT = 768; // §2.7.c — "Lebar < 768px -> JANGAN flipbook, pakai (b)"

export function JournalViewer({
  paperId,
  title,
  originalName,
  sizeBytes,
  downloadCount,
}: {
  paperId: string;
  title: string;
  originalName: string;
  sizeBytes: number;
  downloadCount: number;
}) {
  const [isMobile, setIsMobile] = useState<boolean | null>(null);
  // PATCH_Perbaikan_PDF_Viewer_Flipbook.md §3.3 — "Aturan mutlak: Flipbook/viewer -> /file,
  // tombol 'Unduh PDF' -> /download. Jangan pernah tertukar." Dua endpoint, dua peran, tidak
  // ada lagi ?view=1 di /download (lihat src/app/api/v1/papers/[id]/download/route.ts).
  const viewUrl = `/api/v1/papers/${paperId}/file`;
  const downloadUrl = `/api/v1/papers/${paperId}/download`;

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  return (
    <div className="mt-6 space-y-3">
      <div className="flex items-center justify-between">
        <p className="text-sm text-secondary">
          {originalName} · {(sizeBytes / 1024 / 1024).toFixed(1)}MB · {downloadCount} unduhan
        </p>
        {/* §2.7.c — "Tombol unduh tetap terlihat", dirender di sini SEKALI, di luar cabang
            mobile/flipbook manapun, supaya selalu ada apa pun status pemuatan flipbook. */}
        <a href={downloadUrl} className="rounded-md bg-brand-700 px-4 py-2 text-sm font-medium text-white hover:bg-brand-900">
          Unduh PDF
        </a>
      </div>

      {isMobile === null ? (
        <div className="h-[80vh] w-full animate-pulse rounded-[14px] border border-warm bg-card-alt" />
      ) : isMobile ? (
        <SimplePdfViewer viewUrl={viewUrl} downloadUrl={downloadUrl} title={title} />
      ) : (
        <FlipbookViewer viewUrl={viewUrl} downloadUrl={downloadUrl} title={title} />
      )}
    </div>
  );
}
