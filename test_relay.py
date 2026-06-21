import RPi.GPIO as GPIO
import time

RELAY_PIN = 17  # GPIO17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Relé VYPNUTO")
        time.sleep(15)

        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Relé ZAPNUTO")
        time.sleep(15)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Konec")
