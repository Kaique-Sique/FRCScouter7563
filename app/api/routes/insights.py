from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient

router = APIRouter(prefix="/insights", tags=["Insights"])


# =========================================================
# INSIGHTS
# =========================================================

@router.get("/leaderboards/{year}")
def get_insights_leaderboards_year(year: int, tbaClient=Depends(get_tbaClient)):
    '''LeaderboardInsight objects for a year (year=0 for all-time). GET /insights/leaderboards/{year}'''
    return tbaClient.get_insights_leaderboards_year(year)


@router.get("/notables/{year}")
def get_insights_notables_year(year: int, tbaClient=Depends(get_tbaClient)):
    '''NotablesInsight objects for a year (year=0 for all-time). GET /insights/notables/{year}'''
    return tbaClient.get_insights_notables_year(year)

@router.get("/{year}")
def get_insights_year(year: int, tbaClient=Depends(get_tbaClient)):
    '''All Insight objects for a year across all categories (year=0 for all-time). GET /insights/{year}'''
    return tbaClient.get_insights_year(year)    

@router.get("/{year}/{category}")
def get_insights_year_category(year: int, category: str, tbaClient=Depends(get_tbaClient)):
    '''Insight objects for a year filtered by category (leaderboard/streak/timeseries). GET /insights/{year}/{category}'''
    return tbaClient.get_insights_year_category(year, category)

@router.get("/{year}/district/{district_abbreviation}")
def get_insights_v2_year_district(year: int, district_abbreviation: str, tbaClient=Depends(get_tbaClient)):
    '''Insight objects for a year scoped to a district across all categories. GET /insights/{year}/district/{district_abbreviation}'''
    return tbaClient.get_insights_v2_year_district(year, district_abbreviation)

@router.get("/{year}/{category}/district/{district_abbreviation}")
def get_insights_v2_year_category_district(year: int, category: str, district_abbreviation: str, tbaClient=Depends(get_tbaClient)):   
    '''InsightV2 objects for a year, category, and district. GET /insights/{year}/{category}/district/{district_abbreviation}'''                     
    return tbaClient.get_insights_v2_year_category_district(year, category, district_abbreviation)
