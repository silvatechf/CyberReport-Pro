import json

import pytest

from cyberreport_pro.core.loader import FindingsFileError, load_report_from_json


def test_load_valid_sample_file():
    report = load_report_from_json("data/sample_findings.json")

    assert report.metadata.client_name == "Acme Retail S.A."
    assert len(report.mapped_findings) == 5


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_report_from_json("data/file_does_not_exist.json")


def test_missing_top_level_key_raises_findings_file_error(tmp_path):
    payload = {"client_name": "X", "project_name": "Y", "findings": []}
    bad_file = tmp_path / "bad.json"
    bad_file.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(FindingsFileError, match="author"):
        load_report_from_json(bad_file)


def test_empty_findings_list_raises_error(tmp_path):
    payload = {
        "client_name": "X",
        "project_name": "Y",
        "author": "Z",
        "findings": [],
    }
    bad_file = tmp_path / "empty.json"
    bad_file.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(FindingsFileError, match="non-empty"):
        load_report_from_json(bad_file)


def test_incomplete_finding_raises_error(tmp_path):
    payload = {
        "client_name": "X",
        "project_name": "Y",
        "author": "Z",
        "findings": [{"id": "F-1", "title": "missing other fields"}],
    }
    bad_file = tmp_path / "incomplete.json"
    bad_file.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(FindingsFileError, match="incomplete"):
        load_report_from_json(bad_file)
