from __future__ import annotations

import argparse
import json
from pathlib import Path

from .detector import detect_project
from .ai import build_ai_prompt
from .generator import generate_readme
from .scanner import scan_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-readme-polisher",
        description="Scan a local project and generate a polished GitHub README draft.",
    )
    parser.add_argument("project", nargs="?", default=".", help="Path to the project directory to scan. Defaults to the current directory.")
    parser.add_argument("-o", "--output", default="README_DRAFT.md", help="Output README draft path. Defaults to README_DRAFT.md in the current working directory.")
    parser.add_argument("--title", default=None, help="Override the generated project title.")
    parser.add_argument("--stdout", action="store_true", help="Print the generated README to stdout instead of writing a file.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format. Use json to inspect detected project metadata.")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="README language for markdown output.")
    parser.add_argument("--template", choices=["minimal", "portfolio"], default="portfolio", help="README template style.")
    parser.add_argument("--ai", action="store_true", help="Prepare an AI rewrite prompt next to the generated README. This does not call external APIs yet.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    project_path = Path(args.project).expanduser().resolve()
    if not project_path.exists() or not project_path.is_dir():
        parser.error(f"project path does not exist or is not a directory: {project_path}")

    scan = scan_project(project_path)
    profile = detect_project(scan)

    if args.format == "json":
        payload = {
            "project": {"name": scan.name, "root": str(scan.root)},
            "profile": profile.to_dict(),
            "important_files": sorted(scan.important_files),
        }
        output = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        output = generate_readme(scan, profile, title=args.title, lang=args.lang, template=args.template)

    if args.stdout or args.format == "json":
        print(output)
        return 0

    output_path = Path(args.output).expanduser()
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path
    output_path.write_text(output, encoding="utf-8")
    print(f"README draft written to {output_path}")
    if args.ai:
        prompt_path = output_path.with_suffix(output_path.suffix + ".ai-prompt.md")
        prompt_path.write_text(build_ai_prompt(scan, profile, output), encoding="utf-8")
        print(f"AI rewrite prompt written to {prompt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

