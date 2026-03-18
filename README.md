# Buyer's Guide

**Objectivity. No bias. Depth and breadth.**

A multi-agent pipeline that produces professional buyer's guide PDFs for any product category. The pipeline is designed to give buyers an honest answer to "what should I buy?" derived entirely from evidence — measured performance, verified specifications, and real owner experience — with no influence from marketing spend, editorial relationships, or name recognition.

The architecture was built around a specific failure mode: editorial "best of" lists are optimized for SEO and affiliate revenue, not truth. Retailer-exclusive products — often the best value in a category — are systematically invisible to generic editorial searches. This tool is structured to find them.

See [`docs/principles.md`](docs/principles.md) for the full product premise and the standards that govern how this pipeline is built and maintained.

---

## How it works

Run `/buyers-guide <request>` in Claude Code. The pipeline handles the rest:

1. **Intake** — conversational requirements gathering (category, budget, region, city/state, hard filters, use case), outputs `requirements.json`
2. **Research Orchestrator** — Track A discovers retailers through process (not a fixed list), verifies physical store locations near the user's city before claiming in-store availability, builds a candidate pool, then spawns four parallel subagents (B–E) for community intel, spec verification, price intelligence, and availability/recalls. Track F does per-product live price and availability verification using Playwright.
3. **Track D** — finds every retailer carrying each product (not just the cheapest), verifies all prices and stock live via Playwright, and records all verified purchase options within budget. The guide shows multiple buy links per product sorted by price. In-store retailers are verified against the nearest actual store location to the user's city/state via the retailer's store locator.
4. **Scoring** — applies a five-factor weighted methodology (30/25/20/15/10), flags edge cases. Spec integrity is derived from per-spec verification data — each spec carries its own status (`verified`, `diverges`, `no_source`, `inconclusive`), claimed value, measured value, and source URL.
5. **Generation** — writes `guide.js`, runs it, converts to PDF via LibreOffice
6. **Evals** — validates every output contract after generation

Every stage boundary is validated against a JSON schema. A malformed output from one stage cannot silently corrupt the next.

---

## File structure

```
buyer-guide/
├── CLAUDE.md                        # /buyers-guide command wiring + dev principles
├── docs/
│   └── principles.md                # Product premise, bias/determinism standards
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
│   │   ├── scored_products.schema.json
│   │   └── research_log.schema.json
│   ├── tests/
│   │   └── test_validate.py         # 31 schema validation tests
│   ├── validate.py                  # Schema validation between stages
│   └── requirements.txt
├── references/
│   ├── research.md                  # Research methodology (Tracks A–F)
│   ├── rules.md                     # Scoring rules and edge cases
│   └── template-structure.md       # Document generation template
├── evals/
│   ├── contract-evals.json          # 10 contract validation tests
│   ├── runner.py                    # Eval runner
│   └── tests/
│       └── test_runner.py
├── guides/                          # PDF output (gitignored)
└── runs/                            # Per-run JSON contracts (gitignored)
    └── YYYY-MM-DDTHHMMSS/
        ├── requirements.json
        ├── research_foundation.json
        ├── candidate_pool.json
        ├── scored_products.json
        ├── research_log.json        # Audit trail: all searches + Playwright fetches
        └── screenshots/             # Playwright screenshots per product per retailer
```

---

## Agent contracts

| Stage | Input | Output |
|---|---|---|
| Intake | User conversation | `requirements.json` |
| Research Orchestrator | `requirements.json` | `research_foundation.json`, `candidate_pool.json` |
| Scoring | `candidate_pool.json` | `scored_products.json` |
| Generation | `scored_products.json` | `guides/[category-slug]-[YYYY-MM-DD].pdf` |

---

## Setup

```bash
pip install -r agents/requirements.txt
brew install node
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

---

## Web app migration

Each agent's instruction file becomes a system prompt in an Anthropic SDK API call. The JSON schemas become structured output formats. The orchestrator's parallel subagent spawning becomes `asyncio.gather()`. The eval runner runs against the API pipeline unchanged.
