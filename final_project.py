import numpy as np 
import pycxsimulator
import matplotlib as plt 
from random import random

max_lum = 100
max_x = 10
max_y = 10

class Firefly():
    def __init__(self,location):
        # if inside jar, location = 0
        # if outside jar, location = 1
        base_lum = np.random.uniform(1,10)
        if (location == 0):
            x_pos = int(np.random.uniform(0,max_x))
            y_pos = int(np.random.uniform(0,max_y))
        else:
            return
            # comment
    
    def move(self): 
        return self.x_pos
