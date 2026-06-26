# DocuLedger Backend

FastAPI backend for the free-first DocuLedger MVP.

Current workflow:

```text
upload document -> process text/OCR -> extract invoice draft -> review/correct -> export CSV
```

The backend owns validation, document storage, extraction, review persistence, and CSV export. The frontend is available under `frontend/`.

## Local Setup On Windows

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

The backend uses safe local defaults from environment variables. The root `.env.example` is the placeholder reference. Do not commit real `.env` files or secrets.

## Environment Variables

Common local settings:

```text
APP_ENV=local
APP_DEBUG=true
DOCULEDGER_DATABASE_URL=sqlite:///./doculedger.db
DOCULEDGER_LOCAL_STORAGE_DIR=./storage
DOCULEDGER_MAX_UPLOAD_MB=10
DOCULEDGER_OCR_PROVIDER=tesseract
DOCULEDGER_TESSERACT_CMD=
DOCULEDGER_EXTRACTOR_PROVIDER=rule_based
DOCULEDGER_EXTERNAL_AI_ENABLED=false
DOCULEDGER_GOOGLE_VISION_ENABLED=false
DOCULEDGER_QUICKBOOKS_SYNC_ENABLED=false
DOCULEDGER_XERO_SYNC_ENABLED=false
DOCULEDGER_STRIPE_ENABLED=false
DOCULEDGER_CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Tesseract OCR On Windows

Image OCR uses local Tesseract through `pytesseract`. Install Tesseract separately before OCR processing real image files.

Either add Tesseract to `PATH` or set:

```powershell
$env:DOCULEDGER_TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

OCR remains local/free. Google Vision, OpenAI, Claude, and paid OCR providers are not used in this MVP.

## Run The API

```powershell
python -m uvicorn app.main:app --reload
```

Open:

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

If Windows blocks port `8000`, run on another port:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Then update the frontend `.env.local` value.

## Endpoints

### Health

```text
GET /health
```

### Upload

```text
POST /documents/upload
```

Form field: `file`

Accepted formats:

- PDF
- PNG
- JPG/JPEG

The response includes a safe relative `storage_key`, not an absolute internal file path.

### PDF Text Extraction

```text
POST /documents/{document_id}/extract-text
```

Supports text-based PDFs. Scanned/image PDFs need a future page-conversion step.

### Image OCR

```text
POST /documents/{document_id}/ocr
```

Supports PNG, JPG, and JPEG through local Tesseract. Scanned PDFs return a limitation warning for now.

### Invoice Field Extraction

```text
POST /extractions/invoice
```

Runs the rule-based extractor on text and returns draft invoice fields, confidence scores, and warnings.

### End-To-End Processing

```text
POST /documents/{document_id}/process
```

Optional body:

```json
{
  "force_ocr": false,
  "include_text_preview": true
}
```

The endpoint resolves the stored document, extracts text/OCR where supported, runs rule-based invoice extraction, and returns a review-required draft.

### Human Review

Save a reviewed invoice:

```text
POST /documents/{document_id}/review
```

Retrieve a reviewed invoice:

```text
GET /documents/{document_id}/review
```

Check status:

```text
GET /documents/{document_id}/status
```

Status rules:

- `uploaded`: document exists but no review has been saved.
- `review_required`: review data exists but has not been approved.
- `reviewed`: human-reviewed invoice data has been approved.

Reviewed invoice data is stored in SQLite through Python's built-in `sqlite3`.

### CSV Export

```text
GET /documents/{document_id}/export?format=generic
GET /documents/{document_id}/export?format=quickbooks
GET /documents/{document_id}/export?format=xero
```

CSV export uses the saved reviewed invoice as the source of truth. Unreviewed or unapproved invoices cannot be exported.

The QuickBooks and Xero outputs are MVP-style CSV templates. They are not direct QuickBooks/Xero API integrations and may need client-specific mapping later.

## CORS For Local Frontend

The backend allows local frontend requests from:

```text
http://localhost:3000
```

Override with:

```powershell
$env:DOCULEDGER_CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

## Run Tests

```powershell
python -m pytest
```

The pytest configuration focuses collection on `backend/tests` and uses a local `.pytest-tmp` base directory to avoid Windows permission issues with stray pytest temp folders.

## Limitations

- Not production-ready.
- No authentication or workspace isolation yet.
- No dashboard/history yet.
- No batch upload or batch export yet.
- No direct QuickBooks/Xero API sync.
- Scanned PDF page conversion is not implemented yet.
- OCR depends on local Tesseract installation and image quality.
- Rule-based extraction is imperfect and always requires review before export.
