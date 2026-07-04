"""The Blue Alliance (TBA) service singletons.

Wraps the third-party ``bluealliance`` package (the ``BlueAlliancePy``
library, developed alongside this project — see
https://github.com/Kaique-Sique/BlueAlliancePy) with two module-level
singletons, created once at import time using the API key from
:mod:`app.core.config`:

- ``tba_client``: a :class:`bluealliance.TBAClient` used for on-demand,
  request-scoped calls to the TBA REST API (teams, events, matches,
  districts, insights, etc). This is injected into route handlers via
  FastAPI's ``Depends(get_tbaClient)``.
- ``tba_collector``: a :class:`bluealliance.TBACollector`, intended for
  batched/background data collection use cases (e.g. pre-fetching or
  caching TBA data) rather than per-request calls.

Keeping these as singletons avoids re-authenticating / re-instantiating a
new HTTP client on every request.
"""

from app.core.config import TBA_KEY
import bluealliance


tba_client = bluealliance.TBAClient(TBA_KEY)
tba_collector = bluealliance.TBACollector(TBA_KEY)

def get_tbaClient():
    """Return the shared :class:`bluealliance.TBAClient` singleton.

    Intended to be used as a FastAPI dependency
    (``tbaClient=Depends(get_tbaClient)``) so route handlers don't need to
    import ``tba_client`` directly.

    :return: The application-wide TBA API client.
    :rtype: bluealliance.TBAClient
    """
    return tba_client

def get_tba_collector():
    """Return the shared :class:`bluealliance.TBACollector` singleton.

    :return: The application-wide TBA data collector instance.
    :rtype: bluealliance.TBACollector
    """
    return tba_collector    