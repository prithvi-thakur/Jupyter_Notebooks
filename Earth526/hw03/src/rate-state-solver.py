######################################################
#   SLIP WEAKENING BEHAVIOR OF RATE-STATE FRICTION
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 02-13-2019
#
#   Earth 526 Practice Session 3:
#           Solve the Differential Algebraic Equation
#           for rate and state friction:              
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy as sp
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw03/figs/'


# Initial Parameters
class params:
    μ = 32e10   # Shear Modulus
    ρ = 2700    # density

    L = 1000    # width of 1D block (m)
    vs = np.sqrt(μ/ρ) # shear wave velocity

    k = μ/L     # spring constant
    Vp = 1e-9   # loading velocity (m/s)
    η = μ/2*vs  # radiation damping

    σ = 100     # Normal Stress = 100 MPa
    fo = 0.6    # Reference friction coefficient = 0.6
    Vo = 1e-6   # Reference slip velocity = 10^(-6) m/s
    Dc = 4   # Critical slip distance = 1 m
    θo = 1  # Initial state variable

    a = 0.012   # Rate-state parameter a
    b = 0.016   # Rate-state parameter b

    tmax = 1    # maximum simulation time in seconds

def traction(P, V, θ):
    return P.σ*( P.fo + P.a*np.log(V/P.Vo + 1) + P.b*np.log(P.Vo*θ/P.Dc) )

def velocity(P, τqs, Vold, θ):
    # solve for velocity
    def f(V):
        return τqs - P.η*V - traction(P, V, θ)
    return sp.optimize.fsolve()

def solver(P, Nx, Nt):

    time = np.linspace(0.001,P.tmax, num=Nt)
    slip = np.linspace(0.001,P.L, num=Nx)
    
    dx = slip[1] - slip[0]
    dt = time[1] - time[0]

    τ = np.zeros((Nx,Nt))
    v = np.zeros((Nx,Nt))
    u = np.zeros((Nx,Nt))
    θ = np.zeros(Nt)

    # Initial conditions
    τ[:,0] = 5
    θ[0] = P.θo
    v[:,0] = np.linspace(1e-3, 5, num=Nx)

    for t in range(Nt-1):
        for x in range(Nx-1):
            
            τ[x,t+1] = traction(P, v[x,t], θ[t])
            v[x,t+1] = v[x,t] + (dt/P.ρ*dx)*(τ[x+1,t] - τ[x,t])

            θ[t+1] = θ[t] + dt*(1 - θ[t]*v[x,t]/P.Dc)

            u[x,t+1] = u[x,t] + v[x,t+1]*dt

    return τ,θ,u,v

def main():
    P = params()
    Nx = 100
    Nt = 100

    return solver(P, Nx, Nt)

def plot(x1,x2,y):
    fig = plt.figure(figsize=(12,5))
    ax1 = fig.add_subplot(121)
    ax1.plot(x1, y, ".-")
    ax1.set_xlabel("Slip velocity (m/s)")
    ax1.set_ylabel("Shear stress (MPa)")
    ax2 = fig.add_subplot(122)
    ax2.plot(x2, y, ".-")
    ax2.set_xlabel("Slip (m)")
    #  ax2.set_ylabel("Shear stress (MPa)")
    plt.suptitle("Stress evolution for a linear slip velocity (Dc = 0.1m)")
    #  plt.legend()
    filename = os.path.join(path, 'fig1_test.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()


t, theto, u, v = main()

plot(v[-2,:], u[-2,:], t[-2,:])


