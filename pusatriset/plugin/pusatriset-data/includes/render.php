<?php
/**
 * Renderer HTML: port literal komponen React aplikasi lama (kelas Tailwind SAMA persis, CSS dikompilasi dari kelas itu)
 * supaya tampilan identik. Semua keluaran di dalam <div class="pr-scope">.
 */
if (!defined('ABSPATH')) exit;

// ---------------------------------------------------------------- util
function pr_e($s) { return esc_html((string) $s); }
function pr_a($s) { return esc_attr((string) $s); }

function pr_icon($name, $cls = '') {
    static $icons = null;
    if ($icons === null) $icons = require PR_DIR . 'includes/icons.php';
    $inner = $icons[$name] ?? '';
    $slug = strtolower(preg_replace('/(?<!^)[A-Z0-9]/', '-$0', $name));
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-' . $slug . ($cls ? ' ' . $cls : '') . '" aria-hidden="true">' . $inner . '</svg>';
}

function pr_num($n) { return number_format((float) $n, 0, ',', '.'); }
function pr_year($d) { return $d ? substr((string) $d, 0, 4) : ''; }
function pr_date_id($d) {
    if (!$d) return '';
    $m = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
    $t = strtotime(substr((string) $d, 0, 10) . ' UTC');
    return (int) gmdate('j', $t) . ' ' . $m[(int) gmdate('n', $t) - 1] . ' ' . gmdate('Y', $t);
}

function pr_url_katalog() { return apply_filters('pr_url_katalog', home_url('/katalog/')); }
function pr_url_dashboard() { return apply_filters('pr_url_dashboard', home_url('/dashboard/')); }
function pr_url_paper($id, $qs = '') { return home_url('/riset/' . $id . ($qs ? '?' . $qs : '')); }

// ---------------------------------------------------------------- badge
function pr_quartile_badge($q, $size = 'sm') {
    $labels = ['q1' => 'Q1', 'q2' => 'Q2', 'q3' => 'Q3', 'q4' => 'Q4', 'unindexed' => 'Non-Scopus'];
    $cls = ['q1' => 'bg-emerald-100 text-emerald-800', 'q2' => 'bg-sky-100 text-sky-800', 'q3' => 'bg-amber-100 text-amber-800', 'q4' => 'bg-orange-100 text-orange-800', 'unindexed' => 'bg-slate-100 text-slate-600'];
    if (!$q || !isset($labels[$q])) return '';
    $sz = $size === 'lg' ? 'px-3 py-1.5 text-sm' : 'px-2 py-0.5 text-xs';
    return '<span class="inline-flex items-center rounded-full font-medium ' . $sz . ' ' . $cls[$q] . '" title="Kuartil SJR (Scimago Journal Rank)">' . $labels[$q] . '</span>';
}

function pr_relevance_badge($s, $size = 'sm') {
    $labels = ['still_relevant' => 'Masih Relevan', 'needs_update' => 'Perlu Pembaruan', 'superseded' => 'Sudah Digantikan', 'retracted' => 'Ditarik', 'foundational' => 'Riset Fondasi'];
    $cls = [
        'still_relevant' => 'bg-[var(--badge-still-relevant-bg)] text-[var(--badge-still-relevant-fg)]',
        'needs_update' => 'bg-[var(--badge-needs-update-bg)] text-[var(--badge-needs-update-fg)]',
        'superseded' => 'bg-[var(--badge-superseded-bg)] text-[var(--badge-superseded-fg)]',
        'retracted' => 'bg-[var(--badge-retracted-bg)] text-[var(--badge-retracted-fg)]',
        'foundational' => 'bg-[var(--badge-foundational-bg)] text-[var(--badge-foundational-fg)]',
    ];
    if (!$s || !isset($labels[$s])) return '';
    $sz = $size === 'lg' ? 'px-3 py-1.5 text-sm' : 'px-2 py-0.5 text-xs';
    return '<span class="inline-flex items-center rounded-full font-medium ' . $sz . ' ' . $cls[$s] . '">' . $labels[$s] . '</span>';
}

function pr_origin_flag($origin) {
    return $origin === 'local' ? '<span title="Riset Indonesia" aria-label="Riset Indonesia">🇮🇩</span>' : '';
}

function pr_publication_badge($t) {
    return $t === 'own_publication' ? '<span class="inline-flex items-center rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700" title="Publikasi PusatRiset.ai">Publikasi PusatRiset.ai</span>' : '';
}

function pr_retracted_banner($reasoning = null, $compact = false) {
    if ($compact) return '<p class="text-xs font-medium text-[var(--badge-retracted-fg)]">⚠ Paper ini telah ditarik (retracted)</p>';
    return '<div class="mb-6 rounded-md border border-[var(--badge-retracted-fg)]/30 bg-[var(--badge-retracted-bg)] p-4"><p class="font-semibold text-[var(--badge-retracted-fg)]">⚠ Paper ini telah ditarik (retracted)</p>'
        . ($reasoning ? '<p class="mt-1 text-sm text-[var(--badge-retracted-fg)]">' . pr_e($reasoning) . '</p>' : '') . '</div>';
}

// ---------------------------------------------------------------- kartu paper
function pr_authors_line(array $preview, $count) {
    if (!$preview) return 'Penulis tidak diketahui';
    $shown = implode(', ', array_slice($preview, 0, 3));
    return $count > 3 ? $shown . ', dkk.' : $shown;
}

function pr_paper_card(array $p) {
    $h = '<article class="group relative overflow-hidden rounded-2xl border border-warm bg-card p-5 shadow-[var(--shadow-card)] transition hover:-translate-y-0.5 hover:border-brand-700/40 hover:shadow-lg">';
    $h .= '<span class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-teal-400 via-brand-700 to-indigo-500 opacity-0 transition-opacity group-hover:opacity-100"></span>';
    $h .= '<div class="flex flex-wrap items-start justify-between gap-2">';
    $h .= '<a href="' . pr_a(pr_url_paper($p['id'])) . '" class="flex items-start gap-2 text-base font-semibold leading-snug text-primary hover:text-brand-700 hover:underline">' . pr_icon('FileText', 'mt-0.5 h-4 w-4 shrink-0 text-brand-700');
    $h .= '<span>' . pr_origin_flag($p['origin']) . ' ' . pr_e($p['title']) . '</span></a>';
    $h .= '<span class="flex shrink-0 items-center gap-1.5">' . pr_quartile_badge($p['sjrQuartile']) . pr_relevance_badge($p['relevanceBadge']) . '</span></div>';
    if ($p['relevanceBadge'] === 'retracted') $h .= '<div class="mt-1">' . pr_retracted_banner(null, true) . '</div>';
    $line = pr_authors_line($p['authorsPreview'], $p['authorCount']);
    if ($p['venueDisplayName']) $line .= ' · ' . $p['venueDisplayName'];
    if ($p['publishedDate']) $line .= ' · ' . pr_year($p['publishedDate']);
    $h .= '<p class="mt-2 text-sm text-secondary">' . pr_e($line) . '</p>';
    if ($p['publicationType'] === 'own_publication') $h .= '<div class="mt-3 flex flex-wrap gap-1.5">' . pr_publication_badge($p['publicationType']) . '</div>';
    return $h . '</article>';
}

