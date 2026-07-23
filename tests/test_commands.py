"""Test module lifecycle command implementations."""

from pathlib import Path

import pytest
from forge.commands import removemodule
from forge.generator import create_module


def test_removemodule_removes_module_and_registration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that removemodule deletes files and router registration."""
    monkeypatch.chdir(tmp_path)
    module_path = create_module("orders")
    monkeypatch.setattr("builtins.input", lambda _prompt: "y")

    removemodule.execute(["orders"])

    assert not module_path.exists()
    registry = (tmp_path / "src" / "modules" / "__init__.py").read_text(encoding="utf-8")
    assert "orders_router" not in registry


def test_removemodule_cancel_preserves_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that declining confirmation preserves the module."""
    monkeypatch.chdir(tmp_path)
    module_path = create_module("orders")
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    removemodule.execute(["orders"])

    assert module_path.exists()


@pytest.mark.parametrize("args", [[".."], ["--force", ".."]])
def test_removemodule_rejects_parent_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: list[str],
) -> None:
    """Verify that removal cannot escape the modules directory."""
    monkeypatch.chdir(tmp_path)
    modules_dir = tmp_path / "src" / "modules"
    modules_dir.mkdir(parents=True)
    sentinel = tmp_path / "src" / "must-not-be-deleted.txt"
    sentinel.write_text("safe", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        removemodule.execute(args)

    assert exc_info.value.code == 1
    assert "not a valid Python module name" in capsys.readouterr().out
    assert sentinel.read_text(encoding="utf-8") == "safe"


def test_removemodule_dry_run_preserves_files_without_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that removal dry-run neither prompts nor changes files."""
    monkeypatch.chdir(tmp_path)
    module_path = create_module("orders")

    def fail_if_prompted(_prompt: str) -> str:
        pytest.fail("dry-run must not request confirmation")

    monkeypatch.setattr("builtins.input", fail_if_prompted)

    removemodule.execute(["orders", "--dry-run"])

    assert module_path.exists()
    assert "Dry run: module directory would be removed" in capsys.readouterr().out
    registry = (tmp_path / "src" / "modules" / "__init__.py").read_text(encoding="utf-8")
    assert "orders_router" in registry


def test_removemodule_force_skips_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that force removal skips only the confirmation prompt."""
    monkeypatch.chdir(tmp_path)
    module_path = create_module("orders")

    def fail_if_prompted(_prompt: str) -> str:
        pytest.fail("--force must not request confirmation")

    monkeypatch.setattr("builtins.input", fail_if_prompted)

    removemodule.execute(["--force", "orders"])

    assert not module_path.exists()
