##########################################################
#
#   EBOLA VIRUS SPREADING MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-13-2018
#
#   Clasp 410 Lab 1: In a two dimensional world
#                    with some healthy and some infected
#                    people, simulate the spread of disease
#      
#   Vectorized version: Only have time loop
###########################################################


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
start_disease = 0.000025 # Probability that disease initiates
catch_disease = 0.7    # Probability that a neighboring people catch disease
immune = 0 # Probability that there is immunization 
cure_prob = 0.5 # Probability of getting cured and immunity

#------------------------
# Grid point values:
#       1 = Immune people
#       2 = Healthy people
#       3 = Diseased people
#       4 = Dead people
#------------------------


# Initialize grid

# 1. Create a matrix of random numbers same size as the inner grid
rnd = np.random.rand(Nx-2, Ny-2)
# 2. Compare the random matrix with the bare patch probability and for the locations
#    where random number is greater, assign trees to the inner grid 
inner_grid[rnd > immune] = 2      

# Set initial disease: similar procedure as above
rnd = np.random.rand(Nx-2, Ny-2)
inner_grid[rnd < start_disease] = 3

# Assemble the grid: inner grid + boundary elements
Grid[1:Nx-1, 1:Ny-1] = inner_grid

# Number of cells on fire
cells_on_fire = (Grid == 3).sum()

# Reshape grid matrix as array
grd = Grid.reshape(Nx*Ny)

# Compute the neighboring indices for 1D array
neighbour = lambda x: np.array([x-Nx, x+Nx, x-1, x+1])


# Data structure for animation
anim_Grid = np.ones((700, Nx, Ny))

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
    tree_idx = tree_idx[rnd < catch_disease]   # filter indices
    
    # Set filtered neighours to fire
    grd[tree_idx] = 3

    # Dead people have index = 4
    grd[get_indx] = 4

    # Some people are cured and immune to future attacks
    rnd = np.random.rand(get_indx.size)
    cured_indx = get_indx[rnd < cure_prob]
    grd[cured_indx] = 1

    # Compute the new number of cells on fire
    cells_on_fire = (Grid == 3).sum()
    
    # Store grid at every time-step for animation
    anim_Grid[it,:,:] = grd.reshape(Nx, Ny)

#-----------end loop-----------------------------------------


# Remove the unallocated matrices from the animation grid
anim_Grid = anim_Grid[0:it, :, :] 

# Create colormap: 1 = grey, 2 = green, 3 = red, 4 = blue
cmap = colors.ListedColormap(['grey', 'green', 'red', 'blue'])
bounds = [0,1.1, 2.1, 3.1, 4.1]
norm = colors.BoundaryNorm(bounds, cmap.N)

# Function to plot figures at various timesteps
def grid_plot(anim_Grid, it):

    #for i in range(it-1):       # use this if you want every timestep
    for i in [10, 50, 100, 200]: #[0,int(it/2),it-1]:   # use this for specific timesteps
        fig = plt.figure()
        ax = plt.axes(xlim=(0,Nx), ylim=(0,Ny))
        ax.set_xlabel("Points along X axis")
        ax.set_ylabel("Points along Y axis")
        ax.set_title("Bonus Q2: Iteration " + str(i))

        im = ax.imshow(anim_Grid[i,:,:], extent = [0,Nx,0,Ny], interpolation='nearest',
                        cmap = cmap, norm = norm)
        plt.show()
        plt.savefig("bonus_" + str(i) + ".png", dpi=300)



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
