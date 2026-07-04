# Banco de dados — FRCScouter7563

O banco de dados é **PostgreSQL** e armazena apenas os dados de scouting coletados pela própria equipe (dados vindos do The Blue Alliance nunca são persistidos localmente — são sempre buscados on-demand através da `TBAClient`).

O DDL completo está em [`sql/database-schema.sql`](../sql/database-schema.sql). Este documento descreve cada tabela campo a campo.

## Diagrama lógico

```
auto_scout_reefscape           teleop_scout_reefscape           pit_scout
┌──────────────────────┐       ┌──────────────────────┐        ┌──────────────────────┐
│ id (PK)               │       │ id (PK)               │        │ id (PK)               │
│ event_key             │       │ event_key             │        │ team_key (UNIQUE)     │
│ match_key             │       │ match_key             │        │ description           │
│ team_key              │       │ team_key              │        │ img_url               │
│ year                  │       │ year                  │        │ created_at            │
│ l1..l4                │       │ l1..l4                │        └──────────────────────┘
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
└──────────────────────┘       │ score                  │
                                │ notes                  │
                                │ created_at             │
                                │ UNIQUE(event,match,     │
                                │        team)            │
                                └──────────────────────┘
```

---

## `auto_scout_reefscape`

Uma linha por combinação (evento, partida, time): o que aquele robô fez durante o período **autônomo** da temporada 2025 Reefscape.

| Coluna             | Tipo             | Default | Descrição                                                                 |
|--------------------|------------------|---------|-----------------------------------------------------------------------------|
| `id`               | `SERIAL`         | —       | Chave primária.                                                             |
| `event_key`        | `VARCHAR(50)`    | —       | Chave do evento na TBA (ex.: `2025sao`). `NOT NULL`.                        |
| `match_key`        | `VARCHAR(50)`    | —       | Chave da partida na TBA (ex.: `2025sao_qm12`). `NOT NULL`.                  |
| `team_key`         | `VARCHAR(50)`    | —       | Chave do time na TBA (ex.: `frc7563`). `NOT NULL`.                          |
| `year`             | `INTEGER`        | —       | Ano da temporada. `NOT NULL`.                                               |
| `l1`               | `INTEGER`        | `0`     | Coral marcado no nível 1 do reef durante o autônomo.                        |
| `l2`               | `INTEGER`        | `0`     | Coral marcado no nível 2.                                                   |
| `l3`               | `INTEGER`        | `0`     | Coral marcado no nível 3.                                                   |
| `l4`               | `INTEGER`        | `0`     | Coral marcado no nível 4.                                                   |
| `coral_misseds`    | `INTEGER`        | `0`     | Quantidade de tentativas de marcar coral que falharam.                      |
| `coral_precision`  | `DECIMAL(5,2)`   | `0`     | Precisão de marcação de coral (%), com `CHECK (0 <= valor <= 100)`.         |
| `algae_removed`    | `INTEGER`        | `0`     | Algas removidas do reef.                                                    |
| `algae_net`        | `INTEGER`        | `0`     | Algas marcadas na rede (net).                                               |
| `algae_processor`  | `INTEGER`        | `0`     | Algas marcadas no processador.                                              |
| `region_scored`    | `JSONB`          | —       | Payload livre descrevendo *onde* no campo a pontuação ocorreu.              |
| `score`            | `INTEGER`        | `0`     | Pontuação estimada de autônomo atribuída ao time.                           |
| `startline`        | `BOOLEAN`        | `FALSE` | Se o robô saiu da linha de partida (mobilidade).                            |
| `notes`            | `TEXT`           | —       | Observações livres do scout.                                                |
| `created_at`       | `TIMESTAMP`      | `CURRENT_TIMESTAMP` | Data/hora de criação do registro.                                |

**Constraints:**
- `uq_auto_match_team`: `UNIQUE (event_key, match_key, team_key)` — impede duas entradas para o mesmo time na mesma partida do mesmo evento.
- `CHECK` em `coral_precision` garantindo o intervalo `[0, 100]`.

---

## `teleop_scout_reefscape`

Uma linha por combinação (evento, partida, time): o que aquele robô fez durante o período **teleoperado** e a **subida final (climb)**.

