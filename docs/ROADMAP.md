# ROADMAP.md

## Build schedule

Recommended build plan: 6 days/week × 5 hours/day × 4 weeks = 24 workdays and 120 focused hours.

The first 24 days should create a sellable free-first MVP. Paid API upgrades come only after client validation.

## Phase 1: Backend OCR and extraction pipeline

Goal: backend scaffold with working upload, validation, OCR, extraction, and tests.

Deliverables:

- FastAPI app scaffold.
- Safe config module.
- Local file upload validation.
- PDF/image processing.
- Tesseract OCR wrapper.
- Rule-based invoice field extractor.
- Confidence scores.
- Basic processing pipeline.
- Unit and integration tests.
- README setup instructions.

Suggested commit:

```text
feat: add backend OCR extraction pipeline
```

## Phase 2: Frontend review UI and CSV export

Goal: user can upload, review, correct, and export invoice data.

Deliverables:

- Next.js frontend scaffold.
- Upload UI.
- Processing progress UI.
- Results/review screen.
- Confidence badges.
- Editable invoice fields.
- CSV export buttons.
- History/dashboard page.
- Basic protected/private access approach.

Suggested commit:

```text
feat: add invoice review UI and CSV exports
```

## Phase 3: Categorization, reporting, batch processing, validation

Goal: product becomes useful for a real trial with bookkeepers.

Deliverables:

- Vendor/category rule engine.
- Client-specific mapping support.
- Duplicate checks.
- Anomaly warnings.
- Batch processing queue.
- Multi-currency formatting.
- PDF summary report.
- E2E testing and edge-case handling.

Suggested commit:

```text
feat: add batch processing and bookkeeping summary reports
```

## Phase 4: Demo, hardening, and launch materials

Goal: product is ready for outreach and free trials.

Deliverables:

- Local and demo deployment instructions.
- Demo dataset and walkthrough.
- Portfolio case study.
- Demo screenshots/video script.
- Pricing sheet.
- Proposal template.
- Cold email and LinkedIn scripts.
- Security checklist.
- Outreach tracker.

Suggested commit:

```text
chore: prepare demo and client launch materials
```

## Paid upgrade roadmap

Do not start until the free-first MVP can process real sample invoices, export reviewed CSV, and support a free trial.

Paid upgrades:

1. LLM extraction adapter.
2. Google Vision OCR fallback.
3. Production Postgres/Supabase data layer.
4. R2/S3 object storage.
5. Client upload portal.
6. QuickBooks/Xero direct sync.
7. Stripe Billing.
8. Email/Dropbox/Google Drive intake.
9. Learning from corrections.

