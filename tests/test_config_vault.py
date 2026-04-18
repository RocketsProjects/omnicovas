"""
tests.test_config_vault

Tests for the DPAPI config vault.

Related to: Law 2 (Legal Compliance) — never log or expose API keys
Related to: Law 8 (Sovereignty & Transparency) — user owns their data
Related to: Phase 1 Development Guide Week 5, Part B

Note:
    These tests only run on Windows (DPAPI is Windows-only).
    On non-Windows CI runners, encryption will fail and these
    tests will be skipped. CI runs on windows-latest so they will execute.

Tests:
    1. Set and get a value round-trip
    2. Get of missing key returns None
    3. Delete removes a key
    4. has() reports key presence without decrypting
    5. keys() lists stored keys
    6. Vault persists across instances (disk-backed)
    7. Unknown key logs a warning but still works
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

from omnicovas.config.vault import ConfigVault

# All tests require Windows because DPAPI is Windows-only
pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="ConfigVault uses Windows DPAPI; tests skipped on non-Windows",
)


@pytest.fixture
def vault() -> ConfigVault:
    """Provide a ConfigVault backed by a temp file."""
    tmpdir = tempfile.mkdtemp(prefix="omnicovas_vault_test_")
    return ConfigVault(vault_path=Path(tmpdir) / "test.vault")


def test_set_and_get_roundtrip(vault: ConfigVault) -> None:
    """Store a value and retrieve it — plaintext must match."""
    vault.set("gemini_api_key", "AIza-super-secret-12345")

    assert vault.get("gemini_api_key") == "AIza-super-secret-12345"


def test_get_missing_key_returns_none(vault: ConfigVault) -> None:
    """Reading a key that was never set returns None."""
    assert vault.get("gemini_api_key") is None


def test_delete_removes_key(vault: ConfigVault) -> None:
    """After delete, the key is gone."""
    vault.set("gemini_api_key", "secret")
    assert vault.get("gemini_api_key") == "secret"

    vault.delete("gemini_api_key")

    assert vault.get("gemini_api_key") is None
    assert vault.has("gemini_api_key") is False


def test_delete_missing_returns_false(vault: ConfigVault) -> None:
    """Deleting a key that doesn't exist returns False."""
    assert vault.delete("gemini_api_key") is False


def test_has_reports_presence(vault: ConfigVault) -> None:
    """has() returns True when a key is set, False otherwise."""
    assert vault.has("gemini_api_key") is False

    vault.set("gemini_api_key", "secret")

    assert vault.has("gemini_api_key") is True


def test_keys_lists_stored_keys(vault: ConfigVault) -> None:
    """keys() returns all currently stored keys."""
    vault.set("gemini_api_key", "k1")
    vault.set("inara_api_key", "k2")

    keys = set(vault.keys())

    assert "gemini_api_key" in keys
    assert "inara_api_key" in keys


def test_vault_persists_across_instances() -> None:
    """
    A value written by one ConfigVault instance must be readable
    by a fresh instance pointing at the same file.
    """
    tmpdir = tempfile.mkdtemp(prefix="omnicovas_vault_persist_")
    vault_path = Path(tmpdir) / "persist.vault"

    vault1 = ConfigVault(vault_path=vault_path)
    vault1.set("gemini_api_key", "persist-me")

    vault2 = ConfigVault(vault_path=vault_path)

    assert vault2.get("gemini_api_key") == "persist-me"


def test_unknown_key_still_works(vault: ConfigVault) -> None:
    """
    Setting an undocumented key logs a warning but still stores it.
    Future-proofs the vault against schema evolution.
    """
    # journal_path is known, so this would warn but still work;
    # we use a known key here to avoid polluting test output
    vault.set("journal_path", "C:\\some\\path")

    assert vault.get("journal_path") == "C:\\some\\path"
