######################################################
#
#   ENERGY-BALANCE MODELS
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 10-02-2018
#
#   Clasp 410 Lab 3: Vertical Energy Balance Models
#                    
######################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt


# PART 2: Single atmospheric layer for earth
def part2():
    # Ground Temperature vs. Emissivity of the atmosphere
    # Equation: Tg^4 = (1-α)So/[2σ(2 - ε)]

    # Given values for earth:
    So = 1350
    α = 0.33
    σ = 5.67e-8

    # ε range of values
    ε = np.linspace(0,1,100)

    Tg4 = (1-α)*So/(2*σ*(2 - ε))

    Tg = np.power(Tg4, 0.25)


    # Plot Ground temp vs emissivity
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ε, Tg)

    ax.set_xlabel("Emissivity")
    ax.set_ylabel("Ground Temperature (K)")
    ax.set_title("Single layer atmospheric model for earth")
    #  plt.savefig("Part1g_population.png", dpi=300)
    plt.show()


# Part 3: N layer atmospheric model
def part3():

    N = 100 # max. no. of atmospheric layers
    
    M = 2*np.eye(N+1,N+1) # coefficient matrix = diagonal matrix of twos
    b = np.zeros(N+1)       # RHS vector
    
    # Constant values for venus:
    So = 2600
    α = 0.71
    σ = 5.67e-8
    
    # Incoming solar radiation
    b[0] = (1 - α)*So/4

    # Assembling the coefficient matrix
    M[0,0] = 1      # first element
    M[-1,-1] = -1   # last element
    
    superdiagonal_indx = (np.arange(N-1), np.arange(N-1)+1)
    subdiagonal_indx = (np.arange(N-1)+1, np.arange(N-1))

    M[superdiagonal_indx] = -1
    M[subdiagonal_indx] = -1

    M[-1,-3] = 0    # The last equation has no flux from upper layer

    # Solve system of linear equations
    fluxes = np.linalg.solve(M,b)
    
    # Temperature
    T = np.power(fluxes/σ, 0.25)[0:-1]

    return len(T) - np.where(T >= 700)[0][-1]

