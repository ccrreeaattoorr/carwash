import sys
import time
import logging
import argparse
import threading
from subprocess import check_call


class ControllerThread:

    def __init__(self, **kwargs):
        self.controllers = kwargs

    def thread_function(self):
        for c in self.controllers:
            self.controllers[c].move_stepper(1000)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Controller administration Args')
    parser.add_argument('--mock', type=bool, default=False, help='Mock controller')
    args = parser.parse_args()

    if args.mock:
        from controller_mock import Controller
    else:
        from controller import Controller

    c1 = Controller(13, 19, 12, 16, 20, 21)
    c2 = Controller(17, 27, 18, 23, 24, 25)
    c1.enable_stepper()
    c2.enable_stepper()

    controllers = {"c1": c1, "c2": c2}
    ct = ControllerThread(**controllers)

    x1 = threading.Thread(target=ct.thread_function)
    x1.start()
    x1.join()

    c1.disable_stepper()
    c2.disable_stepper()
