import psycopg2
from contextlib import contextmanager

from app.core import config


def get_connection():

    return psycopg2.connect(
        dbname=config.dbname,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port
    )


@contextmanager
def get_cursor(commit: bool = True):
    '''
    Context manager that yields a cursor and handles commit/rollback
    and connection cleanup automatically.

    :param commit: Whether to commit the transaction on success.
    :type commit: bool
    '''

    conn = get_connection()
    cur = conn.cursor()

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