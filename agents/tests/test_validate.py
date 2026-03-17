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
        "hard_filters": ["wireless"],
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

def test_research_foundation_requires_three_retailers():
    data = {
        "retailers": ["Amazon", "Best Buy"],
        "category_sources": ["RTings"],
        "editorial_sources_found": [],
        "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer"}]
    }
    with pytest.raises(ValidationError):
        validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))

def test_research_foundation_with_three_retailers_passes():
    data = {
        "retailers": ["Amazon", "Best Buy", "Micro Center"],
        "category_sources": ["RTings"],
        "editorial_sources_found": ["Wirecutter"],
        "candidates": [{"name": "Product A", "source": "Amazon", "source_type": "retailer"}]
    }
    validate_contract(data, os.path.join(SCHEMAS_DIR, 'research_foundation.schema.json'))


VALID_CANDIDATE = {
    "name": "Product A",
    "track_b": {"community_sentiment": "positive", "confirmed_issues": [], "sources": ["Reddit"]},
    "track_c": {"spec_integrity": "verified", "conditional_specs": [], "measurement_sources": ["RTings"], "flags": []},
    "track_d": {"current_price": 99.99, "currency": "USD", "retailer": "Amazon", "price_history": "stable", "sale_eligible": False, "consider_waiting": False},
    "track_e": {"recall_status": "clear", "recall_source": None, "lifecycle_status": "current"},
    "track_f": {"model_verified": True, "url_verified": True, "regional_spec_match": True, "notes": None},
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
