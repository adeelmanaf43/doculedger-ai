# 03_VALIDATION_PROMPT.md

Use this after Codex implements a milestone or before committing.

```text
Act as a strict QA engineer and product reviewer for DocuLedger.

Review the current implementation end to end.

Check whether the app can run in free-first mode without:
- OpenAI
- Claude
- Google Vision
- Stripe
- QuickBooks API
- Xero API
- paid hosting
- paid storage

Validate:
1. upload
2. OCR
3. extraction
4. confidence scoring
5. review/correction
6. CSV export
7. report generation if implemented
8. dashboard/history if implemented
9. security/privacy controls
10. tests and docs

Find:
1. critical bugs
2. missing MVP requirements
3. security/privacy issues
4. test gaps
5. incorrect assumptions
6. accidental paid-service dependencies
7. unrelated changes

Then provide:
1. critical bugs
2. missing MVP requirements
3. security/privacy issues
4. test gaps
5. exact fix plan
6. commands to verify completion

If the implementation is safe to commit, provide a clean commit message.
```

