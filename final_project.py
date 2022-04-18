# CMPLXSYS 530 Final Project Main File - 
# The University of Michigan - Ann Arbor, April 3rd, 2022
# 
# Joe Rottner (jrottner@umich.edu) and Jason Hu (jashu@umich.edu)

import numpy as np 
import pycxsimulator
import matplotlib.pyplot as plt 
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
def is_boundary(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((col == x_pad and row >= y_pad) or (col == (x_pad + x_jar + 1) and row >= y_pad)) or ((row == y_pad and col > x_pad and col < (x_pad + x_jar + 1)) or (row == (y_pad + y_jar + 1) and col > x_pad and col < (x_pad + x_jar + 1)))) else False

def is_oob(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((row < 0) or (row > (1 + y_pad + y_jar))) or ((col < 0) or (col > (1 + 2*x_pad + x_jar))))  else False

fireflies = []
lum_grid = []

class Firefly():
    def __init__(self,flag):
        global fireflies, x_pad, y_pad, x_jar, y_jar, max_lum

        # if inside jar, flag = 0
        # if outside jar, flag = 1
        self.base_lum = np.random.uniform(1,max_lum)
        if (flag == 0):
            self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar))
            self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1))
            while self.checkFirefly(self.row,self.col):
                self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar))
                self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1))
            
        else:
            xpos = 0
            ypos = 0
            while True: 
                xpos = int(np.random.uniform(0,2*x_pad+x_jar+2))
                ypos = int(np.random.uniform(0,2+y_pad+y_jar))
                if not (x_pad <= xpos and xpos <= x_pad+1+x_jar and y_pad <= ypos and ypos <= y_pad+y_jar+1): 
                    if not self.checkFirefly(xpos, ypos):
                        break
            self.row = ypos 
            self.col = xpos 
        fireflies.append(self)
    
    def move(self,lum_grid):
        moves = dict()

        if not is_boundary(self.row-1, self.col): 
            if not self.checkFirefly(self.row-1, self.col):
                if is_oob(self.row-1, self.col): 
                    self.die()
                    return 
                moves["up"] = lum_grid[self.row-1][self.col]
        if not is_boundary(self.row, self.col-1): 
            if not self.checkFirefly(self.row, self.col-1):
                if is_oob(self.row, self.col-1): 
                    self.die()
                    return 
                moves["left"] = lum_grid[self.row][self.col-1]
        if not is_boundary(self.row+1, self.col): 
            if not self.checkFirefly(self.row+1, self.col):
                if is_oob(self.row+1,self.col):
                    self.die()
                    return 
                moves["down"] = lum_grid[self.row+1][self.col]
        if not is_boundary(self.row, self.col+1): 
            if not self.checkFirefly(self.row, self.col+1):
                if is_oob(self.row, self.col+1): 
                    self.die()
                    return 
                moves["right"] = lum_grid[self.row][self.col+1]
        
        if len(moves) == 0: 
            #do nothing 
            return ""
        
        brightest = -1
        themove = ""
        for x in moves: 
            if moves[x] > brightest: 
                brightest = moves[x] 
                themove = x 

        if themove == "up": 
            self.row = self.row-1 
        elif themove == "left": 
            self.col = self.col-1 
        elif themove == "down": 
            self.row = self.row+1
        else: 
            self.col = self.col+1 

        return themove 

        if len(moves) == 1: 
            pass 

        if True: 
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
        fireflies.remove(self) 
        del self # TODO: test die function

def dist(pos1,pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

# TODO compute luminosity from all fireflies.
def compute_luminosity(grid):
    global fireflies
    for fly in fireflies:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                grid[row,col] += (fly.base_lum * 1 / ( max( dist((row,col),(fly.row,fly.col)) ,0.5) ** 2 ) )
            # Note that base_lum will be doubled at the location of where the firefly is
    return grid

def spawn(lum_grid):
    global x_pad, y_pad, max_lum
    end_y = np.shape(lum_grid)[0]
    end_x = np.shape(lum_grid)[1]

    rate = int(np.amax(lum_grid[y_pad + 1:(end_y - 1),x_pad + 1:(end_x - x_pad - 1)]) / max_lum / 5)
    for i in range(rate):
        Firefly(1)
        
def initialize():
    global x_pad, y_pad, x_jar, y_jar, fireflies
    fireflies = []
    for i in range(num_injar): 
        Firefly(0)
    for i in range(num_outjar): 
        Firefly(1)

def update():
    global fireflies
    
    lum_grid = np.zeros((2 + y_pad + y_jar,2 + 2*x_pad + x_jar))
    lum_grid = compute_luminosity(lum_grid)
    for fly in fireflies:
        fly.move(lum_grid)
    spawn(lum_grid)
    
    
def observe():
    global fireflies
    disp_grid = np.zeros((2 + y_pad + y_jar,2 + 2*x_pad + x_jar))
    lum = disp_grid.copy()
    for row in range(len(disp_grid)):
        for col in range(len(disp_grid[0])): 
            if is_boundary(row,col):
                disp_grid[row,col] = 1
    for fly in fireflies:
        disp_grid[fly.row,fly.col] = 2
    lum = compute_luminosity(lum)

    plt.subplot(2,1,1)
    plt.imshow(disp_grid)
    plt.subplot(2,1,2)
    plt.imshow(lum)
    plt.show()
    
#initialize()
#observe()
"""
update()
observe()"""
pycxsimulator.GUI().start(func=[initialize, observe, update])