function pr_card_grid(array $items, $cls = 'grid gap-4 sm:grid-cols-2 lg:grid-cols-3') {
    $h = '<div class="' . $cls . '">';
    foreach ($items as $p) $h .= pr_paper_card($p);
    return $h . '</div>';
}

// ---------------------------------------------------------------- parameter katalog
function pr_catalog_params() {
    $g = function ($k) { return isset($_GET[$k]) ? wp_unslash($_GET[$k]) : null; };
    $first = function ($v) { return is_array($v) ? ($v[0] ?? null) : $v; };
    $list = function ($v) { return $v === null || $v === '' ? [] : array_values(array_map('strval', (array) $v)); };
    $originRaw = $first($g('origin'));
    $own = $originRaw === 'own_publication' || $first($g('ownPublication')) === 'true';
    $rel = $first($g('relevance')); $qr = $first($g('quartile'));
    $page = max(1, (int) ($first($g('hal')) ?: 1));
    return [
        'q' => ($v = $first($g('q'))) !== null ? trim(sanitize_text_field($v)) : '',
        'origin' => in_array($originRaw, ['local', 'international'], true) ? $originRaw : '',
        'own' => $own,
        'yearFrom' => preg_match('/^\d{4}$/', (string) $first($g('yearFrom'))) ? (string) $first($g('yearFrom')) : '',
        'yearTo' => preg_match('/^\d{4}$/', (string) $first($g('yearTo'))) ? (string) $first($g('yearTo')) : '',
        'subfields' => array_map('sanitize_text_field', $list($g('subfield'))),
        'relevance' => in_array($rel, ['still_relevant', 'needs_update', 'superseded', 'retracted', 'foundational', 'none'], true) ? $rel : '',
        'quartile' => in_array($qr, ['q1', 'q2', 'q3', 'q4', 'unindexed'], true) ? $qr : '',
        'policyTag' => ($v = $first($g('policyTag'))) ? sanitize_title($v) : '',
        'hideSuperseded' => $first($g('hideSuperseded')) === 'true',
        'openAccess' => $first($g('openAccess')) === 'true',
        'page' => $page,
    ];
}

function pr_catalog_href(array $c, $targetPage, $overrideQ = null) {
    $params = [];
    $q = $overrideQ !== null ? $overrideQ : $c['q'];
    if ($q !== '') $params[] = 'q=' . rawurlencode($q);
    if ($c['own']) $params[] = 'origin=own_publication'; elseif ($c['origin']) $params[] = 'origin=' . $c['origin'];
    if ($c['yearFrom']) $params[] = 'yearFrom=' . $c['yearFrom'];
    if ($c['yearTo']) $params[] = 'yearTo=' . $c['yearTo'];
    foreach ($c['subfields'] as $s) $params[] = 'subfield=' . rawurlencode($s);
    if ($c['relevance']) $params[] = 'relevance=' . $c['relevance'];
    if ($c['quartile']) $params[] = 'quartile=' . $c['quartile'];
    if ($c['policyTag']) $params[] = 'policyTag=' . rawurlencode($c['policyTag']);
    if ($c['hideSuperseded']) $params[] = 'hideSuperseded=true';
    if ($c['openAccess']) $params[] = 'openAccess=true';
    if ($targetPage > 1) $params[] = 'hal=' . (int) $targetPage;
    return pr_url_katalog() . ($params ? '?' . implode('&', $params) : '');
}

// ---------------------------------------------------------------- filter + pagination
function pr_legend($icon, $text) {
    return '<legend class="mb-2 flex items-center gap-1.5 font-semibold text-primary">' . pr_icon($icon, 'h-4 w-4 text-brand-700') . $text . '</legend>';
}

