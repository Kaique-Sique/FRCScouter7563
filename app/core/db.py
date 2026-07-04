"""Database access helpers.

Thin wrapper around ``psycopg2`` providing:

- :func:`get_connection` — opens a new raw PostgreSQL connection using the
  credentials from :mod:`app.core.config`.
- :func:`get_cursor` — a context manager that yields a
  :class:`~psycopg2.extras.RealDictCursor` (rows come back as dicts) and
  takes care of commit/rollback and closing the cursor/connection.

There is no connection pooling: every call to ``get_cursor`` opens a brand
new connection and closes it afterwards. This is simple and safe for a
low-traffic scouting app, but would need pooling (e.g. via
``psycopg2.pool`` or SQLAlchemy) to scale to many concurrent requests.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from app.core import config


def get_connection():
    """Open a new raw psycopg2 connection to the configured PostgreSQL database.

    :return: A live ``psycopg2`` connection. The caller is responsible for
        closing it (prefer :func:`get_cursor` instead of calling this
        directly, unless you specifically need the raw connection).
    :rtype: psycopg2.extensions.connection
    """
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )


@contextmanager
def get_cursor(commit: bool = True):
    '''
    Context manager that yields a cursor and handles commit/rollback
    and connection cleanup automatically.

    :param commit: Whether to commit the transaction on success.
    :type commit: bool
    :yield: A ``RealDictCursor`` bound to a fresh connection. Rows fetched
        through it behave like dictionaries (``row["column_name"]``) rather
        than plain tuples.
    :raises Exception: Re-raises whatever exception occurred inside the
        ``with`` block, after rolling back the transaction.

    Example:
        >>> with get_cursor(commit=False) as cur:
        ...     cur.execute("SELECT * FROM pit_scout WHERE team_key = %s", ("frc7563",))
        ...     rows = cur.fetchall()
    '''
    conn = get_connection()

    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
