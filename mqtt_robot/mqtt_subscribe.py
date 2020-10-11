import logging
import paho.mqtt.client as mqtt


class MQTTSubscribe:

    def __init__(self, client, channel_name):
        logging.basicConfig(level=logging.INFO)
        self.channel_name = channel_name
        client = mqtt.Client(client)
        client.connect("localhost")
        client.subscribe(channel_name)
        client.on_message = self.on_message
        client.loop_start()
        logging.info("Subscribed for mqtt channel {}".format(self.channel_name))

    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        logging.info(" vv ".format(self.channel_name, msg))
