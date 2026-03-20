# Buyers Guide Agent Architecture — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the buyers-guide skill monolith with a Claude Code agent pipeline — Research Orchestrator (with parallel Community Research / Spec Verification / Price Research / Lifecycle Check subagents), Scoring Agent, and Generation Agent — with validated output contracts between every stage.

**Architecture:** Intake happens conversationally in the main Claude Code session. A `/buyers-guide` command triggers the pipeline. Each stage writes a validated JSON contract to `runs/[timestamp]/` before the next stage begins. The Research Orchestrator's first output is a retailer enumeration list — the structural fix for the Candidate Discovery research ceiling.

**Tech Stack:** Python 3, `jsonschema`, Anthropic Claude Sonnet 4.6 (via Claude Code Agent tool), Node.js (guide.js generation), LibreOffice (PDF conversion)

**Design doc:** `docs/plans/2026-03-17-agent-architecture-design.md`

---

## Phase 1: Foundation — Schemas + Validation

> These must exist before any agent code. Contracts are defined by schemas; agents are built to satisfy them.

---

### Task 1: Set up Python environment

**Files:**
- Create: `agents/requirements.txt`

**Step 1: Create requirements file**

```
jsonschema==4.23.0
```

**Step 2: Install**

```bash
pip install -r agents/requirements.txt
```

Expected: `Successfully installed jsonschema-4.23.0`

**Step 3: Verify**

```bash
python -c "import jsonschema; print(jsonschema.__version__)"
```

Expected: `4.23.0`

**Step 4: Commit**

```bash
git add agents/requirements.txt
git commit -m "feat: add Python deps for schema validation"
```

---

### Task 2: Write requirements.schema.json

**Files:**
- Create: `agents/schemas/requirements.schema.json`

