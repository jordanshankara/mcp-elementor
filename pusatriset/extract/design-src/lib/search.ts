/**
 * BUILD_PLAN_FINAL §1 — pencarian 4 lapis, dari paling tepat ke paling longgar. Dipanggil dari
 * `listPapers()` di src/lib/services/papers.ts (satu-satunya entry point publik, dipakai
 * Server Component halaman DAN /api/v1/papers) — modul ini murni logika internal pencarian,
 * TIDAK dipanggil langsung dari route/halaman.
 *
 * Lapis 1 (perluasan istilah) & 4 (LIKE) hanya menyaring `metadata_status='indexed'` — filter
 * publik LAIN (origin, tahun, subbidang, dst) diterapkan belakangan oleh listPapers() lewat
 * Prisma biasa (andConditions), BUKAN diduplikasi di sini. Ini sengaja: menulis ulang filter
 * relasi (topics.some, policyTags.some, dll) di raw SQL berisiko drift dari sumber kebenarannya
 * (lihat catatan serupa soal computeFacets/getTrends di papers.ts).
 */
import { prisma } from "@/lib/db";

const INDONESIAN_STOPWORDS = new Set([
  "yang", "dan", "di", "ke", "dari", "untuk", "pada", "dengan", "atau", "ini", "itu", "adalah", "dalam", "oleh", "sebagai", "akan", "dapat",
]);

const MAX_QUERY_LENGTH = 200; // §1.5 poin 4
const CANDIDATE_LIMIT = 2000; // batas ambil kandidat per lapis — cukup besar utk 35k+ paper, cegah worst-case query tak terbatas
const SUFFICIENT_RESULTS = 10; // §1.2 — "kalau lapis sebelumnya sudah memberi hasil cukup (>=10), berhenti"
const MIN_TOKEN_LEN_FULLTEXT = 3; // innodb_ft_min_token_size (bawaan MySQL/MariaDB) — kata <3 huruf tidak terindeks FULLTEXT
const MIN_SUGGESTION_WORD_LENGTH = 4; // §1.6
const MAX_LEVENSHTEIN_DISTANCE = 2; // §1.6

export interface SearchResult {
  /** id paper terurut berdasar skor relevansi, sebelum filter publik lain (origin/tahun/dst) diterapkan pemanggil. */
  ids: string[];
  queryNormalized: string;
  /** istilah hasil perluasan lapis 1 yang benar-benar terpakai (kosong = lapis 1 tidak aktif utk kueri ini). */
  matchedSynonyms: string[];
  /** lapis mana yang hasilnya dipakai. 0 = kueri kosong setelah normalisasi (tidak ada pencarian dijalankan). */
  layerUsed: 0 | 2 | 3 | 4;
  /** "Mungkin maksud Anda: '...'" — diisi hanya kalau hasil < 3. */
  suggestion: string | null;
}

/** §1.5 — normalisasi kueri di lapisan aplikasi. */
export function normalizeSearchQuery(raw: string): string {
  let q = raw.toLowerCase();
  q = q.replace(/[^\p{L}\p{N}\s]/gu, " "); // buang tanda baca berlebih
  q = q.replace(/\s+/g, " ").trim(); // rapikan spasi ganda
  if (q.length > MAX_QUERY_LENGTH) q = q.slice(0, MAX_QUERY_LENGTH).trim();
  const words = q.split(" ").filter((w) => w.length > 0 && !INDONESIAN_STOPWORDS.has(w));
  return words.join(" ");
}

interface CandidateRow {
  id: string;
  score: number;
}

