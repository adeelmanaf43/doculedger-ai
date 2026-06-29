# LinkedIn Post Drafts

## Version A: Recruiter / Job-Focused

I recently built DocuLedger, a free-first, review-assisted invoice and receipt processing MVP for my Applied AI Engineering portfolio.

The problem I wanted to explore: bookkeepers and small operators often spend hours reading invoice PDFs/images, typing vendor/date/tax/total fields, correcting OCR mistakes, and preparing CSV files for accounting workflows.

Current workflow:

```text
Upload invoice/receipt -> process with PDF text extraction or local OCR -> extract invoice fields -> review/correct fields -> approve -> export CSV
```

Tech stack:

- FastAPI, Python, Pydantic, pytest
- Tesseract OCR through pytesseract/Pillow
- SQLite for reviewed invoice persistence
- Next.js, TypeScript, TailwindCSS
- Python csv module for Generic, QuickBooks-style, and Xero-style CSV templates

The main product decision was to keep it review-assisted rather than pretending invoice extraction is always correct. Financial data needs a human approval step before export.

Current limitations are intentional: no auth, no production deployment, no direct QuickBooks/Xero API integration, no paid OCR/LLM providers, and no claim of 100% extraction accuracy.

What I learned:

- How to design an end-to-end document AI workflow
- How to keep human review central in AI-assisted financial workflows
- How to combine backend APIs, OCR, extraction rules, review persistence, frontend UX, and CSV export

I would appreciate feedback from engineers, recruiters, and founders on the product direction and technical architecture.

#ai #ocr #fastapi #nextjs #portfolioProject

## Version B: Client / Freelance-Focused

I built a working MVP called DocuLedger to explore a common bookkeeping pain point: turning invoice and receipt PDFs/images into clean CSV data without handing the whole process over to a black-box tool.

DocuLedger is review-assisted. A user uploads an invoice, the system extracts draft fields, a human reviews/corrects the data, and only then exports a CSV.

Workflow:

```text
Upload invoice/receipt -> process with local OCR or PDF text extraction -> review fields -> approve -> export Generic/QuickBooks-style/Xero-style CSV
```

This is not fully automatic bookkeeping, and it does not claim perfect accuracy. The goal is practical time savings while keeping control over financial data.

For the MVP, I kept it free-first:

- Local Tesseract OCR
- Rule-based invoice extraction
- SQLite review persistence
- CSV export templates
- No paid AI APIs required

I am looking for feedback from bookkeepers, accounting firms, ecommerce operators, and property/construction businesses that process invoices manually.

If this sounds relevant, I can process a small test batch of 20 invoices and return a reviewed CSV plus a short summary of extraction quality and time-saving potential.

#bookkeeping #invoiceProcessing #ocr #smallBusiness #automation