**Step 1: Write schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Requirements",
  "type": "object",
  "required": ["category", "budget", "region", "hard_filters", "intake_complete"],
  "properties": {
    "category": { "type": "string", "minLength": 1 },
    "budget": {
      "type": "object",
      "required": ["amount", "currency", "format"],
      "properties": {
        "amount": { "type": "number", "minimum": 0 },
        "currency": { "type": "string", "minLength": 3, "maxLength": 3 },
        "format": { "type": "string", "minLength": 1 }
      }
    },
    "region": { "type": "string", "minLength": 1 },
    "hard_filters": { "type": "array", "items": { "type": "string" } },
    "existing_hardware": { "type": ["string", "null"] },
    "use_case": { "type": "string" },
    "intake_complete": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

**Step 2: Write a passing sample and a failing sample for manual verification**

Passing:
```json
{
  "category": "wireless gaming headsets",
  "budget": { "amount": 150, "currency": "USD", "format": "under $150" },
  "region": "US",
  "hard_filters": ["wireless"],
  "existing_hardware": null,
  "use_case": "competitive FPS gaming",
  "intake_complete": true
}
```

Failing (missing `intake_complete`):
```json
{
  "category": "wireless gaming headsets",
  "budget": { "amount": 150, "currency": "USD", "format": "under $150" },
  "region": "US",
  "hard_filters": []
}
```

**Step 3: Commit**

```bash
git add agents/schemas/requirements.schema.json
git commit -m "feat: add requirements contract schema"
```

---

### Task 3: Write research_foundation.schema.json

**Files:**
- Create: `agents/schemas/research_foundation.schema.json`

**Step 1: Write schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ResearchFoundation",
  "type": "object",
  "required": ["retailers", "category_sources", "editorial_sources_found", "candidates"],
  "properties": {
    "retailers": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 3,
      "description": "All retailers carrying this category in this region"
    },
    "category_sources": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "editorial_sources_found": {
      "type": "array",
      "items": { "type": "string" }
    },
    "candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "source", "source_type"],
        "properties": {
          "name": { "type": "string", "minLength": 1 },
          "source": { "type": "string", "minLength": 1 },
          "source_type": {
            "type": "string",
            "enum": ["editorial", "retailer", "community", "manufacturer"]
          }
        }
      },
      "minItems": 1
    }
  },
  "additionalProperties": false
}
```

**Step 2: Verify schema has retailer minimum enforced**

The `retailers` array has `"minItems": 3` — this is the structural enforcement for the retailer enumeration fix. A schema validation failure here means Candidate Discovery is incomplete.

**Step 3: Commit**

```bash
git add agents/schemas/research_foundation.schema.json
git commit -m "feat: add research_foundation contract schema"
```

---

### Task 4: Write candidate_pool.schema.json

**Files:**
- Create: `agents/schemas/candidate_pool.schema.json`

**Step 1: Write schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CandidatePool",
  "type": "object",
  "required": ["candidates"],
  "properties": {
    "candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "community_research", "spec_verification", "price_research", "lifecycle_check", "final_verification", "safety_flag"],
        "properties": {
          "name": { "type": "string" },
          "community_research": {
            "type": "object",
            "required": ["community_sentiment", "confirmed_issues", "sources"],
            "properties": {
              "community_sentiment": { "type": "string", "enum": ["positive", "mixed", "negative", "insufficient_data"] },
              "confirmed_issues": { "type": "array", "items": { "type": "string" } },
              "sources": { "type": "array", "items": { "type": "string" } }
            }
          },
          "spec_verification": {
            "type": "object",
            "required": ["spec_integrity", "conditional_specs", "measurement_sources", "flags"],
            "properties": {
              "spec_integrity": { "type": "string", "enum": ["verified", "diverges", "unverified"] },
              "conditional_specs": { "type": "array", "items": { "type": "string" } },
              "measurement_sources": { "type": "array", "items": { "type": "string" } },
              "flags": { "type": "array", "items": { "type": "string" } }
            }
          },
          "price_research": {
            "type": "object",
            "required": ["current_price", "currency", "retailer", "price_history", "sale_eligible", "consider_waiting"],
            "properties": {
              "current_price": { "type": "number" },
              "currency": { "type": "string" },
              "retailer": { "type": "string" },
              "price_history": { "type": "string" },
              "sale_eligible": { "type": "boolean" },
              "consider_waiting": {}
            }
          },
          "lifecycle_check": {
            "type": "object",
            "required": ["recall_status", "lifecycle_status"],
            "properties": {
              "recall_status": { "type": "string", "enum": ["clear", "recalled", "check_failed"] },
              "recall_source": { "type": ["string", "null"] },
              "lifecycle_status": { "type": "string", "enum": ["current", "discontinued", "successor_imminent", "successor_announced"] }
            }
          },
          "final_verification": {
            "type": "object",
            "required": ["model_verified", "url_verified", "regional_spec_match"],
            "properties": {
              "model_verified": { "type": "boolean" },
              "url_verified": { "type": "boolean" },
              "regional_spec_match": { "type": "boolean" },
              "notes": { "type": ["string", "null"] }
            }
          },
          "safety_flag": { "type": "boolean" }
        }
      },
      "minItems": 1,
      "maxItems": 15
    }
  },
  "additionalProperties": false
}
```

**Step 2: Commit**

```bash
git add agents/schemas/candidate_pool.schema.json
git commit -m "feat: add candidate_pool contract schema"
```

---

### Task 5: Write scored_products.schema.json

**Files:**
- Create: `agents/schemas/scored_products.schema.json`

**Step 1: Write schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ScoredProducts",
  "type": "object",
  "required": ["ranked_products", "guide_meta"],
  "properties": {
    "ranked_products": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "rank", "score", "score_breakdown", "flags"],
        "properties": {
          "name": { "type": "string" },
          "rank": { "type": "integer", "minimum": 1 },
          "score": { "type": "number", "minimum": 0, "maximum": 10 },
          "score_breakdown": {
            "type": "object",
            "required": ["price_to_value", "spec_integrity", "community_reception", "feature_quality", "availability"],
            "properties": {
              "price_to_value": { "type": ["number", "null"] },
              "spec_integrity": { "type": ["number", "null"] },
              "community_reception": { "type": ["number", "null"] },
              "feature_quality": { "type": ["number", "null"] },
              "availability": { "type": ["number", "null"] },
              "na_factors": { "type": "array", "items": { "type": "string" } }
            }
          },
          "penalties": { "type": "array", "items": { "type": "string" } },
          "flags": {
            "type": "object",
            "required": ["safety_excluded", "stretch_pick", "dominant_winner", "consider_waiting", "all_below_6"],
            "properties": {
              "safety_excluded": { "type": "boolean" },
              "stretch_pick": { "type": "boolean" },
              "dominant_winner": { "type": "boolean" },
              "consider_waiting": {},
              "all_below_6": { "type": "boolean" }
            }
          }
        }
      },
      "minItems": 0
    },
    "guide_meta": {
      "type": "object",
      "required": ["product_count", "category_type", "category_type_rationale"],
      "properties": {
        "product_count": { "type": "integer", "minimum": 0 },
        "category_type": { "type": "string", "enum": ["focused", "broad", "competitive"] },
        "category_type_rationale": { "type": "string", "minLength": 1 },
        "edge_cases_requiring_user_input": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "additionalProperties": false
}
```

**Step 2: Commit**

```bash
git add agents/schemas/scored_products.schema.json
git commit -m "feat: add scored_products contract schema"
```

---

### Task 6: Write validate.py

**Files:**
- Create: `agents/validate.py`
- Create: `agents/tests/test_validate.py`

**Step 1: Write failing test**

```python
# agents/tests/test_validate.py
import pytest
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from validate import validate_contract, ValidationError

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), '..', 'schemas')

