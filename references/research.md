# Research Reference — Tracks A–F

This file is read at the start of Step 3. It contains the full methodology for all six research tracks, with rules embedded inline at the point where they apply.

---

## Output Contract

Before proceeding to Step 4, all of the following must be satisfied:

- **Candidate pool:** minimum 5 products identified across all channels
- **Track A:** at least one retailer-specific search completed (not just editorial roundups)
- **Track B:** community data checked for every finalist
- **Track C:** independent spec verification attempted for every finalist
- **Track D:** price history found or defined fallback applied for every finalist
- **Track E:** recall search run in user's region for every finalist
- **Track F:** final per-product verification completed for every finalist

Do not begin Step 4 until all six conditions are met.

---

## Track A — Category Landscape (4–8 searches)

**Goal: Build the complete candidate pool across all channels. Do not finalize rankings here.**

Run all of the following:

- `best [product type] [year]` — broad landscape sweep
- `[product type] comparison [year]` — review roundups
- `[product type] buying guide [year]` — structured criteria sources
- `[product type] tier list` or `[product type] ranking` — community consensus
- `site:reddit.com best [product type]` — community consensus beyond editorial lists
- **Retailer-specific searches (mandatory):** run targeted searches for retailers that carry the category but may not surface in generic results:
  - Prebuilt PCs: `Micro Center [specs]`, `Costco [product type]`, `Best Buy [product type] [specs]`
  - Appliances: search specific appliance retailers by region
  - Tools: Home Depot, Lowe's, specialty tool retailers
  - For any category: search `best place to buy [product type] in [region]` to identify dominant local retailers not in editorial roundups

**Do not stop after finding 3 familiar names from editorial lists.** Editorial "best of" lists are optimized for SEO and affiliate commission, not truth. Use them only as a discovery tool — never as a source of fact. Retailer-exclusive products are often the best value in a category and will not appear in editorial roundups.

---

## Track B — Community & Owner Intelligence (4–6 searches)

**Goal: Anti-marketing track. Real owners tell the truth in ways reviewers don't.**

- `site:reddit.com [product name] review` or `reddit [product name] problems`
- `[product name] long term reliability` or `[product name] after 6 months`
- `[product name] common issues` or `[product name] defects`
- `[category] recommendations reddit` — community consensus threads
- `[product name] vs [competitor]` — head-to-head community comparisons
- Slickdeals, forums, enthusiast communities specific to the category

**Evidence threshold:** A complaint qualifies as a known issue only if it appears in **at least 3 distinct community sources**. Single-source complaints may be noted as unverified. Do not flag anecdote as pattern.

**Flag in the guide** if a product has a known recurring community complaint, even if editorial reviews are positive.

---

## Track C — Specification Verification (3–5 searches)

**Goal: Never trust manufacturer specs at face value. Verify against independent measurements.**

**Always hunt for conditions behind conditional specs.** If a spec says "up to X," find the conditions and document both. Never report "up to X" without also reporting when X applies and what the real-world figure is.

**When sources conflict**, apply this hierarchy:
1. Independent lab measurements — highest authority
2. Long-term owner reports (Reddit threads with 6+ months of use, multiple corroborating accounts)
3. Short-term editorial reviews
4. Manufacturer claims — lowest authority; treat as marketing until independently verified

If two sources at the same level disagree, note both findings and flag the uncertainty. Do not suppress conflicting data.

### Source List by Category

**Electronics & Computing:**
- Displays / Monitors / TVs: RTings.com — measured brightness, contrast, input lag, color accuracy, uniformity
- Headphones / Earbuds / Speakers: RTings.com, AudioScienceReview — frequency response, THD, measured SPL
- Laptops: NotebookCheck, AnandTech — measured battery life, thermal throttling, sustained clock speeds
- Desktops / CPUs / GPUs: Tom's Hardware, AnandTech, Digital Foundry — real-world benchmarks, thermals, power draw
- Storage (SSD/HDD): Tom's Hardware, StorageReview — real-world sequential and random read/write, sustained write speeds
- Smartphones: GSMArena, AnandTech — measured display, battery endurance rating, camera benchmarks
- Networking / Routers: SmallNetBuilder — real-world throughput at range, not just peak spec
- Cameras: DPReview, LensTip, Photons to Photos — measured sensor performance, dynamic range
- Keyboards / Mice / Peripherals: search `[product] switch actuation force measured`; RTings covers some mice

