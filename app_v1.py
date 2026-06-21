from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "/home/mike5d/trativod.db"


@app.route("/")
def index():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, distance_mm
        FROM measurements
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    conn.close()

    level_cm = None

    if row:
        level_cm = round(row[1] / 10, 1)

    return render_template(
        "index.html",
        level_cm=level_cm
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
