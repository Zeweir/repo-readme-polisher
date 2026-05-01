from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    "coverage",
}

IMPORTANT_FILES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "next.config.ts",
    "requirements.txt",
    "pyproject.toml",
    "Pipfile",
    "poetry.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Dockerfile",
    "docker-compose.yml",
    "compose.yml",
    "README.md",
    ".env.example",
    "LICENSE",
}


@dataclass(frozen=True)
class ProjectScan:
    root: Path
    files: list[Path]
    dirs: list[Path]
    important_files: dict[str, Path]
    existing_readme: str | None

    @property
    def name(self) -> str:
        return self.root.name


def scan_project(root: Path, max_files: int = 500) -> ProjectScan:
    files: list[Path] = []
    dirs: list[Path] = []
    important: dict[str, Path] = {}

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.is_dir():
            dirs.append(rel)
            continue
        files.append(rel)
        if path.name in IMPORTANT_FILES:
            important[path.name] = path
        if len(files) >= max_files:
            break

    existing_readme = None
    readme_path = important.get("README.md")
    if readme_path and readme_path.exists():
        try:
            existing_readme = readme_path.read_text(encoding="utf-8")[:4000]
        except UnicodeDecodeError:
            existing_readme = readme_path.read_text(errors="ignore")[:4000]

    return ProjectScan(
        root=root,
        files=sorted(files),
        dirs=sorted(dirs),
        important_files=important,
        existing_readme=existing_readme,
    )
