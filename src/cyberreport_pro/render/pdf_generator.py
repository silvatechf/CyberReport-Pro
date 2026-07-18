"""
Final PDF rendering of the report.

Switched from xhtml2pdf to WeasyPrint after comparing visual output: this
project's reports are meant to look like a real audit deliverable, and
xhtml2pdf's CSS 2.1-era support (no flexbox, no gradients, no reliable
border-radius) was capping report quality. WeasyPrint renders modern CSS
properly and natively supports print-specific features (position: fixed
for repeating watermarks, @page margin boxes with page counters), which
this template now relies on. The trade-off is a heavier dependency on
system libraries (Pango/Cairo) — see the Dockerfile for the apt packages
this requires in a fresh container.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from cyberreport_pro.core.models import Report


class PDFGenerationError(RuntimeError):
    """Raised when WeasyPrint fails to render the HTML into a PDF."""


def _get_template_env() -> Environment:
    template_dir = resources.files("cyberreport_pro").joinpath("templates")
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"]),
    )


def render_html(report: Report) -> str:
    """Render the Report into an HTML string, using the Jinja2 template."""
    env = _get_template_env()
    template = env.get_template("report_template.html")
    return template.render(report=report)


def generate_pdf(report: Report, output_path: str | Path) -> Path:
    """
    Generate the final PDF from a Report.

    Returns the Path of the generated file. Raises PDFGenerationError if
    WeasyPrint fails to render the HTML.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = render_html(report)

    try:
        HTML(string=html_content).write_pdf(str(output_path))
    except Exception as exc:  # noqa: BLE001 - WeasyPrint raises varied internal errors
        raise PDFGenerationError(
            f"WeasyPrint failed to render {output_path}: {exc}"
        ) from exc

    return output_path

