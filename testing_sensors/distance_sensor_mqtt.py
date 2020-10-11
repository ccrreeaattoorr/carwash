
import time
import logging
import paho.mqtt.client as mqtt


logging.basicConfig(level=logging.INFO)
logging.info('vpython setup')


def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    logging.info("Distance mm: {}".format(msg))


client = mqtt.Client("P1")
client.connect("localhost")
client.subscribe("VL53L1X")
client.on_message = on_message
client.loop_start()
time.sleep(30)
