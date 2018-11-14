######################################################
#
#   SNOWBALL EARTH
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 10-30-2018
#
#   Clasp 410 Lab 5: Snowball earth
#                    
######################################################


# Import modules
#  import matplotlib
#  matplotlib.use('TkAgg')
import numpy as np
import os
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/Lab05/figs/'


# Global variables
Re = 6371e3     # Radius of earth
So = 1367       # Solar Flux
Cp = 4.2e6      # Heat Capacity of sea water
λ = 100         # Thermal Diffusivity
ε = 0.6         # Emissivity
σ = 5.67e-8     # Steffan-Boltzmann constant

#------------------------------
# Domain discretization: Step 1
#------------------------------
def domain(N):
    global Re
    Δφ = 180/N  # Latitude discretization
    φ = np.linspace((Δφ/2)-90, 90-(Δφ/2), N)
    h = (np.sin(np.deg2rad(φ + Δφ/2)) - np.sin(np.deg2rad(φ - Δφ/2)))*Re
    area = 2*np.pi*Re*h # of each latitude band
    Δy = np.pi*Re/N
    return φ, area, Δy


#----------------------------------------
# Diffusive part of the equation: Step 2
#----------------------------------------

# General Finite Difference matrix
def fdm(N):
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))
    return K

# Zero slope boundary condition: returns modified finite difference matrix
def boundary(K):
    # Set the first and last row to match the boundary conditions
    K[0,0] = -1
    K[0,1] = 1
    K[-1,-2] = 1
    K[-1,-1] = -1
    return K

# Test the finite difference matrix with a known function
def test_fdm(K, N, φ, Δy):
    global Re
    T = np.sin(np.deg2rad(φ))

    # Analytical second derivative
    u_an = -T.copy()

    # Numerical second derivative
    u_nu = np.dot(K/(Δy**2),T)*Re**2

    return u_an, u_nu

#--------------------------
# Change in area: Step 3
#--------------------------

# forcing term
def forcing(T, area, Δy):

    # T_(i+1) - T_(i-1)
    tdiff = T[2::] - T[0:-2]
    
    # A_(i+1) - A_(i-1)
    Adiff = area[2::] - area[0:-2]

    # forcing
    f = tdiff*Adiff
    
    # Boundary Conditions: f = 0 at boundaries
    return np.hstack([0,f,0])/(area*4*Δy**2)

# Test the diffusion term
def test_area(K, T, f, φ, Δy):
    global Re, λ

    # degrees to radians
    o = np.deg2rad(φ)

    # Analytical expression
    u_an = λ*((-np.sin(o)/Re**2) + (2*o*np.cos(o)/(Re*(Re*o**2 + Re))))

    # Numerical Solution
    u_nu = λ*((K/Δy**2).dot(T) + f)

    return u_an, u_nu

# Main function
def main():
    # Number of latitude bands
    N = 90
    φ, ar, Δy = domain(N)
    Ko = fdm(N)
    K = boundary(Ko)

    y = Re*φ

    # Step 2: test with known function
    #  u_an, u_nu = test_fdm(K, N, φ, Δy)
    #  plot(u_an, u_nu, φ)
    
    # Step 3: Add the change in area to the PDE
    T = np.sin(np.deg2rad(φ))
    area = Re*np.deg2rad(φ)**2 + Re
    f = forcing(T, area, Δy)

    # Step 3: test with known function
    u_an3, u_nu3 = test_area(K, T, f, φ, Δy)
    plot(u_an3, u_nu3, φ)
    
    return u_an3, u_nu3

# Plot analytical vs numerical for step 2, 3
def plot(u_an, u_nu, x):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, u_an, 'k', label='analytical')
    ax.plot(x, u_nu, 'ko', markersize=3, mfc='none', label='finite difference')

    ax.set_xlabel("φ (degrees)")
    ax.set_ylabel("u(φ)")
    ax.set_title("Part 3 test: area term included(N=90 points)")
    plt.legend()
    filename = os.path.join(path, 'part3.png')
    plt.savefig(filename, dpi=300)
    plt.show()