function pr_filter_form(array $c, array $subfieldOptions) {
    $originVal = $c['own'] ? 'own_publication' : $c['origin'];
    $h = '<form method="GET" action="' . pr_a(pr_url_katalog()) . '" class="pr-filter space-y-5 text-sm text-primary">';
    if ($c['q'] !== '') $h .= '<input type="hidden" name="q" value="' . pr_a($c['q']) . '">';
    $h .= '<div class="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-muted-warm">' . pr_icon('SlidersHorizontal', 'h-3.5 w-3.5') . 'Filter</div>';

    $h .= '<fieldset class="border-t border-warm pt-4">' . pr_legend('Globe2', 'Asal Riset') . '<div class="space-y-1.5">';
    foreach ([['', 'Semua'], ['local', 'Indonesia'], ['international', 'Internasional'], ['own_publication', 'Publikasi PusatRiset.ai']] as $o) {
        $h .= '<label class="flex items-center gap-2"><input type="radio" name="origin" value="' . pr_a($o[0]) . '"' . ($originVal === $o[0] ? ' checked' : '') . ' data-autosubmit> ' . pr_e($o[1]) . '</label>';
    }
    $h .= '</div></fieldset>';

    $h .= '<fieldset class="border-t border-warm pt-4">' . pr_legend('CalendarRange', 'Rentang Tahun') . '<div class="flex items-center gap-2">'
        . '<input type="number" name="yearFrom" value="' . pr_a($c['yearFrom']) . '" placeholder="Dari" data-autosubmit-blur class="w-full rounded border border-warm bg-card px-2 py-1">'
        . '<span class="text-muted-warm">—</span>'
        . '<input type="number" name="yearTo" value="' . pr_a($c['yearTo']) . '" placeholder="Sampai" data-autosubmit-blur class="w-full rounded border border-warm bg-card px-2 py-1"></div></fieldset>';

    $h .= '<fieldset class="border-t border-warm pt-4">' . pr_legend('Tags', 'Subbidang') . '<div class="max-h-48 space-y-1.5 overflow-y-auto pr-1">';
    foreach ($subfieldOptions as $o) {
        $h .= '<label class="flex items-center gap-2"><input type="checkbox" name="subfield" value="' . pr_a($o['subfield']) . '"' . (in_array($o['subfield'], $c['subfields'], true) ? ' checked' : '') . ' data-autosubmit> ' . pr_e($o['subfield']) . ' <span class="text-muted-warm">(' . (int) $o['count'] . ')</span></label>';
    }
    $h .= '</div></fieldset>';

    $sel = function ($name, $opts, $val) {
        $s = '<select name="' . $name . '" data-autosubmit class="w-full rounded border border-warm bg-card px-2 py-1.5">';
        foreach ($opts as $o) $s .= '<option value="' . pr_a($o[0]) . '"' . ($val === $o[0] ? ' selected' : '') . '>' . pr_e($o[1]) . '</option>';
        return $s . '</select>';
    };
    $h .= '<fieldset class="border-t border-warm pt-4">' . pr_legend('Award', 'Badge Relevansi')
        . $sel('relevance', [['', 'Semua'], ['still_relevant', 'Masih Relevan'], ['needs_update', 'Perlu Pembaruan'], ['superseded', 'Sudah Digantikan'], ['retracted', 'Ditarik'], ['foundational', 'Riset Fondasi'], ['none', 'Tanpa Badge']], $c['relevance']) . '</fieldset>';
    $h .= '<fieldset class="border-t border-warm pt-4">' . pr_legend('BarChart3', 'Kuartil SJR')
        . $sel('quartile', [['', 'Semua'], ['q1', 'Q1'], ['q2', 'Q2'], ['q3', 'Q3'], ['q4', 'Q4'], ['unindexed', 'Non-Scopus']], $c['quartile']) . '</fieldset>';

    $h .= '<div class="space-y-2 border-t border-warm pt-4">'
        . '<label class="flex items-center gap-2"><input type="checkbox" name="hideSuperseded" value="true"' . ($c['hideSuperseded'] ? ' checked' : '') . ' data-autosubmit> Sembunyikan yang sudah digantikan</label>'
        . '<label class="flex items-center gap-2"><input type="checkbox" name="openAccess" value="true"' . ($c['openAccess'] ? ' checked' : '') . ' data-autosubmit> Hanya akses terbuka</label></div>';

    $h .= '<noscript><button type="submit" class="w-full rounded-md bg-brand-700 px-4 py-2 text-white">Terapkan Filter</button></noscript>';
    $h .= '<a href="' . pr_a(pr_url_katalog()) . '" class="block text-center text-brand-700 hover:underline">Reset semua filter</a></form>';
    return $h;
}

function pr_pagination($page, $perPage, $total, callable $href) {
    $pages = max(1, (int) ceil($total / $perPage));
    if ($pages <= 1) return '';
    $h = '<nav class="mt-8 flex items-center justify-center gap-4 text-sm">';
    $h .= $page <= 1 ? '<span class="text-muted-warm">← Sebelumnya</span>' : '<a href="' . pr_a($href($page - 1)) . '" class="text-brand-700 hover:underline">← Sebelumnya</a>';
    $h .= '<span class="text-secondary">Halaman ' . (int) $page . ' dari ' . (int) $pages . '</span>';
    $h .= $page >= $pages ? '<span class="text-muted-warm">Selanjutnya →</span>' : '<a href="' . pr_a($href($page + 1)) . '" class="text-brand-700 hover:underline">Selanjutnya →</a>';
    return $h . '</nav>';
}

// ---------------------------------------------------------------- halaman: katalog
/** Isi halaman Archive (tanpa Header/Footer situs). $withHero=false bila judul/hero dibuat native di Elementor. */
function pr_render_catalog($withHero = true) {
    $c = pr_catalog_params();
    $res = pr_list_papers([
        'q' => $c['q'], 'origin' => $c['origin'], 'yearFrom' => $c['yearFrom'], 'yearTo' => $c['yearTo'], 'subfield' => $c['subfields'], 'relevance' => $c['relevance'],
        'quartile' => $c['quartile'], 'policyTag' => $c['policyTag'], 'hideSuperseded' => $c['hideSuperseded'], 'openAccess' => $c['openAccess'],
        'publicationType' => $c['own'] ? 'own_publication' : '', 'page' => $c['page'], 'perPage' => 20,
    ]);
    $sub = pr_topics_with_counts();
    $href = function ($p, $q = null) use ($c) { return pr_catalog_href($c, $p, $q); };
    $fmt = pr_num($res['total']);

    $h = '<div class="pr-scope bg-page text-primary">';
    if ($withHero) {
        $h .= '<section class="relative overflow-hidden border-b border-warm bg-card-alt"><div class="pointer-events-none absolute -right-16 -top-16 -z-10 h-56 w-56 rounded-full bg-gradient-to-br from-teal-200/40 to-transparent blur-3xl"></div>'
            . '<div class="mx-auto max-w-6xl px-4 py-10 sm:px-6"><div class="flex items-center gap-3"><div class="flex h-11 w-11 items-center justify-center rounded-full bg-brand-100">' . pr_icon('LibraryBig', 'h-5 w-5 text-brand-700') . '</div>'
            . '<div><h1 class="text-xl font-bold text-brand-900 sm:text-2xl">Archive Riset</h1><p class="text-sm text-secondary">' . $fmt . ' riset AI Indonesia &amp; dunia siap dijelajahi</p></div></div>'
            . pr_catalog_search_form($c) . '</div></section>';
    }
    $h .= '<div class="mx-auto max-w-6xl px-4 py-8 sm:px-6"><div class="grid grid-cols-1 gap-8 lg:grid-cols-[240px_1fr]">';
    $h .= '<aside class="order-2 h-fit rounded-[14px] border border-warm bg-card p-4 shadow-[var(--shadow-card)] lg:sticky lg:top-20 lg:order-1">' . pr_filter_form($c, $sub) . '</aside>';
    $h .= '<div class="order-1 lg:order-2">';
    $s = $res['search'];
    if ($s['queryOriginal']) {
        $h .= '<p class="mb-1 flex flex-wrap items-center gap-1.5 text-sm text-secondary">' . pr_icon('LayoutGrid', 'h-4 w-4 shrink-0 text-brand-700') . 'Menampilkan ' . $fmt . ' hasil untuk “' . pr_e($s['queryOriginal']) . '”';
        if ($s['matchedSynonyms']) $h .= '<span class="text-muted-warm">— termasuk istilah: ' . pr_e(implode(', ', $s['matchedSynonyms'])) . '</span>';
        $h .= '</p>';
    } else {
        $h .= '<p class="mb-1 flex items-center gap-1.5 text-sm text-secondary">' . pr_icon('LayoutGrid', 'h-4 w-4 text-brand-700') . $fmt . ' riset ditemukan</p>';
    }
    if ($s['suggestion']) $h .= '<p class="mb-4 text-sm text-secondary">Mungkin maksud Anda: <a href="' . pr_a($href(1, $s['suggestion'])) . '" class="font-medium text-brand-700 hover:underline">“' . pr_e($s['suggestion']) . '”</a>?</p>';
    else $h .= '<div class="mb-4"></div>';

    if (!$res['data']) {
        $h .= '<div class="rounded-[14px] border border-dashed border-warm bg-card-alt p-12 text-center">' . pr_icon('SearchX', 'mx-auto h-8 w-8 text-muted-warm');
        if ($s['queryOriginal']) {
            $h .= '<p class="mt-3 text-sm text-secondary">Tidak ada hasil untuk “' . pr_e($s['queryOriginal']) . '” — coba kata kunci lain atau longgarkan filter.</p>';
            if ($s['popularSuggestions']) {
                $links = [];
                foreach ($s['popularSuggestions'] as $t) $links[] = '<a href="' . pr_a($href(1, $t)) . '" class="font-medium text-brand-700 hover:underline">' . pr_e($t) . '</a>';
                $h .= '<p class="mt-3 text-sm text-secondary">Coba: ' . implode(', ', $links) . '</p>';
            }
        } else $h .= '<p class="mt-3 text-sm text-secondary">Tidak ada hasil — coba longgarkan filter.</p>';
        $h .= '</div>';
    } else {
        $h .= pr_card_grid($res['data'], 'grid gap-4 sm:grid-cols-2');
    }
    $h .= pr_pagination($res['page'], $res['perPage'], $res['total'], $href);
    return $h . '</div></div></div></div>';
}

