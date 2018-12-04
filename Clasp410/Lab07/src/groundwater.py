######################################################
#
#   GROUNDWATER MODELING
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 11-27-2018
#
#   Clasp 410 Lab 7: Groundwater flow through a porus medium 
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import interpolate
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/Lab07/figs/'

# Linear interpolation between two points
def interp(P1, P2, x):
    y = P1[1] + ((P2[1]-P1[1])/(P2[0]-P1[0]))*(x-P1[0])

    return y

def boundary(u, x, y):
    # Left boundary: x = 20
    P1 = np.array([0,0])
    P2 = np.array([0,3])
    P3 = np.array([0,6])
    P4 = np.array([0,8])

    u[0,0:3] = interp(P1,P2,x[0:3])
    u[0,0:3] = interp(P1,P2,x[0:3])



    # Right boundary: x = 20
    yR = np.array([1,4,9])
    fR = np.array([965,995,970])

    # Top Boundary: y = 10

    # Bottom Boundary: y = 0

    return u

# Define domain of the region
def domain(Nx, Ny):
    return 0

def main():
    Nx = 10
    Ny = 10

    x = np.linspace(0,Nx-1,Nx)
    y = np.linspace(0,Ny-1,Ny)

    # Potential function u
    u = np.zeros((Nx,Ny))


    u = boundary(u, x, y)

    return u

u = main()


