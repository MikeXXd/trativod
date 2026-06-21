import serial
import time
import logging
import sqlite3
import subprocess
from datetime import datetime

logging.basicConfig(
    filename="/var/log/pump_controller.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

logging.info("Pump controller started")

print("Čtu data ze senzoru A01NYUB (Ctrl+C pro ukončení)")

ser = serial.Serial(
    port="/dev/serial0",
    baudrate=9600,
    timeout=1
)

DB_PATH = "/home/mike5d/trativod.db"

samples = []
last_save = time.time()


def check_pump_timeout():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM settings
        WHERE key='pump_state'
    """)

    row = cur.fetchone()

    if not row or row[0] != "ON":
        conn.close()
        return

    cur.execute("""
        SELECT value
        FROM settings
        WHERE key='pump_off_deadline'
    """)

    row = cur.fetchone()

    if not row or not row[0]:
        conn.close()
        return

    try:
        deadline = datetime.strptime(
            row[0],
            "%Y-%m-%d %H:%M:%S"
        )
    except Exception as e:
        logging.error(f"Deadline parse error: {e}")
        conn.close()
        return

    if datetime.now() >= deadline:

        logging.info("Pump timeout reached -> OFF")

        subprocess.run(
            ["python3", "/home/mike5d/pump.py", "off"]
        )

    conn.close()


while True:

    check_pump_timeout()

    if ser.read(1) == b'\xFF':

        data = ser.read(3)

        if len(data) == 3:

            high = data[0]
            low = data[1]
            checksum = data[2]

            distance_mm = high * 256 + low

            calc_checksum = (
                0xFF + high + low
            ) & 0xFF

            if checksum == calc_checksum:

                samples.append(distance_mm)

                print(
                    f"Vzdálenost: {distance_mm} mm "
                    f"({distance_mm / 10:.1f} cm)"
                )

            else:

                logging.warning("Chyba checksum")

    now = time.time()

    if now - last_save >= 10:

        if samples:

            avg_mm = sum(samples) / len(samples)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO measurements
                (timestamp, distance_mm)
                VALUES(datetime('now'), ?)
                """,
                (avg_mm,)
            )

            conn.commit()
            conn.close()

            logging.info(
                f"AVG 10s: {avg_mm:.1f} mm "
                f"({avg_mm / 10:.1f} cm)"
            )

            print(
                f"ULOŽENO AVG: {avg_mm:.1f} mm "
                f"({avg_mm / 10:.1f} cm)"
            )

        samples = []
        last_save = now

    time.sleep(0.05)
