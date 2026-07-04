"""Single-match endpoints, proxied from The Blue Alliance (TBA) API.

Note the router prefix is ``/matchs`` (not the grammatically correct
"matches") — this is intentional/pre-existing and reflected in the actual
URL paths. Every handler is a thin pass-through to the shared ``TBAClient``
(see :mod:`app.services.tba_services`).
"""

from fastapi import APIRouter, Depends
from app.services.tba_services import get_tbaClient

router = APIRouter(prefix="/matchs", tags=["Matchs"])

# =========================================================
# MATCH  (single match)
# =========================================================

@router.get("/{match_key}")
def get_match(match_key: str, tbaClient=Depends(get_tbaClient)):
    '''Gets a full Match object. GET /match/{match_key}'''
    return tbaClient.get_match(match_key)

@router.get("/{match_key}/simple")
def get_match_simple(match_key: str, tbaClient=Depends(get_tbaClient)):
    '''Gets a simple Match object. GET /match/{match_key}/simple'''
    return tbaClient.get_match_simple(match_key)

@router.get("/{match_key}/timeseries")
def get_match_timeseries(match_key: str, tbaClient=Depends(get_tbaClient)):
    '''Game-specific Zebra timeseries data for the match. GET /match/{match_key}/timeseries'''
    return tbaClient.get_match_timeseries(match_key)

@router.get("/{match_key}/zebra_motionworks")
def get_match_zebra(match_key: str, tbaClient=Depends(get_tbaClient)):
    '''Zebra MotionWorks positional data for the match. GET /match/{match_key}/zebra_motionworks'''
    return tbaClient.get_match_zebra(match_key)