def test_valid_requirements_passes():
    data = {
        "category": "wireless gaming headsets",
        "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
        "region": "US",
        "hard_filters": ["wireless"],
        "existing_hardware": None,
        "use_case": "gaming",
        "intake_complete": True
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'requirements.schema.json'))

def test_missing_intake_complete_fails():
    data = {
        "category": "wireless gaming headsets",
        "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
        "region": "US",
        "hard_filters": []
    }
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'requirements.schema.json'))

def test_research_foundation_requires_three_retailers():
    data = {
        "retailers": ["Amazon", "Best Buy"],  # only 2 — should fail
        "category_sources": ["RTings"],
        "editorial_sources_found": [],
        "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer"}]
    }
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))

def test_research_foundation_with_three_retailers_passes():
    data = {
        "retailers": ["Amazon", "Best Buy", "Micro Center"],
        "category_sources": ["RTings"],
        "editorial_sources_found": ["Wirecutter"],
        "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer"}]
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))
```

**Step 2: Run — verify it fails**

```bash
cd agents && python -m pytest tests/test_validate.py -v
```

Expected: `ImportError: cannot import name 'validate_contract'`

**Step 3: Write validate.py**

```python
# agents/validate.py
import json
import jsonschema


class ValidationError(Exception):
    pass


def validate_contract(data: dict, schema_path: str) -> None:
    """Validate data against a JSON schema file. Raises ValidationError on failure."""
    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"Contract validation failed: {e.message}") from e


