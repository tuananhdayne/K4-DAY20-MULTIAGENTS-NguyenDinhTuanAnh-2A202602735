---
name: tabular-data-processing-and-export
description: Use when cleaning, transforming, or aggregating tabular datasets to produce analysis reports and cleaned exports.
---
# Tabular Data Processing and Export Checklist

1. Identify all required output deliverables (summary JSON, cleaned CSV, intermediate reports) and their target paths.
2. Verify value unit conventions (e.g., integer cents vs. floating point currency, ISO-8601 UTC timestamps with trailing `Z`).
3. Standardize categorical fields into canonical casing and formatting (e.g., trimming whitespace, title-casing region names).
4. Handle sentinel values and missing values explicitly as specified by the task criteria.
5. Include required metadata blocks (e.g., source file name, raw row count, processed/valid row count) in the final JSON output.
6. Verify output CSV files have exact expected column headers and row counts matching deduplicated valid records.
