# DocuLedger Frontend

Next.js frontend MVP for the free-first DocuLedger workflow:

```text
upload invoice -> process draft -> review fields -> approve -> export CSV
```

The frontend does not perform OCR or invoice extraction itself. It calls the FastAPI backend and presents the review-assisted workflow in the browser.

## Prerequisites

- Node.js installed
- Backend running locally
- Tesseract installed separately if you want real image OCR

## Local Setup

From the repository root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
```

Default backend URL:

```text
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://localhost:8000
```

If the backend is running on port `8001`, update `.env.local`:

```text
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://127.0.0.1:8001
```

Restart `npm run dev` after changing `.env.local`.

## Run The Backend

In a separate terminal:

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

## Run The Frontend

```powershell
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

## Workflow

1. Upload a PDF, PNG, JPG, or JPEG invoice/receipt.
2. Process the uploaded document through the backend.
3. Review the extracted draft fields, confidence scores, and warnings.
4. Correct fields and save an approved review.
5. Download Generic, QuickBooks-style, or Xero-style CSV.

Export buttons stay disabled until the backend confirms the invoice is reviewed and approved.

## Validation

```powershell
npm run build
npm run lint
```

## Demo Data

Use the fake sample files under:

```text
../demo/sample_invoices/
```

Start with:

```text
abc_supplies_invoice.pdf
```

## Troubleshooting

### Backend Not Running

If the page says it cannot reach the backend, start FastAPI and confirm `/health` works.

### Port Blocked On Windows

If `8000` is blocked, run the backend on `8001`:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Then update:

```text
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://127.0.0.1:8001
```

### CORS Error

The backend allows `http://localhost:3000` by default. If you use another frontend origin, set:

```powershell
$env:DOCULEDGER_CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### OCR Error

Image OCR requires the Tesseract executable to be installed separately. Install Tesseract and configure `DOCULEDGER_TESSERACT_CMD` if Windows cannot find it.

## Limitations

- No authentication.
- No dashboard/history.
- No batch upload or batch export.
- No direct QuickBooks/Xero API sync.
- No paid OCR or AI providers.
- CSV formats are MVP templates and may need client-specific mapping.
- No raw full OCR text is shown by default.
