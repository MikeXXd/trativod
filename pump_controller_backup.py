import serial
import time
import logging

logging.basicConfig(
    filename="/var/log/pump_controller.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

logging.info("Pump controller started")
print("Čtu data ze senzoru A01NYUB (Ctrl+C pro ukončení)")

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

while True:
    if ser.read(1) == b'\xFF':  # začátek rámce
        data = ser.read(3)
        if len(data) == 3:
            high = data[0]
            low = data[1]
            checksum = data[2]

            distance_mm = high * 256 + low
            calc_checksum = (0xFF + high + low) & 0xFF

            if checksum == calc_checksum:
                print(
                    f"Vzdálenost: {distance_mm} mm "
                    f"({distance_mm / 10:.1f} cm)"
                )
                logging.info(
                    f"Vzdalenost: {distance_mm} mm "
                    f"({distance_mm / 10:.1f} cm)"
                )
            else:
                print("Chyba checksum")
                logging.warning("Chyba checksum")

    time.sleep(0.1)

