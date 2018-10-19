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
    KI = K[1:-1, 1:-1]
    
    u2 = np.dot(KI,U[1:-1])

    # Plot analytical vs finite difference
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x[1:-1], u2, label='finite difference')
    ax.plot(x, u_an, label='analytical')

    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    plt.show()


    return u2, u_an
