#libs imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
# FAVICON 
# =========================

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@app.head("/")
def home():
    '''
    Docstring for home route. This route is used to test if the API is running.
    '''
    return {"details": "home page"}

@app.get("/status-db")
def test_Connection_database():
    '''
    Docstring for test_Connection_database route. This route is used to test if the database is running.
    '''
    try:
        db.get_connection()
        return {"status": "Online"}
    except:
        return {"status": "Offline"}

@app.get("/status-tba")
def test_Connection_tba():
    '''
    Docstring for test_Connection_tba route. This route is used to test if the TBA API is running.
    '''
    tba_client = get_tbaClient()
    return tba_client.get_status()