function pr_catalog_search_form(array $c) {
    $h = '<form action="' . pr_a(pr_url_katalog()) . '" method="GET" class="mt-6 flex gap-2">';
    if ($c['own']) $h .= '<input type="hidden" name="origin" value="own_publication">'; elseif ($c['origin']) $h .= '<input type="hidden" name="origin" value="' . pr_a($c['origin']) . '">';
    foreach (['yearFrom', 'yearTo', 'relevance', 'quartile', 'policyTag'] as $k) if ($c[$k]) $h .= '<input type="hidden" name="' . $k . '" value="' . pr_a($c[$k]) . '">';
    foreach ($c['subfields'] as $sf) $h .= '<input type="hidden" name="subfield" value="' . pr_a($sf) . '">';
    if ($c['hideSuperseded']) $h .= '<input type="hidden" name="hideSuperseded" value="true">';
    if ($c['openAccess']) $h .= '<input type="hidden" name="openAccess" value="true">';
    $h .= '<div class="relative flex-1">' . pr_icon('Search', 'pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-warm')
        . '<input type="text" name="q" value="' . pr_a($c['q']) . '" placeholder="Cari judul, topik, atau kata kunci riset..." class="w-full rounded-md border border-warm bg-card py-2.5 pl-10 pr-4 text-sm shadow-[var(--shadow-card)] focus:border-brand-700 focus:outline-none"></div>'
        . '<button type="submit" class="rounded-md bg-brand-700 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-900">Cari</button></form>';
    return $h;
}

// ---------------------------------------------------------------- halaman: dashboard
function pr_chart_year_area(array $data) {
    if (!$data) return '<p class="text-sm text-secondary">Belum ada data.</p>';
    $w = 600; $ht = 220; $px = 8; $py = 12;
    $max = 1; foreach ($data as $d) $max = max($max, $d['local'], $d['international']);
    $n = count($data); $step = $n > 1 ? ($w - $px * 2) / ($n - 1) : 0;
    $y = function ($v) use ($ht, $py, $max) { return $ht - $py - ($v / $max) * ($ht - $py * 2); };
    $x = function ($i) use ($px, $step) { return $px + $i * $step; };
    $fmt = function ($f) { return rtrim(rtrim(sprintf('%.10F', $f), '0'), '.'); };
    $line = function ($key) use ($data, $x, $y, $fmt) { $p = []; foreach ($data as $i => $d) $p[] = ($i === 0 ? 'M' : 'L') . ' ' . $fmt($x($i)) . ' ' . $fmt($y($d[$key])); return implode(' ', $p); };
    $area = function ($key) use ($line, $x, $ht, $py, $n, $fmt) { return $line($key) . ' L ' . $fmt($x($n - 1)) . ' ' . ($ht - $py) . ' L ' . $fmt($x(0)) . ' ' . ($ht - $py) . ' Z'; };
    $h = '<div><svg viewBox="0 0 ' . $w . ' ' . $ht . '" class="w-full" style="height:220px"><defs>'
        . '<linearGradient id="areaTeal" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2dd4bf" stop-opacity="0.35"/><stop offset="100%" stop-color="#2dd4bf" stop-opacity="0"/></linearGradient>'
        . '<linearGradient id="areaBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--brand-blue-700)" stop-opacity="0.3"/><stop offset="100%" stop-color="var(--brand-blue-700)" stop-opacity="0"/></linearGradient></defs>'
        . '<path d="' . $area('international') . '" fill="url(#areaBlue)"/><path d="' . $line('international') . '" fill="none" stroke="var(--brand-blue-700)" stroke-width="2.5"/>'
        . '<path d="' . $area('local') . '" fill="url(#areaTeal)"/><path d="' . $line('local') . '" fill="none" stroke="#0f766e" stroke-width="2.5"/>';
    foreach ($data as $i => $d) $h .= '<g><circle cx="' . $fmt($x($i)) . '" cy="' . $fmt($y($d['local'])) . '" r="3" fill="#0f766e"/><circle cx="' . $fmt($x($i)) . '" cy="' . $fmt($y($d['international'])) . '" r="3" fill="var(--brand-blue-700)"/></g>';
    $h .= '</svg><div class="mt-1 flex justify-between text-[11px] text-muted-warm">';
    foreach ($data as $i => $d) $h .= '<span class="' . ($n > 10 && $i % 2 !== 0 ? 'hidden sm:inline' : '') . '">' . (int) $d['year'] . '</span>';
    return $h . '</div></div>';
}

