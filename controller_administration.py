import argparse


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
        from controller import Controller

    c1 = Controller(13, 19, 12, 16, 20, 21)
    c2 = Controller(17, 27, 18, 23, 24, 25)

    c1.move_stepper(steps=args.steps, direction=args.direction, speed=args.speed)
    c2.move_stepper(steps=args.steps, direction=args.direction, speed=args.speed)
