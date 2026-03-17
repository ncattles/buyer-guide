# Buyer's Guide Skills

Claude.ai skills for generating professional product buyer's guides — research methodology, scoring logic, and PDF document generation.

## Skills

### `buyers-guide.skill`
Produces a comprehensive buyer's guide PDF for any consumer product category. Given a category, budget, and region, it runs six research tracks (category landscape, community intelligence, spec verification, price history, availability/lifecycle, per-product verification), scores each product using a five-factor weighted methodology, and generates a formatted PDF with ratings, spec tables, pros/cons, price history, and final recommendations.

### `mistakes-log.skill`
Institutional memory. Logs mistakes made during past sessions and surfaces relevant ones before starting a task.

### `skill-designer-SKILL.md`
Skill for designing new skills — defines the architecture and review process for building well-structured Claude.ai skills.

## File Structure

```
buyers-guide.skill          # Upload to Claude.ai
mistakes-log.skill          # Upload to Claude.ai
skill-designer-SKILL.md     # Upload to Claude.ai
buyers-guide-refactored/
├── buyers-guide-evals.json     # 15-test eval set
└── buyers-guide/
    ├── SKILL.md                # Orchestration (~178 lines)
    ├── template-structure.md   # Document generation code (unchanged)
    └── references/
        ├── research.md         # Tracks A–F + output contract
        └── rules.md            # Scoring, edge cases, business logic
```

## Architecture

`SKILL.md` is orchestration only — it describes the workflow and tells Claude when to read each reference file. Content lives where it is applied:

- Research rules → `references/research.md`, read at Step 3
- Scoring and business logic → `references/rules.md`, read at Step 4
- Document generation → `template-structure.md`, read at Step 5

## Eval Set

`buyers-guide-evals.json` contains 15 test cases covering the most common failure modes: retailer-exclusive product discovery, regional source selection, safety recall handling, contradictory requirements, mid-research requirement changes, naming variant traps, stretch picks, and baseline correctness.
