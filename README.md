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
from src.modules import main_router

app = FastAPI()
app.include_router(main_router)
```

## Gerado pela primeira vez

Veja [src/modules/telegram/](src/modules/telegram/) como exemplo.
