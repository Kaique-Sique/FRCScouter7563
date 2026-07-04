# Referência da API — FRCScouter7563

Todas as rotas abaixo estão registradas em `app/app.py`. As rotas dos grupos **Teams**, **Events**, **Districts**, **Matchs**, **Insights** e **Regional advancement** são um espelho (thin proxy) da [API v3 do The Blue Alliance](https://www.thebluealliance.com/apidocs/v3); consulte a documentação oficial da TBA para o formato exato de cada payload de resposta. O grupo **Scout** é a única parte que lê/escreve no PostgreSQL da equipe.

> Base URL local: `http://localhost:8000`
> Documentação interativa: `/docs` (Swagger) e `/redoc`

---

## Diagnóstico

| Método | Rota          | Descrição                                    |
|--------|---------------|-----------------------------------------------|
| HEAD   | `/`           | Testa se a API está no ar.                    |
| GET    | `/status-db`  | Testa a conexão com o PostgreSQL.             |
| GET    | `/status-tba` | Repassa o status (`/status`) da API do TBA.   |
| GET    | `/favicon.ico`| Serve o favicon estático.                     |

---

## Teams (`/teams`)

| Método | Rota                                                      | Descrição                                                             |
|--------|-----------------------------------------------------------|-------------------------------------------------------------------------|
| GET    | `/teams/team/{team_key}`                                  | Objeto `Team` completo.                                                 |
| GET    | `/teams/team/{team_key}/simple`                            | Objeto `Team_Simple`.                                                   |
| GET    | `/teams/team/{team_key}/years_participated`                | Anos em que o time competiu em pelo menos um evento.                    |
| GET    | `/teams/team/{team_key}/districts`                         | Distritos que o time participou, por ano.                               |
| GET    | `/teams/team/{team_key}/robots`                            | Pares ano/nome do robô para cada ano com robô nomeado.                  |
| GET    | `/teams/team/{team_key}/history`                           | Histórico completo (eventos e prêmios).                                 |
| GET    | `/teams/team/{team_key}/social_media`                      | Objetos de redes sociais do time.                                       |
| GET    | `/teams/team/{team_key}/awards`                            | Todos os prêmios ganhos pelo time (todos os tempos).                    |
| GET    | `/teams/team/{team_key}/awards/{year}`                     | Prêmios ganhos em um ano específico.                                    |
| GET    | `/teams/team/{team_key}/media/{year}`                      | Mídias do time em um ano específico.                                    |
| GET    | `/teams/team/{team_key}/media/tag/{media_tag}`             | Mídias filtradas por tag.                                                |
| GET    | `/teams/team/{team_key}/media/tag/{media_tag}/{year}`      | Mídias filtradas por tag e ano.                                          |
| GET    | `/teams/team/{team_key}/events`                            | Todos os eventos que o time já competiu.                                |
| GET    | `/teams/team/{team_key}/events/simple`                     | Versão simplificada da lista de eventos.                                |
| GET    | `/teams/team/{team_key}/events/keys`                       | Apenas as chaves dos eventos.                                           |
| GET    | `/teams/team/{team_key}/events/{year}/statuses`            | Mapa chave-valor de status do time por evento, em um ano.                |
| GET    | `/teams/team/{team_key}/events/{year}/keys`                | Chaves dos eventos disputados em um ano.                                 |
| GET    | `/teams/team/{team_key}/events/{year}`                     | Eventos (forma simplificada) disputados em um ano.                       |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches`         | Partidas do time em um evento específico.                                |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches/simple`  | Versão simplificada das partidas.                                        |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches/keys`    | Chaves das partidas.                                                     |
| GET    | `/teams/team/{team_key}/matches/{year}/keys`                | Chaves de todas as partidas do time em um ano.                           |
| GET    | `/teams/team/{team_key}/matches/{year}`                     | Todas as partidas do time em um ano.                                     |
| GET    | `/teams/team/{team_key}/event/{event_key}/awards`           | Prêmios do time em um evento específico.                                 |
| GET    | `/teams/team/{team_key}/event/{event_key}/status`           | Rank e status de competição do time em um evento.                        |
| GET    | `/teams/{page_num}/simple`                                  | Lista `Team_Simple` paginada (grupos de 500).                            |
| GET    | `/teams/{page_num}/keys`                                    | Lista de chaves de times, paginada.                                      |
| GET    | `/teams/{page_num}`                                         | Lista de objetos `Team`, paginada.                                       |
| GET    | `/teams/{year}/{page_num}/simple`                            | Times (forma simplificada) que competiram em um ano, paginado.           |
| GET    | `/teams/{year}/{page_num}/keys`                              | Chaves de times que competiram em um ano, paginado.                      |
| GET    | `/teams/{year}/{page_num}`                                   | Times que competiram em um ano, paginado.                                |

> ⚠️ As rotas específicas (`/team/{team_key}/...`) são registradas **antes** das rotas genéricas de paginação (`/{page_num}`, `/{year}/{page_num}`) propositalmente — veja o comentário no topo de `app/api/routes/teams.py`.

## Events (`/events`)

| Método | Rota                                                          | Descrição                                                       |
|--------|-----------------------------------------------------------------|--------------------------------------------------------------------|
| GET    | `/events/{year}`                                                 | Todos os eventos de um ano.                                        |
| GET    | `/events/{year}/simple`                                          | Versão simplificada.                                                |
| GET    | `/events/{year}/keys`                                            | Apenas as chaves dos eventos.                                       |
| GET    | `/events/event/{event_key}`                                     | Objeto `Event` completo.                                            |
| GET    | `/events/event/{event_key}/simple`                                | Objeto `Event_Simple`.                                              |
| GET    | `/events/event/{event_key}/alliances`                             | Alianças da fase eliminatória.                                      |
| GET    | `/events/event/{event_key}/awards`                                | Prêmios do evento.                                                  |
| GET    | `/events/event/{event_key}/matches`                               | Todas as partidas do evento.                                        |
| GET    | `/events/event/{event_key}/matches/simple`                        | Versão simplificada das partidas.                                   |
| GET    | `/events/event/{event_key}/matches/keys`                          | Chaves das partidas.                                                |
| GET    | `/events/event/{event_key}/matches/timeseries`                    | Chaves de partidas com dados Zebra timeseries.                      |
| GET    | `/events/event/{event_key}/rankings`                              | Rankings dos times no evento.                                       |
| GET    | `/events/event/{event_key}/oprs`                                  | OPR, DPR e CCWM dos times no evento.                                 |
| GET    | `/events/event/{event_key}/coprs`                                  | Component OPRs dos times.                                           |
| GET    | `/events/event/{event_key}/dprs`                                   | DPRs dos times (rota nomeada `district_points` na implementação).    |
| GET    | `/events/event/{event_key}/advancement_points`                     | Pontos de avanço distrital/regional para o Championship.            |
| GET    | `/events/event/{event_key}/regional_champs_pool_points`            | Pontos para o pool de classificação do Championship (2025+, Regionais).|
| GET    | `/events/event/{event_key}/event_insights`                         | Insights específicos do ano (qual e playoff).                       |
| GET    | `/events/event/{event_key}/predictions`                            | Previsões de partidas geradas pelo TBA.                              |
| GET    | `/events/event/{event_key}/teams`                                  | Times que competiram no evento.                                     |
| GET    | `/events/event/{event_key}/teams/simple`                           | Versão simplificada dos times.                                      |
| GET    | `/events/event/{event_key}/teams/keys`                             | Chaves dos times.                                                    |
| GET    | `/events/event/{event_key}/teams/statuses`                         | Mapa chave-valor de status de todos os times no evento.              |
| GET    | `/events/event/{event_key}/team_media`                             | Mídias de todos os times no evento.                                  |

## Districts (`/districts`)

| Método | Rota                                                        | Descrição                                                    |
|--------|---------------------------------------------------------------|------------------------------------------------------------------|
| GET    | `/districts/{year}`                                           | Distritos e suas chaves em um ano.                                |
| GET    | `/districts/{district_key}/events`                             | Eventos de um distrito.                                          |
| GET    | `/districts/{district_key}/events/simple`                      | Versão simplificada.                                              |
| GET    | `/districts/{district_key}/events/keys`                        | Apenas as chaves dos eventos.                                     |
| GET    | `/districts/{district_key}/teams`                              | Times de um distrito.                                             |
| GET    | `/districts/{district_key}/teams/simple`                       | Versão simplificada.                                              |
| GET    | `/districts/{district_key}/teams/keys`                         | Apenas as chaves dos times.                                       |
| GET    | `/districts/{district_key}/rankings`                            | Rankings distritais dos times.                                    |
| GET    | `/districts/{district_key}/awards`                              | Todos os prêmios do distrito.                                     |
| GET    | `/districts/{district_key}/advancement`                         | Informação de avanço por time no distrito.                        |
| GET    | `/districts/{district_abbreviation}/history`                    | Histórico do distrito ao longo dos anos.                          |
| GET    | `/districts/{district_abbreviation}/dcmp_history`                | Eventos e prêmios do DCMP (District Championship).                |
| GET    | `/districts/{district_abbreviation}/insights`                    | Insights do distrito.                                             |

## Matchs (`/matchs`)

| Método | Rota                                     | Descrição                                            |
|--------|--------------------------------------------|---------------------------------------------------------|
| GET    | `/matchs/{match_key}`                       | Objeto `Match` completo.                                 |
| GET    | `/matchs/{match_key}/simple`                | Objeto `Match_Simple`.                                   |
| GET    | `/matchs/{match_key}/timeseries`             | Dados Zebra timeseries específicos do jogo, da partida.  |
| GET    | `/matchs/{match_key}/zebra_motionworks`      | Dados posicionais Zebra MotionWorks da partida.          |

## Insights (`/insights`)

| Método | Rota                                                             | Descrição                                                       |
|--------|---------------------------------------------------------------------|----------------------------------------------------------------------|
| GET    | `/insights/leaderboards/{year}`                                      | Objetos `LeaderboardInsight` (`year=0` para todos os tempos).         |
| GET    | `/insights/notables/{year}`                                          | Objetos `NotablesInsight` (`year=0` para todos os tempos).            |
| GET    | `/insights/{year}`                                                   | Todos os objetos `Insight` de um ano, em todas as categorias.         |
| GET    | `/insights/{year}/{category}`                                        | Insights de um ano filtrados por categoria (`leaderboard`/`streak`/`timeseries`).|
| GET    | `/insights/{year}/district/{district_abbreviation}`                   | Insights de um ano, filtrados por distrito.                            |
| GET    | `/insights/{year}/{category}/district/{district_abbreviation}`        | Insights V2 filtrados por ano, categoria e distrito.                   |

## Regional advancement (`/regional_advancement`)

| Método | Rota                                             | Descrição                                                          |
|--------|-----------------------------------------------------|------------------------------------------------------------------------|
| GET    | `/regional_advancement/{year}`                       | Informação de avanço ao FIRST Championship, por time.                  |
| GET    | `/regional_advancement/{year}/rankings`               | Rankings dos times no pool regional, para um ano.                       |
| GET    | `/regional_advancement/{year}/rankings/{max_num}`     | Top N rankings do pool regional (recorta o resultado da rota anterior). |

---

## Scout (`/scout`)

Este é o único grupo de rotas que acessa o banco de dados PostgreSQL da equipe (via `app/core/db.py`), em vez de apenas repassar chamadas ao TBA. Veja [`DATABASE.md`](DATABASE.md) para o schema das tabelas envolvidas.

> ⚠️ **Atenção:** os endpoints "por scout key" abaixo dependem de colunas
> (`scout_auto_key`, `scout_teleop_key`, `pit_scout_key`) que **não existem**
> em `sql/database-schema.sql` no estado atual do repositório. Veja a seção
> "Problemas conhecidos" no README principal antes de usar essas rotas em
> produção.

### Auto scout (autônomo)

| Método | Rota                                                  | Descrição                                                          |
|--------|----------------------------------------------------------|-------------------------------------------------------------------------|
| POST   | `/scout/add/auto/2025`                                    | Cria uma entrada de scouting do período autônomo.                       |
| GET    | `/scout/auto/scout_key/{scout_key}`                        | Busca por chave composta `match_key_team_key`.                          |
| GET    | `/scout/auto/event/{event_key}`                            | Todas as entradas de um evento.                                         |
| GET    | `/scout/auto/match/{match_key}`                            | Todas as entradas (todos os times) de uma partida.                      |
| GET    | `/scout/auto/match/{match_key}/team/{team_key}`             | Entrada de um time em uma partida específica.                           |
| GET    | `/scout/auto/team/{team_key}`                              | Todas as entradas já registradas de um time.                            |
| GET    | `/scout/auto/team/{team_key}/event/{event_key}`             | Entradas de um time dentro de um evento.                                |
| GET    | `/scout/auto/team/{team_key}/match/{match_key}`             | Entrada de um time em uma partida (equivalente ao endpoint acima com parâmetros invertidos). |
| GET    | `/scout/auto/matches/keys`                                 | Lista as `match_key` com entrada de auto scouting (sem `DISTINCT`).      |
| DELETE | `/scout/delete/auto/match/{match_key}/team/{team_key}`       | Remove a entrada de um time em uma partida.                             |
| DELETE | `/scout/delete/auto/key/{scout_key}`                        | Remove pela chave composta.                                             |

**Corpo da requisição** (`POST /scout/add/auto/2025`), modelo `AutoScout`:

```json
{
  "event_key": "2025sao",
  "match_key": "2025sao_qm12",
  "team_key": "frc7563",
  "year": 2025,
  "l1": 0, "l2": 2, "l3": 1, "l4": 0,
  "coral_misseds": 1,
  "coral_precision": 75.0,
  "algae_removed": 1,
  "algae_net": 0,
  "algae_processor": 1,
  "region_scored": {"reef_face": "A", "branch": "L2"},
  "score": 10,
  "startline": true,
  "notes": "Saiu rápido da linha de partida."
}
```

### Teleop scout (teleoperado + endgame)

| Método | Rota                                                        | Descrição                                                     |
|--------|------------------------------------------------------------------|--------------------------------------------------------------------|
| POST   | `/scout/add/teleop/2025`                                          | Cria uma entrada de scouting do período teleoperado.                |
| GET    | `/scout/teleop/scout_key/{scout_key}`                              | Busca por chave composta `match_key_team_key`.                      |
| GET    | `/scout/teleop/event/{event_key}`                                  | Todas as entradas de um evento.                                     |
| GET    | `/scout/teleop/match/{match_key}`                                  | Todas as entradas (todos os times) de uma partida.                  |
| GET    | `/scout/teleop/match/{match_key}/team/{team_key}`                   | Entrada de um time em uma partida específica.                       |
| GET    | `/scout/teleop/team/{team_key}/event/{event_key}`                   | Entradas de um time dentro de um evento.                            |
| GET    | `/scout/teleop/matches/keys`                                        | Lista as `match_key` com entrada de teleop scouting (sem `DISTINCT`).|
| DELETE | `/scout/delete/teleop/match/{match_key}/team/{team_key}`             | Remove a entrada de um time em uma partida.                         |
| DELETE | `/scout/delete/teleop/key/{scout_key}`                              | Remove pela chave composta.                                         |

**Corpo da requisição** (`POST /scout/add/teleop/2025`), modelo `TeleopScout`:

```json
{
  "event_key": "2025sao",
  "match_key": "2025sao_qm12",
  "team_key": "frc7563",
  "year": 2025,
  "l1": 1, "l2": 3, "l3": 2, "l4": 1,
  "coral_misseds": 2,
  "coral_precision": 80.0,
  "algae_removed": 2,
  "algae_net": 1,
  "algae_processor": 0,
  "climb": "deep",
  "collected_coral_floor": true,
  "collected_coral_station": true,
  "collected_algae_reef": false,
  "issues": false,
  "issues_notes": null,
  "defended": false,
  "driver_rating": 4,
  "score": 45,
  "notes": "Robô consistente, sem intercorrências."
}
```

### Pit scout

| Método | Rota                                                    | Descrição                                                      |
|--------|--------------------------------------------------------------|----------------------------------------------------------------------|
| POST   | `/scout/add/pit/`                                              | Cria uma entrada de pit scouting.                                     |
| GET    | `/scout/pit/scout_key/{scout_key}`                              | Busca por chave composta `event_key_team_key`.                        |
| GET    | `/scout/pit/event/{event_key}`                                  | Todas as entradas de um evento.                                       |
| GET    | `/scout/pit/team/{team_key}`                                    | Todas as entradas já registradas de um time.                          |
| GET    | `/scout/pit/team/{team_key}/event/{event_key}`                   | Entrada de um time em um evento específico.                           |
| GET    | `/scout/pit/events/keys`                                        | Lista as `event_key` distintas com pit scouting (com `DISTINCT`, ordenado). |
| DELETE | `/scout/delete/pit/team/{team_key}/event/{event_key}`             | Remove a entrada de um time em um evento.                             |
| DELETE | `/scout/delete/pit/key/{scout_key}`                               | Remove pela chave composta.                                           |

**Corpo da requisição** (`POST /scout/add/pit/`), modelo `PitScout`:

```json
{
  "event_key": "2025sao",
  "team_key": "frc7563",
  "description": "Swerve drive, elevador de 4 estágios, garra de coral e algae.",
  "img_url": "https://exemplo.com/fotos/frc7563.jpg"
}
```

### Respostas de erro (deleção)

Todas as rotas `DELETE` retornam:

- `{"message": "Scout deleted successfully"}` (ou `"Pit scout deleted successfully"`) quando uma linha foi removida.
- `{"message": "Scout not found"}` (ou `"Pit scout not found"`) quando nenhuma linha correspondia aos parâmetros — **isso é retornado com HTTP 200**, não 404, então clientes precisam checar o corpo da resposta, não apenas o status code.
