from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient

router = APIRouter(prefix="/regional_advancement", tags=["Regional advancement"])

# =========================================================
# REGIONAL ADVANCEMENT
# =========================================================


@router.get("/{year}")
def get_regional_advancement(year: int,  tbaClient=Depends(get_tbaClient)):
    '''Per-team advancement information to the FIRST Championship. GET /regional_advancement/{year}'''
    return tbaClient.get_regional_advancement(year)

@router.get("/{year}/rankings")
def get_regional_advancement(year: int, tbaClient=Depends(get_tbaClient)):
    '''
    Team rankings in the regional pool for a specific year. GET /regional_advancement/{year}/rankings
    '''
    return tbaClient.get_regional_rankings(year)


@router.get("/{year}/rankings/{max_num}")
def get_regional_advancement_top(year: int, max_num: int, tbaClient=Depends(get_tbaClient)):
    '''
    Top N team rankings in the regional pool for a specific year. GET /regional_advancement/{year}/rankings/{max_num}
    '''
    rankings = tbaClient.get_regional_rankings(year)
    return rankings[:max_num]