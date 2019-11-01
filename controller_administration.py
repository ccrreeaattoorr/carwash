import sys
import time
import logging
import argparse
import threading
from subprocess import check_call


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Controller administration Args')
    parser.add_argument('--mock', type=bool, default=False, help='Mock controller')
    parser.add_argument('--steps', type=int, default=1000, help='Steps')
    parser.add_argument('--direction', type=str, default='forward', help='direction (forward or backward')
    parser.add_argument('--delay', type=str, default='MAX', help='delay between steps')
    args = parser.parse_args()

    if args.mock:
        from controller_mock import Controller
    else:
        from controller import Controller

    c1 = Controller(13, 19, 12, 16, 20, 21)
    c2 = Controller(17, 27, 18, 23, 24, 25)

    c1.move_stepper(args.steps)
    c2.move_stepper(args.steps)
