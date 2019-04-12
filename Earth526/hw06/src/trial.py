import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
r1 = signal.boxcar(int(0.2*321/8))
r2 = signal.boxcar(int(1*321/8))

#  r1 = np.zeros(321)
#  r2 = np.zeros(321)
#  r1[150:158] = 1
#  r2[120:160] = 1

r3 = np.convolve(r1,r2)
fig, ax = plt.subplots(3,1)
ax[0].plot(r1, label = "Rise Time")
ax[1].plot(r2, label = "Rupture Time")
ax[2].plot(r3, label = "Convolution")

ax[1].set_ylabel("Amplitude")
ax[0].set_xlabel("Rise Time")
ax[1].set_xlabel("Rupture Time")
ax[2].set_xlabel("Timesteps")
plt.suptitle("Source-time function: convolution of two boxcars")
plt.legend()

#  filename = os.path.join(path, 'boxcars.pdf')
plt.savefig("../figs/boxcars.pdf", dpi=300)
plt.show()
