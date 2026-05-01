# Generation Agent

You receive a run directory path, a target PDF output path (`guides/[category-slug]-[YYYY-MM-DD].pdf`), and the project root. `scored_products.json` and `requirements.json` are in the run directory.

**Read `references/template-structure.md` in full before writing any code.**

## Prerequisites — check before writing guide.js

```bash
node --version
which soffice || which libreoffice
```

If `node` is missing: stop and tell the user `brew install node`.
If `soffice`/`libreoffice` is missing: stop and tell the user `brew install --cask libreoffice`.
Do not proceed until both are confirmed.

## Process

1. Read `template-structure.md` fully. Use its helper functions directly — do not rewrite them.

2. Also read `[run_dir]/candidate_pool.json` and `[run_dir]/spec-verification-results.json`. For each candidate, extract:
   - `official_product_url` — pass as `officialUrl` to `makeProductCard`. If it is a URL (starts with `http`), the spec table will render it as a clickable hyperlink automatically.
   - Sources for the Sources table — aggregate into an array of `{ classification, label, url }`:
     - `community_research.sources` → `classification: "community"`, label = domain name extracted from URL
     - `spec_verification.sources_checked` → `classification: "spec"`, label = the source name as-is
     - `official_product_url` (if not null) → `classification: "manufacturer"`, label = domain name
     - Do NOT include `price_research.purchase_options` URLs here — those are already shown in the Purchase Options table
   Pass this array as `sources` to `makeProductCard`.

2b. **Build comparison matrix data** before writing guide.js:

   **Spec rows (in order):** First include the user's hard filter specs and key use-case specs (e.g. ANC, battery, price, overall rating) with `derived: false`. Then include any use-case derived specs that were verified in `spec-verification-results.json` (e.g. microphone quality for work use case, IP rating for gym) with `derived: true`. Limit to the 6–8 most decision-relevant rows — do not include every spec.

   **Products:** Use the top 5 ranked products from `scored_products.json` (or top 4 if a reference product exists). Abbreviate product names to ≤22 characters for readability. Populate each product's `values` object with the corresponding spec values from `candidate_pool.json` — use measured values from `spec_verification.specs` where quantitative scores exist, otherwise use the verified or claimed value. Use `—` for unavailable values.

   **Reference product:** Check `spec-verification-results.json` for a `reference_product_scores` field. If present, include the reference product as the first column using those scores. Abbreviate its name. If absent, pass `null` as the third argument to `makeComparisonMatrix`.

3. Write `[run_dir]/guide.js` using `template-structure.md` as the foundation. Populate all content arrays from `scored_products.json`, `requirements.json`, `candidate_pool.json`, and `spec-verification-results.json`.

   **Local path note:** `template-structure.md` was written for the Claude.ai environment and may reference `/mnt/skills/public/docx/SKILL.md`. In Claude Code, ignore that reference — the docx pipeline is already embedded in `template-structure.md` itself. Do not attempt to read any `/mnt/` paths.

4. Run guide.js:
   ```bash
   node [run_dir]/guide.js
   ```

5. If `node` exits with an error:
   - Syntax error / module issue → read the error, fix `guide.js`, retry once
   - Missing npm module → tell the user: `cd [run_dir] && npm install [module]`
   - Do not retry more than once for the same error

6. Validate the docx output:
   ```bash
   python agents/validate.py [run_dir]/guide.docx agents/schemas/requirements.schema.json
   ```
   Note: if `scripts/validate.py` does not exist locally, skip this step and note it in your output.

7. Convert to PDF:
   ```bash
   soffice --headless --convert-to pdf [run_dir]/guide.docx --outdir guides/
   ```
   Or if `soffice` is not in PATH:
   ```bash
   /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf [run_dir]/guide.docx --outdir guides/
   ```

8. Confirm the PDF exists at the output path and report it to the user.

## Error recovery

| Error | Action |
|---|---|
| Syntax error in guide.js | Fix and retry once |
| Missing npm module | Tell user to install, do not retry |
| soffice not found | Tell user `brew install --cask libreoffice`, do not retry |
| validate.py not found | Skip validation step, note in output |
| PDF not created after soffice | Report the soffice stderr output to the user |