**Audio / Home Entertainment:**
- Hi-Fi / Amplifiers / DACs: AudioScienceReview — measured SINAD, THD+N, noise floor
- Soundbars / Home Theater: RTings.com, Sound & Vision — measured frequency response, output levels
- Turntables: search `[product] wow flutter measured` or `[product] cartridge alignment review`

**Appliances & Home:**
- Washing Machines / Dryers: Consumer Reports (US only); UK: Which?; AU: Choice.com.au; DE: Stiftung Warentest; FR: UFC-Que Choisir; for all regions: search `[product] IEC test results` or `[product] energy consumption measured`
- Refrigerators / Dishwashers: Consumer Reports (US only); UK: Which?; AU: Choice.com.au; DE: Stiftung Warentest; for all regions: search `[product] temperature uniformity test` or `[product] noise level dB measured`
- Vacuums / Robot Vacuums: RTings.com covers robot vacuums; for uprights: search `[product] suction pascal measured`
- Air Purifiers: search `[product] CADR measured` — manufacturer CADR claims are often inflated
- Air Conditioners / Heat Pumps: US: search `[product] SEER measured`; EU/UK: search `[product] EER measured` or `[product] SCOP rating`; AU: search `[product] star rating measured`
- Coffee / Espresso Machines: search `[product] brew temperature measured`; Home-Barista forum for espresso

**Tools & Equipment:**
- Power Tools: search `[product] torque measured` or `[product] runtime test`; Project Farm on YouTube runs systematic real-world tests
- Hand Tools: search `[product] steel hardness tested` or `[product] edge retention test`
- Outdoor Power Equipment: search `[product] CFM measured` or `[product] runtime test`; Project Farm

**Vehicles & Mobility:**
- Cars: US: Car and Driver, Motor Trend, Consumer Reports; UK: Autocar, What Car?; EU: Auto Motor und Sport; AU: Drive.com.au, CarAdvice; for all regions: search `[product] reliability survey` or `[product] long-term test`
- Electric Vehicles: US: search `[product] real-world range test`; EU/UK: search `[product] WLTP real-world range` (EPA and WLTP are different standards — do not compare directly); InsideEVs and Bjørn Nyland cover global real-world range tests
- Bikes / E-Bikes: search `[product] actual range test` or `[product] motor output measured`

**Fitness & Health:**
- Fitness Trackers / Smartwatches: DC Rainmaker — gold standard for GPS accuracy, heart rate accuracy
- Exercise Equipment: search `[product] motor amp draw tested`; Garage Gym Reviews

**Furniture & Ergonomics:**
- Standing Desks: search `[product] stability test` or `[product] wobble measurement`; Autonomous, Wired, and Wirecutter have done systematic wobble tests
- Office Chairs: search `[product] lumbar adjustability review` or `[product] long-term comfort report`; Wirecutter

**Universal Verification Approach (any category not listed above):**
1. Search `[product name] [key spec] measured` or `[product name] [key spec] tested`
2. Search `[product name] review site:[enthusiast site for that category]`
3. Search `[product name] teardown` — construction quality reveals longevity
4. Search `[product name] long term` or `[product name] 6 months later`
5. If no independent measurement exists for a spec, flag it as "manufacturer-claimed, unverified by independent testing"

**For non-US users:** confirm you are using the correct regional source. Consumer Reports, Yale Appliance, and many other named sources are US-only. If a listed source does not cover the user's region, use the fallback search pattern for that category.

---

## Track D — Price Intelligence (2–3 searches per finalist)

**Goal: Verify current price, understand price history, identify sale patterns.**

