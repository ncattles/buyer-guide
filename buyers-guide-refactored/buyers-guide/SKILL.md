---
name: buyers-guide
description: "Use this skill whenever the user wants a product comparison, buyer's guide, market research, or product recommendation report for any consumer product category. Triggers include: requests to find the 'best' product in a category, compare multiple products head-to-head, research what's available on the market, rate and rank products, or create a buying guide document. Also triggers when the user asks for deep dives on product specs, value analysis, price-to-performance rankings, or 'what should I buy' style questions for any product type (PCs, laptops, monitors, TVs, headphones, cameras, appliances, tools, cars, etc.). Even if the user just asks 'what's the best X right now' — use this skill. Also triggers when the user asks to refresh, update, or revisit an existing buyer's guide. Produces a professional PDF buyer's guide with ratings, spec tables, pros/cons, links, and final recommendations."
---

# Buyer's Guide — Product Research & Recommendation PDF

## Overview

This skill produces a comprehensive, professional buyer's guide PDF for any consumer product category. The output is a polished document built via docx-js → LibreOffice PDF conversion. Research methodology is in `references/research.md`; scoring and business logic is in `references/rules.md`; document generation code is in `template-structure.md`.

---

## Workflow

### Step 1: Understand the Request

Clarify all of the following before proceeding:

- **Product category** — what are they looking for?
- **Budget** — what is the ceiling? Is there flexibility above it? Note the exact phrasing (e.g. "under $500", "around $500", "$400–600") for use in the banner meta line.
- **Location / region** — where are they based? Determines retailers, pricing, availability, and currency. Ask explicitly if not provided — never assume.
- **Priority factors** — what matters most (performance, portability, value, brand, aesthetics)?
- **Use case** — how and where will it be used?
- **Specific brands or products** already considered — any ruled out or leaning toward?

**Budget formatting for the banner meta line:**
- Exact ceiling: `Budget: Under $500`
- Approximate: `Budget: ~$500`
- Range: `Budget: $400–600`
- Flexible: `Budget: $500 (flexible)`

**Location must be confirmed before research begins.**

---

### Step 1.5: Verify User's Existing Hardware (Accessories & Compatibility Guides Only)

**If the recommended product must physically interact with hardware the user already owns**, verify the exact model and variant of that hardware before any research begins. Do not assume — ask or search.

- Confirm the exact model name and variant (not just brand or product line)
- Check for naming variants that are easily confused
- Document confirmed hardware in the Requirements Checklist
- If the user's hardware variant changes which products qualify, treat this as make-or-break

---

### Step 2: Make-or-Break Requirements Gate

**Before any research begins**, identify and confirm the user's non-negotiable requirements. Wait for answers before proceeding.

- Ask 3–5 binary yes/no questions specific to the category (e.g., "Must it have a VESA mount?")
- Store confirmed requirements — they become hard filters in Step 4 and appear as the Requirements Checklist in the document
- Category-specific dealbreaker examples → see `references/rules.md`

---

### Step 2.5: Contradictory Requirements Check

**Before research begins, scan the confirmed requirements and budget for internal contradictions.** Common patterns:

- Budget that cannot realistically support the required specs (e.g., "4K OLED 144Hz under $200")
- Mutually exclusive features (e.g., "ultra-portable but must have a discrete GPU and full-size ports")
- Requirements that eliminate the entire market

**If a contradiction is found:**
1. Stop before researching. Do not try to silently work around it.
2. Tell the user clearly: explain which requirements conflict, and what the realistic options are.
3. Offer a ranked list of which requirement to relax for the best outcome.
4. Wait for the user to revise before proceeding.

---

### Step 3: Deep Research Phase

**READ `references/research.md` before beginning any research track.**

Research consists of six tracks. Minimum 15–25 web searches total. Do not shortcut any track.

