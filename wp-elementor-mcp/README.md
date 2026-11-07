# wp-elementor-mcp

Satu MCP server untuk mengelola banyak situs WordPress + Elementor (**Free maupun Pro**) dari Claude Code.
Cara pakai sehari-hari ada di skill `.claude/skills/wp-elementor/SKILL.md` (panggil `/wp-elementor <alias> <perintah>`).

## Komponen
| Bagian | Fungsi |
|---|---|
| `src/index.ts` | 14 tool MCP (semua wajib `site`) |
| `src/elementor.ts` | fungsi murni: outline, find, patch, insert/duplicate/move/remove, lint performa |
| `src/ops.ts` | tulis aman: rev (baca-sebelum-tulis), guard situs, validasi widget Free/Pro, backup lokal, verifikasi, auto-restore |
| `src/media.ts` | upload gambar teroptimasi (sharp → WebP, resize per slot, budget, alt wajib) |
| `src/visual.ts` / `src/perf.ts` | regresi visual (Playwright) & PageSpeed/Lighthouse |
| `bridge-plugin/claude-bridge/` | plugin WP kecil (endpoint `/claude/v1/*`) — `npm run build-zip` → `dist/claude-bridge.zip` |
| `src/cli.ts` | CLI cadangan: `node src/cli.ts <tool> '<json>'` |

## Perintah
```bash
npm install                 # sekali
npm test                    # unit test
npm run playground          # 2 WordPress lokal (Elementor Free) — biarkan jalan
npm run e2e                 # tes end-to-end lewat MCP sungguhan → ../reports/e2e-report.md
npm run build-zip           # dist/claude-bridge.zip untuk di-upload ke situs
```

## Catatan teknis
- Butuh Node ≥ 22.18 (TypeScript dijalankan langsung tanpa build). Playground CLI dipatok 3.1.53 (versi lebih baru butuh Node ≥ 24.18).
- Elementor Free mendaftarkan widget Pro sebagai *placeholder promosi*; bridge memisahkannya (`promo`) sehingga engine tidak menyisipkan widget yang render kosong.
- `get_builder_content_for_display()` kosong di konteks REST; bridge memakai `get_builder_content()` untuk render check.
- Setelah purge cache global, Elementor membuat ulang CSS saat kunjungan pertama → engine melakukan warm-up sebelum visual check.
