from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient


router = APIRouter(prefix="/teams", tags=["Teams"])

# =========================================================
# TEAM  (single team) -- must come BEFORE the generic
# /{page_num} and /{year}/{page_num} routes below, otherwise
# requests like /teams/team/frc7563 get matched by shape to
# /{year}/{page_num} first and fail int conversion (422).
# =========================================================

@router.get("/team/{team_key}")
def get_team(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Gets a Team object. GET /team/{team_key}
    '''
    return tbaClient.get_team(team_key)

@router.get("/team/{team_key}/simple")
def get_team_simple(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Gets a Team_Simple object. GET /team/{team_key}/simple
    '''
    return tbaClient.get_team_simple(team_key)

@router.get("/team/{team_key}/years_participated")
def get_team_years_participated(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Years the team competed in at least one event. GET /team/{team_key}/years_participated
    '''
    return tbaClient.get_team_years_participated(team_key)

@router.get("/team/{team_key}/districts")
def get_team_districts(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Districts the team has participated in, by year. GET /team/{team_key}/districts
    '''
    return tbaClient.get_team_districts(team_key)

@router.get("/team/{team_key}/robots")
def get_team_robots(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Year/robot-name pairs for every year the team named a robot. GET /team/{team_key}/robots
    '''
    return tbaClient.get_team_robots(team_key)

@router.get("/team/{team_key}/history")
def get_team_history(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Full team history including events and awards. GET /team/{team_key}/history
    '''
    return tbaClient.get_team_history(team_key)


@router.get("/team/{team_key}/social_media")
def get_team_social_media(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Social media objects for the team. GET /team/{team_key}/social_media
    '''
    return tbaClient.get_team_social_media(team_key)

@router.get("/team/{team_key}/awards")
def get_team_awards(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    All awards the team has won (all time). GET /team/{team_key}/awards
    '''
    return tbaClient.get_team_awards(team_key)

@router.get("/team/{team_key}/awards/{year}")
def get_team_awards_by_year(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Awards the team won in a specific year. GET /team/{team_key}/awards/{year}
    '''
    return tbaClient.get_team_awards_by_year(team_key, year)

@router.get("/team/{team_key}/media/{year}")
def get_team_media_by_year(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Media objects for the team in a given year. GET /team/{team_key}/media/{year}
    '''
    return tbaClient.get_team_media_by_year(team_key, year)

@router.get("/team/{team_key}/media/tag/{media_tag}")
def get_team_media_by_tag(team_key: str, media_tag: str, tbaClient=Depends(get_tbaClient)):
    '''
    Media for the team filtered by tag. GET /team/{team_key}/media/tag/{media_tag}
    '''
    return tbaClient.get_team_media_by_tag(team_key, media_tag)

@router.get("/team/{team_key}/media/tag/{media_tag}/{year}")
def get_team_media_by_tag_year(team_key: str, media_tag: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Media for the team filtered by tag and year. GET /team/{team_key}/media/tag/{media_tag}/{year}
    '''
    return tbaClient.get_team_media_by_tag_year(team_key, media_tag, year)

@router.get("/team/{team_key}/events")
def get_team_events(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    All events this team has competed at (all time). GET /team/{team_key}/events
    '''
    return tbaClient.get_team_events(team_key)

@router.get("/team/{team_key}/events/simple")
def get_team_events_simple(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Short-form events this team has competed at (all time). GET /team/{team_key}/events/simple
    '''
    return tbaClient.get_team_events_simple(team_key)

@router.get("/team/{team_key}/events/keys")
def get_team_events_keys(team_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Event keys for all events this team has competed at. GET /team/{team_key}/events/keys
    '''
    return tbaClient.get_team_events_keys(team_key)

@router.get("/team/{team_key}/events/{year}/statuses")
def get_team_events_statuses_by_year(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Key-value map of Team_Event_Status for each event in a given year. GET /team/{team_key}/events/{year}/statuses
    '''
    return tbaClient.get_team_events_statuses_by_year(team_key, year)

@router.get("/team/{team_key}/events/{year}/keys")
def get_team_events_by_year_keys(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Event keys for events this team competed at in a given year. GET /team/{team_key}/events/{year}/keys
    '''
    return tbaClient.get_team_events_by_year_keys(team_key, year)

@router.get("/team/{team_key}/events/{year}")
def get_team_events_by_year(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Short-form events this team competed at in a given year. GET /team/{team_key}/events/{year}/simple
    '''
    return tbaClient.get_team_events_by_year(team_key, year)

@router.get("/team/{team_key}/event/{event_key}/matches")
def get_team_event_matches(team_key: str, event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Matches for the team at a specific event. GET /team/{team_key}/event/{event_key}/matches
    '''
    return tbaClient.get_team_event_matches(team_key, event_key)

@router.get("/team/{team_key}/event/{event_key}/matches/simple")
def get_team_event_matches_simple(team_key: str, event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Short-form matches for the team at a specific event. GET /team/{team_key}/event/{event_key}/matches/simple
    '''
    return tbaClient.get_team_event_matches_simple(team_key, event_key)

@router.get("/team/{team_key}/event/{event_key}/matches/keys")
def get_team_event_matches_keys(team_key: str, event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Match keys for the team at a specific event. GET /team/{team_key}/event/{event_key}/matches/keys
    '''
    return tbaClient.get_team_event_matches_keys(team_key, event_key)

@router.get("/team/{team_key}/matches/{year}/keys")
def get_team_matches_by_year_keys(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Match keys for the team in a given year. GET /team/{team_key}/matches/{year}/keys
    '''
    return tbaClient.get_team_matches_by_year_keys(team_key, year)

@router.get("/team/{team_key}/matches/{year}")
def get_team_matches_by_year(team_key: str, year: int, tbaClient=Depends(get_tbaClient)):
    '''
    All matches for the team in a given year. GET /team/{team_key}/matches/{year}
    '''
    return tbaClient.get_team_matches_by_year(team_key, year)

@router.get("/team/{team_key}/event/{event_key}/awards")
def get_team_event_awards(team_key: str, event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Awards the team has won at a specific event. GET /team/{team_key}/event/{event_key}/awards
    '''
    return tbaClient.get_team_event_awards(team_key, event_key)

@router.get("/team/{team_key}/event/{event_key}/status")
def get_team_event_status(team_key: str, event_key: str, tbaClient=Depends(get_tbaClient)):
    '''
    Competition rank and status for the team at a specific event. GET /team/{team_key}/event/{event_key}/status
    '''
    return tbaClient.get_team_event_status(team_key, event_key)


# =========================================================
# TEAM  (team group) -- generic /{page_num} and /{year}/{page_num}
# routes come LAST since they match any 1- or 2-segment path shape.
# =========================================================

@router.get("/{page_num}/simple")
def get_teams_simple(page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Short-form Team_Simple list, paginated. GET /teams/{page_num}/simple
    '''
    return tbaClient.get_teams_simple(page_num)

@router.get("/{page_num}/keys")
def get_teams_keys(page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Team key list, paginated. GET /teams/{page_num}/keys
    '''
    return tbaClient.get_teams_keys(page_num)

@router.get("/{page_num}")
def get_teams(page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Gets a list of Team objects, paginated in groups of 500. GET /teams/{page_num}
    '''
    return tbaClient.get_teams(page_num)

@router.get("/{year}/{page_num}/simple")
def get_teams_by_year_simple(year: int, page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Short-form teams that competed in a given year, paginated. GET /teams/{year}/{page_num}/simple
    '''
    return tbaClient.get_teams_by_year_simple(year, page_num)

@router.get("/{year}/{page_num}/keys")
def get_teams_by_year_keys(year: int, page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    gets a list of Team objects that competed in a given year, paginated. GET /teams/{year}/{page_num}/keys
    '''
    return tbaClient.get_teams_by_year_keys(year, page_num)

@router.get("/{year}/{page_num}")
def get_teams_by_year(year: int, page_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Teams that competed in a given year, paginated. GET /teams/{year}/{page_num}
    '''
    return tbaClient.get_teams_by_year(year, page_num)