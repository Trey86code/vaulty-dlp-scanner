"""File type routing + text extraction + detection."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any

from .extractors import from_txt, from_csv, from_pdf
from .patterns import detect, Finding


SUPPORTED_SUFFIXES = {".txt", ".csv", ".pdf"}
SUPPORTED_MIME_TYPES = {
    "text/plain",
    "text/csv",
    "application/pdf",
}


def _pick_extractor(path: Path):
    """Return the correct extractor function for the file."""
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return from_txt
    if suffix == ".csv":
        return from_csv
    if suffix == ".pdf":
        return from_pdf

    # Fallback: try mime-type guessing if suffix is weird
    mime, _ = mimetypes.guess_type(str(path))
    if mime == "text/plain":
        return from_txt
    if mime == "text/csv":
        return from_csv
    if mime == "application/pdf":
        return from_pdf

    return None


def scan_file(
    input_path: str | Path,
    *,
    options: dict[str, Any] | None = None,
) -> list[Finding]:
    """Scan a file by extracting text and running detectors.

    Args:
        input_path: Path to file to scan.
        options: Pending Development — scan toggles (ipv4/phone/etc.).

    Returns:
        List of Finding objects.
    """
    path = Path(input_path)

    extractor = _pick_extractor(path)
    if extractor is None:
        # Unsupported file type → no findings
        return []

    file_type, text = extractor(path)

    # Pending Development:
    # options will later control which detectors are enabled.
    findings = detect(text, file_name=path.name)

    return findings
