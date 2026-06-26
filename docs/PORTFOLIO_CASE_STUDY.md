# DocuLedger Portfolio Case Study

## Problem

Small bookkeepers, CPA firms, ecommerce operators, property managers, and small businesses often receive invoices and receipts as PDFs or images. Manually reading each document and entering vendor, invoice number, date, subtotal, tax, total, and currency is slow and error-prone.

## Target Users

- Small bookkeeping teams
- CPA firms handling client documents
- Ecommerce operators with receipt-heavy workflows
- Property managers processing vendor invoices
- Small businesses that need cleaner invoice intake

## Solution

DocuLedger is a free-first, review-assisted invoice and receipt processing MVP. It lets a user upload a document, create an extraction draft, review and correct the fields, approve the invoice, and export CSV files for common accounting workflows.

The product is intentionally review-assisted. It improves speed, but it does not claim to replace human accounting judgment.

## Core Workflow

```text
upload document -> process text/OCR -> extract invoice draft -> human review -> approved CSV export
```

## Architecture

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, Python, Pydantic
- Storage: local temporary document storage
- OCR: local Tesseract through `pytesseract` and Pillow
- PDF text extraction: free local PDF text extraction
- Extraction: rule-based invoice parser
- Persistence: SQLite for reviewed invoices
- Export: standard-library CSV generation
- Tests: pytest for backend workflow coverage

## AI And Document Processing

The current MVP uses deterministic processing rather than paid AI APIs:

- Text-based PDFs are read directly.
- PNG/JPG/JPEG receipts can be processed with local OCR.
- Rule-based extraction creates a draft invoice.
- Confidence scores and warnings guide the reviewer.

This keeps the MVP private, low-cost, and easy to run locally.

## Human Review Design

Financial data needs accountability. DocuLedger requires review before export so extracted values are treated as drafts. Reviewers can correct fields, add notes, and approve the invoice before CSV generation.

## Free-First Design

The MVP avoids OpenAI, Claude, Google Vision, Stripe, QuickBooks APIs, Xero APIs, paid hosting, and paid storage. Paid providers can be added later behind adapter interfaces, but the first version proves the workflow without requiring them.

## Security And Privacy Notes

- Demo files contain fake data only.
- Uploaded files are treated as sensitive financial documents.
- Full OCR/invoice text is not logged unnecessarily.
- API responses avoid exposing absolute internal storage paths.
- CSV export is blocked until review approval.
- Local `.env`, storage, database, and cache files are ignored.

## Testing And Validation

The backend test suite covers health checks, upload validation, PDF text extraction, OCR behavior, rule-based extraction, processing, review persistence, and CSV export. Frontend validation uses Next.js production build and lint checks.

## Current Limitations

- Not production-ready.
- No authentication or user accounts yet.
- No dashboard or document history.
- No batch upload or batch export.
- No direct QuickBooks or Xero API integration.
- Scanned PDF page conversion is not implemented yet.
- OCR quality depends on local Tesseract setup and image quality.
- Rule-based extraction is imperfect and requires human review.

## Next Steps

- Add authentication and workspace isolation.
- Add document history and audit logs.
- Add retention cleanup for uploaded source files.
- Add scanned PDF page conversion.
- Add batch export.
- Add client-specific CSV mapping.
- Add optional paid AI/OCR adapters behind disabled-by-default feature flags.

## Interview-Ready Explanation

"DocuLedger is a free-first, review-assisted invoice processing MVP. I built a FastAPI backend and Next.js frontend that let a user upload invoices or receipts, process them locally with PDF text extraction or Tesseract OCR, extract draft invoice fields with rule-based logic, review and correct the data, then export approved CSV files. The key design choice is that financial extraction is not treated as fully automatic. Human review is required before export, which makes the workflow safer and more realistic for bookkeeping."
