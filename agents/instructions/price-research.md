# Price Research — Price Intelligence

You receive a list of candidate products (each with a `url` field), the user's region, the currency, the budget, and a run directory path. Your job is to find **every retailer** where each product is sold within the user's region, verify prices and stock status live, and research price history.

**Read the Price Research section of `references/research.md` before starting.**

## Step 1 — Multi-retailer discovery

For each candidate, do not rely only on the URL provided by Candidate Discovery. Search for all retailers carrying this product:
- **Find and check the official manufacturer product page.** Search `[manufacturer name] [product name] official` or `[product name] site:[manufacturer domain]`. Navigate to it with Playwright. If the page has a price / add-to-cart button, the manufacturer sells direct — record it as a purchase option and verify its price in Step 2. Do not wait for or depend on Spec Verification's output — Price Research runs in parallel and must find the official URL independently.
- Search `[product name] buy` and `[product name] price` to surface all active retailers
- Check price comparison aggregators (Google Shopping, PriceGrabber) for the full retailer list

Record every retailer that lists this product. You will verify each one live in Step 2.

**The official product page is never skipped.** Even if it only shows info (no price), record it. If it sells direct, it must be Playwright-verified the same as any other retailer — it may have a price cheaper or different from third-party retailers.

## Step 2 — Live price and stock verification via Playwright

**Use Playwright exclusively for live price and availability checks. Do not use WebFetch — major retailers (Micro Center, Best Buy, Amazon, Walmart) block it and will return 403 errors or CAPTCHA pages, producing stale or fabricated prices.**

For each retailer found in Step 1, use Playwright to navigate to the product listing page:
- Confirm the page loads as a product listing (product name visible, price shown, add-to-cart or availability status present)
- Extract the **current price** shown on the page
- Extract **in-stock status** (look for "Add to Cart", "In Stock", "Out of Stock", "Sold Out", "Unavailable", "Backordered", "Pickup Unavailable" / "Shipping Unavailable" indicators — if both pickup and shipping are unavailable, `in_stock: false`)
- Confirm the product name on the page matches the candidate name
- Set `verified_live: true` if price and stock were read directly from a live page; `false` only if Playwright itself fails to load the page (network error, hard block)

**For any retailer with physical store locations** (including hybrid retailers like Best Buy, Walmart, Target — not just in-store-only retailers): Before verifying price/stock, set the store/zip location to the user's city/state:
- Navigate to the retailer's store locator or zip code selector
- Enter the user's city and state from `requirements.json`
- Select the nearest store result
- Only then navigate to the product page — availability and pickup status shown will reflect that specific store
- Record the actual store name and city in `store_location` (e.g., `"Best Buy — Raleigh, NC (6030 Glenwood Ave)"`)
- **The screenshot must visibly show the location indicator** so the audit trail proves which store's availability was read
- **Never assume a store exists in the user's city.** Verify the nearest location via the store locator before claiming in-store or pickup availability.
- **Distance is never a reason to exclude a product.** If the nearest store is 50 miles away or 300 miles away, include the product in `purchase_options` and note the distance clearly (e.g., `"store_location": "Micro Center — Charlotte, NC (~170 miles from Raleigh)"`). Whether to make that drive is the user's decision, not the pipeline's.
- **Always report in-store/pickup stock separately from shipping stock.** A product can be available to ship nationally but out of stock for pickup at the user's nearest store — report both. Use `in_stock_pickup` and `in_stock_shipping` in your notes if they differ. The `in_stock` field in `purchase_options` reflects whether the product can actually be obtained — true if either pickup or shipping is available.

**Screenshot evidence (required):** For each product listing page loaded via Playwright:
1. After the page loads, **do not screenshot immediately** — the initial view shows only the product image and specs, not availability.
2. Use `browser_scroll` (scroll down the page, repeating as needed) until the **Add to Cart button, pickup availability, and shipping availability are all visible** on screen. For sites that use sticky headers with the location/zip indicator, it will remain visible as you scroll — confirm it is still in frame before screenshotting.
3. **Verify before saving:** the screenshot must show all of: (a) Add to Cart button or stock status message, (b) pickup and/or shipping availability, (c) the store name or zip code / location indicator. If any of these are missing, scroll to find a position where all three are simultaneously visible, then screenshot.
4. Save the screenshot to `[run_dir]/screenshots/[product-slug]-[retailer-slug].png`. Use lowercase, hyphens only, no spaces in filenames.
5. Record the screenshot filename in the `research_log.json` entry for that fetch.

