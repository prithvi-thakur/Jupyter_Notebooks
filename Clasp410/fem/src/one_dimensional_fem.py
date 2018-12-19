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
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/fem/figs/'

class setup:
    # Discretization
    node = 10       # no. of nodes
    nel = node - 1  # no. of elements
    part = np.linspace(0, 1, node+2, endpoint = True)   # independent variable
    h = part[1]-part[0]     # element size: constant
    
    # Evaluate basis function at a point
    def phi(self, j, x):
        # Support points
        x_minus = self.part[j-1]
        x_j = self.part[j]
        x_plus = self.part[j+1]

        if (x == x_j):
            phi_point = 1
        elif(x > x_minus and x< x_j):
            phi_point = (1/h)*x
        elif(x > x_j and x < x_plus):
            phi_point = (-1//hj)*x
        else:
            phi_point = 0
        return phi_point

    def basis_function(self, j,xv):
        # evaluate over a whole range
        # xv = x vector
        bf = np.zeros(len(xv))
        for idx in range(0,len(xv)):
            bf[idx] = self.phi(j, xv[idx])
        return bf
    
    def f(self,x):       # Right hand side function
        return 1
    
    def rhs(self,j,x):   # Right hand size of the matrix
        return self.f(x)*self.basis_function(j,x)


class solver:
    def assemble_load_vector(self,part,M,rhs):
        load_vector = np.zeros(M)
        for indx in range(M):
            # integrate using simpsons rule
            load_vector[indx] = simps(rhs(indx+1, part), part)
        return load_vector

    # Assemble the stiffness matrix
    def assemble_stiffness(self,M):
        A = np.zeros((M,M))
        for i in range(M):
            A[i,i] = 2
            if i != 0:
                A[i,i-1] = -1
            if i != M-1:
                A[i,i+1] = -1
        return A

def main():
    # Create object instances
    S = setup()
    Sol = solver()

    # Get the A and b matrices
    b = Sol.assemble_load_vector(S.part, S.node, S.rhs)
    A = Sol.assemble_stiffness(S.node)

    # Normalize by space discretization
    A = A/S.h

    # Solve the system of equations
    coef = np.linalg.solve(A,b)

    # Multiply coefficients with basis functions to get solutions
    solution = np.zeros(S.node)
    for indx in range(S.node):
        solution[indx] = coef[indx]*S.basis_function(indx,S.part)[indx]

    # Analytical estimate
    anal = (-S.part**2 + S.part)/2

    # Plot solution
    plot_solution(S.part,solution,anal)

    # Plot errors
    #  error = np.abs(anal[1:S.node+1] - solution)
    #  plot_errors(S.part,error)
   
    # Plot basis functions for demonstration
    #  basis = np.zeros((S.node+2,S.node))
    #  for i in range(S.node-2):
        #  basis[:,i] = S.basis_function(i,S.part)

    #  fig = plt.figure(figsize=(9,6))
    #  ax = fig.add_subplot(111)

    #  ax.plot(S.part, basis[:,3:6],"k--")
    #  ax.set_title("Hat Basis functions")
    #  ax.set_xlabel("x")
    #  ax.set_ylabel(r"$\phi (x)$")

    #  fname = os.path.join(path,'fe_basis1.pdf')
    #  plt.savefig(fname,dpi=300)
    #  plt.show()


def plot_solution(part,solution,anal):
    M = len(part) - 2
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111)
            
    ax.plot(part[1:M+1],solution,"k.",label="Finite Element")
    ax.plot(part[1:M+1],anal[1:M+1], "k-", label="Analytical")
    ax.set_title("1D Finite Element Method (Hat basis functions)")
    ax.set_xlabel("x")
    ax.set_ylabel("u(x)")
    plt.legend()
    
    fname = os.path.join(path,'fe_sol2.pdf')
    plt.savefig(fname,dpi=300)
    plt.show()


def plot_errors(part,error):
    M = len(part) - 2
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111)

    ax.plot(part[1:M+1],error,"k.")
    ax.set_title("Errors")
    ax.set_xlabel("x")
    ax.set_ylabel("Absolute Error")

    fname = os.path.join(path,'fe_err.pdf')
    plt.savefig(fname,dpi=300)
    plt.show()

main()
