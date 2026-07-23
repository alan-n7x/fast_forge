# fast_forge

CLI scaffolding generator for FastAPI Clean Architecture modules.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Comandos

| Comando | Descrição |
|---|---|
| `python manage.py startmodule <nome>` | Gera um novo módulo |
| `python manage.py removemodule <nome>` | Remove um módulo |

### Opções seguras

```bash
# Valida e mostra o destino sem criar arquivos
python manage.py startmodule notifications --dry-run

# Mostra o que seria removido sem alterar arquivos
python manage.py removemodule notifications --dry-run

# Remove sem confirmação interativa, mantendo todas as validações de segurança
python manage.py removemodule notifications --force
```

## Exemplo

```bash
python manage.py startmodule notifications
```

Gera `src/modules/notifications/` com a estrutura:

```
presentation/     router, schemas, dependencies
application/      use_cases, services, dto
domain/           entities, repository, exceptions, value_objects
infrastructure/   repositories, gateways, settings
tests/            test_router, test_use_cases, test_gateway
```

O router é registrado automaticamente em `src/modules/__init__.py`.

## Usando os módulos no FastAPI

```python
from fastapi import FastAPI
from modules import main_router

app = FastAPI()
app.include_router(main_router)
```

## Desenvolvimento

Requer [uv](https://docs.astral.sh/uv/) e Python 3.12 ou superior.

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

O `pytest` exige cobertura mínima de 80% do pacote `forge`.

## Gerado pela primeira vez

Veja [src/modules/telegram/](src/modules/telegram/) como exemplo.
