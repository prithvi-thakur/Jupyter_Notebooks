---
title: "Lab01: Spread of Forest Fires and Infectious Disease"
output: 
    pdf_document:
        latex_engine: xelatex
        sansfont: roboto
author: Prithvi Thakur
date: "08-09-2018"
---

Code and test case
====================


Experiment 1
===================
Considering a dry forest with the following parameters:
```python
# Grid setup
Nx = 250    # Points in the x-direction
Ny = 250    # Points in the y-direction

# Probability that a cell is on fire
prob.start_fire = 0.000025

# Probability a neighboring node catches fire
prob.catch_fire = 1
```

Since the probability of cell catching fire initially is very low, only a few points are on fire initially (Fig 1).

![img1](figs/Experiment1a_0.png)
