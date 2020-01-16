from time import sleep
from a4988 import A4988


class MecanumWheelsController:

    def __init__(self, left_down_wheel, left_up_wheel, right_down_wheel, right_up_wheel):
        # Left down wheel
        self.ld_wheel = left_down_wheel
        self.lu_wheel = left_up_wheel
        self.rd_wheel = right_down_wheel
        self.ru_wheel = right_up_wheel

    def move_forward(self):
        self.ld_wheel.move(1000, 1)
        self.lu_wheel.move(1000, 1)
        self.rd_wheel.move(1000, 1)
        self.ru_wheel.move(1000, 1)


if __name__ == "__main__":
    #        direction, step, enable
    wheel1 = A4988(13, 19, 26)
    wheel2 = A4988(16, 20, 21)
    wheel3 = A4988(5, 6, 12)
    wheel4 = A4988(23, 24, 25)
    m = MecanumWheelsController(wheel1, wheel2, wheel3, wheel4)
    m.move_forward()
