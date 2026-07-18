
# Security Policy

Yes, a security-reporting tool needs one of these too — applying the same process to itself is part of the point of this project.

## Responsible Disclosure

We take the security of this project seriously. Please do not report security vulnerabilities in public issues.

## Security Posture

* **Static Analysis**: Automated security auditing via `bandit` on every push/PR.
* **Dependencies**: Monitored for vulnerabilities.
* **Supply Chain Integrity**: Commits are GPG-signed to ensure authorship authenticity.

## Supported versions

| Version | Supported |
| --- | --- |
| 0.1.x | ✅ |

This project is in early, active development (pre-1.0). Only the latest release on `main` receives fixes.

## Reporting a vulnerability

If you find a security issue in CyberReport-Pro itself (not in the sample findings data, which is intentionally illustrative), please **do not** open a public GitHub issue.

Instead:

1. Open a [GitHub Security Advisory](https://www.google.com/search?q=../../security/advisories/new) on this repository (private by default), or
2. Reach out via private message through the GitHub profile linked to this repository with a description of the issue, steps to reproduce, and potential impact.

You can expect an initial response within 7 days. This is a portfolio/learning project maintained outside working hours, so turnaround is best effort, not SLA-backed.

## Scope

In scope:

* The Python package (`src/cyberreport_pro/`): injection risks in the Jinja2 template rendering, path traversal in file handling, dependency vulnerabilities, etc.
* The CLI's handling of untrusted input files.

Out of scope:

* The illustrative content in `data/sample_findings.json` (it describes fictional vulnerabilities on purpose, as report-generation test data).
* Vulnerabilities that require modifying the tool's own source code to trigger (e.g. hardcoding a malicious template).

## What this project already does about it

* [`bandit`](https://github.com/PyCQA/bandit) runs in CI on every push, scanning `src/` for common insecure patterns.
* Jinja2 autoescaping is enabled for all HTML template rendering (see `render/pdf_generator.py`) to reduce injection risk in generated reports.
* Dependencies are pinned to minimum tested versions in `pyproject.toml`.

---
