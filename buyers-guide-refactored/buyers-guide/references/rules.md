# Rules Reference — Scoring, Business Logic, Edge Cases

This file is read at the start of Step 4. It contains the full scoring methodology, rating definitions, all edge case handling, and category-specific dealbreaker examples.

---

## Scoring Methodology

Ratings are not arbitrary. Each product is scored across five weighted factors. Sum the weighted scores to arrive at the final rating.

| Factor | Weight | What it measures |
|---|---|---|
| Price-to-value | 30% | Does the price match what you get vs. direct competitors? Is there a better option for the same money? |
| Spec integrity | 25% | How closely does real-world performance (Track C) match manufacturer claims? |
| Community reception | 20% | Owner-reported reliability, confirmed complaints, durability reports from Track B. |
| Feature quality | 15% | How well does it execute its core features vs. alternatives — not just whether it has the feature, but how well it works. |
| Availability & support | 10% | Easy to buy in the user's region, in stock, reasonable warranty, responsive brand support. |

**Applying the weights:**
1. Score each factor from 0–10 independently
2. Multiply each score by its weight
3. Sum the five weighted scores for the final rating

**Worked example:** A product scoring 9/10 on price-to-value (×0.30 = 2.7), 7/10 on spec integrity (×0.25 = 1.75), 8/10 on community reception (×0.20 = 1.6), 8/10 on feature quality (×0.15 = 1.2), 9/10 on availability (×0.10 = 0.9) = **8.15 → rounded to 8.2**

**Document the score breakdown** in your reasoning before writing each product card. The breakdown does not appear in the PDF — the rating number alone does — but a defensible basis prevents arbitrary scores.

### N/A Factors

If a factor genuinely cannot be scored due to insufficient data (e.g., product just launched, no Track B community data exists, no independent Track C measurements exist), mark it N/A and exclude it from the weighted average. Redistribute its weight proportionally across the remaining scoreable factors. Note in the product card which factors were N/A and why.

**Never assign a score to a factor based on no evidence.** An honest partial score is more defensible than a fabricated complete one.

**Community reception is not N/A simply because a product is new.** If early failure reports or early owner impressions exist, score from that data and note it is early-stage. Mark N/A only if Track B returns literally nothing.

### Penalties (applied after weighted score)

- Confirmed recurring community complaint (3+ distinct sources): −0.3 per distinct confirmed issue
- Spec significantly diverges from manufacturer claim on a key feature: −0.2 to −0.5 depending on severity

### Safety Override — Hard Exclusion

