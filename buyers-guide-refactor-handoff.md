# Buyers-Guide Skill — Refactor Handoff Document
*Produced in Claude.ai session, March 16 2026. Hand this to Claude Code to implement.*

---

## Context

The buyers-guide skill has grown to 741 lines (SKILL.md) + 624 lines (template-structure.md) = 1,365 lines total. It mixes research methodology, business logic, and document generation in one file. It has 36 Critical Rules accumulated at the bottom that are disconnected from the workflow steps where they apply. It has never been tested against a structured eval set.

This document defines the refactor, the eval set, and the implementation order.

---

## Current File State (confirmed live as of March 16 2026)

```
buyers-guide/
├── SKILL.md              (741 lines — monolith)
└── template-structure.md (624 lines — document generation code, keep as-is)
```

The live skill files are in `/mnt/skills/user/buyers-guide/`. Do not edit them directly — they are read-only in the mounted filesystem. Work in `/home/claude/` and output to `/mnt/user-data/outputs/`.

---

## Target File Structure

```
buyers-guide/
├── SKILL.md              (~200 lines — orchestration only, pointers to reference files)
├── template-structure.md (unchanged)
└── references/
    ├── research.md       (~250 lines — Tracks A–F, all Track C sources by category)
    └── rules.md          (~200 lines — scoring methodology, business logic, edge cases)
```

**Total target: ~650 lines across 4 files, down from 1,365.**

---

## Design Decisions

### 1. Critical Rules list is eliminated
The 36 Critical Rules at the bottom of SKILL.md are eliminated as a list. Every rule is embedded in the workflow step or reference file where it is actually applied. A rule at line 727 that applies at step 3 will not be read at step 3. Rules 1–10 (docx technical rules) are already covered by template-structure.md and are redundant.

### 2. SKILL.md is orchestration only
SKILL.md describes the workflow and tells Claude *when* to read each reference file. It does not contain the content of those files. Structure:
- Step 1–2.5: Intake (inline — short enough)
- Step 3: "Read references/research.md before beginning Track A"
- Step 4: "Read references/rules.md before scoring"
- Step 5: "Read template-structure.md before writing any code"

### 3. Self-improvement loop is removed from mistakes-log
The self-improvement loop does not belong in mistakes-log (wrong trigger condition, buyers-guide-specific). It is not being moved into buyers-guide either. It is being replaced by the eval system — evals catch real failures; self-review catches known patterns. The eval set defined below is the replacement.

### 4. Agent architecture (future)
In Claude Code, Track A–F research should eventually become a research agent with a defined output contract (minimum candidate pool, required search types satisfied). This prevents the "stop at three familiar names" failure structurally. The refactored file structure mirrors this — research.md is the research agent's instructions in waiting. Implement as a skill now; convert to agent when ready.

---

## SKILL.md — New Content Outline (~200 lines)

```
---
name: buyers-guide
description: [existing description — keep as-is]
---

## Overview (3 lines)

## Workflow

### Step 1: Understand the Request
[intake questions — keep existing content, ~15 lines]

### Step 1.5: Verify Existing Hardware (Accessories only)
[keep existing content, ~8 lines]

### Step 2: Make-or-Break Requirements Gate
[keep existing content, ~10 lines]
[pointer: category-specific dealbreaker examples moved to references/rules.md]

### Step 2.5: Contradictory Requirements Check
[keep existing content, ~10 lines]

### Step 3: Deep Research Phase
READ references/research.md before beginning any research track.
[1-line summary of each track A–F — no content, just names and purposes]

### Step 3.5: Mid-Research Requirement Change
[keep existing content, ~8 lines]

### Step 4: Organize and Rank
READ references/rules.md before scoring any product.
[budget enforcement rule — keep inline, ~5 lines]
[product count rule — keep inline, ~8 lines]
[pointer: scoring methodology, edge cases, all other ranking logic in references/rules.md]

### Step 5: Generate the Document
READ template-structure.md before writing any code.
[mandatory order — keep inline, ~8 lines]

## Living Document Refresh Protocol
[keep existing content — ~15 lines]

## Output Process
[keep existing — 4 lines]

## Iteration and Correction
[keep existing — 4 lines]
```

---

## references/research.md — Content Outline (~250 lines)

Everything currently in Track A through Track F, including:

- Track A — Category Landscape (with retailer-specific search requirement)
- Track B — Community & Owner Intelligence
- Track C — Specification Verification (full category source list: electronics, audio, appliances, tools, vehicles, fitness, furniture, universal approach)
- Track D — Price Intelligence (CamelCamelCamel + non-Amazon alternatives by region)
- Track E — Availability & Lifecycle (recall databases by region: CPSC, RAPEX, OPSS, AU, CA)
- Track F — Final Per-Product Verification

