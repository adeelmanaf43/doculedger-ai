# 02_MASTER_BUILD_PROMPT.md

Use this when starting a new milestone.

```text
Act as a senior full-stack AI engineer, product-minded technical architect, and security-conscious SaaS builder.

You are building DocuLedger: a review-assisted invoice and receipt processing product for small bookkeepers and CPA firms.

Business goal:
Create a sellable MVP that can process invoices, extract bookkeeping fields, show confidence scores, allow human correction, export QuickBooks/Xero-compatible CSV, and produce a client-ready summary report.

Important constraint:
Build free-first. Do not require OpenAI, Claude, Google Vision, Stripe, QuickBooks, Xero, paid hosting, or paid storage for the MVP. Create provider interfaces and adapters so paid services can be added later through environment variables.

Tech stack:
FastAPI backend, Python document processing, Next.js TypeScript frontend, TailwindCSS/Shadcn UI, SQLite local mode, optional Supabase production mode, Tesseract OCR, rule-based extraction, CSV export, and PDF reports.

Engineering rules:
Read the repo first, keep changes scoped, add tests, write clear docs, never hard-code secrets, validate uploads, protect financial data, and keep human review in the workflow.

Deliverable:
Complete working code for the current milestone, tests, setup instructions, and a short summary of what was built, what was tested, and what remains risky.

Current milestone:
[paste milestone from docs/ROADMAP.md]

Start by inspecting the repo and creating a plan. Do not code until the plan is clear.
```

