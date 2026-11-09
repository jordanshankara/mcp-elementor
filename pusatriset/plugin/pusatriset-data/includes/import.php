<?php
/**
 * Impor batch idempoten (REPLACE INTO) dari JSONL hasil ekstraksi. Hanya tabel & kolom pada whitelist pr_tables().
 */
if (!defined('ABSPATH')) exit;

function pr_import_value($v) {
    if ($v === null) return 'NULL';
    if (is_bool($v)) return $v ? '1' : '0';
    if (is_int($v) || is_float($v)) return (string) $v;
    if (is_array($v)) $v = wp_json_encode($v);
    $v = (string) $v;
    // ISO 8601 -> format DATETIME MySQL
    if (preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/', $v)) $v = str_replace('T', ' ', substr($v, 0, 19));
    return "'" . esc_sql($v) . "'";
}

/**
 * @param string $table nama tabel tanpa prefix
 * @param array  $rows  daftar objek (kolom => nilai)
 * @return array ['inserted' => n, 'skipped' => n]
 */
function pr_import_rows($table, array $rows) {
    global $wpdb;
    $defs = pr_tables();
    if (!isset($defs[$table])) return new WP_Error('pr_table', 'Tabel tidak dikenal: ' . $table, ['status' => 400]);
    $cols = $defs[$table]['cols'];
    $n = 0; $skip = 0; $values = [];
    foreach ($rows as $r) {
        if (!is_array($r)) { $skip++; continue; }
        $vals = [];
        foreach ($cols as $c) $vals[] = pr_import_value(array_key_exists($c, $r) ? $r[$c] : null);
        $values[] = '(' . implode(',', $vals) . ')';
        $n++;
    }
    if ($values) {
        $colSql = '`' . implode('`,`', $cols) . '`';
        foreach (array_chunk($values, 200) as $chunk) {
            $ok = $wpdb->query('REPLACE INTO ' . pr_t($table) . " ($colSql) VALUES " . implode(',', $chunk));
            if ($ok === false) return new WP_Error('pr_db', 'Gagal menulis ' . $table . ': ' . $wpdb->last_error, ['status' => 500]);
        }
    }
    pr_flush_cache();
    return ['inserted' => $n, 'skipped' => $skip];
}

function pr_table_counts() {
    global $wpdb;
    $out = [];
    foreach (array_keys(pr_tables()) as $t) $out[$t] = (int) $wpdb->get_var('SELECT COUNT(*) FROM ' . pr_t($t));
    $out['disputes'] = (int) $wpdb->get_var('SELECT COUNT(*) FROM ' . pr_t('disputes'));
    return $out;
}
