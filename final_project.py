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
num_injar = 3
num_outjar = 5

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
o o . . . . . . o o

"""
# TODO: Terniary statment here
def is_boundary(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((col == x_pad) or (col == (x_pad + x_jar + 1))) or ((row == y_pad) or (row == (y_pad + y_jar + 1)))) else False

def is_oob(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((row < 0) or (row > (1 + y_pad + y_jar))) or ((col < 0) or (col > (1 + 2*x_pad + x_jar))))  else False

fireflies = []
lum_grid = []

class Firefly():
    def __init__(self,flag):
        global fireflies, x_pad, y_pad, x_jar, y_jar

        # if inside jar, flag = 0
        # if outside jar, flag = 1
        self.base_lum = np.random.uniform(1,10)
        if (flag == 0):
            self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar))
            self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1))
        else: # TODO: figure out outside of jar spawing locations
            xpos = 0
            ypos = 0
            while True: 
                xpos = int(np.random.uniform(0,2*x_pad+x_jar+2))
                ypos = int(np.random.uniform(0,2+y_pad+y_jar))
                if not (x_pad <= xpos and xpos <= x_pad+1+x_jar): 
                    if ypos < y_pad:
                        break
            self.row = xpos 
            self.col = ypos 
        fireflies.append(self)
    
    def move(self,lum_grid):
        moves = dict()
        if self.row > 0:
            if not self.is_boundary(self.row-1, self.col): 
                if not self.checkFirefly(self.row-1, self.col):
                    moves["up"] = lum_grid[self.row-1][self.col]
        if self.col > 0:
            if not self.is_boundary(self.row, self.col-1): 
                if not self.checkFirefly(self.row, self.col-1):
                    moves["left"] = lum_grid[self.row][self.col-1]
        if self.row < 1+x_jar+2*x_pad:
            if not self.is_boundary(self.row+1, self.col): 
                if not self.checkFirefly(self.row+1, self.col):
                    moves["down"] = lum_grid[self.row+1][self.col]
        if self.col < 1+y_jar+y_pad:
            if not self.is_boundary(self.row, self.col+1): 
                if not self.checkFirefly(self.row, self.col+1):
                    moves["right"] = lum_grid[self.row][self.col+1]
        
        if len(moves) == 0: 
            #do nothing 
            return 
        if len(moves) == 1: 
            
        themove = ""
        if : 
            self.row = self.row-1 
        elif "left" in moves: 
            self.col = self.col-1 
        elif "down" in moves: 
            self.row = self.row+1
        else: 
            self.col = self.col+1 
        return 
         

    def checkFirefly(self, rowNum, colNum): 
        #return a boolean indicating whether there is a firefly on rowNum, colNum 
        for x in fireflies: 
            if x.row == rowNum and x.col == colNum: 
                return True 
        return False    

    def die(self):
        fireflies.remove(self) # TODO: test die function

def dist(pos1,pos2):
    return ((pos1[0] - pos2[0])^2 + (pos1[1] - pos2[1])^2)^0.5

# TODO compute luminousity from all fireflies.
def compute_luminousity(grid):
    global fireflies
    for fly in fireflies:
        for row,col in grid:
            grid[row,col] += (fly.base_lum * 1 / ( max( dist((row,col),(fly.row,fly.col)) ,0.5) ^ 2 ) )
            # Note that base_lum will be doubled at the location of where the firefly is
    return grid
        
def initialize():
    global x_pad, y_pad, x_jar, y_jar, fireflies
    lum_grid = np.zeros((2 + y_pad + y_jar,2 + 2*x_pad + x_jar))
    for i in range(num_injar): 
        Firefly(0)
    for i in range(num_outjar): 
        Firefly(1)

def update():
    global fireflies, lum_grid
    for fly in fireflies:
        fly.move(lum_grid)
    