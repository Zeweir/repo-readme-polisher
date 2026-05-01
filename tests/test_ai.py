from pathlib import Path

from repo_readme_polisher.ai import build_ai_prompt
from repo_readme_polisher.detector import detect_project
from repo_readme_polisher.generator import generate_readme
from repo_readme_polisher.scanner import scan_project


def test_ai_prompt_contains_draft_and_guardrails():
    root = Path(__file__).resolve().parents[1]
    scan = scan_project(root)
    profile = detect_project(scan)
    draft = generate_readme(scan, profile)
    prompt = build_ai_prompt(scan, profile, draft)

    assert "Do not invent features" in prompt
    assert "---BEGIN DRAFT---" in prompt
    assert "Repo Readme Polisher" in prompt
