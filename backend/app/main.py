from fastapi import FastAPI

from app.api.routes_documents import router as documents_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
        "free_first": True,
    }
