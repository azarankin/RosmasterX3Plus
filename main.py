from conf import Rosmaster, pygame, sleep, clamp
from move_motor import MoveMotors
import time


#TODO: set the CH3341SER first
#TODO: check which usb device is available as Rosmater

CONTROLLER_ID = 0 # /dev/input/js*
EXTENSION_BOARD_ADDRESS = "/dev/ttyUSB1" # /dev/ttyUSB*


class MoveArm():
    def __init__(self, bot:Rosmaster):
        assert isinstance(bot, Rosmaster), "Please set bot as instances of Rosmaster."

        # Start servo position
        self.set_servo_global_limits(min=0, max=180, begin=90, clamp_close_min=30,)
        
        self.SERVO_ROTATION_STEP = 15

        self.arm_open_value = 0 #close
        self.ARM_OPEN_VALUE_STEP = 1
        self.MIN_OPEN_VALUE = 0
        self.MAX_OPEN_VALUE = 10

        self.bot = bot
        self.set_arm_clamp_openning(value=None, is_applied=False)
        self.reset_servo() #after set set_servo_global_limits
        

    def set_servo_global_limits(self, min, max, begin, clamp_close_min):
        self.MIN_SERVO_VALUE = min
        self.MIN_SERVO_CLAMP_OPEN_VALUE = clamp_close_min
        self.MAX_SERVO_VALUE = max
        self.SERVO_BEGIN = begin
        self.SERVO_CLIP_CLOSE_BEGIN = max

    def reset_servo(self):
        self.set_arm_servo(self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_BEGIN, self.SERVO_CLIP_CLOSE_BEGIN)


    def set_arm_servo(self, base_rotation=None, arm_bottom=None, arm_middle=None, arm_top=None, camip_rotation=None, clamp_close=None):
        value_clamp = lambda value, min_servo_value=self.MIN_SERVO_VALUE, max_servo_value=self.MAX_SERVO_VALUE: clamp(value, min_servo_value, max_servo_value)
        
        if base_rotation:
            self.base_rotation = value_clamp(base_rotation)
        if arm_bottom:
            self.arm_bottom = value_clamp(arm_bottom)
        if arm_middle:
            self.arm_middle = value_clamp(arm_middle)
        if arm_top:
            self.arm_top = value_clamp(arm_top)
        if camip_rotation:
            self.clamp_rotation = value_clamp(camip_rotation)
        if clamp_close:
            self.clamp_close = value_clamp(clamp_close, self.MIN_SERVO_CLAMP_OPEN_VALUE)

        angle_s = [self.base_rotation, self.arm_bottom, self.arm_middle, self.arm_top, self.clamp_rotation, self.clamp_close]
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
            open_step = self.MAX_SERVO_VALUE / self.MAX_OPEN_VALUE
            self.clamp_close = self.MAX_SERVO_VALUE - open_step * value
            
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


    def calibrate():
        pass

    def __del__(self):
        self.reset_servo() #after init set_servo_global_limits


# Check and run the extension board
bot = Rosmaster(com=EXTENSION_BOARD_ADDRESS)
bot.create_receive_threading()

move_arm = MoveArm(bot)
sleep()
move_arm.arm_step_open()
sleep()
move_arm.arm_step_open()
sleep()
move_arm.arm_step_open()
sleep()
move_arm.arm_step_open()
sleep()
move_arm.arm_step_open()
sleep()

move_arm.arm_step_close()
sleep()
move_arm.arm_step_close()
sleep()
move_arm.arm_step_close()
sleep()
move_arm.arm_step_close()
sleep()

move_arm.set_arm_servo(50)
sleep()
move_arm.arm_rotate0()
sleep()
move_arm.arm_rotate1()



move_motor = MoveMotors(bot)
# sleep()
# move_motor.move_forward(is_move=True)
# sleep()
# move_motor.move_backward(is_move=True)
# sleep()
# move_motor.move_turn0(is_move=True)
# sleep()
# move_motor.move_turn1(is_move=True)
# sleep()
# move_motor.move_side0(is_move=True)
# sleep()
# move_motor.move_side1(is_move=True)


"""
# Initialize pygame and the joystick
pygame.init()
pygame.joystick.init()


# Check for available joysticks
assert pygame.joystick.get_count() == 0, "No joystick found."



joystick = pygame.joystick.Joystick(CONTROLLER_ID)
joystick.init()
print(f"Joystick detected: {joystick.get_name()}")

print("Listening for joystick inputs... Press Ctrl+C to stop.")
try:
    while True:
        # Process events
        pygame.event.pump()
        
        # Check for button and axis events
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis} moved to {event.value}")
        
        # Check for D-pad (hat) movement
        num_hats = joystick.get_numhats()  # Get number of hats (D-pads)
        for i in range(num_hats):
            hat_value = joystick.get_hat(i)  # Get the position of the D-pad
            if hat_value != (0, 0):  # Only print if the D-pad is pressed in a direction
                print(f"D-pad {i} moved to {hat_value}")

        time.sleep(0.1)  # Short delay to reduce CPU usage
except KeyboardInterrupt:
    print("Stopped listening for joystick inputs.")
finally:
    pygame.joystick.quit()
    pygame.quit()
"""


sleep()

# close the arm action
del move_arm

# close the motor action
del move_motor

# After the program is complete, delete the object to avoid conflicts caused by using the library in other programs
del bot