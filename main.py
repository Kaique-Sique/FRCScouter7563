"""Application entry point.

Running this module directly starts the FastAPI application (``app.app:app``)
using the Uvicorn ASGI server on ``0.0.0.0:8000`` with auto-reload enabled,
which is convenient for local development.

Usage:
    python main.py

This module creates and configures the FRCScouter7563 FastAPI application:

- Instantiates the singleton ``TBAClient`` / ``TBACollector`` used to talk to
  The Blue Alliance (TBA) API (see :mod:`app.services.tba_services`).
- Mounts the ``/static`` directory (favicon, etc).
- Registers every route module under :mod:`app.api.routes` as an
  ``APIRouter``.
- Exposes a couple of lightweight health-check endpoints
  (``/status-db`` and ``/status-tba``).

The ASGI app object created here (``app``) is what Uvicorn serves; see
``main.py`` for how the server is launched.
"""

#libs imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import uvicorn

# Routes imports
from app.api.routes import (
    scout,
    teams,
    events,
    districts,
    matchs,
    insights,
    regional_advancement
)

# tools imports
from app.core import db
from app.services.tba_services import (get_tba_collector, get_tbaClient)

app = FastAPI(
    title="FRCScouter 7563",
    version="1.0"
)

tba_client = get_tbaClient()
tba_collector = get_tba_collector()

# =========================
# ROUTES
# =========================

'''include here all projets
            routes          '''
app.include_router(teams.router) # host:8000 /teams/ 
app.include_router(events.router) # host:8000 /events/ 
app.include_router(districts.router) # host:8000 /districts/ 
app.include_router(matchs.router) # host:8000 /matchs/ 
app.include_router(insights.router) # host:8000 /insights/ 
app.include_router(regional_advancement.router) # host:8000 /regional_advancement/ 
app.include_router(scout.router) # host:8000 /scout/ 

# =========================
# ReadTheDocs Site
# =========================

app.mount(
    "/ReadTheDocs", 
    StaticFiles(directory="site", html=True),
    name="ReadTheDocs"
)


@app.head("/")
def home():
    '''
    Docstring for home route. This route is used to test if the API is running.
    '''
    return {"details": "home page"}

@app.get("/status-db")
def test_Connection_database():
    '''
    Health-check for the PostgreSQL database.

    Attempts to open a raw connection via :func:`app.core.db.get_connection`.
    GET /status-db

    :return: ``{"status": "Online"}`` if the connection succeeds, otherwise
        ``{"status": "Offline"}``. The connection is opened and immediately
        discarded (not explicitly closed) — this endpoint is only meant as a
        cheap connectivity probe, not for production monitoring.
    :rtype: dict
    '''
    try:
        db.get_connection()
        return {"status": "Online"}
    except:
        return {"status": "Offline"}

@app.get("/status-tba")
def test_Connection_tba():
    '''
    Health-check for The Blue Alliance (TBA) API.

    Proxies to the TBA ``/status`` endpoint via the shared ``TBAClient``.
    GET /status-tba

    :return: The raw TBA status payload (API version, current season,
        whether the season is "down" for maintenance, etc).
    :rtype: dict
    '''
    tba_client = get_tbaClient()
    return tba_client.get_status()


if __name__ == "__main__":
    # Launch the FastAPI app defined in app/app.py.
    # `reload=True` makes Uvicorn watch the source files and restart the
    # server automatically whenever a change is saved (development only —
    # disable this in production).
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
        )