from __future__ import annotations

from .detector import ProjectProfile
from .scanner import ProjectScan


def generate_readme(scan: ProjectScan, profile: ProjectProfile, title: str | None = None, lang: str = "en", template: str = "portfolio") -> str:
    if lang == "zh":
        return _generate_zh(scan, profile, title, template)
    return _generate_en(scan, profile, title, template)


def _generate_en(scan: ProjectScan, profile: ProjectProfile, title: str | None, template: str) -> str:
    project_title = title or _title_from_name(scan.name)
    tree = _format_tree(scan)
    compact = template == "minimal"
    extra = "" if compact else f"""
## Architecture

```mermaid
flowchart TD
    A[User] --> B[Application]
    B --> C[Core Features]
    C --> D[Output]
```

## Technical Highlights

- Detected languages: {", ".join(profile.languages)}
- Detected frameworks/tools: {", ".join(profile.frameworks)}
- Detected databases: {", ".join(profile.databases)}
- Deployment hints: {", ".join(profile.deployment)}
- Generated from a structure-aware scan instead of a blank template

## Roadmap

- [ ] Add screenshots/demo GIF
- [ ] Expand installation instructions
- [ ] Document API or CLI usage
- [ ] Add tests and CI workflow
- [ ] Polish the project description for portfolio/resume usage
"""
    return f"""# {project_title}

A polished GitHub README draft generated from the local project structure.

> Replace this paragraph with a sharper one-sentence pitch: what the project does, who it is for, and why it is useful.

## Preview

Add screenshots, a GIF, or a demo link here.

## Features

{_bullet_list(profile.features)}
- Clean project summary generated from local files
- Quick-start section prepared for GitHub visitors

## Tech Stack

| Category | Detected |
| --- | --- |
| Languages | {", ".join(profile.languages)} |
| Frameworks | {", ".join(profile.frameworks)} |
| Package/build tools | {", ".join(profile.package_managers)} |
| Databases | {", ".join(profile.databases)} |
| Testing | {", ".join(profile.test_tools)} |
| Deployment | {", ".join(profile.deployment)} |

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
{chr(10).join(profile.run_commands)}
```

## Testing

```bash
{chr(10).join(profile.test_commands)}
```

## Environment Variables

If the project uses environment variables, create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

{extra}
## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
"""


def _generate_zh(scan: ProjectScan, profile: ProjectProfile, title: str | None, template: str) -> str:
    project_title = title or _title_from_name(scan.name)
    tree = _format_tree(scan)
    compact = template == "minimal"
    extra = "" if compact else f"""
## 架构

```mermaid
flowchart TD
    A[用户] --> B[应用]
    B --> C[核心功能]
    C --> D[输出结果]
```

## 技术亮点

- 检测到的语言：{", ".join(profile.languages)}
- 检测到的框架/工具：{", ".join(profile.frameworks)}
- 检测到的数据库：{", ".join(profile.databases)}
- 部署线索：{", ".join(profile.deployment)}
- 基于项目结构生成，而不是空白模板

## 路线图

- [ ] 添加截图或演示 GIF
- [ ] 完善安装说明
- [ ] 补充 API 或 CLI 使用文档
- [ ] 添加测试和 CI 工作流
- [ ] 优化成适合作品集/简历展示的项目描述
"""
    return f"""# {project_title}

一份根据本地项目结构生成的 GitHub README 草稿。

> 请把这段替换成更准确的一句话介绍：这个项目做什么、给谁用、为什么有用。

## 预览

在这里添加截图、GIF 或在线演示链接。

## 功能

{_bullet_list(profile.features)}
- 根据本地文件生成项目摘要
- 生成适合 GitHub 访问者阅读的快速开始章节

## 技术栈

| 类别 | 检测结果 |
| --- | --- |
| 语言 | {", ".join(profile.languages)} |
| 框架 | {", ".join(profile.frameworks)} |
| 包管理/构建工具 | {", ".join(profile.package_managers)} |
| 数据库 | {", ".join(profile.databases)} |
| 测试 | {", ".join(profile.test_tools)} |
| 部署 | {", ".join(profile.deployment)} |

## 项目结构

```text
{tree}
```

## 快速开始

```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd {scan.name}

# 2. 安装依赖
# TODO: 添加安装命令

# 3. 运行项目
{chr(10).join(profile.run_commands)}
```

## 测试

```bash
{chr(10).join(profile.test_commands)}
```

## 环境变量

如果项目使用环境变量，可以从 `.env.example` 创建 `.env`：

```bash
cp .env.example .env
```

{extra}
## 许可证

本项目基于 MIT License 开源。详见 [LICENSE](LICENSE)。
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
