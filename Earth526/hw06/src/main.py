######################################################
#   WAVEFORM
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 03-13-2019
#
#   Earth 526 Practice Session 6:
#               Waveforms and egf's
#                    
######################################################


# Import modules
import numpy as np
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
plt.ion()

# obspy import stuff
from obspy import read

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw06/figs/'


# read input file
st = read("../raw/2011-11-06-mw57-oklahoma.miniseed")

st.filter('bandpass', freqmax=2, freqmin=0.02)

fig = plt.figure()
ax = fig.add_subplot(111)
for tr in st:

    x = np.linspace(0, 10, tr.data.size)
    ax.plot(x, tr, "k-", lw=0.6)
    
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time (s)")
    ax.set_title("master event waveforms")

filename = os.path.join(path, 'master_waveform.pdf')
plt.savefig(filename, dpi=300)
plt.show()
    
