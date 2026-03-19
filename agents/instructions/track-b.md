# Track B — Community & Owner Intelligence

You receive a list of candidate products, the user's region, and a run directory path. Research community and owner intelligence for each candidate.

**Read the Track B section of `references/research.md` before starting.**

## Output

Write `[run_dir]/track_b_results.json`:
```json
{
  "results": {
    "Product Name": {
      "community_sentiment": "positive",
      "confirmed_issues": ["issue confirmed by 3+ distinct sources"],
      "sources": ["https://reddit.com/...", "https://..."]
    }
  }
}
```

Valid values for `community_sentiment`: `positive`, `mixed`, `negative`, `insufficient_data`.

A complaint qualifies as a confirmed issue only if it appears in at least 3 distinct community sources.

**Source quality — independent vs. manufacturer-hosted:**
- **Independent sources** (Reddit, enthusiast forums, independent review sites, YouTube): full weight
- **Manufacturer-hosted review platforms** (Judge.me on the brand's own storefront, Trustpilot linked from the brand's site, on-site star ratings): note the platform in `sources` and treat with lower weight — these can be curated or filtered by the seller
- If community sentiment is positive but based primarily on manufacturer-hosted reviews with minimal independent discussion, set `community_sentiment: "insufficient_data"` and note: `"Sentiment appears positive but based largely on manufacturer-hosted reviews ([platform]) — limited independent community data found."`
- Never let a high aggregate score on a manufacturer-hosted platform drive a `positive` rating if independent Reddit/forum discussion is absent or minimal
