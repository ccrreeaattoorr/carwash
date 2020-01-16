from time import sleep
import RPi.GPIO as GPIO


class A4988:

    def __init__(self, direction, step, enable):
        # DIR = 13   # Direction GPIO Pin
        # STEP = 19  # Step GPIO Pin
        # CW = 1     # Clockwise Rotation
        # CCW = 0    # Counterclockwise Rotation
        # SPR = 1000   # Steps per Revolution (360 / 7.5)
        # ENA = 26
        self.dir = direction
        self.step = step
        self.enable = enable
        self.delay = .001

    def enable_stepper(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)

    def move(self, step_count, direction):
        self.enable_stepper()

        GPIO.output(self.enable, GPIO.HIGH)
        GPIO.output(self.dir, direction)
        for x in range(step_count):
            GPIO.output(self.step, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.step, GPIO.LOW)
            sleep(self.delay)

        self.disable_stepper()

    def disable_stepper(self):
        GPIO.output(self.enable, GPIO.LOW)
        GPIO.cleanup()


if __name__ == "__main__":
    c = A4988(13, 19, 26)
    c.move(1000, 1)
    c.move(1000, 0)
