from services.database import get_connection


def get_setting(key, default=None):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT value
        FROM settings
        WHERE key=?
        """,
        (key,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return default


def set_setting(key, value):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO settings(key,value)
        VALUES(?, ?)
        """,
        (key, str(value))
    )

    conn.commit()
    conn.close()
