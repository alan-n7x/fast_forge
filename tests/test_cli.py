import sys
from pathlib import Path

import pytest
from forge.cli import main


def test_cli_without_arguments_shows_help(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["forge"])

    main()

    output = capsys.readouterr().out
    assert "Usage:" in output
    assert "startmodule" in output
    assert "removemodule" in output


def test_cli_rejects_unknown_command(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["forge", "unknown"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    assert "Unknown command: 'unknown'" in capsys.readouterr().out


def test_cli_startmodule_generates_module(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["forge", "startmodule", "order-items"])

    main()

    assert (tmp_path / "src" / "modules" / "order_items").is_dir()
    assert "Module 'order_items' created" in capsys.readouterr().out


def test_cli_startmodule_rejects_unsafe_name(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["forge", "startmodule", ".."])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    assert "not a valid Python module name" in capsys.readouterr().out
    assert not (tmp_path / "src").exists()


def test_cli_startmodule_dry_run_does_not_create_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        ["forge", "startmodule", "order-items", "--dry-run"],
    )

    main()

    output = capsys.readouterr().out
    assert "Dry run: module 'order_items' would be created" in output
    assert not (tmp_path / "src").exists()
