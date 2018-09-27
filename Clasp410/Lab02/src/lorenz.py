######################################################
#
#   LORENZ EQUATIONS
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 09-18-2018
#
#   Clasp 410 Lab 2: Lorenz equations
#                    Solve using odeint from scipy
######################################################

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def main():
    
    # Create object: 
    C = lorenz_system()

    # Set the values of σ, b, r
    params = C.set_parameters(10, (8/3), 29)   

    # Time related variables
    tmax = 100       # maximum time
    nsteps = 10000    # number of timesteps

    # Create timesteps as an array 
    time_ = np.linspace(0, tmax, nsteps)
    
    # Set initial conditions
    IC = C.set_initial_conditions(1, 1, 1)

    # Perturbed initial conditions
    IC2 = C.set_initial_conditions(1+1e-5, 1+1e-5, 1)

    # Solve equations
    solution = odeint(C.diff_eqn, IC, time_, params)
    
    # Solution after perturbation
    solution2 = odeint(C.diff_eqn, IC2, time_, params)

    x = solution[:,0]
    y = solution[:,1]
    z = solution[:,2]

    x2 = solution2[:,0]
    y2 = solution2[:,1]
    
    # Plot results
    plot_trajectory(x, y, z, time_)
    plot_phase(x, y, z)

    # Plot difference in trajectories
    plot_trajectory_diff(x2-x, y2-y, time_)


    return x, y, z

#----------end main---------


class lorenz_system:
    "Lorenz system of equations"
    # (dx/dt) = -σx + σy
    # (dy/dt) = -xz + rx + y
    # (dz/dt) = xy - bz
    
    # Parameters  σ, b, r
    def set_parameters(self, σ, b, r):
        return σ, b, r

    def set_initial_conditions(self, xo, yo, zo):
        return np.array([xo, yo, zo])
    
    # Function to integrate:
    def diff_eqn(self, IC, t, σ, b, r):
        "IC[0] = x
         IC[1] = y
         IC[2] = z"
        
        dx_dt = -σ*IC[0] + σ*IC[1]
        dy_dt = -IC[0]*IC[2] + r*IC[0] - IC[1]
        dz_dt = IC[0]*IC[1] - b*IC[2]

        return np.array([dx_dt, dy_dt, dz_dt])

#----------end class---------



# Plot trajectories
def plot_trajectory(x, y, z, time_):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_, x, '-', label='x-trajectory', alpha=0.8)
    ax.plot(time_, y, '-', label='y-trajectory', alpha=0.8)
    ax.plot(time_, z, '-', label='z-trajectory', alpha=0.8)

    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Position (x,y,z)")
    ax.set_title("Lorenz system: Trajectories (r = 29)")
    ax.legend(loc="upper right")
    plt.savefig("Part3d_trajectory.png", dpi=300)
    plt.show()

# Plot trajectory difference
def plot_trajectory_diff(x, y, time_):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(time_, x, '-', label='x-difference', alpha=0.8)
    ax.plot(time_, y, '-', label='y-difference', alpha=0.8)

    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Change in position for perturbation (x,y)")
    ax.set_title("Lorenz system: Change in Trajectories ")
    ax.legend(loc="upper right")
    plt.savefig("Part4d_diff.png", dpi=300)
    plt.show()

# Plot phase diagram
def plot_phase(x, y, z):

    #fig = plt.figure()
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8,8))

    ax[0][0].plot(x, y)
    #  ax[0][0].set_xlabel("x axis")
    ax[0][0].set_ylabel("y axis")
    
    ax[1][1].plot(y, z)
    ax[1][1].set_xlabel("y axis")
    #  ax[1][1].set_ylabel("z axis")
    
    ax[1][0].plot(x, z)
    ax[1][0].set_xlabel("x axis")
    ax[1][0].set_ylabel("z axis")
    
    plt.suptitle("Lorenz System: Phase diagram (r = 29) ")
    plt.savefig("Part3d_phase.png", dpi=300)
    plt.show()

# Execute main function
if __name__ =="__main__":
    main()
