from conf import Rosmaster, clamp, sleep

class MoveArm():
    def __init__(self, bot:Rosmaster):
        assert isinstance(bot, Rosmaster), "Please set bot as instances of Rosmaster."

        self.MIN_SERVO_VALUE = 0
        self.MIN_SERVO_CLAMP_OPEN_VALUE = 30
        self.MAX_SERVO_VALUE = 180
        self.SERVO_BEGIN = 90
        self.SERVO_CLAMP_CLOSE_BEGIN = self.MAX_SERVO_VALUE 

        #self.arm_bent_value = 0
        self.ARM_BENT_MIN_VALUE = 0
        self.ARM_BENT_MAX_VALUE = 100
        self.ARM_BENT_MOTORS = 3
        self.ARM_BENT_VALUE = self.MAX_SERVO_VALUE / self.ARM_BENT_MAX_VALUE

        self.SERVO_ROTATION_STEP = 15

        self.arm_open_value = 0 #close
        self.ARM_OPEN_VALUE_STEP = 1
        self.MIN_OPEN_VALUE = 0
        self.MAX_OPEN_VALUE = 10
        self.OPEN_VALUE_STEP = self.MAX_SERVO_VALUE / self.MAX_OPEN_VALUE

        self.bot = bot
        self.set_arm_clamp_openning(value=None, is_applied=False)
        self.reset_servo() #after set set_servo_global_limits
        

    def reset_servo(self):
        self.set_arm_servo(self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_CLAMP_CLOSE_BEGIN)
    
    def value_clamp(self, value, min_servo_value=None, max_servo_value=None):
        if not min_servo_value:
            min_servo_value=self.MIN_SERVO_VALUE
        if not max_servo_value:
            max_servo_value=self.MAX_SERVO_VALUE
        return clamp(int(value), min_servo_value, max_servo_value)


    def set_base_rotation(self, base_rotation, min_value=None, max_value=None):
        if base_rotation:
            self.base_rotation = self.value_clamp(base_rotation, min_value, max_value)

    def set_arm_position(self, arm_bottom, arm_middle, arm_top, min_value=None, max_value=None):
        if arm_bottom:
            self.arm_bottom = self.value_clamp(arm_bottom, min_value, max_value)
        if arm_middle:
                    self.arm_middle = self.value_clamp(arm_middle)
        if arm_top:
            self.arm_top = self.value_clamp(arm_top, min_value, max_value)

        self.arm_position = self.arm_top + self.arm_middle + self.arm_bottom

    def set_clamp_rotation(self, clamp_rotation, min_value=None, max_value=None):
        if clamp_rotation:
            self.clamp_rotation = self.value_clamp(clamp_rotation, min_value, max_value)

    def set_clamp_close(self, clamp_rotation, min_value=None, max_value=None):
        if clamp_rotation:
            self.clamp_rotation = self.value_clamp(clamp_rotation, min_value, max_value)


    def set_arm_servo(self, base_rotation=None, arm_bottom=None, arm_middle=None, arm_top=None, clamp_rotation=None, clamp_close=None):
        self.set_base_rotation(base_rotation) 
        self.set_arm_position(arm_bottom, arm_middle, arm_top)
        self.set_clamp_rotation(clamp_rotation)
        self.set_clamp_close(clamp_close, self.MIN_SERVO_CLAMP_OPEN_VALUE)
        angle_s = [self.base_rotation, self.arm_bottom, self.arm_middle, self.arm_top, self.clamp_rotation, self.clamp_close]
        print(angle_s)
        self.bot.set_uart_servo_angle_array(angle_s)

    def get_arm_servo_total(self):
        return self.base_rotation, self.arm_bottom, self.arm_top, self.clamp_rotation, self.clamp_close


    def set_arm_rotate(self, value=None):
        self.base_rotation += value
        self.set_arm_servo()

    def set_arm_clamp_openning(self, value=None, is_applied=True):
        if value is None:
            value = self.arm_open_value
        else:
            self.arm_open_value = value

        if value<=self.MIN_OPEN_VALUE: #close the arm
            self.clamp_close = self.MAX_SERVO_VALUE 
        elif value>=self.MAX_OPEN_VALUE: #open the arm
            self.clamp_close = self.MIN_SERVO_CLAMP_OPEN_VALUE 
        else:
            self.clamp_close = self.MAX_SERVO_VALUE - self.OPEN_VALUE_STEP * value

        if is_applied is True:
            self.set_arm_servo()


    def get_clamp_close(self):
        return self.clamp_close 
 
    def get_clamp_opening(self):
        return self.MAX_SERVO_VALUE - self.clamp_close 
 
    def arm_rotate0(self):
        self.set_arm_rotate(-self.SERVO_ROTATION_STEP)

    def arm_rotate1(self):
        self.set_arm_rotate(self.SERVO_ROTATION_STEP)

    def arm_full_close(self):
        self.set_arm_clamp_openning(value=0)

    def arm_full_open(self, value=None):
        if not value:
            value = self.MAX_OPEN_VALUE
        self.set_arm_clamp_openning(value)

    def arm_step_close(self):
        if self.arm_open_value > self.MIN_OPEN_VALUE:
            self.arm_open_value -= self.ARM_OPEN_VALUE_STEP
            self.set_arm_clamp_openning()

    def arm_step_open(self):
        if self.arm_open_value < self.MAX_OPEN_VALUE:
            self.arm_open_value += self.ARM_OPEN_VALUE_STEP
            self.set_arm_clamp_openning()

    def set_arm_bent(self, value):
        value_per_motor = value / self.ARM_BENT_MOTORS
        self.set_arm_position(value_per_motor, value_per_motor, value_per_motor)
        self.set_arm_servo()

    #def arm_value(self, value)
        



    def set_arm_bent_by(self, value):
        value_per_motor = value / self.ARM_BENT_MOTORS
        self.set_arm_position(self.arm_bottom + value_per_motor, self.arm_middle + value_per_motor, self.arm_top + value_per_motor)
        self.set_arm_servo()

    def arm_bent_down(self):
        self.set_arm_bent_by(self.ARM_BENT_VALUE)

    def arm_bent_up(self):
        self.set_arm_bent_by(-self.ARM_BENT_VALUE)

    def arm_bent_by(self, times):
        self.set_arm_bent(self.arm_position + self.ARM_BENT_VALUE * times)

    def arm_bent_down_by(self, times):
        self.arm_bent_by(times)

    def arm_bent_up_by(self, times):
        self.arm_bent_by(-times)


    def calibrate():
        pass

    def close(self):
        sleep()
        self.reset_servo() #after init set_servo_global_limits

    def __del__(self):
        self.close()
