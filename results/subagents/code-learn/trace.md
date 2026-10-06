### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: task
{"description": "Please explore the workspace/ folder.\nCheck:\n1. What files are in workspace/ (package structure, tests, setup/pyproject/etc., any style guides or Acme convention files or linting configs).\n2. Run pytest in workspace/ to see current test failures and output.\n3. Check for any linters/formatters/conventions (flake8, ruff, black, mypy, pylint, Acme guidelines, etc.) configured in workspace/.\n4. Inspect all docstrings and implementations in the inventory package and test files in tests/.\nReport your findings in detail without modifying any files.", "subagent_type": "explorer"}

### Tool result
Here is the detailed exploration report for `workspace/`:

---

### 1. Package Structure & Files in `workspace/`

- **Root files**:
  - `workspace/README.md`: Instructions to run tests (`cd workspace && python -m pytest tests -q`).
  - `workspace/CHANGELOG.md`: Lists unreleased and version 0.3.1 history.
- **Package directory (`workspace/inventory/`)**:
  - `workspace/inventory/__init__.py`: Empty module file.
  - `workspace/inventory/pricing.py`: Price parsing (`parse_price`) and discount calculation (`apply_discount`).
  - `workspace/inventory/report.py`: Inventory reports (`total_value`, `low_stock`).
  - `workspace/inventory/export.py`: Export utility (`to_csv_row`).
- **Tests directory (`workspace/tests/`)**:
  - `workspace/tests/test_report.py`: Contains 6 unit tests covering the inventory modules.
- **Setup / Config files**:
  - There are **no** `pyproject.toml`, `setup.py`, `setup.cfg`, `tox.ini`, `.flake8`, `.ruff.toml`, or other configuration files present.

---

### 2. Pytest Results

Running `pytest` inside `workspace/` collected 6 items: **4 passed, 2 failed**.

#### Failures:
1. **`test_total_value_thousands_separator`**:
   - **Error**: `decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]`
   - **Location**: `inventory/pricing.py:15` inside `parse_price` called from `report.py:14`.
   - **Cause**: Input `"$1,299.50"` has commas (`','`) and possibly accounting parentheses not handled by `parse_price` (`cleaned = text.strip().replace("$", "")`). Passin

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py"}

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents