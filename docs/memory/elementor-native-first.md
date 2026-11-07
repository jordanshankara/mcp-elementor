---
name: elementor-native-first
description: User wants Elementor edits built with native controls (visuals never via HTML widget/custom CSS); HTML widget only allowed for functional features they approve; Elementor 4 atomic format gotchas learned on regulasi
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1683db9e-be5d-404a-9c30-db44ad92af69
  modified: 2026-11-06T01:29:04.373Z
---

Never use the `html` widget (or inline `<style>`) as a shortcut to style a section. Build with native Elementor controls: in Elementor 4.3.6 Free, atomic `e-flexbox` / `e-heading` support background (gradient), border, radius, box-shadow and `backdrop-filter` natively; legacy `container` supports gradient, border, radius, shadow but no backdrop blur.

**Why:** user was upset (2026-11-05) when the glassmorphism "MCP BERHASIL" box on regulasi `/testing` was built with an HTML widget; pages must stay editable by other people in the editor with no code visible, and they fear the MCP will wipe sections and replace them with HTML. They also said: don't judge/assume they made a mistake, accept the fact and fix.

**Exception (2026-11-06, regulasi redesign):** user explicitly allowed the HTML widget ONLY for functional features (document search + filter, simple input form saved to a spreadsheet). Layout/visuals stay native. Ask before using it anywhere else. User also said the "Pro risks" (search form, form, loop grid) are all clear/decided. Workflow: design first with html-design-studio in `E:\1. Code\regulasi\design`, then build into the site with /wp-elementor.

**How to apply:**
- Atomic JSON: element `styles` = `{ "<class-id>": {id, label:"local", type:"class", variants:[{meta:{breakpoint:"desktop"|"mobile",state:null},custom_css:null,props:{...}}]} }` and `settings.classes = {$$type:"classes", value:[class-id]}`. Prop shapes: `size` {size,unit}, `color`, `string`, `number`, `dimensions`, `box-shadow`, `backdrop-filter`, gradient via `background`→`background-overlay`→`background-gradient-overlay`.
- `e-heading` title MUST be `{"$$type":"escaped-html","value":"text"}`.
- Prop schemas: github.com/elementor/elementor tag `4.3.6` (modules/atomic-widgets/...).
- After writing atomic styles via the bridge, run `POST /claude/v1/purge` (wp_request) and visit the page; bridge should purge automatically (todo).
- `elementor_update` only patches `settings` (changes need `id`, not `element_id`); to change styles re-insert the element.
- Legacy inner container: `boxed_width` ignored when nested; use `width` px + `width_mobile` %.
- If the page shows an old version, the user's editor may have saved stale data over MCP writes; ask them to reload the editor first.
- Regulasi build gotchas (2026-11-06): Astra squeezes Elementor pages unless page meta `ast-site-content-layout=full-width-container`, `site-content-layout=page-builder`, `site-content-style=unboxed`, `site-sidebar-layout=no-sidebar`. Nested containers have default 10px padding, set padding 0 or px-width rows wrap. icon-box shows lorem description unless `description_text:""`. Astra gives buttons a blue border: set `border_border:solid`, width 0, color transparent. Publishing via wp_request is blocked by auto mode until the user confirms in chat. Always pass `fields` on wp_request POST (huge output otherwise). Site has HFE plugin (header/footer via Elementor), SureForms + OttoKit (Google Sheets) installed.
- Verify with `visual_check` (`op: snapshot`, `url`, `name`); images land in `reports/<alias>/`.
