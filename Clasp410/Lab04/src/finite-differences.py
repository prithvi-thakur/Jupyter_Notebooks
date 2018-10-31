######################################################
#
#   SECOND-ORDER FINITE DIFFERENCES
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 10-25-2018
#
#   Clasp 410 Lab 4: Finite Difference Matrices
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/Lab04/figs/'

# Given function: u(x) = (1-x^2)
def u(x):
    return (1 - x**2)**2

def part1():

    global path

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

    ax.plot(x[1:-1], u_an[1:-1], 'k', label='analytical')
    ax.plot(x[1:-1], u2, 'ko', markersize=3, mfc='none', label='finite difference')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    ax.set_title("Solution for part 1 (N=100 points)")
    plt.legend()
    filename = os.path.join(path, 'part1.png')
    plt.savefig(filename, dpi=300)
    plt.show()


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

    # Analytical solution
    u_an = 1 - x**2

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(x, u_an, 'k', label='analytical solution')
    ax.plot(x, sol2, 'ko', markersize=3,  mfc='none', label='finite difference solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    ax.set_title("Solution for part 2 (N=100 points)")
    plt.legend()
    filename = os.path.join(path, 'part2.png')
    plt.savefig(filename, dpi=300)
    plt.show()


def part3():

    global path

    # Domain discretization
    N = 100
    xmax = 1; xmin = -1
    dx = (xmax-xmin)/(N-1)  # grid spacing
    x = np.linspace(xmin, xmax, N)

    # Right hand side of the matrix
    rhs = -2*np.ones(N-1)
    
    # Finite difference matrix
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))/dx**2

    # Strip the last row and column for bottom dirichlet boundary
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

    ax.plot(x, u_an, 'k', label='analytical solution')
    ax.plot(x, sol2, 'ko', markersize=3,  mfc='none', label='finite difference solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    ax.set_title("Solution for part 3 (N=100 points)")
    plt.legend()
    filename = os.path.join(path, 'part3.png')
    plt.savefig(filename, dpi=300)
    plt.show()

    #  return K2


def part4():

    global path

    # Domain discretization
    N = 100
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

    ax.plot(x, u_an, 'k', label='analytical solution')
    ax.plot(x, sol, 'ko', markersize=3.0, mfc='none', label='finite difference solution')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    ax.set_title("Solution for bonus (N=100 points)")
    plt.legend()
    filename = os.path.join(path, 'bonus.png')
    plt.savefig(filename, dpi=300)
    plt.show()

