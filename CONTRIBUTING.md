# Contributing to OmniCOVAS

Thank you for your interest in contributing!

## Before You Start

All contributions require a signed **Contributor License Agreement (CLA)** before your pull request can be merged. This protects the project and your rights as a contributor.

When you open your first PR, you'll be asked to sign the CLA via GitHub. It takes 2 minutes.

## Development Setup

See `CLAUDE.MD` and the `OmniCOVAS_Phase1_Development_Guide.docx` for step-by-step setup instructions.

## Coding Standards

- **Python 3.11+** only
- **Type hints required** (mypy strict mode)
- **All functions documented** with docstrings
- **Tests required** for new features (pytest)
- **No blocking I/O** in async code

## Code Quality Gates

Before committing, run:
```bash
ruff check omnicovas/
ruff format omnicovas/
mypy omnicovas/
pytest
```

All must pass. GitHub Actions CI will also run these checks on every push.

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run code quality gates (see above)
5. Commit: `git commit -m "Clear, descriptive message"`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request
8. Sign the CLA when prompted
9. Address any review feedback

## Questions?

Open an issue on GitHub or ask in discussions.

Thanks for contributing!
