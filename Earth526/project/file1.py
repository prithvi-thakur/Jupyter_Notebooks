# Figure 1 stuff.

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

N = 100
A = 0.1
w = 5
x = np.linspace(0,25e3, num=N)

y = A*square(w*x*2*np.pi/25e3) + 1


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(x,y, "k.-")
ax.set_ylabel("Dc (m)")
plt.savefig("fig1.pdf")
plt.show()

np.savetxt("dc_values.txt",  np.array([x,y]).transpose(), fmt="%.2f")
