from datetime import date

import pytest

from cyberreport_pro.core.compliance_mapper import map_findings
from cyberreport_pro.core.models import Finding, Report, ReportMetadata, Severity


def _sample_report() -> Report:
    findings = [
        Finding(
            id="F-1",
            title="Crítico",
            description="d",
            severity=Severity.CRITICAL,
            category="sql_injection",
            affected_asset="a",
        ),
        Finding(
            id="F-2",
            title="Baixo",
            description="d",
            severity=Severity.LOW,
            category="missing_headers",
            affected_asset="a",
        ),
        Finding(
            id="F-3",
            title="Alto",
            description="d",
            severity=Severity.HIGH,
            category="public_storage",
            affected_asset="a",
        ),
    ]
    metadata = ReportMetadata(
        client_name="Cliente Teste",
        project_name="Projeto Teste",
        author="Autor Teste",
        report_date=date(2026, 1, 1),
    )
    return Report(metadata=metadata, mapped_findings=map_findings(findings))


def test_severity_weight_orders_correctly():
    assert Severity.CRITICAL.weight > Severity.HIGH.weight
    assert Severity.HIGH.weight > Severity.MEDIUM.weight
    assert Severity.MEDIUM.weight > Severity.LOW.weight
    assert Severity.LOW.weight > Severity.INFO.weight


def test_finding_accepts_severity_as_string():
    finding = Finding(
        id="F-X",
        title="t",
        description="d",
        severity="high",
        category="sql_injection",
        affected_asset="a",
    )
    assert finding.severity == Severity.HIGH


def test_finding_rejects_invalid_severity_string():
    with pytest.raises(ValueError):
        Finding(
            id="F-X",
            title="t",
            description="d",
            severity="apocaliptico",
            category="sql_injection",
            affected_asset="a",
        )


def test_risk_summary_counts_by_severity():
    report = _sample_report()

    summary = report.risk_summary

    assert summary["critical"] == 1
    assert summary["high"] == 1
    assert summary["low"] == 1
    assert summary["medium"] == 0


def test_sorted_findings_orders_by_severity_descending():
    report = _sample_report()

    ordered_ids = [mf.finding.id for mf in report.sorted_findings]

    assert ordered_ids == ["F-1", "F-3", "F-2"]


def test_risk_score_is_zero_for_empty_report():
    metadata = ReportMetadata(
        client_name="C", project_name="P", author="A", report_date=date(2026, 1, 1)
    )
    empty_report = Report(metadata=metadata, mapped_findings=[])

    assert empty_report.risk_score == 0


def test_risk_score_is_100_when_all_findings_are_critical():
    findings = [
        Finding(
            id=f"F-{i}",
            title="t",
            description="d",
            severity=Severity.CRITICAL,
            category="sql_injection",
            affected_asset="a",
        )
        for i in range(3)
    ]
    metadata = ReportMetadata(
        client_name="C", project_name="P", author="A", report_date=date(2026, 1, 1)
    )
    report = Report(metadata=metadata, mapped_findings=map_findings(findings))

    assert report.risk_score == 100


def test_risk_score_is_between_0_and_100_for_mixed_severities():
    report = _sample_report()

    assert 0 < report.risk_score < 100