/** Lapis 1 — perluasan istilah lewat tabel search_synonyms (dikelola admin, §3.2 synonym.manage — belum diimplementasikan di Fitur 1). */
async function expandSynonyms(normalizedQuery: string): Promise<{ expandedQuery: string; matched: string[] }> {
  if (!normalizedQuery) return { expandedQuery: "", matched: [] };
  const synonyms = await prisma.searchSynonym.findMany({ where: { active: true }, select: { term: true, expandsTo: true } });

  const matched: string[] = [];
  for (const syn of synonyms) {
    if (normalizedQuery.includes(syn.term.toLowerCase())) {
      matched.push(...syn.expandsTo.split(",").map((s) => s.trim()).filter(Boolean));
    }
  }
  const uniqueMatched = Array.from(new Set(matched));
  const expandedQuery = uniqueMatched.length > 0 ? `${normalizedQuery} ${uniqueMatched.join(" ")}` : normalizedQuery;
  return { expandedQuery, matched: uniqueMatched };
}

/** Lapis 2 — FULLTEXT natural language mode (§1.3). Parameter terikat lewat tagged template $queryRaw, TIDAK pernah sambung string. */
async function fulltextNatural(query: string): Promise<CandidateRow[]> {
  if (!query) return [];
  return prisma.$queryRaw<CandidateRow[]>`
    SELECT id, MATCH(title, abstract_raw) AGAINST(${query} IN NATURAL LANGUAGE MODE) AS score
    FROM papers
    WHERE metadata_status = 'indexed'
      AND MATCH(title, abstract_raw) AGAINST(${query} IN NATURAL LANGUAGE MODE)
    ORDER BY score DESC
    LIMIT ${CANDIDATE_LIMIT}
  `;
}

/** Buang karakter operator BOOLEAN MODE (+-<>()~*"@) dari satu kata — pertahanan berlapis; normalizeSearchQuery() sudah membuang tanda baca lebih dulu. */
function sanitizeBooleanTerm(word: string): string {
  return word.replace(/[+\-<>()~*"@]/g, "");
}

/** Lapis 3 — FULLTEXT boolean mode + wildcard (§1.3), menangkap kata berimbuhan/sebagian. */
async function fulltextBoolean(words: string[]): Promise<CandidateRow[]> {
  const eligible = words.map(sanitizeBooleanTerm).filter((w) => w.length >= MIN_TOKEN_LEN_FULLTEXT);
  if (eligible.length === 0) return [];
  const booleanQuery = eligible.map((w) => `${w}*`).join(" ");
  return prisma.$queryRaw<CandidateRow[]>`
    SELECT id, MATCH(title, abstract_raw) AGAINST(${booleanQuery} IN BOOLEAN MODE) AS score
    FROM papers
    WHERE metadata_status = 'indexed'
      AND MATCH(title, abstract_raw) AGAINST(${booleanQuery} IN BOOLEAN MODE)
    ORDER BY score DESC
    LIMIT ${CANDIDATE_LIMIT}
  `;
}

/** Lapis 4 — LIKE fallback per kata (§1.2 poin 4), menangkap kata pendek (<3 huruf, mis. "AI") yang tidak terindeks FULLTEXT. Lewat Prisma biasa, bukan raw SQL (aman, tidak perlu $queryRaw). */
async function likeFallback(words: string[]): Promise<CandidateRow[]> {
  if (words.length === 0) return [];
  const rows = await prisma.paper.findMany({
    where: {
      metadataStatus: "indexed",
      OR: words.flatMap((w) => [{ title: { contains: w } }, { abstractRaw: { contains: w } }]),
    },
    select: { id: true, title: true, abstractRaw: true },
    take: CANDIDATE_LIMIT,
  });
  return rows
    .map((r) => {
      const titleLower = r.title.toLowerCase();
      const abstractLower = (r.abstractRaw ?? "").toLowerCase();
      let score = 0;
      for (const w of words) {
        if (titleLower.includes(w)) score += 3;
        else if (abstractLower.includes(w)) score += 1;
      }
      return { id: r.id, score };
    })
    .filter((r) => r.score > 0);
}

/** Jarak edit klasik (DP) — dipakai §1.6 "Mungkin maksud Anda?", tidak ada fungsi bawaan MySQL untuk ini. */
function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
    }
  }
  return dp[m][n];
}

