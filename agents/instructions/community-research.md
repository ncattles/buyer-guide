# Community Research — Community & Owner Intelligence

You receive a list of candidate products, the user's region, and a run directory path. Research community and owner intelligence for each candidate.

**Read the Community Research section of `references/research.md` before starting.**

## Use-case derived signals

Before searching for general community sentiment, read `use_case` from `requirements.json` and identify signals that matter for that use case. Users often don't know to search for these — but discovering them after purchase causes returns.

Target these additional searches based on the stated use case:
- **work / office / calls**: search `[product] microphone quality calls`, `[product] mic Zoom Teams`, `[product] background noise pickup`, `[product] call clarity review`. A mic that picks up keyboard noise, HVAC, or construction sounds in calls is a confirmed issue if 3+ sources report it.
- **travel / commute**: search `[product] comfort long flight`, `[product] ear pressure airplane`, `[product] passive isolation without ANC`.
- **gym / fitness**: search `[product] slips during workout`, `[product] sweat damage`, `[product] IP rating real world`.
- **gaming**: search `[product] input lag`, `[product] mic sidetone`, `[product] surround sound test`.

Any confirmed finding (3+ distinct sources) from use-case derived searches must appear in `confirmed_issues`. If positive, note it in the `community_sentiment` rationale. Do not omit these findings just because the user didn't ask — they are the most valuable part of community research for users who don't know what they don't know.

## Output

Write `[run_dir]/community-research-results.json`:
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