def validate_file(json_path: str, schema_path: str) -> None:
    """Load a JSON file and validate it against a schema."""
    with open(json_path) as f:
        data = json.load(f)
    validate_contract(data, schema_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python validate.py <json_file> <schema_file>")
        sys.exit(1)
    try:
        validate_file(sys.argv[1], sys.argv[2])
        print(f"✓ {sys.argv[1]} is valid")
    except ValidationError as e:
        print(f"✗ {e}")
        sys.exit(1)
```

**Step 4: Run — verify tests pass**

```bash
cd agents && python -m pytest tests/test_validate.py -v
```

Expected: `4 passed`

**Step 5: Commit**

```bash
git add agents/validate.py agents/tests/test_validate.py
git commit -m "feat: add contract schema validator with tests"
```

---

## Phase 2: Eval Runner

---

### Task 7: Write runner.py

**Files:**
- Create: `evals/runner.py`
- Create: `evals/contract-evals.json`

**Step 1: Write contract-evals.json**

```json
{
  "eval_set": "buyers-guide-contracts",
  "version": "1.0",
  "description": "Validates that agent output files conform to their schemas. Run after a guide generation.",
  "tests": [
    {
      "id": "C1",
      "name": "requirements.json is valid",
      "file": "requirements.json",
      "schema": "agents/schemas/requirements.schema.json",
      "required": true
    },
    {
      "id": "C2",
      "name": "research_foundation.json is valid",
      "file": "research_foundation.json",
      "schema": "agents/schemas/research_foundation.schema.json",
      "required": true
    },
    {
      "id": "C3",
      "name": "research_foundation has 3+ retailers",
      "file": "research_foundation.json",
      "assertion": "len(data['retailers']) >= 3",
      "required": true
    },
    {
      "id": "C4",
      "name": "research_foundation has non-editorial source",
      "file": "research_foundation.json",
      "assertion": "any(c['source_type'] != 'editorial' for c in data['candidates'])",
      "required": true
    },
    {
      "id": "C5",
      "name": "candidate_pool.json is valid",
      "file": "candidate_pool.json",
      "schema": "agents/schemas/candidate_pool.schema.json",
      "required": true
    },
    {
      "id": "C6",
      "name": "all candidates have safety_flag set",
      "file": "candidate_pool.json",
      "assertion": "all('safety_flag' in c for c in data['candidates'])",
      "required": true
    },
    {
      "id": "C7",
      "name": "scored_products.json is valid",
      "file": "scored_products.json",
      "schema": "agents/schemas/scored_products.schema.json",
      "required": true
    },
    {
      "id": "C8",
      "name": "scored products between 3 and 6",
      "file": "scored_products.json",
      "assertion": "3 <= data['guide_meta']['product_count'] <= 6",
      "required": true
    },
    {
      "id": "C9",
      "name": "category_type_rationale is present",
      "file": "scored_products.json",
      "assertion": "len(data['guide_meta']['category_type_rationale']) > 0",
      "required": true
    }
  ]
}
```

**Step 2: Write runner.py**

```python
#!/usr/bin/env python3
# evals/runner.py
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.validate import validate_contract, ValidationError


def run_evals(run_dir: str, eval_file: str) -> dict:
    """
    Run contract evals against a completed guide run directory.
    run_dir: path to runs/[timestamp]/ containing output JSON files
    eval_file: path to contract-evals.json
    """
    with open(eval_file) as f:
        eval_set = json.load(f)

    results = {"passed": [], "failed": [], "skipped": []}

    for test in eval_set["tests"]:
        file_path = os.path.join(run_dir, test["file"])

        if not os.path.exists(file_path):
            if test.get("required"):
                results["failed"].append({
                    "id": test["id"],
                    "name": test["name"],
                    "reason": f"Required file not found: {test['file']}"
                })
            else:
                results["skipped"].append(test["id"])
            continue

        with open(file_path) as f:
            data = json.load(f)

        # Schema validation
        if "schema" in test:
            schema_path = os.path.join(os.path.dirname(__file__), '..', test["schema"])
            try:
                validate_contract(data, schema_path)
            except ValidationError as e:
                results["failed"].append({"id": test["id"], "name": test["name"], "reason": str(e)})
                continue

        # Assertion check
        if "assertion" in test:
            try:
                passed = eval(test["assertion"], {"data": data})
                if not passed:
                    results["failed"].append({
                        "id": test["id"],
                        "name": test["name"],
                        "reason": f"Assertion failed: {test['assertion']}"
                    })
                    continue
            except Exception as e:
                results["failed"].append({"id": test["id"], "name": test["name"], "reason": str(e)})
                continue

        results["passed"].append(test["id"])

    return results


def print_results(results: dict) -> None:
    total = len(results["passed"]) + len(results["failed"]) + len(results["skipped"])
    print(f"\n{'='*50}")
    print(f"Results: {len(results['passed'])}/{total} passed")
    print(f"{'='*50}")
    for tid in results["passed"]:
        print(f"  ✓ {tid}")
    for item in results["failed"]:
        print(f"  ✗ {item['id']}: {item['name']}")
        print(f"    {item['reason']}")
    if results["skipped"]:
        print(f"  - Skipped: {', '.join(results['skipped'])}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py <run_dir> [eval_file]")
        print("  run_dir:   path to runs/[timestamp]/ directory")
        print("  eval_file: defaults to evals/contract-evals.json")
        sys.exit(1)

    run_dir = sys.argv[1]
    eval_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(__file__), 'contract-evals.json'
    )

    results = run_evals(run_dir, eval_file)
    print_results(results)
    sys.exit(0 if not results["failed"] else 1)
```

**Step 3: Write test for runner**

Create `evals/tests/test_runner.py`:

```python
import json
import os
import tempfile
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from evals.runner import run_evals

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), '../../agents/schemas')
EVALS_FILE = os.path.join(os.path.dirname(__file__), '../contract-evals.json')

