# MCP Integration

`repo-readme-polisher` includes a lightweight stdio tool server that can be adapted for MCP-compatible agent clients.

> Status: experimental. The current implementation intentionally avoids runtime dependencies and exposes a small JSON-RPC-like interface. A future version may migrate to the official MCP Python SDK.

## Start the server

```bash
python -m repo_readme_polisher.mcp_server
```

## List tools

Send one JSON request per line:

```json
{"id":1,"method":"tools/list","params":{}}
```

## Inspect a project

```json
{"id":2,"method":"tools/call","params":{"name":"inspect_project","arguments":{"path":"."}}}
```

## Generate a README draft

```json
{"id":3,"method":"tools/call","params":{"name":"generate_readme_draft","arguments":{"path":".","lang":"en","template":"portfolio"}}}
```

## Tools

- `inspect_project`: returns detected project metadata.
- `generate_readme_draft`: returns a README draft as Markdown.

## Why this exists

The CLI is useful for humans. The server mode is useful for agents: an assistant can inspect a repository and generate a README draft without scraping shell output.
