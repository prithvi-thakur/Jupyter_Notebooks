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
Mw = 7      # Moment Magnitude
G = 3e10    # Shear Modulus
Dc = 1    # Critical Slip Distance

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

# Fracture Energy
def fracture(xp, yp):
    return 0.5*xp[1]*(yp[1]-yp[2])
    
# Friction Energy
def friction(xp, yp):
    return xp[2]*yp[2]

# Radiated Energy
def radiated(xp, yp):
    return 0.5*xp[2]*(yp[0]-yp[2])

# Energy partitioning plot
def energy_partition(xp, yp, N, z):
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

    # Fill the fracture energy
    egx = [xp[0], xp[0], xp[1]]
    egy = [yp[2], yp[1], yp[2]]
    eg = round(fracture(xp,yp),2)

    # Fill the friction energy
    efx = [xp[0], xp[0], xp[2], xp[2]]
    efy = [0, yp[2], yp[2], 0]
    ef = round(friction(xp,yp),2)

    # Fill the radiated energy
    erx = [xp[0], xp[0], xp[2]]
    ery = [yp[2], yp[0], yp[2]]
    er = round(radiated(xp,yp),2)

    fig = plt.figure(figsize=(12,5))
    ax1 = fig.add_subplot(121)
    ax1.plot(u, y, ".-")
    ax1.set_xlabel("Displacement (m)")
    ax1.set_ylabel("Shear Stress (MPa)")
    ax1.fill(egx, egy, alpha=0.7, label="Fracture Energy = "+str(eg)+" MPa")
    ax1.fill(efx, efy, alpha=0.7, label="Friciton Energy = "+str(ef)+" Mpa")
    ax1.fill(erx, ery, alpha=0.7, label="Radiated Energy = "+str(er)+" MPa")
    plt.legend()

    # pie chart for energies
    labels = ["Fracture Energy = "+str(eg)+" MPa", "Friction Energy = "+str(ef)+" MPa", "Radiated Energy = "+str(er)+" MPa"]
    sizes = [eg, ef, er]
    ax2 = fig.add_subplot(122)
    patches = ax2.pie(sizes, autopct="%.2f%%", wedgeprops={'alpha':0.7})
    plt.legend(patches, labels=labels, loc="best")
    ax2.axis('equal')
    plt.suptitle("Energy Partitioning at "+str(z)+" km depth")

    filename = os.path.join(path, 'depth'+str(int(z))+'.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

#  Partitioning energy as a function of depth
def partition_plot(xp,yp,z):
    eg = fracture(xp,yp)
    ef = friction(xp,yp)
    er = radiated(xp,yp)
    
    fig = plt.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    ax1.plot(eg, z, ".-", label="Fracture Energy")
    ax1.plot(ef, z, ".-", label="Friction Energy")
    ax1.plot(er, z, ".-", label="Radiated Energy")
    ax1.set_xlabel("Energy (MPa)")
    ax1.set_ylabel("Depth (km)")
    ax1.invert_yaxis()
    plt.legend()
    filename = os.path.join(path, 'energy_part_M7.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

def main():
    # Depth
    z = np.linspace(3, 15, num=13)
    #  i = 12

    N = 10
    
    # effective normal stress
    σn = eff_normal_stress(z)

    # Static and dynamic strength
    τs = tau(μs, σn)
    τd = tau(μd, σn)

    # Shear Stress before and after the earthquake
    τbefore = Δσ + τd
    τafter = τd

    # Rupture dimensions
    L, S = rupture_dims(moment(Mw), Δσ)
    
    # Final Slip
    Df = final_slip(G, L, Δσ) 

    # Plotting stuff
    xp = np.array([0,Dc,Df])
    yp = np.array([τbefore,τs,τafter])

    return xp, yp, N, z

xp, yp, N, z = main()
#  energy_partition(xp, yp, N,z)
partition_plot(xp,yp,z)
