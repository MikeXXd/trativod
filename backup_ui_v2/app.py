from flask import Flask, render_template, redirect
import sqlite3
import subprocess

app = Flask(__name__)

DB_PATH = "/home/mike5d/trativod.db"


@app.route("/")
def index():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT distance_mm
        FROM measurements
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    level_cm = None

    if row:
        level_cm = round(row[0] / 10, 1)

    cur.execute("""
        SELECT value
        FROM settings
        WHERE key='pump_state'
    """)

    pump_row = cur.fetchone()

    pump_state = "UNKNOWN"

    if pump_row:
        pump_state = pump_row[0]

    cur.execute("""
        SELECT value
        FROM settings
        WHERE key='auto_mode'
    """)

    auto_row = cur.fetchone()

    auto_mode = "0"

    if auto_row:
        auto_mode = auto_row[0]

    conn.close()

    return render_template(
        "index.html",
        level_cm=level_cm,
        pump_state=pump_state,
        auto_mode=auto_mode
    )

@app.route("/pump/on")
def pump_on():

    subprocess.run(
        ["python3", "/home/mike5d/pump.py", "on"]
    )

    return redirect("/")


@app.route("/pump/off")
def pump_off():

    subprocess.run(
        ["python3", "/home/mike5d/pump.py", "off"]
    )

    return redirect("/")

@app.route("/auto/toggle")
def auto_toggle():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM settings
        WHERE key='auto_mode'
    """)

    row = cur.fetchone()

    current = "0"

    if row:
        current = row[0]

    new_value = "1" if current == "0" else "0"

    cur.execute("""
        INSERT OR REPLACE INTO settings(key,value)
        VALUES('auto_mode', ?)
    """, (new_value,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
