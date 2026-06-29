# DocuLedger Demo Video Script

## Video Title

DocuLedger MVP Demo: Review-Assisted Invoice Processing To CSV

## Target Audience

Recruiters, founders, small bookkeeping operators, and technical interviewers reviewing an Applied AI Engineer portfolio project.

## Recording Checklist

- [ ] Backend running locally.
- [ ] Frontend running locally.
- [ ] Browser zoom set to a readable level.
- [ ] Use only fake demo files.
- [ ] Close private tabs, terminals with secrets, and notifications.
- [ ] Prepare `demo/sample_invoices/abc_supplies_invoice.pdf`.
- [ ] Prepare a text editor or spreadsheet for the exported CSV.

## What Not To Show

- Real invoices or receipts.
- `.env` files.
- API keys, secrets, tokens, or credentials.
- Internal absolute storage paths.
- Personal browser data.

## Timeline And Script

### 0:00-0:20 - Problem And Product Intro

Show: frontend home/upload screen.

Say:
"This is DocuLedger, a free-first, review-assisted invoice and receipt processing MVP. The problem is that small bookkeeping teams often spend hours reading invoices, typing fields like vendor, date, tax, and total, then cleaning that data for accounting workflows."

### 0:20-0:45 - Upload Invoice

Show: upload panel and select `abc_supplies_invoice.pdf`.

Say:
"I start by uploading a fake sample invoice. The backend validates the file type and size, stores it locally, and returns a document ID. The frontend is only orchestrating the workflow; the backend owns validation and processing."

### 0:45-1:15 - Process Document

Show: processing result with extraction method, confidence, warnings, and draft fields.

Say:
"Next I process the document. For text-based PDFs, the backend extracts embedded text. For image receipts, it can use local Tesseract OCR. Then a rule-based extractor creates draft invoice fields with confidence scores and warnings."

### 1:15-1:50 - Review And Approve

Show: review form and edit a small field or add reviewer notes.

Say:
"This is intentionally review-assisted. Financial data should not be treated as fully automatic. A human reviewer checks the extracted fields, corrects anything needed, adds notes, and approves the invoice before export."

### 1:50-2:20 - Export CSV

Show: enabled export buttons and downloaded CSV.

Say:
"After approval, CSV export unlocks. The MVP supports Generic CSV plus QuickBooks-style and Xero-style CSV templates. These are CSV templates, not official QuickBooks or Xero API integrations."

### 2:20-2:45 - Architecture And Tech Stack

Show: README architecture section or backend Swagger docs.

Say:
"Technically, this uses a Next.js and TypeScript frontend with a FastAPI backend. The backend handles upload, processing, review persistence with SQLite, and CSV export. The system is free-first, so it uses local OCR and rule-based extraction instead of paid AI services."

### 2:45-3:00 - Limitations And Next Steps

Show: README limitations section.

Say:
"The current MVP is not production-ready. It has no auth, no batch processing, and scanned PDF support is limited. The next steps would be dashboard history, better scanned PDF handling, client-specific export mappings, and optional paid OCR or LLM adapters behind feature flags."

## Ending Call-To-Action

"I built DocuLedger to demonstrate practical AI product engineering: document processing, human-in-the-loop design, backend API design, frontend integration, and honest handling of AI limitations. I would welcome feedback from bookkeeping operators, founders, and engineering teams."
