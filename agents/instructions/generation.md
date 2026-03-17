# Generation Agent

You receive a run directory path, a target PDF output path (`guides/[category-slug]-[YYYY-MM-DD].pdf`), and the project root. `scored_products.json` and `requirements.json` are in the run directory.

**Read `buyers-guide-refactored/buyers-guide/template-structure.md` in full before writing any code.**

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

2. Write `[run_dir]/guide.js` using `template-structure.md` as the foundation. Populate all content arrays from `scored_products.json` and `requirements.json`.

   **Local path note:** `template-structure.md` was written for the Claude.ai environment and may reference `/mnt/skills/public/docx/SKILL.md`. In Claude Code, ignore that reference — the docx pipeline is already embedded in `template-structure.md` itself. Do not attempt to read any `/mnt/` paths.

3. Run guide.js:
   ```bash
   node [run_dir]/guide.js
   ```

4. If `node` exits with an error:
   - Syntax error / module issue → read the error, fix `guide.js`, retry once
   - Missing npm module → tell the user: `cd [run_dir] && npm install [module]`
   - Do not retry more than once for the same error

5. Validate the docx output:
   ```bash
   python buyers-guide-refactored/buyers-guide/scripts/validate.py [run_dir]/guide.docx
   ```
   Note: if `scripts/validate.py` does not exist locally, skip this step and note it in your output.

6. Convert to PDF:
   ```bash
   soffice --headless --convert-to pdf [run_dir]/guide.docx --outdir guides/
   ```
   Or if `soffice` is not in PATH:
   ```bash
   /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf [run_dir]/guide.docx --outdir guides/
   ```

7. Confirm the PDF exists at the output path and report it to the user.

## Error recovery

| Error | Action |
|---|---|
| Syntax error in guide.js | Fix and retry once |
| Missing npm module | Tell user to install, do not retry |
| soffice not found | Tell user `brew install --cask libreoffice`, do not retry |
| validate.py not found | Skip validation step, note in output |
| PDF not created after soffice | Report the soffice stderr output to the user |
