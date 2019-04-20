import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

A = 0.01
w = 40

x = np.linspace(0,80,num=100)
y = A*square(w*x) + 0.4

np.savetxt([x,y],"dc_values.txt")
