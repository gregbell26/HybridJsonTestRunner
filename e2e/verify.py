import json
import sys
import os

assert os.path.exists(sys.argv[1]), "File does NOT exist!"

with open(sys.argv[1], "r") as r:
    results = json.load(r)

assert results, "Results are empty!"

assert "score" in results, "Results have no score!"
assert results["score"] == 2, "Score was not 2!"

assert "tests" in results
assert len(results["tests"]) == 3, "Expected 3 tests to run!"

# grab test with number 2.0

test = None

for t in results["tests"]:
    if "number" in t and t["number"] == "2.0":
        test = t
        break

assert test is not None, "Failed to locate Test #: 2.0"

assert "name" in test
assert test["name"] == "test_set_output_html", "Invalid name"
assert "output_format" in test
assert test["output_format"] == "html", "Should be HTML"

assert "<p>" in test["output"], "Missing HTML start tag"
assert "</p>" in test["output"], "Missing HTML end tag"
assert "Huzzah!" in test["output"], "Missing HTML content"