Key rules embedded inline where they apply:
- "Do not stop after 3 familiar names" → inside Track A
- "Price History row fallback for new products" → inside Track D
- "Recall search by region" → inside Track E
- "Naming variant verification" → inside Track F
- "Community complaints require 3+ distinct sources" → inside Track B

---

## references/rules.md — Content Outline (~200 lines)

### Scoring Methodology
- Five-factor weighted table (price-to-value 30%, spec integrity 25%, community reception 20%, feature quality 15%, availability 10%)
- Applying weights + worked example
- N/A factors for new products
- Penalties (community complaints, spec divergence)
- Safety override (hard exclusion regardless of score)

### Rating Scale
- 9.0–10.0 through below 6.0 definitions
- When all finalists score below 6.0 → least-bad framing

### Edge Case Handling
- Dominant winner (≥1.0 gap) → intro + rec cards framing
- Sale price budget eligibility (≥3 confirmed sale events required)
- New product price history fallback
- Stretch picks (>15% over budget)
- Fewer than 3 viable products → stop and tell user
- Safety exclusion causing shortfall → Rule 36 first, then product count rule

### Rating Tiebreaker
- Price → availability → community sentiment

### Refresh-Specific Rules
- Product count applies on refresh same as new guide
- New entrant replaces lowest-rated, max 6 still holds
- Ranking order changes must propagate to rankings table, badges, rec cards

### Category-Specific Dealbreaker Examples
- Monitors, desks, laptops, PCs, headphones (moved from Step 2)

---

## Eval Set — 15 Test Cases

### How to run (Claude Code)
```bash
# After implementing refactored skill:
python -m scripts.run_eval \
  --skill-path /mnt/skills/user/buyers-guide \
  --eval-set buyers-guide-evals.json \
  --model claude-sonnet-4-6 \
  --verbose
```

### Test Cases

**Test 1 — Research depth: retailer-exclusive products**
- Prompt: "Best prebuilt PC with RTX 5080 and Ryzen 9800X3D, budget under $3,000, US, gaming and streaming at 1440p"
- Failure mode: Track A stops at editorial-list products, misses Micro Center
- Mechanical assertions: product count ≥ 5; all products have 2 links; all have Price History row
- Human assertions: Micro Center option present; track A search log shows retailer-specific searches run

**Test 2 — Regional sources: UK appliances**
- Prompt: "Best washing machines under £600, UK"
- Failure mode: Track C uses Consumer Reports (US-only); retailers are US
- Mechanical assertions: no Consumer Reports citation; currency is GBP; product count ≥ 4
- Human assertions: Which? or IEC test results cited; UK retailers only (AO.com, Currys etc.)

**Test 3 — Regional sources: AU non-electronics**
- Prompt: "Best standing desks under AU$800, Australia"
- Failure mode: Track C uses US sources; retailers are US
- Mechanical assertions: currency is AUD; no US-only retailers
- Human assertions: AU retailers present; wobble test sources cited

**Test 4 — Safety recall + pool count**
- Prompt: "Best espresso machines under €400, Germany — [provide context that one top product has an EU RAPEX recall]"
- Failure mode: recalled product included; pool drops below 3 without telling user
- Mechanical assertions: recalled product not in ranked list; recalled product present in What To Avoid
- Human assertions: RAPEX recall notice linked; if pool drops below 3, user informed before generation

**Test 5 — All finalists below 6.0**
- Prompt: "Best gaming chairs under $100, US" [a category where quality at this price is genuinely poor]
- Failure mode: ratings inflated; normal positive intro written
- Mechanical assertions: if all ratings < 6.0, intro contains "least-bad" or equivalent framing
- Human assertions: Final Recommendations framed as least-bad; budget increase recommended

**Test 6 — Mid-research requirement change**
- Prompt: "Best power tools under $200, Canada" then mid-conversation add "must be cordless only"
- Failure mode: silently continues with pre-change candidate list
- Mechanical assertions: guide not generated without explicit confirmation of updated candidate list
- Human assertions: affected products removed; new candidates searched for; user confirms before proceeding

**Test 7 — Refresh protocol**
- Prompt: "Refresh my 6-month-old robot vacuum guide, US" [provide mock original guide]
- Failure mode: skips Track C spot-check; skips recall search; doesn't note updated date
- Mechanical assertions: banner meta line contains "Updated [Month YYYY]"
- Human assertions: Track C spot-check performed; recall search run; new entrants checked

**Test 8 — Contradictory requirements**
- Prompt: "Best gaming monitors under $150, US — must be 4K OLED 144Hz"
- Failure mode: proceeds to research despite impossible requirements at this budget
- Mechanical assertions: guide not generated; user informed of contradiction
- Human assertions: specific conflict explained (4K OLED 144Hz does not exist under $150); options to relax offered

