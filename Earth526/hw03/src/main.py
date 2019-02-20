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
    Dc = 0.4   # Critical slip distance = 1 m
    θo = 1  # Initial state variable

    a = 0.012   # Rate-state parameter a
    b = 0.016   # Rate-state parameter b

    tmax = 10    # maximum simulation time in seconds

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
    #  return np.linspace(1e-2,5, num=N)
    return np.linspace(1e-2, 4, num=N)
    #  v1 = (np.linspace(1e-1, 1, num=int(N/3)))
    #  v2 = (np.linspace(1, 5, num=int(N/3)))
    #  v3 = (np.linspace(5, 1, num= N - 2*int(N/3)))
    #  return np.hstack([v1, v2, v3])

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
        θ[it+1] = evolution(θ[it], dt, V[it+1], params.Dc)
        τ[it+1] = rsf(params, V[it+1], θ[it+1])
        x[it+1] = V[it]*time[it] + x[it]
        
        #  print(θ[it])
        #  print(τ[it])
    return θ[1::], τ[1::], V[1::], x[1::], time[1::]

def main():
    p = params()
    N = 80
    
    return solver(p, N)



def plot(x1,x2,y):
    fig = plt.figure(figsize=(10,4))
    ax1 = fig.add_subplot(121)
    ax1.plot(x1, y, ".-")
    ax1.set_xlabel("Slip velocity (m/s)")
    ax1.set_ylabel("Shear stress (MPa)")
    ax2 = fig.add_subplot(122)
    ax2.plot(x2, y, ".-")
    ax2.set_xlabel("Slip (m)")
    #  ax2.set_ylabel("Shear stress (MPa)")
    plt.suptitle("Stress evolution for a nonlinear slip velocity (Dc = 0.4 m)")
    #  plt.legend()
    filename = os.path.join(path, 'fig4.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

def plot2(v,t):
    fig = plt.figure(figsize=(5,4))
    ax1 = fig.add_subplot(111)
    ax1.plot(t, v, ".-")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Slip Velocity (m/s)")
    ax1.set_title("Assumed Slip Velocity in time")
    filename = os.path.join(path, 'fig4_v.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

state, stress, V, x, time = main()
plot(V, x, stress)
plot2(V, time)
