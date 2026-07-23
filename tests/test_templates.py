"""Test packaged template loading, rendering, and output equivalence."""

from pathlib import Path

import pytest
from forge.generator import create_module
from forge.templates import load_template, render_template

PROJECT_ROOT = Path(__file__).parents[1]


def test_load_template_reads_packaged_resource() -> None:
    """Verify that a template can be loaded from package resources."""
    template = load_template("module/presentation/router.py.tpl")

    assert "from modules.{module_name}.presentation.schemas" in template


def test_load_template_rejects_missing_resource() -> None:
    """Verify that loading a missing template reports its resource name."""
    with pytest.raises(FileNotFoundError, match="Template not found"):
        load_template("module/missing.py.tpl")


def test_load_template_rejects_parent_path() -> None:
    """Verify that template paths cannot escape the resource directory."""
    with pytest.raises(ValueError, match="Unsafe template path"):
        load_template("../cli.py")


def test_render_template_reports_missing_context() -> None:
    """Verify that rendering reports absent context variables."""
    with pytest.raises(RuntimeError, match="Error formatting template"):
        render_template("module/presentation/router.py.tpl", {})


def test_generated_module_matches_versioned_example(tmp_path: Path) -> None:
    """Verify that templates reproduce the versioned example text."""
    generated = create_module("telegram", tmp_path / "modules")
    example = PROJECT_ROOT / "src" / "modules" / "telegram"

    example_files = {
        path.relative_to(example)
        for path in example.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    generated_files = {
        path.relative_to(generated)
        for path in generated.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }

    assert generated_files == example_files
    for relative_path in example_files:
        assert generated.joinpath(relative_path).read_text(encoding="utf-8") == example.joinpath(
            relative_path
        ).read_text(encoding="utf-8")
