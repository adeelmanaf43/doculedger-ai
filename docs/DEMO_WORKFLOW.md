# DocuLedger Demo Workflow

Use this guide to run a local portfolio demo of the current MVP.

## 1. Start The Backend

```powershell
cd E:\portfolio-projects\doculedger\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/health
```

Expected result: a JSON response with `status: "ok"` and `free_first: true`.

If Windows blocks port `8000`, use port `8001` and update the frontend `.env.local` file.

## 2. Start The Frontend

```powershell
cd E:\portfolio-projects\doculedger\frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open:

```text
http://localhost:3000
```

Expected result: the page shows a backend connection message.

## 3. Run The Happy Path

1. Upload `demo/sample_invoices/abc_supplies_invoice.pdf`.
2. Confirm the upload returns a document ID.
3. Click `Process document`.
4. Confirm the draft invoice fields appear.
5. Review the fields and correct anything needed.
6. Add a short reviewer note, such as `Demo reviewed and approved.`
7. Click `Approve and save review`.
8. Download the Generic, QuickBooks, and Xero CSV files.

Expected result: export is unavailable before approval and available after approval.

## 4. OCR Demo

Use:

```text
demo/sample_invoices/fresh_office_mart_receipt.png
```

Expected result: the backend uses local Tesseract OCR if Tesseract is installed. If Tesseract is not installed, the UI should show a clear backend error.

## 5. Review-Required Demo

Use:

```text
demo/sample_invoices/global_paper_review_invoice.png
```

This file intentionally omits a due date. Use it to explain why DocuLedger is review-assisted and not autonomous bookkeeping.

## 6. What To Say In A Demo Video

"DocuLedger is a free-first, review-assisted invoice and receipt processing MVP. The user uploads a document, the backend validates and stores it locally, extracts text using PDF text extraction or local OCR, creates a draft invoice using rule-based logic, and then requires a human review before CSV export. The current QuickBooks and Xero outputs are CSV templates, not direct API integrations."

## Known Limitations To Mention

- OCR quality depends on Tesseract and image quality.
- Scanned PDF page conversion is not implemented yet.
- Rule-based extraction is a first-pass draft, not guaranteed accounting truth.
- No authentication, dashboard, batch processing, or production deployment yet.
- QuickBooks and Xero outputs are CSV templates and may need client-specific mapping.
