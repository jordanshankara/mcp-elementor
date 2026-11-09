/// Nama lembaga sendiri untuk publikasi §2.5 — file terpisah TANPA import Prisma (zero
/// dependency) supaya aman diimpor komponen client (PublicationForm.tsx) maupun server
/// (src/lib/services/own-institution.ts) tanpa membawa serta Prisma Client ke bundle browser.
export const OWN_INSTITUTION_NAME = "Pusat Riset AI Indonesia";
