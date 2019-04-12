# Figure 1 stuff.

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square


A = 0.01
w = 2
x = np.linspace(0,80, num=1000)

y = A*square(w*x) + 0.4


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(x,y, "k")
ax.set_ylabel("Dc (m)")
plt.savefig("fig1.pdf")
plt.show()
