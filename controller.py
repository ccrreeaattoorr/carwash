import time
import argparse
import RPi.GPIO as GPIO
#--enable_a 17 --enable_b 27 --coil_A_1_pin 18 --coil_A_2_pin 23 --coil_B_1_pin 24 --coil_B_2_pin 25 --direction backward


class Controller:

    def __init__(self, enable_a, enable_b, coil_a_1_pin, coil_a_2_pin, coil_b_1_pin, coil_b_2_pin):

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
        print("is_stepper_enabled: {}".format(self.is_stepper_enabled))

    # Function for step sequence
    def set_step(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def move_stepper(self, steps, direction="forward", delay=0.008):
        # loop through step sequence based on number of steps
        print("steps {} direction: {} delay {}".format(steps, direction, delay))

        if self.is_stepper_enabled and not self.is_moving_now:
            self.is_moving_now = True
            print("self.is_moving_now: {}".format(self.is_moving_now))
            if direction in "forward":
                for i in range(0, steps):
                    self.set_step(1, 0, 1, 0)
                    time.sleep(delay)
                    self.set_step(0, 1, 1, 0)
                    time.sleep(delay)
                    self.set_step(0, 1, 0, 1)
                    time.sleep(delay)
                    self.set_step(1, 0, 0, 1)
                    time.sleep(delay)
            elif direction in "backward":
                for i in range(0, steps):
                    self.set_step(1, 0, 0, 1)
                    time.sleep(delay)
                    self.set_step(0, 1, 0, 1)
                    time.sleep(delay)
                    self.set_step(0, 1, 1, 0)
                    time.sleep(delay)
                    self.set_step(1, 0, 1, 0)
                    time.sleep(delay)
        self.is_moving_now = False

    def disable_stepper(self):
        self.is_stepper_enabled = False
        self.is_moving_now = False
        GPIO.output(self.enable_a, False)
        GPIO.output(self.enable_b, False)
        print("is_stepper_enabled: {}, is_moving_now = {}".format(self.is_stepper_enabled, self.is_moving_now))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--enable_a', type=int, help='ENA')
    parser.add_argument('--enable_b', type=int, help='ENB')
    parser.add_argument('--coil_A_1_pin', type=int, help='Input1')
    parser.add_argument('--coil_A_2_pin', type=int, help='Input2')
    parser.add_argument('--coil_B_1_pin', type=int, help='Input3')
    parser.add_argument('--coil_B_2_pin', type=int, help='Input4')
    args = parser.parse_args()

    c = Controller(args.enable_a, args.enable_b, args.coil_A_1_pin, args.coil_A_2_pin, args.coil_B_1_pin,
                   args.coil_B_2_pin)
    c.enable_stepper()
    c.move_stepper(1000)
