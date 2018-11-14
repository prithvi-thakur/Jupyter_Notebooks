#################################################
#
#  FENICS TUTORIAL: LINEAR ELASTICITY
#           
#   Description: 3-D beam clamped at one end
#                One end is fixed
#                Everything else is traction free
#
#       Author: Prithvi Thakur
#       Last Modified: 11-05-2018
#################################################

from __future__ import print_function
from fenics import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Path to save figures
#  path = '/Volumes/GoogleDrive/My Drive/Courses/coursework \
        #  /Clasp410/project/figs/elasticity'

path = "/home/fenics/shared/figs/"


# Domain: Scaled Variables
L = 1       # Length of beam
W = 0.2     # Width of the square cross section

rho = 1     # Density of the beam
mu = 1      # Elastic modulus
delta = W/L
gamma = 0.4*delta**2    #
beta = 1.25    #
lambda_ = beta       #
g = gamma       #

# Create mesh and define function space
mesh = BoxMesh(Point(0,0,0), Point(L,W,W), 10,3,3)
V = VectorFunctionSpace(mesh, 'P', 1)

# Define boundary condition:
tol = 1e-14

def clamped_boundary(x, on_boundary):
    return on_boundary and x[0]<tol

bc = DirichletBC(V, Constant((0,0,0)), clamped_boundary)

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
f = Constant((0, 0, -rho*g))
T = Constant((0, 0, 0))
a = inner(sigma(u), epsilon(v))*dx
L = dot(f, v)*dx + dot(T, v)*ds

# Compute solution
u = Function(V)
solve(a == L, u, bc)

# Plot solution
plot(u, title='Displacement', mode='displacement')

# Plot stress
s = sigma(u) - (1./3)*tr(sigma(u))*Identity(d)  # deviatoric stress
von_Mises = sqrt(3./2*inner(s, s))
V = FunctionSpace(mesh, 'P', 1)
von_Mises = project(von_Mises, V)
plot(von_Mises, title='Stress intensity')

# Compute magnitude of displacement
u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
plot(u_magnitude, 'Displacement magnitude')
print('min/max u:',
      u_magnitude.vector().array().min(),
      u_magnitude.vector().array().max())


# Plot stress
vv = von_Mises.compute_vertex_values()

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(vv, 'ko')

filename = path+"vom-mises"
plt.savefig(filename, dpi=300)
plt.show()


#  # Mesh plot
#  coor = mesh.coordinates()

#  fig = plt.figure()
#  ax = fig.add_subplot(111, projection = '3d')

#  ax.scatter(coor[:,0], coor[:,1], coor[:,2])

#  filename = path+"mesh"
#  plt.savefig(filename, dpi=300)
#  plt.show()
