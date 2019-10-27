import time
import logging
import threading
from controller_mock import Controller
from subprocess import check_call


class ControllerThread:

    def __init__(self, _c1, _c2):
        self.c1 = _c1
        self.c2 = _c2

    def thread_function(self):
        print("thread")
        self.c1.move_stepper(1000)
        self.c2.move_stepper(1000, direction="backward")


if __name__ == "__main__":
    c1 = Controller(13, 19, 12, 16, 20, 21)
    c2 = Controller(17, 27, 18, 23, 24, 25)
    c1.enable_stepper()
    c2.enable_stepper()

    ct = ControllerThread(c1, c2)

    x1 = threading.Thread(target=ct.thread_function)
    x1.start()
    x2 = threading.Thread(target=ct.thread_function)
    x2.start()
