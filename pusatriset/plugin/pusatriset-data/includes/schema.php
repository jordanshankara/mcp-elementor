<?php
/**
 * Skema tabel khusus (meniru skema aplikasi lama; UUID dipertahankan agar tautan /riset/<uuid> tetap hidup).
 * Nama tabel = {prefix}pr_<nama lama>. Tidak memakai foreign key (relasi dijaga aplikasi), semua kolom FK di-index.
 */
if (!defined('ABSPATH')) exit;

/** Nama tabel berprefix. */
function pr_t($name) {
    global $wpdb;
    return $wpdb->prefix . 'pr_' . $name;
}

/** Daftar tabel yang boleh diimpor + kolomnya (urutan) + kunci utama + kolom bertipe khusus. */
function pr_tables() {
    return [
        'papers' => ['pk' => ['id'], 'cols' => ['id', 'title', 'title_lang', 'abstract_raw', 'abstract_display_policy', 'published_date', 'language', 'origin', 'venue_id', 'venue_name_raw', 'venue_country', 'source_tier', 'tier_reason', 'is_foundational', 'metadata_status', 'inclusion_basis', 'canonical_url', 'license_raw', 'license_normalized', 'affiliation_inferred', 'enrichment_status', 'priority_pinned_at', 'issn_l', 'sjr_quartile', 'sjr_score', 'sjr_year', 'created_at', 'updated_at', 'publication_type']],
        'paper_titles' => ['pk' => ['paper_id', 'language'], 'cols' => ['paper_id', 'language', 'title', 'is_primary']],
        'paper_identifiers' => ['pk' => ['id'], 'cols' => ['id', 'paper_id', 'id_type', 'id_value']],
        'authors' => ['pk' => ['id'], 'cols' => ['id', 'name', 'orcid_id', 'openalex_author_id']],
        'paper_authors' => ['pk' => ['paper_id', 'author_id'], 'cols' => ['paper_id', 'author_id', 'author_order']],
        'institutions' => ['pk' => ['id'], 'cols' => ['id', 'name', 'country', 'institution_type', 'openalex_institution_id', 'ror_id', 'profile_description']],
        'institution_name_variants' => ['pk' => ['institution_id', 'name'], 'cols' => ['institution_id', 'name']],
        'author_affiliations' => ['pk' => ['author_id', 'institution_id', 'paper_id'], 'cols' => ['author_id', 'institution_id', 'paper_id']],
        'paper_affiliation_countries' => ['pk' => ['paper_id', 'country_code'], 'cols' => ['paper_id', 'country_code']],
        'paper_topics' => ['pk' => ['id'], 'cols' => ['id', 'paper_id', 'domain', 'field', 'subfield', 'topic', 'topic_id', 'is_primary', 'score']],
        'citation_stats' => ['pk' => ['paper_id'], 'cols' => ['paper_id', 'citation_count_total', 'citation_by_year', 'fwci', 'citation_normalized_percentile', 'local_percentile', 'retraction_status']],
        'summaries' => ['pk' => ['id'], 'cols' => ['id', 'paper_id', 'language', 'content', 'source_type', 'provenance', 'status', 'authored_by', 'reviewed_by', 'version', 'created_at']],
        'paper_relations' => ['pk' => ['id'], 'cols' => ['id', 'paper_id_old', 'paper_id_new', 'relation_type', 'confidence_score', 'reasoning_text', 'status']],
        'relevance_scores' => ['pk' => ['paper_id'], 'cols' => ['paper_id', 'computed_score', 'computed_status', 'computed_reasoning', 'published_status', 'published_reasoning', 'override_by', 'override_reason']],
        'policy_tags' => ['pk' => ['id'], 'cols' => ['id', 'slug', 'label_id', 'label_en', 'tag_group', 'active']],
        'paper_policy_tags' => ['pk' => ['paper_id', 'tag_id'], 'cols' => ['paper_id', 'tag_id', 'status']],
        'search_synonyms' => ['pk' => ['id'], 'cols' => ['id', 'term', 'expands_to', 'active']],
        'search_terms' => ['pk' => ['term'], 'cols' => ['term', 'frequency']],
        'approved_venues' => ['pk' => ['id'], 'cols' => ['id', 'display_name', 'venue_type', 'tier', 'ranking_basis', 'openalex_source_id', 'issn_l', 'country', 'active']],
        'venue_arxiv_categories' => ['pk' => ['venue_id', 'category'], 'cols' => ['venue_id', 'category']],
        'paper_versions' => ['pk' => ['id'], 'cols' => ['id', 'paper_id', 'version_number', 'changed_summary', 'version_date']],
        'paper_merges' => ['pk' => ['surviving_id', 'merged_id'], 'cols' => ['surviving_id', 'merged_id', 'method', 'merged_at']],
        'paper_files' => ['pk' => ['id'], 'cols' => ['id', 'paper_id', 'storage_key', 'original_name', 'size_bytes', 'page_count', 'download_count', 'uploaded_by', 'uploaded_at']],
    ];
}

