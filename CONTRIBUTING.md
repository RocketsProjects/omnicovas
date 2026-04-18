# Contributing to OmniCOVAS

Thank you for your interest in contributing. This project is built on a constitutional framework, and contributions are most welcome when they work within that framework.

## Before You Start

Every contribution requires a signed **Contributor License Agreement** (CLA) before it can be merged. The CLA is electronic and takes about two minutes — when you open your first pull request, a bot will prompt you automatically.

See `CLA.md` for the full CLA text.

## Read These First

Before making non-trivial changes, please read:

- `README.md` — what OmniCOVAS is and why it exists
- `OmniCOVAS_Master_Blueprint_v4_0.txt` — the Ten Laws, Ten Architectural Principles, and tech stack
- `OmniCOVAS_Roadmap.txt` — feature priorities and release planning
- `CLAUDE.MD` — engineering operational parameters

Every pull request is evaluated against the Ten Laws and Ten Architectural Principles. Features that conflict with the constitution will not be accepted, regardless of code quality.

## Development Setup

OmniCOVAS v1.0 targets Windows 10/11 only.

Required tooling:

- Git
- Python 3.11 (pinned — do not use 3.12 or 3.13)
- `uv` (Python package manager): `pip install uv`
- Node.js LTS
- Rust toolchain (via `rustup`)
- Microsoft C++ Build Tools
- VS Code recommended with extensions: Python, Rust Analyzer, Tauri, GitLens

Project setup:

```bash
git clone https://github.com/RocketsProjects/omnicovas.git
cd omnicovas
uv venv --python 3.11
.venv\Scripts\activate
uv sync --all-extras
pre-commit install
```

Verify the environment:

```bash
pytest
```

All tests should pass on a fresh clone.

## Coding Standards

- **Python 3.11 only.** Syntax or stdlib features newer than 3.11 are not permitted.
- **Full type hints.** Every function signature is annotated. `mypy --strict` runs in CI and must pass.
- **Async-first.** Core code is `async def`. No blocking I/O in the event loop.
- **Docstrings required** on every public class and function, referencing the relevant Law or Principle where appropriate.
- **Tests required** for any non-trivial logic.
- **No direct AI provider calls.** AI access goes through the `AIProvider` interface (Law 4).
- **No silent data flows.** Every outbound request is logged and opt-in gated.
- **No game automation.** Every AI suggestion passes through the Confirmation Gate (Law 1).

## Code Quality Gates

Before committing, run locally:

```bash
ruff check omnicovas/ tests/
ruff format omnicovas/ tests/
mypy omnicovas/
pytest
```

All four must pass. Pre-commit hooks run these automatically when you commit.

GitHub Actions CI runs the same checks on every push and pull request. Pull requests cannot be merged with red CI.

## Submitting Changes

1. **Open an issue first** for anything beyond a small bugfix. This avoids wasted work on changes that conflict with the roadmap or constitution.
2. **Fork and branch.** Branch names: `feature/...`, `fix/...`, `docs/...`
3. **Keep commits focused.** One logical change per commit where possible.
4. **Write clear commit messages.** First line ≤ 72 chars, imperative mood ("Add X", not "Added X").
5. **Run the quality gates locally** before pushing.
6. **Open a pull request** against `main`. Link the issue it addresses.
7. **Sign the CLA** when prompted.
8. **Respond to review feedback.** Reviewers may ask for changes to align with the constitution — this is normal.

## What Gets Merged

- Bugfixes with a regression test ✓
- Documentation improvements ✓
- Performance improvements with before/after measurements ✓
- New features that align with the roadmap and pass the Ten Laws ✓
- Refactors that improve clarity without changing behavior ✓

## What Doesn't Get Merged

- Changes that violate any of the Ten Laws
- Features not on the roadmap (open an issue for discussion first)
- Bundling or redistributing third-party software
- Anything that automates in-game actions or bypasses the Confirmation Gate
- Features gated behind a paywall
- Telemetry or analytics reporting back to maintainers
- Changes that add blocking I/O to the event loop

## Questions

Open a GitHub Issue or Discussion. Please be patient — this is a volunteer project.

Fly safely.
