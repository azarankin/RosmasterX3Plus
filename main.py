from conf import Rosmaster, sleep
from move_motor import MoveMotors
from move_arm import MoveArm
from gamepad import Gamepad
import time

#TODO: set the CH3341SER first
#TODO: check which usb device is available as Rosmater
#TODO: check the option to set sleep for extreme movements


CONTROLLER_ID = 0 # /dev/input/js*
EXTENSION_BOARD_ADDRESS = "/dev/ttyUSB1" # /dev/ttyUSB*

# Check and run the extension board
bot = Rosmaster(com=EXTENSION_BOARD_ADDRESS)
#bot.create_receive_threading()

move_arm = MoveArm(bot)
move_motor = MoveMotors(bot)

# samples
from samples import samples
samples(move_arm, move_motor)





gamepad = Gamepad(CONTROLLER_ID)



print("Listening for joystick inputs... Press Ctrl+C to stop.")
try:
    while True:
        actions = gamepad.loop()
        for act in actions:
            action = act["action"]
            mode = act["mode"]
            value = act["value"]

            if action is "button":
                if value is 0: # A
                    move_arm.arm_full_open() if mode is 1 else move_arm.arm_full_close()
                elif value is 3: # X
                    move_motor.gas() if mode is 1 else move_motor.stop()
                elif value is 4: # Y
                        move_arm.set_arm_bent(0)

                print(action ," ", value, "is ",  mode)

            elif action is "axis":
                if value is 1 and mode < 0: #up
                    a= 50 - mode * 100
                    move_arm.set_arm_bent(a)
                    print(a)
                elif value is 1 and mode > 0:
                    a= 50 + mode * 100
                    move_arm.set_arm_bent( a )
                    print(a)
                else:
                    move_arm.set_arm_bent(0)
                    #move_arm.
                print(action ," ", value, "is ",  mode)


            elif action is "dpad":
                if mode is "neutral":
                    move_motor.stop()
                elif mode is "up":
                    move_motor.move_forward()
                elif mode is "down":
                    move_motor.move_backward()
                elif mode is "right":
                    move_motor.move_side0()
                elif mode is "left":
                    move_motor.move_side1()
                elif mode is "up-left" or mode is "down-left": #TODO:
                    move_motor.move_turn0()
                elif mode is "up-right" or mode is "down-right": #TODO:
                    move_motor.move_turn1()

                else:

                    print(action ," ", value, "is ",  mode)


except KeyboardInterrupt or Exception:
    print("Stopped listening for joystick inputs.")

finally:
    #close gamepad
    if 'gamepad' in locals():
        gamepad.close()
    # close the arm action
    if 'move_arm' in locals():
        move_arm.close()
    # close the motor action
    if 'move_motor' in locals():
        move_motor.close()

del gamepad
del move_arm
del move_motor


# After the program is complete, delete the object to avoid conflicts caused by using the library in other programs
del bot

print("done")