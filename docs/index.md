# FRCScouter7563

[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Kaique-Sique/FRCScouter7563/blob/main/LICENSE) 
![Last Commit](https://img.shields.io/github/last-commit/Kaique-Sique/FRCScouter7563)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

Scouting and data API for the **FRC 2025 — Reefscape** season, built by team **Megazord 7563** (Jundiaí, SP, Brazil).

The project is a **FastAPI + PostgreSQL** backend with two major feature blocks:

1. **The Blue Alliance (TBA) API proxy** — teams, events, districts, matches, insights, and regional advancement, all consumed through the team's own [`BlueAlliancePy`](https://github.com/Kaique-Sique/BlueAlliancePy) library.
2. **In-house scouting** — endpoints to record and query on-field scouting data (autonomous, teleop, and pit scouting), persisted in the team's own PostgreSQL database.

> 📄 For the full endpoint reference, see [`docs/API.md`](/ReadTheDocs/API).
> 
> 🗄️ For the database schema, see [`docs/DATABASE.md`](/ReadTheDocs/DATABASE).

---

## Table of contents

- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration (environment variables)](#configuration-environment-variables)
- [Database](#database)
- [Running the application](#running-the-application)
- [Endpoints overview](#endpoints-overview)
- [Known issues](#known-issues)
- [License](#license)

---

## Architecture

```
┌─────────────┐        ┌──────────────────────────┐        ┌────────────────────────┐
│    Client    │──────▶│      FastAPI (app)        │──────▶│  The Blue Alliance API  │
│ (scouting    │        │  app/app.py + routers      │        │  (via BlueAlliancePy)   │
│  app,        │        │                            │        └────────────────────────┘
│  dashboards) │        │                            │
└─────────────┘        │                            │        ┌────────────────────────┐
                        │                            │──────▶│   PostgreSQL            │
                        └──────────────────────────┘        │  (in-house scouting)    │
                                                              └────────────────────────┘
```

- **Routes layer** (`app/api/routes/`): each file is a FastAPI `APIRouter`, grouped by domain (`teams`, `events`, `districts`, `matchs`, `insights`, `regional_advancement`, `scout`).
- **Schemas layer** (`app/api/schemas/`): Pydantic models used to validate scouting request bodies (`AutoScout`, `TeleopScout`, `PitScout`).
- **Services layer** (`app/services/`): instantiates and exposes the TBA singleton clients (`TBAClient`, `TBACollector`).
- **Core layer** (`app/core/`): configuration (`config.py`) and database access (`db.py`).

The `teams`, `events`, `districts`, `matchs`, `insights`, and `regional_advancement` endpoints **never touch the database** — they only forward the call to the public TBA API through `TBAClient`. The `scout` endpoints, on the other hand, run `INSERT`/`SELECT`/`DELETE` directly against the team's own PostgreSQL database.

## Project structure

```
FRCScouter7563/
├── main.py                          # Entry point (uvicorn)
├── requirements.txt                 # Python dependencies
├── .env.exemple                     # Environment variable template
├── sql/
│   └── database-schema.sql          # DDL for the scouting tables
├── docs/
│   ├── API.md                       # Full endpoint reference
│   └── DATABASE.md                  # Database schema documentation
└── app/
    ├── app.py                       # Creates and configures the FastAPI instance
    ├── static/                      # Static files (favicon)
    ├── core/
    │   ├── config.py                 # Environment variable loading/validation
    │   └── db.py                     # psycopg2 connection + cursor context manager
    ├── services/
    │   └── tba_services.py           # TBA client/collector singletons
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

## Requirements

- Python 3.11+ (recommended)
- PostgreSQL 13+
- A Read API Key from [The Blue Alliance](https://www.thebluealliance.com/account)
- Git (to install the `bluealliance` dependency directly from GitHub)

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Kaique-Sique/FRCScouter7563.git
cd FRCScouter7563

# 2. Create and activate a virtual environment (optional, but recommended)
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Configuration (environment variables)

Copy `.env.exemple` to `.env` and fill in the values:

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

| Variable       | Required | Description                                                                |
|----------------|:--------:|-------------------------------------------------------------------------------|
| `DB_NAME`      | ✅       | PostgreSQL database name                                                      |
| `DB_USER`      | ✅       | Database user                                                                  |
| `DB_PASSWORD`  | ✅       | Database password                                                             |
| `DB_HOST`      | ✅       | Database host (e.g. `localhost`)                                              |
| `DB_PORT`      | ✅       | Database port (e.g. `5432`)                                                   |
| `TBA_KEY`      | ✅       | The Blue Alliance Read API key                                                |
| `TBA_BASE_URL` | ✅       | TBA API base URL (`https://www.thebluealliance.com/api/v3`)                   |
| `FRC_YEAR`     | ❌       | Default season year. Default: `2026`                                          |

Reading and validation of these variables happens in `app/core/config.py`: missing or blank required variables make the application fail **immediately** on startup, with a clear message (`Variable <NAME> is not set in the environment`).

## Database

The schema lives in sql/database-schema.sql and creates three tables:

- `auto_scout_reefscape` — autonomous period data.
- `teleop_scout_reefscape` — teleop period + endgame climb data.
- `pit_scout` — pit scouting data (robot description, photo).

To apply the schema to an empty PostgreSQL database:

```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/database-schema.sql
```

See [`docs/DATABASE.md`](ReadTheDocs/DATABASE) for a field-by-field description of each table.

## Running the application

```bash
python main.py
```

This starts the Uvicorn server on `http://0.0.0.0:8000` with auto-reload enabled. Alternatively:

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

With the server running, FastAPI's auto-generated interactive docs are available at:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### Diagnostic endpoints

| Route             | Description                                             |
|-------------------|-------------------------------------------------------------|
| `HEAD /`          | Checks whether the API is up.                                |
| `GET /status-db`  | Tests the PostgreSQL connection (`Online`/`Offline`).        |
| `GET /status-tba` | Forwards the TBA API status (`/status` on TBA).              |

## Endpoints overview

| Prefix                      | Data source              | Description                                             |
|-------------------------------|----------------------------|--------------------------------------------------------------|
| `/teams`                    | The Blue Alliance         | Teams, history, events, media, awards                        |
| `/events`                   | The Blue Alliance         | Events by year, alliances, rankings, OPRs, predictions        |
| `/districts`                | The Blue Alliance         | Districts, teams/events per district, advancement             |
| `/matchs`                   | The Blue Alliance         | Single match, timeseries, Zebra MotionWorks                   |
| `/insights`                 | The Blue Alliance         | Leaderboards, notables, insights by year/category              |
| `/regional_advancement`     | The Blue Alliance         | Championship advancement, regional rankings                   |
| `/scout`                    | PostgreSQL (in-house)     | Scouting CRUD: autonomous, teleop, and pit                     |

The full reference — with HTTP method, parameters, and a description of each of the dozens of routes — is in [`docs/API.md`](ReadTheDocs/API).

## Known issues

- **Mismatch between `sql/database-schema.sql` and `app/api/routes/scout.py`:** the "by key" `INSERT`/`SELECT`/`DELETE` queries in `scout.py` use columns (`scout_auto_key`, `scout_teleop_key`, `pit_scout_key`) that don't exist in the current schema (which instead uses `id SERIAL PRIMARY KEY` + `UNIQUE (event_key, match_key, team_key)`). This means those routes will fail with `psycopg2.errors.UndefinedColumn` until the schema is updated with those columns (or the queries are adjusted to use the existing composite unique constraint).
- The `GET /regional_advancement/{year}` and `GET /regional_advancement/{year}/rankings` endpoints share the same Python function name (`get_regional_advancement`) in the source code; this works because FastAPI dispatches by the registered route, not the function name, but the second definition shadows the first at the Python module level.
- The key-listing routes (`/scout/auto/matches/keys`, `/scout/teleop/matches/keys`) don't use `DISTINCT`, so the same `match_key` may appear more than once if there's more than one scouting entry for that match.

## License

Distributed under the MIT license — see [`LICENSE`](LICENSE).
