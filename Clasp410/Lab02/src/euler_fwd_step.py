
######################################################
#
#   LOTKA-VOLTERRA MODEL
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


# Main Function
def main():
    
    # Create object: choose between the two models
    C = competition_model()     
    #  C = predator_prey_model()

    # Set the values of a,b,c,d
    param = C.set_parameters(1,2,1,3)   # set parameters: task 1
    #  param = C.set_parameters(3,2,4,3)   # set parameters: task 2

    # Time related variables
    dt = 0.001      # shortest timestep
    t = 0.0       # time variable
    tmax = 20    # maximum time
    it = 0      # iterator
    nmax = int(tmax/dt) + 1   # maximum number of timesteps

    # Pre-allocate variables (store N1, N2, time in arrays)
    N1 = np.zeros(nmax)
    N2 = np.zeros(nmax)
    time_ = np.zeros(nmax)
    
    # Set initial conditions
    N1[0], N2[0] = C.set_initial_conditions(0.5,0.5)

    #  ###############################################################
    #  # Plot a range of initial conditions: uncomment the section
    #  # create a 2D array: one dimension for time and other for 
    #  # different initial conditions.
    #  nIC = 40    # no. of different initial conditions
    #  NN1 = np.zeros((nmax, nIC))
    #  NN2 = np.zeros((nmax, nIC))

    #  for i in range(nIC):

        #  NN1[0,i], NN2[0,i] = C.set_initial_conditions((1/nIC)*i, 1 - (1/nIC)*i)
        
        #  it = 0; t = 0
        #  while t < tmax:
            
            #  it = it + 1
            #  t = round(t + dt,8)     # Rounding off due to floating point precision error in python

            #  NN1[it,i], NN2[it,i] = C.euler_fwd_step(param, NN1[it-1,i], NN2[it-1,i], dt)
            
            #  time_[it] = t
    #  #------end while-------
    
    #  ##############################################################

    # Time-loop
    while t < tmax:
        
        it = it + 1
        t = round(t + dt,8)     # Rounding off due to floating point precision error in python

        N1[it], N2[it] = C.euler_fwd_step(param, N1[it-1], N2[it-1], dt)
        
        time_[it] = t
    #------end while-------

    # Plot results
    #  plot_population(N1, N2, time_)
    #  plot_phase(N1, N2)
    
    return NN1, NN2, time_
#----------end main---------



class competition_model:
    "Lotka-Volterra Competition between species model"
    # (dN1/dt) = aN1(1-N1) - bN1N2      # Differential Equations
    # (dN2/dt) = cN2(1-N2) - dN2N1
    
    # Parameters a,b,c,d 
    def set_parameters(self,a, b,c,d):
        return a,b,c,d
    
    # Initial conditions
    def set_initial_conditions(self, N1o, N2o):
        return N1o, N2o
    
    def euler_fwd_step(self, param, N1, N2, dt):
        # Euler forward step discretized equations
        # N1[t + dt] = N1[t] + (aN1[t]*(1-N1[t]) - bN1[t]*N2[t])dt
        # N2[t + dt] = N2[t] + (cN2[t]*(1-N2[t]) - dN1[t]N2[t])dt
        
        a,b,c,d = param
        
        # N1, N2 at the next time-steps
        N1_it = N1 + (a*N1*(1 - N1) - b*N1*N2)*dt
        N2_it = N2 + (c*N2*(1 - N2) - d*N1*N2)*dt

        return N1_it, N2_it
#----------end class---------


class predator_prey_model:
    "Lotka-Volterra predator-prey model"
    # (dN1/dt) = aN1 - bN1N2
    # (dN2/dt) = -cN2 + dN2N1
    
    # Parameters a,b,c,d 
    def set_parameters(self,a, b,c,d):
        return a,b,c,d

    def set_initial_conditions(self, N1o, N2o):
        return N1o, N2o
    
    def euler_fwd_step(self, param, N1, N2, dt):
        # N1[t + dt] = N1[t] + (aN1[t] - bN1[t]*N2[t])dt
        # N2[t + dt] = N2[t] - (cN2[t] - dN1[t]N2[t])dt
        
        a,b,c,d = param
        
        # N1, N2 at the next time-steps
        N1_it = N1 + (a*N1 - b*N1*N2)*dt
        N2_it = N2 - (c*N2 - d*N1*N2)*dt

        return N1_it, N2_it

#----------end class---------



# Plot population
def plot_population(N1, N2, time_):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_, N1, 'k-', label='Species 1 population')
    ax.plot(time_, N2, 'b-', label='Species 2 population')

    ax.fill_between(time_, N1, alpha=0.4)
    ax.fill_between(time_, N2, alpha=0.4)

    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Population densities (N1 or N2)")
    ax.set_title("Lotka-Volterra competition between species model ")
    ax.legend(loc="upper right")
    plt.savefig("Part1g_population.png", dpi=300)
    plt.show()


# Plot phase diagram
def plot_phase(N1, N2):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(N1, N2, 'k-')
    ax.set_xlabel("N1 Population density")
    ax.set_ylabel("N2 Population density")
    ax.set_title("Lotka-Volterra competition between species model: Phase diagram")
    
    plt.savefig("Part1g_phase.png", dpi=300)
    plt.show()

# Execute main function
if __name__ =="__main__":
    main()
