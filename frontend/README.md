# DocuLedger Frontend

Next.js frontend MVP for the free-first DocuLedger workflow:

```text
upload invoice -> process draft -> review fields -> approve -> export CSV
```

## Local Setup

From the repository root:

```powershell
cd frontend
npm install
```

Create a local environment file if needed:

```powershell
Copy-Item .env.example .env.local
```

Default backend URL:

```text
NEXT_PUBLIC_DOCULEDGER_API_BASE_URL=http://localhost:8000
```

## Run the Backend

In a separate terminal:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run the Frontend

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
2. Process the uploaded document through the FastAPI backend.
3. Review the extracted draft fields.
4. Correct fields and save an approved review.
5. Download Generic, QuickBooks-style, or Xero-style CSV.

## Validation

```powershell
npm run build
npm run lint
```

## Limitations

- No authentication.
- No dashboard/history.
- No batch upload or batch export.
- No direct QuickBooks/Xero API sync.
- No paid OCR or AI providers.
- No raw full OCR text is shown by default.
- Export buttons unlock only after backend review approval.

## Troubleshooting

If the app cannot reach the backend, make sure FastAPI is running at the URL in `NEXT_PUBLIC_DOCULEDGER_API_BASE_URL`.

If the browser reports a CORS error, the backend may need local-only CORS enabled for `http://localhost:3000`.
