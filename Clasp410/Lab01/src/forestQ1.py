###################################################
#
#   FOREST FIRE MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-13-2018
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
Nx = 250; Ny = 250
Grid = np.ones((Nx,Ny))

# Grid without boundary elements
inner_grid = Grid[1:Nx-1, 1:Ny-1]

# Define probabilities
start_fire = 0.000025 # Probability that each cell is on fire   
catch_fire = 0.7    # Probability that a neighboring node catches fire
bare_patch = 0.225 # Probability that there is a bare patch 


#------------------------
# Grid point values:
#       1 = bare patch
#       2 = trees
#       3 = trees on fire
#------------------------


# Initialize grid

# 1. Create a matrix of random numbers same size as the inner grid
rnd = np.random.rand(Nx-2, Ny-2)
# 2. Compare the random matrix with the bare patch probability and for the locations
#    where random number is greater, assign trees to the inner grid 
inner_grid[rnd > bare_patch] = 2      

# Set initial fire: similar procedure as above
rnd = np.random.rand(Nx-2, Ny-2)
inner_grid[rnd < start_fire] = 3

# Assemble the grid: inner grid + boundary elements
Grid[1:Nx-1, 1:Ny-1] = inner_grid

# Number of cells on fire
cells_on_fire = (Grid == 3).sum()

# Reshape grid matrix as array
grd = Grid.reshape(Nx*Ny)

# Compute the neighboring indices for 1D array
neighbour = lambda x: np.array([x-Nx, x+Nx, x-1, x+1])

"""
BcL = np.arange(0, Nx*Ny, Nx)   #   Left boundary indices
BcT = np.arange(0, Nx)          #   Top boundary indices
BcR = BcL + (Nx-1)              #   Right boundary indices
BcB = BcT + Nx*(Ny-1)           #   Bottom boundary indices
"""

# Data structure for animation
anim_Grid = np.ones((500, Nx, Ny))

anim_Grid[0,:,:] = Grid # Initial Grid

it = 0  # iterator

# while loop
while cells_on_fire > 0:

    it = it + 1
    
    # Get index of cells on fire
    get_indx = np.where(grd == 3)[0]

    # Get neighboring indices
    n_idx = neighbour(get_indx)
    
    # reshape the neighbouring indices to a 1d array for simplicity: 
    # because the above is an arraay of array rather than a matrix
    n_array = n_idx.reshape(n_idx.size)     # array of neighboring indices

    # Get the indices where the neighbour is tree
    tree_idx = n_array[grd[n_array] == 2]

    # Filter the neighbouring indices with unfavorable probability
    rnd = np.random.random(tree_idx.size)   # array of random numbers
    tree_idx = tree_idx[rnd < catch_fire]   # filter indices
    
    # Set filtered neighours to fire
    grd[tree_idx] = 3

    # Extinguish the initial fire
    grd[get_indx] = 1

    # Compute the new number of cells on fire
    cells_on_fire = (Grid == 3).sum()
    
    # Store grid at every time-step for animation
    anim_Grid[it,:,:] = grd.reshape(Nx, Ny)

#-----------end loop-----------------------------------------


# Remove the unallocated matrices from the animation grid
anim_Grid = anim_Grid[0:it, :, :] 

# Create colormap: 1 = grey, 2 = green, 3 = red
cmap = colors.ListedColormap(['grey', 'green', 'red'])
bounds = [0,1.1, 2.1, 3.1]
norm = colors.BoundaryNorm(bounds, cmap.N)

# Function to plot figures at various timesteps
def grid_plot(anim_Grid, it):

    #for i in range(it-1):       # use this if you want every timestep
    for i in [50, 100, 200, 300, 400]: #[0,int(it/2),it-1]:   # use this for specific timesteps
        fig = plt.figure()
        ax = plt.axes(xlim=(0,Nx), ylim=(0,Ny))
        ax.set_xlabel("Points along X axis")
        ax.set_ylabel("Points along Y axis")
        ax.set_title("Experiment 3: Mixed setting: Iteration " + str(i))

        im = ax.imshow(anim_Grid[i,:,:], extent = [0,Nx,0,Ny], interpolation='nearest',
                        cmap = cmap, norm = norm)
        plt.show()
        plt.savefig("exp3_" + str(i) + ".png", dpi=300)



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
ax.set_title("Experiment 1a: with 10 percent catch fire probability")

im = ax.imshow(anim_Grid[0,:,:], extent = [0,Nx,0,Ny], interpolation='nearest',
                cmap = cmap, norm = norm)

anim = animation.FuncAnimation(fig, updatefig, init_func=init, frames = it,
                               interval=40)

#  mywriter = animation.FFMpegWriter()
#  anim.save('Experiment1a.mp4', writer=mywriter)

plt.show()
anim
