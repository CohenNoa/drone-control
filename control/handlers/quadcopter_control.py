from .attitude_handler import AttitudeHandler as Attitude

# order = [pitch, yaw, roll. throttle]

class Drone(object):
    def __init__(self):
        self.attitude = Attitude(12, 16, 20, 21)
        self.enable_controls = True;
    
    def run_command(self, command):
        args = command.split("_")
        if args[0] == "attitude" and self.enable_controls:
            if args[1] in ["pitch", "roll", "yaw", "throttle"] and float(args[2]) <= 100 and float(args[2]) >= 0:
                self.attitude.change_channel_duty_cycle(args[1], int(float(args[2])))
            
            #args[2] = args[2].split(",")
            #data = [float(args[2][0]), float(args[2][1])]
            #if args[1] == "left":
            #    # yaw, throttle
            #    print("Left")
            #    print(data)
            #    #self.attitude.change_left_duty_cycle(data)
            #if args[1] == "right":
            #    # roll, pitch
            #    print("Right")
            #    print(data)
            #    #self.attitude.change_right_duty_cycle(data)
        
        
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
