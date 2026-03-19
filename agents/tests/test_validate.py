import pytest
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from validate import validate_contract, ValidationError

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), '..', 'schemas')

def test_valid_requirements_passes():
    data = {
        "category": "wireless gaming headsets",
        "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
        "region": "US",
        "location": {"city": "Charlotte", "state": "NC"},
        "hard_filters": ["wireless"],
        "existing_hardware": None,
        "use_case": "gaming",
        "intake_complete": True
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'requirements.schema.json'))

def test_requirements_location_null_passes():
    data = {
        "category": "wireless gaming headsets",
        "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
        "region": "US",
        "location": None,
        "hard_filters": [],
        "existing_hardware": None,
        "use_case": "gaming",
        "intake_complete": True
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'requirements.schema.json'))

def test_missing_intake_complete_fails():
    data = {
        "category": "wireless gaming headsets",
        "budget": {"amount": 150, "currency": "USD", "format": "under $150"},
        "region": "US",
        "hard_filters": []
    }
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'requirements.schema.json'))

VALID_RESEARCH_FOUNDATION = {
    "retailers": ["Amazon", "Best Buy", "Micro Center"],
    "retailers_searched": ["Amazon", "Best Buy", "Micro Center", "Walmart", "Costco"],
    "category_sources": ["RTings"],
    "editorial_sources_found": ["Wirecutter"],
    "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer", "url": "https://www.amazon.com/dp/B0XXXXX"}]
}

def test_research_foundation_requires_three_retailers():
    data = {**VALID_RESEARCH_FOUNDATION, "retailers": ["Amazon", "Best Buy"]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))

def test_research_foundation_with_three_retailers_passes():
    validate_contract(VALID_RESEARCH_FOUNDATION, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))

def test_research_foundation_missing_retailers_searched_fails():
    data = {k: v for k, v in VALID_RESEARCH_FOUNDATION.items() if k != "retailers_searched"}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))

def test_research_foundation_candidate_missing_url_fails():
    data = {**VALID_RESEARCH_FOUNDATION, "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer"}]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))


VALID_CANDIDATE = {
    "name": "Product A",
    "official_product_url": "https://manufacturer.com/product-a",
    "community_research": {"community_sentiment": "positive", "confirmed_issues": [], "sources": ["Reddit"]},
    "spec_verification": {
        "specs": {"peak_brightness": {"status": "verified", "claimed": "1000 nits", "measured": "980 nits", "source": "https://rtings.com/..."}},
        "sources_checked": ["rtings.com", "reddit.com/r/Monitors", "youtube.com/search?q=teardown", "tftcentral.co.uk", "manufacturer.com/specs"],
        "conditional_specs": [],
        "flags": []
    },
    "price_research": {
        "current_price": 99.99,
        "currency": "USD",
        "retailer": "Amazon",
        "retailer_url": "https://www.amazon.com/dp/B0XXXXX",
        "in_stock": True,
        "price_history": "stable",
        "sale_eligible": False,
        "consider_waiting": False,
        "in_budget_only_at_sale_price": False,
        "purchase_options": [
            {"retailer": "Amazon", "url": "https://www.amazon.com/dp/B0XXXXX", "price": 99.99, "in_stock": True, "verified_live": True, "store_location": None, "page_title": "Product A - Amazon.com"}
        ]
    },
    "lifecycle_check": {"recall_status": "clear", "recall_source": None, "lifecycle_status": "current", "ownership_change": None},
    "final_verification": {"model_verified": True, "url_verified": True, "regional_spec_match": True, "price_verified_live": True, "price_at_generation": 99.99, "notes": None},
    "safety_flag": False
}

def test_valid_candidate_pool_passes():
    data = {"candidates": [VALID_CANDIDATE]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_requires_at_least_one_candidate():
    data = {"candidates": []}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_enforces_max_15():
    data = {"candidates": [VALID_CANDIDATE] * 16}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_track_c_fewer_than_5_sources_checked_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["spec_verification"] = {
        "specs": {"brightness": {"status": "verified", "claimed": "500 nits", "measured": "490 nits", "source": "https://rtings.com/"}},
        "sources_checked": ["rtings.com", "notebookcheck.net", "reddit.com"],
        "conditional_specs": [],
        "flags": []
    }
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_track_c_missing_sources_checked_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["spec_verification"] = {
        "specs": {"brightness": {"status": "verified", "claimed": "500 nits", "measured": "490 nits", "source": "https://rtings.com/"}},
        "conditional_specs": [],
        "flags": []
    }
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_track_c_empty_specs_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["spec_verification"] = {
        "specs": {},
        "sources_checked": ["rtings.com"],
        "conditional_specs": [],
        "flags": []
    }
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_track_c_invalid_status_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["spec_verification"] = {
        "specs": {"brightness": {"status": "unverified", "claimed": "500 nits", "measured": None, "source": None}},
        "sources_checked": ["rtings.com"],
        "conditional_specs": [],
        "flags": []
    }
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_track_c_no_source_status_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["spec_verification"] = {
        "specs": {"battery_life": {"status": "no_source", "claimed": "20 hours", "measured": None, "source": None}},
        "sources_checked": ["notebookcheck.net", "reddit.com/r/hardware", "youtube.com/search?q=teardown", "anandtech.com", "manufacturer.com/specs"],
        "conditional_specs": [],
        "flags": ["Battery life: No independent measurements found — manufacturer claim unverified"]
    }
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_price_verified_live_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["final_verification"] = {"model_verified": True, "url_verified": True, "regional_spec_match": True, "notes": None}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_price_at_generation_null_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["final_verification"] = {"model_verified": True, "url_verified": False, "regional_spec_match": True, "price_verified_live": False, "price_at_generation": None, "notes": "Page unavailable at generation time"}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_purchase_options_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {k: v for k, v in VALID_CANDIDATE["price_research"].items() if k != "purchase_options"}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_purchase_options_multiple_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {**VALID_CANDIDATE["price_research"], "purchase_options": [
        {"retailer": "Amazon", "url": "https://www.amazon.com/dp/B0XXXXX", "price": 99.99, "in_stock": True, "verified_live": True, "store_location": None},
        {"retailer": "Best Buy", "url": "https://www.bestbuy.com/product/12345", "price": 109.99, "in_stock": True, "verified_live": True, "store_location": None}
    ]}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_purchase_option_with_store_location_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {**VALID_CANDIDATE["price_research"], "purchase_options": [
        {"retailer": "Micro Center", "url": "https://www.microcenter.com/product/12345", "price": 99.99, "in_stock": True, "verified_live": True, "store_location": "Micro Center — Charlotte, NC"}
    ]}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_purchase_option_missing_verified_live_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {**VALID_CANDIDATE["price_research"], "purchase_options": [
        {"retailer": "Amazon", "url": "https://www.amazon.com/dp/B0XXXXX", "price": 99.99, "in_stock": True}
    ]}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_in_stock_fails():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {k: v for k, v in VALID_CANDIDATE["price_research"].items() if k != "in_stock"}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_safety_flag_fails():
    candidate = {k: v for k, v in VALID_CANDIDATE.items() if k != "safety_flag"}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_valid_scored_products_passes():
    data = {
        "ranked_products": [{
            "name": "Product A",
            "rank": 1,
            "score": 8.5,
            "score_breakdown": {
                "price_to_value": 9.0, "spec_integrity": 8.0,
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
            "product_count": 1,
            "category_type": "focused",
            "category_type_rationale": "Hard filters reduced pool to 1 product.",
            "edge_cases_requiring_user_input": []
        }
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'scored_products.schema.json'))

def test_scored_products_missing_guide_meta_fails():
    data = {"ranked_products": []}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'scored_products.schema.json'))

