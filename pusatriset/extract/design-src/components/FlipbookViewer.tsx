"use client";

import { forwardRef, useCallback, useEffect, useRef, useState } from "react";
import HTMLFlipBook from "react-pageflip";
import * as pdfjsLib from "pdfjs-dist";
import type { PDFDocumentProxy, PDFPageProxy } from "pdfjs-dist";
import { SimplePdfViewer } from "./SimplePdfViewer";

/// BUILD_PLAN_FINAL §2.7.c — worker DISALIN ke public/ (public/pdfjs/pdf.worker.min.mjs, lihat
/// README §Flipbook), BUKAN dari CDN — supaya tidak gagal kalau CDN tidak bisa diakses. Salinan
/// ini HARUS diperbarui manual kalau versi pdfjs-dist di package.json pernah diubah (versi dikunci
/// tanpa `^` persis karena library ini berubah antar versi minor — jangan bump tanpa sengaja).
pdfjsLib.GlobalWorkerOptions.workerSrc = "/pdfjs/pdf.worker.min.mjs";

const MAX_FLIPBOOK_PAGES = 60; // §2.7.c — "PDF > 60 halaman -> lewati flipbook" (batas memori browser)
const EAGER_PAGES = 4; // §2.7.c — "Lazy render — eager 4 halaman pertama saja"
const RENDER_SCALE = 1.5; // PATCH §4.3 — "Skala render 1.5x ukuran tampilan"

const FlipPage = forwardRef<
  HTMLDivElement,
  { pageNumber: number; pdf: PDFDocumentProxy; shouldRender: boolean; onRendered: (pageNumber: number) => void }
