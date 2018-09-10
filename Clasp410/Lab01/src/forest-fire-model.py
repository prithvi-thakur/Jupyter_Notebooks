###################################################
#
#   FOREST FIRE MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-08-2018
#
#   Clasp 410 Lab 1: In a two dimensional forest
#                    with some trees and some bare
#                    land, initiate and spread fire
#       
###################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation, rc
from matplotlib import colors
import os

#my_path = os.path.abspath(__file__)

# Define grid
def grid(Nx, Ny):
    return np.ones((Nx, Ny))

# Define probabilities
class probabilities:
    start_fire = 0.000025   # Probability that each cell is on fire   
    catch_fire = 1    # Probability that a neighboring node catches fire
    bare_patch = 1  # Probability that there is a bare patch 

def initialize(Grid, Nx, Ny, prob):
    # Initialize the domain
    #   1 = bare ground
    #   2 = forest
    #   3 = fire
    # Edges are bare ground by default
    for i in range(1,Nx-1):
        for j in range(1,Ny-1):
            # initialize trees in forest, default is bare ground
            if np.random.random() > prob.bare_patch:
                Grid[i,j] = 2

    return Grid

def initial_forest_fire(Grid, Nx, Ny, prob):
    # Assign initial forest fire cells
    for i in range(1,Nx-1):
        for j in range(1,Ny-1):
            if np.random.random() < prob.start_fire:
                # If grid is forest and probability is favorable, then start fire
                if Grid[i,j] == 2:
                    Grid[i,j] = 3
    return Grid


def spread_fire(Grid, Nx, Ny, prob):
    # Spread the fire
    # Future burning cells are given a value 4 till the loop is complete

    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            
            if Grid[i,j] == 3:        # If the current cell is on fire
                
                if Grid[i,j+1] == 2:  # If neighbors are trees, check each neighbor
                    if np.random.random() < prob.catch_fire:
                        Grid[i,j+1] = 4

                if Grid[i+1,j] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i+1,j] = 4

                if Grid[i-1,j] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i-1,j] = 4

                if Grid[i,j-1] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i,j-1] = 4
             
                # Extinguish initial fire
                Grid[i,j] = 1   


    Grid[Grid == 4] = 3      # Assign the value 3 to the burning cells
    return Grid


# Main function
#def main():
# Domain size and timesteps
Nx = 250     # X dimension
Ny = 250     # Y dimension

t = 0        # Iterator

# Initialize grid
Grid = grid(Nx, Ny)

# Initialize Probabilities
prob = probabilities()

# Initialize the domain
Grid = initialize(Grid, Nx, Ny, prob)

# Initial forest fire
Grid = initial_forest_fire(Grid, Nx, Ny, prob)

# Create colormap: 1 = grey, 2 = green, 3 = red
cmap = colors.ListedColormap(['grey', 'green', 'red'])
bounds = [0,1.1, 2.1, 3.1]
norm = colors.BoundaryNorm(bounds, cmap.N)

#"""
# Plot initial grid    
fig, ax = plt.subplots(1,1)
ax.imshow(Grid, interpolation='nearest', extent = [0,Nx,0,Ny], cmap=cmap, norm=norm)
ax.set_xlabel("Points along X axis")
ax.set_ylabel("Points along Y axis")
ax.set_title("Experiment 1 with no bare patch: Initial Grid")
plt.savefig("Experiment1a_0.png", dpi=150)
plt.show()
#"""

# Data structure for animation
anim_Grid = np.ones((500, Nx, Ny))


# No. of cells on fire initially
unique, counts =  np.unique(Grid, return_counts = True)
no_fire_cells = counts[np.where(unique == 3)[0]]

# Time loop
while no_fire_cells.size != 0:

    anim_Grid[t,:,:] = Grid
    
    # Spread the fire
    Grid = spread_fire(Grid, Nx, Ny, prob)
    
    # Count the number of trees on fire, i.e., the value is 3
    # This function returns the number of unique values and count of those values
    unique, counts =  np.unique(Grid, return_counts = True)
    
    # Calculate the number of cells on fire
    no_fire_cells = counts[np.where(unique == 3)[0]]

    t = t+1

#------------end of while----------

"""anim_Grid = anim_Grid[0:t, :,:]

# Plot grid after certain intervals  
fig, ax = plt.subplots(1,1)
ax.imshow(anim_Grid[50,:,:], interpolation='nearest', extent = [0,Nx,0,Ny], cmap=cmap, norm=norm)
ax.set_xlabel("Points along X axis")
ax.set_ylabel("Points along Y axis")
ax.set_title("Experiment 1 with no bare patch: Grid after 50 iterations")
plt.savefig("Experiment1a_50.png", dpi=150)
plt.show()
"""

# Animation functions
def init():
    return [im]

def updatefig(i):
    a = im.get_array()
    a = anim_Grid[i,:,:]
    im.set_array(a)
    return [im]


# Plot and animate
fig = plt.figure()
ax = plt.axes(xlim=(0,Nx), ylim=(0,Ny))
ax.set_xlabel("Points along X axis")
ax.set_ylabel("Points along Y axis")
ax.set_title("Experiment 1: with no bare patches")

im = ax.imshow(anim_Grid[0,:,:], extent = [0,Nx,0,Ny], interpolation='nearest',
                cmap = cmap, norm = norm)

anim = animation.FuncAnimation(fig, updatefig, init_func=init, frames = t,
                               interval=10)

mywriter = animation.FFMpegWriter()
anim.save('Experiment1a.mp4', writer=mywriter)

plt.show()
anim


# Execute main function
#if __name__ =="__main__":
#    main()
