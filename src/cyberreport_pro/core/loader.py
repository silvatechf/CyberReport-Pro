"""
Loads Findings from a JSON input file.

Expected format (see data/sample_findings.json for a full example):

{
  "client_name": "...",
  "project_name": "...",
  "author": "...",
  "findings": [
    {
      "id": "F-001",
      "title": "...",
      "description": "...",
      "severity": "high",
      "category": "sql_injection",
      "affected_asset": "...",
      "evidence": "...",
      "remediation": "..."
    }
  ]
}
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from cyberreport_pro.core.compliance_mapper import map_findings
from cyberreport_pro.core.models import Finding, Report, ReportMetadata


class FindingsFileError(ValueError):
    """Raised when the input file is malformed or incomplete."""


_REQUIRED_TOP_LEVEL_KEYS = {"client_name", "project_name", "author", "findings"}
_REQUIRED_FINDING_KEYS = {"id", "title", "description", "severity", "category", "affected_asset"}


def _validate_payload(payload: dict[str, Any]) -> None:
    missing = _REQUIRED_TOP_LEVEL_KEYS - payload.keys()
    if missing:
        raise FindingsFileError(f"Missing required fields in JSON: {sorted(missing)}")

    if not isinstance(payload["findings"], list) or not payload["findings"]:
        raise FindingsFileError("'findings' must be a non-empty list.")

    for idx, item in enumerate(payload["findings"]):
        missing_fields = _REQUIRED_FINDING_KEYS - item.keys()
        if missing_fields:
            raise FindingsFileError(
                f"Finding at index {idx} is incomplete: missing {sorted(missing_fields)}"
            )


def load_report_from_json(path: str | Path) -> Report:
    """Read a JSON findings file and return a fully mapped Report, ready to render."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Findings file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    _validate_payload(payload)

    findings = [Finding(**item) for item in payload["findings"]]
    mapped = map_findings(findings)

    metadata = ReportMetadata(
        client_name=payload["client_name"],
        project_name=payload["project_name"],
        author=payload["author"],
        report_date=date.today(),
    )

    return Report(metadata=metadata, mapped_findings=mapped)
