from dataclasses import dataclass
from pathlib import Path
import re
from uuid import UUID
from uuid import uuid4

from fastapi import UploadFile, status

from app.core.config import Settings
from app.schemas.document import UploadedDocumentMetadata


ALLOWED_CONTENT_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}
CHUNK_SIZE_BYTES = 1024 * 1024


@dataclass(frozen=True)
class StoredDocumentRef:
    document_id: str
    storage_key: str
    path: Path
    safe_filename: str
    content_type: str


class DocumentUploadError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class DocumentStorageError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class LocalDocumentStorage:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.storage_root = Path(settings.local_storage_dir)

    async def save_upload(self, file: UploadFile) -> UploadedDocumentMetadata:
        original_filename = file.filename or ""
        safe_base_name = sanitize_filename(original_filename)
        extension = Path(safe_base_name).suffix.lower()
        content_type = file.content_type or "application/octet-stream"

        self._validate_file_type(extension, content_type)

        document_id = str(uuid4())
        safe_filename = f"{document_id}_{safe_base_name}"
        document_dir = self.storage_root / document_id
        destination = document_dir / safe_filename
        storage_key = f"{document_id}/{safe_filename}"

        self._ensure_safe_destination(destination)
        document_dir.mkdir(parents=True, exist_ok=True)

        size_bytes = 0
        try:
            with destination.open("wb") as output_file:
                while chunk := await file.read(CHUNK_SIZE_BYTES):
                    size_bytes += len(chunk)
                    if size_bytes > self.settings.max_upload_bytes:
                        raise DocumentUploadError(
                            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            f"File exceeds the {self.settings.max_upload_mb} MB upload limit.",
                        )
                    output_file.write(chunk)
        except DocumentUploadError:
            destination.unlink(missing_ok=True)
            if document_dir.exists() and not any(document_dir.iterdir()):
                document_dir.rmdir()
            raise

        if size_bytes == 0:
            destination.unlink(missing_ok=True)
            if document_dir.exists() and not any(document_dir.iterdir()):
                document_dir.rmdir()
            raise DocumentUploadError(
                status.HTTP_400_BAD_REQUEST,
                "Uploaded file is empty.",
            )

        return UploadedDocumentMetadata(
            document_id=document_id,
            original_filename=original_filename,
            safe_filename=safe_filename,
            content_type=content_type,
            size_bytes=size_bytes,
            storage_key=storage_key,
            status="uploaded",
        )

    def get_stored_document(self, document_id: str) -> StoredDocumentRef:
        if not _is_valid_document_id(document_id):
            raise DocumentStorageError(
                status.HTTP_404_NOT_FOUND,
                "Document not found.",
            )

        document_dir = self.storage_root / document_id
        self._ensure_safe_destination(document_dir)
        if not document_dir.is_dir():
            raise DocumentStorageError(
                status.HTTP_404_NOT_FOUND,
                "Document not found.",
            )

        files = [path for path in document_dir.iterdir() if path.is_file()]
        if not files:
            raise DocumentStorageError(
                status.HTTP_404_NOT_FOUND,
                "Document not found.",
            )
        if len(files) > 1:
            raise DocumentStorageError(
                status.HTTP_409_CONFLICT,
                "Document storage contains more than one source file.",
            )

        document_path = files[0]
        self._ensure_safe_destination(document_path)
        extension = document_path.suffix.lower()
        content_type = ALLOWED_CONTENT_TYPES.get(extension, "application/octet-stream")

        return StoredDocumentRef(
            document_id=document_id,
            storage_key=f"{document_id}/{document_path.name}",
            path=document_path,
            safe_filename=document_path.name,
            content_type=content_type,
        )

    def _validate_file_type(self, extension: str, content_type: str) -> None:
        expected_content_type = ALLOWED_CONTENT_TYPES.get(extension)
        if expected_content_type is None:
            raise DocumentUploadError(
                status.HTTP_400_BAD_REQUEST,
                "Unsupported file type. Upload a PDF, PNG, JPG, or JPEG file.",
            )
        if content_type != expected_content_type:
            raise DocumentUploadError(
                status.HTTP_400_BAD_REQUEST,
                "File content type does not match an allowed invoice or receipt format.",
            )

    def _ensure_safe_destination(self, destination: Path) -> None:
        root = self.storage_root.resolve()
        resolved_destination = destination.resolve()
        if root != resolved_destination and root not in resolved_destination.parents:
            raise DocumentUploadError(
                status.HTTP_400_BAD_REQUEST,
                "Invalid upload filename.",
            )


def sanitize_filename(filename: str) -> str:
    base_name = filename.replace("\\", "/").split("/")[-1].strip()
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", base_name).strip("._")
    if not safe_name or "." not in safe_name:
        raise DocumentUploadError(
            status.HTTP_400_BAD_REQUEST,
            "Uploaded file must have a valid filename and extension.",
        )
    return safe_name


def _is_valid_document_id(document_id: str) -> bool:
    try:
        return str(UUID(document_id)) == document_id
    except ValueError:
        return False
