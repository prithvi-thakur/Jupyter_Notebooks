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

# Define grid
def grid(Nt, Nx, Ny):
    return np.ones((Nt, Nx, Ny))

# Define probabilities
class probabilities:
    start_fire = 0.0025   # Probability that each cell is on fire   
    catch_fire = 1    # Probability that a neighboring node catches fire
    bare_patch = 0.225  # Probability that there is a bare patch 

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
                Grid[0, i,j] = 2

    return Grid

def initial_forest_fire(Grid, Nx, Ny, prob):
    # Assign initial forest fire cells
    for i in range(1,Nx-1):
        for j in range(1,Ny-1):
            if np.random.random() < prob.start_fire:
                # If grid is forest and probability is favorable, then start fire
                if Grid[0, i,j] == 2:
                    Grid[0, i,j] = 3
    return Grid


def spread_fire(Grid, Nx, Ny, prob):
    # Spread the fire
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            
            if Grid[i,j] == 3:        # If the current cell is on fire
                
                if Grid[i,j+1] == 2:  # If neighbors are trees, check each neighbor
                    if np.random.random() < prob.catch_fire:
                        Grid[i,j+1] = 3

                if Grid[i+1,j] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i+1,j] = 3

                if Grid[i-1,j] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i-1,j] = 3

                if Grid[i,j-1] == 2:
                    if np.random.random() < prob.catch_fire:
                        Grid[i,j-1] = 3
             
                # Extinguish initial fire
                Grid[i,j] = 1   
    return Grid


# Main function
def main():
    # Domain size and timesteps
    Nx = 250     # X dimension
    Ny = 250     # Y dimension
    Nt = 60     # No. of timesteps
    
    # Iterators
    k = 1       # Check when no more trees on fire 
    t = 0       # Iterator

    # Initialize grid
    Grid = grid(Nt, Nx, Ny)
    
    # Initialize Probabilities
    prob = probabilities()

    # Initialize the domain
    Grid = initialize(Grid, Nx, Ny, prob)

    # Initial grid for plotting
    Grid_initial = Grid[0,:,:]

    # Initial forest fire
    Grid = initial_forest_fire(Grid, Nx, Ny, prob)

    # Time loop
    while k != 0:

        # Spread the fire
        Grid[t,:,:] = spread_fire(Grid[t,:,:], Nx, Ny, prob)
        
        # Assign previous solution to the next iteration
        Grid[t+1,:,:] = Grid[t,:,:]

        # Count the number of trees on fire, i.e., the value is 3
        unique, counts =  np.unique(Grid[t,:,:], return_counts = True)
        
        no_fire_cells = counts[np.where(unique == 3)[0]]
        
        # Check if no more trees are on fire
        if no_fire_cells.size == 0:
            k = 0
        
        #  print(Grid[t,:,:])
        t = t+1

    # Remove extra allocations from Grid
    Grid = Grid[0:t, :,:]
    print(t)
    # Animation functions
    def init():
        return [im]

    def frame(i):
        a = im.get_array()
        a = Grid[i,:,:]
        im.set_array(a)
        return [im]

    # Plot and animate
    fig = plt.figure()
    ax = plt.axes(xlim=(0,Nx), ylim=(0,Ny))
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_title("Forest fire spread")

    im = ax.imshow(Grid[0,:,:], extent = [0,Nx,0,Ny], interpolation='bilinear')

    anim = animation.FuncAnimation(fig, frame, init_func=init, frames = t,
                                   interval=500, blit=True)
    plt.show()
    anim


# Execute main function
if __name__ =="__main__":
    main()
