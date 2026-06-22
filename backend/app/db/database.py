from pathlib import Path
import re
import sqlite3
from urllib.parse import unquote, urlparse

from app.core.config import Settings


def sqlite_path_from_url(database_url: str) -> Path:
    parsed = urlparse(database_url)
    if parsed.scheme != "sqlite":
        raise ValueError("Only sqlite database URLs are supported for the local MVP.")

    if parsed.netloc:
        raise ValueError("SQLite database URL must use a local file path.")

    if database_url.startswith("sqlite:///./"):
        return Path(database_url.removeprefix("sqlite:///"))

    if database_url.startswith("sqlite:////"):
        return Path(_normalize_sqlite_path(unquote(parsed.path)))

    if database_url == "sqlite:///:memory:":
        return Path(":memory:")

    if parsed.path:
        return Path(_normalize_sqlite_path(unquote(parsed.path)))

    raise ValueError("SQLite database URL must include a file path.")


def _normalize_sqlite_path(path: str) -> str:
    cleaned = path.replace("\\", "/")
    if re.match(r"^/[A-Za-z]:/", cleaned):
        return cleaned[1:]
    if re.match(r"^//[A-Za-z]:/", cleaned):
        return cleaned[2:]
    return cleaned


def connect(settings: Settings) -> sqlite3.Connection:
    database_path = sqlite_path_from_url(settings.database_url)
    if str(database_path) != ":memory:":
        database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(settings: Settings) -> None:
    with connect(settings) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reviewed_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL UNIQUE,
                reviewed_invoice_json TEXT NOT NULL,
                corrections_json TEXT NOT NULL,
                reviewer_notes TEXT,
                status TEXT NOT NULL,
                approved INTEGER NOT NULL,
                original_extraction_method TEXT,
                corrected_fields_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                reviewed_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
