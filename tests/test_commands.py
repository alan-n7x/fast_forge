from pathlib import Path

import pytest
from forge.commands import removemodule
from forge.generator import create_module


def test_removemodule_removes_module_and_registration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
    monkeypatch.chdir(tmp_path)
    module_path = create_module("orders")
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    removemodule.execute(["orders"])

    assert module_path.exists()


def test_removemodule_rejects_parent_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    modules_dir = tmp_path / "src" / "modules"
    modules_dir.mkdir(parents=True)
    sentinel = tmp_path / "src" / "must-not-be-deleted.txt"
    sentinel.write_text("safe", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        removemodule.execute([".."])

    assert exc_info.value.code == 1
    assert "not a valid Python module name" in capsys.readouterr().out
    assert sentinel.read_text(encoding="utf-8") == "safe"
