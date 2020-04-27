import threading
from time import sleep
# import RPi.GPIO as GPIO
from pynput.keyboard import Key, Listener
from testing_roboclaw.roboclaw_3 import Roboclaw


class MecanumRobot:

    def __init__(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        print("Init MecanumRobot started")
        self.address_front_wheels = 0x80
        self.address_rear_wheels = 0x81
        self.full_speed = 127
        self.sleep_time = 0.005
        self.roboclaw = Roboclaw("/dev/ttyS0", 38400)
        self.roboclaw.Open()
        print("-----------------Errors-----------------")
        print("-----------------Front wheels-----------------")
        print(self.roboclaw.ReadError(self.address_front_wheels))
        print("-----------------Rear wheels-----------------")
        print(self.roboclaw.ReadError(self.address_rear_wheels))
        print("-----------------Errors-----------------")
        self.roboclaw.SetMinVoltageMainBattery(self.address_front_wheels, 60)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_front_wheels, 150)

        self.roboclaw.SetMinVoltageMainBattery(self.address_rear_wheels, 60)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_rear_wheels, 150)
        print("-----------------Errors-----------------")
        print("-----------------Front wheels-----------------")
        print(self.roboclaw.ReadError(self.address_front_wheels))
        print("-----------------Rear wheels-----------------")
        print(self.roboclaw.ReadError(self.address_rear_wheels))
        print("-----------------Errors-----------------")
        print("Init MecanumRobot finished")

    def move_backward(self):
        threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)

    def move_forward(self):
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)

    def slide_right(self):
        threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)

    def slide_left(self):
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM1, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)

    def rotate_left(self):
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_front_wheels, self.full_speed)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.BackwardM2, args=(self.address_rear_wheels, self.full_speed)).start()
        sleep(self.sleep_time)

    def stop(self):
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_front_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM1, args=(self.address_rear_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_front_wheels, 0)).start()
        sleep(self.sleep_time)
        threading.Thread(target=self.roboclaw.ForwardM2, args=(self.address_rear_wheels, 0)).start()
        sleep(self.sleep_time)


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
    global key_pressed
    key_pressed = False
    m.stop()
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
