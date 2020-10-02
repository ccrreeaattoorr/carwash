import threading
from time import sleep
# import RPi.GPIO as GPIO
from pynput.keyboard import Key, Listener
# from testing_roboclaw.roboclaw_3 import Roboclaw


def move(name):
    print("move start - {}".format(name))
    sleep(2)
    print("move end - {}".format(name))


def stop(name):
    print("stop start - {}".format(name))
    sleep(2)
    print("stop end - {}".format(name))


class MecanumRobot:

    def __init__(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        print("Init MecanumRobot started")
        self.address_front_wheels = 0x80
        self.address_rear_wheels = 0x81
        self.full_speed = 127
        self.sleep_time = 0.005
        # self.roboclaw = Roboclaw("/dev/ttyS0", 38400)
        # self.roboclaw.Open()
        # print("-----------------Errors-----------------")
        # print("-----------------Front wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_front_wheels))
        # print("-----------------Rear wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_rear_wheels))
        # print("-----------------Errors-----------------")
        # self.roboclaw.SetMinVoltageMainBattery(self.address_front_wheels, 60)
        # self.roboclaw.SetMaxVoltageMainBattery(self.address_front_wheels, 150)

        # self.roboclaw.SetMinVoltageMainBattery(self.address_rear_wheels, 60)
        # self.roboclaw.SetMaxVoltageMainBattery(self.address_rear_wheels, 150)
        # print("-----------------Errors-----------------")
        # print("-----------------Front wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_front_wheels))
        # print("-----------------Rear wheels-----------------")
        # print(self.roboclaw.ReadError(self.address_rear_wheels))
        # print("-----------------Errors-----------------")
        print("Init MecanumRobot finished")

    def move_backward(self):
        threading.Thread(target=move, args=("backward_1",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("backward_2",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("backward_3",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("backward_4",)).start()
        sleep(self.sleep_time)

    def move_forward(self):
        print("move_forward start")
        threading.Thread(target=move, args=("forward_1",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("forward_2",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("forward_3",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("forward_4",)).start()
        sleep(self.sleep_time)
        print("move_forward end")

    def slide_right(self):
        threading.Thread(target=move, args=("right_1",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("right_2",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("right_3",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("right_4",)).start()
        sleep(self.sleep_time)

    def slide_left(self):
        threading.Thread(target=move, args=("left_1",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("left_2",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("left_3",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args=("left_4",)).start()
        sleep(self.sleep_time)

    def rotate_left(self):
        threading.Thread(target=move, args="rotate_left_1").start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args="rotate_left_2").start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args="rotate_left_3").start()
        sleep(self.sleep_time)
        threading.Thread(target=move, args="rotate_left_4").start()
        sleep(self.sleep_time)

    def stop(self):
        print("stop function start")
        threading.Thread(target=stop, args=("stop_1",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=stop, args=("stop_2",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=stop, args=("stop_3",)).start()
        sleep(self.sleep_time)
        threading.Thread(target=stop, args=("stop_4",)).start()
        sleep(self.sleep_time)
        print("stop function end")


key_pressed = False
m = MecanumRobot()


def on_press(key):
    global key_pressed
    # print("key pressed: {}".format(key_pressed))
    if not key_pressed:
        key_pressed = True
        print('{0} pressed'.format(key))
        if hasattr(key, 'char'):
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


def on_release(key):
    print('{0} release'.format(
        key))
    global key_pressed
    key_pressed = False
    m.stop()
    if key == Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
