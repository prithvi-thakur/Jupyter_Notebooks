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
from scipy.sparse import spdiags, eye, kron
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/Lab07/figs/'

# Linear interpolation between two points
def interp(P1, P2, x):
    y = P1[1] + ((P2[1]-P1[1])/(P2[0]-P1[0]))*(x-P1[0])
    return y

def boundary(u, x, y):
    # Left boundary: x = 0, list of coordinates
    L1 = np.array([0e3,967])
    L2 = np.array([3e3,985])
    L3 = np.array([6e3,1000])
    L4 = np.array([8e3,990])

    u[0,0:4] = interp(L1,L2,y[0:4])
    u[0,4:7] = interp(L2,L3,y[4:7])
    u[0,7:11] = interp(L3,L4,y[7:11])

    # Right boundary: x = 20, list of coordinates
    R1 = np.array([1e3,965])
    R2 = np.array([4e3,995])
    R3 = np.array([9e3,970])

    u[-1,0:5] = interp(R1,R2,y[0:5])
    u[-1,5:11] = interp(R2,R3,y[5:11])
    
    # Top Boundary: y = 10
    T1 = np.array([0e3,980])
    T2 = np.array([20e3,965])

    u[:,-1] = interp(T1,T2,x)

    # Bottom Boundary: y = 0
    B1 = np.array([0e3,967])
    B2 = np.array([20e3,955])

    u[:,0] = interp(B1,B2,x)

    return u

def steady_state_diffusion(u,x,y,Nx, Ny):
    # Global index for u:
    uglob = np.reshape(u,u.size,1)

def main():

    dx = 1e3
    dy = 1e3

    Lx = 21e3     # x-dimension of domain
    Ly = 11e3     # y-dimension of domain

    x = np.linspace(0,Lx-1e3,int(Lx/dx))
    y = np.linspace(0,Ly-1e3,int(Ly/dy))

    Nx = len(x)
    Ny = len(y)

    K = 0.005   # hydraulic conductivity
    z = 10      # Thickness in z-dimension

    # Boundary values bo
    bo = np.zeros((Nx,Ny))
    bo = boundary(bo, x, y)

    # Create a sparse matrix to compute laplacian operator
    ex = np.ones(Nx)
    Dxx = spdiags(np.array([ex, -2*ex, ex]), np.array([-1,0,1]), Nx,Nx)/dx**2
    ey = np.ones(Ny)
    Dyy = spdiags(np.array([ey, -2*ey, ey]), np.array([-1,0,1]), Ny,Ny)/dy**2
    # Kronecker product
    L = K*(kron(Dxx,eye(Ny,Ny)) + kron(Dyy,eye(Nx,Nx)))

    # Apply boundary condition
    bo[0,:] = bo[0,:]/dy**2
    bo[-1,:] = bo[-1,:]/dy**2
    bo[:,0] = bo[:,0]/dx**2
    bo[:,-1] = bo[:,-1]/dx**2

    Hbc = np.reshape(bo,Nx*Ny)

    # SOlve the system of equations
    C = np.linalg.solve(-L.toarray(),Hbc)

    C = C.reshape(Nx,Ny)

    return C

C = main()


