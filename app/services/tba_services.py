from app.core.config import TBA_KEY
import bluealliance


tba_client = bluealliance.TBAClient(TBA_KEY)
tba_collector = bluealliance.TBACollector(TBA_KEY)

def get_tbaClient():
    return tba_client

def get_tba_collector():
    return tba_collector    