# Release Process

This project publishes GitHub Releases from version tags.

## Create a release

```bash
git checkout main
git pull --ff-only origin main
git tag -a v0.5.0 -m "v0.5.0"
git push origin v0.5.0
```

GitHub Actions will then:

1. Build the Python package.
2. Create a GitHub Release.
3. Attach files from `dist/`.

## Versioning

This project uses semantic versioning while it is still experimental:

- `0.x`: early feature iteration.
- Patch versions: bug fixes and documentation improvements.
- Minor versions: new CLI options, detectors, templates, or integrations.
