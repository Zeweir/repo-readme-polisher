from __future__ import annotations

from .detector import ProjectProfile
from .scanner import ProjectScan


def generate_readme(scan: ProjectScan, profile: ProjectProfile, title: str | None = None) -> str:
    project_title = title or _title_from_name(scan.name)
    tree = _format_tree(scan)
    tech_stack = _bullet_list(profile.languages + profile.frameworks)
    features = _bullet_list(profile.features)
    package_managers = ", ".join(profile.package_managers)
    run_commands = "\n".join(profile.run_commands)
    test_commands = "\n".join(profile.test_commands)
    notes = "\n".join(f"- {note}" for note in profile.notes) or "- No scanner warnings."

    return f"""# {project_title}

A polished GitHub README draft generated from the local project structure.

> Replace this paragraph with a sharper one-sentence pitch: what the project does, who it is for, and why it is useful.

## Preview

Add screenshots, a GIF, or a demo link here.

## Features

{features}
- Clean project summary generated from local files
- Quick-start section prepared for GitHub visitors
- Roadmap and technical highlights ready to customize

## Tech Stack

{tech_stack}

Package manager / build tool: **{package_managers}**

## Project Structure

```text
{tree}
```

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd {scan.name}

# 2. Install dependencies
# TODO: add install command

# 3. Run the project
{run_commands}
```

## Testing

```bash
{test_commands}
```

## Environment Variables

If the project uses environment variables, create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Document required variables here:

| Name | Description | Required |
| --- | --- | --- |
| `EXAMPLE_KEY` | Replace with a real variable | No |

## Usage

Describe the main workflow here:

1. Open or run the project.
2. Complete the primary action.
3. Review the result/output.

## Technical Highlights

- Detected project languages: {", ".join(profile.languages)}
- Detected frameworks/tools: {", ".join(profile.frameworks)}
- Generated from a structure-aware scan instead of a blank template

## Scanner Notes

{notes}

## Roadmap

- [ ] Add screenshots/demo GIF
- [ ] Expand installation instructions
- [ ] Document API or CLI usage
- [ ] Add tests and CI workflow
- [ ] Polish the project description for portfolio/resume usage

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
"""


def _title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-") if part)


def _bullet_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def _format_tree(scan: ProjectScan, max_entries: int = 80) -> str:
    entries = ["."]
    paths = scan.dirs + scan.files
    for path in paths[:max_entries]:
        depth = len(path.parts) - 1
        indent = "│   " * depth
        marker = "├── "
        entries.append(f"{indent}{marker}{path.as_posix()}")
    if len(paths) > max_entries:
        entries.append(f"└── ... ({len(paths) - max_entries} more entries)")
    return "\n".join(entries)
