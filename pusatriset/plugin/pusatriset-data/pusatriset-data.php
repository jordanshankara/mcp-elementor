<?php
/**
 * Plugin Name: PusatRiset Data
 * Description: Katalog riset AI (35 ribuan paper) di tabel khusus (bukan post): impor batch, pencarian FULLTEXT + sinonim, filter, halaman detail /riset/<id>, dashboard tren, BibTeX, sanggahan. Tampilan identik dengan aplikasi PusatRiset.ai lama.
 * Version: 0.1.4
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author: Asosiasi AI Indonesia
 * License: GPLv2 or later
 * Text Domain: pusatriset-data
 */

if (!defined('ABSPATH')) exit;

define('PR_VERSION', '0.1.4');
define('PR_DB_VERSION', 1);
define('PR_DIR', plugin_dir_path(__FILE__));
define('PR_URL', plugin_dir_url(__FILE__));

require_once PR_DIR . 'includes/schema.php';
require_once PR_DIR . 'includes/query.php';
require_once PR_DIR . 'includes/render.php';
require_once PR_DIR . 'includes/import.php';
require_once PR_DIR . 'includes/rest.php';
require_once PR_DIR . 'includes/routes.php';
require_once PR_DIR . 'includes/shortcodes.php';

register_activation_hook(__FILE__, function () {
    pr_install_schema();
    pr_add_rewrite_rules();
    flush_rewrite_rules();
});
register_deactivation_hook(__FILE__, 'flush_rewrite_rules');

// Skema bermigrasi otomatis bila versi DB tertinggal (mis. setelah plugin diperbarui).
add_action('plugins_loaded', function () {
    if ((int) get_option('pr_db_version', 0) < PR_DB_VERSION) pr_install_schema();
});
