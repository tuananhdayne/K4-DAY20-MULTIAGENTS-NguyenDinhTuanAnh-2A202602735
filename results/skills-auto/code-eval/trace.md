### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: read_file
{"file_path": "skills/code-patch-quality-and-artifacts/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-11 of 11 @@
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

### Tool call: glob
{"pattern": "**/*", "path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-314.pyc', '/workspace/bookings/__pycache__/billing.cpython-314.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-314.pyc', '/workspace/bookings/__pycache__/schedule.cpython-314.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-314.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-314-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "pytest workspace"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_o4l_3ot8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/tmp/lab_sandbox_o4l_3ot8/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~/vinuni/0610/K4-DAY20-MULTIAGENTS-NguyenDinhTuanAnh-2A202602735/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.06s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python3 -m pytest workspace -o pythonpath=workspace"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_o4l_3ot8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py FF.                                     [100%]

=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

~/vinuni/0610/K4-DAY20-MULTIAGENTS-NguyenDinhTuanAnh-2A202602735/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
workspace/bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surround

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 1000}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "limit": 1000}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 1000}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: read_file
{"limit": 1000, "file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 1000}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 1000}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: read_file
{"limit": 1000, "file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: grep
{"pattern": "Acme", "path": "workspace"}

### Tool result
No matches found

### Tool call: glob
{"pattern": "**/*", "path": "skills"}

### Tool result
['/skills/code-patch-quality-and-artifacts/SKILL.md', '/skills/log-parsing-and-schema-contracts/SKILL.md', '/skills/tabular-data-processing-and-export/SKILL.md']

### Tool call: glob
{"pattern": "*"}

### Tool result
['/.pytest_cache/CACHEDIR.TAG', '/.pytest_cache/README.md', '/.pytest_cache/v/cache/lastfailed', '/.pytest_cache/v/cache/nodeids', '/skills/code-patch-quality-and-artifacts/SKILL.md', '/skills/log-parsing-and-schema-contracts/SKILL.md', '/skills/tabular-data-processing-and-export/SKILL.md', '/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-314.pyc', '/workspace/bookings/__pycache__/billing.cpython-314.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-314.pyc', '/workspace/bookings/__pycache__/schedule.cpython-314.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-314.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-314-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: edit_file
{"old_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))", "new_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    s = text.strip()\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", s)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    m = re.fullmatch(r\"(\\d+)h\", s)\n    if m:\n        return int(m.group(1)) * 60\n    m = re.fullmatch(r\"(\\d+)m\", s)\n    if m:\n        return int(m.group(1))\n    m = re.fullmatch(r\"(\\d+):(\\d+)\", s)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    m = re.fullmatch(r\"(\\d+)\", s)\n    if m:\n        return int(m.group(1))\n    raise ValueErro

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)", "new_string": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return math.ceil(minutes / block)\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"new_string": "\"\"\"Schedule helpers.\"\"\"\nfrom typing import List, Optional, Sequence\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Sequence[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: str, slots: Optional[Sequence[str]] = None) -> List[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        return [slot]\n    return list(slots) + [slot]\n", "old_string": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots", "file_path": "workspace/bookings/schedule.py"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: edit_file
{"new_string": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n", "old_string": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute, duration_text):\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)", "file_path": "workspace/bookings/calendar_export.py"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/calendar_export.py'

### Tool call: write_file
{"file_path": "workspace/tests/test_regression.py", "content": "import pytest\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n\ndef test_parse_duration_all_formats():\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n\n\ndef test_parse_duration_whitespace():\n    assert parse_duration(\"  1h30m  \") == 90\n    assert parse_duration(\"  2h  \") == 120\n    assert parse_duration(\"\\t45m\\n\") == 45\n    assert parse_duration(\" 1:30 \") == 90\n    assert parse_duration(\" 45 \") == 45\n\n\ndef test_parse_duration_invalid():\n    with pytest.raises(ValueError):\n        parse_duration(\"invalid\")\n    with pytest.raises(ValueError):\n        parse_duration(\"1h30\")\n    with pytest.raises(ValueError):\n        parse_duration(\"1hour\")\n    with pytest.raises(ValueError):\n        parse_duration(\"\")\n\n\ndef test_billable_blocks_calculation():\n    assert billable_blocks(0) == 0\n    assert billable_blocks(1) == 1\n    assert billable_blocks(15) == 1\n    assert billable_blocks(16) == 2\n    assert billable_blocks(20) == 2\n    assert billable_blocks(45) == 3\n    assert billable_blocks(30, block=10) == 3\n    assert billable_blocks(31, block=10) == 4\n\n\ndef test_bi

### Tool result
Updated file /workspace/tests/test_regression.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_o4l_3ot8/workspace
plugins: anyio-4.15.1, langsmith-0.14.4
collected 12 items

tests/test_bookings.py ...                                               [ 25%]
tests/test_regression.py .........                                       [100%]

============================== 12 passed in 0.02s ==============================

[Command succeeded with exit code 0]

### Tool call: edit_file
{"old_string": "# Changelog\n\n## Unreleased\n\n## 1.4.2\n- initial import", "file_path": "workspace/CHANGELOG.md", "new_string": "# Changelog\n\n## Unreleased\n- `[timeutil]` Fixed `parse_duration` to support formats `\"2h\"`, `\"45m\"`, `\"1:30\"`, and `\"45\"`, ignoring surrounding whitespace.\n- `[billing]` Fixed `billable_blocks` to always round up partial blocks (`math.ceil`) and raise `ValueError` on negative minutes.\n- `[schedule]` Fixed default mutable argument in `add_slot` to return a new list and prevent shared state across calls.\n- `[typing]` Added type annotations across all public functions.\n\n## 1.4.2\n- initial import"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 1000}

### Tool result
@@ lines 1-33 of 33 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text: str) -> int:
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    s = text.strip()
    m = re.fullmatch(r"(\d+)h(\d+)m", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(\d+)h", s)
    if m:
        return int(m.group(1)) * 60
    m = re.fullmatch(r"(\d+)m", s)
    if m:
        return int(m.group(1))
    m = re.fullmatch(r"(\d+):(\d+)", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(\d+)", s)
    if m:
        return int(m.group(1))
    raise ValueError(f"bad duration: {text!r}")


### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 1000}

### Tool result
@@ lines 1-17 of 17 @@
"""Billing rules."""
import math


def billable_blocks(minutes: int, block: int = 15) -> int:
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError("minutes must be >= 0")
    if block <= 0:
        raise ValueError("block must be > 0")
    return math.ceil(minutes / block)


### Tool call: read_file
{"limit": 1000, "file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-20 of 20 @@
"""Schedule helpers."""
from typing import List, Optional, Sequence
from .timeutil import parse_duration


def total_minutes(durations: Sequence[str]) -> int:
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot: str, slots: Optional[Sequence[str]] = None) -> List[str]:
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    if slots is None:
        return [slot]
    return list(slots) + [slot]


### Tool call: read_file
{"limit": 1000, "file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-8 of 8 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute: int, duration_text: str) -> int:
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)


### Tool call: execute
{"command": "cd workspace && python -m pytest -v"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- ~/vinuni/0610/K4-DAY20-MULTIAGENTS-NguyenDinhTuanAnh-2A202602735/.venv/bin/python
cachedir: .pytest_cache
rootdir: /tmp/lab_sandbox_o4l_3ot8/workspace
plugins: anyio-4.15.1, langsmith-0.14.4
collecting ... collected 12 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [  8%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 16%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [ 25%]
tests/test_regression.py::test_parse_duration_all_formats PASSED         [ 33%]
tests/test_regression.py::test_parse_duration_whitespace PASSED          [ 41%]
tests/test_regression.py::test_parse_duration_invalid PASSED             [ 50%]
tests/test_regression.py::test_billable_blocks_calculation PASSED        [ 58%]
tests/test_regression.py::test_billable_blocks_negative PASSED           [ 66%]
tests/test_regression.py::test_add_slot_no_shared_state PASSED           [ 75%]
tests/test_regression.py::test_add_slot_with_existing_list PASSED        [ 83%]
tests/test_regression.py::test_total_minutes PASSED                      [ 91%]
tests/test_regression.py::test_slot_end PASSED                           [100%]

============================== 12 passed in 0.02s ==============================

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "git status --porcelain workspace"}

### Tool result
[stderr] fatal: not a git repository (or any parent up to mount point /)
[stderr] Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

Exit code: 128
[Command failed with exit code 128]

### Assistant
### Summary of Changes

1. **`workspace/bookings/timeutil.py`**:
   - Expanded `parse_duration` to support all documented formats (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, and bare numbers `"45"`), while ignoring leading/trailing whitespace and raising `ValueError` on invalid formats.
   - Added explicit type annotations (`text: str -> int`).

2. **`workspace/bookings/billing.py`**:
   - Fixed `billable_blocks` to always round up partial blocks using `math.ceil` instead of `round`.
   - Added validation to raise `ValueError` when `minutes < 0` (and when `block <= 0`).
   - Added explicit type annotations (`minutes: int, block: int = 15 -> int`).

3. **`workspace/bookings/schedule.py`**:
   - Fixed mutable default argument in `add_slot` (`slots: Optional[Sequence[str]] = None`) so calling the function creates and returns a new list without sharing state across invocations.
   - Added explicit type annotations to `total_minutes` and `add_slot`.

4. **`workspace/bookings/calendar_export.py`**:
   - Added explicit type annotations (`start_minute: int, duration_text: str -> int`).

5. **`workspace/tests/test_regression.py`**:
   - Added a dedicated regression test suite covering all supported duration formats, whitespace handling, invalid duration strings, rounding behavior, negative input errors, and slot state isolation.

6. **`workspace/CHANGELOG.md`**:
   - Documented the bug fixes and enhancements under the `## Unreleased` section.