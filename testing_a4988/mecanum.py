import logging
import sys
import time
import threading
from time import sleep
from a4988 import A4988
from python_console_menu import AbstractMenu, MenuItem


class MecanumWheelsController:

    def __init__(self, left_down_wheel, left_up_wheel, right_down_wheel, right_up_wheel):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        # Left down wheel
        self.ld_wheel = left_down_wheel
        self.lu_wheel = left_up_wheel
        self.rd_wheel = right_down_wheel
        self.ru_wheel = right_up_wheel

    def init(self):
        self.ld_wheel.init_stepper()
        self.lu_wheel.init_stepper()
        self.rd_wheel.init_stepper()
        self.ru_wheel.init_stepper()

    def enable(self, delay=0.2):
        self.ld_wheel.enable_stepper()
        self.lu_wheel.enable_stepper()
        self.rd_wheel.enable_stepper()
        self.ru_wheel.enable_stepper()
        time.sleep(delay)

    def disable(self):
        self.ld_wheel.disable_stepper()
        self.lu_wheel.disable_stepper()
        self.rd_wheel.disable_stepper()
        self.ru_wheel.disable_stepper()

    def wait(self):
        while self.ld_wheel.is_moving or self.lu_wheel.is_moving or self.rd_wheel.is_moving or self.ru_wheel.is_moving:
            print("left down: {} left up: {} right down: {} right up: {}".format(self.ld_wheel.is_moving,
                                                                                 self.lu_wheel.is_moving,
                                                                                 self.rd_wheel.is_moving,
                                                                                 self.ru_wheel.is_moving))
            time.sleep(0.5)

    def pre_move(self):
        self.disable()
        self.enable()

    def post_move(self):
        self.enable()
        self.disable()

    def move_forward(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 1)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 0)
        # self.wait()

    def move_backward(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 0)
        self.rd_wheel.move_non_blocking(steps, 1)
        self.ru_wheel.move_non_blocking(steps, 1)
        # self.wait()

    def slide_left(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 1)
        self.lu_wheel.move_non_blocking(steps, 0)
        self.rd_wheel.move_non_blocking(steps, 1)
        self.ru_wheel.move_non_blocking(steps, 0)
        # self.wait()

    def slide_right(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 1)
        # self.wait()

    def concerning_left(self, steps=1000):
        self.pre_move()
        self.ld_wheel.enable_stepper()
        self.lu_wheel.disable_stepper()
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 0)
        # self.wait()

    def concerning_right(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 1)
        self.lu_wheel.move_non_blocking(steps, 1)
        self.rd_wheel.enable_stepper()
        self.ru_wheel.disable_stepper()
        # self.wait()

    def rotate_right(self, steps=1000):
        self.pre_move()
        self.ld_wheel.move_non_blocking(steps, 0)
        self.lu_wheel.move_non_blocking(steps, 0)
        self.rd_wheel.move_non_blocking(steps, 0)
        self.ru_wheel.move_non_blocking(steps, 0)


class MecanumWheelsMenu(AbstractMenu):
    show_hidden_menu = False

    def __init__(self):
        super().__init__("Welcome to the mecanum robot menu.")
        # direction, step, enable

        # left_down_wheel
        wheel1 = A4988(13, 19, 26)
        # left_up_wheel
        wheel2 = A4988(16, 20, 21)
        # right_down_wheel
        wheel3 = A4988(5, 6, 12)
        # right_up_wheel
        wheel4 = A4988(23, 24, 25)
        self.m = MecanumWheelsController(wheel1, wheel2, wheel3, wheel4)
        self.m.init()

    def initialise(self):
        self.add_menu_item(MenuItem(0, "Exit menu").set_as_exit_option())
        self.add_menu_item(MenuItem(1, "Stop", lambda: [print("Stop"), self.m.enable(), self.m.disable()]))
        self.add_menu_item(MenuItem(2, "Forward",
                                    lambda: [print("move forward"),
                                             self.m.move_forward(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(3, "Backward",
                                    lambda: [print("move backward"),
                                             self.m.move_backward(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(4, "Left",
                                    lambda: [print("move left"),
                                             self.m.slide_left(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(5, "Right",
                                    lambda: [print("move right"),
                                             self.m.slide_right(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(6, "Concerning Left",
                                    lambda: [print("concerning left"),
                                             self.m.concerning_left(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(7, "Concerning Right",
                                    lambda: [print("concerning right"),
                                             self.m.concerning_right(infinite_move),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(8, "Rotate Right",
                                    lambda: [print("rotate right"),
                                             self.m.rotate_right(infinite_move),
                                             print("moving")
                                             ]))


if __name__ == "__main__":
    # # direction, step, enable
    #
    # # left_down_wheel
    # wheel1 = A4988(13, 19, 26)
    # # left_up_wheel
    # wheel2 = A4988(16, 20, 21)
    # # right_down_wheel
    # wheel3 = A4988(5, 6, 12)
    # # right_up_wheel
    # wheel4 = A4988(23, 24, 25)
    # m = MecanumWheelsController(wheel1, wheel2, wheel3, wheel4)
    # m.init()
    infinite_move = -1

    menu = MecanumWheelsMenu()
    menu.display()


            #
            # if 'w' == key.char:
            #     print("w - forward")
            #     m.disable()
            #     m.enable()
            #     m.move_forward(infinite_move)
            #
            # if 's' == key.char:
            #     print("s - backward")
            #     m.disable()
            #     m.enable()
            #     m.move_backward(infinite_move)
            #
            # if 'a' == key.char:
            #     print("s - slide left")
            #     m.disable()
            #     m.enable()
            #     m.slide_left(infinite_move)
            #
            # if 'd' == key.char:
            #     print("s - slide right")
            #     m.disable()
            #     m.enable()
            #     m.slide_right(infinite_move)
