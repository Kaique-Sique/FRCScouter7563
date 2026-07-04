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
    
@router.get("/teleop/match/{match_key}/team/{team_key}")
def get_teleop_by_match_team(match_key: str, team_key: str):

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