def test_scored_products_invalid_category_type_fails():
    data = {
        "ranked_products": [],
        "guide_meta": {
            "product_count": 0,
            "category_type": "unknown",
            "category_type_rationale": "test"
        }
    }
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'scored_products.schema.json'))


VALID_RESEARCH_LOG = {
    "run_dir": "runs/2026-03-18T001035",
    "searches": [
        {"track": "candidate-discovery", "query": "RTX 5080 9800X3D prebuilt buy US", "result_summary": "Found 6 retailers"},
        {"track": "price-research", "query": "PowerSpec G757 price", "result_summary": "Found Micro Center listing"}
    ],
    "playwright_fetches": [
        {
            "track": "price-research",
            "product": "PowerSpec G757",
            "retailer": "Micro Center",
            "url": "https://www.microcenter.com/product/698877/powerspec-g757-gaming-pc",
            "page_title": "PowerSpec G757 Gaming PC; AMD Ryzen 7 9800X3D - Micro Center",
            "price_found": 2499.99,
            "in_stock_found": True,
            "store_location_verified": "Micro Center — Charlotte, NC",
            "screenshot": "screenshots/powerspec-g757-micro-center.png",
            "notes": None
        }
    ],
    "errors": []
}

def test_valid_research_log_passes():
    validate_contract(VALID_RESEARCH_LOG, os.path.join(SCHEMAS_DIR, 'research_log.schema.json'))

def test_research_log_missing_searches_fails():
    data = {k: v for k, v in VALID_RESEARCH_LOG.items() if k != "searches"}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_log.schema.json'))

def test_research_log_missing_playwright_fetches_fails():
    data = {k: v for k, v in VALID_RESEARCH_LOG.items() if k != "playwright_fetches"}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_log.schema.json'))

def test_research_log_fetch_missing_page_title_fails():
    bad_fetch = {k: v for k, v in VALID_RESEARCH_LOG["playwright_fetches"][0].items() if k != "page_title"}
    data = {**VALID_RESEARCH_LOG, "playwright_fetches": [bad_fetch]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_log.schema.json'))

def test_research_log_empty_errors_passes():
    data = {**VALID_RESEARCH_LOG, "errors": []}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_log.schema.json'))

def test_candidate_pool_official_product_url_string_passes():
    data = {"candidates": [VALID_CANDIDATE]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_official_product_url_null_passes():
    candidate = {**VALID_CANDIDATE, "official_product_url": None}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_official_product_url_fails():
    candidate = {k: v for k, v in VALID_CANDIDATE.items() if k != "official_product_url"}
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_in_budget_only_at_sale_price_fails():
    candidate = dict(VALID_CANDIDATE)
    price_research = {k: v for k, v in VALID_CANDIDATE["price_research"].items() if k != "in_budget_only_at_sale_price"}
    candidate["price_research"] = price_research
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_in_budget_only_at_sale_price_true_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["price_research"] = {**VALID_CANDIDATE["price_research"], "in_budget_only_at_sale_price": True}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_missing_ownership_change_fails():
    candidate = dict(VALID_CANDIDATE)
    lifecycle_check = {k: v for k, v in VALID_CANDIDATE["lifecycle_check"].items() if k != "ownership_change"}
    candidate["lifecycle_check"] = lifecycle_check
    data = {"candidates": [candidate]}
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))

def test_candidate_pool_ownership_change_string_passes():
    candidate = dict(VALID_CANDIDATE)
    candidate["lifecycle_check"] = {**VALID_CANDIDATE["lifecycle_check"], "ownership_change": "Acme Corp acquired by MegaCorp on June 2024. Brand continues to operate independently; warranty obligations transferred."}
    data = {"candidates": [candidate]}
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'candidate_pool.schema.json'))
