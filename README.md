# Accident Defense Command — Court Artifact Contract (Starter)

This starter repo packages the court-defensible artifact schemas and locked CSV headers for **Accident Defense Command (ADC)**.

## What’s inside
- `/schemas` — JSON Schema files (draft 2020-12) for v1 court artifacts
- `/docs/csv_headers.md` — Locked CSV header definitions (column order is part of the contract)

## Quick start
1. Create a new GitHub repo.
2. Upload the contents of the `adc-court-artifacts` folder (or unzip the archive).
3. In your app/services, validate every generated JSON artifact against the matching schema before writing to storage.

## Why this matters
These artifacts are designed to survive:
- authenticity challenges
- hearsay/business-record disputes
- spoliation arguments
- jury confusion objections

Keep them boring, consistent, and append-only.
