import json
import os
import tempfile
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from evals.runner import run_evals

EVALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'contract-evals.json')

VALID_PURCHASE_OPTION = {
    "retailer": "Amazon",
    "url": "https://www.amazon.com/dp/B0XXXXX",
    "price": 149.99,
    "in_stock": True,
    "verified_live": True,
    "store_location": None,
    "page_title": "Product A - Amazon.com"
}

VALID_RESEARCH_LOG = {
    "run_dir": "runs/test",
    "searches": [
        {"track": "candidate-discovery", "query": "wireless gaming headsets buy US", "result_summary": "Found retailers"}
    ],
    "playwright_fetches": [
        {
            "track": "price-research",
            "product": "Product A",
            "retailer": "Amazon",
            "url": "https://www.amazon.com/dp/B0XXXXX",
            "page_title": "Product A - Amazon.com",
            "price_found": 149.99,
            "in_stock_found": True,
            "store_location_verified": None,
            "screenshot": "screenshots/product-a-amazon.png",
            "notes": None
        }
    ],
    "errors": []
}

def write_valid_run(run_dir):
    files = {
        "requirements.json": {
            "category": "wireless gaming headsets",
            "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
            "region": "US",
            "location": {"city": "Charlotte", "state": "NC"},
            "hard_filters": ["wireless"],
            "existing_hardware": None,
            "use_case": "gaming",
            "intake_complete": True
        },
        "research_foundation.json": {
            "retailers": ["Amazon", "Best Buy", "Micro Center"],
            "retailers_searched": ["Amazon", "Best Buy", "Micro Center", "Walmart", "Costco"],
            "category_sources": ["RTings"],
            "editorial_sources_found": ["Wirecutter"],
            "candidates": [
                {"name": "HyperX Cloud III", "source": "Best Buy", "source_type": "retailer", "url": "https://www.bestbuy.com/site/hyperx-cloud-iii/12345.p"}
            ]
        },
        "candidate_pool.json": {
            "candidates": [{
                "name": "HyperX Cloud III",
                "official_product_url": "https://hyperx.com/products/cloud-iii",
                "community_research": {"community_sentiment": "positive", "confirmed_issues": [], "sources": ["reddit.com/r/headphones"]},
                "spec_verification": {
                    "specs": {"frequency_response": {"status": "verified", "claimed": "10-21000Hz", "measured": "10-20000Hz", "source": "https://rtings.com/..."}},
                    "sources_checked": ["rtings.com", "reddit.com/r/headphones", "youtube.com/search?q=teardown", "notebookcheck.net", "hyperx.com/specs"],
                    "conditional_specs": [],
                    "flags": []
                },
                "price_research": {
                    "current_price": 149.99,
                    "currency": "USD",
                    "retailer": "Amazon",
                    "retailer_url": "https://www.amazon.com/dp/B0XXXXX",
                    "in_stock": True,
                    "price_history": "Typically $130-150",
                    "sale_eligible": False,
                    "consider_waiting": False,
                    "in_budget_only_at_sale_price": False,
                    "purchase_options": [VALID_PURCHASE_OPTION]
                },
                "lifecycle_check": {"recall_status": "clear", "recall_source": None, "lifecycle_status": "current", "ownership_change": None},
                "final_verification": {
                    "model_verified": True,
                    "url_verified": True,
                    "regional_spec_match": True,
                    "price_verified_live": True,
                    "price_at_generation": 149.99,
                    "notes": None
                },
                "safety_flag": False
            }]
        },
        "scored_products.json": {
            "ranked_products": [{
                "name": "HyperX Cloud III", "rank": 1, "score": 8.5,
                "score_breakdown": {
                    "price_to_value": 8.0, "spec_integrity": 9.0,
                    "community_reception": 8.5, "feature_quality": 8.5, "availability": 9.0,
                    "na_factors": []
                },
                "penalties": [],
                "flags": {
                    "safety_excluded": False, "stretch_pick": False,
                    "dominant_winner": False, "consider_waiting": False, "all_below_6": False
                }
            }],
            "guide_meta": {
                "product_count": 1, "category_type": "competitive",
                "category_type_rationale": "Wide market with 10+ options at this price point",
                "edge_cases_requiring_user_input": []
            }
        },
        "research_log.json": VALID_RESEARCH_LOG
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


def test_two_retailers_fails_c3():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "research_foundation.json")) as f:
            data = json.load(f)
        data["retailers"] = ["Amazon", "Best Buy"]
        with open(os.path.join(run_dir, "research_foundation.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        failed_ids = [f["id"] for f in results["failed"]]
        assert "C3" in failed_ids


def test_c11_zero_price_on_verified_option_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["purchase_options"][0]["price"] = 0
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C11" for f in results["failed"])


def test_c12_store_location_echoes_user_city_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        # store_location that just echoes the user's city/state — no store name
        data["candidates"][0]["price_research"]["purchase_options"][0]["store_location"] = "Charlotte, NC"
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C12" for f in results["failed"])


def test_c12_store_location_with_store_name_passes():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        # store_location includes actual store name — passes
        data["candidates"][0]["price_research"]["purchase_options"][0]["store_location"] = "Micro Center — Charlotte, NC"
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert not any(f["id"] == "C12" for f in results["failed"])


def test_c13_unverified_option_claiming_in_stock_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["purchase_options"][0]["verified_live"] = False
        # in_stock still True — should fail C13
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C13" for f in results["failed"])


def test_c14_missing_research_log_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        os.remove(os.path.join(run_dir, "research_log.json"))
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C14" for f in results["failed"])


def test_c16_in_budget_only_at_sale_without_consider_waiting_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["in_budget_only_at_sale_price"] = True
        data["candidates"][0]["price_research"]["consider_waiting"] = False
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C16" for f in results["failed"])


def test_c16_in_budget_only_at_sale_with_consider_waiting_passes():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["in_budget_only_at_sale_price"] = True
        data["candidates"][0]["price_research"]["consider_waiting"] = True
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert not any(f["id"] == "C16" for f in results["failed"])
