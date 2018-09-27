######################################################
#
#   LOTKA-VOLTERRA MODEL
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-13-2018
#
#   Clasp 410 Lab 2: Nonlinear population growth model
#                    Solve using odeint from scipy
######################################################

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Main Function
def main():
    
    # Create object: 
    C = predator_prey_model()

    # Set the values of a,b,c,d
    params = C.set_parameters(1,2,1,3)   

    # Time related variables
    tmax = 10       # maximum time
    nsteps = 10000    # number of timesteps

    # Create timesteps as an array 
    time_ = np.linspace(0, tmax, nsteps)
    
    # Set initial conditions
    IC = C.set_initial_conditions(0.5,0.5)

    # Solve equations
    solution = odeint(C.diff_eqn, IC, time_, params)

    N1 = solution[:,0]  # predator
    N2 = solution[:,1]  # prey

    # Plot results
    plot_population(N1, N2, time_)
    plot_phase(N1, N2)

    return N1, N2
#----------end main---------


class predator_prey_model:
    "Lotka-Volterra predator-prey model"
    # (dN1/dt) = aN1 - bN1N2
    # (dN2/dt) = -cN2 + dN2N1
    
    # Parameters a,b,c,d 
    def set_parameters(self,a, b,c,d):
        return a,b,c,d

    def set_initial_conditions(self, N1o, N2o):
        return np.array([N1o, N2o])
    
    # Function to integrate:
    def diff_eqn(self, IC, t, a,b,c,d):
        
        dN1_dt = a*IC[0] - b*IC[0]*IC[1]
        dN2_dt = -c*IC[1] + d*IC[0]*IC[1]

        return np.array([dN1_dt, dN2_dt])

#----------end class---------



# Plot population
def plot_population(N1, N2, time_):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_, N1, label='Predator population N1')
    ax.plot(time_, N2, label='Prey population N2')

    ax.fill_between(time_, N1, alpha=0.4)
    ax.fill_between(time_, N2, alpha=0.4)

    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Population densities (N1 or N2)")
    ax.set_title("Lotka-Volterra Predator-Prey model")
    ax.legend(loc="upper right")
    plt.savefig("Part2a_population.png", dpi=300)
    plt.show()


# Plot phase diagram
def plot_phase(N1, N2):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(N1, N2)
    ax.set_xlabel("N1 Population density")
    ax.set_ylabel("N2 Population density")
    ax.set_title("Lotka-Volterra Predator-Prey model: Phase diagram")
    
    plt.savefig("Part2a_phase.png", dpi=300)
    plt.show()

# Execute main function
if __name__ =="__main__":
    main()
