/// BUILD_PLAN_FINAL §2.6 — badge "Publikasi PusatRiset.ai", tampil di kartu katalog & halaman
/// detail. Konsisten pola dengan OriginFlag/QuartileBadge — komponen kecil, satu tanggung jawab.
export function PublicationBadge({ publicationType }: { publicationType: "indexed" | "own_publication" }) {
  if (publicationType !== "own_publication") return null;
  return (
    <span className="inline-flex items-center rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700" title="Publikasi PusatRiset.ai">
      Publikasi PusatRiset.ai
    </span>
  );
}
