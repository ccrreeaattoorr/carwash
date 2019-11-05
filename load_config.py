import sys
import json
import logging
import argparse
from controller_mock import Controller
from urllib3.connectionpool import xrange
from task_administration import TaskAdministration


class LoadConfig:

    def __init__(self, config):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.controllers = dict()
        self.instructions = dict()

        with open(config) as config_file:
            config = json.load(config_file)
        self.frames = config["Frames"]
        for frame_number in xrange(1, len(config["Frames"])+1):
            logging.info("Frame number: {} - Init started".format(frame_number))
            logging.info("Node id: {}".format(config["Frames"]["frame{}".format(frame_number)]["id"]))
            self.init_controllers(frame_number)
            self.init_instructions(frame_number)
            logging.info("Frame number: {} - Init finished".format(frame_number))

    def init_controllers(self, frame_number):
        logging.info("Init controllers")
        for controller_name in self.frames["frame{}".format(frame_number)]["controllers"]:
            logging.info("Controller name: {}".format(controller_name))
            controller_init_config = self.frames["frame{}".format(frame_number)]["controllers"][controller_name]
            c = Controller(controller_init_config["ena"], controller_init_config["enb"],
                           controller_init_config["a1"], controller_init_config["a2"], controller_init_config["b1"],
                           controller_init_config["b2"], name=controller_name)
            self.controllers[controller_name] = c

    def init_instructions(self, frame_number):
        for instruction in self.frames["frame{}".format(frame_number)]["instructions"]:
            logging.info("Init instructions, Instruction name: {}".format(instruction))
            controller_names = self.frames["frame{}".format(frame_number)]["instructions"][instruction]
            self.instructions[instruction] = dict()
            for controller in controller_names:
                logging.info("Controller: {}".format(controller))
                self.instructions[instruction][controller] = dict()
                self.instructions[instruction][controller]["steps"] = controller_names[controller]["steps"]
                self.instructions[instruction][controller]["direction"] = controller_names[controller]["direction"]
                self.instructions[instruction][controller]["speed"] = controller_names[controller]["speed"]

                logging.info("Direction: {} Steps: {} Speed: {}".format(controller_names[controller]["steps"],
                                                                        controller_names[controller]["direction"],
                                                                        controller_names[controller]["speed"]))

    def execute_config(self):
        ta = TaskAdministration(self.controllers, self.instructions)
        ta.execute_tasks()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Controller administration Args')
    parser.add_argument('--json_config', required=True, type=str, help='JSON configuration file for washer machine')
    parser.add_argument('--mock', type=bool, default=False, help='Mock controller')
    args = parser.parse_args()
    lc = LoadConfig(args.json_config)
    lc.execute_config()