>(function FlipPage({ pageNumber, pdf, shouldRender, onRendered }, ref) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const textLayerRef = useRef<HTMLDivElement>(null);
  const renderedRef = useRef(false);

  useEffect(() => {
    if (!shouldRender || renderedRef.current) return;
    let cancelled = false;
    let page: PDFPageProxy | null = null;
    (async () => {
      try {
        page = await pdf.getPage(pageNumber);
        if (cancelled) return;
        const viewport = page.getViewport({ scale: RENDER_SCALE });
        const canvas = canvasRef.current;
        if (!canvas) return;
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        await page.render({ canvas, viewport }).promise;
        if (cancelled) return;

        // PATCH_Perbaikan_PDF_Viewer_Flipbook.md §2 & §4.1 — lapisan teks transparan di atas
        // canvas, supaya teks tetap bisa diseleksi/dicari meski tampilan visualnya gambar
        // (mengoreksi catatan lama "flipbook kehilangan Ctrl+F" — itu keliru, TextLayer pdf.js
        // yang membuatnya tetap bisa).
        const textLayerDiv = textLayerRef.current;
        if (textLayerDiv) {
          textLayerDiv.style.width = `${viewport.width}px`;
          textLayerDiv.style.height = `${viewport.height}px`;
          textLayerDiv.innerHTML = "";
          const textLayer = new pdfjsLib.TextLayer({
            textContentSource: page.streamTextContent(),
            container: textLayerDiv,
            viewport,
          });
          await textLayer.render();
        }

        if (!cancelled) {
          renderedRef.current = true;
          onRendered(pageNumber);
        }
      } catch (error) {
        // React (StrictMode dev, atau navigasi menjauh) memanggil cleanup di bawah SEBELUM
        // render async ini selesai — page.render()/textLayer.render() yang sedang berjalan
        // otomatis melempar RenderingCancelledException. Itu SENGAJA (bukan kegagalan asli),
        // jangan dicatat sebagai error kalau memang kita sendiri yang membatalkannya.
        if (!cancelled) console.error(`[FlipbookViewer] Gagal me-render halaman ${pageNumber}:`, error);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [shouldRender, pdf, pageNumber, onRendered]);

  return (
    <div ref={ref} className="relative flex h-full w-full items-center justify-center overflow-hidden bg-white">
      {shouldRender ? (
        <div className="relative h-full max-w-full">
          <canvas ref={canvasRef} className="h-full max-w-full" />
          <div ref={textLayerRef} className="textLayer" />
        </div>
      ) : (
        <div className="flex h-full w-full items-center justify-center text-xs text-secondary">Halaman {pageNumber}</div>
      )}
    </div>
  );
});

export function FlipbookViewer({ viewUrl, downloadUrl, title }: { viewUrl: string; downloadUrl: string; title: string }) {
  const [pdf, setPdf] = useState<PDFDocumentProxy | null>(null);
  const [numPages, setNumPages] = useState(0);
  const [renderedPages, setRenderedPages] = useState<Set<number>>(new Set());
  const [loadedCount, setLoadedCount] = useState(0);
  const [fallback, setFallback] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const bookRef = useRef<{ pageFlip(): { flipNext(): void; flipPrev(): void; turnToPage(n: number): void; getCurrentPageIndex(): number } } | null>(null);

  useEffect(() => {
    let cancelled = false;
    // PATCH_Perbaikan_PDF_Viewer_Flipbook.md §4.1-4.2 — pdf.js menarik file lewat URL (BUKAN
    // fetch() penuh ke ArrayBuffer di sini), supaya pdf.js meminta byte-nya secara BERTAHAP lewat
    // HTTP Range request (perilaku bawaan pdf.js utk sumber URL dgn Accept-Ranges: bytes, lihat
    // /api/v1/papers/:id/file). Ini BUKAN sekadar gaya kode — satu fetch() utuh ke endpoint yang
    // berbalas Content-Type: application/pdf + Content-Length besar adalah bentuk request yang
    // paling sering disergap download manager (mis. Internet Download Manager): disergap berarti
    // halaman menerima respons kosong dari request PERTAMA ke URL, viewer gagal, jatuh ke
    // fallback yang juga ikut gagal — persis gejala "PDF malah ke-download". Request berbentuk
    // Range (potongan demi potongan) terbukti TIDAK disergap pada mesin yang sama, PDF yang sama.
    const loadingTask = pdfjsLib.getDocument({ url: viewUrl, withCredentials: true });
    loadingTask.onProgress = ({ loaded, total }: { loaded: number; total: number }) => {
      if (total > 0) setProgress(Math.round((loaded / total) * 100));
    };
    loadingTask.promise
      .then((doc) => {
        if (cancelled) return;
        // §2.7.c — "PDF > 60 halaman -> lewati flipbook", jatuh balik ke viewer (b), BUKAN error.
        if (doc.numPages > MAX_FLIPBOOK_PAGES) {
          setFallback(true);
          return;
        }
        setPdf(doc);
        setNumPages(doc.numPages);
        const eager = new Set<number>();
        for (let i = 1; i <= Math.min(EAGER_PAGES, doc.numPages); i++) eager.add(i);
        setRenderedPages(eager);
      })
      .catch((error) => {
        // loadingTask.destroy() (efek cleanup di bawah — StrictMode dev atau viewUrl berganti)
        // MEMANG melempar "Loading aborted" (pdf.js AbortException) — itu sengaja kita sendiri
        // yang batalkan, bukan kegagalan asli. Jangan dicatat sebagai error kalau `cancelled`
        // sudah true saat catch ini jalan; kegagalan SUNGGUHAN (viewUrl memang gagal dimuat)
        // tetap wajib dicatat (§9 patch, tabel troubleshooting) — sebelumnya kegagalan itu tidak
        // tercatat SAMA SEKALI, membuat bug ini sulit dilacak pertama kali.
        if (cancelled) return;
        console.error("[FlipbookViewer] Gagal memuat PDF:", error);
        setFallback(true);
      });
    return () => {
      cancelled = true;
      loadingTask.destroy();
    };
  }, [viewUrl]);

  const handleRendered = useCallback(() => {
    setLoadedCount((c) => c + 1);
  }, []);

  const expandWindow = useCallback(
    (centerZeroIndexed: number) => {
      setRenderedPages((prev) => {
        const next = new Set(prev);
        for (const p of [centerZeroIndexed, centerZeroIndexed + 1, centerZeroIndexed + 2]) {
          if (p >= 1 && p <= numPages) next.add(p);
        }
        return next;
      });
    },
    [numPages]
  );

  const handleFlip = useCallback(
    (e: { data: number }) => {
      // §2.7.c lazy render — muat halaman di sekitar posisi baca saat pengguna membalik.
      // e.data dari react-pageflip 0-indexed; tampilan nomor halaman ke pengguna 1-indexed.
      setCurrentPage(e.data + 1);
      expandWindow(e.data);
    },
    [expandWindow]
  );

  const goPrev = useCallback(() => bookRef.current?.pageFlip().flipPrev(), []);
  const goNext = useCallback(() => bookRef.current?.pageFlip().flipNext(), []);

  // PATCH_Perbaikan_PDF_Viewer_Flipbook.md §6 — "Tombol navigasi kiri/kanan, plus dukungan
  // tombol panah keyboard".
  useEffect(() => {
    if (fallback || !pdf) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "ArrowLeft") goPrev();
      else if (e.key === "ArrowRight") goNext();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [fallback, pdf, goPrev, goNext]);

  if (fallback) return <SimplePdfViewer viewUrl={viewUrl} downloadUrl={downloadUrl} title={title} />;

  const eagerTarget = Math.min(EAGER_PAGES, numPages || EAGER_PAGES);
  const ready = pdf !== null && loadedCount >= eagerTarget;

  // §2.7.c catatan implementasi: HTMLFlipBook & FlipPage HARUS tetap ter-mount selama memuat —
  // FlipPage-lah yang men-trigger onRendered() lewat efeknya sendiri, jadi menyembunyikannya
  // total (unmount) sampai "ready" justru membuat ready TIDAK PERNAH tercapai (deadlock). Solusi:
  // selalu render flipbook begitu `pdf` ada, overlay indikator "Memuat halaman X dari Y" DI ATASNYA
  // (bukan menggantikannya) selama halaman eager belum selesai.
  if (!pdf) {
    return (
      <div className="flex h-[80vh] w-full flex-col items-center justify-center gap-2 rounded-[14px] border border-warm bg-card-alt">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-brand-700 border-t-transparent" />
        {/* PATCH §6 — "Memuat jurnal… 45%", indikator progres jelas, bukan layar kosong. */}
        <p className="text-sm text-secondary">Memuat jurnal{progress !== null ? `… ${progress}%` : "…"}</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="relative flex justify-center overflow-x-auto rounded-[14px] border border-warm bg-card-alt p-4">
        {!ready ? (
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-2 rounded-[14px] bg-card-alt/90">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-brand-700 border-t-transparent" />
            <p className="text-sm text-secondary">
              Memuat halaman {Math.min(loadedCount + 1, eagerTarget)} dari {numPages}
            </p>
          </div>
        ) : null}
        <HTMLFlipBook
          ref={bookRef}
          width={420}
          height={594}
          size="stretch"
          minWidth={280}
          maxWidth={600}
          minHeight={400}
          maxHeight={850}
          startPage={0}
          drawShadow={true}
          flippingTime={600}
          usePortrait={true}
          startZIndex={0}
          autoSize={true}
          maxShadowOpacity={0.5}
          showCover={false}
          mobileScrollSupport={true}
          swipeDistance={30}
          clickEventForward={true}
          useMouseEvents={true}
          showPageCorners={true}
          disableFlipByClick={false}
          onFlip={handleFlip}
          className="flipbook"
          style={{}}
        >
          {Array.from({ length: numPages }, (_, i) => i + 1).map((pageNumber) => (
            <FlipPage
              key={pageNumber}
              pageNumber={pageNumber}
              pdf={pdf}
              shouldRender={renderedPages.has(pageNumber)}
              onRendered={handleRendered}
            />
          ))}
        </HTMLFlipBook>
      </div>
      {/* PATCH §6 — nomor halaman terlihat ("3 / 76"), tombol navigasi kiri/kanan. */}
      <div className="flex items-center justify-center gap-4">
        <button
          type="button"
          onClick={goPrev}
          disabled={currentPage <= 1}
          className="rounded-md border border-warm px-3 py-1 text-sm text-primary hover:bg-card-alt disabled:opacity-40"
          aria-label="Halaman sebelumnya"
        >
          ←
        </button>
        <span className="text-sm text-secondary tabular-nums">
          {currentPage} / {numPages}
        </span>
        <button
          type="button"
          onClick={goNext}
          disabled={currentPage >= numPages}
          className="rounded-md border border-warm px-3 py-1 text-sm text-primary hover:bg-card-alt disabled:opacity-40"
          aria-label="Halaman berikutnya"
        >
          →
        </button>
      </div>
      <p className="text-center text-xs text-muted-warm">Mode buku — teks tetap bisa diseleksi/dicari (Ctrl+F).</p>
    </div>
  );
}
