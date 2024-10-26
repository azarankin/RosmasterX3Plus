from Rosmaster_Lib import Rosmaster
import pygame
import time



def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))
    

def sleep(min=2): # Wait
    time.sleep(min)