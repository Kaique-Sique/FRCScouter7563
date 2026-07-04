"""Regional advancement endpoints, proxied from The Blue Alliance (TBA) API.

Covers per-team advancement info towards the FIRST Championship, plus
regional-pool rankings (relevant to the 2025+ Regional Champs points
system). Every handler is a thin pass-through to the shared ``TBAClient``
(see :mod:`app.services.tba_services`).

.. note::
    ``get_regional_advancement`` (the plain ``/{year}`` route) and
    ``get_regional_advancement`` (the ``/{year}/rankings`` route) share the
    same Python function name in the source file. This works today only
    because FastAPI dispatches by the registered path, not the function
    name, but it means the second definition shadows the first at the
    Python level — calling either function directly from other code (as
    opposed to hitting it over HTTP) would resolve to the ``/rankings``
    implementation.
"""

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