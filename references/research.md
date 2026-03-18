# Research Reference — Tracks A–F

This file is read at the start of Step 3. It contains the full methodology for all six research tracks, with rules embedded inline at the point where they apply.

**What belongs in this file:** Search patterns, evidence thresholds, source hierarchies, verification logic. Methodology that works for any product in any category.

**What does not belong:** Named retailers, named brands, named editorial publications. Any hardcoded name creates a selection bias — the tool will find what those names cover and miss everything they don't. When updating this file, replace any specific name with the process that would discover it.

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
  - Search `best place to buy [product type] in [region]` and `where to buy [product type] [region]` to discover which retailers carry this category
  - Search community discussions (`site:reddit.com buy [product type] [region]`) — buyers name the stores they used, including smaller regional and specialty retailers not in editorial coverage
  - Check price comparison aggregators (Google Shopping, PriceGrabber) to see which retailers are actively listing this category
  - Include specialty retailers, warehouse clubs, manufacturer-direct storefronts, and boutique builders — not just large general retailers

**For any retailer with physical store locations:** before listing it as an in-store source, verify a store exists within a reasonable distance of the user's city/state by checking the retailer's store locator. Never assume a location exists in or near the user's city. If the nearest store is in a different city, record the actual city and distance — the guide must reflect the real location, not the user's city. If no store exists within ~100 miles, treat the retailer as online-only for this user.

**Do not stop after finding 3 familiar names from editorial lists.** Editorial "best of" lists are optimized for SEO and affiliate commission, not truth. Use them only as a discovery tool — never as a source of fact. Retailer-exclusive products are often the best value in a category and will not appear in editorial roundups.

---

## Track B — Community & Owner Intelligence (4–6 searches)

**Goal: Anti-marketing track. Real owners tell the truth in ways reviewers don't.**

- `site:reddit.com [product name] review` or `reddit [product name] problems`
- `[product name] long term reliability` or `[product name] after 6 months`
- `[product name] common issues` or `[product name] defects`
- `[category] recommendations reddit` — community consensus threads
- `[product name] vs [competitor]` — head-to-head community comparisons
- Deal aggregator communities and enthusiast forums specific to the category (search `[product type] deal site:[region-appropriate aggregator]` or search `[product type] forum` to find active communities)

**Evidence threshold:** A complaint qualifies as a known issue only if it appears in **at least 3 distinct community sources**. Single-source complaints may be noted as unverified. Do not flag anecdote as pattern.

**Flag in the guide** if a product has a known recurring community complaint, even if editorial reviews are positive.

---

## Track C — Specification Verification (3–5 searches)

**Goal: Never trust manufacturer specs at face value. Verify against independent measurements. Also locate the official manufacturer product page.**

**Always find the official product page first.** Before verifying any spec, search for the manufacturer's official product page and navigate to it with Playwright. Record it as `official_product_url`. If the page has a price or add-to-cart, flag it so Track D Playwright-verifies it as a purchase option — the manufacturer may sell direct at a different price than third-party retailers. If no official page exists (retailer-exclusive brand, OEM-only), record `official_product_url: null` with a `flags` explanation.

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
- Soundbars / Home Theater: RTings.com — measured frequency response, output levels, directivity; search `[product] frequency response measured` for additional independent measurements
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
- Cars: search `[product] long-term reliability test`, `[product] owner reliability survey [region]`, `[product] real-world fuel economy measured`; for safety: search `[product] crash test [region standard]` (NHTSA for US, Euro NCAP for EU/UK, ANCAP for AU)
- Electric Vehicles: search `[product] real-world range test [region]` — EPA and WLTP are different standards, do not compare across regions without noting the standard used; search `[product] real-world range measured` for independent tests not funded by the manufacturer
- Bikes / E-Bikes: search `[product] actual range test` or `[product] motor output measured`

**Fitness & Health:**
- Fitness Trackers / Smartwatches: DC Rainmaker — gold standard for GPS accuracy, heart rate accuracy
- Exercise Equipment: search `[product] motor amp draw tested`; Garage Gym Reviews

**Furniture & Ergonomics:**
- Standing Desks: search `[product] stability test` or `[product] wobble measurement`; search `[product] wobble review site:youtube.com` for video demonstrations
- Office Chairs: search `[product] lumbar adjustability review` or `[product] long-term comfort report`; search owner forums and ergonomics communities

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

- **Use Playwright exclusively for live price and stock verification.** WebFetch is blocked by most major retailers (Micro Center, Best Buy, Amazon, Walmart) and will return 403 errors or CAPTCHA pages. Prices from deal aggregators or search snippets are not live-verified and must not be used as the headline price.
- **Always check the official product URL from Track C first.** If it exists, navigate to it with Playwright. If it shows a price, the manufacturer sells direct — Playwright-verify the price and include it in `purchase_options`. The official page price can be lower than any retailer — it must be checked, not assumed.
- Search for all retailers carrying the product in the user's region — not just the one URL from Track A. Use Google Shopping and price comparison aggregators to surface all active sellers. Verify each retailer's listing live via Playwright.
- **For any retailer with physical locations** (including hybrid retailers like Best Buy, Walmart, Target — not just in-store-only): set the zip code or store location to the user's city/state before loading the product page. The screenshot must show the location indicator. Record the actual store name and city — never report availability without confirming which specific location was checked. Report in-store pickup availability and shipping availability separately if they differ — a product available to ship nationally may be out of stock for pickup at the nearest store.
- **Distance is never a reason to exclude a product.** If the nearest store is far from the user's city (50 miles or 300 miles), include the product in `purchase_options` with the distance clearly noted. The user decides whether to make the trip — the pipeline never filters on distance.
- **Screenshots must show Add to Cart / availability, not just the product image.** Scroll down until the Add to Cart button and pickup/shipping availability status are visible before taking the screenshot. A screenshot showing only the product image or specs is not valid evidence.
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

**Use Playwright exclusively for all page fetches in Track F.** WebFetch is blocked by most major retailers and will silently return stale data or fail. Playwright renders the live page as a real browser would.

For each finalist:
- Use Playwright to navigate to the primary retailer URL (the lowest-price option from `purchase_options`)
- Confirm the page loads as a product listing: product name visible, price shown, add-to-cart or stock status present
- Confirm model name on the page matches the candidate name
- Read the **live price** directly from the page. If it differs from `current_price` by more than 5%, update `current_price` in the merge output to reflect the live price
- Set `price_verified_live: true` and record the confirmed price in `price_at_generation`
- If the page is unavailable, sold out, or returns no price: set `price_verified_live: false`, `price_at_generation: null`, and `in_stock: false`
- **For in-store retailers:** verify the store location is set to the correct nearest store (per the user's city/state) before reading availability. Record the actual store name in `notes` if it differs from the user's city.

**Naming variant trap:** Near-identical product names are among the most common sources of wrong recommendations. Before finalizing any product, identify all naming variants in the product line and confirm which is correct. Search `[brand] [product line] variants` or `[product name] vs [similar name]` to surface the full variant tree.

**For non-US users:** confirm the regional model has identical specs to what is being described. Note any regional spec differences explicitly in the product card.

**If the product must interact with the user's existing hardware:** confirm compatibility at variant level before writing the card.
