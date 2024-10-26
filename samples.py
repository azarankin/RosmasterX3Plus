from conf import sleep
from move_arm import MoveArm
from move_motor import MoveMotors

def samples(move_arm:MoveMotors, move_motor:MoveArm):
    sleep()
    move_arm.arm_bent_by(-30)
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




    sleep()
    move_motor.move_forward(is_move=True)
    sleep()
    move_motor.move_backward(is_move=True)
    sleep()
    move_motor.move_turn0(is_move=True)
    sleep()
    move_motor.move_turn1(is_move=True)
    sleep()
    move_motor.move_side0(is_move=True)
    sleep()
    move_motor.move_side1(is_move=True)
    sleep()