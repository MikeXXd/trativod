import serial
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

print("Čtu data ze senzoru A01NYUB (Ctrl+C pro ukončení)")

while True:
    if ser.read(1) == b'\xFF':          # začátek rámce
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
            else:
                print("Chyba checksum")

    time.sleep(0.1)
