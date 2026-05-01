from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .detector import detect_project
from .generator import generate_readme
from .scanner import scan_project

TOOLS = [
    {
        "name": "inspect_project",
        "description": "Scan a local project and return detected metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "generate_readme_draft",
        "description": "Generate a README draft for a local project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "lang": {"type": "string", "enum": ["en", "zh"]},
                "template": {"type": "string", "enum": ["minimal", "portfolio"]},
            },
            "required": ["path"],
        },
    },
]


def run_server() -> int:
    """Run a tiny JSON-RPC-like stdio server for MCP-style clients.

    This intentionally avoids third-party dependencies. It is not a full MCP SDK
    implementation yet, but it exposes a compatible tool model that can be
    adapted to the official SDK later.
    """
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
        except Exception as exc:  # noqa: BLE001 - server boundary
            response = {"error": {"message": str(exc)}}
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    return 0


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    method = request.get("method")
    request_id = request.get("id")
    params = request.get("params") or {}

    if method == "tools/list":
        return {"id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        return {"id": request_id, "result": _call_tool(name, arguments)}
    return {"id": request_id, "error": {"message": f"Unknown method: {method}"}}


def _call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    path = Path(arguments.get("path", ".")).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"path does not exist or is not a directory: {path}")

    scan = scan_project(path)
    profile = detect_project(scan)

    if name == "inspect_project":
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "project": {"name": scan.name, "root": str(scan.root)},
                            "profile": profile.to_dict(),
                            "important_files": sorted(scan.important_files),
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                }
            ]
        }
    if name == "generate_readme_draft":
        lang = arguments.get("lang", "en")
        template = arguments.get("template", "portfolio")
        readme = generate_readme(scan, profile, lang=lang, template=template)
        return {"content": [{"type": "text", "text": readme}]}
    raise ValueError(f"Unknown tool: {name}")


def main() -> int:
    return run_server()


if __name__ == "__main__":
    raise SystemExit(main())
