# Contributing

Thanks for your interest in contributing to `repo-readme-polisher`.

## Development setup

```bash
git clone https://github.com/Zeweir/repo-readme-polisher.git
cd repo-readme-polisher
python -m pip install -e .
python -m pytest
```

## Contribution ideas

Good first contributions:

- Add a new framework detector.
- Improve generated README wording.
- Add tests for another project type.
- Improve documentation or examples.

## Pull request checklist

Before opening a PR:

- [ ] The change has a clear purpose.
- [ ] Tests pass with `python -m pytest`.
- [ ] New behavior is documented if needed.
- [ ] The PR description explains the user-facing impact.

## Code style

Keep the project simple:

- Prefer standard library solutions.
- Avoid adding dependencies unless they are clearly worth it.
- Keep detectors small and easy to test.
- Do not upload or transmit user project files.
