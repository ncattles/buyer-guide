# Track D — Price Intelligence

You receive a list of candidate products (each with a `url` field), the user's region, the currency, and a run directory path. Verify current prices and stock status by fetching each retailer listing directly, then research price history.

**Read the Track D section of `references/research.md` before starting.**

## Step 1 — Live price and stock check

For each candidate, fetch the retailer product page URL using WebFetch. From the live page extract:
- **Current price** — the price shown on the product listing right now
- **In stock** — whether the product is available to purchase (look for "Add to Cart", "In Stock", "Out of Stock", "Sold Out", "Currently Unavailable" indicators)
- **Retailer** — confirm which retailer this is

If the page fails to load or returns an error, record `current_price: 0`, `in_stock: false`, and note in `price_history`.

## Step 2 — Price history

Use the correct price history tool for each retailer (CamelCamelCamel for Amazon, Keepa for Amazon DE/UK, check retailer's own price history where available). Record the typical price range and whether current price is at/above/below average.

## Output

Write `[run_dir]/track_d_results.json`:
```json
{
  "results": {
    "Product Name": {
      "current_price": 149.99,
      "currency": "USD",
      "retailer": "Amazon",
      "retailer_url": "https://www.amazon.com/dp/B0XXXXX",
      "in_stock": true,
      "price_history": "Typically $130–150; currently near average",
      "sale_eligible": false,
      "consider_waiting": false
    }
  }
}
```

For new products with no price history, set `price_history` to `"Insufficient data — launched [Month YYYY]"`.
Sale eligibility requires ≥3 confirmed sale events at the lower price.
