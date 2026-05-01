from pathlib import Path

from repo_readme_polisher.detector import detect_project
from repo_readme_polisher.generator import generate_readme
from repo_readme_polisher.scanner import scan_project


def test_scan_and_generate_current_project():
    root = Path(__file__).resolve().parents[1]
    scan = scan_project(root)
    profile = detect_project(scan)
    readme = generate_readme(scan, profile)

    assert "# Repo Readme Polisher" in readme
    assert "## Quick Start" in readme
    assert "Python" in readme
