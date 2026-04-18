"""
tests.test_ai_providers

Tests for the AI provider abstraction layer.

Related to: Law 4 (AI Provider Agnosticism) — swappable providers
Related to: Law 5 (Zero Hallucination) — None is always a valid return
Related to: Law 6 (Performance Priority) — providers never crash the loop
Related to: Phase 1 Development Guide Week 4, Part A

Tests:
    1. NullProvider always returns None from query()
    2. NullProvider is always available
    3. NullProvider has the expected name
    4. Factory returns NullProvider for 'null' type
    5. Factory returns NullProvider when Gemini requested without api_key
    6. Factory returns NullProvider for unknown type
    7. Factory returns GeminiProvider for 'gemini' with api_key
    8. GeminiProvider with bad key returns None gracefully (never raises)
    9. GeminiProvider caches responses (same prompt = same cache key)
"""

from __future__ import annotations

import pytest

from omnicovas.ai.factory import get_provider
from omnicovas.ai.gemini_provider import GeminiProvider
from omnicovas.ai.null_provider import NullProvider


@pytest.mark.asyncio
async def test_null_provider_always_returns_none() -> None:
    """NullProvider.query must always return None regardless of input."""
    provider = NullProvider()

    assert await provider.query("anything") is None
    assert await provider.query("", context={"foo": "bar"}) is None
    assert await provider.query("a very long prompt " * 100) is None


@pytest.mark.asyncio
async def test_null_provider_is_always_available() -> None:
    """NullProvider must always report as available — no dependencies."""
    provider = NullProvider()
    assert await provider.is_available() is True


def test_null_provider_name() -> None:
    """NullProvider name must be recognizable for logs and UI."""
    assert NullProvider().name() == "NullProvider"


def test_factory_null_type() -> None:
    """Factory returns NullProvider for 'null'."""
    provider = get_provider("null")
    assert isinstance(provider, NullProvider)


def test_factory_gemini_without_key_falls_back() -> None:
    """
    Law 4: If Gemini is requested but no key is configured,
    fall back to NullProvider rather than crashing.
    """
    provider = get_provider("gemini", api_key=None)
    assert isinstance(provider, NullProvider)


def test_factory_unknown_type_falls_back() -> None:
    """Factory returns NullProvider for unknown provider types."""
    provider = get_provider("unicorn-9000")
    assert isinstance(provider, NullProvider)


def test_factory_case_insensitive() -> None:
    """Factory handles capitalization gracefully."""
    assert isinstance(get_provider("NULL"), NullProvider)
    assert isinstance(get_provider(" null "), NullProvider)


def test_factory_gemini_with_key() -> None:
    """Factory returns GeminiProvider when key is provided."""
    provider = get_provider("gemini", api_key="test-key-not-real")
    assert isinstance(provider, GeminiProvider)
    assert "Gemini" in provider.name()


@pytest.mark.asyncio
async def test_gemini_bad_key_returns_none_not_raises() -> None:
    """
    Law 6: Provider failures must return None, never raise.
    Using an obviously-invalid key triggers initialization failure,
    which must be handled silently.
    """
    provider = GeminiProvider(api_key="not-a-real-key-should-fail")

    result = await provider.query("test prompt")

    assert result is None


def test_gemini_cache_key_is_deterministic() -> None:
    """
    Same prompt must produce the same cache key — required for cache hits.
    """
    provider = GeminiProvider(api_key="test")
    key1 = provider._cache_key("Hello world")
    key2 = provider._cache_key("Hello world")
    key3 = provider._cache_key("Different prompt")

    assert key1 == key2
    assert key1 != key3


def test_gemini_cache_put_and_get() -> None:
    """Cache stores and retrieves values within TTL."""
    provider = GeminiProvider(api_key="test")
    key = provider._cache_key("prompt")

    assert provider._cache_get(key) is None

    provider._cache_put(key, "cached answer")
    assert provider._cache_get(key) == "cached answer"


def test_gemini_rate_limit_blocks_after_burst() -> None:
    """
    Law 3: after GEMINI_FREE_RPM requests are recorded within a minute,
    the rate limiter must report "not allowed".
    """
    from omnicovas.ai.gemini_provider import GEMINI_FREE_RPM

    provider = GeminiProvider(api_key="test")

    for _ in range(GEMINI_FREE_RPM):
        provider._record_request()

    assert provider._rate_limit_allows_request() is False
