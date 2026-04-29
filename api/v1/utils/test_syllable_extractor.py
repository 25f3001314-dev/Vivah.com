"""Simple unit-style tests for the Devanagari syllable extractor.

Run with:
    python -m api.v1.utils.test_syllable_extractor

These are lightweight assertions to demonstrate expected behavior.
"""

import os
import sys

# Ensure project package is importable when running this file directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.v1.utils import extract_first_syllable


def run_tests():
    cases = {
        "विराट": "वि",
        "काव्या": "का",
        "श्रेया": "श्रे",
        "ध्रुव": "ध्रु",
        "चैतन्य": "चै",
        "प्रिया": "प्रि",
    }

    failed = []
    for name, expected in cases.items():
        try:
            got = extract_first_syllable(name)
        except Exception as e:
            failed.append((name, expected, f"RAISED {e}"))
            continue
        if got != expected:
            failed.append((name, expected, got))

    if not failed:
        print("All tests passed")
        return 0

    print("Failures:")
    for name, expected, got in failed:
        print(f"  {name}: expected={expected!r} got={got!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(run_tests())
