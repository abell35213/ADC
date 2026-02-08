#!/usr/bin/env python3
"""
Validate ADC example JSON artifacts against JSON Schema files.

Usage:
  python3 scripts/validate.py

Exit codes:
  0 = all validations passed
  1 = one or more validations failed
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples"

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main() -> int:
    if not SCHEMAS_DIR.exists():
        print(f"ERROR: schemas directory not found: {SCHEMAS_DIR}")
        return 1
    if not EXAMPLES_DIR.exists():
        print(f"ERROR: examples directory not found: {EXAMPLES_DIR}")
        return 1

    schema_docs = {}
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        schema_docs[schema_path.name] = load_json(schema_path)

    mapping = {
        "eld_duty_status.json": "eld_duty_status.schema.json",
        "gps_trace.json": "gps_trace.schema.json",
        "safety_events.json": "safety_events.schema.json",
        "vehicle_state.json": "vehicle_state.schema.json",
        "evidence_inventory.json": "evidence_inventory.schema.json",
        "chain_of_custody.json": "chain_of_custody.schema.json",
    }

    failures = 0
    for example_name, schema_name in mapping.items():
        example_path = EXAMPLES_DIR / example_name
        schema = schema_docs.get(schema_name)

        if not example_path.exists():
            print(f"SKIP: missing example: {example_name}")
            continue
        if schema is None:
            print(f"ERROR: missing schema: {schema_name}")
            failures += 1
            continue

        instance = load_json(example_path)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

        if errors:
            failures += 1
            print(f"FAIL: {example_name} against {schema_name}")
            for e in errors[:20]:
                loc = "/".join(str(p) for p in e.absolute_path) or "(root)"
                print(f"  - {loc}: {e.message}")
            if len(errors) > 20:
                print(f"  ... {len(errors)-20} more errors")
        else:
            print(f"PASS: {example_name} against {schema_name}")

    if failures:
        print(f"\nValidation failed: {failures} file(s) invalid.")
        return 1

    print("\nAll validations passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
