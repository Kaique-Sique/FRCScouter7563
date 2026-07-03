from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient

router = APIRouter(prefix="/districts", tags=["Districts"])

# =========================================================
# DISTRICTS
# =========================================================

@router.get("/{year}")
def get_districts_by_year(year: int, tbaClient=Depends(get_tbaClient)):
    '''Districts and their keys for a given year. GET /districts/{year}'''
    return tbaClient.get_districts_by_year(year)


@router.get("/{district_key}/events")
def get_district_events(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Events in a given district. GET /district/{district_key}/events'''
    return tbaClient.get_district_events(district_key)

@router.get("/{district_key}/events/simple")
def get_district_events_simple(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Short-form events in a given district. GET /district/{district_key}/events/simple'''
    return tbaClient.get_district_events_simple(district_key)

@router.get("/{district_key}/events/keys")
def get_district_events_keys(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Event keys for a given district. GET /district/{district_key}/events/keys'''
    return tbaClient.get_district_events_keys(district_key)

@router.get("/{district_key}/teams")
def get_district_teams(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Teams in a given district. GET /district/{district_key}/teams'''
    return tbaClient.get_district_teams(district_key)


@router.get("/{district_key}/teams/simple")
def get_district_teams_simple(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Short-form teams in a given district. GET /district/{district_key}/teams/simple'''
    return tbaClient.get_district_teams_simple(district_key)

@router.get("/{district_key}/teams/keys")
def get_district_teams_keys(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team keys for a given district. GET /district/{district_key}/teams/keys'''
    return tbaClient.get_district_teams_keys(district_key)

@router.get("/{district_key}/rankings")
def get_district_rankings(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Team district rankings for the given district. GET /district/{district_key}/rankings'''
    return tbaClient.get_district_rankings(district_key)

@router.get("/{district_key}/awards")
def get_district_awards(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''All awards in the given district. GET /district/{district_key}/awards'''
    return tbaClient.get_district_awards(district_key)

@router.get("/{district_key}/advancement")
def get_district_advancement(district_key: str, tbaClient=Depends(get_tbaClient)):
    '''Advancement information per team in a district. GET /district/{district_key}/advancement'''
    return tbaClient.get_district_advancement(district_key)

@router.get("/{district_abbreviation}/history")
def get_district_history(district_abbreviation: str, tbaClient=Depends(get_tbaClient)):
    '''District objects across all years for a given district abbreviation. GET /district/{district_abbreviation}/history'''
    return tbaClient.get_district_history(district_abbreviation)

@router.get("/{district_abbreviation}/dcmp_history")
def get_district_dcmp_history(district_abbreviation: str, tbaClient=Depends(get_tbaClient)):
    '''DCMP events and awards for a given district abbreviation. GET /district/{district_abbreviation}/dcmp_history'''
    return tbaClient.get_district_dcmp_history(district_abbreviation)

@router.get("/{district_abbreviation}/insights")
def get_district_insights(district_abbreviation: str, tbaClient=Depends(get_tbaClient)):
    '''Insights for a given district. GET /district/{district_abbreviation}/insights'''
    return tbaClient.get_district_insights(district_abbreviation)

