from services.database import get_connection


def get_last_level_cm():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT distance_mm
        FROM measurements
        ORDER BY timestamp DESC
        LIMIT 1
        """
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    return round(row[0] / 10.0, 1)


def get_history(range_name):

    conn = get_connection()
    cur = conn.cursor()

    if range_name == "1h":

        sql = """
        SELECT
            timestamp,
            ROUND(distance_mm / 10.0, 1)
        FROM measurements
        WHERE timestamp >= datetime('now','-1 hour')
        ORDER BY timestamp
        """

    elif range_name == "24h":

        sql = """
        SELECT
            substr(timestamp,1,16),
            ROUND(avg(distance_mm)/10.0,1)
        FROM measurements
        WHERE timestamp >= datetime('now','-24 hour')
        GROUP BY substr(timestamp,1,16)
        ORDER BY substr(timestamp,1,16)
        """

    elif range_name == "3d":

        sql = """
        SELECT
            strftime('%Y-%m-%d %H:',timestamp) ||
            printf('%02d',
            (cast(strftime('%M',timestamp) as integer)/5)*5),
            ROUND(avg(distance_mm)/10.0,1)
        FROM measurements
        WHERE timestamp >= datetime('now','-3 day')
        GROUP BY 1
        ORDER BY 1
        """

    elif range_name == "1w":

        sql = """
        SELECT
            strftime('%Y-%m-%d %H:',timestamp) ||
            printf('%02d',
            (cast(strftime('%M',timestamp) as integer)/15)*15),
            ROUND(avg(distance_mm)/10.0,1)
        FROM measurements
        WHERE timestamp >= datetime('now','-7 day')
        GROUP BY 1
        ORDER BY 1
        """

    else:

        sql = """
        SELECT
            strftime('%Y-%m-%d %H:00',timestamp),
            ROUND(avg(distance_mm)/10.0,1)
        FROM measurements
        WHERE timestamp >= datetime('now','-30 day')
        GROUP BY strftime('%Y-%m-%d %H',timestamp)
        ORDER BY strftime('%Y-%m-%d %H',timestamp)
        """

    cur.execute(sql)

    rows = cur.fetchall()

    conn.close()

    return [
        {
            "time": row[0],
            "level": row[1]
        }
        for row in rows
    ]
