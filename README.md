# FastForge

FastForge é uma caixa de ferramentas para criar aplicações FastAPI com a
experiência de desenvolvimento produtiva do Django e uma arquitetura modular,
explícita e testável.

## Visão do produto

O objetivo é reduzir o trabalho repetitivo necessário para iniciar e evoluir
APIs FastAPI. O FastForge deverá oferecer dois níveis de geração:

```bash
forge startproject minha_api
forge startmodule orders
```

O `startproject` será responsável pela fundação completa da aplicação. O
`startmodule` continuará adicionando módulos de negócio em Clean Architecture.

## Estado atual

A versão atual gera e remove módulos de negócio com as seguintes camadas:

```text
presentation/     routers, schemas e dependências
application/      casos de uso, serviços e DTOs
domain/           entidades, contratos, exceções e value objects
infrastructure/   repositórios, gateways e configurações
tests/            testes unitários e de integração
```

O gerador já oferece:

- validação e confinamento seguro dos caminhos;
- registro automático do router;
- operações `--dry-run`;
- remoção interativa ou automatizada com `--force`;
- templates distribuídos dentro do pacote;
- testes, tipagem estrita e CI para Python 3.12 e 3.14;
- documentação de código no padrão Google.

O FastForge ainda não gera um projeto completo nem possui autenticação de
usuários. Esses recursos fazem parte da próxima fase do produto.

## Instalação para desenvolvimento

Requer [uv](https://docs.astral.sh/uv/) e Python 3.12 ou superior.

```bash
git clone https://github.com/alan-n7x/fast_forge.git
cd fast_forge
uv sync
```

Para consultar a CLI:

```bash
uv run forge --help
```

## Comandos

### Criar um módulo

```bash
uv run forge startmodule notifications
```

O módulo é criado em `src/modules/notifications/` e seu router é registrado em
`src/modules/__init__.py`.

Use `--dry-run` para validar o nome e visualizar o destino sem criar arquivos:

```bash
uv run forge startmodule notifications --dry-run
```

### Remover um módulo

```bash
uv run forge removemodule notifications
```

Use `--dry-run` para inspecionar a operação:

```bash
uv run forge removemodule notifications --dry-run
```

Use `--force` em automações que não podem responder à confirmação interativa:

```bash
uv run forge removemodule notifications --force
```

O `--force` remove somente a confirmação. As validações de nome e segurança do
caminho permanecem obrigatórias.

## Integração com FastAPI

Com `src` disponível no caminho de importação da aplicação:

```python
from fastapi import FastAPI
from modules import main_router

app = FastAPI()
app.include_router(main_router)
```

Veja [`src/modules/telegram/`](src/modules/telegram/) como exemplo versionado da
estrutura produzida.

## Padrão de documentação

Módulos, pacotes, classes, métodos e funções usam docstrings no padrão Google.
O Ruff verifica esse contrato por meio das regras `pydocstyle`.

Exemplo:

```python
def create_module(module_name: str, target_dir: str) -> Path:
    """Generate a Clean Architecture module.

    Args:
        module_name: Name used for the Python package.
        target_dir: Directory that owns the generated module.

    Returns:
        Absolute path to the generated module.

    Raises:
        FileExistsError: If the target module already exists.
        ValueError: If the module name or target path is unsafe.
    """
```

## Qualidade

Execute todas as verificações antes de enviar alterações:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

O projeto exige cobertura mínima de 80% do pacote `forge`.

## Roadmap

### Confiabilidade do ciclo de vida

- criação e remoção transacionais;
- rollback automático em falhas;
- descoberta automática da raiz do projeto;
- configuração por meio de `[tool.fastforge]`.

### Geração de projetos

- comando `forge startproject`;
- aplicação FastAPI executável;
- configurações por ambiente;
- SQLAlchemy e Alembic;
- Docker e banco PostgreSQL;
- logging, health check e testes iniciais.

### Sistema de usuários

O perfil padrão de projeto deverá oferecer um módulo `accounts` opcional,
inspirado nas funcionalidades integradas do Django:

- cadastro e gerenciamento de usuários;
- login com access token e refresh token;
- logout e revogação de sessões;
- endpoint do usuário autenticado;
- alteração e recuperação de senha;
- verificação de e-mail;
- usuários ativos e inativos;
- papéis e permissões;
- migrations e testes;
- painel administrativo opcional.

Exemplos planejados:

```bash
forge startproject minha_api
forge startproject minha_api --auth jwt
forge startproject minha_api --no-auth
```

### Perfis e extensibilidade

- perfis `minimal`, `standard` e `full`;
- templates personalizados;
- novos tipos de módulos;
- saída estruturada para automações;
- publicação e versionamento no PyPI.