If a product has a confirmed safety recall, documented fire/injury/electrocution risk, or active regulatory action (CPSC, RAPEX, OPSS, or equivalent in the user's region), it is **automatically excluded** from the guide regardless of its weighted score. Do not include it as a stretch pick, do not caveat it with warnings — exclude it entirely. Move it to the What To Avoid section with a brief explanation and a direct link to the recall or regulatory notice. This override cannot be argued around by a high score or positive community reception.

---

## Rating Scale

- **9.0–10.0**: Exceptional, best-in-class, nearly no compromises
- **8.0–8.9**: Very good, strong recommendation with minor trade-offs
- **7.0–7.9**: Good but with notable compromises or overpricing
- **6.0–6.9**: Below average value or significant shortcomings
- **Below 6.0**: Not recommended at current price

---

## Edge Case Handling

### Dominant Winner

If the highest-rated product scores ≥1.0 rating points above the next product, the guide must reflect this clearly rather than implying false parity:

- In the Intro paragraph: name the dominant winner and note the gap
- In Final Recommendations: lead with a clear "if you only read one recommendation" statement for that product
- Do not soften or obscure a category where one product is genuinely head-and-shoulders above the rest — that clarity is valuable to the user

### All Finalists Below 6.0

If every qualifying product scores below 6.0 after applying the weighted methodology, do not suppress this:

1. Note prominently in the Intro paragraph that no strong options exist at this budget in this category
2. Frame all Final Recommendations cards as "least-bad" picks — not genuine endorsements
3. Recommend the user either raise their budget to a stated threshold where better options exist, or wait for prices to improve
4. Never inflate ratings to avoid this situation — a guide that honestly says "nothing here is great" is more valuable than one that falsely implies otherwise

### Sale Price Budget Eligibility

A product whose regular price exceeds the budget may be included in the primary pool — but only if price history confirms **≥3 sale events** at a within-budget price. One-off deals do not qualify. Always flag clearly: "Regularly available at [sale price] — currently [regular price]. Watch for sales."

### Stretch Picks (>15% Over Budget)

Products exceeding the stated budget by more than 15% may only appear as explicitly flagged stretch picks:

- Verdict badge must be suffixed with " (OVER BUDGET)"
- Product name must include ⚠ in the rankings table
- Card copy must explicitly state the amount over budget as a percentage
- No rating penalty, but never present as equal to in-budget options

### Fewer Than 3 Viable Products

If hard filters leave fewer than 3 qualifying products, do not pad the guide. Stop before generating:

1. Tell the user how many qualifying products exist
2. Explain which filters caused the shortfall
3. Offer to either widen the criteria or produce a shorter guide with a note explaining the limited market

### Safety Exclusion Causing Shortfall

If a safety recall exclusion drops the pool below 3, apply the safety override unconditionally first — the product is excluded regardless. Then:

1. Stop before generating
2. Tell the user how many products remain
3. Explain that the shortfall is due to a safety exclusion, not a filter that can be relaxed
4. Offer to widen other criteria to find replacements, or produce a shorter guide
5. Never suggest including a recalled product to meet the minimum count

### New Product — No Price History

Do not leave the Price History row empty or omit it. Use:
`"Price History: Insufficient data — launched [Month YYYY]; no pricing history available yet."`

Also note in the product's Weaknesses: "Too new to assess price stability — no historical data to confirm whether current price is typical or elevated."

### Announced-But-Unavailable Successor

If a direct replacement is expected within 1–3 months:
- Note it in the relevant product card Weaknesses and in Final Recommendations
- Include a recommendation card: "Consider waiting for [product] — announced for [timeframe]. [What it improves.]"
- Do not include the unshipped product as a reviewed product

### Timing Recommendations

Include a "consider waiting" note when:
- CamelCamelCamel (or equivalent) shows the product is at a historic high and regularly dips ≥15%
- A direct successor is announced or confirmed within 1–3 months

If both apply, make "consider waiting" the primary recommendation framing. Do not include a "consider waiting" note for minor fluctuations (<15%) or vague unconfirmed rumors.

---

## Rating Tiebreaker

If two products score identically, rank by:
1. Price (lower is ranked higher)
2. Availability (in-stock at more retailers ranks higher)
3. Community sentiment (fewer confirmed complaints ranks higher)

Apply consistently — never break ties arbitrarily.

---

## Refresh-Specific Rules

**Product count rules apply on refresh exactly as on a new guide:**
- If a discontinuation or failed re-verification drops the pool below 3 qualifying products, stop before regenerating. Tell the user how many products remain, what caused the shortfall, and offer to widen criteria or produce a shorter guide.
- If a strong new entrant qualifies, it may replace the lowest-rated existing product — but the maximum of 6 still holds. Never silently expand the guide beyond 6 products on a refresh.
- If the refresh results in a different ranking order, update the rankings table, verdict badges, and Final Recommendations to match — do not leave the old order in place.

---

## Category-Specific Dealbreaker Examples

Use these as starting points for Step 2 make-or-break questions. Always adapt to the specific product and user context.

- **Monitors:** VESA mount, HDMI 2.1 (for consoles), USB-C PD, panel coating (matte vs. glossy), stand adjustability (height/tilt/swivel/pivot)
- **Standing Desks:** Motor type (electric vs. manual crank), minimum width, height range (especially for very tall or short users), weight capacity
- **Laptops:** Minimum RAM/storage, port requirements (Thunderbolt, SD card, HDMI), battery life threshold, weight limit, discrete GPU required
- **Prebuilt PCs:** GPU/CPU generation minimums, upgradability (PCIe slots, RAM slots), form factor constraints (ITX/ATX), included WiFi/Bluetooth, PSU headroom for future upgrades
- **Headphones:** Wired vs. wireless, ANC required, microphone quality (for calls/recording), platform compatibility (Xbox, PlayStation, PC), open-back vs. closed-back
