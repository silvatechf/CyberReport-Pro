from cyberreport_pro.core.loader import load_report_from_json
from cyberreport_pro.render.pdf_generator import generate_pdf, render_html


def test_render_html_contains_client_name_and_findings():
    report = load_report_from_json("data/sample_findings.json")

    html = render_html(report)

    assert "Acme Retail S.A." in html
    assert "SQL Injection" in html
    assert "ENS" in html
    assert "RGPD" in html


def test_generate_pdf_creates_valid_pdf_file(tmp_path):
    report = load_report_from_json("data/sample_findings.json")
    output_file = tmp_path / "relatorio.pdf"

    result_path = generate_pdf(report, output_file)

    assert result_path.exists()
    assert result_path.stat().st_size > 1000  # PDF não-trivial foi gerado
    with result_path.open("rb") as f:
        header = f.read(5)
    assert header == b"%PDF-"
