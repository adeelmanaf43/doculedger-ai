# DocuLedger Backend

FastAPI backend scaffold for the free-first DocuLedger MVP.

## Local Setup on Windows

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

The backend reads configuration from environment variables and uses safe local defaults when variables are not set. The root `.env.example` is the source of truth for current placeholders. Do not commit a real `.env` file or secrets.

## Tesseract OCR on Windows

Image OCR uses local Tesseract through `pytesseract`. Install Tesseract separately before running OCR on real files. On Windows, install Tesseract and either add it to `PATH` or set:

```powershell
$env:DOCULEDGER_TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

OCR remains local/free. No Google Vision, OpenAI, Claude, or paid OCR provider is used.

## Run the API

```powershell
uvicorn app.main:app --reload
```

Then open:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "DocuLedger",
  "environment": "local",
  "free_first": true
}
```

## Upload a Document

The local MVP accepts PDF, PNG, JPG, and JPEG uploads at:

```text
POST http://localhost:8000/documents/upload
```

The form field name is `file`. Uploaded source files are stored under `DOCULEDGER_LOCAL_STORAGE_DIR`, which defaults to `./storage`. The API response returns a relative `storage_key` instead of an absolute internal path.

PowerShell example:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/documents/upload" `
  -Method Post `
  -Form @{ file = Get-Item ".\sample-invoice.pdf" }
```

## Extract Text From a PDF

Text-based PDFs can be extracted after upload:

```text
POST http://localhost:8000/documents/{document_id}/extract-text
```

The response includes page count, combined text, per-page text, extraction method, and warnings.

## OCR an Image

PNG, JPG, and JPEG uploads can be OCR processed locally after upload:

```text
POST http://localhost:8000/documents/{document_id}/ocr
```

The response includes combined OCR text, per-page text, extraction method, optional confidence, and warnings. Scanned/image-based PDFs return a limitation warning for now because PDF-to-image page conversion has not been added yet.

## Extract Invoice Fields

Extracted PDF/OCR text can be converted into draft invoice fields with the local rule-based extractor:

```text
POST http://localhost:8000/extractions/invoice
```

The request body includes `text`, `source`, and optional `ocr_confidence`. The extractor uses deterministic regex and simple heuristics for invoice number, dates, money totals, currency, email, phone, vendor name, and basic line-item drafts. It always returns `requires_review: true` because DocuLedger is review-assisted. This extractor is intentionally limited and should be treated as a first-pass draft, not authoritative bookkeeping data.

## Process an Uploaded Document

After upload, a document can be processed end to end:

```text
POST http://localhost:8000/documents/{document_id}/process
```

Optional request body:

```json
{
  "force_ocr": false,
  "include_text_preview": true
}
```

The processing endpoint resolves the stored document, extracts text with the existing PDF text extractor or local Tesseract image OCR, runs the rule-based invoice extractor, and returns a review-required structured invoice draft. It returns processing metadata, confidence scores, warnings, and only an optional short text preview instead of the full raw invoice text.

Limitations:

- Scanned PDF page conversion is not implemented yet.
- Rule-based extraction is imperfect and should be treated as a draft.
- Human review is always required before export or bookkeeping use.
- No paid APIs are required.

## Review and Correct an Invoice

After processing, a human reviewer can save corrected invoice fields and approve the invoice draft:

```text
POST http://localhost:8000/documents/{document_id}/review
```

Example request:

```json
{
  "invoice": {
    "vendor_name": "ABC Supplies Ltd",
    "invoice_number": "INV-1001",
    "invoice_date": "2026-06-20",
    "due_date": "2026-07-20",
    "subtotal": 100.0,
    "tax": 10.0,
    "total": 110.0,
    "currency": "USD",
    "email": "billing@example.com",
    "phone": "+1 555 123 4567",
    "line_items": []
  },
  "corrections": {
    "vendor_name": {
      "original": "ABC Supplles",
      "corrected": "ABC Supplies Ltd"
    },
    "total": {
      "original": 100.0,
      "corrected": 110.0
    }
  },
  "reviewer_notes": "Corrected vendor name and total.",
  "approved": true,
  "original_extraction_method": "rule_based"
}
```

If `approved` is `true`, the saved status is `reviewed` and `requires_review` is `false`. If `approved` is `false`, the saved status is `review_required` and `requires_review` remains `true`.

Retrieve the saved reviewed invoice:

```text
GET http://localhost:8000/documents/{document_id}/review
```

Check document review status:

```text
GET http://localhost:8000/documents/{document_id}/status
```

Status rules:

- `uploaded`: document exists but no review has been saved yet.
- `review_required`: review data is saved but not approved.
- `reviewed`: human-reviewed invoice data has been approved.

Reviewed invoice data is persisted in local SQLite using `DOCULEDGER_DATABASE_URL`, which defaults to `sqlite:///./doculedger.db`. The review workflow stores corrected invoice fields, correction metadata, reviewer notes, timestamps, and approval status. It does not store raw full OCR text.

Limitations:

- No frontend review UI is implemented yet.
- No accounting sync is implemented yet.
- CSV export is single-invoice only for now.

## Export a Reviewed Invoice as CSV

Approved reviewed invoices can be exported as bookkeeping-ready CSV:

```text
GET http://localhost:8000/documents/{document_id}/export?format=generic
```

Supported formats:

- `generic`
- `quickbooks`
- `xero`

PowerShell examples:

```powershell
curl.exe -L `
  "http://localhost:8000/documents/{document_id}/export?format=generic" `
  -o "doculedger-generic.csv"

curl.exe -L `
  "http://localhost:8000/documents/{document_id}/export?format=quickbooks" `
  -o "doculedger-quickbooks.csv"

curl.exe -L `
  "http://localhost:8000/documents/{document_id}/export?format=xero" `
  -o "doculedger-xero.csv"
```

CSV export uses the saved reviewed invoice as the source of truth. Invoices with `status: review_required` or `approved: false` cannot be exported.

The generic export includes one row per invoice with document ID, invoice fields, review status, reviewed timestamp, and reviewer notes. The QuickBooks and Xero formats are MVP-style CSV templates for common accounting workflows; client-specific column mapping may be needed later.

Limitations:

- Only reviewed and approved invoices can be exported.
- QuickBooks/Xero CSV files are templates, not direct QuickBooks/Xero API integrations.
- Client-specific chart-of-accounts and tax mapping may need adjustment later.
- Batch export is not implemented yet.
- No frontend export UI is implemented yet.
- No direct QuickBooks/Xero API sync is implemented yet.

## Run Tests

```powershell
pytest
```

Current scope includes the app entrypoint, safe config defaults, health endpoint, local document upload storage, text extraction for text-based PDFs, local Tesseract OCR for images, rule-based invoice field extraction, an end-to-end document processing endpoint, backend review/correction persistence, and single-invoice CSV export. PDF page conversion, human review UI, batch export, paid APIs, and frontend work are intentionally not implemented yet.
