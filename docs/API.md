# API Reference — FRCScouter7563

All routes below are registered in `app/app.py`. The **Teams**, **Events**, **Districts**, **Matchs**, **Insights**, and **Regional advancement** route groups are a thin proxy/mirror of the [The Blue Alliance API v3](https://www.thebluealliance.com/apidocs/v3); check the official TBA documentation for the exact shape of each response payload. **Scout** is the only group that reads/writes to the team's own PostgreSQL database.

> Local base URL: `http://localhost:8000`
> Interactive docs: `/docs` (Swagger) and `/redoc`

---

## Diagnostics

| Method | Route          | Description                                    |
|--------|----------------|--------------------------------------------------|
| HEAD   | `/`            | Checks whether the API is up.                     |
| GET    | `/status-db`   | Tests the PostgreSQL connection.                  |
| GET    | `/status-tba`  | Forwards the TBA API status (`/status`).          |
| GET    | `/favicon.ico` | Serves the static favicon.                        |

---

## Teams (`/teams`)

| Method | Route                                                       | Description                                                              |
|--------|--------------------------------------------------------------|------------------------------------------------------------------------------|
| GET    | `/teams/team/{team_key}`                                     | Full `Team` object.                                                          |
| GET    | `/teams/team/{team_key}/simple`                               | `Team_Simple` object.                                                        |
| GET    | `/teams/team/{team_key}/years_participated`                   | Years the team competed in at least one event.                              |
| GET    | `/teams/team/{team_key}/districts`                            | Districts the team has participated in, by year.                            |
| GET    | `/teams/team/{team_key}/robots`                               | Year/robot-name pairs for every year the team named a robot.                |
| GET    | `/teams/team/{team_key}/history`                              | Full history (events and awards).                                           |
| GET    | `/teams/team/{team_key}/social_media`                         | The team's social media objects.                                             |
| GET    | `/teams/team/{team_key}/awards`                               | All awards the team has won (all time).                                     |
| GET    | `/teams/team/{team_key}/awards/{year}`                        | Awards won in a specific year.                                               |
| GET    | `/teams/team/{team_key}/media/{year}`                         | Team media for a specific year.                                              |
| GET    | `/teams/team/{team_key}/media/tag/{media_tag}`                | Media filtered by tag.                                                       |
| GET    | `/teams/team/{team_key}/media/tag/{media_tag}/{year}`         | Media filtered by tag and year.                                              |
| GET    | `/teams/team/{team_key}/events`                               | All events the team has ever competed at.                                   |
| GET    | `/teams/team/{team_key}/events/simple`                        | Short-form version of the events list.                                      |
| GET    | `/teams/team/{team_key}/events/keys`                          | Event keys only.                                                             |
| GET    | `/teams/team/{team_key}/events/{year}/statuses`               | Key-value map of the team's status per event, for a given year.             |
| GET    | `/teams/team/{team_key}/events/{year}/keys`                   | Event keys for events competed at in a given year.                          |
| GET    | `/teams/team/{team_key}/events/{year}`                        | Events (short form) competed at in a given year.                            |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches`            | The team's matches at a specific event.                                     |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches/simple`     | Short-form version of the matches.                                          |
| GET    | `/teams/team/{team_key}/event/{event_key}/matches/keys`       | Match keys.                                                                  |
| GET    | `/teams/team/{team_key}/matches/{year}/keys`                  | Keys for all of the team's matches in a given year.                         |
| GET    | `/teams/team/{team_key}/matches/{year}`                       | All of the team's matches in a given year.                                  |
| GET    | `/teams/team/{team_key}/event/{event_key}/awards`             | Awards the team won at a specific event.                                    |
| GET    | `/teams/team/{team_key}/event/{event_key}/status`             | The team's competition rank and status at an event.                         |
| GET    | `/teams/{page_num}/simple`                                    | Paginated `Team_Simple` list (groups of 500).                               |
| GET    | `/teams/{page_num}/keys`                                      | Paginated list of team keys.                                                 |
| GET    | `/teams/{page_num}`                                           | Paginated list of `Team` objects.                                            |
| GET    | `/teams/{year}/{page_num}/simple`                             | Teams (short form) that competed in a given year, paginated.                |
| GET    | `/teams/{year}/{page_num}/keys`                               | Keys of teams that competed in a given year, paginated.                     |
| GET    | `/teams/{year}/{page_num}`                                    | Teams that competed in a given year, paginated.                             |

> ⚠️ The specific routes (`/team/{team_key}/...`) are registered **before** the generic paginated routes (`/{page_num}`, `/{year}/{page_num}`) on purpose — see the comment at the top of `app/api/routes/teams.py`.

## Events (`/events`)

| Method | Route                                                              | Description                                                             |
|--------|-----------------------------------------------------------------------|------------------------------------------------------------------------------|
| GET    | `/events/{year}`                                                        | All events for a given year.                                                 |
| GET    | `/events/{year}/simple`                                                 | Short-form version.                                                          |
| GET    | `/events/{year}/keys`                                                   | Event keys only.                                                             |
| GET    | `/events/event/{event_key}`                                            | Full `Event` object.                                                         |
| GET    | `/events/event/{event_key}/simple`                                       | `Event_Simple` object.                                                       |
| GET    | `/events/event/{event_key}/alliances`                                    | Elimination-round alliances.                                                 |
| GET    | `/events/event/{event_key}/awards`                                       | Awards from the event.                                                       |
| GET    | `/events/event/{event_key}/matches`                                      | All matches for the event.                                                   |
| GET    | `/events/event/{event_key}/matches/simple`                               | Short-form version of the matches.                                           |
| GET    | `/events/event/{event_key}/matches/keys`                                 | Match keys.                                                                  |
| GET    | `/events/event/{event_key}/matches/timeseries`                           | Match keys that have Zebra timeseries data.                                  |
| GET    | `/events/event/{event_key}/rankings`                                     | Team rankings at the event.                                                  |
| GET    | `/events/event/{event_key}/oprs`                                         | OPR, DPR, and CCWM for teams at the event.                                   |
| GET    | `/events/event/{event_key}/coprs`                                         | Component OPRs for teams.                                                    |
| GET    | `/events/event/{event_key}/dprs`                                          | DPRs for teams (named `district_points` in the implementation).             |
| GET    | `/events/event/{event_key}/advancement_points`                            | District/regional advancement points toward the Championship.               |
| GET    | `/events/event/{event_key}/regional_champs_pool_points`                   | Points toward the Championship qualification pool (2025+ Regionals).        |
| GET    | `/events/event/{event_key}/event_insights`                                | Year-specific insights (qual and playoff).                                   |
| GET    | `/events/event/{event_key}/predictions`                                   | TBA-generated match predictions.                                             |
| GET    | `/events/event/{event_key}/teams`                                         | Teams that competed at the event.                                            |
| GET    | `/events/event/{event_key}/teams/simple`                                  | Short-form version of the teams.                                             |
| GET    | `/events/event/{event_key}/teams/keys`                                    | Team keys.                                                                    |
| GET    | `/events/event/{event_key}/teams/statuses`                                | Key-value map of every team's status at the event.                          |
| GET    | `/events/event/{event_key}/team_media`                                    | Media for every team at the event.                                           |

## Districts (`/districts`)

| Method | Route                                                        | Description                                                       |
|--------|------------------------------------------------------------------|-------------------------------------------------------------------------|
| GET    | `/districts/{year}`                                                | Districts and their keys for a given year.                              |
| GET    | `/districts/{district_key}/events`                                  | Events in a district.                                                    |
| GET    | `/districts/{district_key}/events/simple`                          | Short-form version.                                                      |
| GET    | `/districts/{district_key}/events/keys`                            | Event keys only.                                                         |
| GET    | `/districts/{district_key}/teams`                                   | Teams in a district.                                                     |
| GET    | `/districts/{district_key}/teams/simple`                            | Short-form version.                                                      |
| GET    | `/districts/{district_key}/teams/keys`                              | Team keys only.                                                          |
| GET    | `/districts/{district_key}/rankings`                                 | Team district rankings.                                                  |
| GET    | `/districts/{district_key}/awards`                                   | All awards in the district.                                              |
| GET    | `/districts/{district_key}/advancement`                              | Per-team advancement info within the district.                          |
| GET    | `/districts/{district_abbreviation}/history`                         | District history across years.                                          |
| GET    | `/districts/{district_abbreviation}/dcmp_history`                     | DCMP (District Championship) events and awards.                         |
| GET    | `/districts/{district_abbreviation}/insights`                        | District insights.                                                       |

## Matchs (`/matchs`)

| Method | Route                                      | Description                                                |
|--------|------------------------------------------------|-----------------------------------------------------------------|
| GET    | `/matchs/{match_key}`                            | Full `Match` object.                                             |
| GET    | `/matchs/{match_key}/simple`                     | `Match_Simple` object.                                           |
| GET    | `/matchs/{match_key}/timeseries`                  | Game-specific Zebra timeseries data for the match.               |
| GET    | `/matchs/{match_key}/zebra_motionworks`           | Zebra MotionWorks positional data for the match.                 |

## Insights (`/insights`)

| Method | Route                                                                | Description                                                            |
|--------|--------------------------------------------------------------------------|------------------------------------------------------------------------------|
| GET    | `/insights/leaderboards/{year}`                                            | `LeaderboardInsight` objects (`year=0` for all-time).                        |
| GET    | `/insights/notables/{year}`                                                | `NotablesInsight` objects (`year=0` for all-time).                           |
| GET    | `/insights/{year}`                                                         | All `Insight` objects for a year, across every category.                    |
| GET    | `/insights/{year}/{category}`                                             | Insights for a year filtered by category (`leaderboard`/`streak`/`timeseries`).|
| GET    | `/insights/{year}/district/{district_abbreviation}`                        | Insights for a year, filtered by district.                                  |
| GET    | `/insights/{year}/{category}/district/{district_abbreviation}`             | InsightV2 filtered by year, category, and district.                         |

## Regional advancement (`/regional_advancement`)

| Method | Route                                                | Description                                                              |
|--------|----------------------------------------------------------|-------------------------------------------------------------------------------|
| GET    | `/regional_advancement/{year}`                              | Per-team advancement info to the FIRST Championship.                          |
| GET    | `/regional_advancement/{year}/rankings`                     | Team rankings in the regional pool, for a given year.                         |
| GET    | `/regional_advancement/{year}/rankings/{max_num}`           | Top N regional-pool rankings (slices the result of the route above).          |

---

## Scout (`/scout`)

This is the only route group that accesses the team's own PostgreSQL database (via `app/core/db.py`), rather than simply forwarding calls to TBA. See [`DATABASE.md`](DATABASE.md) for the schema of the tables involved.

> ⚠️ **Warning:** the "by scout key" endpoints below rely on columns
> (`scout_auto_key`, `scout_teleop_key`, `pit_scout_key`) that **do not
> exist** in `sql/database-schema.sql` as currently checked into the
> repository. See the "Known issues" section in the main README before
> using these routes in production.

### Auto scout (autonomous)

| Method | Route                                                    | Description                                                                    |
|--------|---------------------------------------------------------------|--------------------------------------------------------------------------------------|
| POST   | `/scout/add/auto/2025`                                          | Creates a new autonomous-period scouting entry.                                       |
| GET    | `/scout/auto/scout_key/{scout_key}`                              | Look up by composite key `match_key_team_key`.                                        |
| GET    | `/scout/auto/event/{event_key}`                                  | All entries for an event.                                                              |
| GET    | `/scout/auto/match/{match_key}`                                  | All entries (every team) for a match.                                                 |
| GET    | `/scout/auto/match/{match_key}/team/{team_key}`                   | A single team's entry for a specific match.                                           |
| GET    | `/scout/auto/team/{team_key}`                                    | Every entry ever recorded for a team.                                                 |
| GET    | `/scout/auto/team/{team_key}/event/{event_key}`                   | A team's entries within an event.                                                     |
| GET    | `/scout/auto/team/{team_key}/match/{match_key}`                   | A team's entry for a match (equivalent to the endpoint above with swapped params).     |
| GET    | `/scout/auto/matches/keys`                                       | Lists the `match_key` values with an auto scouting entry (no `DISTINCT`).             |
| DELETE | `/scout/delete/auto/match/{match_key}/team/{team_key}`             | Deletes a team's entry for a match.                                                   |
| DELETE | `/scout/delete/auto/key/{scout_key}`                              | Deletes by composite key.                                                             |

**Request body** (`POST /scout/add/auto/2025`), `AutoScout` model:

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
  "notes": "Left the starting line quickly."
}
```

### Teleop scout (teleop + endgame)

| Method | Route                                                              | Description                                                              |
|--------|-------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| POST   | `/scout/add/teleop/2025`                                                  | Creates a new teleop-period scouting entry.                                    |
| GET    | `/scout/teleop/scout_key/{scout_key}`                                      | Look up by composite key `match_key_team_key`.                                 |
| GET    | `/scout/teleop/event/{event_key}`                                          | All entries for an event.                                                       |
| GET    | `/scout/teleop/match/{match_key}`                                          | All entries (every team) for a match.                                          |
| GET    | `/scout/teleop/match/{match_key}/team/{team_key}`                           | A single team's entry for a specific match.                                    |
| GET    | `/scout/teleop/team/{team_key}/event/{event_key}`                           | A team's entries within an event.                                              |
| GET    | `/scout/teleop/matches/keys`                                                | Lists the `match_key` values with a teleop scouting entry (no `DISTINCT`).     |
| DELETE | `/scout/delete/teleop/match/{match_key}/team/{team_key}`                     | Deletes a team's entry for a match.                                            |
| DELETE | `/scout/delete/teleop/key/{scout_key}`                                      | Deletes by composite key.                                                      |

**Request body** (`POST /scout/add/teleop/2025`), `TeleopScout` model:

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
  "notes": "Consistent robot, no issues."
}
```

