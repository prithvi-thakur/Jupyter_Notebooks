######################################################
#   AIRCRAFT FAILURE
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 01-23-2019
#
#   Earth 526 Practice Session 2:
#               Stress Inversion
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw02/figs/'


fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot()
ax.set_xlabel("Crack length a (m)")
ax.set_ylabel("Energy (kPa)")
ax.set_title("Energy vs. Crack Length for Aluminium")
plt.legend()
filename = os.path.join(path, 'fig1.pdf')
plt.savefig(filename, dpi=300)
plt.show()
