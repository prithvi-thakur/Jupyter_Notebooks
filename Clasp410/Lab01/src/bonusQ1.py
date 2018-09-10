###################################################
#
#   FOREST FIRE MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-09-2018
#
#   Clasp 410 Lab 1: In a two dimensional forest
#                    with some trees and some bare
#                    land, initiate and spread fire
#      
#   Vectorized version: Only have time loop
###################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation, rc
from matplotlib import colors

#---------------
# Main commands
#---------------

# Define grid of ones
Nx = 6; Ny = 6
Grid = np.ones((Nx,Ny))

# Grid without boundary elements
inner_grid = Grid[1:Nx-1, 1:Ny-1]

# Define probabilities
start_fire = 0.1   # Probability that each cell is on fire   
catch_fire = 1    # Probability that a neighboring node catches fire
bare_patch = 1  # Probability that there is a bare patch 

# Initialize grid
rnd = np.random.rand(Nx-2, Ny-2)    # matrix of random numbers of grid size
# if random number is less than bare patch probability, grid point is tree
inner_grid[rnd < bare_patch] = 2      

# Set initial fire
rnd = np.random.rand(Nx-2, Ny-2)
inner_grid[rnd < start_fire] = 3

# Assemble final grid
Grid[1:Nx-1, 1:Ny-1] = inner_grid

# Number of cells on fire
cells_on_fire = (Grid == 3).sum()

# while loop
while cells_on_fire > 0:

    # Get index of cells on fire
    get_indx = np.where(Grid == 3)

    # Get adjacent indices if probability of spreading fire is favorable
    rnd = np.random.random(len(get_indx[0]))

    adj1 = (get_indx[0][rnd<catch_fire] - 1, get_indx[1][rnd<catch_fire])
    adj2 = (get_indx[0][rnd<catch_fire] + 1, get_indx[1][rnd<catch_fire])
    adj3 = (get_indx[0][rnd<catch_fire], get_indx[1][rnd<catch_fire] - 1)
    adj4 = (get_indx[0][rnd<catch_fire], get_indx[1][rnd<catch_fire] + 1)

    # Set fire to adjacent index  ONLY IF IT IS TREE=2!!!!!!!!
    Grid[adj1] = 3
    Grid[adj2] = 3
    Grid[adj3] = 3
    Grid[adj4] = 3

    # Extinguish the initial fire
    Grid[get_indx] = 1

    # Restore the boundary conditions
    Grid[0,:] = Grid[:,0] = Grid[:,Ny-1] = Grid[Nx-1,:] = 1

    # Compute the new cells on fire
    cells_on_fire = (Grid == 3).sum()

    print(Grid)

