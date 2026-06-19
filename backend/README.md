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

## Run Tests

```powershell
pytest
```

Current scope includes only the app entrypoint, safe config defaults, and the health endpoint. Upload, OCR, extraction, storage, database models, and frontend work are intentionally not implemented yet.
