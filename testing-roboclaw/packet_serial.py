from time import sleep
from roboclaw import Roboclaw

if __name__ == "__main__":
    
    address = 0x80
    roboclaw = Roboclaw("/dev/ttyS0", 38400)
    roboclaw.Open()

    roboclaw.ForwardM1(address, 64)
    sleep(2)
    roboclaw.ForwardM1(address, 0)
    sleep(2)
    roboclaw.BackwardM1(address, 64)
    sleep(2)
    roboclaw.BackwardM1(address, 0)
    sleep(2)
