# Buyer's Guide — Claude Code Project

## Development principles

**Read `docs/principles.md` before modifying any methodology, instruction, or schema file.** It defines the product premise (objectivity, no bias, depth and breadth through process) and the standards that govern how this pipeline is built.

Short version:

- **Structural fixes over behavioral patches.** Can this failure be caught by a schema, contract field, or eval assertion? If yes, enforce it structurally. Instructions can be ignored; contracts cannot.
- **No hardcoded names in methodology.** Named retailers, brands, or editorial publications in instruction files create selection ceilings. Replace with the process that would discover them.
- **Evals test process, not outputs.** A test that checks for a specific brand name is a regression patch, not a process test.

Before merging any change, ask: *does this instruction work for a product category I've never heard of?* If no, it doesn't belong in shared methodology.

---

## /buyers-guide

**Trigger:** When the user runs `/buyers-guide` followed by a product request.

### What this command does

Runs a multi-agent pipeline to produce a professional buyer's guide PDF.

### Agent instruction files

| Stage | Instructions |
|---|---|
| Intake | Main conversation — gather requirements, write `requirements.json` |
| Research Orchestrator | `agents/instructions/research-orchestrator.md` |
| Track B subagent | `agents/instructions/track-b.md` |
| Track C subagent | `agents/instructions/track-c.md` |
| Track D subagent | `agents/instructions/track-d.md` |
| Track E subagent | `agents/instructions/track-e.md` |
| Scoring | `agents/instructions/scoring.md` |
| Generation | `agents/instructions/generation.md` |

### Reference files

| Purpose | File |
|---|---|
| Research methodology (Tracks A–F) | `references/research.md` |
| Scoring rules and edge cases | `references/rules.md` |
| Document generation template | `references/template-structure.md` |

### Output locations

| Output | Location |
|---|---|
| Run contracts (JSON) | `runs/YYYY-MM-DDTHHMMSS/` |
| PDF guides | `guides/[category-slug]-[YYYY-MM-DD].pdf` |

### Pipeline — step by step

1. **Intake** — conversationally gather: category, budget, region, hard filters, existing hardware (or null), use case. Set `intake_complete: true` only when all fields are explicitly confirmed.

   **Do not pre-warn about budget feasibility based on component prices or assumptions.** Accept the user's budget and proceed to research. Budget shortfalls surface naturally: Track A reports nothing found under budget, or scoring flags all products over budget. Only raise budget concerns if research confirms them — not before.

2. **Write requirements.json** — create `runs/[timestamp]/requirements.json` with the confirmed requirements. Validate:
   ```bash
   python agents/validate.py runs/[timestamp]/requirements.json agents/schemas/requirements.schema.json
   ```

3. **Research** — spawn Research Orchestrator agent with instructions from `agents/instructions/research-orchestrator.md`. Pass the run directory path. Wait for `research_foundation.json` and `candidate_pool.json` to be written and validated.

4. **Score** — spawn Scoring Agent with instructions from `agents/instructions/scoring.md`. Pass the run directory path. Wait for `scored_products.json` to be written and validated.

5. **Check for edge cases** — read `scored_products.json`. If `edge_cases_requiring_user_input` is non-empty, surface each to the user and wait for resolution before generating.

6. **Generate** — spawn Generation Agent with instructions from `agents/instructions/generation.md`. Pass the run directory path and output path `guides/[category-slug]-[YYYY-MM-DD].pdf`.

7. **Run evals** — after generation completes:
   ```bash
   python evals/runner.py runs/[timestamp]/
   ```
   Report results to the user.

### Run directory structure

Create at the start of each guide run:
```
runs/
└── YYYY-MM-DDTHHMMSS/
    ├── requirements.json        ← written after intake
    ├── research_foundation.json ← written by Research Orchestrator (Track A)
    ├── candidate_pool.json      ← written by Research Orchestrator (after B–F)
    └── scored_products.json     ← written by Scoring Agent
```

Create the run directory with:
```bash
mkdir -p runs/$(date +%Y-%m-%dT%H%M%S)
```

### Dependency check

Before the first run, verify:
```bash
node --version
python3 --version
python3 -c "import jsonschema"
which soffice || which libreoffice
```

Install if missing:
- Node.js: `brew install node`
- LibreOffice: `brew install --cask libreoffice`
- jsonschema: `pip install -r agents/requirements.txt`