function pr_chart_donut($local, $intl) {
    $total = $local + $intl; $pct = $total > 0 ? $local / $total : 0;
    $size = 160; $stroke = 18; $r = ($size - $stroke) / 2; $circ = 2 * M_PI * $r; $len = $circ * $pct;
    $f = function ($v) { return rtrim(rtrim(sprintf('%.10F', $v), '0'), '.'); };
    return '<div class="flex flex-col items-center"><svg width="' . $size . '" height="' . $size . '" viewBox="0 0 ' . $size . ' ' . $size . '" class="-rotate-90">'
        . '<circle cx="' . $size / 2 . '" cy="' . $size / 2 . '" r="' . $f($r) . '" fill="none" stroke="var(--bg-card-alt)" stroke-width="' . $stroke . '"/>'
        . '<circle cx="' . $size / 2 . '" cy="' . $size / 2 . '" r="' . $f($r) . '" fill="none" stroke="var(--brand-blue-700)" stroke-width="' . $stroke . '" stroke-dasharray="' . $f($len) . ' ' . $f($circ - $len) . '" stroke-linecap="round"/></svg>'
        . '<div class="-mt-[100px] flex h-[100px] flex-col items-center justify-center"><p class="text-2xl font-bold text-primary">' . (int) round($pct * 100) . '%</p><p class="text-[11px] text-secondary">Indonesia</p></div></div>';
}

function pr_chart_subfield_bars(array $data) {
    if (!$data) return '<p class="text-sm text-secondary">Belum ada data.</p>';
    $max = 1; foreach ($data as $d) $max = max($max, $d['local'] + $d['international']);
    $h = '<div class="space-y-3">';
    foreach ($data as $d) {
        $h .= '<div><div class="mb-1 flex justify-between text-xs text-secondary"><span>' . pr_e($d['subfield']) . '</span><span>' . ($d['local'] + $d['international']) . '</span></div>'
            . '<div class="flex h-4 w-full overflow-hidden rounded-full bg-card-alt"><div class="gradient-card-teal" style="width:' . ($d['local'] / $max * 100) . '%" title="Indonesia: ' . $d['local'] . '"></div>'
            . '<div class="gradient-card-blue" style="width:' . ($d['international'] / $max * 100) . '%" title="Internasional: ' . $d['international'] . '"></div></div></div>';
    }
    return $h . '</div>';
}

function pr_dash_legend() {
    return '<div class="mt-4 flex gap-4 border-t border-warm pt-3 text-xs text-secondary"><span class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-full" style="background:#0f766e"></span> Indonesia</span>'
        . '<span class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-full bg-brand-700"></span> Internasional</span></div>';
}

function pr_render_dashboard($withHero = true) {
    $t = pr_trends();
    $local = 0; $intl = 0;
    foreach ($t['byYear'] as $d) { $local += $d['local']; $intl += $d['international']; }
    $total = $local + $intl; $share = $total > 0 ? (int) round($local / $total * 100) : 0;
    $kpi = [['Riset Indonesia', pr_num($local), 'Flag', 'gradient-card-teal'], ['Riset Internasional', pr_num($intl), 'Globe2', 'gradient-card-blue'], ['Porsi Riset Indonesia', $share . '%', 'PieChart', 'gradient-card-indigo']];
    $h = '<div class="pr-scope bg-page text-primary">';
    if ($withHero) {
        $h .= '<section class="border-b border-warm bg-card-alt"><div class="mx-auto flex max-w-5xl items-center gap-3 px-4 py-10 sm:px-6"><div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brand-100">' . pr_icon('LineChart', 'h-5 w-5 text-brand-700') . '</div>'
            . '<div><h1 class="text-xl font-bold text-brand-900 sm:text-2xl">Dashboard Tren Riset</h1><p class="mt-1 max-w-2xl text-sm text-secondary">Perbandingan pertumbuhan riset AI Indonesia dengan riset internasional dari waktu ke waktu dan per subbidang — gambaran awal area yang masih jarang diteliti di Indonesia dibanding tren global.</p></div></div></section>';
    }
    $h .= '<div class="relative overflow-hidden"><div class="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-b from-brand-100/50 via-transparent to-transparent"></div>'
        . '<div class="pointer-events-none absolute -right-24 top-10 -z-10 h-72 w-72 rounded-full bg-gradient-to-br from-teal-200/40 to-transparent blur-3xl"></div>'
        . '<div class="mx-auto max-w-5xl px-4 py-8 sm:px-6"><div class="grid gap-4 sm:grid-cols-3">';
    foreach ($kpi as $k) {
        $h .= '<div class="' . $k[3] . ' rounded-2xl p-5 text-white shadow-lg"><div class="flex items-start justify-between"><div class="flex h-9 w-9 items-center justify-center rounded-full bg-white/15">' . pr_icon($k[2], 'h-4 w-4 text-white') . '</div>' . pr_icon('TrendingUp', 'h-4 w-4 text-white/70') . '</div>'
            . '<p class="mt-3 text-2xl font-bold">' . pr_e($k[1]) . '</p><p class="mt-1 text-xs text-white/80">' . pr_e($k[0]) . '</p></div>';
    }
    $h .= '</div><div class="mt-6 grid gap-6 lg:grid-cols-[1fr_260px]">'
        . '<section class="glass-card rounded-2xl p-6 shadow-[var(--shadow-card)]"><h2 class="flex items-center gap-2 text-lg font-semibold text-primary">' . pr_icon('TrendingUp', 'h-5 w-5 text-brand-700') . 'Jumlah Riset per Tahun</h2><div class="mt-4">' . pr_chart_year_area($t['byYear']) . '</div>' . pr_dash_legend() . '</section>'
        . '<section class="glass-card flex flex-col items-center justify-center rounded-2xl p-6 shadow-[var(--shadow-card)]"><h2 class="self-start flex items-center gap-2 text-sm font-semibold text-primary">' . pr_icon('PieChart', 'h-4 w-4 text-brand-700') . 'Proporsi Total</h2><div class="mt-4">' . pr_chart_donut($local, $intl) . '</div>' . pr_dash_legend() . '</section></div>'
        . '<section class="mt-6 glass-card rounded-2xl p-6 shadow-[var(--shadow-card)]"><h2 class="flex items-center gap-2 text-lg font-semibold text-primary">' . pr_icon('PieChart', 'h-5 w-5 text-brand-700') . 'Riset per Subbidang</h2><div class="mt-4">' . pr_chart_subfield_bars($t['bySubfield']) . '</div>' . pr_dash_legend() . '</section>'
        . '</div></div></div>';
    return $h;
}

