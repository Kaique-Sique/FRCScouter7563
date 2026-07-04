"""In-house scouting data endpoints (auto, teleop, and pit scouting).

Unlike the other route modules (``teams``, ``events``, ``districts``,
``matchs``, ``insights``, ``regional_advancement``), which proxy read-only
requests to The Blue Alliance API, this module owns the team's *own*
PostgreSQL data: scouting entries collected by humans in the stands and in
the pits during a competition.

Three resources are exposed, each with create / read / delete endpoints:

- **Auto scout** (``/scout/add/auto/2025``, ``/scout/auto/...``) — one row
  per (match, team), describing what a robot did during the autonomous
  period. Backed by the ``auto_scout_reefscape`` table.
- **Teleop scout** (``/scout/add/teleop/2025``, ``/scout/teleop/...``) —
  one row per (match, team), describing the driver-controlled period and
  endgame climb. Backed by the ``teleop_scout_reefscape`` table.
- **Pit scout** (``/scout/add/pit/``, ``/scout/pit/...``) — one row per
  (event, team), describing the robot itself (mechanisms, photo, etc).
  Backed by the ``pit_scout`` table.

For auto and teleop scouting, a composite "scout key" is derived as
``f"{match_key}_{team_key}"`` (pit scouting uses ``f"{event_key}_{team_key}"``)
so a given team's entry for a given match/event can be looked up directly.

.. note::
    **Known schema/code mismatch:** the ``INSERT`` statements below write
    to (and the "get/delete by key" endpoints read from) a
    ``scout_auto_key`` / ``scout_teleop_key`` / ``pit_scout_key`` column
    that is **not** present in ``sql/database-schema.sql`` (which instead
    defines a plain ``id SERIAL PRIMARY KEY`` and a
    ``UNIQUE (event_key, match_key, team_key)`` constraint). Running these
    endpoints against the schema as currently checked in will raise a
    ``psycopg2.errors.UndefinedColumn`` error. Either add the missing
    ``*_key`` column(s) to the schema, or change these queries to use the
    existing composite unique constraint — this file only documents the
    current behavior, it does not change it.
"""

from fastapi import APIRouter, Depends
from psycopg2.extras import Json
from app.api.schemas.auto_scout_reefscape import AutoScout
from app.api.schemas.pit_scout import PitScout
from app.api.schemas.teleop_scout_reefscape import TeleopScout
from app.core.db import get_cursor

router = APIRouter(prefix="/scout", tags=["Scout"])

# ===================================
# AUTO - SCOUT CREATE
# ===================================

