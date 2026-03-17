import json
import jsonschema


class ValidationError(Exception):
    pass


def validate_contract(data: dict, schema_path: str) -> None:
    """Validate data against a JSON schema file. Raises ValidationError on failure."""
    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"Contract validation failed: {e.message}") from e


def validate_file(json_path: str, schema_path: str) -> None:
    """Load a JSON file and validate it against a schema."""
    with open(json_path) as f:
        data = json.load(f)
    validate_contract(data, schema_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python validate.py <json_file> <schema_file>")
        sys.exit(1)
    try:
        validate_file(sys.argv[1], sys.argv[2])
        print(f"✓ {sys.argv[1]} is valid")
    except FileNotFoundError as e:
        print(f"✗ File not found: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        sys.exit(1)
    except ValidationError as e:
        print(f"✗ {e}")
        sys.exit(1)
