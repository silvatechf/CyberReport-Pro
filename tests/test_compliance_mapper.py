from cyberreport_pro.core.compliance_mapper import known_categories, map_finding, map_findings
from cyberreport_pro.core.models import Finding, Severity


def _make_finding(**overrides) -> Finding:
    defaults = dict(
        id="F-TEST",
        title="Test finding",
        description="Test description",
        severity=Severity.HIGH,
        category="sql_injection",
        affected_asset="test.asset.local",
    )
    defaults.update(overrides)
    return Finding(**defaults)


def test_known_category_returns_ens_and_rgpd_mappings():
    finding = _make_finding(category="sql_injection")

    mapped = map_finding(finding)

    frameworks = {m.framework for m in mapped.mappings}
    assert "ENS" in frameworks
    assert "RGPD/LOPDGDD" in frameworks


def test_public_storage_mapping_includes_sanction_reference():
    finding = _make_finding(category="public_storage", severity=Severity.HIGH)

    mapped = map_finding(finding)

    rgpd_mapping = next(m for m in mapped.mappings if m.framework == "RGPD/LOPDGDD")
    assert rgpd_mapping.sanction_reference != ""
    assert "RGPD" in rgpd_mapping.sanction_reference or "%" in rgpd_mapping.sanction_reference


def test_unknown_category_falls_back_to_default_mapping():
    finding = _make_finding(category="unknown_category_xyz")

    mapped = map_finding(finding)

    assert len(mapped.mappings) == 1
    assert "no catalogada" in mapped.mappings[0].risk_statement


def test_map_findings_preserves_order_and_count():
    findings = [
        _make_finding(id="F-1", category="sql_injection"),
        _make_finding(id="F-2", category="weak_crypto"),
        _make_finding(id="F-3", category="secrets_exposure"),
    ]

    mapped = map_findings(findings)

    assert len(mapped) == 3
    assert [m.finding.id for m in mapped] == ["F-1", "F-2", "F-3"]


def test_known_categories_returns_sorted_unique_list():
    categories = known_categories()

    assert categories == sorted(categories)
    assert len(categories) == len(set(categories))
    assert "sql_injection" in categories
