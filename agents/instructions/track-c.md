# Track C — Specification Verification

You receive a list of candidate products, the category, the user's region, and a run directory path. Verify specs against independent measurements for each candidate.

**Read the Track C section of `references/research.md` before starting. Use the category-specific sources listed there for this category. If the category is not listed, use the Universal Verification Approach.**

Maximum 8 candidates per run. If more than 8 are passed, process the top 8 by order received.

## Step 0 — Find the official manufacturer product page

Before verifying any specs, find the manufacturer's official product page for each candidate:

1. Search `[manufacturer name] [product name] official` or `[product name] site:[manufacturer domain]`
2. Navigate to the page with Playwright and confirm it loads as the correct product
3. Check whether the page has a price / add-to-cart option (manufacturer sells direct)
4. Record the URL as `official_product_url` in your output

**If the page sells direct:** flag this in your output so Track D includes it in `purchase_options` and Playwright-verifies its price. The official page price can be cheaper, more expensive, or match other retailers — it must be checked regardless.

**If no official product page exists** (OEM-only product, retailer exclusive, product page is the retailer): record `official_product_url: null` and add a `flags` entry: `"Official product page: Not found — [reason, e.g. retailer-exclusive brand, no manufacturer website]"`.

Do not confuse a retailer product listing with an official manufacturer page. A Newegg or Best Buy URL is not an official product page.

## Hard filter spec verification

If the user's hard filters include a component-level spec (e.g. "minimum 2 free M.2 slots", "Wi-Fi 6E required", "USB-C front panel"), and the product listing does not explicitly confirm it:

1. Identify the exact motherboard (or relevant component) model from the product listing
2. Fetch the manufacturer's spec page for that component directly
3. Verify the spec from the official spec sheet
4. Only flag as `unverified` if the component model cannot be determined at all — do not surface to the user if a spec sheet lookup can resolve it

Record the spec sheet URL in `measurement_sources` and the confirmed value in `conditional_specs` or `flags`.

## Spec status definitions

Apply one status per spec verified:

- `verified` — independent measurement confirms the manufacturer claim, or is within acceptable tolerance
- `diverges` — independent measurement significantly contradicts the claim; note discrepancy in `flags` with both figures
- `inconclusive` — a source exists and was checked, but could not definitively confirm or deny the spec (e.g., methodology unclear, conflicting results across sources at the same level)
- `no_source` — no independent measurement source exists for this spec in this category; set `claimed` to the manufacturer value, `measured` and `source` to null; this is a data gap, not a product failure

**Minimum specs to verify:** the 2–3 specs most relevant to the user's use case plus any spec claimed with "up to" or a suspiciously round number. Do not verify every spec in the datasheet — focus on the ones that matter for the decision.

**For niche categories with no dedicated measurement database:**
Exhaust the Universal Verification Approach before using `no_source`. A spec is only `no_source` after you have:
1. Run the `[product name] [spec] measured` and `[product name] [spec] tested` searches
2. Checked enthusiast forums and communities for owner-measured data
3. Searched YouTube for teardown or hands-on measurement content
4. Checked if a manufacturer competitor has published comparative test data

If all four return nothing: use `no_source` and add a `flags` entry: `"[Spec]: No independent measurements found — manufacturer claim unverified"`. Do not leave `no_source` specs unexplained.

**`sources_checked`** must list every source you consulted, including those that returned no result. Minimum 5 entries required — one per exhaustion step (measured search, community/forum, YouTube/teardown, competitor comparison, manufacturer spec page). A product returning all `no_source` after checking only one or two places has not been adequately verified; a product returning all `no_source` after exhausting all five steps has been.

## Output

Write `[run_dir]/track_c_results.json`:
```json
{
  "results": {
    "Product Name": {
      "official_product_url": "https://manufacturer.com/product-page",
      "specs": {
        "peak_brightness": {
          "status": "diverges",
          "claimed": "1000 nits",
          "measured": "650 nits sustained",
          "source": "https://rtings.com/..."
        },
        "response_time": {
          "status": "no_source",
          "claimed": "1ms GtG",
          "measured": null,
          "source": null
        },
        "refresh_rate": {
          "status": "verified",
          "claimed": "165Hz",
          "measured": "165Hz confirmed",
          "source": "https://rtings.com/..."
        }
      },
      "sources_checked": ["rtings.com", "notebookcheck.net", "tftcentral.co.uk"],
      "conditional_specs": ["165Hz requires DisplayPort 1.4"],
      "flags": ["Peak brightness: manufacturer claims 1000 nits; measured 650 nits sustained"]
    }
  }
}