**Test 9 — New product, no price history**
- Prompt: "Best [product launched 4 weeks ago] under $X, US" [construct a scenario with a very new product]
- Failure mode: Price History row omitted or guessed; community reception marked N/A when early reports exist
- Mechanical assertions: Price History row present; contains "Insufficient data — launched"
- Human assertions: community reception scored from early reports if any exist, not marked N/A

**Test 10 — Dominant winner**
- Prompt: "Best noise-cancelling headphones under $400, US" [Sony WH-1000XM5 dominates this category]
- Failure mode: intro doesn't name dominant winner; false parity implied
- Mechanical assertions: intro paragraph present
- Human assertions: dominant product named in intro; gap noted; rec cards lead with "if you only read one recommendation"

**Test 11 — Naming variant trap**
- Prompt: "Best gaming monitors under $500, US" [category with near-identical model names like AOC Q27GAZD vs Q27G4ZD]
- Failure mode: wrong ASIN linked; similar model name recommended
- Mechanical assertions: all product links return 200 status; product link URLs contain correct model identifier
- Human assertions: linked pages match the model described in the guide

**Test 12 — Compatibility guide (Step 1.5)**
- Prompt: "Best MagSafe power banks for my iPhone 17 Pro Max with OtterBox Defender Series Pro case"
- Failure mode: skips Step 1.5 hardware verification; doesn't confirm MagSafe compatibility with specific case
- Mechanical assertions: requirements checklist contains existing hardware entry
- Human assertions: OtterBox Defender Series Pro MagSafe compatibility confirmed before research; variant-level verification noted

**Test 13 — Stretch pick**
- Prompt: "Best 4K monitors under $400, US" [where the best option is $449]
- Failure mode: over-budget product included silently without stretch pick flag
- Mechanical assertions: if any product >15% over budget, verdict badge contains "OVER BUDGET"; product name contains ⚠ in rankings table
- Human assertions: stretch pick framing in card copy; not presented as equal to in-budget options

**Test 14 — Hardest combined scenario**
- Prompt: "Refresh my standing desk guide from 6 months ago, UK" [provide mock original guide with one discontinued product and one new entrant]
- Failure mode: misses UK non-Amazon price history; uses US Track C sources; skips spot-check; doesn't update rankings when order changes
- Mechanical assertions: currency GBP; banner contains "Updated"; discontinued product removed or flagged
- Human assertions: UK retailers used; Track C uses furniture-appropriate sources; rankings updated if order changed; Track C spot-check performed

**Test 15 — Baseline correctness**
- Prompt: "Best wireless gaming headsets under $150, US"
- Failure mode: any mechanical rule violation on a clean, uncomplicated request
- Mechanical assertions:
  - Product count between 4 and 6
  - Every product has exactly 2 links (product + price)
  - Every product has a Price History row
  - Every product has a Strengths and Weaknesses section
  - All ratings between 5.0 and 10.0
  - Banner meta contains budget, date, and location
  - Disclaimer present with "no affiliate tracking"

---

## Implementation Order (Claude Code)

1. **Read this document**
2. **Unpack the live buyers-guide.skill** from `/mnt/skills/user/buyers-guide/`
3. **Create the new file structure** in `/home/claude/buyers-guide-refactor/`
   - Write SKILL.md (~200 lines, orchestration only)
   - Write references/research.md (~250 lines, Tracks A–F content)
   - Write rules.md (~200 lines, scoring + business logic)
   - Copy template-structure.md unchanged
4. **Verify line counts** — SKILL.md must be under 250 lines, no Critical Rules list
5. **Write buyers-guide-evals.json** using the 15 test cases above in the skill-creator eval format
6. **Run evals against the OLD skill first** — establish baseline failure rate
7. **Pack the refactored skill** as buyers-guide.skill
8. **Run evals against the NEW skill** — confirm same or better pass rate
9. **Present diff summary** — what moved where, line count reduction, eval results

---

## Open Decisions (resolve in Claude Code session)

1. **Self-improvement loop final resting place** — currently in mistakes-log but architecturally wrong. Options: (a) delete it entirely, replaced by evals, (b) move into a standalone skill-reviewer skill that runs after any skill edit. Recommendation: (a) delete, evals are the replacement.

2. **mistakes-log scope** — once the self-improvement loop is removed, mistakes-log returns to its core job: institutional memory read before tasks. The "at the start of a skill editing session, ask for live files" instruction stays. The Self-Improvement Loop section, Steps 1–3, and the Self-Improvement Process category of mistakes entries can all be removed or condensed significantly.

3. **Agent conversion trigger** — when to convert the refactored skill to a proper agent with a research subagent. Suggested trigger: when a second real-world guide fails Track A research (misses obvious candidates). One failure could be a prompt issue; two is a structural issue.

---

## Files to Carry Forward

