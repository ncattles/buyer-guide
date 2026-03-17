# Track E — Availability & Lifecycle

You receive a list of candidate products, the user's region, and a run directory path. Check recall status and lifecycle for each candidate.

**Read the Track E section of `references/research.md` before starting. Use the correct recall database for the user's region (CPSC for US, RAPEX for EU, OPSS for UK, productsafety.gov.au for AU, healthycanadians.gc.ca for CA).**

## Output

Write `[run_dir]/track_e_results.json`:
```json
{
  "results": {
    "Product Name": {
      "recall_status": "clear",
      "recall_source": null,
      "lifecycle_status": "current"
    }
  }
}
```

Valid values for `recall_status`: `clear`, `recalled`, `check_failed`.
Valid values for `lifecycle_status`: `current`, `discontinued`, `successor_imminent`, `successor_announced`.