def write_valid_run(run_dir):
    """Write all valid contract files to a temp run directory."""
    files = {
        "requirements.json": {
            "category": "wireless gaming headsets",
            "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
            "region": "US", "hard_filters": ["wireless"],
            "existing_hardware": None, "use_case": "gaming", "intake_complete": True
        },
        "research_foundation.json": {
            "retailers": ["Amazon", "Best Buy", "Micro Center"],
            "category_sources": ["RTings"],
            "editorial_sources_found": ["Wirecutter"],
            "candidates": [
                {"name": "SteelSeries Arctis Nova Pro", "source": "RTings", "source_type": "editorial"},
                {"name": "HyperX Cloud III", "source": "Best Buy", "source_type": "retailer"}
            ]
        },
        "candidate_pool.json": {
            "candidates": [{
                "name": "SteelSeries Arctis Nova Pro",
                "community_research": {"community_sentiment": "positive", "confirmed_issues": [], "sources": ["reddit.com/r/headphones"]},
                "spec_verification": {"spec_integrity": "verified", "conditional_specs": [], "measurement_sources": ["rtings.com"], "flags": []},
                "price_research": {"current_price": 149, "currency": "USD", "retailer": "Amazon", "price_history": "Typically $130-150", "sale_eligible": False, "consider_waiting": False},
                "lifecycle_check": {"recall_status": "clear", "recall_source": None, "lifecycle_status": "current"},
                "final_verification": {"model_verified": True, "url_verified": True, "regional_spec_match": True, "notes": None},
                "safety_flag": False
            }]
        },
        "scored_products.json": {
            "ranked_products": [{
                "name": "SteelSeries Arctis Nova Pro", "rank": 1, "score": 8.5,
                "score_breakdown": {"price_to_value": 8, "spec_integrity": 9, "community_reception": 8, "feature_quality": 9, "availability": 9, "na_factors": []},
                "penalties": [],
                "flags": {"safety_excluded": False, "stretch_pick": False, "dominant_winner": False, "consider_waiting": False, "all_below_6": False}
            }],
            "guide_meta": {
                "product_count": 4, "category_type": "competitive",
                "category_type_rationale": "Wide market with 10+ options at this price point",
                "edge_cases_requiring_user_input": []
            }
        }
    }
    for filename, data in files.items():
        with open(os.path.join(run_dir, filename), 'w') as f:
            json.dump(data, f)

def test_all_valid_files_pass():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        results = run_evals(run_dir, EVALS_FILE)
        assert not results["failed"], f"Unexpected failures: {results['failed']}"

def test_missing_required_file_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        os.remove(os.path.join(run_dir, "requirements.json"))
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C1" for f in results["failed"])

