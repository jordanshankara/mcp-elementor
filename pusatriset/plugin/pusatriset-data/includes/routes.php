<?php
/** Rute /riset/<uuid>[/bibtex|/unduh], aset CSS/JS terskop, dan tata letak Astra. */
if (!defined('ABSPATH')) exit;

function pr_add_rewrite_rules() {
    add_rewrite_rule('^riset/([0-9a-fA-F-]{36})/(bibtex|unduh)/?$', 'index.php?pr_paper=$matches[1]&pr_action=$matches[2]', 'top');
    add_rewrite_rule('^riset/([0-9a-fA-F-]{36})/?$', 'index.php?pr_paper=$matches[1]', 'top');
}
add_action('init', 'pr_add_rewrite_rules');

add_filter('query_vars', function ($v) { $v[] = 'pr_paper'; $v[] = 'pr_action'; return $v; });

// Jangan "membenarkan" URL (mis. menambah/menghapus slash atau menebak slug) untuk halaman riset.
add_filter('redirect_canonical', function ($url) { return get_query_var('pr_paper') ? false : $url; });

function pr_register_assets() {
    $css = PR_DIR . 'assets/css/pr.css';
    wp_register_style('pusatriset-data', PR_URL . 'assets/css/pr.css', [], file_exists($css) ? filemtime($css) : PR_VERSION);
    $js = PR_DIR . 'assets/js/pr.js';
    wp_register_script('pusatriset-data', PR_URL . 'assets/js/pr.js', [], file_exists($js) ? filemtime($js) : PR_VERSION, true);
}
add_action('wp_enqueue_scripts', 'pr_register_assets', 5);

function pr_enqueue() { pr_register_assets(); wp_enqueue_style('pusatriset-data'); wp_enqueue_script('pusatriset-data'); }

add_action('template_redirect', function () {
    $id = get_query_var('pr_paper');
    if (!$id) return;
    $id = strtolower($id);
    $action = get_query_var('pr_action');
    $lang = (isset($_GET['lang']) && $_GET['lang'] === 'en') ? 'en' : 'id';
    $tab = isset($_GET['tab']) ? sanitize_key($_GET['tab']) : '';

    $res = pr_get_paper_detail($id, $lang);
    if ($res['type'] === 'redirect') {
        $suffix = $action ? '/' . $action : '';
        wp_redirect(pr_url_paper($res['survivingId']) . $suffix, 301); exit;
    }
    if ($res['type'] === 'not_found') { global $wp_query; $wp_query->set_404(); status_header(404); nocache_headers(); return; }

    if ($action === 'bibtex') {
        $b = pr_get_bibtex($id);
        if (!$b) return;
        nocache_headers();
        header('Content-Type: application/x-bibtex; charset=utf-8');
        header('Content-Disposition: attachment; filename="' . $id . '.bib"');
        echo $b; exit;
    }
    if ($action === 'unduh') { wp_redirect(pr_url_paper($id)); exit; } // paper_files = 0 pada data awal

    $GLOBALS['pr_current'] = ['data' => $res['data'], 'lang' => $lang, 'tab' => $tab];
    pr_enqueue();
    status_header(200);
    add_filter('pre_get_document_title', function () { return $GLOBALS['pr_current']['data']['title'] . ' – Pusat Riset AI Indonesia'; });
    add_filter('document_title_parts', function ($p) { return $p; });
    add_filter('body_class', function ($c) { $c[] = 'pr-page'; return $c; });
    add_filter('astra_page_layout', function () { return 'no-sidebar'; });
    add_filter('astra_get_content_layout', function () { return 'page-builder'; });
    add_filter('astra_the_title_enabled', '__return_false');
    add_action('wp_head', function () {
        $d = $GLOBALS['pr_current']['data'];
        $desc = $d['abstract'] ? wp_trim_words($d['abstract'], 40) : $d['title'];
        echo '<meta name="description" content="' . esc_attr($desc) . '">' . "\n";
    });

    get_header();
    echo pr_render_paper($GLOBALS['pr_current']['data'], $lang, $tab);
    get_footer();
    exit;
});

// CSS (termasuk @font-face Geist) dimuat di seluruh situs agar bagian native Elementor memakai font yang sama.
// Semua aturan Tailwind di dalamnya terskop ke .pr-scope, jadi tidak mengubah tampilan di luar komponen plugin.
add_action('wp_enqueue_scripts', function () { wp_enqueue_style('pusatriset-data'); }, 20);

// Desain lama menampilkan menu penuh mulai 640px (Tailwind sm); Astra bawaan baru memakai hamburger di bawah 921px.
add_filter('astra_header_break_point', function () { return 640; });
