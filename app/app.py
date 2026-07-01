#libs imports
from fastapi import FastAPI

# Routes imports
#from app.api.routes import ()

# tools imports
from app.core import db
from app.services.tba_services import TBAClient

app = FastAPI(
    title="FRC Scout System",
    version="1.0"
)

tba_client = TBAClient()

# =========================
# ROUTES
# =========================

'''include here all projets
            routes          '''



@app.get("/")
def home():
    return {"details": "home page"}

@app.get("/status-db")
def test_Connection_database():
    try:
        db.get_connection()
        return {"status": "Onine"}
    except:
        return {"status": "Offline"}

@app.get("/status-tba")
def test_Connection_tba():
    tba_client = TBAClient()
    return tba_client.get_status()