def test_two_retailers_fails_c3():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "research_foundation.json")) as f:
            data = json.load(f)
        data["retailers"] = ["Amazon", "Best Buy"]  # only 2
        with open(os.path.join(run_dir, "research_foundation.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        failed_ids = [f["id"] for f in results["failed"]]
        assert "C2" in failed_ids or "C3" in failed_ids
```

**Step 4: Run tests**

```bash
cd /path/to/buyer_guide && python -m pytest evals/tests/test_runner.py -v
```

Expected: `3 passed`

**Step 5: Commit**

```bash
git add evals/
git commit -m "feat: add eval runner with contract validation tests"
```

---

## Phase 3: CLAUDE.md + /buyers-guide Command

---

### Task 8: Write CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

**Step 1: Write CLAUDE.md**

```markdown
# Buyer's Guide — Claude Code Project

## /buyers-guide

Trigger: when the user runs `/buyers-guide` followed by a product request.

### What this command does

Runs a multi-agent pipeline to produce a professional buyer's guide PDF.

### Agent instruction files

- Intake: `buyers-guide-refactored/buyers-guide/SKILL.md` (Steps 1–2.5)
- Research Orchestrator: `agents/instructions/research-orchestrator.md`
- Community Research subagent: `agents/instructions/community-research.md`
- Spec Verification subagent: `agents/instructions/spec-verification.md`
- Price Research subagent: `agents/instructions/price-research.md`
- Lifecycle Check subagent: `agents/instructions/lifecycle-check.md`
- Scoring: `agents/instructions/scoring.md`
- Generation: `agents/instructions/generation.md`

### Reference files

- Research methodology: `buyers-guide-refactored/buyers-guide/references/research.md`
- Scoring rules: `buyers-guide-refactored/buyers-guide/references/rules.md`
- Document template: `buyers-guide-refactored/buyers-guide/template-structure.md`

### Output contracts + schemas

- Schemas: `agents/schemas/`
- Validation: `agents/validate.py`
- Run output: `runs/[YYYY-MM-DDTHHMMSS]/`
- PDF output: `guides/[category-slug]-[YYYY-MM-DD].pdf`

### How to run

1. Intake: gather requirements conversationally (Steps 1–2.5 from SKILL.md)
2. Write confirmed requirements to `runs/[timestamp]/requirements.json`
3. Validate: `python agents/validate.py runs/[timestamp]/requirements.json agents/schemas/requirements.schema.json`
4. Spawn Research Orchestrator agent with `agents/instructions/research-orchestrator.md`
5. Validate `research_foundation.json` and `candidate_pool.json` as they are written
6. Spawn Scoring Agent with `agents/instructions/scoring.md`
7. Validate `scored_products.json`
8. Spawn Generation Agent with `agents/instructions/generation.md`
9. Run eval suite: `python evals/runner.py runs/[timestamp]/`

### Run directory structure

Create at start of each guide:
\`\`\`
runs/
└── YYYY-MM-DDTHHMMSS/
    ├── requirements.json
    ├── research_foundation.json
    ├── candidate_pool.json
    └── scored_products.json
\`\`\`
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add CLAUDE.md with /buyers-guide command wiring"
```

---

## Phase 4: Agent Instruction Files

---

### Task 9: Write research-orchestrator.md

**Files:**
- Create: `agents/instructions/research-orchestrator.md`

**Step 1: Write instruction file**

````markdown
# Research Orchestrator

You are the Research Orchestrator for the buyers-guide pipeline. You receive `requirements.json` and produce two output files: `research_foundation.json` (after Candidate Discovery) and `candidate_pool.json` (after all phases complete).

**Read `buyers-guide-refactored/buyers-guide/references/research.md` before doing anything else.**

## Run directory

All files are written to the run directory passed in the task prompt.

## Candidate Discovery — Retailer Enumeration + Candidate Pool

Before searching for any products, produce `research_foundation.json`:

1. Enumerate every retailer that carries this category in the user's region. Include general retailers, specialty retailers, manufacturer-direct, and warehouse clubs. Minimum 3 retailers. At least 1 must be non-editorial.
2. Identify the correct Spec Verification verification sources for this category from `references/research.md`.
3. Search each retailer directly (not just generic queries). Note which candidates came from which source and source type.
4. Build the candidate list. Maximum 15 candidates. If more found, prioritise by source diversity (keep retailer-sourced over editorial duplicates).

Write `research_foundation.json` and validate:
```bash
python agents/validate.py [run_dir]/research_foundation.json agents/schemas/research_foundation.schema.json
```

If validation fails, fix and rewrite before continuing.

**Early exit check:** If candidates < 3, stop. Write a file `shortfall.json` with `{"reason": "...", "candidate_count": N}` and return. Do not spawn parallel subagents.

## Parallel Subagents — Community Research / Spec Verification / Price Research / Lifecycle Check

Spawn all four in parallel, passing the candidate list and run directory to each:

- Community Research agent: `agents/instructions/community-research.md`
- Spec Verification agent: `agents/instructions/spec-verification.md`
- Price Research agent: `agents/instructions/price-research.md`
- Lifecycle Check agent: `agents/instructions/lifecycle-check.md`

Wait for all four to complete.

## Cross-Phase Safety Aggregation + Final Verification

After Community Research / Spec Verification / Price Research / Lifecycle Check return:

1. For each candidate, check ALL phase outputs for safety signals: fire risk, injury, recall, regulatory action in any phase. Set `safety_flag: true` if any found.
2. Run Final Verification (final per-product verification) for each candidate. Instructions in `references/research.md` Final Verification section.
3. Merge all phase data into `candidate_pool.json`.

Write `candidate_pool.json` and validate:
```bash
python agents/validate.py [run_dir]/candidate_pool.json agents/schemas/candidate_pool.schema.json
```

Return when both files are written and validated.
````

**Step 2: Commit**

```bash
git add agents/instructions/research-orchestrator.md
git commit -m "feat: add research orchestrator agent instructions"
```

---

### Task 10: Write subagent instruction files

**Files:**
- Create: `agents/instructions/community-research.md`
- Create: `agents/instructions/spec-verification.md`
- Create: `agents/instructions/price-research.md`
- Create: `agents/instructions/lifecycle-check.md`

**Step 1: Write community-research.md**

````markdown
# Community Research — Community & Owner Intelligence

You receive a candidate list and a run directory. Research community and owner intelligence for each candidate. Write your results to `[run_dir]/community_research_results.json`.

**Read the Community Research section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting.**

## Output format

```json
{
  "results": {
    "[product_name]": {
      "community_sentiment": "positive | mixed | negative | insufficient_data",
      "confirmed_issues": ["each confirmed by 3+ distinct sources"],
      "sources": ["url1", "url2"]
    }
  }
}
```

Write to `[run_dir]/community_research_results.json` when complete.
````

**Step 2: Write spec-verification.md**

````markdown
# Spec Verification — Specification Verification

You receive a candidate list, region, category, and run directory. Verify specs against independent measurements for each candidate. Maximum 8 candidates per run — if more than 8, process the top 8 by research_foundation ranking.

**Read the Spec Verification section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting. Use the category-specific sources listed there.**

## Output format

```json
{
  "results": {
    "[product_name]": {
      "spec_integrity": "verified | diverges | unverified",
      "conditional_specs": ["spec: condition that applies"],
      "measurement_sources": ["url"],
      "flags": ["manufacturer claims X; measured Y"]
    }
  }
}
```

Write to `[run_dir]/spec_verification_results.json` when complete.
````

**Step 3: Write price-research.md**

````markdown
# Price Research — Price Intelligence

You receive a candidate list, region, currency, and run directory. Research current prices and price history for each candidate.

**Read the Price Research section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting. Use the correct price history tool for each retailer.**

## Output format

```json
{
  "results": {
    "[product_name]": {
      "current_price": 149.99,
      "currency": "USD",
      "retailer": "Amazon",
      "price_history": "Typically $130-150; currently near average",
      "sale_eligible": false,
      "consider_waiting": false
    }
  }
}
```

Write to `[run_dir]/price_research_results.json` when complete.
````

**Step 4: Write lifecycle-check.md**

````markdown
# Lifecycle Check — Availability & Lifecycle

You receive a candidate list, region, and run directory. Check recall status and lifecycle for each candidate.

**Read the Lifecycle Check section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting. Use the correct recall database for the user's region.**

## Output format

```json
{
  "results": {
    "[product_name]": {
      "recall_status": "clear | recalled | check_failed",
      "recall_source": "url or null",
      "lifecycle_status": "current | discontinued | successor_imminent | successor_announced"
    }
  }
}
```

Write to `[run_dir]/lifecycle_check_results.json` when complete.
````

**Step 5: Commit**

```bash
git add agents/instructions/community-research.md agents/instructions/spec-verification.md agents/instructions/price-research.md agents/instructions/lifecycle-check.md
git commit -m "feat: add parallel subagent instruction files"
```

---

### Task 11: Write scoring.md

**Files:**
- Create: `agents/instructions/scoring.md`

**Step 1: Write instruction file**

````markdown
# Scoring Agent

You receive `candidate_pool.json`, `requirements.json`, and a run directory. Score every candidate and produce `scored_products.json`.

**Read `buyers-guide-refactored/buyers-guide/references/rules.md` before scoring anything.**

## Process

1. Apply safety override first: any candidate with `safety_flag: true` is excluded. Add to `scored_products.json` with `safety_excluded: true` and score 0.
2. Apply hard filters from `requirements.json`. Remove non-qualifying candidates.
3. Apply budget rule: candidates >15% over budget are stretch picks only.
4. Score each remaining candidate using the five-factor weighted methodology in `rules.md`. Document the breakdown.
5. Apply category type heuristic:
   - `competitive` if candidate pool ≥ 10 AND budget ≥ regional median for category
   - `focused` if hard filters reduce pool to ≤ 5 OR category is inherently narrow
   - `broad` otherwise
   State your rationale explicitly.
6. Apply edge case flags: dominant_winner (≥1.0 gap), all_below_6, consider_waiting.
7. If edge cases require user input before generation can proceed, list them in `edge_cases_requiring_user_input`.

Write `scored_products.json` and validate:
```bash
python agents/validate.py [run_dir]/scored_products.json agents/schemas/scored_products.schema.json
```
````

**Step 2: Commit**

```bash
git add agents/instructions/scoring.md
git commit -m "feat: add scoring agent instruction file"
```

---

### Task 12: Write generation.md + fix local paths

**Files:**
- Create: `agents/instructions/generation.md`
- Modify: `buyers-guide-refactored/buyers-guide/template-structure.md` (audit for `/mnt/` paths)

**Step 1: Audit template-structure.md for Claude.ai path dependencies**

```bash
grep -n "/mnt/" buyers-guide-refactored/buyers-guide/template-structure.md
```

Note every line with `/mnt/` — these need local equivalents.

**Step 2: Write generation.md**

````markdown
# Generation Agent

You receive `scored_products.json`, `requirements.json`, and a run directory. Produce the buyer's guide PDF.

**Read `buyers-guide-refactored/buyers-guide/template-structure.md` before writing any code.**

## Prerequisites check

Before writing guide.js, verify:
```bash
node --version       # must exist
which soffice || which libreoffice  # must exist
```

If either is missing, stop and surface to the user with the install instruction. Do not proceed.

## Process

1. Read `template-structure.md` fully. Use its helper functions — do not rewrite them.
2. Write `guide.js` in the run directory, populating content arrays from `scored_products.json` and `requirements.json`.
3. Output file: `guides/[category-slug]-[YYYY-MM-DD].pdf` (create `guides/` if it doesn't exist).
4. Run:

```bash
node [run_dir]/guide.js
python buyers-guide-refactored/buyers-guide/scripts/validate.py [run_dir]/guide.docx
soffice --headless --convert-to pdf [run_dir]/guide.docx --outdir guides/
```

## Error handling

- Syntax error in guide.js → fix and retry once
- Missing Node module → tell user: `npm install [module]`
- soffice not found → tell user: `brew install --cask libreoffice`
- Validation failure → fix and retry once; surface if still failing
````

**Step 3: Commit**

```bash
git add agents/instructions/generation.md
git commit -m "feat: add generation agent instruction file"
```

---

## Phase 5: End-to-End Test

---

### Task 13: Create runs/ and guides/ directories + run first guide

**Files:**
- Create: `runs/.gitkeep`
- Create: `guides/.gitkeep`

**Step 1: Create output directories**

```bash
mkdir -p runs guides
touch runs/.gitkeep guides/.gitkeep
```

**Step 2: Add to .gitignore**

Add to `.gitignore`:
```
runs/*/
guides/*.pdf
!runs/.gitkeep
!guides/.gitkeep
```

**Step 3: Run first guide manually**

In Claude Code, type:
```
/buyers-guide best wireless gaming headsets under $150, US
```

Follow the intake conversation. Confirm requirements. Observe the agent pipeline run.

**Step 4: Validate the run**

```bash
python evals/runner.py runs/[timestamp]/
```

Expected: all contract evals pass.

**Step 5: Commit directory structure**

```bash
git add runs/.gitkeep guides/.gitkeep .gitignore
git commit -m "feat: add output directories and gitignore rules"
```

---

### Task 14: Run full eval suite on first completed guide

**Step 1: Run contract evals**

```bash
python evals/runner.py runs/[timestamp]/ evals/contract-evals.json
```

Expected: 9/9 passed.

**Step 2: Note any failures and their root causes**

If any contract eval fails, document in `docs/eval-results/[date]-baseline.md`:
- Which test failed
- What the actual output contained
- Root cause (agent instruction gap, schema bug, or missing data)

**Step 3: Fix and re-run**

Fix the root cause (agent instruction or schema), re-run the guide, re-validate.

**Step 4: Commit baseline results**

```bash
git add docs/eval-results/
git commit -m "docs: add baseline eval results"
```

---

## Appendix: Dependency Check

Before starting Phase 5, verify:

```bash
node --version          # Node.js required for guide.js
python3 --version       # Python 3 required for validate.py and runner.py
python3 -c "import jsonschema"  # jsonschema required
which soffice || which libreoffice  # LibreOffice required for PDF conversion
```

Install missing:
- Node.js: `brew install node`
- LibreOffice: `brew install --cask libreoffice`
- jsonschema: `pip install jsonschema`
