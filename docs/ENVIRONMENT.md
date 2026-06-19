# ENVIRONMENT.md

## Local development target

The project should be Windows-friendly and should not require Docker for the MVP.

## Expected tools

- Python 3.10+
- Node.js LTS
- Git
- Tesseract OCR installed locally
- Optional: Poppler for PDF-to-image workflows

## Backend environment variables

Create `.env.example` with placeholders only:

```text
APP_ENV=local
APP_DEBUG=true
DOCULEDGER_DATABASE_URL=sqlite:///./doculedger.db
DOCULEDGER_STORAGE_PROVIDER=local
DOCULEDGER_LOCAL_STORAGE_DIR=./storage
DOCULEDGER_MAX_UPLOAD_MB=10
DOCULEDGER_FILE_RETENTION_HOURS=24
DOCULEDGER_OCR_PROVIDER=tesseract
DOCULEDGER_EXTRACTOR_PROVIDER=rule_based
DOCULEDGER_EXTERNAL_AI_ENABLED=false
DOCULEDGER_GOOGLE_VISION_ENABLED=false
DOCULEDGER_QUICKBOOKS_SYNC_ENABLED=false
DOCULEDGER_XERO_SYNC_ENABLED=false
DOCULEDGER_STRIPE_ENABLED=false
```

## Frontend environment variables

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Local startup target

Backend:

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Provider mode rules

Default MVP:

```text
OCR provider = tesseract
Extractor provider = rule_based
Storage provider = local
Database = sqlite
Accounting sync = disabled
Billing = disabled
```

Paid provider modes must be opt-in only.