Upload these to Claude Code to start:
- This handoff document
- The live buyers-guide.skill (current state)
- The live mistakes-log.skill (current state)
- The skill-designer-SKILL.md (produced this session — upload to `/mnt/skills/user/skill-designer/SKILL.md`)

---

## Design Rationale

*Why the architecture is the way it is. Read this before questioning any decision.*

### Why the self-improvement loop is being deleted, not moved

The self-improvement loop evolved through six iterations in a single session:
1. Checklist of gap questions
2. Adversarial scenario simulation
3. Four fixed mandatory scenarios
4. Five exhaustive audits
5. Explicit cross-checking of new rules against each other
6. Audit 2 extended to cover all sections, not just research tracks

Each iteration was triggered by the previous one failing. After all six iterations, the loop still missed the Micro Center gap — one of the most important failures of the entire session.

The reason: self-review has a hard ceiling. The loop can only check for failure patterns Claude already knows to look for. The Micro Center gap wasn't caught because "Micro Center exists and has exclusive products not in editorial roundups" was not a known failure pattern until the guide was actually run. No amount of self-review would have surfaced it in advance.

Evals catch real failures. Test 1 — a prompt for a prebuilt PC where Micro Center has the best option — would have caught this failure on the first run, before the guide was delivered. The self-improvement loop is an elaborate substitute for evals that will always have blind spots the eval system wouldn't.

**The replacement:** The 15-test eval set in this document. Run it after every significant skill change. If a new failure mode is discovered in production, add a test case for it. That is the correct improvement loop — not self-review, but test coverage that grows with discovered failures.

### Why the Critical Rules list is being eliminated, not cleaned up

The 36 Critical Rules at the bottom of SKILL.md each started as a real failure. Rule 22 ("always include Price History row") was added after a guide was delivered without one. Rule 36 ("safety recall is a hard exclusion") was added after the interaction between recall exclusion and product count minimum was undefined.

Each rule was added as a patch at the end of the file rather than as a fix to the workflow step where the failure occurred. The result: Rule 22 applies during Step 4 and Component 8, but lives at line 727. Rule 36 applies during Track E and Step 4, but lives at line 741.

A rule at line 727 that is needed at Step 3 will not be read at Step 3. During execution, Claude reads the relevant section of the skill. It does not re-read the entire file before each step. Rules disconnected from their workflow step are rules that will be forgotten — which is exactly what happened repeatedly during guide generation.

**The fix:** Every rule is embedded in the workflow step or reference file where it applies. If a rule applies in two places, it lives in the reference file that covers both. The Critical Rules list is not cleaned up or reorganized — it is eliminated entirely. Its contents are redistributed into context.

### Why the file grew to 741 lines and what prevented earlier refactoring

The skill grew reactively. Each session identified a gap, the gap got a fix, the fix got appended. This is the skill equivalent of spaghetti code — each individual change was locally correct, but the accumulated structure became incoherent.

What prevented earlier refactoring: there was no design review before building. The first question asked before each session should have been "what is the single job of this skill?" — which would have revealed the research/ranking/generation split immediately. The skill-designer skill built this session exists to prevent this pattern on future skills.

### Why research.md and rules.md are separate files, not one references file

Research methodology and business logic change for different reasons and at different rates:

- **research.md** changes when new product categories are added, when new regional sources are discovered, or when Track A misses candidates from a new channel. It is updated by experience with real guides.
- **rules.md** changes when edge cases are discovered that require new business logic (a new type of budget situation, a new edge case in scoring). It changes less frequently and only when a real scenario exposes an undefined case.

Keeping them separate means a Track C source addition (research.md) doesn't require re-reading scoring methodology (rules.md), and vice versa. Claude reads only what's relevant to the current phase.

### Why this is being implemented as a skill refactor now rather than an agent

True agent architecture — with a research subagent that has an independent output contract — would structurally prevent the "stop at three familiar names" failure. The research agent's contract would require: minimum candidate pool size, retailer-specific searches completed, community sources checked. A subagent cannot skip these without failing to return a valid result.

The refactored skill with research.md as a reference file is a skill-world approximation of this. It gets most of the benefit: Claude reads research.md at the start of Step 3 and follows its instructions, including the retailer-specific search requirement. It doesn't get the structural guarantee that a subagent with an output contract provides.

The agent conversion is deferred because:
1. The refactor is the prerequisite — a well-structured skill is easier to convert to an agent than a monolith
2. The eval system needs to be in place first — you need a way to verify the agent produces better results than the skill
3. One real-world failure doesn't confirm the need; two does

**Trigger for conversion:** If a second real-world guide fails Track A research (misses obvious candidates despite the retailer-specific search instruction), that confirms a structural problem that only an output-contract subagent can solve. One failure could be execution; two is architecture.
