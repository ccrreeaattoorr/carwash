#!/usr/bin/python
import time
import math
import logging
import threading
import numpy as np
#from vpython import *
import paho.mqtt.client as mqtt
from pyquaternion import Quaternion
#import paho.mqtt.subscribe as subscribe


logging.basicConfig(level=logging.INFO)
logging.info('vpython setup')

# scene.range = 5
# scene.background = color.yellow
# toRad = 2 * np.pi / 360
# toDeg = 1 / toRad
# scene.forward = vector(-1, -1, -1)
#
# scene.width = 1200
# scene.height = 1080
#
# xarrow = arrow(lenght=2, shaftwidth=.1, color=color.red, axis=vector(1, 0, 0))
# yarrow = arrow(lenght=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
# zarrow = arrow(lenght=4, shaftwidth=.1, color=color.blue, axis=vector(0, 0, 1))
#
# frontArrow = arrow(length=4, shaftwidth=.1, color=color.purple, axis=vector(1, 0, 0))
# upArrow = arrow(length=1, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))
# sideArrow = arrow(length=2, shaftwidth=.1, color=color.orange, axis=vector(0, 0, 1))
#
# bBoard = box(length=6, width=2, height=.2, opacity=.8, pos=vector(0, 0, 0, ))
# bn = box(length=1, width=.75, height=.1,  pos=vector(-.5, .1 + .05, 0), color=color.blue)
# nano = box(lenght=1.75, width=.6, height=.1, pos=vector(-2, .1 + .05, 0), color=color.green)
# myObj = compound([bBoard, bn, nano])


# def print_msg(client, userdata, message):
#     # print("%s : %s" % (message.topic, message.payload))
#     message_bno055.append(message.payload)

def on_message(client, userdata, message):
    # print("message received " ,str(message.payload.decode("utf-8")))
    msg = message.payload.decode("utf-8")
    split_packet = msg.split(";")
    logging.info("parsed data: {}".format(str(split_packet)))
    w = float(split_packet[0])
    x = float(split_packet[1])
    y = float(split_packet[2])
    z = float(split_packet[3])

    

    # roll = -math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))
    # pitch = math.asin(2 * (q0 * q2 - q3 * q1))
    # yaw = -math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)) - np.pi / 2

    # rate(50)
    # k = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
    # y = vector(0, 1, 0)
    # s = cross(k, y)
    # v = cross(s, k)
    # vrot = v * cos(roll) + cross(k, v) * sin(roll)
    #
    # frontArrow.axis = k
    # sideArrow.axis = cross(k, vrot)
    # upArrow.axis = vrot
    # myObj.axis = k
    # myObj.up = vrot
    # sideArrow.length = 2
    # frontArrow.length = 4
    # upArrow.length = 1


logging.info('before callback')
client = mqtt.Client("P1")
client.connect("localhost")
client.subscribe("bno055")
client.on_message = on_message
client.loop_start()
time.sleep(30)
logging.info('after callback')
