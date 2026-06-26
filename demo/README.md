# DocuLedger Demo Data

This folder contains fake, safe demo files for recording or presenting the DocuLedger MVP workflow. Do not replace these files with real client invoices or sensitive financial documents.

## Sample Invoices

- `sample_invoices/abc_supplies_invoice.pdf` - clean text-based invoice for the first demo pass.
- `sample_invoices/fresh_office_mart_receipt.png` - receipt-style image for local Tesseract OCR.
- `sample_invoices/global_paper_review_invoice.png` - imperfect invoice image with a missing due date to demonstrate warnings and human review.

## Expected CSV Outputs

- `expected_outputs/generic_example.csv`
- `expected_outputs/quickbooks_example.csv`
- `expected_outputs/xero_example.csv`

These CSV files are examples of reviewed exports. QuickBooks and Xero files are MVP-style CSV templates, not official direct integrations.

## Demo Notes

Start with `abc_supplies_invoice.pdf` when you want the most predictable extraction. Use the image samples when you want to demonstrate local OCR and why human review matters.
