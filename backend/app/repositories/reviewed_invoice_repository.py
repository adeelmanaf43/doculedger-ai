from datetime import UTC, datetime
import json
import sqlite3
from typing import Any

from app.core.config import Settings
from app.db.database import connect, init_db


class ReviewNotFoundError(Exception):
    pass


class ReviewedInvoiceRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        init_db(settings)

    def save_review(
        self,
        document_id: str,
        reviewed_invoice: dict[str, Any],
        corrections: dict[str, Any],
        reviewer_notes: str | None,
        approved: bool,
        original_extraction_method: str | None,
        corrected_fields: list[str],
    ) -> dict[str, Any]:
        now = _utc_now()
        status = "reviewed" if approved else "review_required"

        with connect(self.settings) as connection:
            existing = connection.execute(
                "SELECT created_at FROM reviewed_invoices WHERE document_id = ?",
                (document_id,),
            ).fetchone()
            created_at = existing["created_at"] if existing else now

            connection.execute(
                """
                INSERT INTO reviewed_invoices (
                    document_id,
                    reviewed_invoice_json,
                    corrections_json,
                    reviewer_notes,
                    status,
                    approved,
                    original_extraction_method,
                    corrected_fields_json,
                    created_at,
                    updated_at,
                    reviewed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(document_id) DO UPDATE SET
                    reviewed_invoice_json = excluded.reviewed_invoice_json,
                    corrections_json = excluded.corrections_json,
                    reviewer_notes = excluded.reviewer_notes,
                    status = excluded.status,
                    approved = excluded.approved,
                    original_extraction_method = excluded.original_extraction_method,
                    corrected_fields_json = excluded.corrected_fields_json,
                    updated_at = excluded.updated_at,
                    reviewed_at = excluded.reviewed_at
                """,
                (
                    document_id,
                    json.dumps(reviewed_invoice),
                    json.dumps(corrections),
                    reviewer_notes,
                    status,
                    int(approved),
                    original_extraction_method,
                    json.dumps(corrected_fields),
                    created_at,
                    now,
                    now,
                ),
            )
            connection.commit()

        return self.get_review(document_id)

    def get_review(self, document_id: str) -> dict[str, Any]:
        with connect(self.settings) as connection:
            row = connection.execute(
                "SELECT * FROM reviewed_invoices WHERE document_id = ?",
                (document_id,),
            ).fetchone()

        if row is None:
            raise ReviewNotFoundError("Review not found.")

        return _row_to_review(row)

    def get_status(self, document_id: str) -> str | None:
        with connect(self.settings) as connection:
            row = connection.execute(
                "SELECT status FROM reviewed_invoices WHERE document_id = ?",
                (document_id,),
            ).fetchone()
        return row["status"] if row else None


def _row_to_review(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "document_id": row["document_id"],
        "reviewed_invoice": json.loads(row["reviewed_invoice_json"]),
        "corrections": json.loads(row["corrections_json"]),
        "reviewer_notes": row["reviewer_notes"],
        "status": row["status"],
        "approved": bool(row["approved"]),
        "original_extraction_method": row["original_extraction_method"],
        "corrected_fields": json.loads(row["corrected_fields_json"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "reviewed_at": row["reviewed_at"],
    }


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()
