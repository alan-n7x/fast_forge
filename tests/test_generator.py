from pathlib import Path

import pytest
from forge.generator import create_module, plan_module, resolve_module_path, to_pascal_case


def test_to_pascal_case() -> None:
    assert to_pascal_case("order_items") == "OrderItems"
    assert to_pascal_case("order-items") == "OrderItems"


def test_create_module_generates_structure_and_registration(tmp_path: Path) -> None:
    target_dir = tmp_path / "src" / "modules"

    module_path = create_module("order-items", target_dir)

    assert module_path == (target_dir / "order_items").resolve()
    assert (module_path / "domain" / "entities.py").is_file()
    assert (module_path / "application" / "use_cases" / "create_order_items_use_case.py").is_file()
    assert (module_path / "presentation" / "router.py").is_file()
    assert (module_path / "infrastructure" / "repositories" / "fake_repository.py").is_file()
    assert (module_path / "tests" / "test_router.py").is_file()

    router = (module_path / "presentation" / "router.py").read_text(encoding="utf-8")
    registry = (target_dir / "__init__.py").read_text(encoding="utf-8")
    assert "from modules.order_items.presentation.schemas import HealthResponse" in router
    assert "from .order_items.presentation.router import router as order_items_router" in registry
    assert "main_router.include_router(order_items_router)" in registry


def test_create_module_rejects_duplicate(tmp_path: Path) -> None:
    target_dir = tmp_path / "modules"
    create_module("orders", target_dir)

    with pytest.raises(FileExistsError):
        create_module("orders", target_dir)


def test_plan_module_validates_without_creating_files(tmp_path: Path) -> None:
    target_dir = tmp_path / "src" / "modules"

    module_path = plan_module("order-items", target_dir)

    assert module_path == (target_dir / "order_items").resolve()
    assert not target_dir.exists()


@pytest.mark.parametrize("module_name", ["", "..", "../outside", "class", "orders/items"])
def test_module_path_rejects_unsafe_names(tmp_path: Path, module_name: str) -> None:
    target_dir = tmp_path / "src" / "modules"

    with pytest.raises(ValueError):
        resolve_module_path(module_name, target_dir)

    assert not (tmp_path / "outside").exists()
