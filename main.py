import time
from mqtt_robot import mqtt_subscribe

sensor_VL53L1X = mqtt_subscribe.MQTTSubscribe(client="sensor_distance_1", channel_name="VL53L1X")
sensor_bno055 = mqtt_subscribe.MQTTSubscribe(client="sensor_imu_1", channel_name="bno055")
time.sleep(20)