/** §1.6 — "Mungkin maksud Anda?" dihitung di lapisan aplikasi, bukan SQL. */
async function buildSuggestion(originalWords: string[]): Promise<string | null> {
  const eligible = originalWords.filter((w) => w.length >= MIN_SUGGESTION_WORD_LENGTH);
  if (eligible.length === 0) return null;

  // Kamus (search_terms, dibangun scripts/build-search-dictionary.ts) diambil sekali, bukan
  // per-kata — jumlahnya (~ribuan) cukup kecil untuk dimuat penuh & dihitung jaraknya di JS
  // per pencarian, tanpa fungsi jarak-kata bawaan MySQL.
  const dictionary = await prisma.searchTerm.findMany({
    where: { frequency: { gte: 3 } },
    orderBy: { frequency: "desc" },
    select: { term: true, frequency: true },
  });

  for (const word of eligible) {
    let best: { term: string; frequency: number; distance: number } | null = null;
    for (const candidate of dictionary) {
      if (candidate.term === word) continue;
      if (Math.abs(candidate.term.length - word.length) > MAX_LEVENSHTEIN_DISTANCE) continue; // batas matematis jarak edit
      const distance = levenshtein(word, candidate.term);
      if (distance > 0 && distance <= MAX_LEVENSHTEIN_DISTANCE) {
        if (!best || distance < best.distance || (distance === best.distance && candidate.frequency > best.frequency)) {
          best = { term: candidate.term, frequency: candidate.frequency, distance };
        }
      }
    }
    if (best) return best.term;
  }
  return null;
}

/** 3 kata kunci populer utk halaman nol-hasil (§1.7). */
export async function getPopularSearchTerms(limit = 3): Promise<string[]> {
  const rows = await prisma.searchTerm.findMany({ orderBy: { frequency: "desc" }, take: limit, select: { term: true } });
  return rows.map((r) => r.term);
}

/**
 * Orkestrasi 4 lapis (§1.2): jalankan berurutan, berhenti begitu satu lapis memberi hasil
 * cukup (>=10). Lapis 3/4 dicoba HANYA kalau lapis sebelumnya belum cukup, dan hasilnya
 * dipakai kalau memberi kandidat (>0) — karena tiap lapis berikutnya dirancang lebih longgar
 * dari sebelumnya (wildcard/berimbuhan lalu LIKE per-substring), jadi diasumsikan superset yang
 * lebih relevan begitu lapis lebih ketat gagal mencukupi, bukan cuma "lebih banyak angka".
 */
export async function searchPapers(rawQuery: string): Promise<SearchResult> {
  const normalized = normalizeSearchQuery(rawQuery);
  if (!normalized) {
    return { ids: [], queryNormalized: "", matchedSynonyms: [], layerUsed: 0, suggestion: null };
  }

  const { expandedQuery, matched } = await expandSynonyms(normalized);

  let candidates = await fulltextNatural(expandedQuery);
  let layerUsed: 2 | 3 | 4 = 2;

  if (candidates.length < SUFFICIENT_RESULTS) {
    const words = expandedQuery.split(" ").filter(Boolean);
    const layer3 = await fulltextBoolean(words);
    if (layer3.length > 0) {
      candidates = layer3;
      layerUsed = 3;
    }
  }

  if (candidates.length < SUFFICIENT_RESULTS) {
    const originalWords = normalized.split(" ").filter(Boolean);
    const expansionWords = matched.flatMap((m) => m.toLowerCase().split(/\s+/)).filter(Boolean);
    const words4 = Array.from(new Set([...originalWords, ...expansionWords]));
    const layer4 = await likeFallback(words4);
    if (layer4.length > 0) {
      candidates = layer4;
      layerUsed = 4;
    }
  }

  const ids = [...candidates].sort((a, b) => b.score - a.score).map((c) => c.id);

  let suggestion: string | null = null;
  if (ids.length < 3) {
    suggestion = await buildSuggestion(normalized.split(" ").filter(Boolean));
  }

  return { ids, queryNormalized: normalized, matchedSynonyms: matched, layerUsed, suggestion };
}
