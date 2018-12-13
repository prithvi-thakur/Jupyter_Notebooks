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
#  import matplotlib
#  matplotlib.use('TkAgg')
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.integrate import quadrature
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/fem/figs/'

class setup:
    # Discretization
    node = 10       # no. of nodes
    nel = node - 1  # no. of elements
    x = np.linspace(0,1,node)   # independent variable
    h = x[1]-x[0]     # element size: constant

    def hat1(self, x, x1, x2):
        return (x-x1)/(x2-x1)

    def hat2(self, x, x1, x2):
        return(x2-x)/(x2-x1)

    def basis(self, node, x, h):
        phi = np.zeros((node-2,node))
        #  for i in range(node-2):,cc
        return phi


class solver:
    def fe_matrix(self, h, N):
        M = (2/h)*np.eye(N)
        D1 = (-1/h)*np.diag(np.ones(N-1),k=1)
        D2 = (-1/h)*np.diag(np.ones(N-1),k=-1)
        M = M + D1 + D2
        return M

    def f(self, x):           # rhs function
        return 1

    def rhs(self,x):         # RHS matrix
        F = np.zeros(len(x))
        for i in range(2,len(x)-1):
            F[i] = quadrature(self.f(x),x[i], x[i+1])
            #  F[i+1] = quadrature(f,x[])
        return F

def main():
    S = solver()
    x = np.linspace(1,10,9)
    arr = S.rhs(x)
    return S, arr

S, arr = main()


