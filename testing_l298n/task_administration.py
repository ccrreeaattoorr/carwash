import time
import argparse


class TaskAdministration:

    def __init__(self, controllers, instructions):
        self.controllers = controllers
        self.instructions = instructions
        pass

    def execute_tasks(self):
        for instruction in self.instructions:
            for controller in self.instructions[instruction]:
                c = self.instructions[instruction][controller]
                self.controllers[controller].non_blocking_move_stepper(c["steps"], c["direction"], c["speed"])
            task_finished = False
            while not task_finished:
                time.sleep(0.5)
                for controller in self.controllers:
                    if self.controllers[controller].is_moving_now:
                        task_finished = False
                        break
                    task_finished = True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Controller administration Args')
    parser.add_argument('--mock', type=bool, default=False, help='Mock controller')
    parser.add_argument('--steps', type=int, default=50, help='Number of steps')
    parser.add_argument('--direction', type=str, default='forward', help='direction (forward or backward')
    parser.add_argument('--speed', type=str, default='MAX_SPEED', help='stepper speed (MAX_SPEED or MIN_SPEED')
    args = parser.parse_args()

    if args.mock:
        from controller_mock import Controller
    else:
        from controller_L298N import Controller

    c1 = Controller(13, 19, 12, 16, 20, 21)
    c2 = Controller(17, 27, 18, 23, 24, 25)

    c1.non_blocking_move_stepper(steps=args.steps, direction=args.direction, speed=args.speed)
    c2.non_blocking_move_stepper(steps=args.steps, direction=args.direction, speed=args.speed)
