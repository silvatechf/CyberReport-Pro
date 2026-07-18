"""
CyberReport-Pro CLI, built with Click.

Usage example:
    cyberreport-pro generate data/sample_findings.json -o output/report.pdf
    cyberreport-pro list-categories
"""

from __future__ import annotations

import sys

import click

from cyberreport_pro import __version__
from cyberreport_pro.core.compliance_mapper import known_categories
from cyberreport_pro.core.loader import FindingsFileError, load_report_from_json
from cyberreport_pro.render.pdf_generator import PDFGenerationError, generate_pdf


@click.group()
@click.version_option(version=__version__, prog_name="cyberreport-pro")
def cli() -> None:
    """CyberReport-Pro: generates security reports mapped to ENS and RGPD compliance."""


@cli.command()
@click.argument("findings_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    "output_path",
    default="output/report.pdf",
    show_default=True,
    help="Path where the generated PDF will be saved.",
)
def generate(findings_file: str, output_path: str) -> None:
    """Generate a PDF report from a FINDINGS_FILE JSON file."""
    try:
        report = load_report_from_json(findings_file)
    except (FindingsFileError, FileNotFoundError) as exc:
        click.secho(f"Error reading '{findings_file}': {exc}", fg="red", err=True)
        sys.exit(1)

    total = len(report.mapped_findings)
    click.echo(f"Loaded {total} finding(s). Generating report...")

    try:
        result_path = generate_pdf(report, output_path)
    except PDFGenerationError as exc:
        click.secho(f"Failed to generate PDF: {exc}", fg="red", err=True)
        sys.exit(1)

    summary = report.risk_summary
    click.secho(f"✔ Report generated at: {result_path}", fg="green")
    click.echo(
        f"  Critical: {summary['critical']} | High: {summary['high']} | "
        f"Medium: {summary['medium']} | Low: {summary['low']} | Info: {summary['info']}"
    )


@cli.command("list-categories")
def list_categories() -> None:
    """List technical categories that already have a legal mapping implemented."""
    click.echo("Categories with legal mapping available:")
    for category in known_categories():
        click.echo(f"  • {category}")


def main() -> None:
    """Entry point used by pyproject.toml (console_scripts)."""
    cli()


if __name__ == "__main__":
    main()
