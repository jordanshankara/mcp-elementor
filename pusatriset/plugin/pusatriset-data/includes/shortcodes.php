<?php
/**
 * Shortcode untuk widget Shortcode Elementor Free:
 *  [pr_katalog hero="0"]  [pr_dashboard hero="0"]  [pr_kpi]  [pr_terbaru]  [pr_populer]  [pr_hero_art]  [pr_cari]
 * hero="0" (default) = judul/hero dibuat native di Elementor; hero="1" = hero bawaan plugin.
 */
if (!defined('ABSPATH')) exit;

add_action('init', function () {
    $wrap = function ($fn) {
        return function ($atts) use ($fn) {
            pr_enqueue();
            $a = shortcode_atts(['hero' => '0'], $atts);
            return $fn($a['hero'] === '1');
        };
    };
    add_shortcode('pr_katalog', $wrap(function ($hero) { return pr_render_catalog($hero); }));
    add_shortcode('pr_dashboard', $wrap(function ($hero) { return pr_render_dashboard($hero); }));
    add_shortcode('pr_kpi', $wrap(function () { return pr_render_kpi(); }));
    add_shortcode('pr_terbaru', $wrap(function () { return pr_render_home_list('recent'); }));
    add_shortcode('pr_populer', $wrap(function () { return pr_render_home_list('popular'); }));
    add_shortcode('pr_cari', $wrap(function () { return pr_render_cari(); }));
    add_shortcode('pr_hero_art', $wrap(function () { return pr_render_hero_art(); }));
});
