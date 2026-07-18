.PHONY: install dev test lint typecheck security demo clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy src/

security:
	bandit -r src/ -q

check: lint typecheck security test  ## Runs everything CI runs, locally

demo:
	mkdir -p output
	cyberreport-pro generate data/sample_findings.json -o output/report.pdf
	@echo "Report generated at output/report.pdf"

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage output
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
