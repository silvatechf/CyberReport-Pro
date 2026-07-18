# Contributing

This is a portfolio/learning project, but maintained with the same
practices I'd use on a professional project. Suggestions, issues, and
PRs are welcome — including corrections to my own reasoning on the
legal mapping, which is an area where I still have a lot to learn.

## Environment setup

```bash
git clone https://github.com/your-username/cyberreport-pro.git
cd cyberreport-pro
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Running the tests

```bash
pytest
```

## Before opening a PR

1. `ruff check .` — no lint errors.
2. `bandit -r src/` — no new security findings.
3. `pytest` — all tests passing, coverage should not drop.
4. If you add a new vulnerability category to `compliance_mapper.py`,
   include the corresponding test and, if possible, a reference to the
   legal source used (RGPD article, ENS section, etc.).

## Contribution ideas (good for fellow learners too)

- New categories in the legal mapping (e.g. XXE, SSRF, IDOR).
- Support for other compliance frameworks (e.g. ISO 27001, NIST CSF).
- Export formats besides PDF (e.g. Markdown, standalone HTML).
- Improvements to the report's visual template.
