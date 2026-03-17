import json
import os
import tempfile
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from evals.runner import run_evals

EVALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'contract-evals.json')

def write_valid_run(run_dir):
    files = {
        "requirements.json": {
            "category": "wireless gaming headsets",
            "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
            "region": "US", "hard_filters": ["wireless"],
            "existing_hardware": None, "use_case": "gaming", "intake_complete": True
        },
        "research_foundation.json": {
            "retailers": ["Amazon", "Best Buy", "Micro Center"],
            "category_sources": ["RTings"],
            "editorial_sources_found": ["Wirecutter"],
            "candidates": [
                {"name": "SteelSeries Arctis Nova Pro", "source": "RTings", "source_type": "editorial", "url": "https://www.rtings.com/headphones/steelseries-arctis-nova-pro"},
                {"name": "HyperX Cloud III", "source": "Best Buy", "source_type": "retailer", "url": "https://www.bestbuy.com/site/hyperx-cloud-iii/12345.p"}
            ]
        },
        "candidate_pool.json": {
            "candidates": [{
                "name": "SteelSeries Arctis Nova Pro",
                "track_b": {"community_sentiment": "positive", "confirmed_issues": [], "sources": ["reddit.com/r/headphones"]},
                "track_c": {"spec_integrity": "verified", "conditional_specs": [], "measurement_sources": ["rtings.com"], "flags": []},
                "track_d": {"current_price": 149, "currency": "USD", "retailer": "Amazon", "retailer_url": "https://www.amazon.com/dp/B0XXXXX", "in_stock": True, "price_history": "Typically $130-150", "sale_eligible": False, "consider_waiting": False},
                "track_e": {"recall_status": "clear", "recall_source": None, "lifecycle_status": "current"},
                "track_f": {"model_verified": True, "url_verified": True, "regional_spec_match": True, "notes": None},
                "safety_flag": False
            }]
        },
        "scored_products.json": {
            "ranked_products": [{
                "name": "SteelSeries Arctis Nova Pro", "rank": 1, "score": 8.5,
                "score_breakdown": {"price_to_value": 8, "spec_integrity": 9, "community_reception": 8, "feature_quality": 9, "availability": 9, "na_factors": []},
                "penalties": [],
                "flags": {"safety_excluded": False, "stretch_pick": False, "dominant_winner": False, "consider_waiting": False, "all_below_6": False}
            }],
            "guide_meta": {
                "product_count": 1, "category_type": "competitive",
                "category_type_rationale": "Wide market with 10+ options at this price point",
                "edge_cases_requiring_user_input": []
            }
        }
    }
    for filename, data in files.items():
        with open(os.path.join(run_dir, filename), 'w') as f:
            json.dump(data, f)

def test_all_valid_files_pass():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        results = run_evals(run_dir, EVALS_FILE)
        assert not results["failed"], f"Unexpected failures: {results['failed']}"

def test_missing_required_file_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        os.remove(os.path.join(run_dir, "requirements.json"))
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C1" for f in results["failed"])

def test_two_retailers_fails_c2_or_c3():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "research_foundation.json")) as f:
            data = json.load(f)
        data["retailers"] = ["Amazon", "Best Buy"]
        with open(os.path.join(run_dir, "research_foundation.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        failed_ids = [f["id"] for f in results["failed"]]
        assert "C2" in failed_ids or "C3" in failed_ids
