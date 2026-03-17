# Track C — Specification Verification

You receive a list of candidate products, the category, the user's region, and a run directory path. Verify specs against independent measurements for each candidate.

**Read the Track C section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting. Use the category-specific sources listed there for this category. If the category is not listed, use the Universal Verification Approach.**

Maximum 8 candidates per run. If more than 8 are passed, process the top 8 by order received.

## Output

Write `[run_dir]/track_c_results.json`:
```json
{
  "results": {
    "Product Name": {
      "spec_integrity": "verified",
      "conditional_specs": ["165Hz requires DisplayPort 1.4"],
      "measurement_sources": ["https://rtings.com/..."],
      "flags": ["Manufacturer claims 1000 nits peak; measured 650 nits sustained"]
    }
  }
}
```

Valid values for `spec_integrity`: `verified`, `diverges`, `unverified`.
