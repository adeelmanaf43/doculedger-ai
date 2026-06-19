# DECISIONS.md

## Decision log

### Decision 1: Build review-assisted invoice processing first

Decision:

Build DocuLedger as a review-assisted invoice-to-CSV product, not a fully autonomous bookkeeping SaaS.

Reason:

Bookkeepers need speed and accuracy, but they also need control. A human-review workflow is easier to trust, easier to sell, and safer for financial data.

### Decision 2: Free-first MVP

Decision:

The MVP must run without paid APIs.

Reason:

The product should be buildable and demoable with zero API budget. Paid APIs should be added only after client validation or when accuracy/scale blocks revenue.

### Decision 3: CSV before direct QuickBooks/Xero API

Decision:

Build QuickBooks/Xero-compatible CSV export before direct accounting integrations.

Reason:

CSV export is enough for first trials and retainers. Direct sync increases complexity, OAuth risk, support burden, and accounting liability.

### Decision 4: Rule-based extraction before LLM extraction

Decision:

Start with regex/rules/schema validation/confidence scoring. Add LLM extraction later as an adapter.

Reason:

Rule-based extraction is free, testable, explainable, and safer. LLM extraction can improve messy layouts later but must be cost-controlled.

### Decision 5: SQLite before production database

Decision:

Use SQLite for local MVP. Move to Postgres/Supabase when paid clients need cloud access, backups, and multi-user support.

Reason:

SQLite reduces early setup friction and keeps the MVP simple.

### Decision 6: Local storage before object storage

Decision:

Use local temporary storage first. Add R2/S3 later with signed URLs, encryption, and lifecycle deletion.

Reason:

The first MVP only needs local demo/trial capability. Object storage is needed when production clients upload real documents.

### Decision 7: Manual billing before Stripe

Decision:

Use manual invoices, Wise/Payoneer/bank transfer, or platform escrow for first clients. Add Stripe later for self-serve SaaS.

Reason:

Manual billing is enough for the first service/retainer clients and avoids unnecessary early billing complexity.

