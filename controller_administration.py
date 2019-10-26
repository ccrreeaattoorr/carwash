
import time
import logging
import threading
from controller import Controller
from subprocess import check_call


def thread_function(c):
    c.move_stepper()


if __name__ == "__main__":
    c1 = Controller(13, 19, 12, 16, 20, 21).enable_stepper()
    c2 = Controller(17, 27, 18, 23, 24, 25).enable_stepper()

    x1 = threading.Thread(target=thread_function, args=c1)
    x1.start()
    x2 = threading.Thread(target=thread_function, args=c2)
    x2.start()
