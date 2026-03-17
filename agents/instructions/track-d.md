# Track D — Price Intelligence

You receive a list of candidate products, the user's region, the currency, and a run directory path. Research current prices and price history for each candidate.

**Read the Track D section of `references/research.md` before starting. Use the correct price history tool for each retailer (CamelCamelCamel for Amazon, regional alternatives for others).**

## Output

Write `[run_dir]/track_d_results.json`:
```json
{
  "results": {
    "Product Name": {
      "current_price": 149.99,
      "currency": "USD",
      "retailer": "Amazon",
      "price_history": "Typically $130–150; currently near average",
      "sale_eligible": false,
      "consider_waiting": false
    }
  }
}
```

For new products with no price history, set `price_history` to `"Insufficient data — launched [Month YYYY]"`.
Sale eligibility requires ≥3 confirmed sale events at the lower price.
