# TASKS.md

## Current milestone

Prepare and build the free-first DocuLedger MVP.

## Rule for Codex

Only work on one task at a time. Do not jump ahead to later SaaS features.

## Phase 1 tasks: backend foundation

- [ ] Create FastAPI backend scaffold.
- [ ] Add config and environment loading.
- [ ] Add safe logging and error handling.
- [ ] Add document upload endpoint.
- [ ] Add file type, extension, size, and filename validation.
- [ ] Add local temporary storage.
- [ ] Add PDF text/image extraction service.
- [ ] Add Tesseract OCR wrapper.
- [ ] Add OCR metadata and confidence fields.
- [ ] Add invoice Pydantic schemas.
- [ ] Add rule-based extractor.
- [ ] Add extractor provider interface.
- [ ] Add paid LLM extractor stub disabled by default.
- [ ] Add confidence scoring.
- [ ] Add processing pipeline/orchestrator.
- [ ] Add tests for upload, OCR, extraction, and validation.

## Phase 2 tasks: frontend and review

- [ ] Create Next.js frontend scaffold.
- [ ] Add global layout/theme.
- [ ] Add upload component.
- [ ] Add API client.
- [ ] Add upload progress and error states.
- [ ] Add results page.
- [ ] Add confidence badges.
- [ ] Add editable invoice review form.
- [ ] Add document preview area.
- [ ] Add save-reviewed-invoice flow.
- [ ] Add CSV export buttons.
- [ ] Add generic CSV export.
- [ ] Add QuickBooks-compatible CSV export.
- [ ] Add Xero-compatible CSV export.
- [ ] Add dashboard/history page.

## Phase 3 tasks: sellable workflow

- [ ] Add vendor/category rules.
- [ ] Add client-specific mapping.
- [ ] Add duplicate detection.
- [ ] Add anomaly warnings.
- [ ] Add batch processing.
- [ ] Add batch progress.
- [ ] Add PDF summary report.
- [ ] Add multi-currency support.
- [ ] Add E2E tests.
- [ ] Add sample invoice dataset.

## Phase 4 tasks: launch readiness

- [ ] Add deployment instructions.
- [ ] Add demo walkthrough.
- [ ] Add README polish.
- [ ] Add portfolio case study.
- [ ] Add security checklist.
- [ ] Add pricing sheet.
- [ ] Add proposal template.
- [ ] Add cold email templates.
- [ ] Add LinkedIn posts.
- [ ] Add outreach tracker.

## Active task

Start with:

```text
Create the backend FastAPI scaffold and config layer only.
```

