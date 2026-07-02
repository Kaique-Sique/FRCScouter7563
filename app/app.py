#libs imports
from fastapi import FastAPI

# Routes imports
#from app.api.routes import ()

# tools imports
from app.core import db
from app.services.tba_services import (get_tba_collector, get_tbaClient)

app = FastAPI(
    title="FRC Scout System",
    version="1.0"
)

tba_client = get_tbaClient()
tba_collector = get_tba_collector()

# =========================
# ROUTES
# =========================

'''include here all projets
            routes          '''



@app.get("/")
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