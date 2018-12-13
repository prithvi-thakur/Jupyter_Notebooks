######################################################
#
#   2D ELASTIC WAVE EQUATION WITH A POINT SOURCE
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 11-23-2018
#
#   Clasp 410 Final Project
#                    
######################################################


# Import modules
from fenics import *
import numpy as np
import os
import matplotlib.pyplot as plt
path ='/home/fenics/shared/figs/'

# Global Constants: Material properties
rho = 1     # density
mu = 1e9    # shear modulus

# Function to specify where the boundary conditions should be applied
def boundary(x, on_boundary):
    return on_boundary

# Define stress
def sigma(u):
    globla mu
    return mu*nabla_grad(u)

def main():
    globla rho, mu
    # Domain
    Nx = 10
    Ny = 10

    #----------------------
    # Generate simple mesh
    #----------------------
    mesh = UnitSquareMesh(Nx, Ny)

    #-------------------------------------
    # Define finite element function space
    #   P = lagrange elements
    #   1 = degree of finite element: 
    #       P1 = linear
    #--------------------------------------
    V = VectorFunctionSpace(mesh, 'P', 1)

    #-------------------------------------
    # Define the trial and test functions
    #-------------------------------------
    u = TrialFunction(V)
    v = TestFunction(V)

    #--------------------------------
    # Define the boundary conditions
    #--------------------------------
    u_D = Expression('1 + x[0]*x[0] + 2*x[1]*x[1]', degree=2)
    bc = DirichletBC(V, u_D, boundary)

    #--------------------------------
    # Define the variational problem
    #--------------------------------
    

    #------------------
    # Compute Solution
    #------------------
    u = Function(V)
