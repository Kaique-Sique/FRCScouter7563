"""Event-related endpoints, proxied from The Blue Alliance (TBA) API.

Covers both year-level listings (all events in a season) and single-event
detail endpoints (alliances, awards, matches, rankings, OPRs, insights,
predictions, teams, media). Every handler is a thin pass-through to the
shared ``TBAClient`` (see :mod:`app.services.tba_services`).
"""

from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient

router = APIRouter(prefix="/events", tags=["Events"])

# =========================================================
# EVENTS  (by year)
# =========================================================

@router.get("/{year}")
def get_events_by_year(year: int, tbaClient=Depends(get_tbaClient)):
    '''All events in a given year. GET /events/{year}'''
    return tbaClient.get_events_by_year(year)

@router.get("/{year}/simple")
def get_events_by_year_simple(year: int, tbaClient=Depends(get_tbaClient)):
    '''Short-form events in a given year. GET /events/{year}/simple'''
    return tbaClient.get_events_by_year_simple(year)

@router.get("/{year}/keys")
def get_events_by_year_keys(year: int, tbaClient=Depends(get_tbaClient)):
    '''Event keys for a given year. GET /events/{year}/keys'''
    return tbaClient.get_events_by_year_keys(year)

# =========================================================
# EVENTS  (single)
# =========================================================

@router.get("/event/{event_key}")
def get_event(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Gets an Event object. GET /event/{event_key}'''
    return tbaClient.get_event(event_key)

@router.get("/event/{event_key}/simple")
def get_event_simple(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Short-form Event_Simple object. GET /event/{event_key}/simple'''
    return tbaClient.get_event_simple(event_key)


@router.get("/event/{event_key}/alliances")
def get_event_alliances(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Elimination alliances for the event. GET /event/{event_key}/alliances'''
    return tbaClient.get_event_alliances(event_key)

@router.get("/event/{event_key}/awards")
def get_event_awards(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Awards from the event. GET /event/{event_key}/awards'''
    return tbaClient.get_event_awards(event_key)

@router.get("/event/{event_key}/matches")
def get_event_matches(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''All matches for the event. GET /event/{event_key}/matches'''
    return tbaClient.get_event_matches(event_key)

@router.get("/event/{event_key}/matches/simple")
def get_event_matches_simple(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Short-form matches for the event. GET /event/{event_key}/matches/simple'''
    return tbaClient.get_event_matches_simple(event_key)

@router.get("/event/{event_key}/matches/keys")
def get_event_matches_keys(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Match keys for the event. GET /event/{event_key}/matches/keys'''
    return tbaClient.get_event_matches_keys(event_key)

@router.get("/event/{event_key}/matches/timeseries")
def get_event_match_timeseries(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Match keys that have Zebra timeseries data at this event. GET /event/{event_key}/matches/timeseries
    '''
    return tbaClient.get_event_match_timeseries(event_key)

@router.get("/event/{event_key}/rankings")
def get_event_rankings(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team rankings for the event. GET /event/{event_key}/rankings'''
    return tbaClient.get_event_rankings(event_key)
                                                         
@router.get("/event/{event_key}/oprs")
def get_event_oprs(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''OPR, DPR, and CCWM for teams at the event. GET /event/{event_key}/oprs'''
    return tbaClient.get_event_oprs(event_key)

@router.get("/event/{event_key}/coprs")
def get_event_coprs(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Component OPRs for teams at the event. GET /event/{event_key}/coprs'''
    return tbaClient.get_event_coprs(event_key)

@router.get("/event/{event_key}/dprs")
def get_event_district_points(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''DPRs for teams at the event. GET /event/{event_key}/district_points'''
    return tbaClient.get_event_district_points(event_key)

@router.get("/event/{event_key}/advancement_points")
def get_event_advancement_points(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    District or regional CMP points, depending on event type. GET /event/{event_key}/advancement_points
    '''
    return tbaClient.get_event_advancement_points(event_key)

@router.get("/event/{event_key}/regional_champs_pool_points")
def get_event_regional_champs_pool_points(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''For 2025+ Regional events, points toward the Championship qualification pool. GET /event/{event_key}/regional_champs_pool_points''' 
    return tbaClient.get_event_regional_champs_pool_points(event_key)

@router.get("/event/{event_key}/event_insights")
def get_event_insights(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Year-specific event insights (qual and playoff). GET /event/{event_key}/insights'''
    return tbaClient.get_event_insights(event_key)

@router.get("/event/{event_key}/predictions")
def get_event_predictions(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''TBA-generated match predictions for the event. GET /event/{event_key}/predictions'''
    return tbaClient.get_event_predictions(event_key)

@router.get("/event/{event_key}/teams")
def get_event_teams(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team objects for all teams that competed at the event. GET /event/{event_key}/teams'''
    return tbaClient.get_event_teams(event_key)

@router.get("/event/{event_key}/teams/simple")
def get_event_teams_simple(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team objects for all teams that competed at the event. GET /event/{event_key}/teams/simple'''
    return tbaClient.get_event_teams_simple(event_key)

@router.get("/event/{event_key}/teams/keys")
def get_event_teams_keys(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team keys for the event. GET /event/{event_key}/teams/keys'''
    return tbaClient.get_event_teams_keys(event_key)

@router.get("/event/{event_key}/teams/statuses")
def get_event_teams_statuses(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Key-value map of Team_Event_Status for all teams at the event. GET /event/{event_key}/teams/statuses
    '''
    return tbaClient.get_event_teams_statuses(event_key)

@router.get("/event/{event_key}/team_media")
def get_event_team_media(event_key: str, tbaClient=Depends(get_tbaClient)):
    '''Media objects for all teams at the event. GET /event/{event_key}/team_media'''
    return tbaClient.get_event_team_media(event_key)
