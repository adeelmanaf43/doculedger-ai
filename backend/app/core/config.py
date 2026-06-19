from dataclasses import dataclass, field
import os


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = "DocuLedger"
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "local"))
    app_debug: bool = field(default_factory=lambda: _get_bool("APP_DEBUG", True))
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DOCULEDGER_DATABASE_URL",
            "sqlite:///./doculedger.db",
        )
    )
    storage_provider: str = field(
        default_factory=lambda: os.getenv("DOCULEDGER_STORAGE_PROVIDER", "local")
    )
    local_storage_dir: str = field(
        default_factory=lambda: os.getenv("DOCULEDGER_LOCAL_STORAGE_DIR", "./storage")
    )
    max_upload_mb: int = field(
        default_factory=lambda: _get_int("DOCULEDGER_MAX_UPLOAD_MB", 10)
    )
    file_retention_hours: int = field(
        default_factory=lambda: _get_int("DOCULEDGER_FILE_RETENTION_HOURS", 24)
    )
    ocr_provider: str = field(
        default_factory=lambda: os.getenv("DOCULEDGER_OCR_PROVIDER", "tesseract")
    )
    extractor_provider: str = field(
        default_factory=lambda: os.getenv("DOCULEDGER_EXTRACTOR_PROVIDER", "rule_based")
    )
    external_ai_enabled: bool = field(
        default_factory=lambda: _get_bool("DOCULEDGER_EXTERNAL_AI_ENABLED", False)
    )
    google_vision_enabled: bool = field(
        default_factory=lambda: _get_bool("DOCULEDGER_GOOGLE_VISION_ENABLED", False)
    )
    quickbooks_sync_enabled: bool = field(
        default_factory=lambda: _get_bool("DOCULEDGER_QUICKBOOKS_SYNC_ENABLED", False)
    )
    xero_sync_enabled: bool = field(
        default_factory=lambda: _get_bool("DOCULEDGER_XERO_SYNC_ENABLED", False)
    )
    stripe_enabled: bool = field(
        default_factory=lambda: _get_bool("DOCULEDGER_STRIPE_ENABLED", False)
    )

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


settings = Settings()


def get_settings() -> Settings:
    return settings
