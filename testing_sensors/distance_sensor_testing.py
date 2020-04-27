import time
import VL53L1X

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x30)
tof.open()  # Initialise the i2c bus and configure the sensor

time_to_run = 60
tof.set_timing(66000, 70)
tof.start_ranging(3)  # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
t_end = time.time() + time_to_run

try:
    while time.time() < t_end:
        distance_in_mm = tof.get_distance()  # Grab the range in mm
        print(distance_in_mm)
except KeyboardInterrupt:
    print("Ctrl+C was pressed")
finally:
    tof.stop_ranging()  # Stop ranging