function pr_install_schema() {
    global $wpdb;
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    $c = $wpdb->get_charset_collate();
    $t = 'pr_t';
    $sql = [];

    $sql[] = "CREATE TABLE {$t('papers')} (
      id CHAR(36) NOT NULL,
      title VARCHAR(500) NOT NULL,
      title_lang VARCHAR(20) NULL,
      abstract_raw MEDIUMTEXT NULL,
      abstract_display_policy VARCHAR(20) NOT NULL DEFAULT 'summary_only',
      published_date DATE NULL,
      language VARCHAR(20) NULL,
      origin VARCHAR(20) NOT NULL,
      venue_id CHAR(36) NULL,
      venue_name_raw VARCHAR(500) NULL,
      venue_country VARCHAR(50) NULL,
      source_tier VARCHAR(10) NOT NULL DEFAULT 'tier_3',
      tier_reason VARCHAR(255) NULL,
      is_foundational TINYINT(1) NOT NULL DEFAULT 0,
      metadata_status VARCHAR(20) NOT NULL DEFAULT 'indexed',
      inclusion_basis VARCHAR(255) NULL,
      canonical_url TEXT NULL,
      license_raw TEXT NULL,
      license_normalized VARCHAR(20) NOT NULL DEFAULT 'unknown',
      affiliation_inferred TINYINT(1) NOT NULL DEFAULT 0,
      enrichment_status VARCHAR(30) NOT NULL DEFAULT 'pending',
      priority_pinned_at DATETIME NULL,
      issn_l VARCHAR(20) NULL,
      sjr_quartile VARCHAR(12) NULL,
      sjr_score DOUBLE NULL,
      sjr_year INT NULL,
      created_at DATETIME(3) NULL,
      updated_at DATETIME(3) NULL,
      publication_type VARCHAR(20) NOT NULL DEFAULT 'indexed',
      PRIMARY KEY  (id),
      KEY pr_pub_date (published_date),
      KEY pr_status_date (metadata_status, published_date),
      KEY pr_origin (origin),
      KEY pr_tier (source_tier),
      KEY pr_venue (venue_id),
      KEY pr_quartile (sjr_quartile),
      KEY pr_pubtype (publication_type)
    ) $c;";

    $sql[] = "CREATE TABLE {$t('paper_titles')} (
      paper_id CHAR(36) NOT NULL, language VARCHAR(20) NOT NULL, title VARCHAR(500) NOT NULL, is_primary TINYINT(1) NOT NULL DEFAULT 0,
      PRIMARY KEY  (paper_id, language)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_identifiers')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, id_type VARCHAR(30) NOT NULL, id_value VARCHAR(255) NOT NULL,
      PRIMARY KEY  (id), UNIQUE KEY pr_idf (id_type, id_value), KEY pr_idf_paper (paper_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('authors')} (
      id CHAR(36) NOT NULL, name VARCHAR(500) NOT NULL, orcid_id VARCHAR(40) NULL, openalex_author_id VARCHAR(60) NULL,
      PRIMARY KEY  (id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_authors')} (
      paper_id CHAR(36) NOT NULL, author_id CHAR(36) NOT NULL, author_order INT NOT NULL,
      PRIMARY KEY  (paper_id, author_id), KEY pr_pa_author (author_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('institutions')} (
      id CHAR(36) NOT NULL, name VARCHAR(500) NOT NULL, country VARCHAR(10) NULL, institution_type VARCHAR(50) NULL,
      openalex_institution_id VARCHAR(60) NULL, ror_id VARCHAR(60) NULL, profile_description TEXT NULL,
      PRIMARY KEY  (id), KEY pr_inst_country (country)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('institution_name_variants')} (
      institution_id CHAR(36) NOT NULL, name VARCHAR(255) NOT NULL, PRIMARY KEY  (institution_id, name)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('author_affiliations')} (
      author_id CHAR(36) NOT NULL, institution_id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL,
      PRIMARY KEY  (author_id, institution_id, paper_id), KEY pr_aa_inst (institution_id), KEY pr_aa_paper (paper_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_affiliation_countries')} (
      paper_id CHAR(36) NOT NULL, country_code VARCHAR(10) NOT NULL, PRIMARY KEY  (paper_id, country_code)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_topics')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, domain VARCHAR(200) NULL, field VARCHAR(200) NULL, subfield VARCHAR(200) NULL,
      topic VARCHAR(300) NULL, topic_id VARCHAR(60) NULL, is_primary TINYINT(1) NOT NULL DEFAULT 0, score DOUBLE NULL,
      PRIMARY KEY  (id), KEY pr_topic_paper (paper_id), KEY pr_topic_sub (subfield)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('citation_stats')} (
      paper_id CHAR(36) NOT NULL, citation_count_total INT NOT NULL DEFAULT 0, citation_by_year LONGTEXT NULL, fwci DOUBLE NULL,
      citation_normalized_percentile DOUBLE NULL, local_percentile DOUBLE NULL, retraction_status VARCHAR(30) NOT NULL DEFAULT 'none',
      PRIMARY KEY  (paper_id), KEY pr_cit_total (citation_count_total)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('summaries')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, language VARCHAR(5) NOT NULL DEFAULT 'id', content MEDIUMTEXT NULL,
      source_type VARCHAR(20) NOT NULL, provenance VARCHAR(20) NOT NULL DEFAULT 'from_abstract', status VARCHAR(20) NOT NULL DEFAULT 'draft',
      authored_by CHAR(36) NULL, reviewed_by CHAR(36) NULL, version INT NOT NULL DEFAULT 1, created_at DATETIME(3) NULL,
      PRIMARY KEY  (id), KEY pr_sum_lookup (paper_id, language, status)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_relations')} (
      id CHAR(36) NOT NULL, paper_id_old CHAR(36) NOT NULL, paper_id_new CHAR(36) NOT NULL, relation_type VARCHAR(30) NOT NULL,
      confidence_score DOUBLE NULL, reasoning_text TEXT NULL, status VARCHAR(20) NOT NULL DEFAULT 'suggested',
      PRIMARY KEY  (id), UNIQUE KEY pr_rel_uniq (paper_id_old, paper_id_new, relation_type), KEY pr_rel_new (paper_id_new)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('relevance_scores')} (
      paper_id CHAR(36) NOT NULL, computed_score INT NULL, computed_status VARCHAR(30) NOT NULL DEFAULT 'too_new_to_score',
      computed_reasoning TEXT NULL, published_status VARCHAR(30) NULL, published_reasoning TEXT NULL, override_by CHAR(36) NULL, override_reason TEXT NULL,
      PRIMARY KEY  (paper_id), KEY pr_rel_pub (published_status)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('policy_tags')} (
      id CHAR(36) NOT NULL, slug VARCHAR(100) NOT NULL, label_id VARCHAR(200) NOT NULL, label_en VARCHAR(200) NULL, tag_group VARCHAR(100) NULL, active TINYINT(1) NOT NULL DEFAULT 1,
      PRIMARY KEY  (id), UNIQUE KEY pr_tag_slug (slug)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_policy_tags')} (
      paper_id CHAR(36) NOT NULL, tag_id CHAR(36) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'suggested',
      PRIMARY KEY  (paper_id, tag_id), KEY pr_ppt_tag (tag_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('search_synonyms')} (
      id CHAR(36) NOT NULL, term VARCHAR(190) NOT NULL, expands_to TEXT NOT NULL, active TINYINT(1) NOT NULL DEFAULT 1,
      PRIMARY KEY  (id), UNIQUE KEY pr_syn_term (term)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('search_terms')} (
      term VARCHAR(190) NOT NULL, frequency INT NOT NULL DEFAULT 0, PRIMARY KEY  (term), KEY pr_term_freq (frequency)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('approved_venues')} (
      id CHAR(36) NOT NULL, display_name VARCHAR(300) NOT NULL, venue_type VARCHAR(20) NOT NULL, tier VARCHAR(10) NOT NULL, ranking_basis VARCHAR(255) NULL,
      openalex_source_id VARCHAR(60) NULL, issn_l VARCHAR(20) NULL, country VARCHAR(50) NULL, active TINYINT(1) NOT NULL DEFAULT 1,
      PRIMARY KEY  (id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('venue_arxiv_categories')} (
      venue_id CHAR(36) NOT NULL, category VARCHAR(60) NOT NULL, PRIMARY KEY  (venue_id, category)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_versions')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, version_number INT NOT NULL, changed_summary TEXT NULL, version_date DATE NULL,
      PRIMARY KEY  (id), UNIQUE KEY pr_ver_uniq (paper_id, version_number)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_merges')} (
      surviving_id CHAR(36) NOT NULL, merged_id CHAR(36) NOT NULL, method VARCHAR(60) NOT NULL, merged_at DATETIME NULL,
      PRIMARY KEY  (surviving_id, merged_id), KEY pr_merge_old (merged_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('paper_files')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, storage_key VARCHAR(500) NOT NULL, original_name VARCHAR(500) NOT NULL, size_bytes INT NOT NULL,
      page_count INT NULL, download_count INT NOT NULL DEFAULT 0, uploaded_by CHAR(36) NULL, uploaded_at DATETIME NULL,
      PRIMARY KEY  (id), UNIQUE KEY pr_file_paper (paper_id)
    ) $c;";
    $sql[] = "CREATE TABLE {$t('disputes')} (
      id CHAR(36) NOT NULL, paper_id CHAR(36) NOT NULL, dispute_type VARCHAR(40) NOT NULL, submitted_by_name VARCHAR(200) NULL, submitted_by_email VARCHAR(200) NULL,
      argument TEXT NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'open', resolution TEXT NULL, created_at DATETIME NULL,
      PRIMARY KEY  (id), KEY pr_disp_paper (paper_id)
    ) $c;";

    // CREATE TABLE IF NOT EXISTS (bukan dbDelta: definisi padat per-baris tidak aman untuk parser dbDelta).
    // Perubahan skema berikutnya = ALTER bersyarat di bawah, dinaikkan lewat PR_DB_VERSION.
    foreach ($sql as $s) $wpdb->query(preg_replace('/^CREATE TABLE /', 'CREATE TABLE IF NOT EXISTS ', $s));

    // FULLTEXT dibuat terpisah (dbDelta tidak andal untuk FULLTEXT). Bila hosting tak mendukung, pencarian otomatis turun ke LIKE.
    $papers = pr_t('papers');
    $has = $wpdb->get_var("SHOW INDEX FROM $papers WHERE Key_name = 'pr_ft'");
    if (!$has) $wpdb->query("ALTER TABLE $papers ADD FULLTEXT KEY pr_ft (title, abstract_raw)");

    update_option('pr_db_version', PR_DB_VERSION);
}

function pr_has_fulltext() {
    global $wpdb;
    static $r = null;
    if ($r === null) $r = (bool) $wpdb->get_var("SHOW INDEX FROM " . pr_t('papers') . " WHERE Key_name = 'pr_ft'");
    return $r;
}