- **Track A** — Category Landscape: build the complete candidate pool including retailer-specific searches
- **Track B** — Community & Owner Intelligence: real owner reports, complaints, reliability
- **Track C** — Specification Verification: independent measurements against manufacturer claims
- **Track D** — Price Intelligence: current prices, price history, sale patterns
- **Track E** — Availability & Lifecycle: recalls, discontinuation, imminent successors
- **Track F** — Final Per-Product Verification: confirm exact model, URL, and regional specs

All track detail, inline rules, and source lists are in `references/research.md`.

---

### Step 3.5: Mid-Research Requirement Change

**If the user adds, removes, or changes a requirement after research has already begun**, stop and assess impact before continuing.

1. Identify which products are affected — eliminated by the new requirement, or newly eligible
2. If products are eliminated: remove them. If pool drops below 3, surface this to the user before proceeding
3. If new products are eligible: run Track A scoped to the new requirement, then Track F on any new finalists
4. If the change is a contradiction with existing requirements: treat as Step 2.5 — stop, surface, wait
5. **Never silently continue** with the pre-change candidate list. Acknowledge the change and confirm the updated list with the user before generating the document

---

### Step 4: Organize and Rank

**READ `references/rules.md` before scoring any product.**

Apply make-or-break requirements as hard filters first. Then apply the budget rule, then rank.

**Budget enforcement rule:**
- Products within budget are the primary pool
- Products exceeding budget by more than 15% may only appear as explicitly flagged stretch picks — labelled in the verdict badge and card copy. Never silently include over-budget products
- If no products within budget meet the requirements, tell the user before generating

**Product count per guide:**
- Focused categories (narrow budget, few qualifying products): 3 products
- Broad categories (wide use case, wide range): 4–5 products
- Competitive categories with many options (prebuilt PCs, laptops, TVs, appliances): always target 5–6 products
- Maximum: 6 products
- Fewer than 3 viable products: stop, tell the user, explain which filters caused the shortfall

All scoring methodology, rating scale, penalties, edge cases, tiebreaker rules, and safety override are in `references/rules.md`.

---

### Step 5: Generate the Document

**READ `template-structure.md` before writing any code.**

**Mandatory order:**
1. Read `template-structure.md` — use as the script foundation; do NOT rewrite helper functions from scratch
2. Write `guide.js` starting from `template-structure.md`, populating content arrays with researched data
3. Run: `node guide.js`
4. Validate: `python /mnt/skills/public/docx/scripts/office/validate.py guide.docx`
5. Convert: `python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf guide.docx`
6. Copy to `/mnt/user-data/outputs/`
7. Present with `present_files`

---

## Living Document Refresh Protocol

When a user asks to **refresh or update** an existing buyer's guide:

1. **Re-run Track D** — prices change most frequently
2. **Re-run Track E** — discontinued products, new successors, new recalls
3. **Re-run Track B** — new complaints or long-term reports since original guide
4. **Re-run Track C spot-check** — re-fetch each product's current manufacturer spec page; confirm no specs have been quietly revised. Full Track C is not required — but any spec that could have changed must be re-confirmed.
5. **Check for new entrants** — run Track A with current date
6. **Re-verify any spec claims** flagged as unverified in the original guide
7. **Re-verify the user's existing hardware** if time has passed
8. **Re-check timing recommendations** — has the price situation changed? Is a successor now confirmed?
9. **Re-run contradictory requirements check** if requirements have changed
10. **Regenerate the document** using `template-structure.md` as the base — do not patch the old PDF

Product count rules apply on refresh exactly as on a new guide — see `references/rules.md` for refresh-specific edge cases.

Note in the updated guide's banner meta line: "Updated [Month YYYY] — original guide [Month YYYY]"

---

## Output Process

```bash
node guide.js
python /mnt/skills/public/docx/scripts/office/validate.py guide.docx
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf guide.docx
cp guide.pdf /mnt/user-data/outputs/
```

---

## Iteration and Correction

When the user provides corrections:
- **Re-verify from primary sources** before updating any spec or price
- **Update all affected sections** — a price change affects the spec table, rankings table, AND recommendations
- **Regenerate the full PDF** using `template-structure.md` as the base — never patch the existing PDF
- **Acknowledge the error clearly**
