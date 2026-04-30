powershell -NoProfile -Command "@'
# Automated Gates

Date: 2026-04-30

## Results

| Gate | Status | Evidence |
|---|---:|---|
| Ruff format check | PASS | logs/ruff_format_check.txt |
| Ruff lint check | PASS | logs/ruff_check.txt |
| MyPy | PASS | logs/mypy.txt |
| Pytest | PASS — 326 passed, 2 skipped | logs/pytest.txt |
| Cargo check | PASS | logs/cargo_check.txt |
| npm build | PASS | logs/npm_build.txt |

## Notes

Automated Phase 4 live retest baseline is green.

Captured results:
- Ruff format: 80 files already formatted.
- Ruff lint: all checks passed.
- MyPy: no issues found in 45 source files.
- Pytest: 326 passed, 2 skipped.
- Cargo check: finished successfully.
- npm build: completed without detected error output.

## Verdict

PASS.
'@ | Set-Content -Encoding UTF8 $env:RETEST\automated_gates.md"
