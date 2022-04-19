# CMPLXSYS 530 Final Project Main File -
# The University of Michigan - Ann Arbor, April 3rd, 2022
#
# Joe Rottner (jrottner@umich.edu) and Jason Hu (jashu@umich.edu)

import numpy as np
import numpy.matlib as npm
import pycxsimulator
import matplotlib.pyplot as plt
from random import random
import random
import math
from pyDOE import lhs

max_lum = 100
x_jar = 10 # size of jar in X dimension
y_jar = 10 # size of jar in Y dimension
x_pad = 5 # size of padding in X dimension on each side of jar
y_pad = 5 # size of padding in Y dimension on each side of jar
num_injar = 3 #number of fireflies starting inside the jar
num_outjar = 5 #number of fireflies starting outside the jar
randomness = 0.5 # how randomly the fireflies move according to luminosity

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

# Description: checks if a certain position is on the boundary of the jar.
# Input: row and column integers representing position
# Output: Boolean value - returns True if on the boundary of the jar, False otherwise. 
def is_boundary(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((col == x_pad and row >= y_pad) or (col == (x_pad + x_jar + 1) and row >= y_pad)) or ((row == y_pad and col > x_pad and col < (x_pad + x_jar + 1)) or (row == (y_pad + y_jar + 1) and col > x_pad and col < (x_pad + x_jar + 1)))) else False

# Decription: checks if a certain position is out of the boundary of the stage (a.k.a. valid locations being observed)
# Input: row and column integers representing position
# Output: Boolean value - returns True if position is out of the defined array bounds, returns False otherwise
def is_oob(row,col):
    global x_pad, y_pad, x_jar, y_jar
    return True if (((row < 0) or (row > (1 + y_pad + y_jar))) or ((col < 0) or (col > (1 + 2*x_pad + x_jar))))  else False

fireflies = [] # Array of Fireflies (class) to pass through functions
lum_grid = [] # Array representing the luminosity at specific stage positions

class Firefly():
    
    # Description: initializes a Firefly variable in the simulation
    # Input: integer flag of value 0 or 1. 0 represents a firefly spawning inside the jar, and 1 represents a firefly spawning out of the jar
    # Output: Firefly variable added to "fireflies" array
    # Member Variables:
    # # loc - location, has value of 0 or 1 corresponding to whether it is inside or outside the jar
    # # row - row position of firefly
    # # col - column position of firefly
    # # base_lum - base luminosity of firefly, chosen randomly between 0 and max_lum variable defined above
    
    def __init__(self,flag):
        global fireflies, x_pad, y_pad, x_jar, y_jar, max_lum

        # if inside jar, flag = 0
        # if outside jar, flag = 1
        self.base_lum = np.random.uniform(1,max_lum) # Selects base_lum uniformly distributed from 0 and max_lum
        if (flag == 0): # if inside the jar...
            self.loc = 0 # boolean set to inside the jar
            self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar)) # select row position uniformly distributed between edges of jar, int function rounds down float returned from random draw 
            self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1)) # select column position uniformly distributed between edges of jar, int function rounds down float returned from random draw
            
            while self.checkFirefly(self.row,self.col):
                self.row = int(np.random.uniform(y_pad + 1,1 + y_pad + y_jar))
                self.col = int(np.random.uniform(x_pad + 1,x_pad + x_jar + 1))

        else:
            self.loc = 1
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
    
    # Determines what direction for the firefly to move 
    # Input: luminosity grid from compute_luminosity
    # Output: String for the move: either left, up, down, or right
    def move(self,lum_grid):
        global randomness
        moves = dict()
        
        # For each of the four possible directions it can move, check if there is a jar boundary or firefly there
        # If not, but the space is out of bounds, delete the firefly 
        # If the space is valid, add the move to the dictionary key, value is the luminosity of the new space
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
        
        # Set the move to the direction which leads to the greatest luminosity 
        brightest = -1
        themove = ""
        for x in moves:
            if moves[x] > brightest:
                brightest = moves[x]
                themove = x

        # With some chance, the firefly chooses to move in any of the random legal directions
        if np.random.uniform() < randomness:
            themove = random.choice(list(moves.keys()))

        if themove == "up":
            self.row = self.row-1
        elif themove == "left":
            self.col = self.col-1
        elif themove == "down":
            self.row = self.row+1
        else:
            self.col = self.col+1

        return themove

    # Determine whether there is a firefly at a current location
    # Input: rowNum and colNum representing the row and column that needs to be checked
    # Output: Boolean True if there is a firefly on that row and col, False otherwise
    def checkFirefly(self, rowNum, colNum):
        #return a boolean indicating whether there is a firefly on rowNum, colNum
        for x in fireflies:
            if x.row == rowNum and x.col == colNum:
                return True
        return False

    def die(self):
        fireflies.remove(self)
        del self # TODO: test die function

