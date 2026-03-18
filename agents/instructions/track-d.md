# Track D — Price Intelligence

You receive a list of candidate products (each with a `url` field), the user's region, the currency, the budget, and a run directory path. Your job is to find **every retailer** where each product is sold within the user's region, verify prices and stock status live, and research price history.

**Read the Track D section of `references/research.md` before starting.**

## Step 1 — Multi-retailer discovery

For each candidate, do not rely only on the URL provided by Track A. Search for all retailers carrying this product:
- Search `[product name] buy` and `[product name] price` to surface all active retailers
- Check price comparison aggregators (Google Shopping, PriceGrabber) for the full retailer list
- Check manufacturer direct if applicable

Record every retailer that lists this product. You will verify each one live in Step 2.

## Step 2 — Live price and stock verification via Playwright

**Use Playwright exclusively for live price and availability checks. Do not use WebFetch — major retailers (Micro Center, Best Buy, Amazon, Walmart) block it and will return 403 errors or CAPTCHA pages, producing stale or fabricated prices.**

For each retailer found in Step 1, use Playwright to navigate to the product listing page:
- Confirm the page loads as a product listing (product name visible, price shown, add-to-cart or availability status present)
- Extract the **current price** shown on the page
- Extract **in-stock status** (look for "Add to Cart", "In Stock", "Out of Stock", "Sold Out", "Unavailable", "Backordered", "Pickup Unavailable" / "Shipping Unavailable" indicators — if both pickup and shipping are unavailable, `in_stock: false`)
- Confirm the product name on the page matches the candidate name
- Set `verified_live: true` if price and stock were read directly from a live page; `false` only if Playwright itself fails to load the page (network error, hard block)

**For in-store-only retailers:** Before verifying price/stock, set the store location to the nearest location to the user's city/state:
- Navigate to the retailer's store locator
- Search by the user's city and state from `requirements.json`
- Select the nearest store result
- Only then navigate to the product page — availability shown will reflect that specific store
- Record the actual store name and city in `store_location` (e.g., `"Micro Center — Charlotte, NC"`)
- **Never assume a store exists in the user's city.** Verify the nearest location via the store locator before claiming in-store availability. If no store exists within 100 miles, note the distance to the nearest location.

**Price eligibility:** Only include purchase options where the verified live price is within the user's budget. Options where the live price exceeds budget are excluded from `purchase_options` (do not include over-budget options even if the research agent found them).

## Step 3 — Price history

Use the correct price history tool for each retailer:
- Amazon: CamelCamelCamel (`camelcamelcamel.com/product/[ASIN]`)
- Others: Google Shopping price history graph, regional deal aggregators (Slickdeals for US, HotUKDeals for UK, etc.), search `[product name] price history`

Record the typical price range and whether the current price is at/above/below average.

## Output

Write `[run_dir]/track_d_results.json`:
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
      "purchase_options": [
        {
          "retailer": "Micro Center",
          "url": "https://www.microcenter.com/product/XXXXX/product-name",
          "price": 2499.99,
          "in_stock": true,
          "verified_live": true,
          "store_location": "Micro Center — Charlotte, NC"
        },
        {
          "retailer": "Newegg",
          "url": "https://www.newegg.com/p/XXXXX",
          "price": 2599.99,
          "in_stock": true,
          "verified_live": true,
          "store_location": null
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
