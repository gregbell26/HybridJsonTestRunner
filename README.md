# Hybrid JSON Test Runner

> A replacement for Gradescope's autograder-utils package


### Why?

Gradescope's autograder-utils package has been largely unmaintained since 2022, which is problematic as many features
have been added to the autograder platform since then. AND there exists well know breaking bugs with their implementation

This package aims to address those concerns by supporting the most recent iteration of the autograder (last update 10-2-23)
while also adding support for other platforms (Like PrairieLearn) that also use similar JSON output formats.

### How?

This package operates very similarly to the existing autograder-utils package.

The main difference is that this implements the PR proposed [here](https://github.com/gradescope/gradescope-utils/pull/38), updates decorator syntax, and adds supports for images via the decorators.

Additionally, it uses the newer `pyproject.toml` config for running as opposed to the legacy `setup.py` that the old Gradescope package.

Example usages are coming, but for now, refer to the _mostly_ working unit tests.

Expect breaking changes as I finalize how the API should be updated.
