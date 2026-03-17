import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.validate import validate_contract, ValidationError


def run_evals(run_dir: str, eval_file: str) -> dict:
    with open(eval_file) as f:
        eval_set = json.load(f)

    results = {"passed": [], "failed": [], "skipped": []}

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

        with open(file_path) as f:
            data = json.load(f)

        if "schema" in test:
            schema_path = os.path.join(os.path.dirname(eval_file), '..', test["schema"])
            try:
                validate_contract(data, schema_path)
            except ValidationError as e:
                results["failed"].append({"id": test["id"], "name": test["name"], "reason": str(e)})
                continue

        if "assertion" in test:
            try:
                passed = eval(test["assertion"], {"data": data})
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
