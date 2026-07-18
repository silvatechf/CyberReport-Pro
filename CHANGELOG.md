# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- Replaced `xhtml2pdf` with `WeasyPrint` as the PDF rendering engine.
  WeasyPrint supports modern CSS (flexbox, gradients, `border-radius`,
  `box-shadow`, and `position: fixed` for a genuinely repeating watermark
  across pages), which noticeably improved report visual quality.
  Trade-off: the Docker image now needs Pango/Cairo system libraries.
- Redesigned the report template's cover page and risk gauge to take
  advantage of the above (gradient-filled gauge, diagonal watermark,
  page numbering via `@page` counters).

### Planned
- Additional compliance categories (XXE, SSRF, IDOR).
- ISO 27001 as a second compliance framework.
- Direct integration with `sql-defender` as a findings source.

## [0.1.0] - 2026-07-16

### Added
- Core domain models: `Finding`, `ComplianceMapping`, `MappedFinding`, `Report`.
- Compliance mapper covering 4 categories (`sql_injection`, `public_storage`,
  `weak_crypto`, `secrets_exposure`) against ENS and RGPD/LOPDGDD.
- JSON loader with input validation (`FindingsFileError`).
- PDF report generation via Jinja2 + xhtml2pdf, including a dedicated cover
  page, a visual risk gauge (0-100 score), and a confidentiality watermark.
- Installable CLI (`cyberreport-pro generate`, `cyberreport-pro list-categories`)
  built with Click.
- Test suite: 24 tests, 95% coverage (pytest + pytest-cov).
- Code quality tooling: ruff (lint), bandit (security scan).
- GitHub Actions CI running on Python 3.10, 3.11, and 3.12.
- Pre-commit hooks for ruff and bandit.
