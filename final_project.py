# CMPLXSYS 530 Final Project Main File - 
# The University of Michigan - Ann Arbor, April 3rd, 2022
# 
# Joe Rottner (jrottner@umich.edu) and Jason Hu (jashu@umich.edu)

import numpy as np 
import pycxsimulator
import matplotlib as plt 
from random import random

max_lum = 100
x_jar = 10 # size of jar in X dimension
y_jar = 10 # size of jar in Y dimension
x_pad = 5 # size of padding in X dimension on each side of jar
y_pad = 5 # size of padding in Y dimension on each side of jar

""" 
Data structure for grid - Array of Arrays

[0,0   0,1   0,2 ...
 1,0   1,1   1,2 ...
 ...
 N-1,0 ...   ... N-1,N-1]

 the jar will have dimensions (2 + 2*x_pad + x_jar) by (1 + y_pad + y_jar) and will have corners at points (y_pad + y_jar,x_pad), (y_pad + y_jar,1 + x_pad + jar_x), (y_pad,x_pad), (y_pad,1 + x_pad + jar_x)

For example, if x_pad = y_pad = 2, x_jar = 4, and y_jar = 5, the following graph will be made:
(Legend: o = blank space, . = jar coordinate)

o o o o o o o o o o
o o o o o o o o o o
o o . . . . . . o o
o o . o o o o . o o
o o . o o o o . o o
o o . o o o o . o o
o o . o o o o . o o
o o . o o o o . o o

*TODO: having trouble with making outside jar spawning position equiprobable, as we can get y positions from 0 to 

"""
# TODO: Terniary statment here
def check_boundary(x_in,y_in):
    global x_pad, y_pad, x_jar, y_jar
    return (() or ())

fireflies = [] 

class Firefly():
    def __init__(self,location):
        global fireflies, x_pad, y_pad, x_jar, y_jar

        # if inside jar, location = 0
        # if outside jar, location = 1
        self.base_lum = np.random.uniform(1,10)
        if (location == 0):
            self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar))
            self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1))
        else: # TODO: figure out outside of jar spawing locations
            pass
        fireflies.append(self)
    
    def move(self):
        return

def dist(pos1,pos2):
    return ((pos1[0] - pos2[0])^2 + (pos1[1] - pos2[1])^2)^0.5

# TODO compute luminousity from all fireflies.
def compute_luminousity(grid):
    global fireflies
    for fly in fireflies:
        for row,col in grid:
            grid[row,col] += (fly.base_lum * 1 / ( max( dist((row,col),(fly.row,fly.col)) ,1) ^ 2 ) )
    return grid
    


        
def initialize():
    global x_pad, y_pad, x_jar, y_jar
    grid = np.zeros((1 + y_pad + y_jar,2 + 2*x_pad + x_jar))