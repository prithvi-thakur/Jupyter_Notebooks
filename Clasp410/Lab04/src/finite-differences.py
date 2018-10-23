######################################################
#
#   SECOND-ORDER FINITE DIFFERENCES
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 10-18-2018
#
#   Clasp 410 Lab 4: Finite Difference Matrices
#                    
######################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt


# Given function: u(x) = (1-x^2)
def u(x):
    return (1 - x**2)**2

def part1():
    # Domain: [-1,1]
    xmin = -1
    xmax = 1

    N = 100   # Number of discretized points
    dx = (xmax-xmin)/(N-1)  # grid spacing
    x = np.linspace(xmin, xmax, N)
   
    # Given function
    U = u(x)

    # Analytical second derivative
    u_an = 12*x**2 - 4
    
    # Construct the matrix for second derivative
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))/dx**2

    K2 = K[1:-1, :]

    # Square matrix without first and last rows and columns
    KI = K[1:-1, 1:-1]
    
    # Solution
    u2 = np.dot(KI,U[1:-1])

    # Plot analytical vs finite difference
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x[1:-1], u2, label='finite difference')
    ax.plot(x[1:-1], u_an[1:-1], label='analytical')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    plt.show()

    return u2, u_an


# Finite difference matrix
def fdmatrix(N, dx):
    
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))/dx**2

    # return the inner part of the matrix without first and last rows and columns
    return K[1:-1, 1:-1]



def part2():

    # Domain discretization
    N = 100
    xmax = 1; xmin = -1
    dx = (xmax-xmin)/(N-1)  # grid spacing
    x = np.linspace(xmin, xmax, N)

    # Right hand side of the matrix
    rhs = -2*np.ones(N-2)
    
    # Finite difference matrix
    K = fdmatrix(N, dx)

    # Solve the matrix equation
    sol = np.linalg.solve(K, rhs)
    
    # Include boundary conditions
    sol2 = np.hstack([0,sol,0])

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, sol2, label='finite difference solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    plt.show()


def part3():

    # Domain discretization
    N = 100
    xmax = 1; xmin = -1
    dx = (xmax-xmin)/(N-1)  # grid spacing
    x = np.linspace(xmin, xmax, N)

    # Right hand side of the matrix
    rhs = -2*np.ones(N-1)
    
    # Finite difference matrix
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))/dx**2

    # Strip the last row and column
    K2 = K[0:-1, 0:-1]

    # Top Boundary:
    K2[0,0] = 1; K2[0,1] = -1
    rhs[0] = 0


    # Analytical solution
    u_an = -x**2 -2*x + 3
    
    # Solve the matrix equation
    sol = np.linalg.solve(K2, rhs)
    
    # Include boundary conditions
    sol2 = np.hstack([sol,0])

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, sol2, label='finite difference solution')
    ax.plot(x, u_an, label='analytical solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    plt.show()

    #  return K2


def part4():

    # Domain discretization
    N = 1000
    xmax = 1; xmin = -1
    dx = (xmax-xmin)/(N-1)  # grid spacing
    x = np.linspace(xmin, xmax, N)

    # Right hand side of the matrix
    rhs = -2*np.ones(N)
    
    # Finite difference matrix
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))/dx**2

    # Top Boundary:
    K[0,0] = 1; K[0,1] = -1
    rhs[0] = 0

    # Bottom Boundary
    K[-1,-1] = 1
    K[-1,-2] = 0
    rhs[-1] = 1

    # Analytical solution
    u_an = -x**2 -2*x + 4
    
    # Solve the matrix equation
    sol = np.linalg.solve(K, rhs)
    
    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, sol, label='finite difference solution')
    ax.plot(x, u_an, label='analytical solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    plt.show()