// ---------------------------------------------------------------- beranda: potongan dinamis
function pr_render_hero_art() {
    $line = function ($a) { return '<line x1="' . $a[0] . '" y1="' . $a[1] . '" x2="' . $a[2] . '" y2="' . $a[3] . '"/>'; };
    $lines = [[90, 120, 200, 80], [200, 80, 310, 130], [90, 120, 140, 230], [200, 80, 200, 200], [310, 130, 270, 240], [140, 230, 200, 200], [200, 200, 270, 240], [140, 230, 180, 320], [270, 240, 240, 320], [180, 320, 240, 320]];
    $dots = [[90, 120, 6], [200, 80, 8], [310, 130, 6], [140, 230, 7], [200, 200, 10], [270, 240, 7], [180, 320, 5], [240, 320, 5]];
    $h = '<div class="pr-scope"><div class="relative mx-auto aspect-square w-full max-w-sm sm:max-w-md" aria-hidden="true"><div class="absolute inset-0 rounded-full bg-gradient-to-br from-brand-100 via-brand-100/60 to-transparent"></div>'
        . '<svg viewBox="0 0 400 400" class="absolute inset-0 h-full w-full"><g stroke="var(--brand-blue-700)" stroke-opacity="0.35" stroke-width="1.5" fill="none">' . implode('', array_map($line, $lines)) . '</g><g fill="var(--brand-blue-700)">';
    foreach ($dots as $d) $h .= '<circle cx="' . $d[0] . '" cy="' . $d[1] . '" r="' . $d[2] . '"/>';
    $h .= '</g></svg>'
        . '<div class="absolute left-2 top-6 flex items-center gap-2 rounded-xl bg-card px-3 py-2 shadow-lg sm:left-4 sm:top-10">' . pr_icon('BarChart3', 'h-4 w-4 text-brand-700') . '<span class="text-xs font-medium text-primary">Tren Riset</span></div>'
        . '<div class="absolute right-0 top-1/3 flex items-center gap-2 rounded-xl bg-card px-3 py-2 shadow-lg sm:-right-2">' . pr_icon('GraduationCap', 'h-4 w-4 text-brand-700') . '<span class="text-xs font-medium text-primary">Akademik</span></div>'
        . '<div class="absolute bottom-8 left-0 flex items-center gap-2 rounded-xl bg-card px-3 py-2 shadow-lg sm:-left-4">' . pr_icon('Cpu', 'h-4 w-4 text-brand-700') . '<span class="text-xs font-medium text-primary">Kecerdasan Buatan</span></div>'
        . '<div class="absolute bottom-2 right-6 flex items-center gap-2 rounded-xl bg-brand-700 px-3 py-2 shadow-lg sm:right-10">' . pr_icon('Sparkles', 'h-4 w-4 text-white') . '<span class="text-xs font-medium text-white">Terkurasi</span></div></div></div>';
    return $h;
}

function pr_render_kpi() {
    $s = pr_home_stats();
    $cards = [['Total Riset', $s['totalPapers'], 'FileStack', 'gradient-card-blue'], ['Riset Indonesia', $s['localPapers'], 'Flag', 'gradient-card-teal'], ['Institusi Terlibat', $s['institutionCount'], 'Building2', 'gradient-card-indigo'], ['Ringkasan Terkurasi', $s['curatedSummaryCount'], 'Sparkles', 'gradient-card-blue']];
    $h = '<div class="pr-scope"><div class="grid grid-cols-2 gap-4 sm:grid-cols-4">';
    foreach ($cards as $c) $h .= '<div class="' . $c[3] . ' rounded-2xl p-5 text-white shadow-lg transition hover:-translate-y-0.5 hover:shadow-xl"><div class="flex h-10 w-10 items-center justify-center rounded-full bg-white/15">' . pr_icon($c[2], 'h-5 w-5 text-white') . '</div><p class="mt-3 text-2xl font-bold">' . pr_num($c[1]) . '</p><p class="mt-1 text-xs text-white/80">' . pr_e($c[0]) . '</p></div>';
    return $h . '</div></div>';
}

function pr_render_home_list($which) {
    $s = pr_home_stats();
    $items = pr_card_items($which === 'popular' ? $s['popularIds'] : $s['recentIds']);
    if (!$items) return '<div class="pr-scope"><p class="text-sm text-secondary">Belum ada riset yang tayang.</p></div>';
    return '<div class="pr-scope">' . pr_card_grid($items) . '</div>';
}

