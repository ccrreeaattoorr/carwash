import time
import threading
from time import sleep
from a4988 import A4988


class MecanumWheelsController:

    def __init__(self, left_down_wheel, left_up_wheel, right_down_wheel, right_up_wheel):
        # Left down wheel
        self.ld_wheel = left_down_wheel
        self.lu_wheel = left_up_wheel
        self.rd_wheel = right_down_wheel
        self.ru_wheel = right_up_wheel

    def wait(self):
        while self.ld_wheel.is_moving or self.lu_wheel.is_moving or self.rd_wheel.is_moving or self.ru_wheel.is_moving:
            print("left down: {} left up: {} right down: {} right up: {}".format(self.ld_wheel.is_moving,
                                                                                 self.lu_wheel.is_moving,
                                                                                 self.rd_wheel.is_moving,
                                                                                 self.ru_wheel.is_moving))
            time.sleep(0.5)

    def move_forward(self, steps=1000):
        self.ld_wheel.move_non_blocking(steps, 1)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.move_non_blocking(steps, 1)
        self.ru_wheel.move_non_blocking(steps, 1)
        self.wait()

    def move_backward(self, steps=1000):
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 0)
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 0)
        self.wait()

    def slide_left(self, steps=1000):
        self.ld_wheel.move_non_blocking(steps, 1)
        self.lu_wheel.move_non_blocking(steps, 0)
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 1)
        self.wait()

    def slide_right(self, steps=1000):
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.move_non_blocking(steps, 1)
        self.ru_wheel.move_non_blocking(steps, 0)
        self.wait()

    def rotate_left(self, steps=1000):
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.move_non_blocking(steps, 1)
        self.ru_wheel.move_non_blocking(steps, 0)
        self.wait()


if __name__ == "__main__":
    # direction, step, enable

    # left_down_wheel
    wheel1 = A4988(13, 19, 26)
    # left_up_wheel
    wheel2 = A4988(16, 20, 21)
    # right_down_wheel
    wheel3 = A4988(5, 6, 12)
    # right_up_wheel
    wheel4 = A4988(23, 24, 25)
    m = MecanumWheelsController(wheel1, wheel2, wheel3, wheel4)
    m.move_forward(5000)
    time.sleep(2)
    m.move_backward(5000)
    time.sleep(2)
    m.slide_left(5000)
    time.sleep(2)
    m.slide_right(5000)

