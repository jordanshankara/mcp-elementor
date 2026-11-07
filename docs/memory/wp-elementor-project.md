---
name: wp-elementor-project
description: "E:\\1. Code hosts a custom MCP + skill to manage the user's 8 WordPress/Elementor (Free) sites from Claude Code; status and constraints"
metadata:
  node_type: memory
  type: project
  originSessionId: 1683db9e-be5d-404a-9c30-db44ad92af69
  modified: 2026-11-06T14:49:14.011Z
---

User (Indonesian-speaking) manages 8 WordPress + Elementor Free sites from Claude Code in `E:\1. Code` (no Claude in Chrome). Engine: `wp-elementor-mcp/` (Node/TS MCP, 14 tools) + bridge plugin (now v1.2.0: theme-option/Astra settings, custom-css, flush, atomic CSS auto-purge) + skill `.claude/skills/wp-elementor` (see `references/lessons-redesign.md`).

**Status 2026-11-06:** only `regulasi` (regulasiai.id) is fully connected and redesigned (Regal Heritage palette navy #0B1B3A / gold #C9A24A / ivory #E8DAC0; Home + Regulasi Indonesia/Global + Pustaka Dokumen (218 docs from `_AI Regulations.xlsx`, cards+filter+pagination) + Perbandingan Negara + Informasi; header/footer via Astra; brand + asosiasi.ai logos WebP). Design source of truth: `E:\1. Code\regulasi\design\` (DNA.md, OUTLINE.md, build_site.py, build_library.py). Other 7 sites still need app password + bridge upload (readonly=true). Pending on regulasi: Kirim Dokumen form not connected to Google Sheets (SureForms+OttoKit), sample data cards (Update Terbaru, Perbandingan) still "contoh", mobile hero/footer visuals not fully screenshot-verified.

**Why:** user priorities: proven to work, never edit wrong site, Elementor FREE, token-thrifty but high quality, fast pages, responsive (desktop+tablet+mobile together), user is picky about design quality and gets frustrated by repeated revisions.

**How to apply:**
- Read the skill's lessons file before any build/redesign; follow [[elementor-native-first]].
- Rotate passwords: 8 wp-admin passwords were pasted in chat early on (never use/store them).
- Laptop: Node 24.14, no PHP/Docker; C: drive nearly full — keep temp on E:.
- Respond in Indonesian; user prefers detailed plans, then hands-off execution; report honestly what is NOT verified.

**Update 2026-11-07:** repo GitHub: https://github.com/jordanshankara/mcp-elementor (panduan lanjut: `docs/HANDOFF.md`). Situs ke-9 `pusatriset` (pusatriset.ai) terdaftar, mode tulis; Elementor + Classic Editor sudah aktif, menunggu Bridge 1.3.0 diunggah pengguna untuk memasang Astra (`/claude/v1/theme-install`). Bridge terbaru 1.3.0 (tambahan: theme-option Astra, custom-css, flush, theme-install, auto-purge atomic). Skill sudah berisi `references/lessons-redesign.md`.
