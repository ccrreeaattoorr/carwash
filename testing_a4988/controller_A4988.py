from time import sleep
import RPi.GPIO as GPIO

DIR = 13   # Direction GPIO Pin
STEP = 19  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1000   # Steps per Revolution (360 / 7.5)
ENA = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CCW)

step_count = SPR
delay = .001
GPIO.output(ENA, GPIO.HIGH)

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.output(ENA, GPIO.LOW)
GPIO.cleanup()
