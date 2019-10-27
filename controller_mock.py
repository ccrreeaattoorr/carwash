import time
import argparse


class Controller:

    def __init__(self, enable_a, enable_b, coil_a_1_pin, coil_a_2_pin, coil_b_1_pin, coil_b_2_pin):

        self.is_stepper_enabled = False
        self.is_moving_now = False

        # Variables
        # self.delay = 0.0008
        # self.steps = 0
        # self.direction = "forward"

        # Enable GPIO pins for  ENA and ENB for stepper
        self.enable_a = enable_a
        self.enable_b = enable_b

        # Enable pins for IN1-4 to control step sequence
        self.coil_A_1_pin = coil_a_1_pin
        self.coil_A_2_pin = coil_a_2_pin
        self.coil_B_1_pin = coil_b_1_pin
        self.coil_B_2_pin = coil_b_2_pin

        print("Init complete")

    def enable_stepper(self):
        # Set pin states
        self.is_stepper_enabled = True
        print("is_stepper_enabled: {}".format(self.is_stepper_enabled))

    # Function for step sequence
    def set_step(self, w1, w2, w3, w4):
        print("step {} {} {} {}".format(w1, w2, w3, w4))

    def move_stepper(self, steps, direction="forward", delay=0.0008):
        # loop through step sequence based on number of steps
        print("steps {} direction: {} delay {}".format(steps, direction, delay))
        if self.is_stepper_enabled and not self.is_moving_now:
            self.is_moving_now = True
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
        print("is_stepper_enabled: {}".format(self.is_stepper_enabled))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--enable_a', type=int, help='ENA')
    parser.add_argument('--enable_b', type=int, help='ENB')
    parser.add_argument('--coil_A_1_pin', type=int, help='Input1')
    parser.add_argument('--coil_A_2_pin', type=int, help='Input2')
    parser.add_argument('--coil_B_1_pin', type=int, help='Input3')
    parser.add_argument('--coil_B_2_pin', type=int, help='Input4')
    # parser.add_argument('--delay', type=int, help='Delay', default=0.0008)
    # parser.add_argument('--steps', type=int, help='Steps', default=1000)
    # parser.add_argument('--direction', type=str, help='Direction', default="forward")
    args = parser.parse_args()

    c = Controller(args.enable_a, args.enable_b, args.coil_A_1_pin, args.coil_A_2_pin, args.coil_B_1_pin,
                   args.coil_B_2_pin)
    c.enable_stepper()
    c.move_stepper(3)
