import sys
import time
import logging
import argparse
import itertools
import constants
import threading
import RPi.GPIO as GPIO
consts = constants.Constants(variable='AN_ENVIRONMENT_VARIABLE', filename='constants.cfg')


class Controller:

    id_iter = itertools.count()

    def __init__(self, enable_a, enable_b, coil_a_1_pin, coil_a_2_pin, coil_b_1_pin, coil_b_2_pin):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.id = next(self.id_iter)
        self.is_stepper_enabled = False
        self.is_moving_now = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Enable GPIO pins for  ENA and ENB for stepper
        self.enable_a = enable_a
        self.enable_b = enable_b

        # Enable pins for IN1-4 to control step sequence
        self.coil_A_1_pin = coil_a_1_pin
        self.coil_A_2_pin = coil_a_2_pin
        self.coil_B_1_pin = coil_b_1_pin
        self.coil_B_2_pin = coil_b_2_pin

    def enable_stepper(self):
        # Set pin states
        GPIO.setup(self.enable_a, GPIO.OUT)
        GPIO.setup(self.enable_b, GPIO.OUT)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

        # Set ENA and ENB to high to enable stepper
        GPIO.output(self.enable_a, True)
        GPIO.output(self.enable_b, True)

        self.is_stepper_enabled = True
        logging.info(
            "id:{} stepper enabled: {} moving now: {}".format(self.id, self.is_stepper_enabled, self.is_moving_now))

    # Function for step sequence
    def set_step(self, w1, w2, w3, w4):
        # logging.INFO('id: {} w1: {} w2: {} w3: {} w4: {}'.format(self.id, w1, w2, w3, w4))
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def non_blocking_move_stepper(self, steps, direction="forward", speed=consts.MAX_SPEED):
        # loop through step sequence based on number of steps
        logging.info("id:{} steps: {} direction: {} speed: {}".format(self.id, steps, direction, speed))
        self.enable_stepper()
        if self.is_stepper_enabled and not self.is_moving_now:
            self.is_moving_now = True
            logging.info("id:{} moving now: {}".format(self.id, self.is_moving_now))

            if direction in "forward":
                for i in range(0, steps):
                    self.set_step(1, 0, 1, 0)
                    time.sleep(speed)
                    self.set_step(0, 1, 1, 0)
                    time.sleep(speed)
                    self.set_step(0, 1, 0, 1)
                    time.sleep(speed)
                    self.set_step(1, 0, 0, 1)
                    time.sleep(speed)
            elif direction in "backward":
                for i in range(0, steps):
                    self.set_step(1, 0, 0, 1)
                    time.sleep(speed)
                    self.set_step(0, 1, 0, 1)
                    time.sleep(speed)
                    self.set_step(0, 1, 1, 0)
                    time.sleep(speed)
                    self.set_step(1, 0, 1, 0)
                    time.sleep(speed)
        self.is_moving_now = False
        logging.info("id:{} moving_now: {}".format(self.id, self.is_moving_now))
        self.disable_stepper()

    def move_stepper(self, steps, direction="forward", speed=consts.MAX_SPEED):
        thread = threading.Thread(target=self.non_blocking_move_stepper, args=(steps, direction, speed))
        thread.start()

    def disable_stepper(self):
        self.is_stepper_enabled = False
        self.is_moving_now = False
        GPIO.output(self.enable_a, False)
        GPIO.output(self.enable_b, False)
        logging.info(
            "id:{} stepper enabled: {} moving now: {}".format(self.id, self.is_stepper_enabled, self.is_moving_now))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connected pins')
    parser.add_argument('--enable_a', type=int, help='ENA')
    parser.add_argument('--enable_b', type=int, help='ENB')
    parser.add_argument('--coil_A_1_pin', type=int, help='Input1')
    parser.add_argument('--coil_A_2_pin', type=int, help='Input2')
    parser.add_argument('--coil_B_1_pin', type=int, help='Input3')
    parser.add_argument('--coil_B_2_pin', type=int, help='Input4')
    args = parser.parse_args()

    con = Controller(args.enable_a, args.enable_b, args.coil_A_1_pin, args.coil_A_2_pin, args.coil_B_1_pin,
                     args.coil_B_2_pin)
    con.enable_stepper()
    con.move_stepper(1000)
