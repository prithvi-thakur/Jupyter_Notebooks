###################################################
#
#   FOREST FIRE MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 
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
    start_fire = 0.25
    catch_fire = 0.3
    bare_patch = 0.225
    ignite = 0.5

# Domain size and timesteps
Nx = 100
Ny = 100
Nt = 20
Grid = grid(Nt, Nx, Ny)

# Initialize Probabilities
prob = probabilities()

# Initialize the domain
#   1 = bare ground
#   2 = forest
# Edges are bare ground by default
for i in range(1,Nx-1):
    for j in range(1,Ny-1):
        # initialize trees in forest, default is bare ground
        if np.random.random() > prob.bare_patch:
            Grid[0, i,j] = 2

# Initial grid for plotting
Grid_initial = Grid[0,:,:]

# Initial forest fire
for i in range(1,Nx-1):
    for j in range(1,Ny-1):
        if np.random.random() < prob.catch_fire:
            if Grid[0, i,j] == 2:
                Grid[0, i,j] = 3


# Spread the fire
for t in range(Nt-1):
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            
            if Grid[t,i,j] == 3:        # If the current cell is on fire
                
                if Grid[t,i,j+1] == 2:  # If neighbors are trees
                    if np.random.random() < prob.ignite:
                        Grid[t,i,j+1] = 3

                if Grid[t,i+1,j] == 2:
                    if np.random.random() < prob.ignite:
                        Grid[t,i+1,j] = 3

                if Grid[t,i-1,j] == 2:
                    if np.random.random() < prob.ignite:
                        Grid[t,i-1,j] = 3

                if Grid[t,i,j-1] == 2:
                    if np.random.random() < prob.ignite:
                        Grid[t,i,j-1] = 3
             
                # Extinguish initial fire
                Grid[t,i,j] = 1   

    # Assign previous solution to the next iteration
    Grid[t+1,:,:] = Grid[t,:,:]


# Animate the spread

def init():
    return [im]

def frame(i):
    a = im.get_array()
    a = Grid[i,:,:]
    im.set_array(a)

    return [im]


#  def anim(Grid):

#  Nx = len(Grid[0,:,0])
#    Ny = len(Grid[0,0,:])
#    Nt = len(Grid[:,0,0])

fig = plt.figure()
ax = plt.axes(xlim=(0,Nx), ylim=(0,Ny))
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.set_title("Forest fire spread")

im = ax.imshow(Grid[0,:,:], extent = [0,Nx,0,Ny], interpolation='bilinear')

anim = animation.FuncAnimation(fig, frame, init_func=init, frames = Nt,
                               interval=500, blit=True)

plt.show()


anim
