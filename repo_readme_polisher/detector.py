from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from .scanner import ProjectScan


@dataclass(frozen=True)
class ProjectProfile:
    languages: list[str]
    frameworks: list[str]
    package_managers: list[str]
    run_commands: list[str]
    test_commands: list[str]
    features: list[str]
    notes: list[str] = field(default_factory=list)


def detect_project(scan: ProjectScan) -> ProjectProfile:
    languages: set[str] = set()
    frameworks: set[str] = set()
    package_managers: set[str] = set()
    run_commands: list[str] = []
    test_commands: list[str] = []
    features: set[str] = set()
    notes: list[str] = []

    suffixes = {file.suffix.lower() for file in scan.files}
    if ".py" in suffixes:
        languages.add("Python")
    if suffixes & {".js", ".jsx", ".ts", ".tsx"}:
        languages.add("JavaScript/TypeScript")
    if ".java" in suffixes:
        languages.add("Java")
    if suffixes & {".vue"}:
        languages.add("Vue")
    if suffixes & {".go"}:
        languages.add("Go")

    if "pyproject.toml" in scan.important_files:
        package_managers.add("pip / build backend")
        run_commands.append("python -m <module>")
        test_commands.append("python -m pytest")
    if "requirements.txt" in scan.important_files:
        package_managers.add("pip")
        run_commands.append("pip install -r requirements.txt")
    if "package.json" in scan.important_files:
        package_managers.add(_detect_js_package_manager(scan))
        _read_package_json(scan, frameworks, run_commands, test_commands, notes)
    if "pom.xml" in scan.important_files:
        package_managers.add("Maven")
        frameworks.add("Spring Boot" if _pom_contains(scan, "spring-boot") else "Java")
        run_commands.append("mvn spring-boot:run")
        test_commands.append("mvn test")
    if "build.gradle" in scan.important_files or "build.gradle.kts" in scan.important_files:
        package_managers.add("Gradle")
        run_commands.append("./gradlew bootRun")
        test_commands.append("./gradlew test")
    if "Dockerfile" in scan.important_files:
        features.add("Dockerized runtime")
    if "docker-compose.yml" in scan.important_files or "compose.yml" in scan.important_files:
        features.add("Docker Compose setup")
    if ".env.example" in scan.important_files:
        features.add("Environment-based configuration")
    if "LICENSE" in scan.important_files:
        features.add("Open-source license included")

    if any(str(file).startswith("tests") or str(file).startswith("test") for file in scan.files):
        features.add("Test directory present")
    if any("api" in file.parts for file in scan.files):
        features.add("API-oriented structure")
    if any("components" in file.parts for file in scan.files):
        features.add("Component-based frontend structure")

    return ProjectProfile(
        languages=sorted(languages) or ["Unknown"],
        frameworks=sorted(frameworks) or ["Not detected yet"],
        package_managers=sorted(package_managers) or ["Not detected yet"],
        run_commands=_dedupe(run_commands) or ["# Add your run command here"],
        test_commands=_dedupe(test_commands) or ["# Add your test command here"],
        features=sorted(features) or ["Local project structure analysis"],
        notes=notes,
    )


def _detect_js_package_manager(scan: ProjectScan) -> str:
    if "pnpm-lock.yaml" in scan.important_files:
        return "pnpm"
    if "yarn.lock" in scan.important_files:
        return "yarn"
    if "package-lock.json" in scan.important_files:
        return "npm"
    return "npm / pnpm / yarn"


def _read_package_json(scan: ProjectScan, frameworks: set[str], run_commands: list[str], test_commands: list[str], notes: list[str]) -> None:
    path = scan.important_files["package.json"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - best effort scanner
        notes.append(f"Could not parse package.json: {exc}")
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    dep_names = set(deps)
    if "react" in dep_names:
        frameworks.add("React")
    if "vue" in dep_names:
        frameworks.add("Vue")
    if "vite" in dep_names:
        frameworks.add("Vite")
    if "next" in dep_names:
        frameworks.add("Next.js")
    if "express" in dep_names:
        frameworks.add("Express")
    if "fastify" in dep_names:
        frameworks.add("Fastify")
    if "tailwindcss" in dep_names:
        frameworks.add("Tailwind CSS")

    scripts = data.get("scripts", {})
    if "dev" in scripts:
        run_commands.append("npm run dev")
    if "start" in scripts:
        run_commands.append("npm start")
    if "test" in scripts:
        test_commands.append("npm test")
    if "build" in scripts:
        test_commands.append("npm run build")


def _pom_contains(scan: ProjectScan, keyword: str) -> bool:
    try:
        text = scan.important_files["pom.xml"].read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    try:
        ET.fromstring(text)
    except ET.ParseError:
        pass
    return bool(re.search(re.escape(keyword), text, re.IGNORECASE))


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output
