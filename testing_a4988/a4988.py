import sys
import logging
import threading
import itertools
from time import sleep
import RPi.GPIO as GPIO


class A4988:

    id_iter = itertools.count()

    def __init__(self, direction, step, enable):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.id = next(self.id_iter)

        # GPIO pins
        self.dir = direction
        self.step = step
        self.enable = enable
        self.delay = .001

        # Setup flags
        self.is_moving = False
        self.enabled = False
        self.continuous_move = False

        logging.info("Pins\nDirection: {} Step: {} Enable: {}".format(self.dir, step, enable))

    def init_stepper(self):
        self.is_moving = False
        self.enabled = False
        self.continuous_move = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        logging.info("init stepper")

    def enable_stepper(self):
        if not self.enabled:
            self.enabled = True
            self.is_moving = False
            self.continuous_move = False
            GPIO.output(self.enable, GPIO.HIGH)
            logging.info("enable stepper")
        else:
            logging.info("stepper is already enabled")

    def move_non_blocking(self, step_count, direction):
        logging.info("move_non_blocking")
        # self.busy_wait()
        thread = threading.Thread(target=self.__move, args=(step_count, direction))
        thread.start()

    def busy_wait(self):
        while self.is_moving:
            sleep(0.01)
            logging.info("Busy wait sleep")

    def __step(self):
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)

    def __move(self, step_count, direction):
        if self.enabled and not self.is_moving:
            # self.enable_stepper()
            self.is_moving = True
            logging.info("move")

            GPIO.output(self.dir, direction)
            if step_count == -1:
                self.continuous_move = True
                while self.continuous_move:
                    self.__step()
            else:
                for x in range(step_count):
                    self.__step()

            # self.disable_stepper()
            self.is_moving = False
            logging.info("finished move")
        else:
            logging.info("skipped move, stepper is moving now")

    def disable_stepper(self):
        if self.enabled:
            logging.info("disable_stepper")
            GPIO.output(self.enable, GPIO.LOW)
            self.enabled = False
            self.is_moving = False
            self.continuous_move = False
            # GPIO.cleanup()
        else:
            logging.info("stepper is already disabled")


if __name__ == "__main__":
    # c = A4988(23, 24, 25)
    # c = A4988(16, 20, 21)
    # c = A4988(13, 19, 26)
    c = A4988(13, 19, 26)
    c.init_stepper()
    c.enable_stepper()
    c.move_non_blocking(-1, 0)
    sleep(60)
    c.disable_stepper()