''' 2025 - REEFSCAPE '''
@router.post("/add/auto/2025")
def create_auto_scout(scout: AutoScout):
    """Create a new autonomous-period scouting entry.

    POST /scout/add/auto/2025

    The scout key is derived as ``f"{match_key}_{team_key}"`` and returned
    to the caller so it can be used later to fetch/delete this exact entry.

    :param scout: Auto scouting payload validated against
        :class:`~app.api.schemas.auto_scout_reefscape.AutoScout`.
    :type scout: AutoScout
    :return: ``{"scout_key": "<match_key>_<team_key>"}``.
    :rtype: dict
    """
    scout_key = f"{scout.match_key}_{scout.team_key}"

    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO auto_scout_reefscape (
                scout_auto_key,
                event_key,
                match_key,
                team_key,
                year,
                l1,
                l2,
                l3,
                l4,
                coral_misseds,
                coral_precision,
                algae_removed,
                algae_net,
                algae_processor,
                region_scored,
                score,
                startline,
                notes
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,
                %s,%s,%s,
                %s,%s,%s,%s
            )
            RETURNING scout_auto_key
            """,
            (
                scout_key,
                scout.event_key,
                scout.match_key,
                scout.team_key,
                scout.year,
                scout.l1,
                scout.l2,
                scout.l3,
                scout.l4,
                scout.coral_misseds,
                scout.coral_precision,
                scout.algae_removed,
                scout.algae_net,
                scout.algae_processor,
                Json(scout.region_scored),
                scout.score,
                scout.startline,
                scout.notes,
            )
        )

        return {"scout_key": cur.fetchone()[0]}
    
# ===================================
# AUTO - SCOUT GET
# ===================================

@router.get("/auto/scout_key/{scout_key}")
def get_scout_by_key(scout_key: str):
    """Fetch auto scouting entries by their composite scout key.

    GET /scout/auto/scout_key/{scout_key}

    :param scout_key: Composite key, ``"<match_key>_<team_key>"``.
    :type scout_key: str
    :return: Matching rows (normally zero or one) as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE scout_auto_key = %s
            """,
            (scout_key,)
        )

        return cur.fetchall()

@router.get("/auto/event/{event_key}")
def get_scout_by_event(event_key: str):
    """Fetch all auto scouting entries for a given event.

    GET /scout/auto/event/{event_key}

    :param event_key: TBA event key, e.g. ``"2025sao"``.
    :type event_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE event_key = %s
            """,
            (event_key,)
        )

        return cur.fetchall()
    


@router.get("/auto/match/{match_key}")
def get_scout_by_match(match_key: str):
    """Fetch all auto scouting entries (all teams) for a given match.

    GET /scout/auto/match/{match_key}

    :param match_key: TBA match key, e.g. ``"2025sao_qm12"``.
    :type match_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE match_key = %s
            """,
            (match_key,)
        )

        return cur.fetchall()
    

@router.get("/auto/match/{match_key}/team/{team_key}")
def get_scout_by_match_team(match_key: str, team_key: str):
    """Fetch the auto scouting entry for one team in one match.

    GET /scout/auto/match/{match_key}/team/{team_key}

    :param match_key: TBA match key.
    :type match_key: str
    :param team_key: TBA team key, e.g. ``"frc7563"``.
    :type team_key: str
    :return: The matching row as a dict, or ``None`` if not found.
    :rtype: dict | None
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE match_key = %s
            AND team_key = %s
            """,
            (match_key, team_key)
        )

        return cur.fetchone()

@router.get("/auto/team/{team_key}")
def get_scout_by_team(team_key: str):
    """Fetch every auto scouting entry ever recorded for a team.

    GET /scout/auto/team/{team_key}

    :param team_key: TBA team key.
    :type team_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE team_key = %s
            """,
            (team_key,)
        )

        return cur.fetchall()

@router.get("/auto/team/{team_key}/event/{event_key}")
def get_scout_by_team_event(team_key: str, event_key: str):
    """Fetch a team's auto scouting entries within a single event.

    GET /scout/auto/team/{team_key}/event/{event_key}

    :param team_key: TBA team key.
    :type team_key: str
    :param event_key: TBA event key.
    :type event_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE team_key = %s
            AND event_key = %s
            """,
            (team_key, event_key)
        )

        return cur.fetchall()

@router.get("/auto/team/{team_key}/match/{match_key}")
def get_scout_by_team_on_match(team_key: str, match_key: str):
    """Fetch a team's auto scouting entry for a specific match.

    GET /scout/auto/team/{team_key}/match/{match_key}

    Functionally equivalent to :func:`get_scout_by_match_team` with the
    path parameters swapped.

    :param team_key: TBA team key.
    :type team_key: str
    :param match_key: TBA match key.
    :type match_key: str
    :return: The matching row as a dict, or ``None`` if not found.
    :rtype: dict | None
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM auto_scout_reefscape
            WHERE team_key = %s
            AND match_key = %s
            """,
            (team_key, match_key)
        )

        return cur.fetchone()
    

@router.get("/auto/matches/keys")
def get_scout_match_keys():
    """List every distinct match key that has an auto scouting entry.

    GET /scout/auto/matches/keys

    .. note::
        This does **not** de-duplicate (no ``DISTINCT``); if multiple
        teams/scouts recorded entries for the same match, its key will
        appear multiple times in the result.

    :return: List of match key strings.
    :rtype: list[str]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT match_key
            FROM auto_scout_reefscape
            """
        )

        rows = cur.fetchall()

        return [r[0] for r in rows]


# ===================================
# AUTO - SCOUT DELETE
# ===================================


@router.delete("/delete/auto/match/{match_key}/team/{team_key}")
def delete_auto_scout(match_key: str, team_key: str):
    """Delete a team's auto scouting entry for a specific match.

    DELETE /scout/delete/auto/match/{match_key}/team/{team_key}

    :param match_key: TBA match key.
    :type match_key: str
    :param team_key: TBA team key.
    :type team_key: str
    :return: ``{"message": "Scout deleted successfully"}`` on success, or
        ``{"message": "Scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM auto_scout_reefscape
            WHERE match_key = %s
            AND team_key = %s
            """,
            (match_key, team_key)
        )

        if cur.rowcount == 0:
            return {"message": "Scout not found"}

        return {"message": "Scout deleted successfully"}
    
@router.delete("/delete/auto/key/{scout_key}")
def delete_auto_scout_by_key(scout_key: str):
    """Delete an auto scouting entry by its composite scout key.

    DELETE /scout/delete/auto/key/{scout_key}

    :param scout_key: Composite key, ``"<match_key>_<team_key>"``.
    :type scout_key: str
    :return: ``{"message": "Scout deleted successfully"}`` on success, or
        ``{"message": "Scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM auto_scout_reefscape
            WHERE scout_auto_key = %s
            """,
            (scout_key,)
        )

        if cur.rowcount == 0:
            return {"message": "Scout not found"}

        return {"message": "Scout deleted successfully"}

# ===================================
# TELEOP - SCOUT CREATE
# ===================================

@router.post("/add/teleop/2025")
def create_teleop_scout(scout: TeleopScout):
    """Create a new teleop-period (+ endgame) scouting entry.

    POST /scout/add/teleop/2025

    The scout key is derived as ``f"{match_key}_{team_key}"`` and returned
    to the caller so it can be used later to fetch/delete this exact entry.

    :param scout: Teleop scouting payload validated against
        :class:`~app.api.schemas.teleop_scout_reefscape.TeleopScout`.
    :type scout: TeleopScout
    :return: ``{"scout_key": "<match_key>_<team_key>"}``.
    :rtype: dict
    """
    scout_key = f"{scout.match_key}_{scout.team_key}"

    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO teleop_scout_reefscape (
                scout_teleop_key,
                event_key,
                match_key,
                team_key,
                year,
                l1,
                l2,
                l3,
                l4,
                coral_misseds,
                coral_precision,
                algae_removed,
                algae_net,
                algae_processor,
                climb,
                collected_coral_floor,
                collected_coral_station,
                collected_algae_reef,
                issues,
                issues_notes,
                defended,
                driver_rating,
                score,
                notes
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,
                %s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s
            )
            RETURNING scout_teleop_key
            """,
            (
                scout_key,
                scout.event_key,
                scout.match_key,
                scout.team_key,
                scout.year,
                scout.l1,
                scout.l2,
                scout.l3,
                scout.l4,
                scout.coral_misseds,
                scout.coral_precision,
                scout.algae_removed,
                scout.algae_net,
                scout.algae_processor,
                scout.climb,
                scout.collected_coral_floor,
                scout.collected_coral_station,
                scout.collected_algae_reef,
                scout.issues,
                scout.issues_notes,
                scout.defended,
                scout.driver_rating,
                scout.score,
                scout.notes,
            )
        )

        return {"scout_key": cur.fetchone()[0]}


# ===================================
# TELEOP - SCOUT GET
# ===================================

@router.get("/teleop/scout_key/{scout_key}")
def get_teleop_by_key(scout_key: str):
    """Fetch teleop scouting entries by their composite scout key.

    GET /scout/teleop/scout_key/{scout_key}

    :param scout_key: Composite key, ``"<match_key>_<team_key>"``.
    :type scout_key: str
    :return: Matching rows (normally zero or one) as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM teleop_scout_reefscape
            WHERE scout_teleop_key = %s
            """,
            (scout_key,)
        )

        return cur.fetchall()

