# DocuLedger

DocuLedger is a free-first, review-assisted invoice and receipt processing MVP that turns uploaded documents into human-reviewed bookkeeping-ready CSV exports.

## Problem

Bookkeepers and small operators often spend hours reading invoice PDFs or receipt images, typing vendor/date/tax/total fields, correcting OCR mistakes, and preparing data for accounting tools. DocuLedger speeds up that workflow while keeping a human reviewer in control before anything is exported.

## Target Users

- Small bookkeeping firms
- Independent bookkeepers
- Small CPA and accounting practices
- Ecommerce operators processing receipts
- Property and construction businesses handling supplier invoices

## What The MVP Does

- Accepts PDF, PNG, JPG, and JPEG invoices or receipts.
- Validates uploads and stores them locally.
- Extracts text from text-based PDFs.
- Runs local Tesseract OCR for image uploads.
- Extracts draft invoice fields with rule-based logic.
- Shows confidence scores and warnings.
- Lets a human reviewer correct and approve fields.
- Exports reviewed invoices as Generic, QuickBooks-style, or Xero-style CSV.

DocuLedger is not autonomous bookkeeping. Extracted values are treated as drafts until reviewed and approved.

## End-To-End Workflow

```text
Upload invoice/receipt -> process with PDF text extraction or OCR -> extract invoice fields -> review/correct fields -> approve invoice -> export Generic/QuickBooks/Xero-style CSV
```

## Demo Status

The local MVP is demo-ready for a single-document workflow:

- Backend API workflow is implemented and tested.
- Frontend upload/review/export workflow is implemented.
- Fake demo invoices and expected CSV examples are included under `demo/`.
- Demo instructions are available in `docs/DEMO_WORKFLOW.md`.

## Screenshots

Screenshots have not been captured yet. The planned README screenshots are:

- Upload screen
- Uploaded document success state
- Processing result with confidence/warnings
- Review form with editable fields
- Export CSV buttons
- CSV output example

Manual capture instructions are in `docs/SCREENSHOT_GUIDE.md`.

## Tech Stack

### Backend

- FastAPI
- Python
- Pydantic
- Local PDF text extraction
- Tesseract OCR through `pytesseract` and Pillow
- SQLite
- pytest

### Frontend

- Next.js
- TypeScript
- TailwindCSS
- Native `fetch` API

### Exports

- Python `csv` module
- Generic CSV
- QuickBooks-style CSV template
- Xero-style CSV template

## Architecture Overview

```text
Next.js frontend
  -> FastAPI backend
    -> secure upload validation
    -> local document storage
    -> PDF text extraction or Tesseract OCR
    -> rule-based invoice extraction
    -> SQLite reviewed invoice persistence
    -> CSV export
```

The frontend communicates with the FastAPI backend. The backend owns upload validation, processing, extraction, human review persistence, and CSV export. SQLite stores reviewed invoice data. Paid providers are intentionally not required in the MVP.

## Features Completed

- FastAPI backend scaffold
- Config and environment defaults
- Health endpoint
- Secure upload endpoint
- Local temporary storage
- PDF text extraction for text-based PDFs
- Tesseract OCR for PNG/JPG/JPEG images
- Rule-based invoice field extraction
- Processing pipeline
- Human review and correction workflow
- SQLite persistence for reviewed invoices
- Reviewed-only CSV export
- Next.js frontend MVP
- Demo files and expected CSV outputs
- Backend pytest coverage
- Portfolio/demo documentation

## Run Locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Health check:

```text
http://localhost:8000/health
```

### Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open:

```text
http://localhost:3000
```

If the backend runs on another port, update `frontend/.env.local`:

```text
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://127.0.0.1:8001
```

## Demo Workflow

Use the safe sample invoice:

```text
demo/sample_invoices/abc_supplies_invoice.pdf
```

Then follow:

```text
docs/DEMO_WORKFLOW.md
```

Expected CSV examples are in:

```text
demo/expected_outputs/
```

## API Overview

- `GET /health`
- `POST /documents/upload`
- `POST /documents/{document_id}/extract-text`
- `POST /documents/{document_id}/ocr`
- `POST /documents/{document_id}/process`
- `POST /documents/{document_id}/review`
- `GET /documents/{document_id}/review`
- `GET /documents/{document_id}/status`
- `GET /documents/{document_id}/export?format=generic`
- `GET /documents/{document_id}/export?format=quickbooks`
- `GET /documents/{document_id}/export?format=xero`

## Testing And Validation

Backend:

```powershell
cd backend
python -m pytest
```

Frontend:

```powershell
cd frontend
npm run build
npm run lint
```

Manual QA checklist:

```text
docs/MVP_QA_CHECKLIST.md
```

## Security And Privacy Notes

- Demo files use fake data only.
- Do not commit real invoices, `.env` files, API keys, credentials, or client financial data.
- Uploaded source files are sensitive financial documents.
- API responses avoid exposing absolute internal file paths.
- CSV export is blocked until human review approval.
- Full OCR/invoice text should not be logged in production.
- Paid OCR/LLM providers are not enabled in the MVP.

## Limitations

- Not production-ready.
- No authentication.
- No multi-tenant workspaces.
- No dashboard/history view.
- No batch upload or batch export.
- No direct QuickBooks/Xero API sync.
- QuickBooks/Xero CSV templates may need client-specific mapping.
- Scanned PDF support is limited because PDF page-to-image conversion is not implemented yet.
- OCR accuracy depends on document quality and local Tesseract setup.
- Rule-based extraction is imperfect.
- Human review is required.
- No paid LLM/OCR integrations are included in the MVP.

## Roadmap

- Dashboard and document history
- Batch upload/export
- Better scanned PDF handling
- Client-specific export mappings
- Authentication and workspaces
- Cloud storage
- Optional paid OCR/LLM adapters behind feature flags
- Direct QuickBooks/Xero APIs
- Deployment hardening

## Portfolio And Interview Highlights

This project demonstrates:

- AI product thinking for a real document workflow
- Human-in-the-loop design for financial accuracy
- Document processing and OCR integration
- Backend API design with FastAPI
- Frontend integration with Next.js and TypeScript
- Secure file upload basics
- CSV export safety and reviewed-only export rules
- Testable free-first architecture
- Clear limitations and practical roadmap planning

## Disclaimer

DocuLedger is a portfolio MVP, not production accounting software. It does not guarantee extraction accuracy, does not provide financial advice, and does not include official QuickBooks or Xero API integrations. Human review is required before using exported data in bookkeeping workflows.
