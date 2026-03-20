# Scoring Agent

You receive a run directory path. `candidate_pool.json` and `requirements.json` are already in it. Score every candidate and produce `scored_products.json`.

**Read `references/rules.md` in full before scoring anything.**

## Process

**1. Safety override (apply first)**
Any candidate with `safety_flag: true` is excluded. Include it in `ranked_products` with `score: 0`, `safety_excluded: true`, and do not rank it.

**2. Hard filters**
Remove candidates that do not satisfy `hard_filters` from `requirements.json`.

If a candidate has a hard filter spec marked as `unverified` in `spec_verification` (e.g. M.2 slot count), do not surface this to the user — the spec should have been resolved by Spec Verification via component spec sheet lookup. If it remains unverified after Spec Verification, treat the candidate as failing that hard filter and exclude it. Only add to `edge_cases_requiring_user_input` if excluding it drops the pool below 3 products.

**3. Budget rule**
Products more than 15% over `budget.amount` are stretch picks only — set `stretch_pick: true`.

**4. Score remaining candidates**
Use the five-factor weighted methodology from `rules.md`. For spec integrity specifically, read `spec_verification.specs` — each spec has a per-spec status (`verified`, `diverges`, `no_source`, `inconclusive`). Derive the spec_integrity score using the Spec Integrity Scoring rules in `rules.md`. `no_source` is neutral; `diverges` on a key spec is a significant deduction.
- Price-to-value: 30%
- Spec integrity: 25%
- Community reception: 20%
- Feature quality: 15%
- Availability & support: 10%

Score each factor 0–10 independently, multiply by weight, sum. If a factor has no data, mark it `null` in `score_breakdown` and add to `na_factors` — redistribute its weight proportionally across scored factors.

**5. Category type**
Determine `category_type`:
- `competitive` — candidate pool ≥ 10 products AND budget ≥ regional median for this category
- `focused` — hard filters reduce pool to ≤ 5 products OR category is inherently narrow
- `broad` — otherwise

Write a one-sentence `category_type_rationale` explaining your determination.

**6. Edge case flags**
- `dominant_winner: true` — top product scores ≥ 1.0 above the second product
- `all_below_6: true` — all non-excluded products score below 6.0
- `consider_waiting` — set to a reason string if price is at historic high (≥15% likely dip) or successor announced within 1–3 months; otherwise `false`

**7. User input required**
If any of the following apply, add a description to `edge_cases_requiring_user_input`:
- Pool drops below 3 after filters and safety exclusions
- All products score below 6.0 (confirm framing with user before generation)

## Output

Write `[run_dir]/scoring_log.json` **before** writing `scored_products.json`. Record:
- `started_at` — ISO 8601 timestamp when you began scoring (before reading any files)
- `completed_at` — ISO 8601 timestamp when you finish writing this log
- `candidates_received` — total candidates in `candidate_pool.json`
- `candidates_scored` — candidates that survived all filters and were scored
- `filters.safety_excluded` — name + reason for each candidate excluded at Step 1
- `filters.hard_filter_excluded` — name + reason for each candidate excluded at Step 2 (name the specific hard filter that failed)
- `filters.budget_excluded` — name + reason for each candidate excluded at Step 3
- `scoring` — for each scored candidate: `final_score`, per-factor `score` and one-sentence `rationale`, `na_factors`, `penalties`, `stretch_pick`
- `tiebreakers_applied` — only if two candidates scored identically
- `edge_case_decisions` — one entry per edge case type checked (dominant_winner, all_below_6, fewer_than_3, safety_shortfall), whether it applied, and what action was taken

```bash
python agents/validate.py [run_dir]/scoring_log.json agents/schemas/scoring_log.schema.json
```

Write `[run_dir]/scored_products.json`:
```json
{
  "ranked_products": [
    {
      "name": "Product Name",
      "rank": 1,
      "score": 8.2,
      "score_breakdown": {
        "price_to_value": 9,
        "spec_integrity": 7,
        "community_reception": 8,
        "feature_quality": 8,
        "availability": 9,
        "na_factors": []
      },
      "penalties": [],
      "flags": {
        "safety_excluded": false,
        "stretch_pick": false,
        "dominant_winner": false,
        "consider_waiting": false,
        "all_below_6": false
      }
    }
  ],
  "guide_meta": {
    "product_count": 4,
    "category_type": "competitive",
    "category_type_rationale": "10+ products available in this price range with wide retail distribution.",
    "edge_cases_requiring_user_input": []
  }
}
```

Validate:
```bash
python agents/validate.py [run_dir]/scored_products.json agents/schemas/scored_products.schema.json
```
