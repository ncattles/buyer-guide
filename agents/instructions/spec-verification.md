# Spec Verification — Specification Verification

You receive a list of candidate products, the category, the user's region, and a run directory path. Verify specs against independent measurements for each candidate.

**Read the Spec Verification section of `references/research.md` before starting. Use the category-specific sources listed there for this category. If the category is not listed, use the Universal Verification Approach.**

Maximum 8 candidates per run. If more than 8 are passed, process the top 8 by order received.

## Step 0 — Find the official manufacturer product page

Before verifying any specs, find the manufacturer's official product page for each candidate:

1. Search `[manufacturer name] [product name] official` or `[product name] site:[manufacturer domain]`
2. Navigate to the page with Playwright and confirm it loads as the correct product
3. Check whether the page has a price / add-to-cart option (manufacturer sells direct)
4. Record the URL as `official_product_url` in your output

**If the page sells direct:** record this in `official_product_url` and note it in `flags`. Price Research runs in parallel and independently finds the official URL — your output is the canonical record for the merge, not a handoff signal.

**If no official product page exists** (OEM-only product, retailer exclusive, product page is the retailer): record `official_product_url: null` and add a `flags` entry: `"Official product page: Not found — [reason, e.g. retailer-exclusive brand, no manufacturer website]"`.

Do not confuse a retailer product listing with an official manufacturer page. A Newegg or Best Buy URL is not an official product page.

## Use-case mandatory specs

Before verifying anything else, check `requirements.json` for `existing_hardware`. If it mentions NVMe SSDs or M.2 drives:

- **M.2 slot count is a mandatory spec to verify** — not optional, not estimable from chipset tier
- Identify the exact motherboard model from the product listing. If the listing doesn't name the motherboard, search `[product name] motherboard model` and navigate to a review or teardown that confirms it
- Fetch the official motherboard spec sheet from the manufacturer and count the total M.2 slots and which are occupied by included storage
- Record how many M.2 slots are free after the included drive(s) are accounted for
- If the motherboard model cannot be determined after exhausting the above steps, set status `no_source` and add a flags entry: `"M.2 slots: Motherboard model not identified — buyer must confirm M.2 slot count before migrating existing NVMe SSDs"`

## Use-case derived mandatory specs

Before verifying hard filter specs, read `use_case` from `requirements.json` and infer additional specs that matter for that use case — including ones the user didn't think to request. A user who didn't ask about microphone quality but stated "work" as their use case would be surprised to discover a product has no usable mic. These are mandatory to verify.

Derive the checklist from the stated use case. Examples (not exhaustive — apply judgment to the category):
- **work / office / calls**: microphone quality, call clarity, multipoint Bluetooth pairing, voice pickup pattern, background noise rejection
- **travel / commute**: battery life (actual vs. claimed), fold-flat portability, airline adapter compatibility, passive isolation without ANC
- **gym / fitness / sport**: IP/water resistance rating, secure fit mechanism, sweat resistance
- **gaming**: Bluetooth input latency, surround sound support, mic sidetone
- **audiophile / music**: frequency response accuracy, total harmonic distortion, codec support (LDAC, aptX Lossless)

Add each derived spec to your verification checklist alongside any hard filter specs. If a product fails a derived spec in a way that would likely cause a return (e.g., no microphone for a work use case), add a prominent `flags` entry: `"[Spec]: This product [fails/lacks X], which is important for the stated use case. Verify before purchasing."` Surface this in `notes` at Final Verification so it reaches the generation agent.

## Quantitative performance scores

If the category's spec measurement source (from `category_sources` in `research_foundation.json`) publishes numeric performance scores, look them up and record them in `specs`. Numeric scores enable direct cross-product comparison in the comparison matrix.

For each candidate, look up:
- Any overall or category score published by the measurement source
- Any measured values that replace marketing claims (e.g., measured ANC attenuation in dB vs. "industry-leading ANC", measured battery life vs. claimed)

Store these as spec entries with `status: "verified"`, `claimed: null` if no manufacturer claim exists, `measured: "[value with units]"`, and `source: "[URL]"`.

**Reference product scores:** If `requirements.json`'s `use_case` or `existing_hardware` field names a reference product (e.g., "Sony WH-1000XM6 is the benchmark"), look up that product's scores on the same measurement source and record them in a `reference_product_scores` field at the top level of your output:
```json
"reference_product_scores": {
  "product_name": "Sony WH-1000XM6",
  "scores": {
    "ANC Score": "93/100",
    "ANC Attenuation": "43 dB",
    "Microphone Quality": "Good (RTings: 7.2/10)",
    "Battery Life": "30 hours (measured)"
  },
  "source": "https://rtings.com/..."
}
```
These scores power the comparison matrix benchmark column in the generated guide.

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
- `diverges` — independent measurement significantly contradicts the claim; note discrepancy in `flags` with both figures. **When a spec is `diverges`:** (1) make at least one additional resolution attempt — check the manufacturer's official spec sheet for the specific SKU, and check one other independent review source; (2) if still unresolved, add a `flags` entry that tells the user exactly how to verify before purchasing (e.g., `"Cooler: Product page says 240mm; review source says 360mm. Verify at [manufacturer spec URL] or contact [manufacturer] support before ordering — confirm SKU [model number] cooler spec."`)
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

Write `[run_dir]/spec-verification-results.json`:
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