@router.get("/teleop/event/{event_key}")
def get_teleop_by_event(event_key: str):
    """Fetch all teleop scouting entries for a given event.

    GET /scout/teleop/event/{event_key}

    :param event_key: TBA event key.
    :type event_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM teleop_scout_reefscape
            WHERE event_key = %s
            """,
            (event_key,)
        )

        return cur.fetchall()
    
@router.get("/teleop/match/{match_key}")
def get_teleop_by_match(match_key: str):
    """Fetch all teleop scouting entries (all teams) for a given match.

    GET /scout/teleop/match/{match_key}

    :param match_key: TBA match key.
    :type match_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM teleop_scout_reefscape
            WHERE match_key = %s
            """,
            (match_key,)
        )

        return cur.fetchall()
    
@router.get("/teleop/match/{match_key}/team/{team_key}")
def get_teleop_by_match_team(match_key: str, team_key: str):
    """Fetch the teleop scouting entry for one team in one match.

    GET /scout/teleop/match/{match_key}/team/{team_key}

    :param match_key: TBA match key.
    :type match_key: str
    :param team_key: TBA team key.
    :type team_key: str
    :return: The matching row as a dict, or ``None`` if not found.
    :rtype: dict | None
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM teleop_scout_reefscape
            WHERE match_key = %s
            AND team_key = %s
            """,
            (match_key, team_key)
        )

        return cur.fetchone()
    

