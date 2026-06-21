import sys
import sqlite3
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

RELAY_PIN = 17
DB_PATH = "/home/mike5d/trativod.db"

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def save_state(state):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO settings(key,value)
        VALUES('pump_state', ?)
        """,
        (state,)
    )

    cur.execute(
        """
        INSERT INTO pump_events
        (timestamp, state, source)
        VALUES(datetime('now'), ?, 'MANUAL')
        """,
        (state,)
    )

    if state == "ON":

        deadline = (
            datetime.now() + timedelta(minutes=10)
        ).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(
            """
            INSERT OR REPLACE INTO settings(key,value)
            VALUES('pump_off_deadline', ?)
            """,
            (deadline,)
        )

    else:

        cur.execute(
            """
            INSERT OR REPLACE INTO settings(key,value)
            VALUES('pump_off_deadline', '')
            """
        )

    conn.commit()
    conn.close()

if len(sys.argv) != 2:
    print("Použití: python3 pump.py on/off")
    sys.exit(1)

cmd = sys.argv[1].lower()

if cmd == "on":

    GPIO.output(RELAY_PIN, GPIO.LOW)
    save_state("ON")
    print("Pump ON")

elif cmd == "off":

    GPIO.output(RELAY_PIN, GPIO.HIGH)
    save_state("OFF")
    print("Pump OFF")

else:

    print("Neznámý příkaz:", cmd)