#Returns the euclidean distance between two points on the grid
#Input: tuples where pos1=(row1, col1), pos2=(row2, col2)
#Output: distance between pos1 and pos2
def dist(pos1,pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
#Returns the number of fireflies inside and outside the jar 
#Output: Number of fireflies inside jar, number of fireflies outside
def compute_in(): 
    global fireflies 
    num_in = 0
    num_out = 0
    for fly in fireflies: 
        if fly.loc == 0:
            num_in += 1
        else:
            num_out += 1
    return num_in, num_out

# Computes the luminosity grid from all the fireflies 
# Input: any array with size equal to the size of the global grid 
# Output: array of doubles with each entry representing the combined luminosity from all fireflies for that space
def compute_luminosity(grid):
    global fireflies
    for fly in fireflies:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                grid[row,col] += (fly.base_lum * 1 / (max(dist((row,col),(fly.row,fly.col)),0.5) ** 2 ) )
            # Note that base_lum will be doubled at the location of where the firefly is
    return grid

# Spawns new fireflies on the grid 
# Input: luminosity grid from compute_luminosity 
# Output: None
# Actions: Spawns new fireflies randomly outside of the jar according to the max luminosity
def spawn(lum_grid):
    global x_pad, y_pad, max_lum
    end_y = np.shape(lum_grid)[0]
    end_x = np.shape(lum_grid)[1]

    rate = np.amax(lum_grid[y_pad + 1:(end_y - 1),x_pad + 1:(end_x - x_pad - 1)]) / max_lum
    x = np.random.uniform()
    if x < rate-math.floor(rate):
        Firefly(1)
    for i in range(max(int(rate),2)):
        Firefly(1)

def get_jarsize():
    global x_jar, y_jar, x_pad, y_pad 
    inside = x_jar*y_jar 
    outside = (2*x_pad+x_jar+2)*(2+y_pad+y_jar) - (x_jar+1)*(y_jar+1)
    return inside, outside

# Spawns num_injar fireflies inside of the jar and num_outjar fireflies outside of the jar
def initialize():
    global x_pad, y_pad, x_jar, y_jar, fireflies
    fireflies = []
    for i in range(num_injar):
        Firefly(0)
    for i in range(num_outjar):
        Firefly(1)

# Compute the luminosity grid, update the positions of each of the fireflies one at a time, spawn new fireflies
def update():
    global fireflies
    lum_grid = np.zeros((2 + y_pad + y_jar,2 + 2*x_pad + x_jar))
    lum_grid = compute_luminosity(lum_grid)
    for fly in fireflies:
        fly.move(lum_grid)
    spawn(lum_grid)

# Display the grid with yellow squares representing fireflies and teal squares representing jar boundary 
# Also shows a heatmap of the luminosity across the grid 
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

def get_eq(arr): 
    N = len(arr)
    avg = np.mean(fly_out[int(N/2):])
    for i in range(len(arr)): 
        if arr[i] >= avg:
            return i 
    return N-1

def plot_all():
    plt.cla()
    global params, fly_out_avg_arr, equil_arr
    plt.scatter(params[:,0],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. x_jar")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("x_jar")
    plt.figure()
    plt.scatter(params[:,0],equil_arr)
    plt.title("Time to Reach Equilibrium vs x_jar")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("x_jar")
    plt.figure()
    plt.scatter(params[:,1],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. y_jar")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("y_jar")
    plt.figure()
    plt.scatter(params[:,1],equil_arr)
    plt.title("Time to Reach Equilibrium vs y_jar")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("y_jar")
    plt.figure()
    plt.scatter(params[:,2],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. x_pad")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("x_pad")
    plt.figure()
    plt.scatter(params[:,2],equil_arr)
    plt.title("Time to Reach Equilibrium vs x_pad")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("x_pad")
    plt.figure()
    plt.scatter(params[:,3],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. y_pad")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("y_pad")
    plt.figure()
    plt.scatter(params[:,3],equil_arr)
    plt.title("Time to Reach Equilibrium vs y_pad")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("y_pad")
    plt.figure()
    plt.scatter(params[:,4],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. randomness")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("randomness")
    plt.figure()
    plt.scatter(params[:,4],equil_arr)
    plt.title("Time to Reach Equilibrium vs randomness")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("randomness")
    plt.figure()
    plt.scatter(params[:,5],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. num_injar")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("num_injar")
    plt.figure()
    plt.scatter(params[:,5],equil_arr)
    plt.title("Time to Reach Equilibrium vs num_injar")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("num_injar")
    plt.figure()
    plt.scatter(params[:,6],fly_out_avg_arr)
    plt.title("Average Outside Fireflies vs. num_outjar")
    plt.ylabel("Avg Outside Fireflies")
    plt.xlabel("num_outjar")
    plt.figure()
    plt.scatter(params[:,6],equil_arr)
    plt.title("Time to Reach Equilibrium vs num_outjar")
    plt.ylabel("Time to Reach Equilibrium")
    plt.xlabel("num_outjar")
    plt.show()


nsamples = 5
reruns = 2
nparams = 7

# Set up parameter array
params = npm.repmat(lhs(nparams, samples = nsamples),reruns,1) 
# Each row is a new parameter set

fly_out_avg_arr = []
equil_arr = []
N = 200
i = -1
while i < (np.shape(params)[0] - 1):
    i +=1
    print("Simulation: " + str(i + 1) + " / " + str(np.shape(params)[0]))
    x_jar = int(max(params[i,0] * 10, 2))
    y_jar = int(max(params[i,1] * 10, 2))
    x_pad = int(max(params[i,2] * 10, 1))
    y_pad = int(max(params[i,3] * 10, 1))
    randomness = params[i,4]
    num_injar = int(params[i,5]*20)
    num_outjar = int(params[i,6]*30)
    
    params[i,0] = x_jar
    params[i,1] = y_jar
    params[i,2] = x_pad
    params[i,3] = y_pad
    params[i,5] = num_injar
    params[i,6] = num_outjar
    
    r,s = get_jarsize()
    if num_injar > r or num_outjar > s:
        print("Deleting row...")
        params = np.delete(params, i, 0)
        i -= 1
        continue

    fly_out_avg_sum = 0
    equil_sum = 0
    initialize()
    fly_out = []
    for j in range(N):
        _,b = compute_in()
        fly_out.append(b)
        update()
    fly_out_avg_arr.append(np.mean(fly_out[100:]))   
    equil_arr.append(get_eq(fly_out))

plot_all()

"""
update()
observe()"""
#pycxsimulator.GUI().start(func=[initialize, observe, update])
