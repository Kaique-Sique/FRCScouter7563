#libs imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Routes imports
from app.api.routes import (
    teams,
    events
)

# tools imports
from app.core import db
from app.services.tba_services import (get_tba_collector, get_tbaClient)

app = FastAPI(
    title="FRC Scout System",
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