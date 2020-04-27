import threading
from time import sleep
#import RPi.GPIO as GPIO
from roboclaw_3 import Roboclaw
from python_console_menu import AbstractMenu, MenuItem


class MecanumRobot:

    def __init__(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        self.address_front_wheels = 0x80
        self.address_rear_wheels = 0x81
        self.full_speed = 127
        self.sleep_time = 0.005
        self.roboclaw = Roboclaw("/dev/ttyS0", 38400)
        self.roboclaw.Open()
        print("Error")
        print(self.roboclaw.ReadError(self.address_front_wheels))
        self.roboclaw.SetMinVoltageMainBattery(self.address_front_wheels, 62)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_front_wheels, 112)

        self.roboclaw.SetMinVoltageMainBattery(self.address_rear_wheels, 62)
        self.roboclaw.SetMaxVoltageMainBattery(self.address_rear_wheels, 112)

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


class MecanumRobotMenu(AbstractMenu):

    def __init__(self):
        super().__init__("Welcome to the mecanum robot menu.")
        self.m = MecanumRobot()

    def initialise(self):
        self.add_menu_item(MenuItem(0, "Exit menu").set_as_exit_option())
        self.add_menu_item(MenuItem(1, "Stop", lambda: [print("Stop"), self.m.stop()]))
        self.add_menu_item(MenuItem(2, "Forward",
                                    lambda: [print("move forward"),
                                             self.m.move_forward(),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(3, "Backward",
                                    lambda: [print("move backward"),
                                             self.m.move_backward(),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(4, "Left",
                                    lambda: [print("move left"),
                                             self.m.slide_left(),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(5, "Right",
                                    lambda: [print("move right"),
                                             self.m.slide_right(),
                                             print("moving")
                                             ]))
        self.add_menu_item(MenuItem(6, "Rotate Right",
                                    lambda: [print("rotate right"),
                                             self.m.rotate_left(),
                                             print("moving")
                                             ]))


if __name__ == "__main__":
    demoMenu = MecanumRobotMenu()
    demoMenu.display()

