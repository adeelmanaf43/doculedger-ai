# DocuLedger

DocuLedger is a free-first, review-assisted invoice and receipt processing MVP for small bookkeeping workflows.

It helps users upload invoice or receipt PDFs/images, create a local extraction draft, review and correct the extracted fields, and export approved CSV files for generic Excel, QuickBooks-style, and Xero-style workflows.

DocuLedger is not autonomous bookkeeping. Extracted data is treated as a draft until a human reviewer approves it.

## Target Users

- Small bookkeepers and CPA firms
- Ecommerce operators processing receipts
- Property managers handling vendor invoices
- Small businesses entering invoice data manually

## Problem Solved

Many small teams still read invoice PDFs/images by hand and manually enter vendor names, invoice numbers, dates, totals, tax, and currency into spreadsheets or accounting tools. DocuLedger reduces that manual effort while keeping human review in the loop.

## Current MVP Workflow

```text
upload document -> process text/OCR -> review extracted fields -> approve invoice -> export CSV
```

## Tech Stack

- Backend: FastAPI, Python, Pydantic, pytest
- Frontend: Next.js, TypeScript, Tailwind CSS
- OCR: local Tesseract through `pytesseract` and Pillow
- PDF text extraction: local/free Python PDF tooling
- Extraction: rule-based invoice parser
- Persistence: SQLite for reviewed invoices
- Export: Python standard-library CSV generation

## Features Completed

- Secure PDF/PNG/JPG/JPEG upload validation
- Local temporary document storage
- Text extraction for text-based PDFs
- Local image OCR for PNG/JPG/JPEG
- Rule-based invoice field extraction
- Confidence scores and warnings
- Human review and correction workflow
- Reviewed-only CSV export
- Generic, QuickBooks-style, and Xero-style CSV templates
- Next.js frontend for upload, process, review, and export
- Backend tests for the core workflow
- Demo data and demo workflow documentation

## Run The Backend

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

Run tests:

```powershell
python -m pytest
```

## Run The Frontend

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

If your backend uses a different port, update:

```text
frontend/.env.local
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://127.0.0.1:8001
```

## Demo Workflow

Start with:

```text
demo/sample_invoices/abc_supplies_invoice.pdf
```

Then follow:

```text
docs/DEMO_WORKFLOW.md
```

Expected CSV examples are available under:

```text
demo/expected_outputs/
```

## Screenshots

Screenshots are not included yet. Recommended screenshots for a portfolio README:

- Upload screen with backend connected
- Processed invoice draft with warnings/confidence
- Review form after correction
- CSV export buttons after approval

## Architecture Summary

```text
Next.js frontend
  -> FastAPI backend
    -> local storage
    -> PDF text extraction or local OCR
    -> rule-based invoice extraction
    -> SQLite reviewed invoice persistence
    -> CSV exporter
```

## Free-First Approach

The MVP does not require OpenAI, Claude, Google Vision, Stripe, QuickBooks APIs, Xero APIs, paid hosting, or paid storage. Local/free tools are used first so the workflow can be tested privately and cheaply.

Paid providers may be added later behind adapter interfaces and disabled-by-default feature flags.

## Security And Privacy Notes

- Do not commit real invoices, receipts, `.env` files, API keys, or client financial data.
- Demo files contain fake data only.
- Uploaded source files are sensitive and stored locally in MVP mode.
- API responses avoid exposing absolute internal storage paths.
- CSV export is allowed only after human review approval.
- Full OCR/invoice text should not be logged in production.

## Current Limitations

- Not production-ready.
- No authentication, user accounts, or workspace isolation.
- No dashboard/history view.
- No batch upload or batch export.
- No direct QuickBooks or Xero API integration.
- CSV formats are MVP templates and may need client-specific mapping.
- Scanned PDF page conversion is not implemented yet.
- OCR and rule-based extraction are imperfect and require human review.

## Future Roadmap

- Add authentication and workspace isolation.
- Add audit logs for upload, process, review, export, and delete.
- Add configurable retention cleanup for source files.
- Add scanned PDF page conversion.
- Add batch processing and batch CSV export.
- Add client-specific CSV mapping.
- Add optional paid OCR/LLM adapters behind feature flags.
