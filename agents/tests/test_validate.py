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
