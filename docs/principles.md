# Product Principles

## The premise

This tool exists to give buyers an honest, unbiased answer to "what should I buy?" in any product category. The answer must be derived entirely from evidence — measured performance, verified specifications, and real owner experience — with no influence from marketing spend, editorial relationships, affiliate incentives, or name recognition.

**Objectivity. No bias. Depth and breadth.**

---

## What "no bias" means operationally

**Selection bias** is the most common failure mode. A tool that only looks where it was told to look finds what those places cover — and misses everything they don't. The Micro Center problem (the original motivation for this architecture) is a selection bias failure: the best option in a category was invisible because the process only checked sources that covered products with high marketing spend.

The fix is structural: the process must discover where to look rather than being told where to look.

**Curation bias** is the second failure mode. Editorial "best of" lists, affiliate-driven roundups, and sponsored content reflect the incentives of their publishers, not the interests of buyers. These sources are used only as a discovery starting point — never as a source of fact about product quality.

**Hardcoding creates both.** Any named retailer, named publication, or named brand in the methodology creates a selection ceiling. The ceiling is invisible until something important falls outside it.

---

## What belongs in the methodology

**Process patterns** — search queries, evidence thresholds, verification steps. These work for any product in any category.

**Measurement sources** — databases that publish objective, independently-measured data (frequency response, thermal throttling, suction force). These are used for their *data*, not their *opinions*. A measurement is a measurement regardless of who published it. This is a meaningful distinction: RTings' measured brightness numbers are objective data; RTings' "best TV" recommendations are editorial opinion. Use the former; do not rely on the latter.

**Regulatory sources** — government recall databases (CPSC, RAPEX, OPSS, etc.). These are authoritative and have no commercial interest in the outcome.

**What does not belong:**

- Named retailers (creates a search ceiling at those retailers)
- Named editorial publications used as product discovery or recommendation sources
- Named brands (any mention of a specific brand in methodology creates favoritism)
- Category-specific lists that only apply to one product type

When updating methodology files, apply this test: *does this instruction work for a product category I've never heard of?* If the answer is no, replace the specific name with the process that would discover it.

---

## Structural enforcement over behavioral instructions

Instructions describe intent. Contracts enforce behavior.

An agent can skip an instruction. An agent cannot produce a valid output without satisfying the schema.

When a process failure is found, the first question is always: **can this be caught by a schema field, contract requirement, or eval assertion?** If yes, enforce it structurally. If the only fix is an instruction, that fix will fail again in a different form.

**Examples:**

| Behavioral patch (fragile) | Structural fix (durable) |
|---|---|
| "Search these specific retailers" | `retailers_searched` field required in contract |
| "Don't warn about budget before research" | Budget shortfalls surface through Track A output, not intake |
| "Verify the URL is a product page" | `url_verified: boolean` required in `track_f` contract |
| "Check at least 3 sources for issues" | `confirmed_issues` only populated after 3-source threshold in Track B |
| "Don't say there's a store in the user's city if there isn't one" | `store_location` required on every in-store purchase option; C12 eval rejects values that just echo the user's city with no store name |
| "Verify prices from live pages, not aggregators" | `verified_live: boolean` required per purchase option; C13 eval rejects any unverified option that claims in-stock |
| "Document what you actually did during research" | `research_log.json` required output per run; C14 eval enforces its presence; screenshots required per product |

---

## What determinism means here

Full determinism is not possible — product availability changes, prices change, community sentiment evolves. Two runs at different times will find different products.

What should be deterministic:

- **Process**: the same steps always run in the same order regardless of category
- **Evidence thresholds**: the same evidentiary standard always applies (3+ sources for confirmed issues, ≥3 sale events for price eligibility)
- **Scoring**: the same weights always apply (30/25/20/15/10); scores are calculated from evidence, not adjusted post-hoc
- **Output format**: schema-validated contracts at every stage boundary; a stage cannot be skipped

What is judgment-based (and should be documented, not hidden):

- Individual factor scores (0–10 per factor) — judgment within a defined framework
- Community sentiment classification — judgment from evidence, constrained to 4 values by schema
- Category type determination (focused/broad/competitive) — defined heuristic with required rationale

The goal is that given the same market state, two runs produce the same result. The schema contracts make this verifiable.

---

## How to evaluate future changes

Before merging any change to methodology, instruction, or schema files, answer:

1. **Does this introduce a named source, retailer, or brand?** If yes, replace with the process that would discover it.
2. **Is this a behavioral instruction or a structural enforcement?** If behavioral, can it be made structural?
3. **Does this change apply to all product categories, or only one?** If only one, it probably doesn't belong in shared methodology.
4. **Does this narrow the search space without a contractual reason?** If yes, it creates a selection ceiling.
5. **Is this fixing a symptom or the underlying process?** Symptom patches accumulate; process fixes compound.
