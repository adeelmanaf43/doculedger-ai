# DocuLedger Screenshot Guide

Use this guide to capture real screenshots from the running app. Save screenshots under:

```text
docs/assets/screenshots/
```

Do not use real client invoices. Use fake demo files from:

```text
demo/sample_invoices/
```

## 1. Frontend Home Upload Screen

- Save as: `01-upload-screen.png`
- Capture: `http://localhost:3000` before selecting a file.
- Sample invoice: none yet.
- Visible: DocuLedger title, backend connected status, upload panel, process/review/export panels.
- Do not show: browser bookmarks with private data, local file paths, `.env` values.
- Caption: "DocuLedger upload workflow with FastAPI backend connected."

## 2. Uploaded Document Success

- Save as: `02-upload-success.png`
- Capture: after uploading `abc_supplies_invoice.pdf`.
- Sample invoice: `demo/sample_invoices/abc_supplies_invoice.pdf`.
- Visible: upload success message and document ID.
- Do not show: local storage paths or terminal windows.
- Caption: "A sample invoice uploaded and assigned a document ID."

## 3. Processing Result

- Save as: `03-processing-result.png`
- Capture: after clicking `Process document`.
- Sample invoice: `abc_supplies_invoice.pdf`.
- Visible: processing status, extraction method, confidence values, warnings if present.
- Do not show: full raw OCR text from a real document.
- Caption: "Processing creates a review-required invoice draft with confidence signals."

## 4. Review Form

- Save as: `04-review-form.png`
- Capture: review panel after processing.
- Sample invoice: `abc_supplies_invoice.pdf`.
- Visible: editable vendor, invoice number, date, subtotal, tax, total, currency fields.
- Do not show: real client vendor data.
- Caption: "Human reviewer can correct extracted bookkeeping fields before export."

## 5. Review Approved State

- Save as: `05-review-approved.png`
- Capture: after clicking `Approve and save review`.
- Sample invoice: `abc_supplies_invoice.pdf`.
- Visible: review saved confirmation and `reviewed` status.
- Do not show: private notes or real financial data.
- Caption: "CSV export unlocks only after human approval."

## 6. Export Panel

- Save as: `06-export-buttons.png`
- Capture: after review approval.
- Sample invoice: `abc_supplies_invoice.pdf`.
- Visible: Generic, QuickBooks, and Xero CSV export buttons enabled.
- Do not show: browser download history with private files.
- Caption: "Reviewed invoices can be exported as Generic, QuickBooks-style, or Xero-style CSV."

## 7. CSV Output Example

- Save as: `07-csv-output.png`
- Capture: downloaded CSV opened in a text editor or spreadsheet.
- Sample file: exported Generic CSV or `demo/expected_outputs/generic_example.csv`.
- Visible: CSV headers and fake invoice row.
- Do not show: real client data or private local file paths.
- Caption: "Example reviewed invoice CSV output."

## 8. Optional Backend Swagger Docs

- Save as: `08-api-docs.png`
- Capture: `http://localhost:8000/docs`.
- Sample invoice: none.
- Visible: FastAPI Swagger endpoint list.
- Do not show: stack traces, environment variables, or local database paths.
- Caption: "FastAPI exposes documented backend endpoints for the MVP workflow."
