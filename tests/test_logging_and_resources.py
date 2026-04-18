"""
tests.test_logging_and_resources

Tests for Week 6 infrastructure: logging redaction and resource monitoring.

Related to: Law 2 (Legal Compliance) — API keys must never appear in logs
Related to: Principle 10 (Resource Efficiency) — bounded, measurable
Related to: Phase 1 Development Guide Week 6

Tests:
    1. redaction_processor redacts Gemini-style API keys
    2. redaction_processor redacts OpenAI-style keys
    3. redaction_processor redacts GitHub tokens
    4. redaction_processor leaves normal text alone
    5. ResourceBudget loads defaults when file missing
    6. ResourceBudget loads from YAML correctly
    7. ResourceMonitor takes snapshot without crashing
    8. ResourceMonitor check_budget returns no warnings for normal use
"""

from __future__ import annotations

from pathlib import Path

from omnicovas.core.logging_config import _redact_string, redaction_processor
from omnicovas.core.resource_monitor import (
    ResourceBudget,
    ResourceMonitor,
    ResourceSnapshot,
)


def test_redaction_catches_gemini_key() -> None:
    """Law 2: Gemini API keys must be redacted."""
    text = "config loaded with key=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz0123456789"
    result = _redact_string(text)
    assert "AIza" not in result
    assert "[REDACTED]" in result


def test_redaction_catches_openai_key() -> None:
    """OpenAI-style keys must be redacted."""
    text = "using sk-abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGH"
    result = _redact_string(text)
    assert "sk-abc" not in result
    assert "[REDACTED]" in result


def test_redaction_catches_github_token() -> None:
    """GitHub personal access tokens must be redacted."""
    text = "token: ghp_abc123def456ghi789jkl012mno345pqr678"
    result = _redact_string(text)
    assert "ghp_" not in result
    assert "[REDACTED]" in result


def test_redaction_leaves_short_text_alone() -> None:
    """Normal words must not be falsely redacted."""
    text = "jumped to Sol system and docked at Jameson Memorial"
    result = _redact_string(text)
    assert result == text


def test_redaction_processor_processes_event_dict() -> None:
    """The structlog processor redacts all string values in event dict."""
    event = {
        "event": "auth",
        "api_key": "AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
        "user": "commander",
    }
    result = redaction_processor(None, "info", event)
    assert "AIza" not in result["api_key"]
    assert result["event"] == "auth"
    assert result["user"] == "commander"


def test_resource_budget_defaults_when_file_missing(tmp_path: Path) -> None:
    """If resource_budget.yaml is missing, sensible defaults are used."""
    missing_path = tmp_path / "does_not_exist.yaml"
    budget = ResourceBudget.load(missing_path)

    assert budget.max_cache_size_mb == 512
    assert budget.max_background_task_cpu_percent == 10


def test_resource_budget_loads_from_yaml(tmp_path: Path) -> None:
    """YAML overrides are honored."""
    yaml_content = """
disk:
  max_galaxy_dump_size_gb: 10
  max_log_retention_days: 45
  log_rotation_size_mb: 50
memory:
  max_cache_size_mb: 256
  max_ai_context_tokens: 2000
cpu:
  max_background_task_cpu_percent: 5
bandwidth:
  max_eddn_submission_per_hour: 200
  max_api_calls_per_minute_total: 100
"""
    budget_path = tmp_path / "budget.yaml"
    budget_path.write_text(yaml_content)

    budget = ResourceBudget.load(budget_path)

    assert budget.max_galaxy_dump_size_gb == 10
    assert budget.max_cache_size_mb == 256
    assert budget.max_background_task_cpu_percent == 5


def test_resource_monitor_snapshot_does_not_crash() -> None:
    """snapshot() must return a real measurement without raising."""
    monitor = ResourceMonitor(budget=ResourceBudget())

    snap = monitor.snapshot()

    assert isinstance(snap, ResourceSnapshot)
    assert snap.memory_used_mb > 0
    assert snap.memory_total_mb > 0
    assert snap.disk_free_gb > 0


def test_resource_monitor_check_budget_normal_use() -> None:
    """A normal-looking snapshot produces no warnings."""
    monitor = ResourceMonitor(budget=ResourceBudget())
    normal = ResourceSnapshot(
        memory_used_mb=100.0,
        memory_total_mb=16000.0,
        cpu_percent=2.0,
        disk_free_gb=250.0,
        disk_total_gb=500.0,
    )

    warnings = monitor.check_budget(normal)

    assert warnings == []


def test_resource_monitor_check_budget_flags_disk_low() -> None:
    """Disk space under 1 GB triggers a warning."""
    monitor = ResourceMonitor(budget=ResourceBudget())
    tight = ResourceSnapshot(
        memory_used_mb=100.0,
        memory_total_mb=16000.0,
        cpu_percent=2.0,
        disk_free_gb=0.5,
        disk_total_gb=500.0,
    )

    warnings = monitor.check_budget(tight)

    assert any("Disk free space low" in w for w in warnings)
