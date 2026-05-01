from pathlib import Path

from repo_readme_polisher.mcp_server import handle_request


def test_mcp_list_tools():
    response = handle_request({"id": 1, "method": "tools/list", "params": {}})
    tools = response["result"]["tools"]
    assert {tool["name"] for tool in tools} == {"inspect_project", "generate_readme_draft"}


def test_mcp_generate_readme_draft():
    root = Path(__file__).resolve().parents[1]
    response = handle_request(
        {
            "id": 2,
            "method": "tools/call",
            "params": {"name": "generate_readme_draft", "arguments": {"path": str(root), "lang": "en"}},
        }
    )
    text = response["result"]["content"][0]["text"]
    assert "# Repo Readme Polisher" in text
