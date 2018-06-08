from .attitude_handler import AttitudeHandler as Attitude


# order = [pitch, yaw, roll. throttle]

class Drone(object):
    def __init__(self):
        self.attitude = Attitude(7, 1, 12, 16, 20, 21)
        self.enable_controls = True

    def run_command(self, command):
        args = command.split("_")
        if args[0] == "attitude" and self.enable_controls:
            if args[1] in ["pitch", "roll", "yaw", "throttle"] and 100 >= float(args[2]) >= 0:
                self.attitude.change_channel_duty_cycle(args[1], int(float(args[2])))
        if args[0] == "mode":
            if args[1] in ["0","1","2","3","4"]:
                self.attitude.change_mode(int(args[1]))
        if args[0] == "return-home":
            if args[1] in ["0", "1"]:
                self.attitude.change_return_home(True if args[1] is "1" else False)

    def arm(self):
        print("Arm")
        self.enable_controls = False
        self.attitude.arm()
        self.enable_controls = True

    def disarm(self):
        print("Disarm")
        self.enable_controls = False
        self.attitude.disarm()
        self.enable_controls = True
