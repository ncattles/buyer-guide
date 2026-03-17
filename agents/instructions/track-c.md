# Track C — Specification Verification

You receive a list of candidate products, the category, the user's region, and a run directory path. Verify specs against independent measurements for each candidate.

**Read the Track C section of `references/research.md` before starting. Use the category-specific sources listed there for this category. If the category is not listed, use the Universal Verification Approach.**

Maximum 8 candidates per run. If more than 8 are passed, process the top 8 by order received.

## Hard filter spec verification

If the user's hard filters include a component-level spec (e.g. "minimum 2 free M.2 slots", "Wi-Fi 6E required", "USB-C front panel"), and the product listing does not explicitly confirm it:

1. Identify the exact motherboard (or relevant component) model from the product listing
2. Fetch the manufacturer's spec page for that component directly
3. Verify the spec from the official spec sheet
4. Only flag as `unverified` if the component model cannot be determined at all — do not surface to the user if a spec sheet lookup can resolve it

Record the spec sheet URL in `measurement_sources` and the confirmed value in `conditional_specs` or `flags`.

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
