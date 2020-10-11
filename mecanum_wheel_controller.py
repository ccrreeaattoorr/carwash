import timeit
import threading
from enum import Enum
from time import sleep
# import RPi.GPIO as GPIO
from pynput.keyboard import Key, Listener
from testing_roboclaw.roboclaw_3 import Roboclaw


class MecanumRobotDirection(Enum):
    stop = 0
    forward = 1
    backward = 2
    slide_right = 3
    slide_left = 4
    rotate_left = 5
    rotate_right = 6
    up_left = 7
    up_right = 8
    down_left = 9
    down_right = 10


class MecanumRobot:

    def __init__(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        print("Init MecanumRobot started")
        self.address_front_wheels = 0x80
        self.address_rear_wheels = 0x81
        self.full_speed = 40
        self.sleep_time = 0.005
        self.sleep_time_long = 3.1
        self.roboclaw = Roboclaw("/dev/ttyS0", 38400)
        self.roboclaw.Open()
        self.direction = MecanumRobotDirection.stop
        self.lock = threading.Lock()
        self.stop()
        # print("-----------------Errors-----------------")
        # print("-----------------Front wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_front_wheels))
        # print("-----------------Rear wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_rear_wheels))
        # print("-----------------Errors-----------------")
        self.roboclaw.SetMinVoltageMainBattery(self.address_front_wheels, 60)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_front_wheels, 150)

        self.roboclaw.SetMinVoltageMainBattery(self.address_rear_wheels, 60)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_rear_wheels, 150)
        # print("-----------------Errors-----------------")
        # print("-----------------Front wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_front_wheels))
        # print("-----------------Rear wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_rear_wheels))
        # print("-----------------Errors-----------------")
        print("Init MecanumRobot finished")

    def pre_check(self, direction):
        if self.direction != direction:
            if self.direction != MecanumRobotDirection.stop:
                self.stop()
            self.direction = direction
            return True
        return False

    def move_backward(self):
        print("move_backward() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.backward):
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("move_backward() stop")

    def move_forward(self):
        print("move_forward() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.forward):
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("move_forward() stop")

    def slide_right(self):
        print("slide_right() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.slide_right):
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("slide_right() stop")

    def slide_left(self):
        print("slide_left() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.slide_left):
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("slide_left() stop")

    def rotate_right(self):
        print("rotate_right() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.rotate_right):
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("rotate_right() stop")

    def rotate_left(self):
        print("rotate_left() start")
        self.lock.acquire()
        try:
            if self.pre_check(direction=MecanumRobotDirection.rotate_left):
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels,
                                                                       self.full_speed)).start()
                sleep(self.sleep_time)
                threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels,
                                                                        self.full_speed)).start()
                sleep(self.sleep_time_long)
        finally:
            self.lock.release()
        print("rotate_left() stop")

    def stop(self):
        print("stop wheels start")
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels, 0)).start()
        sleep(self.sleep_time_long)
        print("stop wheels end")


key_pressed = False
m = MecanumRobot()


def on_press(key):
    print('{0} pressed'.format(key))
    global key_pressed
    if hasattr(key, 'char') and not key_pressed:
        key_pressed = True
        if 'w' == key.char:
            print("w - forward")
            m.move_forward()
        if 'a' == key.char:
            print("a - left")
            m.slide_left()
        if 'd' == key.char:
            print("d - right")
            m.slide_right()
        if 's' == key.char:
            print("s - backward")
            m.move_backward()
        if 'z' == key.char:
            print("z - rotate left")
            m.rotate_left()
        if 'x' == key.char:
            print("x - rotate right")
            m.rotate_right()
        if 't' == key.char:
            print("t - stop")
            m.stop()


def on_release(key):
    global key_pressed
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        m.stop()
        return False
    key_pressed = False


if __name__ == "__main__":

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
