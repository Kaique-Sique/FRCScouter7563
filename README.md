# FRCScouter7563

[![Last Commit](https://img.shields.io/github/last-commit/Kaique-Sique/FRCScouter7563?color=informational)](https://github.com/Kaique-Sique/FRCScouter7563/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Kaique-Sique/FRCScouter7563/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](requirements.txt)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

🌐 **Idioma:** [🇧🇷 Português](README.md) | [🇺🇸 English](README.en.md)

API de scouting e dados para a temporada **FRC 2025 — Reefscape**, desenvolvida pela equipe **Megazord 7563** (Jundiaí, SP, Brasil).

O projeto é um backend em **FastAPI + PostgreSQL** com dois grandes blocos de funcionalidade:

1. **Proxy para a API do The Blue Alliance (TBA)** — times, eventos, distritos, partidas, insights e avanço regional, todos consumidos através da biblioteca própria [`BlueAlliancePy`](https://github.com/Kaique-Sique/BlueAlliancePy).
2. **Scouting próprio** — endpoints para registrar e consultar dados de scouting em campo (autônomo, teleop e pit scouting), persistidos em um banco PostgreSQL próprio.

> 📄 Para a referência completa de endpoints veja [`docs/API.md`](docs/API.md).
> 🗄️ Para o esquema do banco de dados veja [`docs/DATABASE.md`](docs/DATABASE.md).

---

## Sumário

- [Arquitetura](#arquitetura)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração (variáveis de ambiente)](#configuração-variáveis-de-ambiente)
- [Banco de dados](#banco-de-dados)
- [Executando a aplicação](#executando-a-aplicação)
- [Visão geral dos endpoints](#visão-geral-dos-endpoints)
- [Problemas conhecidos](#problemas-conhecidos)
- [Licença](#licença)

---

## Arquitetura

```
┌─────────────┐        ┌──────────────────────────┐        ┌────────────────────────┐
│   Cliente    │──────▶│      FastAPI (app)        │──────▶│  The Blue Alliance API  │
│ (app de      │        │  app/app.py + routers      │        │  (via BlueAlliancePy)   │
│  scouting,   │        │                            │        └────────────────────────┘
│  dashboards) │        │                            │
└─────────────┘        │                            │        ┌────────────────────────┐
                        │                            │──────▶│   PostgreSQL            │
                        └──────────────────────────┘        │  (scouting próprio)     │
                                                              └────────────────────────┘
```

- **Camada de rotas** (`app/api/routes/`): cada arquivo é um `APIRouter` do FastAPI, agrupado por domínio (`teams`, `events`, `districts`, `matchs`, `insights`, `regional_advancement`, `scout`).
- **Camada de schemas** (`app/api/schemas/`): modelos Pydantic usados para validar o corpo das requisições de scouting (`AutoScout`, `TeleopScout`, `PitScout`).
- **Camada de serviços** (`app/services/`): instancia e expõe os clientes singleton da TBA (`TBAClient`, `TBACollector`).
- **Camada core** (`app/core/`): configuração (`config.py`) e acesso a banco de dados (`db.py`).

Os endpoints de `teams`, `events`, `districts`, `matchs`, `insights` e `regional_advancement` **não acessam o banco de dados** — eles apenas repassam a chamada para a API pública do TBA através do `TBAClient`. Já os endpoints de `scout` fazem `INSERT`/`SELECT`/`DELETE` diretamente no PostgreSQL da equipe.

## Estrutura do projeto

```
FRCScouter7563/
├── main.py                          # Ponto de entrada (uvicorn)
├── requirements.txt                 # Dependências Python
├── .env.exemple                     # Modelo de variáveis de ambiente
├── sql/
│   └── database-schema.sql          # DDL das tabelas de scouting
├── docs/
│   ├── API.md                       # Referência completa de endpoints
│   └── DATABASE.md                  # Documentação do schema do banco
└── app/
    ├── app.py                       # Cria e configura a instância FastAPI
    ├── static/                      # Arquivos estáticos (favicon)
    ├── core/
    │   ├── config.py                 # Leitura/validação de variáveis de ambiente
    │   └── db.py                     # Conexão psycopg2 + context manager de cursor
    ├── services/
    │   └── tba_services.py           # Singletons do cliente/coletor TBA
    └── api/
        ├── schemas/
        │   ├── auto_scout_reefscape.py
        │   ├── teleop_scout_reefscape.py
        │   └── pit_scout.py
        └── routes/
            ├── teams.py                # /teams
            ├── events.py               # /events
            ├── districts.py            # /districts
            ├── matchs.py               # /matchs
            ├── insights.py             # /insights
            ├── regional_advancement.py # /regional_advancement
            └── scout.py                # /scout (auto, teleop, pit)
```

## Requisitos

- Python 3.11+ (recomendado)
- PostgreSQL 13+
- Uma chave de leitura (Read API Key) do [The Blue Alliance](https://www.thebluealliance.com/account)
- Git (para instalar a dependência `bluealliance` diretamente do GitHub)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Kaique-Sique/FRCScouter7563.git
cd FRCScouter7563

# 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

## Configuração (variáveis de ambiente)

Copie `.env.exemple` para `.env` e preencha os valores:

```dotenv
DB_NAME=your-db
DB_USER=api-user
DB_PASSWORD=your_password_here
DB_HOST=your_database-host
DB_PORT=db_port

TBA_KEY=your_thebluealliance_api_key_here
TBA_BASE_URL=https://www.thebluealliance.com/api/v3

FRC_YEAR=season_year
```

| Variável       | Obrigatória | Descrição                                                                 |
|----------------|:-----------:|----------------------------------------------------------------------------|
| `DB_NAME`      | ✅          | Nome do banco PostgreSQL                                                   |
| `DB_USER`      | ✅          | Usuário do banco                                                           |
| `DB_PASSWORD`  | ✅          | Senha do banco                                                             |
| `DB_HOST`      | ✅          | Host do banco (ex.: `localhost`)                                           |
| `DB_PORT`      | ✅          | Porta do banco (ex.: `5432`)                                               |
| `TBA_KEY`      | ✅          | Chave de leitura da API do The Blue Alliance                               |
| `TBA_BASE_URL` | ✅          | Base URL da API do TBA (`https://www.thebluealliance.com/api/v3`)          |
| `FRC_YEAR`     | ❌          | Ano padrão da temporada. Default: `2026`                                   |

A leitura e validação dessas variáveis acontece em `app/core/config.py`: variáveis obrigatórias ausentes ou vazias fazem a aplicação falhar **imediatamente** ao subir, com uma mensagem clara (`Variable <NOME> is not set in the environment`).

## Banco de dados

O schema fica em [`sql/database-schema.sql`](sql/database-schema.sql) e cria três tabelas:

- `auto_scout_reefscape` — dados do período autônomo.
- `teleop_scout_reefscape` — dados do período teleoperado + subida (climb).
- `pit_scout` — dados de pit scouting (descrição do robô, foto).

Para aplicar o schema em um banco PostgreSQL vazio:

```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/database-schema.sql
```

Veja [`docs/DATABASE.md`](docs/DATABASE.md) para a descrição campo a campo de cada tabela.

## Executando a aplicação

```bash
python main.py
```

Isso sobe o servidor Uvicorn em `http://0.0.0.0:8000` com *auto-reload* habilitado. Alternativamente:

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

Com o servidor no ar, a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI fica disponível em:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### Endpoints de diagnóstico

| Rota             | Descrição                                              |
|------------------|----------------------------------------------------------|
| `HEAD /`         | Verifica se a API está no ar.                            |
| `GET /status-db` | Testa a conexão com o PostgreSQL (`Online`/`Offline`).   |
| `GET /status-tba`| Repassa o status da API do TBA (`/status` do TBA).       |

## Visão geral dos endpoints

| Prefixo                    | Origem dos dados        | Descrição                                              |
|-----------------------------|--------------------------|----------------------------------------------------------|
| `/teams`                    | The Blue Alliance        | Times, histórico, eventos, mídias, prêmios               |
| `/events`                   | The Blue Alliance        | Eventos por ano, alianças, rankings, OPRs, previsões      |
| `/districts`                | The Blue Alliance        | Distritos, times/eventos por distrito, avanço             |
| `/matchs`                   | The Blue Alliance        | Partida individual, timeseries, Zebra MotionWorks         |
| `/insights`                 | The Blue Alliance        | Leaderboards, destaques, insights por ano/categoria       |
| `/regional_advancement`     | The Blue Alliance        | Avanço ao Championship, rankings regionais                |
| `/scout`                    | PostgreSQL (próprio)     | CRUD de scouting: autônomo, teleop e pit                  |

A referência completa — com método HTTP, parâmetros e descrição de cada uma das dezenas de rotas — está em [`docs/API.md`](docs/API.md).

## Problemas conhecidos

- **Divergência entre `sql/database-schema.sql` e `app/api/routes/scout.py`:** as consultas de `INSERT`/`SELECT`/`DELETE` "por chave" em `scout.py` usam colunas (`scout_auto_key`, `scout_teleop_key`, `pit_scout_key`) que não existem no schema atual (que usa `id SERIAL PRIMARY KEY` + `UNIQUE (event_key, match_key, team_key)`). Isso faz com que essas rotas falhem com `psycopg2.errors.UndefinedColumn` até que o schema seja atualizado com essas colunas (ou as queries sejam ajustadas para usar a constraint composta já existente).
- Os endpoints `GET /regional_advancement/{year}` e `GET /regional_advancement/{year}/rankings` compartilham, no código-fonte, o mesmo nome de função Python (`get_regional_advancement`); isso funciona porque o FastAPI despacha pela rota registrada, não pelo nome da função, mas a segunda definição sobrescreve a primeira em nível de módulo Python.
- As rotas de listagem de chaves (`/scout/auto/matches/keys`, `/scout/teleop/matches/keys`) não usam `DISTINCT`, então uma mesma `match_key` pode aparecer repetida se houver mais de um registro de scouting para aquela partida.

## Licença

Distribuído sob a licença MIT — veja [`LICENSE`](LICENSE).
