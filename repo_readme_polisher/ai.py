from __future__ import annotations

from .detector import ProjectProfile
from .scanner import ProjectScan


def build_ai_prompt(scan: ProjectScan, profile: ProjectProfile, draft: str) -> str:
    return f"""You are improving a GitHub README for a software project.

Project name: {scan.name}
Detected languages: {", ".join(profile.languages)}
Detected frameworks/tools: {", ".join(profile.frameworks)}
Detected databases: {", ".join(profile.databases)}
Detected deployment hints: {", ".join(profile.deployment)}

Requirements:
- Keep the README honest and technically accurate.
- Make the opening description specific and compelling.
- Preserve install/run/test commands if they are correct.
- Add concise technical highlights.
- Do not invent features that are not implied by the project structure.
- Keep secrets, tokens, and private paths out of the final README.

Current generated draft:

---BEGIN DRAFT---
{draft}
---END DRAFT---

Return an improved README in Markdown.
"""
