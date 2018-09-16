
######################################################
#
#   PREDATOR PREY MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-13-2018
#
#   Clasp 410 Lab 2: Nonlinear population growth model
#                    
#       
######################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation, rc
from matplotlib import colors


# Lotka-Volterra competition between species model
#--------------------------------------------------
# (dN1/dt) = aN1(1-N1) - bN1N2
# (dN2/dt) = cN2(1-N2) - dN2N1
# a,b,c,d are constants


# Input parameter set
a = 3; b = 2; c = 4; d = 3

# Initial conditions
N1o = 0.1   # N1 at (t = 0)
N2o = 0.9   # N2 at (t = 0)

# Time related variables
dt = 0.001      # shortest timestep
t = 0       # time variable
tmax = 10    # maximum time
it = 0      # iterator
nmax = int(tmax/dt) + 2   # maximum number of timesteps

# Pre-allocate variables (store N1, N2, time in arrays)
N1 = np.zeros(nmax)
N2 = np.zeros(nmax)
time_ = np.zeros(nmax)

N1[0] = N1o
N2[0] = N2o

# EULER FORWARD STEP EQUATIONS
#-----------------------------

# N1[t + dt] = N1[t] + (aN1[t]*(1-N1[t]) - bN1[t]*N2[t])dt
# N2[t + dt] = N2[t] + (cN2[t]*(1-N2[t]) - dN1[t]N2[t])dt


class competition_model:
    "Lotka-Volterra Competition between species model"
    
    # Parameters a,b,c,d 
    def set_parameters(self,a, b,c,d):
        return a,b,c,d
    
    def euler_fwd_step(self, N1, N2, dt):

        a,b,c,d = self.set_parameters()
        
        # N1, N2 at the next time-steps
        N1_it = N1 + (a*N1*(1 - N1) - b*N1*N2)*dt
        N2_it = N2 + (c*N2*(1 - N2) - d*N1*N2)*dt

        return N1_it, N2_it

# Main Function
def main():

    # Specify question 1 or 2
    C = competition_model()     # Create object
    C.set_parameters(3,2,4,3)   # set parameters

# TIME LOOP
#-----------
while t < tmax:
    
    t = t + dt      # update time
    it = it + 1

    N1[it] = N1[it-1] + (a*N1[it-1]*(1-N1[it-1]) - b*N1[it-1]*N2[it-1])*dt

    N2[it] = N2[it-1] + (c*N2[it-1]*(1-N2[it-1]) - d*N1[it-1]*N2[it-1])*dt

    time_[it] = t

#----------end-while---------

# Plot stuff
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(time_, N1, label='Species 1 population')
ax.plot(time_, N2, label='Species 2 population')

ax.fill_between(time_, N1, alpha=0.4)
ax.fill_between(time_, N2, alpha=0.4)

ax.set_xlabel("Time")
ax.set_ylabel("Population (N1 or N2)")
ax.set_title("Lotka-Volterra competition between species model")
ax.legend(loc="upper right")

plt.show()
