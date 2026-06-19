# PROJECT_BRIEF.md

## Product name

DocuLedger

## One-line pitch

DocuLedger turns messy invoices, receipts, and supplier documents into reviewed bookkeeping-ready data, clean CSV exports, and client-ready summaries.

## Target users

- Small bookkeeping firms with 1–5 employees.
- Independent bookkeepers managing 10–50 small business clients.
- Small CPA/accounting practices.
- Ecommerce businesses handling supplier invoices.
- Property management and construction companies with recurring vendor invoices.
- Freelance CFO/controller consultants serving multiple clients.

## Core pain

Bookkeepers waste hours opening PDFs, reading invoice fields, typing vendor/date/invoice/amount data into accounting workflows, categorizing expenses, checking duplicates, and correcting OCR mistakes.

If a bookkeeper bills $40–$75/hour and saves even 10–15 hours/month, a $300–$800/month review-assisted processing workflow has clear ROI.

## Product positioning

DocuLedger is review-assisted invoice processing, not fully automatic bookkeeping.

The product should promise:

- Faster processing.
- Cleaner CSV export.
- Human review before final use.
- Confidence scoring.
- Auditability.
- Safer handling of financial documents.

The product should not promise:

- 100% extraction accuracy.
- Fully autonomous bookkeeping.
- Automatic tax/accounting correctness.
- Direct accounting sync in the first MVP.

## First sellable offer

Offer:

> Send 20 sample invoices. I will process them free and return a clean CSV, summary report, review notes, and estimated time saved.

Potential pricing after trial:

- Backlog batch: $200–$800/batch or $5–$15/document.
- Setup fee: $200–$500 for custom mappings and rules.
- Monthly retainer: $300–$800/month for 100–500 invoices/month.
- Later SaaS: $49–$149/user/month after the workflow is stable.

## MVP workflow

1. User uploads invoice PDFs/images.
2. Backend validates file type, size, and safety.
3. OCR extracts text using free/local tools.
4. Rule-based extraction identifies invoice fields.
5. Confidence scores and warnings are generated.
6. User reviews and corrects fields.
7. System saves reviewed result.
8. User exports QuickBooks/Xero/Excel-compatible CSV.
9. System produces a summary report.

## MVP success criteria

- Runs locally without paid APIs.
- Processes at least 10 sample invoices.
- Extracts core fields into a structured schema.
- Marks low-confidence fields clearly.
- Allows human correction before export.
- Exports CSV in accounting-friendly format.
- Provides basic history and summary.
- Has tests for OCR pipeline, extraction, export, validation, and API endpoints.

