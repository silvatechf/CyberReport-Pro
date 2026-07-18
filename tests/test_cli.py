from click.testing import CliRunner

from cyberreport_pro.cli import cli


def test_list_categories_command():
    runner = CliRunner()

    result = runner.invoke(cli, ["list-categories"])

    assert result.exit_code == 0
    assert "sql_injection" in result.output


def test_generate_command_with_valid_file(tmp_path):
    runner = CliRunner()
    output_path = tmp_path / "out.pdf"

    result = runner.invoke(
        cli, ["generate", "data/sample_findings.json", "-o", str(output_path)]
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "Report generated" in result.output


def test_generate_command_with_missing_file():
    runner = CliRunner()

    result = runner.invoke(cli, ["generate", "data/nao_existe.json"])

    assert result.exit_code != 0


def test_version_flag():
    runner = CliRunner()

    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "cyberreport-pro" in result.output
