"""Application entry point.

Running this module directly starts the FastAPI application (``app.app:app``)
using the Uvicorn ASGI server on ``0.0.0.0:8000`` with auto-reload enabled,
which is convenient for local development.

Usage:
    python main.py
"""

import uvicorn


if __name__ == "__main__":
    # Launch the FastAPI app defined in app/app.py.
    # `reload=True` makes Uvicorn watch the source files and restart the
    # server automatically whenever a change is saved (development only —
    # disable this in production).
    uvicorn.run(
        "app.app:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
        )