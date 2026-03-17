# Track B — Community & Owner Intelligence

You receive a list of candidate products, the user's region, and a run directory path. Research community and owner intelligence for each candidate.

**Read the Track B section of `buyers-guide-refactored/buyers-guide/references/research.md` before starting.**

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
