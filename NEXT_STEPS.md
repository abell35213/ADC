# Next Steps — ADC Web App

This document defines the roadmap for turning the current court-artifact contract repository into a working web application.

## Repository Inventory

| Area | Contents |
|------|----------|
| `/schemas` | 6 JSON Schema (draft 2020-12) files defining the v1 court-artifact contract |
| `/examples` | Sample JSON and CSV artifacts for each schema |
| `/docs` | Locked CSV header definitions (column order is part of the contract) |
| `/scripts` | `validate.py` — validates example JSON against schemas |
| `requirements.txt` | Python dependency: `jsonschema>=4.19.0` |

### Artifact Types Defined

1. **ELD Duty Status** — driver hours-of-service duty events from Samsara ELD
2. **GPS Trace** — timestamped lat/lon breadcrumbs from Samsara GPS
3. **Safety Events** — hard brakes, harsh acceleration, speeding, collisions from Samsara
4. **Vehicle State** — periodic snapshots of odometer, engine hours, fuel, RPM, speed, DTC codes
5. **Evidence Inventory** — manifest of all evidence items and their capture status
6. **Chain of Custody** — append-only log of every action taken on every artifact

### Common Envelope (all artifacts)

Every JSON artifact shares: `schema_version`, `generated_at_utc`, `incident_id`, `carrier_id`, `vehicle`, `capture_window`, `source_system`, `artifacts`, and `data`.

---

## Phase 1 — Project Scaffolding & Core Data Layer

- [ ] **Choose tech stack**: Select web framework (e.g., Next.js, FastAPI + React, Django) and database (e.g., PostgreSQL)
- [ ] **Initialize project**: Scaffold the web app with chosen framework, add linter/formatter configuration
- [ ] **Define data models**: Translate the 6 JSON schemas into database models/tables, preserving all field types and constraints
- [ ] **Implement JSON Schema validation middleware**: Integrate the existing `jsonschema` validation so every incoming artifact is validated against its schema before storage
- [ ] **Set up CI/CD**: Add GitHub Actions workflows for lint, test, build, and deploy

## Phase 2 — Artifact Ingestion & Storage

- [ ] **Build artifact ingestion API**: Create REST endpoints to accept JSON artifacts (one per schema type)
- [ ] **Implement append-only storage**: Artifacts must be immutable once written (court requirement)
- [ ] **SHA-256 integrity hashing**: Compute and store hashes on ingestion for evidence inventory items
- [ ] **CSV export**: Generate CSV files with locked headers matching `docs/csv_headers.md` column order
- [ ] **Capture-failure handling**: Emit `capture-failed` events and create `unavailable` evidence inventory entries when ingestion fails (no silent gaps)

## Phase 3 — Incident Management UI

- [ ] **Incident list view**: Dashboard showing all incidents with carrier, vehicle, and timestamp info
- [ ] **Incident detail view**: Display all artifacts for a given incident, organized by type
- [ ] **Evidence inventory viewer**: Show capture status of every evidence type with unavailable reason codes
- [ ] **Chain of custody timeline**: Render the append-only custody log as a chronological timeline
- [ ] **GPS trace map**: Plot GPS breadcrumbs on an interactive map (e.g., Leaflet / Mapbox)
- [ ] **ELD duty status chart**: Visualize driver duty events on a timeline (OFF_DUTY, SLEEPER, DRIVING, etc.)
- [ ] **Safety events overlay**: Display safety events (hard brakes, speeding, collisions) on the GPS map and timeline

## Phase 4 — Court Package Export

- [ ] **Court package generator**: Bundle all artifacts for an incident into a downloadable ZIP file
- [ ] **PDF summary report**: Auto-generate a court-ready summary document with key facts
- [ ] **Integrity verification**: Include SHA-256 manifest in the export so recipients can verify artifact integrity
- [ ] **Chain of custody record**: Automatically log `export_generated` and `export_downloaded` custody entries

## Phase 5 — Authentication, Authorization & Audit

- [ ] **User authentication**: Add login/signup with role-based access (safety_manager, driver, counsel, insurer)
- [ ] **Role-based permissions**: Restrict access to artifacts based on `actor_type` from the chain-of-custody schema
- [ ] **Audit logging**: Log every artifact access as a chain-of-custody entry (`accessed`, `downloaded`)
- [ ] **API key management**: Support integration accounts (e.g., `samsara-adapter`) for automated ingestion

## Phase 6 — Samsara Integration

- [ ] **Samsara API client**: Build an adapter to pull ELD, GPS, safety, and vehicle data from the Samsara API
- [ ] **Automated capture**: On incident creation, automatically trigger data capture from Samsara for the configured time window
- [ ] **Webhook listener**: Accept Samsara webhooks for real-time safety event ingestion
- [ ] **Vehicle mapping**: Map `adc_vehicle_id` ↔ `samsara_vehicle_id` in the application

## Phase 7 — Testing & Validation

- [ ] **Unit tests**: Validate all data models against the JSON schemas
- [ ] **Integration tests**: Test the full ingestion → storage → export pipeline
- [ ] **Schema contract tests**: Ensure the app rejects artifacts that violate the schema (invalid enums, missing required fields, wrong types)
- [ ] **CSV header contract tests**: Verify exported CSV files match the locked column order from `docs/csv_headers.md`
- [ ] **Use existing examples**: Seed tests with the JSON/CSV files from `/examples`

## Key Constraints (from repository contracts)

These rules are non-negotiable and must be enforced by the web app:

1. **Schema version** `"1.0"` is required in every artifact
2. **Timestamps** must be RFC 3339 `date-time` in UTC (e.g., `2026-02-08T08:21:00Z`)
3. **No free-form narrative** except `unavailable_reason_detail` and `detail` in custody entries (max 240 chars)
4. **CSV column order is locked** — never reorder columns in exported CSVs
5. **Backward-compatible changes only** — may add optional fields or new enum values, but never remove fields, change types, or reorder CSV columns
6. **Append-only** — artifacts are immutable once stored
7. **Fail loudly** — if validation or capture fails, create unavailable inventory entries (no silent gaps)
