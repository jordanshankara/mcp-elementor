<?php
/**
 * Lapisan data publik: port dari src/lib/services/papers.ts + search.ts (aplikasi lama) ke SQL langsung.
 * Aturan keras: publik HANYA melihat metadata_status='indexed'; abstrak hanya jika abstract_display_policy='full'.
 */
if (!defined('ABSPATH')) exit;

const PR_STOPWORDS = ['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 'atau', 'ini', 'itu', 'adalah', 'dalam', 'oleh', 'sebagai', 'akan', 'dapat'];
const PR_CANDIDATE_LIMIT = 2000;
const PR_SUFFICIENT = 10;

// ---------------------------------------------------------------- util
function pr_in_list(array $vals, &$args) {
    foreach ($vals as $v) $args[] = $v;
    return implode(',', array_fill(0, count($vals), '%s'));
}

function pr_cached($key, $ttl, callable $fn) {
    $v = get_transient($key);
    if ($v !== false) return $v;
    $v = $fn();
    set_transient($key, $v, $ttl);
    return $v;
}

/** Hapus cache agregat (dipanggil setelah impor/ubah data). */
function pr_flush_cache() {
    foreach (['pr_c_topics', 'pr_c_trends', 'pr_c_home'] as $k) delete_transient($k);
}

// ---------------------------------------------------------------- pencarian (search.ts)
function pr_normalize_query($raw) {
    $q = mb_strtolower((string) $raw, 'UTF-8');
    $q = preg_replace('/[^\p{L}\p{N}\s]/u', ' ', $q);
    $q = trim(preg_replace('/\s+/u', ' ', $q));
    if (mb_strlen($q, 'UTF-8') > 200) $q = trim(mb_substr($q, 0, 200, 'UTF-8'));
    $words = array_filter(explode(' ', $q), function ($w) { return $w !== '' && !in_array($w, PR_STOPWORDS, true); });
    return implode(' ', $words);
}

function pr_expand_synonyms($normalized) {
    global $wpdb;
    if ($normalized === '') return ['', []];
    $rows = $wpdb->get_results("SELECT term, expands_to FROM " . pr_t('search_synonyms') . " WHERE active = 1", ARRAY_A);
    $matched = [];
    foreach ($rows as $r) {
        if (mb_strpos($normalized, mb_strtolower($r['term'], 'UTF-8')) !== false) {
            foreach (explode(',', $r['expands_to']) as $s) { $s = trim($s); if ($s !== '') $matched[] = $s; }
        }
    }
    $matched = array_values(array_unique($matched));
    return [$matched ? $normalized . ' ' . implode(' ', $matched) : $normalized, $matched];
}

function pr_ft_candidates($query, $boolean) {
    global $wpdb;
    if ($query === '' || !pr_has_fulltext()) return [];
    $p = pr_t('papers');
    $mode = $boolean ? 'IN BOOLEAN MODE' : 'IN NATURAL LANGUAGE MODE';
    $sql = $wpdb->prepare(
        "SELECT id, MATCH(title, abstract_raw) AGAINST (%s $mode) AS score FROM $p WHERE metadata_status = 'indexed' AND MATCH(title, abstract_raw) AGAINST (%s $mode) ORDER BY score DESC LIMIT %d",
        $query, $query, PR_CANDIDATE_LIMIT
    );
    $rows = $wpdb->get_results($sql, ARRAY_A);
    return $rows ?: [];
}

function pr_like_candidates(array $words) {
    global $wpdb;
    if (!$words) return [];
    $p = pr_t('papers');
    $conds = []; $args = [];
    foreach ($words as $w) {
        $like = '%' . $wpdb->esc_like($w) . '%';
        $conds[] = '(title LIKE %s OR abstract_raw LIKE %s)';
        $args[] = $like; $args[] = $like;
    }
    $args[] = PR_CANDIDATE_LIMIT;
    $rows = $wpdb->get_results($wpdb->prepare("SELECT id, title, abstract_raw FROM $p WHERE metadata_status = 'indexed' AND (" . implode(' OR ', $conds) . ") LIMIT %d", $args), ARRAY_A);
    $out = [];
    foreach ($rows as $r) {
        $tl = mb_strtolower($r['title'], 'UTF-8'); $al = mb_strtolower((string) $r['abstract_raw'], 'UTF-8'); $score = 0;
        foreach ($words as $w) { if (mb_strpos($tl, $w) !== false) $score += 3; elseif (mb_strpos($al, $w) !== false) $score += 1; }
        if ($score > 0) $out[] = ['id' => $r['id'], 'score' => $score];
    }
    return $out;
}

function pr_levenshtein($a, $b) {
    $a = preg_split('//u', $a, -1, PREG_SPLIT_NO_EMPTY); $b = preg_split('//u', $b, -1, PREG_SPLIT_NO_EMPTY);
    $m = count($a); $n = count($b);
    if ($m === 0) return $n; if ($n === 0) return $m;
    $prev = range(0, $n);
    for ($i = 1; $i <= $m; $i++) {
        $cur = [$i];
        for ($j = 1; $j <= $n; $j++) {
            $cost = $a[$i - 1] === $b[$j - 1] ? 0 : 1;
            $cur[$j] = min($prev[$j] + 1, $cur[$j - 1] + 1, $prev[$j - 1] + $cost);
        }
        $prev = $cur;
    }
    return $prev[$n];
}

function pr_suggestion(array $originalWords) {
    global $wpdb;
    $eligible = array_values(array_filter($originalWords, function ($w) { return mb_strlen($w, 'UTF-8') >= 4; }));
    if (!$eligible) return null;
    $dict = $wpdb->get_results("SELECT term, frequency FROM " . pr_t('search_terms') . " WHERE frequency >= 3 ORDER BY frequency DESC", ARRAY_A);
    foreach ($eligible as $word) {
        $best = null; $wl = mb_strlen($word, 'UTF-8');
        foreach ($dict as $c) {
            if ($c['term'] === $word) continue;
            if (abs(mb_strlen($c['term'], 'UTF-8') - $wl) > 2) continue;
            $d = pr_levenshtein($word, $c['term']);
            if ($d > 0 && $d <= 2 && (!$best || $d < $best['d'] || ($d === $best['d'] && (int) $c['frequency'] > $best['f']))) {
                $best = ['t' => $c['term'], 'f' => (int) $c['frequency'], 'd' => $d];
            }
        }
        if ($best) return $best['t'];
    }
    return null;
}

function pr_popular_terms($limit = 3) {
    global $wpdb;
    return $wpdb->get_col($wpdb->prepare("SELECT term FROM " . pr_t('search_terms') . " ORDER BY frequency DESC LIMIT %d", $limit));
}

/** Orkestrasi 4 lapis: sinonim -> FULLTEXT natural -> FULLTEXT boolean+wildcard -> LIKE per kata. */
function pr_search_papers($raw) {
    $normalized = pr_normalize_query($raw);
    if ($normalized === '') return ['ids' => [], 'queryNormalized' => '', 'matchedSynonyms' => [], 'layerUsed' => 0, 'suggestion' => null];

    list($expanded, $matched) = pr_expand_synonyms($normalized);
    $cands = pr_ft_candidates($expanded, false);
    $layer = 2;

    if (count($cands) < PR_SUFFICIENT) {
        $eligible = [];
        foreach (array_filter(explode(' ', $expanded)) as $w) {
            $w = preg_replace('/[+\-<>()~*"@]/', '', $w);
            if (mb_strlen($w, 'UTF-8') >= 3) $eligible[] = $w;
        }
        if ($eligible) {
            $bq = implode(' ', array_map(function ($w) { return $w . '*'; }, $eligible));
            $l3 = pr_ft_candidates($bq, true);
            if ($l3) { $cands = $l3; $layer = 3; }
        }
    }
    if (count($cands) < PR_SUFFICIENT) {
        $words = array_filter(explode(' ', $normalized));
        foreach ($matched as $m) foreach (preg_split('/\s+/u', mb_strtolower($m, 'UTF-8')) as $w) if ($w !== '') $words[] = $w;
        $l4 = pr_like_candidates(array_values(array_unique($words)));
        if ($l4) { $cands = $l4; $layer = 4; }
    }
    usort($cands, function ($a, $b) { return $b['score'] <=> $a['score']; });
    $ids = array_map(function ($c) { return $c['id']; }, $cands);
    $suggestion = count($ids) < 3 ? pr_suggestion(array_values(array_filter(explode(' ', $normalized)))) : null;
    return ['ids' => $ids, 'queryNormalized' => $normalized, 'matchedSynonyms' => $matched, 'layerUsed' => $layer, 'suggestion' => $suggestion];
}

// ---------------------------------------------------------------- daftar (listPapers)
function pr_empty_search_meta() {
    return ['queryOriginal' => null, 'queryNormalized' => null, 'matchedSynonyms' => [], 'layerUsed' => 0, 'suggestion' => null, 'popularSuggestions' => []];
}

/** @param array $a q, origin, yearFrom, yearTo, subfield[], tier, quartile, openAccess, country, policyTag, relevance, hideSuperseded, publicationType, page, perPage */
function pr_list_papers(array $a) {
    global $wpdb;
    $P = pr_t('papers'); $R = pr_t('relevance_scores');
    $page = max(1, (int) ($a['page'] ?? 1)); $per = max(1, (int) ($a['perPage'] ?? 20));
    $where = ["p.metadata_status = 'indexed'"]; $args = [];

    if (!empty($a['origin'])) { $where[] = 'p.origin = %s'; $args[] = $a['origin']; }
    if (!empty($a['yearFrom'])) { $where[] = 'p.published_date >= %s'; $args[] = sprintf('%04d-01-01', (int) $a['yearFrom']); }
    if (!empty($a['yearTo'])) { $where[] = 'p.published_date <= %s'; $args[] = sprintf('%04d-12-31', (int) $a['yearTo']); }
    if (!empty($a['subfield'])) {
        $subs = (array) $a['subfield'];
        if ($subs) $where[] = 'EXISTS (SELECT 1 FROM ' . pr_t('paper_topics') . ' t WHERE t.paper_id = p.id AND t.subfield IN (' . pr_in_list($subs, $args) . '))';
    }
    if (!empty($a['tier'])) { $where[] = 'p.source_tier = %s'; $args[] = $a['tier']; }
    if (!empty($a['quartile'])) { $where[] = 'p.sjr_quartile = %s'; $args[] = $a['quartile']; }
    if (!empty($a['openAccess'])) $where[] = "p.abstract_display_policy = 'full'";
    if (!empty($a['country'])) { $where[] = 'EXISTS (SELECT 1 FROM ' . pr_t('paper_affiliation_countries') . ' c WHERE c.paper_id = p.id AND c.country_code = %s)'; $args[] = $a['country']; }
    if (!empty($a['policyTag'])) {
        $where[] = 'EXISTS (SELECT 1 FROM ' . pr_t('paper_policy_tags') . ' pt JOIN ' . pr_t('policy_tags') . " g ON g.id = pt.tag_id WHERE pt.paper_id = p.id AND pt.status = 'published' AND g.slug = %s)";
        $args[] = $a['policyTag'];
    }
    if (!empty($a['relevance'])) {
        if ($a['relevance'] === 'none') $where[] = 'r.published_status IS NULL';
        else { $where[] = 'r.published_status = %s'; $args[] = $a['relevance']; }
    }
    if (!empty($a['hideSuperseded'])) $where[] = "(r.published_status IS NULL OR r.published_status <> 'superseded')";
    if (!empty($a['publicationType'])) { $where[] = 'p.publication_type = %s'; $args[] = $a['publicationType']; }

    $from = "$P p LEFT JOIN $R r ON r.paper_id = p.id";
    $searchMeta = pr_empty_search_meta();
    $order = null; $total = 0; $pageIds = [];

    if (!empty($a['q'])) {
        $res = pr_search_papers($a['q']);
        $searchMeta = ['queryOriginal' => $a['q'], 'queryNormalized' => $res['queryNormalized'], 'matchedSynonyms' => $res['matchedSynonyms'], 'layerUsed' => $res['layerUsed'], 'suggestion' => $res['suggestion'], 'popularSuggestions' => []];
        if (!$res['ids']) { $searchMeta['popularSuggestions'] = pr_popular_terms(3); return pr_empty_result($page, $per, $searchMeta); }
        $a2 = $args; $in = pr_in_list($res['ids'], $a2);
        $sql = "SELECT p.id FROM $from WHERE " . implode(' AND ', $where) . " AND p.id IN ($in)";
        $keep = array_flip($wpdb->get_col($wpdb->prepare($sql, $a2)));
        $order = array_values(array_filter($res['ids'], function ($id) use ($keep) { return isset($keep[$id]); }));
        if (!$order) { $searchMeta['popularSuggestions'] = pr_popular_terms(3); return pr_empty_result($page, $per, $searchMeta); }
        $total = count($order);
        $pageIds = array_slice($order, ($page - 1) * $per, $per);
    } else {
        $sqlW = implode(' AND ', $where);
        $q = "SELECT COUNT(*) FROM $from WHERE $sqlW";
        $total = (int) ($args ? $wpdb->get_var($wpdb->prepare($q, $args)) : $wpdb->get_var($q));
        $a2 = $args; $a2[] = $per; $a2[] = ($page - 1) * $per;
        $pageIds = $wpdb->get_col($wpdb->prepare("SELECT p.id FROM $from WHERE $sqlW ORDER BY p.published_date DESC, p.created_at DESC, p.id ASC LIMIT %d OFFSET %d", $a2));
    }
    return ['data' => pr_card_items($pageIds), 'total' => $total, 'page' => $page, 'perPage' => $per, 'search' => $searchMeta];
}

function pr_empty_result($page, $per, $meta) {
    return ['data' => [], 'total' => 0, 'page' => $page, 'perPage' => $per, 'search' => $meta];
}

/** Data kartu (urutan mengikuti $ids). */
function pr_card_items(array $ids) {
    global $wpdb;
    if (!$ids) return [];
    $a = []; $in = pr_in_list($ids, $a);
    $papers = $wpdb->get_results($wpdb->prepare("SELECT p.id, p.title, p.published_date, p.origin, p.sjr_quartile, p.publication_type, p.venue_id, v.display_name AS venue_name, r.published_status AS relevance
        FROM " . pr_t('papers') . " p LEFT JOIN " . pr_t('approved_venues') . " v ON v.id = p.venue_id LEFT JOIN " . pr_t('relevance_scores') . " r ON r.paper_id = p.id WHERE p.id IN ($in)", $a), ARRAY_A);
    $byId = [];
    foreach ($papers as $p) $byId[$p['id']] = $p;

    $a = []; $in = pr_in_list($ids, $a);
    $au = $wpdb->get_results($wpdb->prepare("SELECT pa.paper_id, pa.author_order, a.name FROM " . pr_t('paper_authors') . " pa JOIN " . pr_t('authors') . " a ON a.id = pa.author_id WHERE pa.paper_id IN ($in) ORDER BY pa.paper_id, pa.author_order", $a), ARRAY_A);
    $authors = [];
    foreach ($au as $r) $authors[$r['paper_id']][] = $r['name'];

    $out = [];
    foreach ($ids as $id) {
        if (!isset($byId[$id])) continue;
        $p = $byId[$id]; $names = $authors[$id] ?? [];
        $out[] = [
            'id' => $p['id'], 'title' => $p['title'], 'publishedDate' => $p['published_date'], 'origin' => $p['origin'],
            'venueDisplayName' => $p['venue_name'], 'authorsPreview' => array_slice($names, 0, 3), 'authorCount' => count($names),
            'relevanceBadge' => $p['relevance'], 'sjrQuartile' => $p['sjr_quartile'], 'publicationType' => $p['publication_type'],
        ];
    }
    return $out;
}

// ---------------------------------------------------------------- agregat (cache)
function pr_topics_with_counts() {
    return pr_cached('pr_c_topics', 6 * HOUR_IN_SECONDS, function () {
        global $wpdb;
        $rows = $wpdb->get_results("SELECT t.subfield AS subfield, COUNT(*) AS c FROM " . pr_t('paper_topics') . " t JOIN " . pr_t('papers') . " p ON p.id = t.paper_id WHERE t.subfield IS NOT NULL AND p.metadata_status = 'indexed' GROUP BY t.subfield ORDER BY c DESC", ARRAY_A);
        return array_map(function ($r) { return ['subfield' => $r['subfield'], 'count' => (int) $r['c']]; }, $rows ?: []);
    });
}

function pr_trends() {
    return pr_cached('pr_c_trends', 6 * HOUR_IN_SECONDS, function () {
        global $wpdb;
        $P = pr_t('papers');
        $yr = $wpdb->get_results("SELECT YEAR(published_date) AS y, origin, COUNT(*) AS c FROM $P WHERE metadata_status = 'indexed' AND published_date IS NOT NULL GROUP BY YEAR(published_date), origin", ARRAY_A);
        $byYear = [];
        foreach ($yr as $r) { $y = (int) $r['y']; $byYear[$y] = $byYear[$y] ?? ['year' => $y, 'local' => 0, 'international' => 0]; $byYear[$y][$r['origin']] = (int) $r['c']; }
        ksort($byYear);
        $sf = $wpdb->get_results("SELECT t.subfield AS s, p.origin AS o, COUNT(*) AS c FROM " . pr_t('paper_topics') . " t JOIN $P p ON p.id = t.paper_id WHERE t.subfield IS NOT NULL AND t.is_primary = 1 AND p.metadata_status = 'indexed' GROUP BY t.subfield, p.origin", ARRAY_A);
        $bySub = [];
        foreach ($sf as $r) { $bySub[$r['s']] = $bySub[$r['s']] ?? ['subfield' => $r['s'], 'local' => 0, 'international' => 0]; $bySub[$r['s']][$r['o']] = (int) $r['c']; }
        uasort($bySub, function ($a, $b) { return ($b['local'] + $b['international']) <=> ($a['local'] + $a['international']); });
        return ['byYear' => array_values($byYear), 'bySubfield' => array_values($bySub)];
    });
}

function pr_home_stats() {
    return pr_cached('pr_c_home', HOUR_IN_SECONDS, function () {
        global $wpdb;
        $P = pr_t('papers');
        $total = (int) $wpdb->get_var("SELECT COUNT(*) FROM $P WHERE metadata_status = 'indexed'");
        $local = (int) $wpdb->get_var("SELECT COUNT(*) FROM $P WHERE metadata_status = 'indexed' AND origin = 'local'");
        $inst = (int) $wpdb->get_var("SELECT COUNT(*) FROM " . pr_t('institutions'));
        $sum = (int) $wpdb->get_var("SELECT COUNT(*) FROM " . pr_t('summaries') . " WHERE status = 'published'");
        $recent = $wpdb->get_col("SELECT id FROM $P WHERE metadata_status = 'indexed' ORDER BY published_date DESC, created_at DESC, id ASC LIMIT 6");
        $popular = $wpdb->get_col("SELECT p.id FROM $P p JOIN " . pr_t('citation_stats') . " c ON c.paper_id = p.id WHERE p.metadata_status = 'indexed' AND c.citation_count_total > 0 ORDER BY c.citation_count_total DESC, p.id ASC LIMIT 6");
        return ['totalPapers' => $total, 'localPapers' => $local, 'institutionCount' => $inst, 'curatedSummaryCount' => $sum, 'recentIds' => $recent, 'popularIds' => $popular];
    });
}

// ---------------------------------------------------------------- detail
/** @return array ['type' => 'found'|'redirect'|'not_found', ...] */
function pr_get_paper_detail($id, $lang = 'id') {
    global $wpdb;
    $id = (string) $id;
    $P = pr_t('papers');
    $paper = $wpdb->get_row($wpdb->prepare("SELECT * FROM $P WHERE id = %s AND metadata_status = 'indexed'", $id), ARRAY_A);
    if (!$paper) {
        $sv = $wpdb->get_var($wpdb->prepare("SELECT surviving_id FROM " . pr_t('paper_merges') . " WHERE merged_id = %s LIMIT 1", $id));
        return $sv ? ['type' => 'redirect', 'survivingId' => $sv] : ['type' => 'not_found'];
    }
    $q = function ($sql, ...$args) use ($wpdb) { return $wpdb->get_results($args ? $wpdb->prepare($sql, ...$args) : $sql, ARRAY_A) ?: []; };

    $venue = $paper['venue_id'] ? $wpdb->get_row($wpdb->prepare("SELECT * FROM " . pr_t('approved_venues') . " WHERE id = %s", $paper['venue_id']), ARRAY_A) : null;
    $titles = $q("SELECT language, title, is_primary FROM " . pr_t('paper_titles') . " WHERE paper_id = %s", $id);
    $idfs = $q("SELECT id_type, id_value FROM " . pr_t('paper_identifiers') . " WHERE paper_id = %s", $id);
    $authorsRows = $q("SELECT a.id, a.name FROM " . pr_t('paper_authors') . " pa JOIN " . pr_t('authors') . " a ON a.id = pa.author_id WHERE pa.paper_id = %s ORDER BY pa.author_order", $id);
    $aff = $q("SELECT aa.author_id, i.id, i.name, i.country FROM " . pr_t('author_affiliations') . " aa JOIN " . pr_t('institutions') . " i ON i.id = aa.institution_id WHERE aa.paper_id = %s", $id);
    $authors = [];
    foreach ($authorsRows as $ar) {
        $inst = [];
        foreach ($aff as $f) if ($f['author_id'] === $ar['id']) $inst[] = ['id' => $f['id'], 'name' => $f['name'], 'country' => $f['country']];
        $authors[] = ['name' => $ar['name'], 'institutions' => $inst];
    }
    $countries = $wpdb->get_col($wpdb->prepare("SELECT country_code FROM " . pr_t('paper_affiliation_countries') . " WHERE paper_id = %s", $id));
    $sum = $wpdb->get_row($wpdb->prepare("SELECT language, content, provenance FROM " . pr_t('summaries') . " WHERE paper_id = %s AND status = 'published' AND language = %s LIMIT 1", $id, $lang), ARRAY_A);
    $rel = $wpdb->get_row($wpdb->prepare("SELECT published_status, published_reasoning FROM " . pr_t('relevance_scores') . " WHERE paper_id = %s", $id), ARRAY_A);
    $succ = $q("SELECT r.relation_type, r.reasoning_text, n.id, n.title, n.published_date FROM " . pr_t('paper_relations') . " r JOIN $P n ON n.id = r.paper_id_new WHERE r.paper_id_old = %s AND r.status = 'approved' AND r.relation_type IN ('superseded_by','extended_by','follow_up_same_author')", $id);
    $relSem = $q("SELECT r.reasoning_text, r.paper_id_old, r.paper_id_new, o.title AS old_title, o.published_date AS old_date, n.title AS new_title, n.published_date AS new_date
        FROM " . pr_t('paper_relations') . " r JOIN $P o ON o.id = r.paper_id_old JOIN $P n ON n.id = r.paper_id_new
        WHERE r.status = 'approved' AND r.relation_type = 'related_semantic' AND (r.paper_id_old = %s OR r.paper_id_new = %s)", $id, $id);
    $versions = $q("SELECT version_number, changed_summary, version_date FROM " . pr_t('paper_versions') . " WHERE paper_id = %s ORDER BY version_number", $id);
    $file = $wpdb->get_row($wpdb->prepare("SELECT original_name, size_bytes, download_count, storage_key FROM " . pr_t('paper_files') . " WHERE paper_id = %s", $id), ARRAY_A);

    $related = [];
    foreach ($relSem as $r) {
        $other = $r['paper_id_old'] === $id ? ['id' => $r['paper_id_new'], 'title' => $r['new_title'], 'publishedDate' => $r['new_date']] : ['id' => $r['paper_id_old'], 'title' => $r['old_title'], 'publishedDate' => $r['old_date']];
        $related[] = ['reasoningText' => $r['reasoning_text'], 'paper' => $other];
    }
    return ['type' => 'found', 'data' => [
        'id' => $paper['id'], 'title' => $paper['title'], 'publishedDate' => $paper['published_date'],
        'titles' => array_map(function ($t) { return ['language' => $t['language'], 'title' => $t['title'], 'isPrimary' => (bool) $t['is_primary']]; }, $titles),
        'abstract' => $paper['abstract_display_policy'] === 'full' ? $paper['abstract_raw'] : null,
        'canonicalUrl' => $paper['canonical_url'],
        'identifiers' => array_map(function ($i) { return ['idType' => $i['id_type'], 'idValue' => $i['id_value']]; }, $idfs),
        'authors' => $authors, 'venue' => $venue ? ['displayName' => $venue['display_name'], 'venueType' => $venue['venue_type']] : null,
        'origin' => $paper['origin'], 'affiliationCountries' => $countries, 'isFoundational' => (bool) $paper['is_foundational'],
        'affiliationInferred' => (bool) $paper['affiliation_inferred'],
        'summary' => $sum ? ['language' => $sum['language'], 'content' => $sum['content'], 'provenance' => $sum['provenance']] : null,
        'relevance' => $rel ? ['publishedStatus' => $rel['published_status'], 'publishedReasoning' => $rel['published_reasoning']] : null,
        'sjrQuartile' => $paper['sjr_quartile'],
        'successors' => array_map(function ($s) { return ['relationType' => $s['relation_type'], 'reasoningText' => $s['reasoning_text'], 'paper' => ['id' => $s['id'], 'title' => $s['title'], 'publishedDate' => $s['published_date']]]; }, $succ),
        'related' => $related,
        'versions' => array_map(function ($v) { return ['versionNumber' => (int) $v['version_number'], 'changedSummary' => $v['changed_summary'], 'versionDate' => $v['version_date']]; }, $versions),
        'publicationType' => $paper['publication_type'],
        'file' => $file ? ['originalName' => $file['original_name'], 'sizeBytes' => (int) $file['size_bytes'], 'downloadCount' => (int) $file['download_count'], 'storageKey' => $file['storage_key']] : null,
    ]];
}

// ---------------------------------------------------------------- BibTeX (bibtex.ts)
function pr_bibtex_escape($v) {
    return preg_replace_callback('/[{}&%$#_]/', function ($m) { return '\\' . $m[0]; }, $v);
}

function pr_get_bibtex($id) {
    global $wpdb;
    $p = $wpdb->get_row($wpdb->prepare("SELECT p.title, p.published_date, p.canonical_url, v.display_name AS vn, v.venue_type AS vt FROM " . pr_t('papers') . " p LEFT JOIN " . pr_t('approved_venues') . " v ON v.id = p.venue_id WHERE p.id = %s AND p.metadata_status = 'indexed'", $id), ARRAY_A);
    if (!$p) return null;
    $authors = $wpdb->get_col($wpdb->prepare("SELECT a.name FROM " . pr_t('paper_authors') . " pa JOIN " . pr_t('authors') . " a ON a.id = pa.author_id WHERE pa.paper_id = %s ORDER BY pa.author_order", $id));
    $doi = $wpdb->get_var($wpdb->prepare("SELECT id_value FROM " . pr_t('paper_identifiers') . " WHERE paper_id = %s AND id_type = 'doi' LIMIT 1", $id));
    $year = $p['published_date'] ? (int) substr($p['published_date'], 0, 4) : null;
    $type = $p['vt'] === 'journal' ? 'article' : ($p['vt'] === 'conference' ? 'inproceedings' : 'misc');
    if (!$authors) $key = 'unknown' . ($year ?? 'nd');
    else {
        $parts = preg_split('/\s+/', trim($authors[0])); $last = strtolower(preg_replace('/[^a-z0-9]/i', '', end($parts) ?: 'unknown'));
        preg_match('/[A-Za-z0-9]+/', trim($p['title']), $m);
        $key = $last . ($year ?? 'nd') . strtolower($m[0] ?? 'untitled');
    }
    $f = ['  title = {' . pr_bibtex_escape($p['title']) . '}'];
    if ($authors) $f[] = '  author = {' . implode(' and ', array_map('pr_bibtex_escape', $authors)) . '}';
    if ($year !== null) $f[] = '  year = {' . $year . '}';
    if ($p['vn']) $f[] = '  ' . ($type === 'article' ? 'journal' : ($type === 'inproceedings' ? 'booktitle' : 'howpublished')) . ' = {' . pr_bibtex_escape($p['vn']) . '}';
    if ($doi) $f[] = '  doi = {' . pr_bibtex_escape($doi) . '}';
    $url = $p['canonical_url'] ?: ($doi ? 'https://doi.org/' . $doi : null);
    if ($url) $f[] = '  url = {' . pr_bibtex_escape($url) . '}';
    return '@' . $type . '{' . $key . ",\n" . implode(",\n", $f) . "\n}\n";
}