- Search for current price at major retailers in the user's region
- Check price history using the appropriate tool:
  - **Amazon products:** CamelCamelCamel (`camelcamelcamel.com/product/[ASIN]`) — most reliable
  - **Non-Amazon products (B&H, Best Buy, manufacturer direct, etc.):** Google Shopping price history graph; search `[product name] price history`; or search deal aggregators by region:
    - US: `[product name] site:slickdeals.net`
    - UK: `[product name] site:hotukdeals.com`
    - FR: `[product name] site:dealabs.com`
    - DE: `[product name] site:mydealz.de`
  - **If no price history tool covers the product:** manually compare current price against 2–3 recent review articles or forum posts that mention price; note that history is limited
- Search `[product name] deal` or `[product name] sale` — is the "sale" actually the normal price?
- Check if the product is sold by the manufacturer directly at a lower price
- **Check for imminent major sale events:** search `[retailer or category] sale [current month/next month]` — if a known event (Prime Day, Black Friday, back-to-school) is within 4 weeks and the product historically discounts, add a "consider waiting" note

**Sale price budget eligibility:** If a product's regular price exceeds the budget but it regularly goes on sale within budget, it may be included — but only if price history confirms **≥3 sale events at the lower price**. One-off deals do not qualify. Always flag clearly: "Regularly available at [sale price] — currently [regular price]."

**New products with no price history:** Do not omit or guess. Use: `"Price History: Insufficient data — launched [Month YYYY]; no pricing history available yet."` Also note in the product's Weaknesses: "Too new to assess price stability."

**Report in the document for every product:**
- Current verified price with retailer link in the user's currency
- Price History spec row: e.g., `"Price History: Typically $X–Y; currently at [historic high / average / near low]"`
- Whether it's frequently on sale and at what typical sale price
- "Consider waiting" note if price is at historic high with likely dip ≥15%

---

## Track E — Availability & Lifecycle Status (2–3 searches)

**Goal: Confirm every finalist is safe to recommend — available, current, and recall-free.**

**Recall search — use the correct database for the user's region:**
- US: `[product name] CPSC recall` or search `cpsc.gov/recalls`
- EU: `[product name] RAPEX` or search `ec.europa.eu/safety-gate` (covers all EU member states)
- UK: `[product name] OPSS recall` or search `gov.uk/product-safety-alerts`
- AU: `[product name] recall Australia` or search `productsafety.gov.au`
- CA: `[product name] recall Canada` or search `healthycanadians.gc.ca/recall`
- Any region: also search `[product name] recall [country]` — manufacturer recalls often appear in news and forums before official databases are updated

Also run:
- `[product name] discontinued` — has it been quietly end-of-lifed?
- `[product name] successor` or `[brand] [product line] [current year]` — is a replacement imminent?
- `[product name] announced` or `[product name] release date` — has a replacement been announced but not yet released?
- Check manufacturer's current product page and stock at 2+ major retailers in the user's region

**Rules:**
- Do not recommend a discontinued product unless no viable alternative exists (flag clearly)
- Flag imminent successors — if a direct replacement is expected within 1–3 months, note it and recommend considering a wait
- Do not include announced-but-unavailable products as reviewed products. Note them in the relevant product card and Final Recommendations
- Do not recommend products unavailable in the user's region

---

## Track F — Final Per-Product Verification (1–2 searches per finalist)

**Goal: Confirm every detail is correct before writing a single product card.**

For each finalist:
- Fetch the current manufacturer product page — confirm exact model name, specs, MSRP
- Fetch the retailer page — confirm SKU matches the correct model, not a similar-named variant
- Verify the product link URL resolves to the correct product

**Naming variant trap:** Near-identical product names are among the most common sources of wrong recommendations. Before finalizing any product, identify all naming variants in the product line and confirm which is correct. Search `[brand] [product line] variants` or `[product name] vs [similar name]` to surface the full variant tree.

**For non-US users:** confirm the regional model has identical specs to what is being described. Note any regional spec differences explicitly in the product card.

**If the product must interact with the user's existing hardware:** confirm compatibility at variant level before writing the card.
