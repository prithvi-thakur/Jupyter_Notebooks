######################################################
#   SLIP WEAKENING BEHAVIOR OF RATE-STATE FRICTION
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 02-13-2019
#
#   Earth 526 Practice Session 3:
#               Friction laws
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw03/figs/'


# Initial Parameters
class params:
    σ = 100   # Normal Stress = 100 MPa
    μo = 0.6    # Reference friction coefficient = 0.6
    Vo = 1e-6   # Reference slip velocity = 10^(-6) m/s
    Dc = 0.1   # Critical slip distance = 1 m
    θo = 0.001  # Initial state variable

    a = 0.012   # Rate-state parameter a
    b = 0.016   # Rate-state parameter b

    tmax = 1    # maximum simulation time in seconds

# This function takes the rate-state parameters and the current slip rate to return the current shear stress:
def rsf(params, V, θ):
    return params.σ*(params.μo + params.a*np.log(V/params.Vo) + params.b*np.log(θ*params.Vo/params.Dc))

# Evolution of the state variable at the next timestep
# given everything at current timestep
def evolution(θt, dt, Vt, Dc):
    θ = θt + dt*(1 - θt*Vt/Dc)
    return θ


# Initial sliding velocity assumption
def initial_velocity(N):
    return np.linspace(1e-2,5, num=N)

def solver(params, N):
    #  x = np.linspace(0,100*params.Dc, num=N)
    time = np.linspace(0.001,params.tmax, num=N)
    diff_t = np.diff(time)
    V = initial_velocity(N)
        
    θ = np.zeros(N)
    θ[0] = params.θo
    τ = np.zeros(N)
    x = np.zeros(N)

    for it in range(len(time)-1):
        dt = diff_t[0]  # dt is constant
        θ[it+1] = evolution(θ[it], dt, V[it], params.Dc)
        τ[it+1] = rsf(params, V[it+1], θ[it+1])
        x[it] = V[it]*time[it] + x[it]
        
        print(θ[it])
        print(τ[it])
    return θ[1::], τ[1::], V[0:-1], x[0:-1]

def main():
    p = params()
    N = 100
    
    return solver(p, N)



def plot(x,y):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.plot(x, y, ".-")
    ax.set_xlabel("Slip (m)")
    ax.set_ylabel("Shear stress (MPa)")
    ax.set_title("Stress evolution for a linear slip velocity (Dc = 0.1m)")
    #  plt.legend()
    filename = os.path.join(path, 'fig1.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()


stress, state, V, x = main()
plot(x, stress)
