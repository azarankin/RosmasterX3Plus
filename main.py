from conf import Rosmaster, pygame, sleep, clamp
from move_motor import MoveMotors
from move_arm import MoveArm

import time


#TODO: set the CH3341SER first
#TODO: check which usb device is available as Rosmater
#TODO: check the option to set sleep for extreme movements


CONTROLLER_ID = 0 # /dev/input/js*
EXTENSION_BOARD_ADDRESS = "/dev/ttyUSB1" # /dev/ttyUSB*

# Check and run the extension board
bot = Rosmaster(com=EXTENSION_BOARD_ADDRESS)
bot.create_receive_threading()

move_arm = MoveArm(bot)
move_motor = MoveMotors(bot)

# samples
from samples import samples
samples(move_arm, move_motor)

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



# close the arm action
del move_arm


# close the motor action
del move_motor


# After the program is complete, delete the object to avoid conflicts caused by using the library in other programs
del bot

print("done")