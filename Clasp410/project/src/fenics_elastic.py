#################################################
#
#   FENICS: ELASTOSTATICS
#           
#   Description: 2-D sheet fixed at one end
#                Everything else is traction free
#
#       Author: Prithvi Thakur
#       Last Modified: 11-05-2018
#   
#   Docker container: fenicsproject start elastic
#################################################

from __future__ import print_function
from fenics import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

path = "/home/fenics/shared/figs/"

# Domain: Scaled Variables
Nx = 10
Ny = 10
L = 1
W = 1
rho = 1     # Density of the beam
mu = 1      # Elastic modulus
delta = W/L
gamma = 0.4*delta**2  
beta = 1.25 
lambda_ = beta 
g = gamma 

# Create mesh and define function space
mesh = RectangleMesh(Point(0,0), Point(L,W), Nx,Ny)
V = VectorFunctionSpace(mesh, 'P', 1)

# Define boundary condition:
tol = 1e-14

def clamped_boundary(x, on_boundary):
    return on_boundary and x[0]<tol

bc = DirichletBC(V, Constant((0,0)), clamped_boundary)

# Define strain and stress
def epsilon(u):
    return 0.5*(nabla_grad(u) + nabla_grad(u).T)
    #return sym(nabla_grad(u))

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d) + 2*mu*epsilon(u)

# Define variational problem
u = TrialFunction(V)
d = u.geometric_dimension()  # space dimension
v = TestFunction(V)
f = Constant((0, -rho*g))
T = Constant((0, 0))
a = inner(sigma(u), epsilon(v))*dx
L = dot(f, v)*dx + dot(T, v)*ds

# Compute solution
u = Function(V)
solve(a == L, u, bc)

# Plot stress
s = sigma(u) - (1./3)*tr(sigma(u))*Identity(d)  # deviatoric stress
von_Mises = sqrt(3./2*inner(s, s))
V = FunctionSpace(mesh, 'P', 1)
von_Mises = project(von_Mises, V)
vm = von_Mises.compute_vertex_values()
mc = mesh.coordinates()

# Compute magnitude of displacement
u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
um = u_magnitude.compute_vertex_values()

# Plot displacement
fig = plt.figure()
ax = fig.add_subplot(111)
sc = ax.tripcolor(mc[:,0], mc[:,1],um)
ax.set_xlabel("X axis of the material (unit length)")
ax.set_ylabel("Y axis of the material (unit legnth)")
ax.set_title("Steady state displacement under gravity (unit displacement)")
filename = path+"u.pdf"
plt.colorbar(sc)
plt.savefig(filename, dpi=300)
plt.show()

# Plot stress
fig = plt.figure()
ax = fig.add_subplot(111)
sc = ax.tripcolor(mc[:,0],mc[:,1],vm)
ax.set_xlabel("X axis of the material (unit length)")
ax.set_ylabel("Y axis of the material (unit length)")
ax.set_title("Steady state stresses under gravity (unit stress)")
filename = path+"vm.pdf"
plt.colorbar(sc)
plt.savefig(filename, dpi=300)
plt.show()