// ---------------------------------------------------------------- halaman: detail riset
function pr_render_paper($data, $lang, $tab) {
    $p = $data;
    $secondary = null;
    foreach ($p['titles'] as $t) if (!$t['isPrimary']) { $secondary = $t; break; }
    $retracted = ($p['relevance']['publishedStatus'] ?? null) === 'retracted';
    $defaultTab = $p['file'] ? 'jurnal' : 'data';
    $tab = in_array($tab, ['ringkasan', 'jurnal', 'data'], true) ? $tab : $defaultTab;
    $id = $p['id']; $langQs = $lang === 'en' ? '&lang=en' : '';
    $idLabels = ['doi' => 'DOI', 'arxiv_id' => 'arXiv', 'openalex_id' => 'OpenAlex'];
    $idUrl = function ($t, $v) { return $t === 'doi' ? 'https://doi.org/' . $v : ($t === 'arxiv_id' ? 'https://arxiv.org/abs/' . $v : null); };
    $relLabels = ['superseded_by' => 'Digantikan oleh', 'extended_by' => 'Diperluas oleh', 'follow_up_same_author' => 'Studi lanjutan (penulis sama)'];
    $short = mb_strlen($p['title'], 'UTF-8') > 60 ? mb_substr($p['title'], 0, 60, 'UTF-8') . '...' : $p['title'];

    $h = '<div class="pr-scope bg-page text-primary"><div class="mx-auto max-w-4xl px-4 py-8 sm:px-6">';
    $h .= '<nav class="mb-4 text-sm text-secondary"><a href="' . pr_a(pr_url_katalog()) . '" class="font-medium hover:text-brand-700">← Kembali ke Archive</a><span class="mx-1.5">/</span><span class="text-primary">' . pr_e($short) . '</span></nav>';
    if ($retracted) $h .= pr_retracted_banner($p['relevance']['publishedReasoning'] ?? null);
    $h .= '<h1 class="text-2xl font-bold leading-tight text-brand-900 sm:text-3xl">' . pr_origin_flag($p['origin']) . ' ' . pr_e($p['title']) . '</h1>';
    if ($secondary) $h .= '<p class="mt-1 text-base italic text-secondary">' . pr_e($secondary['title']) . '</p>';

    $names = array_map(function ($a) { return $a['name']; }, $p['authors']);
    $h .= '<div class="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-secondary"><span>' . ($names ? '<span class="cursor-default text-primary">' . pr_e(implode(', ', $names)) . '</span>' : 'Penulis tidak diketahui') . '</span>';
    if ($p['venue']) $h .= '<span>' . pr_e($p['venue']['displayName']) . '</span>'; elseif ($p['publicationType'] === 'own_publication') $h .= '<span>Pusat Riset AI Indonesia</span>';
    $h .= pr_publication_badge($p['publicationType']);
    if ($p['sjrQuartile']) $h .= pr_quartile_badge($p['sjrQuartile']);
    if ($p['publishedDate']) $h .= '<span>' . pr_e(pr_date_id($p['publishedDate'])) . '</span>';
    if ($p['affiliationCountries']) $h .= '<span>Afiliasi: ' . pr_e(implode(', ', $p['affiliationCountries'])) . '</span>';
    $h .= '</div>';
    if ($p['affiliationInferred']) $h .= '<p class="mt-1 text-xs text-muted-warm">⚑ Afiliasi institusi merupakan perkiraan (belum dikonfirmasi penulis)</p>';

    $ps = $p['relevance']['publishedStatus'] ?? null;
    if (($ps && $ps !== 'retracted') || $p['isFoundational']) {
        $h .= '<div class="mt-5 rounded-[14px] border border-warm bg-card-alt p-4">' . pr_relevance_badge($ps, 'lg');
        if (!empty($p['relevance']['publishedReasoning'])) $h .= '<p class="mt-2 text-sm text-primary">' . pr_e($p['relevance']['publishedReasoning']) . '</p>';
        $h .= '</div>';
    }
    if ($p['successors']) {
        $h .= '<div class="mt-6 space-y-3"><h2 class="text-sm font-semibold text-primary">Riset Penerus</h2>';
        foreach ($p['successors'] as $s) {
            $h .= '<div class="rounded-[14px] border border-warm bg-card p-4 shadow-[var(--shadow-card)]"><p class="text-xs font-medium text-brand-700">' . pr_e($relLabels[$s['relationType']] ?? $s['relationType']) . '</p>'
                . '<a href="' . pr_a(pr_url_paper($s['paper']['id'])) . '" class="mt-1 block font-medium text-primary hover:text-brand-700 hover:underline">' . pr_e($s['paper']['title']) . ' ' . ($s['paper']['publishedDate'] ? '(' . pr_year($s['paper']['publishedDate']) . ')' : '') . '</a>'
                . ($s['reasoningText'] ? '<p class="mt-1 text-sm text-secondary">' . pr_e($s['reasoningText']) . '</p>' : '') . '</div>';
        }
        $h .= '</div>';
    }
    if ($p['related']) {
        $h .= '<div class="mt-6 space-y-3"><h2 class="text-sm font-semibold text-primary">Riset Serupa</h2>';
        foreach ($p['related'] as $r) {
            $h .= '<div class="rounded-[14px] border border-warm bg-card-alt p-4"><a href="' . pr_a(pr_url_paper($r['paper']['id'])) . '" class="block font-medium text-primary hover:text-brand-700 hover:underline">' . pr_e($r['paper']['title']) . ' ' . ($r['paper']['publishedDate'] ? '(' . pr_year($r['paper']['publishedDate']) . ')' : '') . '</a>'
                . ($r['reasoningText'] ? '<p class="mt-1 text-sm text-secondary">' . pr_e($r['reasoningText']) . '</p>' : '') . '</div>';
        }
        $h .= '</div>';
    }

    $tabLink = function ($key, $label, $qs) use ($tab, $id) {
        $on = $tab === $key;
        return '<a href="' . pr_a(pr_url_paper($id, $qs)) . '" class="border-b-2 pb-3 text-sm font-medium ' . ($on ? 'border-brand-700 text-brand-700' : 'border-transparent text-secondary hover:text-primary') . '">' . $label . '</a>';
    };
    $h .= '<div class="mt-8 border-b border-warm"><nav class="flex gap-6">' . $tabLink('data', 'Data Asli', 'tab=data' . $langQs) . $tabLink('ringkasan', 'Ringkasan &amp; Relevansi', 'tab=ringkasan' . $langQs) . ($p['file'] ? $tabLink('jurnal', 'Baca Jurnal', 'tab=jurnal') : '') . '</nav></div>';

    if ($tab === 'data') {
        $h .= '<div class="mt-6 space-y-6"><div><h2 class="mb-2 text-sm font-semibold text-primary">Abstrak</h2>';
        $h .= $p['abstract'] ? '<p class="whitespace-pre-line text-sm leading-relaxed text-primary">' . pr_e($p['abstract']) . '</p>' : '<p class="text-sm italic text-secondary">Abstrak tidak ditampilkan karena kebijakan lisensi — baca di sumber resmi →</p>';
        $h .= '</div>';
        if ($p['identifiers']) {
            $h .= '<div><h2 class="mb-2 text-sm font-semibold text-primary">Identifier</h2><ul class="space-y-1 text-sm">';
            foreach ($p['identifiers'] as $i) {
                $u = $idUrl($i['idType'], $i['idValue']);
                $h .= '<li><span class="text-secondary">' . pr_e($idLabels[$i['idType']] ?? $i['idType']) . ': </span>' . ($u ? '<a href="' . pr_a($u) . '" target="_blank" rel="noopener noreferrer" class="text-brand-700 hover:underline">' . pr_e($i['idValue']) . '</a>' : '<span>' . pr_e($i['idValue']) . '</span>') . '</li>';
            }
            $h .= '</ul></div>';
        }
        $h .= '<div class="flex flex-wrap gap-3">';
        if ($p['file']) $h .= '<a href="' . pr_a(home_url('/riset/' . $id . '/unduh')) . '" class="rounded-md bg-brand-700 px-4 py-2 text-sm font-medium text-white hover:bg-brand-900">Unduh PDF</a>';
        else {
            $first = $p['identifiers'][0] ?? null;
            $src = $p['canonicalUrl'] ?: ($first ? $idUrl($first['idType'], $first['idValue']) : null);
            if ($src) $h .= '<a href="' . pr_a($src) . '" target="_blank" rel="noopener noreferrer" class="rounded-md bg-brand-700 px-4 py-2 text-sm font-medium text-white hover:bg-brand-900">Buka Sumber Resmi</a>';
        }
        if ($p['publicationType'] !== 'own_publication') $h .= '<a href="' . pr_a(home_url('/riset/' . $id . '/bibtex')) . '" download="' . pr_a($id) . '.bib" class="rounded-md border border-warm px-4 py-2 text-sm font-medium text-primary hover:bg-card-alt">Ekspor BibTeX</a>';
        $h .= '</div>';
        if (count($p['versions']) > 1) {
            $h .= '<div><h2 class="mb-2 text-sm font-semibold text-primary">Riwayat Versi</h2><ul class="space-y-2 border-l-2 border-warm pl-4">';
            foreach ($p['versions'] as $v) $h .= '<li class="text-sm"><span class="font-medium text-primary">v' . (int) $v['versionNumber'] . '</span>' . ($v['versionDate'] ? '<span class="text-secondary"> · ' . pr_e(pr_date_id($v['versionDate'])) . '</span>' : '') . ($v['changedSummary'] ? '<p class="text-secondary">' . pr_e($v['changedSummary']) . '</p>' : '') . '</li>';
            $h .= '</ul></div>';
        }
        $h .= '</div>';
    } elseif ($tab === 'jurnal' && $p['file']) {
        $h .= '<div class="mt-6"><p class="text-sm text-secondary">' . pr_e($p['file']['originalName']) . ' · <a class="text-brand-700 hover:underline" href="' . pr_a(home_url('/riset/' . $id . '/unduh')) . '">Unduh PDF</a></p></div>';
    } else {
        $tabq = 'tab=ringkasan';
        $h .= '<div class="mt-6 space-y-6"><div class="flex gap-2 text-sm">'
            . '<a href="' . pr_a(pr_url_paper($id, $tabq)) . '" class="rounded px-3 py-1 ' . ($lang === 'id' ? 'bg-brand-700 text-white' : 'border border-warm text-secondary hover:text-primary') . '">Indonesia</a>'
            . '<a href="' . pr_a(pr_url_paper($id, $tabq . '&lang=en')) . '" class="rounded px-3 py-1 ' . ($lang === 'en' ? 'bg-brand-700 text-white' : 'border border-warm text-secondary hover:text-primary') . '">English</a></div>';
        if (!empty($p['summary']['content'])) {
            $h .= '<div><h2 class="mb-2 text-sm font-semibold text-primary">Ringkasan</h2><div class="summary-content text-sm text-primary">' . wp_kses_post($p['summary']['content']) . '</div></div>'
                . '<p class="text-xs text-muted-warm">' . ($p['summary']['provenance'] === 'from_fulltext' ? 'Dibuat dari teks lengkap' : 'Dibuat dari abstrak') . ' — ringkasan dibantu AI, ditinjau editor sebelum tayang.</p>';
        } else $h .= '<p class="text-sm italic text-secondary">Ringkasan dalam bahasa ini belum tersedia.</p>';
        $h .= '<div class="border-t border-warm pt-4">' . pr_dispute_form($p['id']) . '</div></div>';
    }
    return $h . '</div></div>';
}

