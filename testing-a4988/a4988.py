import sys
import logging
import threading
from time import sleep
import RPi.GPIO as GPIO


class A4988:

    def __init__(self, direction, step, enable):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        # GPIO pins
        self.dir = direction
        self.step = step
        self.enable = enable
        self.delay = .001
        self.is_moving = False
        logging.info("Pins\nDirection: {} Step: {} Enable: {}".format(self.dir, step, enable))

    def enable_stepper(self):
        self.is_moving = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.output(self.enable, GPIO.HIGH)
        logging.info("enable_stepper")
        # logging.info("is_moving {}".format(self.is_moving))

    def move_non_blocking(self, step_count, direction):
        logging.info("move_non_blocking")
        self.busy_wait()
        thread = threading.Thread(target=self.__move, args=(step_count, direction))
        thread.start()

    def busy_wait(self):
        while self.is_moving:
            sleep(0.2)
            logging.info("Busy wait sleep")

    def __move(self, step_count, direction):
        if not self.is_moving:
            self.enable_stepper()
            logging.info("move")

            GPIO.output(self.dir, direction)
            for x in range(step_count):
                GPIO.output(self.step, GPIO.HIGH)
                sleep(self.delay)
                GPIO.output(self.step, GPIO.LOW)
                sleep(self.delay)

            self.disable_stepper()

    def disable_stepper(self):
        logging.info("disable_stepper")
        GPIO.output(self.enable, GPIO.LOW)
        self.is_moving = False
        # GPIO.cleanup()


if __name__ == "__main__":
    c = A4988(23, 24, 25)
    logging.info("1 task")
    c.move_non_blocking(1000, 1)
    # logging.info("2 task")
    # c.move_non_blocking(1000, 0)
