# Security Policy

`repo-readme-polisher` is intended to run locally and inspect project metadata.

## Supported versions

Security fixes are currently applied to the latest version on the `main` branch.

## Reporting a vulnerability

Please do not open a public issue for sensitive security reports.

If you find a vulnerability, contact the maintainer privately or open a minimal report that does not expose secrets or exploit details.

## Security expectations

The tool should not:

- Upload project files to external services.
- Read files outside the requested project directory intentionally.
- Include secrets from `.env` files in generated README output.
- Execute code from the scanned project.

If you notice behavior that violates these expectations, please report it.
