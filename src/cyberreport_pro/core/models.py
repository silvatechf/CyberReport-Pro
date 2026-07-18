"""
Core data models for CyberReport-Pro.

Kept deliberately simple (plain dataclasses, no ORM) because the goal of
this project is the legal-mapping and PDF-generation pipeline, not
persistence. If this ever grows into a real service, these models would
migrate easily to Pydantic without breaking the public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Severity(str, Enum):
    """Technical severity of a finding, aligned with common market conventions (CVSS-like)."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    @property
    def weight(self) -> int:
        """Numeric weight used for ordering and aggregate risk calculation."""
        order = {
            Severity.CRITICAL: 4,
            Severity.HIGH: 3,
            Severity.MEDIUM: 2,
            Severity.LOW: 1,
            Severity.INFO: 0,
        }
        return order[self]


@dataclass
class Finding:
    """
    Represents a raw technical finding, typically coming from a scanning
    tool (SAST, DAST, cloud posture, etc.) or entered manually by an analyst.
    """

    id: str
    title: str
    description: str
    severity: Severity
    category: str  # e.g. "sql_injection", "public_storage", "weak_crypto"
    affected_asset: str
    evidence: str = ""
    remediation: str = ""

    def __post_init__(self) -> None:
        if isinstance(self.severity, str):
            self.severity = Severity(self.severity)


@dataclass
class ComplianceMapping:
    """Result of mapping a Finding to a specific legal/regulatory framework."""

    framework: str  # e.g. "ENS", "RGPD/LOPDGDD"
    articles: list[str]
    risk_statement: str
    sanction_reference: str = ""


@dataclass
class MappedFinding:
    """A Finding already enriched with all of its applicable legal mappings."""

    finding: Finding
    mappings: list[ComplianceMapping] = field(default_factory=list)


@dataclass
class ReportMetadata:
    """Report metadata: who it's for, who wrote it, when."""

    client_name: str
    project_name: str
    author: str
    report_date: date
    classification: str = "CONFIDENCIAL - DISTRIBUCIÓN RESTRINGIDA"


@dataclass
class Report:
    """Final aggregate: everything the Jinja2 template needs to render the PDF."""

    metadata: ReportMetadata
    mapped_findings: list[MappedFinding]

    @property
    def risk_summary(self) -> dict[str, int]:
        """Count of findings by severity, used in the PDF's summary table."""
        summary = {s.value: 0 for s in Severity}
        for mf in self.mapped_findings:
            summary[mf.finding.severity.value] += 1
        return summary

    @property
    def sorted_findings(self) -> list[MappedFinding]:
        """Findings sorted by descending severity (critical first)."""
        return sorted(
            self.mapped_findings,
            key=lambda mf: mf.finding.severity.weight,
            reverse=True,
        )

    @property
    def risk_score(self) -> int:
        """
        Aggregate risk score from 0 to 100, computed as the average severity
        weight across all findings, normalized against the maximum possible
        weight (CRITICAL = 4). Used to drive the visual risk gauge in the
        report; the score-to-label mapping (e.g. "CRÍTICO"/"ALTO") lives in
        the template, not here, since that text belongs to the report layer.
        """
        total = len(self.mapped_findings)
        if total == 0:
            return 0
        weighted_sum = sum(mf.finding.severity.weight for mf in self.mapped_findings)
        max_possible = total * Severity.CRITICAL.weight
        return round(100 * weighted_sum / max_possible)
