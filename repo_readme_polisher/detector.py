from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field

from .scanner import ProjectScan


@dataclass(frozen=True)
class ProjectProfile:
    languages: list[str]
    frameworks: list[str]
    package_managers: list[str]
    databases: list[str]
    test_tools: list[str]
    deployment: list[str]
    run_commands: list[str]
    test_commands: list[str]
    features: list[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def detect_project(scan: ProjectScan) -> ProjectProfile:
    languages: set[str] = set()
    frameworks: set[str] = set()
    package_managers: set[str] = set()
    databases: set[str] = set()
    test_tools: set[str] = set()
    deployment: set[str] = set()
    run_commands: list[str] = []
    test_commands: list[str] = []
    features: set[str] = set()
    notes: list[str] = []

    suffixes = {file.suffix.lower() for file in scan.files}
    file_names = {file.name for file in scan.files}
    path_text = "\n".join(file.as_posix().lower() for file in scan.files)

    if ".py" in suffixes:
        languages.add("Python")
    if suffixes & {".js", ".jsx", ".ts", ".tsx"}:
        languages.add("JavaScript/TypeScript")
    if ".java" in suffixes:
        languages.add("Java")
    if ".vue" in suffixes:
        languages.add("Vue")
    if ".go" in suffixes:
        languages.add("Go")

    if "pyproject.toml" in scan.important_files:
        package_managers.add("pip / build backend")
        pyproject = _read_text(scan, "pyproject.toml")
        _detect_python_metadata(pyproject, frameworks, databases, test_tools, run_commands, test_commands)
    if "requirements.txt" in scan.important_files:
        package_managers.add("pip")
        requirements = _read_text(scan, "requirements.txt")
        _detect_python_requirements(requirements, frameworks, databases, test_tools)
        run_commands.append("pip install -r requirements.txt")
    if "package.json" in scan.important_files:
        package_managers.add(_detect_js_package_manager(scan))
        _read_package_json(scan, frameworks, databases, test_tools, run_commands, test_commands, notes)
    if "pom.xml" in scan.important_files:
        package_managers.add("Maven")
        pom = _read_text(scan, "pom.xml")
        _detect_java_metadata(pom, frameworks, databases, test_tools)
        run_commands.append("mvn spring-boot:run" if "Spring Boot" in frameworks else "mvn exec:java")
        test_commands.append("mvn test")
    if "build.gradle" in scan.important_files or "build.gradle.kts" in scan.important_files:
        package_managers.add("Gradle")
        gradle_name = "build.gradle" if "build.gradle" in scan.important_files else "build.gradle.kts"
        gradle = _read_text(scan, gradle_name)
        _detect_java_metadata(gradle, frameworks, databases, test_tools)
        run_commands.append("./gradlew bootRun" if "Spring Boot" in frameworks else "./gradlew run")
        test_commands.append("./gradlew test")

    if "Dockerfile" in scan.important_files:
        deployment.add("Docker")
        features.add("Dockerized runtime")
    if "docker-compose.yml" in scan.important_files or "compose.yml" in scan.important_files:
        deployment.add("Docker Compose")
        features.add("Docker Compose setup")
    if any(name.startswith("vercel") for name in file_names):
        deployment.add("Vercel")
    if any("nginx" in part.lower() for file in scan.files for part in file.parts):
        deployment.add("Nginx")
    if ".env.example" in scan.important_files:
        features.add("Environment-based configuration")
    if "LICENSE" in scan.important_files:
        features.add("Open-source license included")

    if any(str(file).startswith("tests") or str(file).startswith("test") for file in scan.files):
        features.add("Test directory present")
    if "pytest" in path_text:
        test_tools.add("pytest")
    if any(name in file_names for name in {"jest.config.js", "jest.config.ts"}):
        test_tools.add("Jest")
    if any(name in file_names for name in {"vitest.config.js", "vitest.config.ts"}):
        test_tools.add("Vitest")
    if any("api" in file.parts for file in scan.files):
        features.add("API-oriented structure")
    if any("components" in file.parts for file in scan.files):
        features.add("Component-based frontend structure")

    return ProjectProfile(
        languages=sorted(languages) or ["Unknown"],
        frameworks=sorted(frameworks) or ["Not detected yet"],
        package_managers=sorted(package_managers) or ["Not detected yet"],
        databases=sorted(databases) or ["Not detected yet"],
        test_tools=sorted(test_tools) or ["Not detected yet"],
        deployment=sorted(deployment) or ["Not detected yet"],
        run_commands=_dedupe(run_commands) or ["# Add your run command here"],
        test_commands=_dedupe(test_commands) or ["# Add your test command here"],
        features=sorted(features) or ["Local project structure analysis"],
        notes=notes,
    )


def _read_text(scan: ProjectScan, file_name: str) -> str:
    path = scan.important_files.get(file_name)
    if not path:
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def _detect_python_metadata(text: str, frameworks: set[str], databases: set[str], test_tools: set[str], run_commands: list[str], test_commands: list[str]) -> None:
    lower = text.lower()
    _detect_python_requirements(lower, frameworks, databases, test_tools)
    if "pytest" in lower:
        test_commands.append("python -m pytest")
    run_commands.append("python -m <module>")


def _detect_python_requirements(text: str, frameworks: set[str], databases: set[str], test_tools: set[str]) -> None:
    lower = text.lower()
    tokens = set(re.findall(r"[a-z0-9_.-]+", lower))
    if "fastapi" in tokens:
        frameworks.add("FastAPI")
    if "flask" in tokens:
        frameworks.add("Flask")
    if "django" in tokens:
        frameworks.add("Django")
    if "typer" in tokens:
        frameworks.add("Typer")
    if "click" in tokens:
        frameworks.add("Click")
    if "pytest" in tokens:
        test_tools.add("pytest")
    if tokens & {"sqlalchemy", "psycopg2", "asyncpg"}:
        databases.add("PostgreSQL / SQLAlchemy")
    if tokens & {"pymysql", "mysqlclient"}:
        databases.add("MySQL")
    if tokens & {"redis"}:
        databases.add("Redis")
    if tokens & {"pymongo", "motor"}:
        databases.add("MongoDB")
    if tokens & {"chromadb", "faiss-cpu", "lancedb"}:
        databases.add("Vector database")


def _detect_js_package_manager(scan: ProjectScan) -> str:
    if "pnpm-lock.yaml" in scan.important_files:
        return "pnpm"
    if "yarn.lock" in scan.important_files:
        return "yarn"
    if "package-lock.json" in scan.important_files:
        return "npm"
    return "npm / pnpm / yarn"


def _read_package_json(scan: ProjectScan, frameworks: set[str], databases: set[str], test_tools: set[str], run_commands: list[str], test_commands: list[str], notes: list[str]) -> None:
    path = scan.important_files["package.json"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - best effort scanner
        notes.append(f"Could not parse package.json: {exc}")
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    dep_names = set(deps)
    mapping = {
        "react": "React",
        "vue": "Vue",
        "vite": "Vite",
        "next": "Next.js",
        "express": "Express",
        "fastify": "Fastify",
        "tailwindcss": "Tailwind CSS",
        "@nestjs/core": "NestJS",
    }
    for dep, label in mapping.items():
        if dep in dep_names:
            frameworks.add(label)
    if dep_names & {"mysql2", "mysql"}:
        databases.add("MySQL")
    if dep_names & {"pg", "postgres"}:
        databases.add("PostgreSQL")
    if dep_names & {"redis", "ioredis"}:
        databases.add("Redis")
    if dep_names & {"mongodb", "mongoose"}:
        databases.add("MongoDB")
    if dep_names & {"jest"}:
        test_tools.add("Jest")
    if dep_names & {"vitest"}:
        test_tools.add("Vitest")
    if dep_names & {"playwright", "@playwright/test"}:
        test_tools.add("Playwright")

    scripts = data.get("scripts", {})
    if "dev" in scripts:
        run_commands.append("npm run dev")
    if "start" in scripts:
        run_commands.append("npm start")
    if "test" in scripts:
        test_commands.append("npm test")
    if "build" in scripts:
        test_commands.append("npm run build")


def _detect_java_metadata(text: str, frameworks: set[str], databases: set[str], test_tools: set[str]) -> None:
    lower = text.lower()
    try:
        ET.fromstring(text)
    except ET.ParseError:
        pass
    if "spring-boot" in lower:
        frameworks.add("Spring Boot")
    if "junit" in lower:
        test_tools.add("JUnit")
    if "mysql" in lower:
        databases.add("MySQL")
    if "postgresql" in lower:
        databases.add("PostgreSQL")
    if "redis" in lower:
        databases.add("Redis")
    if "mongodb" in lower:
        databases.add("MongoDB")


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output