| Coluna                    | Tipo             | Default | Descrição                                                              |
|---------------------------|------------------|---------|---------------------------------------------------------------------------|
| `id`                       | `SERIAL`         | —       | Chave primária.                                                            |
| `event_key`                | `VARCHAR(50)`    | —       | Chave do evento na TBA. `NOT NULL`.                                        |
| `match_key`                | `VARCHAR(50)`    | —       | Chave da partida na TBA. `NOT NULL`.                                       |
| `team_key`                 | `VARCHAR(50)`    | —       | Chave do time na TBA. `NOT NULL`.                                          |
| `year`                     | `INTEGER`        | —       | Ano da temporada. `NOT NULL`.                                              |
| `l1`..`l4`                  | `INTEGER`        | `0`     | Coral marcado em cada nível do reef durante o teleop.                      |
| `coral_misseds`            | `INTEGER`        | `0`     | Tentativas de marcar coral que falharam.                                   |
| `coral_precision`          | `DECIMAL(5,2)`   | `0`     | Precisão de marcação de coral (%), `CHECK (0 <= valor <= 100)`.            |
| `algae_removed`            | `INTEGER`        | `0`     | Algas removidas do reef.                                                   |
| `algae_net`                | `INTEGER`        | `0`     | Algas marcadas na rede.                                                    |
| `algae_processor`          | `INTEGER`        | `0`     | Algas marcadas no processador.                                             |
| `climb`                    | `VARCHAR(30)`    | —       | Resultado da subida no endgame (texto livre, ex.: `"deep"`, `"shallow"`, `"park"`, `"none"`). |
| `collected_coral_floor`    | `BOOLEAN`        | `FALSE` | Se o robô coletou coral do chão.                                           |
| `collected_coral_station`  | `BOOLEAN`        | `FALSE` | Se o robô coletou coral da estação do operador humano.                     |
| `collected_algae_reef`     | `BOOLEAN`        | `FALSE` | Se o robô coletou algas do reef.                                           |
| `issues`                   | `BOOLEAN`        | `FALSE` | Se o robô apresentou algum problema/falha.                                 |
| `issues_notes`             | `TEXT`           | —       | Descrição livre do problema, se houver.                                    |
| `defended`                 | `BOOLEAN`        | `FALSE` | Se o robô fez defesa durante a partida.                                    |
| `driver_rating`            | `INTEGER`        | —       | Nota subjetiva de habilidade do piloto (sem limites impostos pelo schema). |
| `score`                    | `INTEGER`        | `0`     | Pontuação estimada de teleop atribuída ao time.                            |
| `notes`                    | `TEXT`           | —       | Observações livres do scout.                                               |
| `created_at`               | `TIMESTAMP`      | `CURRENT_TIMESTAMP` | Data/hora de criação do registro.                               |

**Constraints:**
- `uq_teleop_match_team`: `UNIQUE (event_key, match_key, team_key)`.
- `CHECK` em `coral_precision` garantindo o intervalo `[0, 100]`.

---

## `pit_scout`

Uma linha por (evento, time): dados coletados no **pit** antes/durante o evento — descrição do robô e uma foto.

| Coluna         | Tipo          | Default | Descrição                                                   |
|----------------|---------------|---------|-----------------------------------------------------------------|
| `id`           | `SERIAL`      | —       | Chave primária.                                                  |
| `team_key`     | `VARCHAR(50)` | —       | Chave do time na TBA. `UNIQUE`, `NOT NULL`.                      |
| `description`  | `TEXT`        | —       | Descrição livre do robô/estratégia da equipe.                    |
| `img_url`      | `TEXT`        | —       | URL de uma foto do robô.                                         |
| `created_at`   | `TIMESTAMP`   | `CURRENT_TIMESTAMP` | Data/hora de criação do registro.                       |

> ⚠️ Note que, ao contrário das outras duas tabelas, `pit_scout` define
> `team_key` como `UNIQUE` **global** (não `UNIQUE(event_key, team_key)`) —
> e nem sequer possui uma coluna `event_key`. Isso significa que, tal como o
> schema está definido hoje, **só é possível existir um único registro de
> pit scouting por time em todo o histórico do banco**, mesmo que o código
> em `app/api/routes/scout.py` trate `pit_scout` como se tivesse uma coluna
> `event_key` e uma chave composta `event_key_team_key` (veja "Problemas
> conhecidos" no README principal).

---

## Como aplicar o schema

```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f sql/database-schema.sql
```

O script apenas executa três `CREATE TABLE`; não há `DROP TABLE IF EXISTS` nem migrações — rodá-lo mais de uma vez contra o mesmo banco falhará com erro de tabela já existente. Para ambientes que evoluem o schema, recomenda-se adotar uma ferramenta de migração (ex.: Alembic) no futuro.
