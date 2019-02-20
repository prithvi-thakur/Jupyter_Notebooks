######################################################
#   ENERGY PARTITIONING IN EARTHQUAKES
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 02-13-2019
#
#   Earth 526 Practice Session 4:
#               Energy Balance
#                    
######################################################


# Import modules
import numpy as np
import os
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw04/figs/'

# Parameters
μs = 0.6    # Static Friction Coefficient
μd = 0.2    # Dynamic Friction Coefficient
Δσ = 3      # Stress drop constant at 3 MPa
Mw = 5      # Moment Magnitude
G = 3e10    # Shear Modulus
Dc = 0.1    # Critical Slip Distance

# Effective normal stress (17 MPa/ km)
def eff_normal_stress(z):
    return 17*z

# Shear Strength
def tau(σn, μ):
    return μ*σn

# Moment
def moment(Mw):
    Mo = 10**((10.7 + Mw)*(3/2))/1e7
    return Mo

# Rupture length and area
def rupture_dims(Mo, Δσ):
    L = (Mo/(Δσ*1e6))**(1/3)
    return L, L**2

# Final Slip
def final_slip(G, L, Δσ):
    return Δσ*1e6*L/G


# Energy partitioning plot
def energy_partition(xp, yp, N):
    # x-axis slip
    u1 = np.linspace(xp[0], xp[0], num=N)
    u2 = np.linspace(xp[0], xp[1], num=N)
    u3 = np.linspace(xp[1], xp[2], num=N)
    u = np.hstack([u1,u2,u3])
    
    # y-axis stress
    y1 = np.linspace(yp[0], yp[1], num=N)
    y2 = np.linspace(yp[1], yp[2], num=N)
    y3 = np.linspace(yp[2], yp[2], num=N)
    y = np.hstack([y1,y2,y3])

    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    ax1.plot(u, y, ".-")
    ax1.set_xlabel("Displacement (m)")
    ax1.set_ylabel("Shear Stress (MPa)")
    ax1.set_title("Energy Partitioning")
    filename = os.path.join(path, 'fig1.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()
    # line 1
    #  l1 = np.interp(np.hstack([u1,u2,u3]), xp,yp)
    #  l1 = np.interp(u1, np.array([xp[0], xp[1]]))

    #  return 

def main():
    # Depth
    #  z = np.linspace(3, 15, num=12)
    z = 3 

    N = 10
    
    # effective normal stress
    σn = eff_normal_stress(z)

    # Static and dynamic strength
    τs = tau(μs, σn)
    τd = tau(μd, σn)

    # Shear Stress before and after the earthquake
    τbefore = Δσ + τd
    τafter = τd

    print(τafter)
    print(τbefore)
    print(τs)

    # Rupture dimensions
    L, S = rupture_dims(moment(Mw), Δσ)
    
    # Final Slip
    Df = final_slip(G, L, Δσ) 

    # Plotting stuff
    xp = np.array([0,Dc,Df])
    yp = np.array([τbefore,τs,τafter])

    return xp, yp, N

xp, yp, N = main()
energy_partition(xp, yp, N)

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

