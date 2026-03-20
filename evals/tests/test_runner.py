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
        {"phase": "candidate-discovery", "timestamp": "2026-03-18T17:32:58Z", "query": "wireless gaming headsets buy US Amazon Best Buy Micro Center Walmart Costco", "result_summary": "Found retailers"}
    ],
    "playwright_fetches": [
        {
            "phase": "price-research",
            "timestamp": "2026-03-18T17:45:12Z",
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
    "errors": [],
    "token_usage": {
        "total": 48000,
        "by_phase": {
            "candidate_discovery": 12000,
            "community_research": 8000,
            "spec_verification": 10000,
            "price_research": 12000,
            "lifecycle_check": 4000,
            "final_verification": 2000
        }
    },
    "sources": [
        {
            "candidate": "Product A",
            "phase": "community-research",
            "classification": "community",
            "url": "https://reddit.com/r/headphones/comments/example",
            "label": "reddit.com"
        }
    ]
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
        "research_log.json": VALID_RESEARCH_LOG,
        "scoring_log.json": {
            "run_dir": "runs/test",
            "started_at": "2026-03-18T18:45:00Z",
            "completed_at": "2026-03-18T18:45:30Z",
            "candidates_received": 1,
            "candidates_scored": 1,
            "filters": {"safety_excluded": [], "hard_filter_excluded": [], "budget_excluded": []},
            "scoring": [{
                "name": "HyperX Cloud III",
                "final_score": 8.5,
                "factor_rationale": {
                    "price_to_value": {"score": 8.0, "rationale": "Strong value at $149"},
                    "spec_integrity": {"score": 9.0, "rationale": "All specs verified"},
                    "community_reception": {"score": 8.5, "rationale": "Positive sentiment, no recurring issues"},
                    "feature_quality": {"score": 8.5, "rationale": "Strong audio for gaming"},
                    "availability": {"score": 9.0, "rationale": "In stock at Amazon and Best Buy"}
                },
                "na_factors": [],
                "penalties": [],
                "stretch_pick": False
            }],
            "tiebreakers_applied": [],
            "edge_case_decisions": [
                {"type": "dominant_winner", "applied": False, "detail": None},
                {"type": "all_below_6", "applied": False, "detail": None}
            ]
        }
    }
    for filename, data in files.items():
        with open(os.path.join(run_dir, filename), 'w') as f:
            json.dump(data, f)
    # Create screenshot referenced in research_log so C21 passes
    os.makedirs(os.path.join(run_dir, "screenshots"), exist_ok=True)
    with open(os.path.join(run_dir, "screenshots", "product-a-amazon.png"), 'wb') as f:
        f.write(b'\x89PNG\r\n')


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


def test_c17_retailer_with_no_log_evidence_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "research_foundation.json")) as f:
            data = json.load(f)
        data["retailers_searched"].append("Corsair Direct")
        with open(os.path.join(run_dir, "research_foundation.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C17" for f in results["failed"])


def test_c17_all_retailers_have_evidence_passes():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        results = run_evals(run_dir, EVALS_FILE)
        assert not any(f["id"] == "C17" for f in results["failed"])


def test_c18_missing_scoring_log_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        os.remove(os.path.join(run_dir, "scoring_log.json"))
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C18" for f in results["failed"])


def test_c19_in_stock_no_purchase_options_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["purchase_options"] = []
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C19" for f in results["failed"])


def test_c20_null_official_url_without_flag_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["official_product_url"] = None
        data["candidates"][0]["spec_verification"]["flags"] = []
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C20" for f in results["failed"])


def test_c20_null_official_url_with_flag_passes():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["official_product_url"] = None
        data["candidates"][0]["spec_verification"]["flags"] = ["Official product page: Not found — retailer-exclusive brand"]
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert not any(f["id"] == "C20" for f in results["failed"])


def test_c21_missing_screenshot_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        os.remove(os.path.join(run_dir, "screenshots", "product-a-amazon.png"))
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C21" for f in results["failed"])


def test_c21_existing_screenshot_passes():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        results = run_evals(run_dir, EVALS_FILE)
        assert not any(f["id"] == "C21" for f in results["failed"])


def test_c22_safety_flag_false_with_unclear_recall_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["lifecycle_check"]["recall_status"] = "unclear"
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C22" for f in results["failed"])


def test_c23_unsorted_purchase_options_fails():
    with tempfile.TemporaryDirectory() as run_dir:
        write_valid_run(run_dir)
        with open(os.path.join(run_dir, "candidate_pool.json")) as f:
            data = json.load(f)
        data["candidates"][0]["price_research"]["purchase_options"].append({
            "retailer": "Best Buy",
            "url": "https://www.bestbuy.com/product/XXXXX",
            "price": 99.99,
            "in_stock": True,
            "verified_live": True,
            "store_location": None,
            "page_title": "HyperX Cloud III - Best Buy"
        })
        with open(os.path.join(run_dir, "candidate_pool.json"), 'w') as f:
            json.dump(data, f)
        results = run_evals(run_dir, EVALS_FILE)
        assert any(f["id"] == "C23" for f in results["failed"])
