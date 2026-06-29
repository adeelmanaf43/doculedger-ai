# DocuLedger Portfolio Case Study

## Project Overview

DocuLedger is a free-first, review-assisted invoice and receipt processing MVP. It turns uploaded PDFs/images into draft invoice data, routes that data through human review, and exports approved CSV files for bookkeeping workflows.

This is a portfolio MVP, not production accounting software.

## Problem

Bookkeepers and small operators often spend hours manually reading invoices, typing vendor/date/tax/total fields, correcting OCR mistakes, and preparing CSV files for accounting tools. The work is repetitive, but financial data still needs accountability.

## Target Users

- Small bookkeeping firms
- Independent bookkeepers
- Small CPA/accounting practices
- Ecommerce operators
- Property and construction businesses handling supplier invoices

## What I Built

- FastAPI backend with upload, processing, review, status, and export endpoints.
- Secure local upload validation for PDF, PNG, JPG, and JPEG files.
- PDF text extraction for text-based PDFs.
- Local Tesseract OCR for image receipts.
- Rule-based invoice field extraction with confidence scores and warnings.
- Human review and correction workflow.
- SQLite persistence for reviewed invoices.
- CSV export for Generic, QuickBooks-style, and Xero-style templates.
- Next.js frontend for upload, process, review, approve, and export.
- Fake demo data, QA docs, demo workflow, and portfolio documentation.

## MVP Workflow

```text
Upload invoice/receipt -> process with PDF text extraction or OCR -> extract invoice fields -> review/correct fields -> approve invoice -> export Generic/QuickBooks/Xero-style CSV
```

## Why Review-Assisted Design

Invoice extraction can be uncertain. OCR may misread text, layouts vary, and rule-based extraction can miss edge cases. Because the domain is bookkeeping, DocuLedger treats extracted fields as drafts and requires human approval before export.

The product goal is faster review and cleaner CSV preparation, not fully automatic accounting.

## System Architecture

```text
Next.js frontend
  -> FastAPI backend
    -> local storage
    -> PDF text extraction or Tesseract OCR
    -> rule-based invoice extraction
    -> SQLite reviewed invoice persistence
    -> CSV export
```

## Backend Responsibilities

- Validate upload type, size, and filename safety.
- Store uploaded documents locally.
- Resolve stored documents by document ID.
- Extract text from PDFs or images where supported.
- Run rule-based invoice extraction.
- Return confidence scores and warnings.
- Save human-reviewed invoices in SQLite.
- Enforce reviewed-only CSV export.
- Avoid exposing absolute internal paths.

## Frontend Responsibilities

- Provide a simple upload/process/review/export workflow.
- Call the backend API through a typed API client.
- Show backend connection status.
- Display extracted fields, confidence, warnings, and errors.
- Let a reviewer correct and approve invoice fields.
- Enable export buttons only after approval.

## AI And Document Processing Components

The MVP uses practical local document processing:

- Text-based PDF extraction for embedded PDF text.
- Tesseract OCR through `pytesseract` and Pillow for PNG/JPG/JPEG images.
- Rule-based invoice extraction for vendor, invoice number, dates, subtotal, tax, total, currency, email, phone, and line-item drafts where possible.

No paid OCR or LLM provider is required in the MVP.

## OCR And Extraction Strategy

The first version favors predictable, low-cost processing over maximum extraction accuracy. Rule-based extraction is easier to test, explain, and run locally. Paid LLM/OCR providers can be added later behind adapters, but they should remain optional and disabled by default.

## Review And Correction Workflow

The review workflow stores the corrected invoice JSON, reviewer notes, approval status, corrected fields, and timestamps. If approved, export is allowed. If not approved, the invoice remains `review_required`.

## CSV Export Workflow

CSV export uses reviewed invoice data as the source of truth. The backend supports:

- Generic CSV
- QuickBooks-style CSV template
- Xero-style CSV template

These are CSV templates, not official QuickBooks or Xero API integrations. Client-specific mapping may be needed later.

## Security And Privacy Considerations

- Demo files are fake.
- Real invoices should be treated as sensitive financial documents.
- `.env`, local database files, storage folders, and cache folders should not be committed.
- Full OCR/invoice text should not be logged in production.
- API responses avoid absolute internal paths.
- CSV export requires human approval.

## Testing And Validation

The backend test suite covers health checks, upload validation, PDF text extraction, OCR behavior, rule-based extraction, processing, review persistence, and CSV export. Frontend validation uses Next.js production build and lint checks.

Manual QA is documented in:

```text
docs/MVP_QA_CHECKLIST.md
```

## Business Value

DocuLedger targets a narrow but practical workflow: reducing manual invoice entry while keeping review control. For a small bookkeeping team, the value is less typing, clearer review, and faster CSV preparation.

## Why I Built It This Way

- FastAPI first: backend workflow could be tested before UI.
- Local storage first: simple and free for an MVP.
- SQLite first: enough persistence for reviewed invoices without database overengineering.
- Rule-based extraction first: explainable, testable, and free.
- Human review first: safer for financial data.
- CSV export first: useful before direct accounting integrations.

## Technical Decisions And Tradeoffs

- Tesseract is free/local, but OCR quality depends on image quality and installation.
- Rule-based extraction is transparent, but less flexible than LLM extraction.
- SQLite is simple, but not enough for multi-tenant production usage.
- Local storage is easy to demo, but object storage and retention policies are needed later.
- CSV templates are practical, but client-specific accounting mappings may be required.

## Limitations

- Not production-ready.
- No authentication.
- No multi-tenant workspaces.
- No dashboard/history.
- No batch processing.
- No direct QuickBooks/Xero API sync.
- Scanned PDF support is limited because PDF page-to-image conversion is not implemented yet.
- OCR accuracy depends on document quality.
- Rule-based extraction is imperfect.
- Human review is required.

## Future Roadmap

- Dashboard/history
- Batch upload/export
- Better scanned PDF handling
- Client-specific export mappings
- Auth and workspaces
- Cloud storage
- Optional paid OCR/LLM adapters
- Direct QuickBooks/Xero APIs
- Deployment hardening

## What I Would Improve Next

I would add a document history dashboard, audit logs, better scanned PDF handling, and client-specific CSV mappings. After that, I would add authentication/workspaces and optional paid OCR/LLM adapters behind feature flags.

## How This Maps To Applied AI Engineer Work

DocuLedger demonstrates:

- Translating a business workflow into an AI-assisted product.
- Designing human-in-the-loop review for uncertain model/OCR output.
- Building backend APIs around document processing.
- Handling file upload safety and sensitive data concerns.
- Connecting OCR, extraction rules, confidence, warnings, review, and export.
- Communicating product limitations honestly.

## Interview-Ready Summary

"DocuLedger is a free-first, review-assisted invoice processing MVP. I built a FastAPI backend and Next.js frontend that let a user upload invoices or receipts, process them locally with PDF text extraction or Tesseract OCR, extract draft invoice fields with rule-based logic, review and correct the data, then export approved CSV files. The key design choice is that financial extraction is not treated as fully automatic. Human review is required before export, which makes the workflow safer and more realistic for bookkeeping."
