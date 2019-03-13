######################################################
#   BRUNE SPECTRAL RATIO
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
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Earth526/hw05/figs/'

# Default Parameters
fc1 = 20
fc2 = 50
Mr = 10    # Moment ratio

def brune_spectrum(Mr, fc1, fc2, f):
    spectral_ratio = Mr*((1 + (f/fc2)**2)/(1 + (f/fc1)**2))
    return spectral_ratio

# Curve fit
def func(f, a, b, c):
    spectral_ratio = a*((1 + (f/c)**2)/(1 + (f/b)**2))
    return spectral_ratio

# noise level in percentage
def noise(level, data):
    return data + np.random.uniform(0, level, data.shape)


def plot1(Mr, fc1, fc2, f):
    y = brune_spectrum(Mr, fc1, fc2, f)
    x = f
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, ".-")
    ax.axvline(x=fc1, linestyle="--", color="k", label=r"$f_{c1}$")
    ax.axvline(x=fc2, linestyle="--", color="k", label=r"$f_{c2}$")
    ax.set_xlabel("Spectral Amplitude Ratio")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Brune's spectral ratio")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.legend()
    filename = os.path.join(path, 'fig1.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

def plot2(data, fit, f, popt):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(f, data, "k-", lw=0.6, label="Synthetic data with noise")
    ax.plot(f, fit, "C0-", lw=1, label="Best fit")
    #  ax.axvline(x=popt[1], linestyle="--", color="k", label=r"$f_{c1}$")
    #  ax.axvline(x=-popt[2], linestyle="--", color="k", label=r"$f_{c2}$")
    #  ax.axhline(y=popt[0], linestyle="--", color="k", label="Moment Ratio")
    ax.set_ylabel("Spectral Amplitude Ratio")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_title("Synthetic spectral ratio (Peak noise amplitude = 50)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.legend()
    filename = os.path.join(path, 'fig_mom_noise_4.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

def main():
    N = 500     # sampling points
    level = 50   # noise level in peak amplitude
    f = np.linspace(3,35, N)
    
    return f, level

f, level = main()
#  plot1(Mr, fc1, fc2, f)

data = brune_spectrum(Mr, fc1, fc2, f)
data2 = noise(level, data)

# Curve fit
popt, pcov = curve_fit(func, f, data2, method='trf', bounds=(-10,200))
fit = func(f, *popt)
plot2(data2, fit, f, popt)


