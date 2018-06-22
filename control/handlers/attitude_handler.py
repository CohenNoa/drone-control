import time

debug_mode = False
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ImportError):
    debug_mode = True
    print("GPIO module can only be run on a Raspberry Pi!\n\n")

timeout = 3  # seconds
frequency = 50  # Hz


class AttitudeHandler(object):
    def __init__(self, return_home, mode, pitch, yaw, roll, throttle):
        self.modes_names = {10: "Stabilize",
                            30: "FailSafe 1",
                            50: "Intellegent Orientation Control",
                            70: "FailSafe 2",
                            90: "GPS"}

        self.modes = [10, 30, 50, 70, 90]

        if not debug_mode:
            self.return_home_pin = return_home
            self.mode_pin = mode
            self.pitch_pin = pitch
            self.yaw_pin = yaw
            self.roll_pin = roll
            self.throttle_pin = throttle

            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.return_home_pin, GPIO.OUT)
            GPIO.setup(self.mode_pin, GPIO.OUT)
            GPIO.setup(self.pitch_pin, GPIO.OUT)
            GPIO.setup(self.yaw_pin, GPIO.OUT)
            GPIO.setup(self.roll_pin, GPIO.OUT)
            GPIO.setup(self.throttle_pin, GPIO.OUT)

            self.return_home_pwm = GPIO.PWM(self.return_home_pin, frequency)
            self.mode_pwm = GPIO.PWM(self.mode_pin, frequency)
            self.pitch_pwm = GPIO.PWM(self.pitch_pin, frequency)
            self.yaw_pwm = GPIO.PWM(self.yaw_pin, frequency)
            self.roll_pwm = GPIO.PWM(self.roll_pin, frequency)
            self.throttle_pwm = GPIO.PWM(self.throttle_pin, frequency)

            self.return_home_default = self.get_duty_cycle(0)
            self.mode_default = self.get_duty_cycle(self.modes[0])
            self.min_duty_cycle = self.get_duty_cycle(0)
            self.middle_duty_cycle = self.get_duty_cycle(50)
            self.max_duty_cycle = self.get_duty_cycle(100)

            self.return_home_pwm.start(self.return_home_default)
            self.mode_pwm.start(self.mode_default)
            self.pitch_pwm.start(self.middle_duty_cycle)
            self.yaw_pwm.start(self.middle_duty_cycle)
            self.roll_pwm.start(self.middle_duty_cycle)
            self.throttle_pwm.start(self.min_duty_cycle)

        print("Setup complete")

    @staticmethod
    def get_duty_cycle(percentage):
        return (percentage / 20) + 5

    def default_position(self):
        if not debug_mode:
            self.pitch_pwm.start(self.middle_duty_cycle)
            self.yaw_pwm.start(self.middle_duty_cycle)
            self.roll_pwm.start(self.middle_duty_cycle)
            self.throttle_pwm.start(self.min_duty_cycle)

    def arm(self):
        if not debug_mode:
            self.pitch_pwm.start(self.max_duty_cycle)
            self.yaw_pwm.start(self.max_duty_cycle)
            self.roll_pwm.start(self.min_duty_cycle)
            self.throttle_pwm.start(self.min_duty_cycle)
            time.sleep(timeout)
            self.default_position()

    def disarm(self):
        if not debug_mode:
            self.pitch_pwm.start(self.max_duty_cycle)
            self.yaw_pwm.start(self.min_duty_cycle)
            self.roll_pwm.start(self.max_duty_cycle)
            self.throttle_pwm.start(self.min_duty_cycle)
            time.sleep(timeout)
            self.default_position()

    def change_channel_duty_cycle(self, name, percent):
        print("changing channel with name \"" + name + "\" to " + str(percent) + "%")
        if not debug_mode:
            duty_cycle = self.get_duty_cycle(percent)
            if name == "pitch":
                duty_cycle = self.get_duty_cycle(100 - percent)
                self.pitch_pwm.start(duty_cycle)
            if name == "yaw":
                self.yaw_pwm.start(duty_cycle)
            if name == "roll":
                self.roll_pwm.start(duty_cycle)
            if name == "throttle":
                self.throttle_pwm.start(duty_cycle)

    def change_mode(self, mode):
        duty_cycle = self.get_duty_cycle(self.modes[mode])
        print("changing mode to " + self.modes_names[self.modes[mode]])
        if not debug_mode:
            self.mode_pwm.start(duty_cycle)

    def change_return_home(self, return_home):
        if return_home:
            if not debug_mode:
                self.return_home_pwm.start(self.get_duty_cycle(100))
            print("returning home")
        else:
            if not debug_mode:
                self.return_home_pwm.start(self.get_duty_cycle(0))
            print("business as unusual")
