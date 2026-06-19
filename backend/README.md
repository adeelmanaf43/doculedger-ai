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

## Run Tests

```powershell
pytest
```

Current scope includes the app entrypoint, safe config defaults, health endpoint, local document upload storage, text extraction for text-based PDFs, and local Tesseract OCR for images. PDF page conversion, invoice field extraction, database models, paid APIs, and frontend work are intentionally not implemented yet.
