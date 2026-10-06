---
name: code-patch-quality-and-artifacts
description: Use when fixing bugs, refactoring, or updating functions in a codebase.
---
# Code Patch Quality and Artifacts Checklist

1. Review requirements for mandatory project artifacts (changelog updates, regression test files, documentation).
2. Add explicit type annotations (parameters and return types) to all new and modified public functions (names not starting with `_`).
3. Create a dedicated regression test file with test cases specifically covering each fixed bug or edge case.
4. Update the changelog (e.g., under unreleased section) following the exact requested bullet format and scope tags.
5. Run the full test suite across both existing tests and new regression tests to ensure 100% pass rate.
