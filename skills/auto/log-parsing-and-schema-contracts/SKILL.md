---
name: log-parsing-and-schema-contracts
description: Use when parsing logs or semi-structured records into structured JSON or data payloads.
---
# Log Parsing and Schema Contracts Checklist

1. Verify the top-level schema contract, including required metadata headers (e.g., schema versions, generator tags).
2. Apply string normalization rules to entity identifiers (e.g., converting kebab-case to snake_case, lowercasing service names).
3. Normalize all timestamps into standard UTC ISO-8601 strings (`YYYY-MM-DDTHH:MM:SSZ`).
4. Handle multiline entries (e.g., stack traces, repeated message counters) and map them to their corresponding parent event.
5. Sort output lists strictly by the specified primary and secondary sort keys (e.g., service name ascending, then timestamp ascending).
6. Validate the final output structure and data types against all schema requirements before finishing.
