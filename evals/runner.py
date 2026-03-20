import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.validate import validate_contract, ValidationError


def run_evals(run_dir: str, eval_file: str) -> dict:
    with open(eval_file) as f:
        eval_set = json.load(f)

    # Load requirements.json as `req` — available in all assertion contexts
    req = {}
    req_path = os.path.join(run_dir, "requirements.json")
    if os.path.exists(req_path):
        try:
            with open(req_path) as f:
                req = json.load(f)
        except json.JSONDecodeError:
            pass

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results = {"passed": [], "failed": [], "skipped": []}

    # Pre-load common files so assertions can cross-reference them
    _common_files = {
        "research_foundation": "research_foundation.json",
        "research_log": "research_log.json",
        "candidate_pool": "candidate_pool.json",
        "scored_products": "scored_products.json",
        "scoring_log": "scoring_log.json",
    }
    _file_context = {}
    for _key, _fname in _common_files.items():
        _fpath = os.path.join(run_dir, _fname)
        if os.path.exists(_fpath):
            try:
                with open(_fpath) as f:
                    _file_context[_key] = json.load(f)
            except json.JSONDecodeError:
                _file_context[_key] = None
        else:
            _file_context[_key] = None

    for test in eval_set["tests"]:
        file_path = os.path.join(run_dir, test["file"])

        if not os.path.exists(file_path):
            if test.get("required"):
                results["failed"].append({
                    "id": test["id"],
                    "name": test["name"],
                    "reason": f"Required file not found: {test['file']}"
                })
            else:
                results["skipped"].append(test["id"])
            continue

        try:
            with open(file_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            results["failed"].append({"id": test["id"], "name": test["name"], "reason": f"Invalid JSON: {e}"})
            continue

        if "schema" in test:
            schema_path = os.path.join(project_root, test["schema"])
            try:
                validate_contract(data, schema_path)
            except ValidationError as e:
                results["failed"].append({"id": test["id"], "name": test["name"], "reason": str(e)})
                continue

        if "assertion" in test:
            try:
                passed = eval(test["assertion"], {"data": data, "req": req, "run_dir": run_dir, "os": os, **_file_context})
                if not passed:
                    results["failed"].append({
                        "id": test["id"],
                        "name": test["name"],
                        "reason": f"Assertion failed: {test['assertion']}"
                    })
                    continue
            except Exception as e:
                results["failed"].append({"id": test["id"], "name": test["name"], "reason": str(e)})
                continue

        results["passed"].append(test["id"])

    return results


def print_results(results: dict) -> None:
    total = len(results["passed"]) + len(results["failed"]) + len(results["skipped"])
    print(f"\n{'='*50}")
    print(f"Results: {len(results['passed'])}/{total} passed")
    print(f"{'='*50}")
    for tid in results["passed"]:
        print(f"  ✓ {tid}")
    for item in results["failed"]:
        print(f"  ✗ {item['id']}: {item['name']}")
        print(f"    {item['reason']}")
    if results["skipped"]:
        print(f"  - Skipped: {', '.join(results['skipped'])}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py <run_dir> [eval_file]")
        print("  run_dir:   path to runs/[timestamp]/ directory")
        print("  eval_file: defaults to evals/contract-evals.json")
        sys.exit(1)

    run_dir = sys.argv[1]
    eval_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(__file__), 'contract-evals.json'
    )

    results = run_evals(run_dir, eval_file)
    print_results(results)
    sys.exit(0 if not results["failed"] else 1)