@router.get("/teleop/team/{team_key}/event/{event_key}")
def get_teleop_by_team_event(team_key: str, event_key: str):
    """Fetch a team's teleop scouting entries within a single event.

    GET /scout/teleop/team/{team_key}/event/{event_key}

    :param team_key: TBA team key.
    :type team_key: str
    :param event_key: TBA event key.
    :type event_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM teleop_scout_reefscape
            WHERE team_key = %s
            AND event_key = %s
            """,
            (team_key, event_key)
        )

        return cur.fetchall()
    

@router.get("/teleop/matches/keys")
def get_teleop_match_keys():
    """List every match key that has a teleop scouting entry.

    GET /scout/teleop/matches/keys

    .. note::
        Not de-duplicated — see :func:`get_scout_match_keys` for the same
        caveat on the auto-scout equivalent.

    :return: List of match key strings.
    :rtype: list[str]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT match_key
            FROM teleop_scout_reefscape
            """
        )

        rows = cur.fetchall()

        return [r[0] for r in rows]
    

# ===================================
# TELEOP - SCOUT DELETE
# ===================================

@router.delete("/delete/teleop/match/{match_key}/team/{team_key}")
def delete_teleop(match_key: str, team_key: str):
    """Delete a team's teleop scouting entry for a specific match.

    DELETE /scout/delete/teleop/match/{match_key}/team/{team_key}

    :param match_key: TBA match key.
    :type match_key: str
    :param team_key: TBA team key.
    :type team_key: str
    :return: ``{"message": "Scout deleted successfully"}`` on success, or
        ``{"message": "Scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM teleop_scout_reefscape
            WHERE match_key = %s
            AND team_key = %s
            """,
            (match_key, team_key)
        )

        if cur.rowcount == 0:
            return {"message": "Scout not found"}

        return {"message": "Scout deleted successfully"}
    
@router.delete("/delete/teleop/key/{scout_key}")
def delete_teleop_by_key(scout_key: str):
    """Delete a teleop scouting entry by its composite scout key.

    DELETE /scout/delete/teleop/key/{scout_key}

    :param scout_key: Composite key, ``"<match_key>_<team_key>"``.
    :type scout_key: str
    :return: ``{"message": "Scout deleted successfully"}`` on success, or
        ``{"message": "Scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM teleop_scout_reefscape
            WHERE scout_teleop_key = %s
            """,
            (scout_key,)
        )

        if cur.rowcount == 0:
            return {"message": "Scout not found"}

        return {"message": "Scout deleted successfully"}
    

# ===================================
# PIT - SCOUT CREATE
# ===================================

