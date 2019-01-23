######################################################
#   AIRCRAFT FAILURE
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 01-23-2019
#
#   Earth 526 Practice Session 1:
#               Griffith's failure theory: Aircraft
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw01/figs/'

# Properties
E = 69e9
G = 20e3
sigma = 140e6

# Crack length
N = 30
a = np.linspace(0,0.1,N)

# Energy
surface = G*a
strain = -(sigma**2 *np.pi * a**2)/(2*E)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(a, surface/1e3, "k--", label="Surface Energy")
ax.plot(a, strain/1e3, "ko-", label="Strain Energy")
ax.plot(a, (surface+strain)/1e3, "k-", label="Total Energy")
ax.axvline(x=0.022, color="blue", label="Critical Crack Length = 0.022 m")
ax.axhline(y=0, color="black")
ax.set_xlabel("Crack length a (m)")
ax.set_ylabel("Energy (kPa)")
ax.set_title("Energy vs. Crack Length for Aluminium")
plt.legend()
filename = os.path.join(path, 'fig1.pdf')
plt.savefig(filename, dpi=300)
plt.show()
