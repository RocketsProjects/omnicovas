"""
tests.test_placeholder

Placeholder test to verify pytest is configured correctly.
Will be replaced by real tests as components are built in Phase 1.

Related to: Phase 1 Week 1 - Tooling Configuration
"""


def test_pytest_is_working() -> None:
    """
    Verify pytest discovers and runs tests.

    This is a sanity check test. It should always pass.
    Its purpose is to confirm the testing infrastructure works:
        - pytest discovers tests in the tests/ directory
        - pyproject.toml [tool.pytest.ini_options] is correctly configured
        - GitHub Actions CI can run tests successfully
    """
    assert True