@router.post("/add/pit/")
def create_pit_scout(scout: PitScout):
    """Create a new pit scouting entry.

    POST /scout/add/pit/

    The scout key is derived as ``f"{event_key}_{team_key}"`` (one pit
    scouting record per team per event) and returned to the caller.

    :param scout: Pit scouting payload validated against
        :class:`~app.api.schemas.pit_scout.PitScout`.
    :type scout: PitScout
    :return: ``{"scout_key": "<event_key>_<team_key>"}``.
    :rtype: dict
    """
    pit_key = f"{scout.event_key}_{scout.team_key}"

    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO pit_scout (
                pit_scout_key,
                event_key,
                team_key,
                description,
                img_url
            )
            VALUES (
                %s,%s,%s,%s,%s
            )
            RETURNING pit_scout_key
            """,
            (
                pit_key,
                scout.event_key,
                scout.team_key,
                scout.description,
                scout.img_url,
            )
        )

        return {"scout_key": cur.fetchone()[0]}
    

# ===================================
# PIT - SCOUT GET
# ===================================

@router.get("/pit/scout_key/{scout_key}")
def get_pit_by_key(scout_key: str):
    """Fetch pit scouting entries by their composite scout key.

    GET /scout/pit/scout_key/{scout_key}

    :param scout_key: Composite key, ``"<event_key>_<team_key>"``.
    :type scout_key: str
    :return: Matching rows (normally zero or one) as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM pit_scout
            WHERE pit_scout_key = %s
            """,
            (scout_key,)
        )

        return cur.fetchall()
    
@router.get("/pit/event/{event_key}")
def get_pit_by_event(event_key: str):
    """Fetch all pit scouting entries for a given event.

    GET /scout/pit/event/{event_key}

    :param event_key: TBA event key.
    :type event_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM pit_scout
            WHERE event_key = %s
            """,
            (event_key,)
        )

        return cur.fetchall()
    
@router.get("/pit/team/{team_key}")
def get_pit_by_team(team_key: str):
    """Fetch every pit scouting entry ever recorded for a team.

    GET /scout/pit/team/{team_key}

    :param team_key: TBA team key.
    :type team_key: str
    :return: All matching rows as a list of dicts.
    :rtype: list[dict]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM pit_scout
            WHERE team_key = %s
            """,
            (team_key,)
        )

        return cur.fetchall()

@router.get("/pit/team/{team_key}/event/{event_key}")
def get_pit_by_team_event(team_key: str, event_key: str):
    """Fetch a team's pit scouting entry for a specific event.

    GET /scout/pit/team/{team_key}/event/{event_key}

    :param team_key: TBA team key.
    :type team_key: str
    :param event_key: TBA event key.
    :type event_key: str
    :return: The matching row as a dict, or ``None`` if not found.
    :rtype: dict | None
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT *
            FROM pit_scout
            WHERE team_key = %s
            AND event_key = %s
            """,
            (team_key, event_key)
        )

        return cur.fetchone()

@router.get("/pit/events/keys")
def get_pit_event_keys():
    """List every distinct event key that has at least one pit scouting entry.

    GET /scout/pit/events/keys

    Unlike the match-key listing endpoints, this one uses ``DISTINCT`` and
    is sorted alphabetically.

    :return: Sorted list of unique event key strings.
    :rtype: list[str]
    """
    with get_cursor(False) as cur:
        cur.execute(
            """
            SELECT DISTINCT event_key
            FROM pit_scout
            ORDER BY event_key
            """
        )

        rows = cur.fetchall()

        return [r[0] for r in rows]
    
# ===================================
# PIT - SCOUT DELETE
# ===================================

@router.delete("/delete/pit/team/{team_key}/event/{event_key}")
def delete_pit(team_key: str, event_key: str):
    """Delete a team's pit scouting entry for a specific event.

    DELETE /scout/delete/pit/team/{team_key}/event/{event_key}

    :param team_key: TBA team key.
    :type team_key: str
    :param event_key: TBA event key.
    :type event_key: str
    :return: ``{"message": "Pit scout deleted successfully"}`` on success,
        or ``{"message": "Pit scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM pit_scout
            WHERE team_key = %s
            AND event_key = %s
            """,
            (team_key, event_key)
        )

        if cur.rowcount == 0:
            return {"message": "Pit scout not found"}

        return {"message": "Pit scout deleted successfully"}


@router.delete("/delete/pit/key/{scout_key}")
def delete_pit_by_key(scout_key: str):
    """Delete a pit scouting entry by its composite scout key.

    DELETE /scout/delete/pit/key/{scout_key}

    :param scout_key: Composite key, ``"<event_key>_<team_key>"``.
    :type scout_key: str
    :return: ``{"message": "Pit scout deleted successfully"}`` on success,
        or ``{"message": "Pit scout not found"}`` if no row matched.
    :rtype: dict
    """
    with get_cursor() as cur:
        cur.execute(
            """
            DELETE FROM pit_scout
            WHERE pit_scout_key = %s
            """,
            (scout_key,)
        )

        if cur.rowcount == 0:
            return {"message": "Pit scout not found"}

        return {"message": "Pit scout deleted successfully"}