A screenshot that shows only the product image and specs but not the Add to Cart / availability section is **not valid evidence** — retake it after scrolling. A screenshot missing the location indicator is **not valid evidence for in-store retailers** — scroll to find a position where both location and availability are in frame.

**page_title (required):** For each Playwright fetch, record the browser tab title (`page.title()` or from the page metadata). This proves which page was loaded. Store it in the purchase option's `page_title` field and in the research_log entry.

**Price eligibility:** Only include purchase options where the verified live price is within the user's budget. Options where the live price exceeds budget are excluded from `purchase_options` (do not include over-budget options even if the research agent found them).

## Step 2b — SKU and config consistency check

After verifying all purchase options, confirm the product verified matches what Candidate Discovery found:
- If the SKU or configuration (storage capacity, RAM, etc.) of the verified product differs from what Candidate Discovery's URL pointed to, add a `flags` entry: `"SKU change: Candidate Discovery found [original config/SKU]; Price Research verified [actual config/SKU]. [Brief explanation of the difference and why the switch was made.]"`
- Never silently switch to a different config without flagging it

## Step 3 — Price history

Use the correct price history tool for each retailer:
- Amazon: CamelCamelCamel (`camelcamelcamel.com/product/[ASIN]`)
- Others: Google Shopping price history graph, regional deal aggregators (Slickdeals for US, HotUKDeals for UK, etc.), search `[product name] price history`

Record the typical price range and whether the current price is at/above/below average.

**Price history config consistency:** If the historical price data is for a different configuration (e.g., 1TB variant when the current product is 2TB), note this explicitly in `price_history`: `"Note: historical data is for the [config] variant — not directly comparable to the current [config] listing."` Never present a different config's price history as if it applies to the current product.

## Output

Write `[run_dir]/price-research-results.json`:
```json
{
  "results": {
    "Product Name": {
      "current_price": 2499.99,
      "currency": "USD",
      "retailer": "Micro Center",
      "retailer_url": "https://www.microcenter.com/product/XXXXX/product-name",
      "in_stock": true,
      "price_history": "Typically $2,399–$2,499; currently near average",
      "sale_eligible": false,
      "consider_waiting": false,
      "in_budget_only_at_sale_price": false,
      "purchase_options": [
        {
          "retailer": "Micro Center",
          "url": "https://www.microcenter.com/product/XXXXX/product-name",
          "price": 2499.99,
          "in_stock": true,
          "verified_live": true,
          "store_location": "Micro Center — Charlotte, NC",
          "page_title": "PowerSpec G757 Gaming PC; AMD Ryzen 7 9800X3D ... - Micro Center"
        },
        {
          "retailer": "Newegg",
          "url": "https://www.newegg.com/p/XXXXX",
          "price": 2599.99,
          "in_stock": true,
          "verified_live": true,
          "store_location": null,
          "page_title": "PowerSpec G757 Gaming PC ... - Newegg.com"
        }
      ]
    }
  }
}
```

- `current_price`, `retailer`, `retailer_url`, `in_stock` always reflect the **lowest verified in-stock price** across all purchase options
- `purchase_options` contains all verified options **within budget**, sorted by price ascending
- If only one retailer carries the product under budget, `purchase_options` will have one entry
- For new products with no price history, set `price_history` to `"Insufficient data — launched [Month YYYY]"`
- Sale eligibility requires ≥3 confirmed sale events at the lower price
- **`in_budget_only_at_sale_price` (required):** Set to `true` if the product's regular/list price exceeds the user's budget but the current verified price is within budget (i.e., the product only qualifies because of a sale or promotion). Set to `false` otherwise. You own this field — do not leave it for the orchestrator to infer.
- **`consider_waiting` when `in_budget_only_at_sale_price: true` (required):** If the product's regular/list price exceeds the user's budget and it only qualifies because of a current promotion, you must set `consider_waiting` to a reason string — never `false`. Example: `"Price is promotional — regular retail of $X,XXX exceeds your budget of $Y,YYY. The sale may end at any time. Only purchase if the current price is confirmed active."` Setting `consider_waiting: false` on a product with `in_budget_only_at_sale_price: true` will fail eval C16.
