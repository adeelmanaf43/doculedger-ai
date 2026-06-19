# 04_FIRST_IMPLEMENTATION_PROMPT.md

Use this only after Codex has read and understood the starter docs.

```text
Implement the first backend milestone only.

Goal:
Create the backend FastAPI scaffold and configuration layer for DocuLedger.

Scope:
- Create backend folder structure.
- Create FastAPI app entrypoint.
- Add health endpoint.
- Add config module using environment variables.
- Add `.env.example` with safe placeholders only.
- Add requirements file.
- Add pytest setup.
- Add one passing health endpoint test.
- Add README instructions for running backend locally.

Out of scope:
- Do not build OCR yet.
- Do not build frontend yet.
- Do not add paid APIs.
- Do not add database models yet unless needed for app startup.

Constraints:
- Follow AGENTS.md.
- Keep Windows-friendly setup.
- No Docker required.
- No secrets.
- Keep code clean and minimal.

Done when:
- Backend starts locally.
- Health endpoint returns OK.
- pytest passes.
- README has backend setup command.
- You summarize files changed, commands run, tests passed, and remaining risks.
```