/** Tautan + formulir sanggahan (tanpa JS berat: <details> + POST ke REST lewat pr.js). */
function pr_dispute_form($paperId) {
    $types = [['relevance_badge', 'Badge relevansi tidak tepat'], ['abstract_policy', 'Kebijakan abstrak/lisensi salah'], ['summary_accuracy', 'Ringkasan tidak akurat'], ['other', 'Lainnya']];
    $o = '';
    foreach ($types as $t) $o .= '<option value="' . $t[0] . '">' . pr_e($t[1]) . '</option>';
    return '<details class="pr-dispute"><summary class="cursor-pointer list-none text-sm text-brand-700 hover:underline">Keberatan dengan konten ini?</summary>'
        . '<form class="mt-3 w-full max-w-md space-y-3 rounded-[14px] border border-warm bg-card p-5 text-sm text-primary shadow-xl" data-paper="' . pr_a($paperId) . '" data-endpoint="' . pr_a(rest_url('pusatriset/v1/disputes')) . '">'
        . '<h3 class="text-lg font-semibold text-primary">Ajukan Sanggahan</h3>'
        . '<div><label class="mb-1 block font-medium">Jenis sanggahan</label><select name="disputeType" required class="w-full rounded border border-warm bg-card px-3 py-2">' . $o . '</select></div>'
        . '<div><label class="mb-1 block font-medium">Nama (opsional)</label><input name="name" class="w-full rounded border border-warm bg-card px-3 py-2"></div>'
        . '<div><label class="mb-1 block font-medium">Email (opsional)</label><input name="email" type="email" class="w-full rounded border border-warm bg-card px-3 py-2"></div>'
        . '<div><label class="mb-1 block font-medium">Penjelasan</label><textarea name="argument" required rows="4" class="w-full rounded border border-warm bg-card px-3 py-2"></textarea></div>'
        . '<div class="flex items-center justify-end gap-2 pt-2"><span class="pr-dispute-msg mr-auto text-xs text-secondary"></span><button type="submit" class="rounded-md bg-brand-700 px-4 py-2 text-white hover:bg-brand-900 disabled:opacity-50">Kirim</button></div></form></details>';
}

/** Form cari beranda (bagian fungsional hero): GET ke Archive dengan parameter q. */
function pr_render_cari() {
    return '<div class="pr-scope"><form action="' . pr_e(pr_url_katalog()) . '" method="GET" class="mx-auto flex max-w-xl gap-2 lg:mx-0">'
        . '<div class="relative flex-1">' . pr_icon('Search', 'pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-warm')
        . '<input type="text" name="q" placeholder="Cari judul, topik, atau kata kunci riset..." class="w-full rounded-md border border-warm bg-card py-3 pl-10 pr-4 text-sm shadow-[var(--shadow-card)] focus:border-brand-700 focus:outline-none">'
        . '</div><button type="submit" class="rounded-md bg-brand-700 px-6 py-3 text-sm font-medium text-white hover:bg-brand-900">Cari</button></form></div>';
}
