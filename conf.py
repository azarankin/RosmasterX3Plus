from Rosmaster_Lib import Rosmaster
import pygame
import time



settings = {
    "controller_id": 0,
    "extension_board_address": "/dev/ttyUSB0"
}

def clamp(value, min_value, max_value):
    return min_value if value <= min_value else max_value if value >= max_value else value
    

def sleep(min=2): # Wait
    time.sleep(min)