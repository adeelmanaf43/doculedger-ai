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

## Run Tests

```powershell
pytest
```

Current scope includes the app entrypoint, safe config defaults, health endpoint, and local document upload storage. OCR, extraction, database models, paid APIs, and frontend work are intentionally not implemented yet.
