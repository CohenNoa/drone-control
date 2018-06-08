import time

running_on_computer = False
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ImportError):
    debug_mode = True
    print("GPIO module can only be run on a Raspberry Pi!")

timeout = 3  # seconds
frequency = 50  # Hz


class AttitudeHandler(object):
    def __init__(self, pitch, yaw, roll, throttle):
        if not debug_mode:
            self.pitch_pin = pitch
            self.yaw_pin = yaw
            self.roll_pin = roll
            self.throttle_pin = throttle

            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.pitch_pin, GPIO.OUT)
            GPIO.setup(self.yaw_pin, GPIO.OUT)
            GPIO.setup(self.roll_pin, GPIO.OUT)
            GPIO.setup(self.throttle_pin, GPIO.OUT)

            self.pitch_pwm = GPIO.PWM(self.pitch_pin, frequency)
            self.yaw_pwm = GPIO.PWM(self.yaw_pin, frequency)
            self.roll_pwm = GPIO.PWM(self.roll_pin, frequency)
            self.throttle_pwm = GPIO.PWM(self.throttle_pin, frequency)

            self.min_duty_cycle = self.get_duty_cycle(0)
            self.middle_duty_cycle = self.get_duty_cycle(50)
            self.max_duty_cycle = self.get_duty_cycle(100)

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
            self.pitch_pwm.start(self.min_duty_cycle)
            self.yaw_pwm.start(self.max_duty_cycle)
            self.roll_pwm.start(self.min_duty_cycle)
            self.throttle_pwm.start(self.min_duty_cycle)
            time.sleep(timeout)
            self.default_position()

    def disarm(self):
        if not debug_mode:
            self.pitch_pwm.start(self.min_duty_cycle)
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
                self.pitch_pwm.start(duty_cycle)
            if name == "yaw":
                self.yaw_pwm.start(duty_cycle)
            if name == "roll":
                self.roll_pwm.start(duty_cycle)
            if name == "throttle":
                self.throttle_pwm.start(duty_cycle)