### Pit scout

| Method | Route                                                        | Description                                                              |
|--------|-------------------------------------------------------------------|--------------------------------------------------------------------------------|
| POST   | `/scout/add/pit/`                                                    | Creates a new pit scouting entry.                                              |
| GET    | `/scout/pit/scout_key/{scout_key}`                                    | Look up by composite key `event_key_team_key`.                                 |
| GET    | `/scout/pit/event/{event_key}`                                        | All entries for an event.                                                       |
| GET    | `/scout/pit/team/{team_key}`                                          | Every entry ever recorded for a team.                                          |
| GET    | `/scout/pit/team/{team_key}/event/{event_key}`                         | A team's entry for a specific event.                                           |
| GET    | `/scout/pit/events/keys`                                              | Lists the distinct `event_key` values with pit scouting (`DISTINCT`, sorted).  |
| DELETE | `/scout/delete/pit/team/{team_key}/event/{event_key}`                   | Deletes a team's entry for an event.                                           |
| DELETE | `/scout/delete/pit/key/{scout_key}`                                     | Deletes by composite key.                                                      |

**Request body** (`POST /scout/add/pit/`), `PitScout` model:

```json
{
  "event_key": "2025sao",
  "team_key": "frc7563",
  "description": "Swerve drive, 4-stage elevator, coral and algae claw.",
  "img_url": "https://example.com/photos/frc7563.jpg"
}
```

### Error responses (delete)

All `DELETE` routes return:

- `{"message": "Scout deleted successfully"}` (or `"Pit scout deleted successfully"`) when a row was removed.
- `{"message": "Scout not found"}` (or `"Pit scout not found"`) when no row matched the parameters — **this is returned with HTTP 200**, not 404, so clients need to check the response body, not just the status code.