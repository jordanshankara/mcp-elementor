<?php
if (!defined('ABSPATH')) exit;

add_action('rest_api_init', function () {
    $admin = function () { return current_user_can('manage_options'); };

    register_rest_route('pusatriset/v1', '/import', [
        'methods' => 'POST', 'permission_callback' => $admin,
        'callback' => function (WP_REST_Request $req) {
            $table = (string) $req->get_param('table');
            $rows = $req->get_param('rows');
            // Transport base64: firewall host sering salah mengira teks ilmiah wajar sebagai SQL injection.
            $b64 = $req->get_param('rows_b64');
            if (is_string($b64) && $b64 !== '') {
                $dec = base64_decode($b64, true);
                $rows = $dec === false ? null : json_decode($dec, true);
            }
            if (!is_array($rows)) return new WP_Error('pr_rows', 'rows harus array', ['status' => 400]);
            $res = pr_import_rows($table, $rows);
            return $res;
        },
    ]);

    register_rest_route('pusatriset/v1', '/status', [
        'methods' => 'GET', 'permission_callback' => $admin,
        'callback' => function () {
            return ['version' => PR_VERSION, 'fulltext' => pr_has_fulltext(), 'counts' => pr_table_counts()];
        },
    ]);

    register_rest_route('pusatriset/v1', '/flush', [
        'methods' => 'POST', 'permission_callback' => $admin,
        'callback' => function () { pr_flush_cache(); flush_rewrite_rules(); return ['ok' => true]; },
    ]);

    // Sanggahan publik (maks 5 per jam per IP).
    register_rest_route('pusatriset/v1', '/disputes', [
        'methods' => 'POST', 'permission_callback' => '__return_true',
        'callback' => function (WP_REST_Request $req) {
            global $wpdb;
            $ip = isset($_SERVER['REMOTE_ADDR']) ? preg_replace('/[^0-9a-fA-F:.]/', '', $_SERVER['REMOTE_ADDR']) : 'x';
            $key = 'pr_disp_' . md5($ip);
            $n = (int) get_transient($key);
            if ($n >= 5) return new WP_Error('pr_rate', 'Terlalu banyak pengiriman, coba lagi nanti.', ['status' => 429]);
            $paper = sanitize_text_field((string) $req->get_param('paperId'));
            $type = sanitize_text_field((string) $req->get_param('disputeType'));
            $arg = sanitize_textarea_field((string) $req->get_param('argument'));
            if (!preg_match('/^[0-9a-f-]{36}$/i', $paper) || !in_array($type, ['relevance_badge', 'abstract_policy', 'summary_accuracy', 'other'], true) || mb_strlen($arg) < 5)
                return new WP_Error('pr_bad', 'Data tidak valid.', ['status' => 400]);
            $exists = $wpdb->get_var($wpdb->prepare('SELECT COUNT(*) FROM ' . pr_t('papers') . ' WHERE id = %s', $paper));
            if (!$exists) return new WP_Error('pr_nf', 'Riset tidak ditemukan.', ['status' => 404]);
            $wpdb->insert(pr_t('disputes'), [
                'id' => wp_generate_uuid4(), 'paper_id' => $paper, 'dispute_type' => $type,
                'submitted_by_name' => sanitize_text_field((string) $req->get_param('name')) ?: null,
                'submitted_by_email' => sanitize_email((string) $req->get_param('email')) ?: null,
                'argument' => $arg, 'status' => 'open', 'created_at' => current_time('mysql', true),
            ]);
            set_transient($key, $n + 1, HOUR_IN_SECONDS);
            return ['ok' => true];
        },
    ]);
});
