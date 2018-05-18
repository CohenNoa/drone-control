import RPi.GPIO as GPIO
import time

timeout = 3 #seconds
frequency = 50 #Hz
        
        
class AttitudeHandler(object):
    def __init__(self, pitch, yaw, roll, throttle):
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
        
    def get_duty_cycle(self, percentage):
        return (percentage / 20 ) + 5
    
    def default_position(self):
        self.pitch_pwm.start(self.middle_duty_cycle)
        self.yaw_pwm.start(self.middle_duty_cycle)
        self.roll_pwm.start(self.middle_duty_cycle)
        self.throttle_pwm.start(self.min_duty_cycle)
    
    def arm(self):
        self.pitch_pwm.start(self.min_duty_cycle)
        self.yaw_pwm.start(self.max_duty_cycle)
        self.roll_pwm.start(self.min_duty_cycle)
        self.throttle_pwm.start(self.min_duty_cycle)
        time.sleep(timeout)
        self.default_position()
        
            
    def disarm(self):
        self.pitch_pwm.start(self.min_duty_cycle)
        self.yaw_pwm.start(self.min_duty_cycle)
        self.roll_pwm.start(self.max_duty_cycle)
        self.throttle_pwm.start(self.min_duty_cycle)
        time.sleep(timeout)
        self.default_position()
        
    def change_channel_duty_cycle(self, name, percent):
        print("changing channel with name \"" + name + "\" to " + str(percent) + "%")
        duty_cycle = self.get_duty_cycle(percent)
        if name=="pitch":
            self.pitch_pwm.start(duty_cycle)
        if name=="yaw":
            self.yaw_pwm.start(duty_cycle)
        if name=="roll":
            self.roll_pwm.start(duty_cycle)
        if name=="throttle":
            self.throttle_pwm.start(duty_cycle)
            
    def change_left_duty_cycle(self, duty_cycle_data):
        # duty cycle data order = [yaw, throttle]
        if duty_cycle_data[0] != -1.0:
            yaw_duty_cycle = self.get_duty_cycle(duty_cycle_data[0])
            print("Changing duty yaw duty cycle to " + str(yaw_duty_cycle))
            GPIO.output(self.yaw_pin, yaw_duty_cycle)
            self.yaw_pwm.start(yaw_duty_cycle)
        if duty_cycle_data[1] != -1.0:
            throttle_duty_cycle = self.get_duty_cycle(duty_cycle_data[1])
            print("Changing duty throttle duty cycle to " + str(throttle_duty_cycle))
            GPIO.output(self.throttle_pin, throttle_duty_cycle)
            self.throttle_pwm.start(throttle_duty_cycle)
    
    def change_right_duty_cycle(self, duty_cycle_data):
        # duty cycle data order = [roll, pitch]
        if duty_cycle_data[0] != -1.0:
            roll_duty_cycle = self.get_duty_cycle(duty_cycle_data[0])
            print("Changing duty roll duty cycle to " + str(roll_duty_cycle))
            GPIO.output(self.roll_pin, roll_duty_cycle)
            self.roll_pwm.start(roll_duty_cycle)
        if duty_cycle_data[1] != -1.0:
            pitch_duty_cycle = self.get_duty_cycle(duty_cycle_data[1])
            print("Changing duty pitch duty cycle to " + str(pitch_duty_cycle))
            GPIO.output(self.pitch_pin, pitch_duty_cycle)
            self.pitch_pwm.start(pitch_duty_cycle)

        
        
