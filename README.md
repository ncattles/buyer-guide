# Buyer's Guide

A multi-agent pipeline that produces professional buyer's guide PDFs. Runs entirely in Claude Code. Designed to migrate to the Anthropic SDK as a web app with no redesign required.

## How it works

Run `/buyers-guide <request>` in Claude Code. The pipeline handles the rest:

1. **Intake** — conversational requirements gathering, outputs `requirements.json`
2. **Research Orchestrator** — Track A enumerates retailers and builds a candidate pool, then spawns four parallel subagents (B–E) for community intel, spec verification, price intelligence, and availability/recalls. Track F does per-product verification.
3. **Scoring** — applies a five-factor weighted methodology, flags edge cases
4. **Generation** — writes `guide.js`, runs it, converts to PDF via LibreOffice
5. **Evals** — validates every output contract after generation

Every stage boundary is validated against a JSON schema. A malformed output from one stage cannot silently corrupt the next.

## File structure

```
buyer-guide/
├── CLAUDE.md                        # /buyers-guide command wiring
├── agents/
│   ├── instructions/
│   │   ├── research-orchestrator.md
│   │   ├── track-b.md               # Community & owner intel
│   │   ├── track-c.md               # Spec verification
│   │   ├── track-d.md               # Price intelligence
│   │   ├── track-e.md               # Availability & recalls
│   │   ├── scoring.md
│   │   └── generation.md
│   ├── schemas/
│   │   ├── requirements.schema.json
│   │   ├── research_foundation.schema.json
│   │   ├── candidate_pool.schema.json
│   │   └── scored_products.schema.json
│   ├── tests/
│   │   └── test_validate.py         # 11 schema validation tests
│   ├── validate.py                  # Schema validation between stages
│   └── requirements.txt
├── references/
│   ├── research.md                  # Research methodology (Tracks A–F)
│   ├── rules.md                     # Scoring rules and edge cases
│   └── template-structure.md       # Document generation template
├── evals/
│   ├── contract-evals.json          # 9 contract validation tests
│   ├── runner.py                    # Eval runner
│   └── tests/
│       └── test_runner.py
├── guides/                          # PDF output (gitignored)
├── runs/                            # Per-run JSON contracts (gitignored)
└── docs/
    └── plans/
        ├── 2026-03-17-agent-architecture-design.md
        └── 2026-03-17-agent-architecture-implementation.md
```

## Agent contracts

| Stage | Input | Output |
|---|---|---|
| Intake | User conversation | `requirements.json` |
| Research Orchestrator | `requirements.json` | `research_foundation.json`, `candidate_pool.json` |
| Scoring | `candidate_pool.json` | `scored_products.json` |
| Generation | `scored_products.json` | `guides/[category-slug]-[YYYY-MM-DD].pdf` |

## Setup

```bash
# Python deps
pip install -r agents/requirements.txt

# Node (for guide.js generation)
brew install node

# LibreOffice (for PDF conversion)
brew install --cask libreoffice
```

## Running tests

```bash
python -m pytest agents/tests/ evals/tests/ -v
```

## Running evals after a guide

```bash
python evals/runner.py runs/[timestamp]/
```

## Web app migration

Each agent's instruction file becomes a system prompt in an Anthropic SDK API call. The JSON schemas become structured output formats. The orchestrator's parallel subagent spawning becomes `asyncio.gather()`. The eval runner runs against the API pipeline unchanged.
