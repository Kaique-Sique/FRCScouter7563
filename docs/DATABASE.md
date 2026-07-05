# DATABASE — FRCScouter7563

The database is **PostgreSQL** and stores only the scouting data collected by the team itself (data coming from The Blue Alliance is never persisted locally — it's always fetched on-demand through `TBAClient`).


## Logical diagram

```
auto_scout_reefscape             teleop_scout_reefscape           pit_scout
┌───────────────────────┐       ┌───────────────────────┐        ┌───────────────────────┐
│ id (PK)               │       │ id (PK)               │        │ id (PK)               │
│ event_key             │       │ event_key             │        │ team_key (UNIQUE)     │
│ match_key             │       │ match_key             │        │ description           │
│ team_key              │       │ team_key              │        │ img_url               │
│ year                  │       │ year                  │        │ created_at            │
│ l1..l4                │       │ l1..l4                │        └───────────────────────┘
│ coral_misseds         │       │ coral_misseds         │
│ coral_precision       │       │ coral_precision       │
│ algae_removed/net/... │       │ algae_removed/net/... │
│ region_scored (JSONB) │       │ climb                 │
│ score                 │       │ collected_coral_floor │
│ startline             │       │ collected_coral_stat. │
│ notes                 │       │ collected_algae_reef  │
│ created_at            │       │ issues / issues_notes │
│ UNIQUE(event,match,   │       │ defended              │
│        team)          │       │ driver_rating         │
└───────────────────────┘       │ score                 │
                                │ notes                 │
                                │ created_at            │
                                │ UNIQUE(event,match,   │
                                │        team)          │
                                └───────────────────────┘
```

---

## `auto_scout_reefscape`

One row per (event, match, team) combination: what that robot did during the **autonomous** period of the 2025 Reefscape season.

| Column             | Type             | Default | Description                                                                |
|--------------------|------------------|---------|-------------------------------------------------------------------------------|
| `id`               | `SERIAL`         | —       | Primary key.                                                                   |
| `event_key`        | `VARCHAR(50)`    | —       | TBA event key (e.g. `2025sao`). `NOT NULL`.                                    |
| `match_key`        | `VARCHAR(50)`    | —       | TBA match key (e.g. `2025sao_qm12`). `NOT NULL`.                               |
| `team_key`         | `VARCHAR(50)`    | —       | TBA team key (e.g. `frc7563`). `NOT NULL`.                                     |
| `year`             | `INTEGER`        | —       | Season year. `NOT NULL`.                                                       |
| `l1`               | `INTEGER`        | `0`     | Coral scored on reef level 1 during auto.                                      |
| `l2`               | `INTEGER`        | `0`     | Coral scored on level 2.                                                       |
| `l3`               | `INTEGER`        | `0`     | Coral scored on level 3.                                                       |
| `l4`               | `INTEGER`        | `0`     | Coral scored on level 4.                                                       |
| `coral_misseds`    | `INTEGER`        | `0`     | Number of failed coral scoring attempts.                                       |
| `coral_precision`  | `DECIMAL(5,2)`   | `0`     | Coral scoring accuracy (%), with `CHECK (0 <= value <= 100)`.                  |
| `algae_removed`    | `INTEGER`        | `0`     | Algae removed from the reef.                                                   |
| `algae_net`        | `INTEGER`        | `0`     | Algae scored in the net.                                                       |
| `algae_processor`  | `INTEGER`        | `0`     | Algae scored in the processor.                                                 |
| `region_scored`    | `JSONB`          | —       | Free-form payload describing *where* on the field scoring occurred.           |
| `score`            | `INTEGER`        | `0`     | Estimated auto score contribution assigned to the team.                        |
| `startline`        | `BOOLEAN`        | `FALSE` | Whether the robot left the starting line (mobility).                          |
| `notes`            | `TEXT`           | —       | Free-text scouting notes.                                                      |
| `created_at`       | `TIMESTAMP`      | `CURRENT_TIMESTAMP` | Record creation timestamp.                                        |

**Constraints:**
- `uq_auto_match_team`: `UNIQUE (event_key, match_key, team_key)` — prevents two entries for the same team in the same match of the same event.
- `CHECK` on `coral_precision` enforcing the `[0, 100]` range.

---

## `teleop_scout_reefscape`

One row per (event, match, team) combination: what that robot did during the **teleop** period and the **endgame climb**.

| Column                    | Type             | Default | Description                                                            |
|---------------------------|------------------|---------|-----------------------------------------------------------------------------|
| `id`                       | `SERIAL`         | —       | Primary key.                                                                 |
| `event_key`                | `VARCHAR(50)`    | —       | TBA event key. `NOT NULL`.                                                   |
| `match_key`                | `VARCHAR(50)`    | —       | TBA match key. `NOT NULL`.                                                   |
| `team_key`                 | `VARCHAR(50)`    | —       | TBA team key. `NOT NULL`.                                                    |
| `year`                     | `INTEGER`        | —       | Season year. `NOT NULL`.                                                     |
| `l1`..`l4`                  | `INTEGER`        | `0`     | Coral scored on each reef level during teleop.                              |
| `coral_misseds`            | `INTEGER`        | `0`     | Failed coral scoring attempts.                                              |
| `coral_precision`          | `DECIMAL(5,2)`   | `0`     | Coral scoring accuracy (%), `CHECK (0 <= value <= 100)`.                    |
| `algae_removed`            | `INTEGER`        | `0`     | Algae removed from the reef.                                                |
| `algae_net`                | `INTEGER`        | `0`     | Algae scored in the net.                                                    |
| `algae_processor`          | `INTEGER`        | `0`     | Algae scored in the processor.                                              |
| `climb`                    | `VARCHAR(30)`    | —       | Endgame climb result (free text, e.g. `"deep"`, `"shallow"`, `"park"`, `"none"`). |
| `collected_coral_floor`    | `BOOLEAN`        | `FALSE` | Whether the robot picked up coral from the floor.                          |
| `collected_coral_station`  | `BOOLEAN`        | `FALSE` | Whether the robot picked up coral from the human player station.           |
| `collected_algae_reef`     | `BOOLEAN`        | `FALSE` | Whether the robot picked algae off the reef.                               |
| `issues`                   | `BOOLEAN`        | `FALSE` | Whether the robot had any issue/malfunction.                               |
| `issues_notes`             | `TEXT`           | —       | Free-text description of the issue, if any.                                |
| `defended`                 | `BOOLEAN`        | `FALSE` | Whether the robot played defense during the match.                         |
| `driver_rating`            | `INTEGER`        | —       | Subjective driver-skill rating (no bounds enforced by the schema).         |
| `score`                    | `INTEGER`        | `0`     | Estimated teleop score contribution assigned to the team.                  |
| `notes`                    | `TEXT`           | —       | Free-text scouting notes.                                                   |
| `created_at`               | `TIMESTAMP`      | `CURRENT_TIMESTAMP` | Record creation timestamp.                                     |

**Constraints:**
- `uq_teleop_match_team`: `UNIQUE (event_key, match_key, team_key)`.
- `CHECK` on `coral_precision` enforcing the `[0, 100]` range.

---

## `pit_scout`

One row per (event, team): data collected in the **pit** before/during the event — robot description and a photo.

| Column         | Type          | Default | Description                                                  |
|----------------|---------------|---------|------------------------------------------------------------------|
| `id`           | `SERIAL`      | —       | Primary key.                                                       |
| `team_key`     | `VARCHAR(50)` | —       | TBA team key. `UNIQUE`, `NOT NULL`.                                |
| `description`  | `TEXT`        | —       | Free-text description of the robot/team strategy.                  |
| `img_url`      | `TEXT`        | —       | URL to a photo of the robot.                                       |
| `created_at`   | `TIMESTAMP`   | `CURRENT_TIMESTAMP` | Record creation timestamp.                                |

> ⚠️ Note that, unlike the other two tables, `pit_scout` defines
> `team_key` as **globally** `UNIQUE` (not `UNIQUE(event_key, team_key)`) —
> and doesn't even have an `event_key` column. This means that, as the
> schema is currently defined, **only one pit scouting record can exist
> per team across the entire history of the database**, even though the
> code in `app/api/routes/scout.py` treats `pit_scout` as if it had an
> `event_key` column and a composite `event_key_team_key` key (see "Known
> issues" in the main README).

---

## How to apply the schema

```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/database-schema.sql
```

The script only runs three `CREATE TABLE` statements; there's no `DROP TABLE IF EXISTS` or migration tooling — running it more than once against the same database will fail with a "table already exists" error. For environments where the schema evolves over time, adopting a migration tool (e.g. Alembic) going forward is recommended.