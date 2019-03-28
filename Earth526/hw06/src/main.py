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


# read input master file
master2 = read("master/*_BHE.sac.cut2")

# read input egf file
egf2 = read("egf/*_BHE.sac.cut2")

# choose only same stations
master = master2[0:9] + master2[10:12]
egf = egf2[0:5] + egf2[6:8] + egf2[9:13]


# azimuth locations
az = np.array([346.809, 8.22197, 24.9644, 65.1387, 1.4733, 70.2195, 75.3622, 133.176, 110.339, 161.071, 129.729])

#  st.filter('bandpass', freqmax=2, freqmin=0.02)

# choose just the east west
#  st = st[0::3]    # east west
#  st = st[1::3]       # north south
#  st = st[2::3]       # vertical

#  for tr in st:
    #  # write to sac
    #  name = tr.meta.station + "_" + tr.meta.channel + ".sac"
    #  tr.write(name, format="SAC")
    

# Create convolution boxcar
from scipy import signal

#  N = egf[k].meta.npts

tr = 0.2    # rise time
#  tc = 2    # rupture duration

def convolve(tr,tc,egf):

    N = egf.meta.npts
    rise_time = signal.boxcar(int(tr*N/8))
    rupture_time = signal.boxcar(int(tc*N/8))

    trapezoid = np.convolve(rise_time, rupture_time)

    conv1 = np.convolve(trapezoid, egf.data)[trapezoid.size-2:-1]

    conv1 = (conv1 - np.mean(conv1))/(np.max(conv1-np.mean(conv1)))
    orig = (egf.data - np.mean(egf.data))/(np.max(egf.data - np.mean(egf.data)))

    return conv1, orig

def plot_waveforms(mas, egf, rup_time):
    stno = 11
    fig, ax = plt.subplots(11,1)
    
    for i in range(11):
        
        conv1, ori = convolve(0.2, rup_time[i], egf[i])
        orig = (mas[i].data - np.mean(mas[i].data))/(np.max(mas[i].data - np.mean(mas[i].data)))
        ax[i].plot(conv1, label="convolved egf")
        ax[i].plot(orig, label="master")
        
    ax[5].set_ylabel("Normalized Amplitude")
    ax[i].set_xlabel("Timesteps")
    plt.suptitle("Waveforms")
    plt.legend()

    #  filename = os.path.join(path, 'master_waveform.pdf')
    #  plt.savefig(filename, dpi=300)
    plt.show()

    
#  conv1, orig = convolve(tr,tc, egf[k])

def minimize(egf, mas, tr):
    tc = np.linspace(0.05,1.5,30)
    #  orig = mas.data 
    orig = (mas.data - np.mean(mas.data))/(np.max(mas.data - np.mean(mas.data)))
    
    mf = np.zeros(30)

    for i in range(30):
        conv1,o = convolve(tr,tc[i],egf)
        mf[i] = misfit(orig,conv1)
    
    i = np.where(mf == np.min(mf))[0][0]
    return mf[i], tc[i]

# plot station azimuth and rupture time

# function for misfit values each station
def station_min(egf,mas):
    tr = 0.2
    stno = 11
    rup_time = np.zeros(stno)
    misf = np.zeros(stno)

    for i in range(stno):
        misf[i], rup_time[i] = minimize(egf[i],mas[i],tr)
    
    return misf,rup_time

def plot1(conv1, orig):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(conv1, label="convolved data")
    ax.plot(orig, label="original data")

    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Timesteps")
    ax.set_title("Convolution")
    ax.legend()

    #  filename = os.path.join(path, 'master_waveform.pdf')
    #  plt.savefig(filename, dpi=300)
    plt.show()

def plot_az(az, rup_time):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(az, rup_time, "o")

    ax.set_ylabel("Rupture Time (sec)")
    ax.set_xlabel("Station Azimuth")
    ax.set_title("Rupture Directivity")

    filename = os.path.join(path, 'directivity2.pdf')
    plt.savefig(filename, dpi=300)
    plt.show()

# Master normalize
#  mas1 = (master[k].data - np.mean(master[k].data))/(np.max(master[k].data - np.mean(master[k].data)))
def plot2(conv1, mast1):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(conv1, label="convolved data")
    ax.plot(mas1, label="master data")

    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Timesteps")
    ax.set_title("master event waveforms")
    ax.legend()

    #  filename = os.path.join(path, 'master_waveform.pdf')
    #  plt.savefig(filename, dpi=300)
    plt.show()


# misfit
def misfit(mas, egf_con):
    return np.linalg.norm(mas - egf_con)
