# Track E — Availability & Lifecycle

You receive a list of candidate products, the user's region, and a run directory path. Check recall status, lifecycle, and ownership history for each candidate.

**Read the Track E section of `references/research.md` before starting. Use the correct recall database for the user's region (CPSC for US, RAPEX for EU, OPSS for UK, productsafety.gov.au for AU, healthycanadians.gc.ca for CA).**

## Step 1 — Recall and lifecycle check

For each candidate:
- Search the correct regional recall database for any active recalls
- Search `[product name] discontinued` and `[product name] successor` to determine lifecycle status
- Set `recall_status`, `recall_source`, and `lifecycle_status` per the valid values below

## Step 2 — Ownership and acquisition check

For each candidate, search for any acquisition or ownership change of the manufacturer within the past 3 years:
- Search `[manufacturer name] acquired` and `[manufacturer name] acquisition [year]`
- Search `[manufacturer name] bought by` and `[brand] parent company`
- If an acquisition is found: verify the date, the acquirer, and whether the brand continues to operate independently
- Record in `ownership_change`: `"[Manufacturer] acquired by [Acquirer] on [Month YYYY]. [One sentence on operational continuity and warranty implications.]"`
- If no acquisition is found within the past 3 years: set `ownership_change: null`

Acquisitions matter to buyers because: warranty obligations may transfer, product roadmaps may change, and support quality often shifts post-acquisition. Always surface this information so the buyer can assess risk.

## Output

Write `[run_dir]/track_e_results.json`:
```json
{
  "results": {
    "Product Name": {
      "recall_status": "clear",
      "recall_source": null,
      "lifecycle_status": "current",
      "ownership_change": null
    }
  }
}
```

Valid values for `recall_status`: `clear`, `recalled`, `check_failed`.
Valid values for `lifecycle_status`: `current`, `discontinued`, `successor_imminent`, `successor_announced`.
`ownership_change`: null if no acquisition in past 3 years; otherwise a string describing the acquisition and continuity.
