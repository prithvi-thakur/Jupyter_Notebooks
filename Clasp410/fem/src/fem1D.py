######################################################
#
#   1D FINITE ELEMENT CODE
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 12-01-2018
#
#   Clasp Project: Programming finite element
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.integrate import quadrature as quad
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/fem/figs/'

#define RHS of equation
def f(x):
  return 1 #sin(10.*pi*x)*cos(25.*pi*x)

#uniform partition of the interval I
M = 100
part = np.linspace(0, 1, num = M+2, endpoint = True)
h = part[1] - part[0]

# Evaluate basis function at a point
def phi(j, x):
    global h
    # Support points
    x_minus = part[j-1]
    x_j = part[j]
    x_plus = part[j+1]

    if (x == x_j):
        phi_point = 1
    elif(x > x_minus and x< x_j):
        phi_point = (1/h)*x
    elif(x > x_j and x < x_plus):
        phi_point = (-1/h)*x
    else:
        phi_point = 0

    return phi_point

def basis_function(j,x):
    # evaluate over a whole range
    bf = np.zeros(len(x))

    for idx in range(0,len(x)):
        bf[idx] = phi(j, x[idx])

    return bf

def rhs(j,x):
    return f(x)*basis_function(j,x)

def assemble_load_vector(interval):
    load_vector = np.zeros(M)
    for indx in range(M):
        # integrate using simpsons rule
        load_vector[indx] = simps(rhs(indx+1, part), part)

    return load_vector

# Assemble the rhs = load vector
b = assemble_load_vector(part)


# Assemble the stiffness matrix
A = np.zeros((M,M))
for i in range(M):
    A[i,i] = 2
    if i != 0:
        A[i,i-1] = -1
    if i != M-1:
        A[i,i+1] = -1

# Normalize by space discretization
A = A/h

# Solve the system of equation
coef = np.linalg.solve(A,b)

solution = np.zeros(M)
for idx in range(len(part)-2):
    solution[idx] = coef[idx]*basis_function(idx, part)[idx]

# Analytical estimate
anal = (-part**2 + part)/2

# Plot
fig = plt.figure(figsize = (9,6))
ax = fig.add_subplot(111)

ax.plot(part[1:M+1], solution, "k.", label="Finite Element")
ax.plot(part[1:M+1], anal[1:M+1], "k-", label="Analytical")
ax.set_title("1D Finite Element Method")
ax.set_xlabel("x")
ax.set_ylabel("u(x)")
plt.legend()
fname=os.path.join(path, 'solution.pdf')
plt.savefig(fname, dpi=300)
plt.show()

# Plot error
fig = plt.figure(figsize = (9,6))
ax = fig.add_subplot(111)

ax.plot(solution- anal[1:M+1], "k.")
ax.set_title("Errors ")
ax.set_xlabel("x")
ax.set_ylabel("error")
fname=os.path.join(path, 'errorspdf')
plt.savefig(fname, dpi=300)
plt.show()
