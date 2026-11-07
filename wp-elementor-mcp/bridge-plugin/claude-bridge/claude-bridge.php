<?php
/**
 * Plugin Name: Claude Bridge for Elementor
 * Description: Endpoint REST kecil supaya Claude Code (wp-elementor-mcp) bisa membaca/menulis data Elementor dengan aman: backup otomatis, deteksi bentrok edit, clear cache CSS, render check. Jalan di Elementor Free maupun Pro.
 * Version: 1.3.0
 * Requires at least: 5.6
 * Requires PHP: 7.4
 * Author: wp-elementor-mcp
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) exit;

define('CLAUDE_BRIDGE_VERSION', '1.3.0');
define('CLAUDE_BRIDGE_KEEP', 10); // jumlah backup per halaman

final class Claude_Bridge {
    const NS = 'claude/v1';

    public static function init() {
        add_action('rest_api_init', [__CLASS__, 'routes']);
    }

    private static function elementor() {
        return class_exists('\Elementor\Plugin') ? \Elementor\Plugin::$instance : null;
    }

    public static function routes() {
        $auth   = function () { return is_user_logged_in(); };
        $edit   = function ($r) { return current_user_can('edit_post', (int) $r['id']); };
        $admin  = function () { return current_user_can('manage_options'); };
        $id_arg = ['id' => ['validate_callback' => function ($v) { return is_numeric($v); }]];

        register_rest_route(self::NS, '/info', ['methods' => 'GET', 'permission_callback' => $auth, 'callback' => [__CLASS__, 'info']]);
        register_rest_route(self::NS, '/widgets', ['methods' => 'GET', 'permission_callback' => $auth, 'callback' => [__CLASS__, 'widgets']]);
        register_rest_route(self::NS, '/elementor/(?P<id>\d+)', [
            ['methods' => 'GET', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'get_data'], 'args' => $id_arg],
            ['methods' => 'POST', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'set_data'], 'args' => $id_arg],
        ]);
        register_rest_route(self::NS, '/elementor/(?P<id>\d+)/backups', [
            ['methods' => 'GET', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'list_backups'], 'args' => $id_arg],
            ['methods' => 'POST', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'restore_backup'], 'args' => $id_arg],
        ]);
        register_rest_route(self::NS, '/elementor/(?P<id>\d+)/render', ['methods' => 'GET', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'render'], 'args' => $id_arg]);
        register_rest_route(self::NS, '/elementor/(?P<id>\d+)/draft-copy', ['methods' => 'POST', 'permission_callback' => $edit, 'callback' => [__CLASS__, 'draft_copy'], 'args' => $id_arg]);
        register_rest_route(self::NS, '/kit', [
            ['methods' => 'GET', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'get_kit']],
            ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'set_kit']],
        ]);
        register_rest_route(self::NS, '/experiments', [
            ['methods' => 'GET', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'get_experiments']],
            ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'set_experiment']],
        ]);
        register_rest_route(self::NS, '/purge', ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'purge_all']]);
        register_rest_route(self::NS, '/custom-css', [
            ['methods' => 'GET', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'custom_css']],
            ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'custom_css']],
        ]);
        register_rest_route(self::NS, '/flush', ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'flush']]);
        register_rest_route(self::NS, '/theme-install', ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'theme_install']]);
        register_rest_route(self::NS, '/theme-option', [
            ['methods' => 'GET', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'get_theme_option']],
            ['methods' => 'POST', 'permission_callback' => $admin, 'callback' => [__CLASS__, 'set_theme_option']],
        ]);
    }

    // ---------------- pengaturan tema (Astra Customizer) ----------------
    // Opsi yang boleh dibaca/ditulis (whitelist). Astra menyimpan seluruh Customizer di option "astra-settings".
    private static function theme_option_allowed($name) {
        return in_array($name, ['astra-settings'], true);
    }

    public static function get_theme_option(\WP_REST_Request $r) {
        $name = (string) $r->get_param('name');
        if (!self::theme_option_allowed($name)) return new \WP_Error('claude_forbidden', 'Opsi tidak diizinkan.', ['status' => 403]);
        $v = get_option($name, []);
        $keys = $r->get_param('keys');
        if ($keys) {
            $want = array_filter(array_map('trim', explode(',', (string) $keys)));
            $v = array_intersect_key((array) $v, array_flip($want));
        }
        $mods = get_theme_mod('nav_menu_locations', []);
        return ['name' => $name, 'value' => $v, 'nav_menu_locations' => $mods];
    }

    // Body: { name:"astra-settings", merge:{...}, nav_menu_locations:{primary:3} }  (merge = array_replace di level atas)
    public static function set_theme_option(\WP_REST_Request $r) {
        $b = (array) $r->get_json_params();
        $name = (string) ($b['name'] ?? 'astra-settings');
        if (!self::theme_option_allowed($name)) return new \WP_Error('claude_forbidden', 'Opsi tidak diizinkan.', ['status' => 403]);
        $cur = (array) get_option($name, []);
        update_option('claude_bridge_backup_' . $name, ['at' => current_time('mysql'), 'value' => $cur], false); // backup 1 versi terakhir
        if (!empty($b['merge']) && is_array($b['merge'])) {
            $cur = array_replace($cur, $b['merge']);
            update_option($name, $cur);
        }
        if (!empty($b['nav_menu_locations']) && is_array($b['nav_menu_locations'])) {
            $locs = (array) get_theme_mod('nav_menu_locations', []);
            foreach ($b['nav_menu_locations'] as $loc => $menu) $locs[sanitize_key($loc)] = (int) $menu;
            set_theme_mod('nav_menu_locations', $locs);
        }
        // theme_mods yang diizinkan (logo situs, lokasi menu)
        if (!empty($b['theme_mods']) && is_array($b['theme_mods'])) {
            foreach (['custom_logo' => 'int', 'nav_menu_locations' => 'array'] as $k => $t) {
                if (!array_key_exists($k, $b['theme_mods'])) continue;
                $v = $b['theme_mods'][$k];
                if ($t === 'int') set_theme_mod($k, (int) $v);
                elseif (is_array($v)) { $locs = (array) get_theme_mod($k, []); foreach ($v as $loc => $menu) $locs[sanitize_key($loc)] = (int) $menu; set_theme_mod($k, $locs); }
            }
        }
        if (function_exists('astra_clear_all_assets_cache')) astra_clear_all_assets_cache();
        if (function_exists('wp_cache_flush')) wp_cache_flush();
        return ['ok' => true, 'name' => $name, 'keys' => array_keys((array) ($b['merge'] ?? []))];
    }

    // Additional CSS (Customizer) milik tema aktif. GET = baca, POST {css, append:true|false}.
    public static function custom_css(\WP_REST_Request $r) {
        if ($r->get_method() === 'GET') return ['css' => wp_get_custom_css()];
        $b = (array) $r->get_json_params();
        $css = (string) ($b['css'] ?? '');
        if (!empty($b['append'])) $css = wp_get_custom_css() . "\n" . $css;
        $res = wp_update_custom_css_post($css);
        if (is_wp_error($res)) return $res;
        return ['ok' => true, 'bytes' => strlen($css)];
    }

    // Pasang (dan opsional aktifkan) tema dari wordpress.org. REST inti tidak bisa memasang tema. Hanya slug whitelist.
    // Body: { slug:"astra", activate:true }
    public static function theme_install(\WP_REST_Request $r) {
        $b = (array) $r->get_json_params();
        $slug = sanitize_key((string) ($b['slug'] ?? ''));
        if (!in_array($slug, ['astra'], true)) return new \WP_Error('claude_forbidden', 'Tema tidak diizinkan (whitelist: astra).', ['status' => 403]);
        if (!current_user_can('install_themes') || !current_user_can('switch_themes')) return new \WP_Error('claude_forbidden', 'Akun tidak boleh memasang/mengganti tema.', ['status' => 403]);
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/misc.php';
        require_once ABSPATH . 'wp-admin/includes/theme.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
        if (!wp_get_theme($slug)->exists()) {
            $api = themes_api('theme_information', ['slug' => $slug, 'fields' => ['sections' => false]]);
            if (is_wp_error($api)) return $api;
            $skin = new \WP_Ajax_Upgrader_Skin();
            $up = new \Theme_Upgrader($skin);
            $res = $up->install($api->download_link);
            if (is_wp_error($res)) return $res;
            if (!$res || !wp_get_theme($slug)->exists()) return new \WP_Error('claude_install_failed', 'Instal tema gagal (izin berkas hosting?).', ['status' => 500]);
        }
        if (!empty($b['activate'])) switch_theme($slug);
        return ['ok' => true, 'slug' => $slug, 'active' => get_stylesheet() === $slug];
    }

    // Flush permalink + semua cache (setelah mengubah struktur situs).
    public static function flush() {
        flush_rewrite_rules();
        self::purge_all();
        if (function_exists('astra_clear_all_assets_cache')) astra_clear_all_assets_cache();
        return ['ok' => true];
    }

    // ---------------- info ----------------
    public static function info() {
        global $wp_version;
        $el = self::elementor();
        $active = (array) get_option('active_plugins', []);
        $has = function ($needle) use ($active) { foreach ($active as $p) if (strpos($p, $needle) === 0) return true; return false; };
        $cache = [];
        foreach (['litespeed-cache' => 'LiteSpeed Cache', 'wp-rocket' => 'WP Rocket', 'autoptimize' => 'Autoptimize', 'w3-total-cache' => 'W3 Total Cache', 'wp-super-cache' => 'WP Super Cache', 'wp-fastest-cache' => 'WP Fastest Cache', 'sg-cachepress' => 'SiteGround Optimizer', 'cloudflare' => 'Cloudflare', 'perfmatters' => 'Perfmatters'] as $slug => $name) {
            if ($has($slug . '/')) $cache[] = $name;
        }
        $user = wp_get_current_user();
        return [
            'bridge'        => CLAUDE_BRIDGE_VERSION,
            'site_url'      => home_url('/'),
            'wp'            => $wp_version,
            'php'           => PHP_VERSION,
            'env'           => function_exists('wp_get_environment_type') ? wp_get_environment_type() : 'production',
            'elementor'     => defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : null,
            'elementor_pro' => defined('ELEMENTOR_PRO_VERSION') ? ELEMENTOR_PRO_VERSION : null,
            'theme'         => wp_get_theme()->get('Name'),
            'cache_plugins' => $cache,
            'multilingual'  => $has('sitepress-multilingual-cms/') ? 'WPML' : ($has('polylang') ? 'Polylang' : null),
            'kit_id'        => $el && isset($el->kits_manager) ? (int) $el->kits_manager->get_active_id() : null,
            'user'          => ['login' => $user->user_login, 'roles' => array_values($user->roles), 'can_manage_options' => current_user_can('manage_options'), 'can_install_plugins' => current_user_can('install_plugins')],
            'perf_features' => self::perf_features(),
        ];
    }

    private static function perf_features() {
        $el = self::elementor();
        if (!$el || !isset($el->experiments)) return null;
        $out = [];
        foreach (['e_optimized_markup', 'e_font_icon_svg', 'additional_custom_breakpoints', 'e_lazyload', 'e_element_cache', 'e_local_google_fonts', 'container', 'e_atomic_elements', 'e_opt_in_v4_page'] as $f) {
            if ($el->experiments->get_features($f)) $out[$f] = $el->experiments->is_feature_active($f) ? 'active' : 'inactive';
        }
        // setting performa non-experiment (Elementor > Settings > Performance)
        $out['css_print_method']      = get_option('elementor_css_print_method', 'external');
        $out['optimized_image_loading'] = get_option('elementor_optimized_image_loading', '1');
        $out['optimized_gutenberg_loading'] = get_option('elementor_optimized_gutenberg_loading', '1');
        $out['element_cache_ttl']     = get_option('elementor_element_cache_ttl', '');
        $out['font_display']          = get_option('elementor_font_display', 'auto');
        $out['google_font']           = get_option('elementor_google_font', '1');
        return $out;
    }

    public static function widgets() {
        $el = self::elementor();
        if (!$el) return new WP_Error('no_elementor', 'Elementor tidak aktif di situs ini.', ['status' => 409]);
        // Elementor Free mendaftarkan widget Pro sebagai placeholder promosi (tampil sebagai iklan, render kosong).
        // Pisahkan supaya engine tidak pernah menyisipkan widget "kosong" di situs Free.
        $real = []; $promo = [];
        foreach ($el->widgets_manager->get_widget_types() as $name => $w) {
            $cls = get_class($w);
            if (stripos($cls, 'Promotion') !== false || (method_exists($w, 'is_pro') && $w->is_pro() && !defined('ELEMENTOR_PRO_VERSION'))) $promo[] = $name;
            else $real[] = $name;
        }
        return [
            'widgets'  => $real,
            'promo'    => $promo,
            'elements' => array_values(array_keys($el->elements_manager->get_element_types())),
            'pro'      => defined('ELEMENTOR_PRO_VERSION'),
        ];
    }

    // ---------------- data ----------------
    private static function raw($id) {
        $raw = get_post_meta($id, '_elementor_data', true);
        if (is_array($raw)) $raw = wp_json_encode($raw);
        return is_string($raw) ? $raw : '';
    }

    public static function get_data($r) {
        $id = (int) $r['id'];
        $post = get_post($id);
        if (!$post) return new WP_Error('not_found', 'Post tidak ditemukan.', ['status' => 404]);
        $raw = self::raw($id);
        return [
            'id'            => $id,
            'type'          => $post->post_type,
            'status'        => $post->post_status,
            'title'         => get_the_title($id),
            'link'          => get_permalink($id),
            'modified'      => $post->post_modified_gmt,
            'edit_mode'     => get_post_meta($id, '_elementor_edit_mode', true),
            'template_type' => get_post_meta($id, '_elementor_template_type', true),
            'page_settings' => get_post_meta($id, '_elementor_page_settings', true) ?: new stdClass(),
            'css'           => (function ($m) { return is_array($m) ? ['status' => $m['status'] ?? '', 'time' => $m['time'] ?? 0] : null; })(get_post_meta($id, '_elementor_css', true)),
            'hash'          => md5($raw),
            'data'          => $raw,
        ];
    }

    /** Tulis _elementor_data. Body: { data: string(JSON), hash: string, reason?: string, page_settings?: object } */
    public static function set_data($r) {
        $id = (int) $r['id'];
        if (!get_post($id)) return new WP_Error('not_found', 'Post tidak ditemukan.', ['status' => 404]);
        $p = $r->get_json_params();
        $data = isset($p['data']) ? $p['data'] : null;
        if (is_array($data)) $data = wp_json_encode($data);
        if (!is_string($data) || !is_array(json_decode($data, true))) return new WP_Error('bad_data', '`data` harus string JSON array.', ['status' => 400]);

        $current = self::raw($id);
        if (!isset($p['hash']) || $p['hash'] !== md5($current)) {
            return new WP_Error('conflict', 'Halaman berubah sejak terakhir dibaca (mungkin sedang diedit orang lain). Baca ulang dulu.', ['status' => 409, 'current_hash' => md5($current)]);
        }
        $bk = self::backup($id, $current, isset($p['reason']) ? (string) $p['reason'] : '');
        self::write($id, $data, isset($p['page_settings']) ? $p['page_settings'] : null);
        return ['ok' => true, 'hash' => md5(self::raw($id)), 'backup' => $bk];
    }

    private static function write($id, $json, $page_settings = null) {
        update_post_meta($id, '_elementor_data', wp_slash($json));
        update_post_meta($id, '_elementor_edit_mode', 'builder');
        if (!get_post_meta($id, '_elementor_version', true) && defined('ELEMENTOR_VERSION')) update_post_meta($id, '_elementor_version', ELEMENTOR_VERSION);
        if (!get_post_meta($id, '_elementor_template_type', true)) update_post_meta($id, '_elementor_template_type', get_post_type($id) === 'page' ? 'wp-page' : 'wp-post');
        if (is_array($page_settings)) update_post_meta($id, '_elementor_page_settings', $page_settings);
        self::revision($id);
        self::purge($id);
    }

    /** Revisi WordPress supaya bisa di-undo dari wp-admin juga. Best-effort. */
    private static function revision($id) {
        if (!function_exists('wp_save_post_revision') || !wp_revisions_enabled(get_post($id))) return;
        $force = function () { return true; };
        add_filter('wp_save_post_revision_post_has_changed', $force, 99);
        $rev = wp_save_post_revision($id);
        remove_filter('wp_save_post_revision_post_has_changed', $force, 99);
        if ($rev && !is_wp_error($rev)) {
            foreach (['_elementor_data', '_elementor_edit_mode', '_elementor_page_settings', '_elementor_version', '_elementor_template_type'] as $k) {
                $v = get_post_meta($id, $k, true);
                if ($v !== '') update_metadata('post', $rev, $k, wp_slash($v));
            }
        }
    }

    private static function purge($id) {
        delete_post_meta($id, '_elementor_css');
        delete_post_meta($id, '_elementor_element_cache');
        delete_post_meta($id, '_elementor_page_assets');
        if (class_exists('\Elementor\Core\Files\CSS\Post')) {
            try { \Elementor\Core\Files\CSS\Post::create($id)->delete(); } catch (\Throwable $e) {}
        }
        clean_post_cache($id);
        // Elemen atomic (Editor V4): CSS style-nya di-cache terpisah; tanpa ini style baru tidak muncul.
        $raw = get_post_meta($id, '_elementor_data', true);
        $el = self::elementor();
        if ($el && is_string($raw) && strpos($raw, '"elType":"e-') !== false) {
            try { $el->files_manager->clear_cache(); } catch (\Throwable $e) {}
        }
        // plugin cache halaman populer
        do_action('litespeed_purge_post', $id);
        if (function_exists('rocket_clean_post')) rocket_clean_post($id);
        if (function_exists('w3tc_flush_post')) w3tc_flush_post($id);
        if (function_exists('wp_cache_post_change')) wp_cache_post_change($id);
        if (function_exists('sg_cachepress_purge_cache')) sg_cachepress_purge_cache(get_permalink($id));
        if (class_exists('WpFastestCache') && isset($GLOBALS['wp_fastest_cache']) && method_exists($GLOBALS['wp_fastest_cache'], 'singleDeleteCache')) $GLOBALS['wp_fastest_cache']->singleDeleteCache(false, $id);
    }

    public static function purge_all() {
        $el = self::elementor();
        if ($el) $el->files_manager->clear_cache();
        do_action('litespeed_purge_all');
        if (function_exists('rocket_clean_domain')) rocket_clean_domain();
        if (function_exists('w3tc_flush_all')) w3tc_flush_all();
        if (function_exists('wp_cache_clear_cache')) wp_cache_clear_cache();
        if (function_exists('sg_cachepress_purge_cache')) sg_cachepress_purge_cache();
        return ['ok' => true];
    }

    // ---------------- backups ----------------
    private static function backup($id, $raw, $reason) {
        $key = '_claude_bk_' . gmdate('YmdHis') . '_' . wp_generate_password(4, false, false);
        add_post_meta($id, $key, wp_slash(wp_json_encode(['t' => time(), 'reason' => $reason, 'hash' => md5($raw), 'data' => $raw])));
        // pangkas ke N terbaru
        $keys = self::backup_keys($id);
        foreach (array_slice($keys, CLAUDE_BRIDGE_KEEP) as $old) delete_post_meta($id, $old);
        return $key;
    }

    private static function backup_keys($id) {
        $keys = array_filter(array_keys(get_post_meta($id)), function ($k) { return strpos($k, '_claude_bk_') === 0; });
        rsort($keys);
        return array_values($keys);
    }

    public static function list_backups($r) {
        $id = (int) $r['id'];
        $out = [];
        foreach (self::backup_keys($id) as $k) {
            $b = json_decode(get_post_meta($id, $k, true), true);
            $out[] = ['key' => $k, 'time' => gmdate('c', $b['t'] ?? 0), 'reason' => $b['reason'] ?? '', 'hash' => $b['hash'] ?? '', 'bytes' => strlen($b['data'] ?? '')];
        }
        return $out;
    }

    /** Body: { key, hash } (hash = hash data saat ini, untuk cegah bentrok) */
    public static function restore_backup($r) {
        $id = (int) $r['id'];
        $p = $r->get_json_params();
        $key = isset($p['key']) ? (string) $p['key'] : '';
        if (strpos($key, '_claude_bk_') !== 0) return new WP_Error('bad_key', 'Key backup tidak valid.', ['status' => 400]);
        $b = json_decode(get_post_meta($id, $key, true), true);
        if (!$b || !isset($b['data'])) return new WP_Error('not_found', 'Backup tidak ditemukan.', ['status' => 404]);
        $current = self::raw($id);
        if (!isset($p['hash']) || $p['hash'] !== md5($current)) return new WP_Error('conflict', 'Halaman berubah sejak terakhir dibaca. Baca ulang dulu.', ['status' => 409]);
        $bk = self::backup($id, $current, 'before-restore ' . $key);
        self::write($id, $b['data']);
        return ['ok' => true, 'hash' => md5(self::raw($id)), 'backup' => $bk];
    }

    // ---------------- render ----------------
    /** HTML konten Elementor halaman ini (juga untuk draft), untuk verifikasi teks. */
    public static function render($r) {
        $id = (int) $r['id'];
        $el = self::elementor();
        if (!$el) return new WP_Error('no_elementor', 'Elementor tidak aktif.', ['status' => 409]);
        global $post;
        $post = get_post($id);
        setup_postdata($post);
        $html = '';
        // get_builder_content_for_display() kosong di konteks REST; get_builder_content() merender langsung.
        try { $html = (string) $el->frontend->get_builder_content($id, false); } catch (\Throwable $e) { $html = ''; }
        if ($html === '') { try { $html = (string) $el->frontend->get_builder_content_for_display($id, false); } catch (\Throwable $e) {} }
        wp_reset_postdata();
        return ['id' => $id, 'html' => $html];
    }

    // ---------------- draft copy ----------------
    public static function draft_copy($r) {
        $id = (int) $r['id'];
        $src = get_post($id);
        if (!$src) return new WP_Error('not_found', 'Post tidak ditemukan.', ['status' => 404]);
        $new = wp_insert_post(wp_slash([
            'post_type' => $src->post_type, 'post_status' => 'draft', 'post_title' => $src->post_title . ' (draft Claude)',
            'post_content' => $src->post_content, 'post_excerpt' => $src->post_excerpt, 'post_parent' => $src->post_parent, 'menu_order' => $src->menu_order,
        ]), true);
        if (is_wp_error($new)) return $new;
        foreach (get_post_meta($id) as $k => $vals) {
            if (strpos($k, '_claude_bk_') === 0 || in_array($k, ['_edit_lock', '_edit_last', '_elementor_css', '_elementor_element_cache', '_wp_old_slug'], true)) continue;
            foreach ($vals as $v) add_post_meta($new, $k, wp_slash(maybe_unserialize($v)));
        }
        update_post_meta($new, '_claude_draft_of', $id);
        return ['ok' => true, 'id' => $new, 'preview' => get_preview_post_link($new)];
    }

    // ---------------- kit (global colors/typography) ----------------
    public static function get_kit() {
        $el = self::elementor();
        if (!$el) return new WP_Error('no_elementor', 'Elementor tidak aktif.', ['status' => 409]);
        $kit = (int) $el->kits_manager->get_active_id();
        $s = get_post_meta($kit, '_elementor_page_settings', true) ?: [];
        return ['kit_id' => $kit, 'hash' => md5(wp_json_encode($s)), 'settings' => $s];
    }

    /** Body: { settings: object (merge dangkal), hash } */
    public static function set_kit($r) {
        $el = self::elementor();
        if (!$el) return new WP_Error('no_elementor', 'Elementor tidak aktif.', ['status' => 409]);
        $kit = (int) $el->kits_manager->get_active_id();
        $s = get_post_meta($kit, '_elementor_page_settings', true) ?: [];
        $p = $r->get_json_params();
        if (!isset($p['hash']) || $p['hash'] !== md5(wp_json_encode($s))) return new WP_Error('conflict', 'Kit berubah sejak dibaca. Baca ulang.', ['status' => 409]);
        if (!isset($p['settings']) || !is_array($p['settings'])) return new WP_Error('bad_data', '`settings` wajib object.', ['status' => 400]);
        add_post_meta($kit, '_claude_bk_' . gmdate('YmdHis') . '_kit', wp_slash(wp_json_encode(['t' => time(), 'reason' => 'kit', 'data' => wp_json_encode($s)])));
        foreach ($p['settings'] as $k => $v) { if ($v === null) unset($s[$k]); else $s[$k] = $v; }
        update_post_meta($kit, '_elementor_page_settings', $s);
        $el->files_manager->clear_cache();
        return ['ok' => true, 'hash' => md5(wp_json_encode($s))];
    }

    // ---------------- experiments / performance ----------------
    public static function get_experiments() { return self::perf_features(); }

    /** Body: { name, state: active|inactive|default } atau { option: elementor_css_print_method|..., value } */
    public static function set_experiment($r) {
        $p = $r->get_json_params();
        $allowed_opts = ['elementor_css_print_method', 'elementor_optimized_image_loading', 'elementor_optimized_gutenberg_loading', 'elementor_element_cache_ttl', 'elementor_font_display', 'elementor_google_font'];
        if (!empty($p['option'])) {
            if (!in_array($p['option'], $allowed_opts, true)) return new WP_Error('bad_option', 'Option tidak diizinkan.', ['status' => 400]);
            $old = get_option($p['option'], null);
            update_option($p['option'], $p['value']);
        } else {
            $name = isset($p['name']) ? sanitize_key($p['name']) : '';
            $state = isset($p['state']) ? $p['state'] : '';
            if (!$name || !in_array($state, ['active', 'inactive', 'default'], true)) return new WP_Error('bad_data', 'name & state (active|inactive|default) wajib.', ['status' => 400]);
            $old = get_option('elementor_experiment-' . $name, 'default');
            update_option('elementor_experiment-' . $name, $state);
        }
        $el = self::elementor();
        if ($el) $el->files_manager->clear_cache();
        return ['ok' => true, 'previous' => $old];
    }
}

Claude_Bridge::init();
