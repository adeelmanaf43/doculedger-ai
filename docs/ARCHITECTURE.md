# ARCHITECTURE.md

## Architecture principle

Build local/free mode first, but design adapters so paid providers can be enabled later without rewriting the app.

## Target layers

```text
Frontend
  Upload UI
  Review/correction UI
  Dashboard/history
  Export/report actions

Backend API
  Upload routes
  Processing routes
  Review/save routes
  Export routes
  Report routes
  Health/config routes

Services
  OCR service
  Extraction service
  Categorization service
  Validation service
  Export service
  Report service
  Storage service
  Audit service

Adapters
  Local OCR / Google Vision OCR
  Rule-based extractor / LLM extractor
  SQLite / Postgres
  Local storage / R2/S3
  CSV export / QuickBooks/Xero API
  Manual billing / Stripe
```

## Backend target structure

```text
backend/
  app/
    main.py
    api/
      routes_uploads.py
      routes_processing.py
      routes_reviews.py
      routes_exports.py
      routes_reports.py
      routes_health.py
    core/
      config.py
      logging.py
      security.py
      errors.py
    schemas/
      invoice.py
      extraction.py
      export.py
      report.py
    services/
      ocr/
        base.py
        tesseract_ocr.py
        google_vision_ocr.py
      extractors/
        base.py
        rule_based.py
        llm_extractor.py
      categorization/
        rules.py
        advisor.py
      exporters/
        quickbooks_csv.py
        xero_csv.py
        generic_csv.py
      reports/
        summary_report.py
      storage/
        base.py
        local_storage.py
        object_storage.py
      audit.py
    tests/
```

## Frontend target structure

```text
frontend/
  app/
    page.tsx
    upload/
    review/
    dashboard/
    exports/
  components/
    FileUpload.tsx
    InvoiceReviewForm.tsx
    ConfidenceBadge.tsx
    DocumentPreview.tsx
    ExportActions.tsx
    WarningList.tsx
  lib/
    api.ts
    types.ts
    formatters.ts
```

## Core data objects

### UploadedDocument

- id
- original_filename
- safe_filename
- mime_type
- size_bytes
- storage_path
- status
- created_at
- deleted_at

### ExtractedInvoice

- id
- document_id
- vendor_name
- invoice_number
- invoice_date
- due_date
- subtotal
- tax
- total
- currency
- line_items
- category_suggestion
- confidence_by_field
- warnings
- raw_text_reference

### ReviewedInvoice

- id
- extracted_invoice_id
- reviewed_fields
- corrections
- reviewer_notes
- export_status
- reviewed_at

## Provider strategy

Every paid service must follow this pattern:

1. Define a base interface.
2. Implement free/local provider.
3. Implement paid provider as optional adapter.
4. Select provider through environment variables.
5. Add fallback behavior.
6. Add mocked tests for paid provider.
7. Document cost, data sent, and privacy impact.

## First MVP endpoints

- `GET /health`
- `POST /documents/upload`
- `POST /documents/{document_id}/process`
- `GET /documents/{document_id}/extraction`
- `POST /invoices/{invoice_id}/review`
- `GET /exports/quickbooks.csv`
- `GET /exports/xero.csv`
- `GET /exports/generic.csv`

## Later endpoints

- Batch processing
- PDF summary report
- Client workspace
- Accounting API sync
- Billing
- Intake integrations

