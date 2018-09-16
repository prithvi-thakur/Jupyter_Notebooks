
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
######################################################


# Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation, rc
from matplotlib import colors

# Main Function
def main():

    # Specify question 1 or 2
    C = competition_model()     # Create object
    
    #  P = C.set_parameters(1,2,1,3)   # set parameters: task 1
    P = C.set_parameters(3,2,4,3)   # set parameters: task 2

    # Time related variables
    dt = 0.01      # shortest timestep
    t = 0       # time variable
    tmax = 10    # maximum time
    it = 0      # iterator
    nmax = int(tmax/dt) + 2   # maximum number of timesteps

    # Pre-allocate variables (store N1, N2, time in arrays)
    N1 = np.zeros(nmax)
    N2 = np.zeros(nmax)
    time_ = np.zeros(nmax)
    
    # Set initial conditions
    N1[0], N2[0] = C.set_initial_conditions(0.1,0.9)

    # Time-loop
    while t < tmax:
        
        it = it + 1
        t = t + dt

        N1[it], N2[it] = C.euler_fwd_step(P,N1[it-1], N2[it-1], dt)
        time_[it] = t
    #------end while-------

    # Plot results
    plot(N1, N2, time_)
    
    return N1, N2, time_
#----------end main---------



class competition_model:
    "Lotka-Volterra Competition between species model"
    # (dN1/dt) = aN1(1-N1) - bN1N2
    # (dN2/dt) = cN2(1-N2) - dN2N1
    
    # Parameters a,b,c,d 
    def set_parameters(self,a, b,c,d):
        return a,b,c,d

    def set_initial_conditions(self, N1o, N2o):
        return N1o, N2o
    
    def euler_fwd_step(self, P, N1, N2, dt):
        # N1[t + dt] = N1[t] + (aN1[t]*(1-N1[t]) - bN1[t]*N2[t])dt
        # N2[t + dt] = N2[t] + (cN2[t]*(1-N2[t]) - dN1[t]N2[t])dt
        
        a,b,c,d = P 
        
        # N1, N2 at the next time-steps
        N1_it = N1 + (a*N1*(1 - N1) - b*N1*N2)*dt
        N2_it = N2 + (c*N2*(1 - N2) - d*N1*N2)*dt

        return N1_it, N2_it
#----------end class---------

# Plot function
def plot(N1, N2, time_):

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


# Execute main function
if __name__ =="__main__":
    main()
