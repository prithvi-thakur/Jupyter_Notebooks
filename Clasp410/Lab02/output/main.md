---
title: "Lab02: Lotka-Volterra Population Models"
output: 
    pdf_document:
        latex_engine: xelatex
        sansfont: roboto
author: Prithvi Thakur
date: "09-27-2018"
---

Testing
====================

We use the following parameter set for testing:
```python
a = 1, b = 2, c = 1, d = 3
dt = 0.001
tmax = 20 years
```

We test the Lotka-Volterra competition between species model solved using euler forward step. We consider two end memeber cases, when population for either species N1 or N2 is zero, and the other is one. We expect the population to remain constant in these cases. 

![Test1: Fig 1a](figs/Test1a_population.png){width=60%} 
![Test1: Fig 1b](figs/Test1b_population.png){width=60%}

Another test would be to reduce the timesteps and see whether the output changes. If the output doesn't change, then we can assume that the code converges. We begin with a population density of 0.5 for both the species and test with timesteps `dt = 0.001` and `dt = 0.0001`. The figures are shown below.

![Test1: Fig 1c](figs/Test1c_population.png){width=60%} 
![Test1: Fig 1d](figs/Test1c_phase.png){width=60%}

![Test1: Fig 1e](figs/Test1d_population.png){width=60%} 
![Test1: Fig 1f](figs/Test1d_phase.png){width=60%}

Part 1: Competition between species model
==============

For the parameter choice `a = 1, b = 2, c = 1, d = 3`, we see that the species `N2` become extinct, as shown in the figures below. 

![Part1: Fig 1a](figs/Part1a_population.png){width=55%}
![Part1: Fig 1b](figs/Part1a_phase.png){width=55%}

We can compute the range of initial conditions for which each species survive by looking at the steady state. At the steady state, the time-derivative of the population would be zero. Since the derivative is time-independent, the ratio of $N_1/N_2$ at steady state would also give us the initial ratio of the populations.  We can eliminate the trivial cases where $N_1, N_2 = 0$, then we get:

$aN_1(1-N_1) -bN_2N_1 = 0$

$cN_2(1-N_2) - dN_1N_2 = 0$

$a(1-N_1) = bN_2$

$c(1-N_2) = dN_1$

For $a=1, b=2, c=1, d=3$, we get:

$1-N_1 = 2N_2$

$1-N_2 = 3N_1$

$\frac{N_1}{N_2} = \frac{1}{2}$ 

Thus, for the initial ratio $N1/N2 = 1/2$, we can have the species surviving as shown in figure below.

![Part1: Fig 1c](figs/Part1b_population.png){width=60%}
![Part1: Fig 1d](figs/Part1b_phase.png){width=60%}


The plots for different initial conditions with the above set of parameters for the competition between species model is shown below:

![Population: Different colors show different species](figs/Part1g_population.png){width=80%}

![Phase diagrams for a range of initial conditions](figs/Part1g_phase.png){width=80%}

For the parameter choice `a=3, b=2, c=4, d=3`, we see that both the species co-exist.

![Part1: Fig 1e](figs/Part1f_population.png){width=60%}
![Part1: Fig 1f](figs/Part1f_phase.png){width=60%}

Q1. The four equilibrium points can be calculated by setting both the time derivatives to zero. We can get three trivial points at $N_1 = 0, N_2 = 0; N_1 = 1, N_2 = 0; N_1 = 0, N_2 = 1$. The fourth point can be calculated as foolows:

$aN_1(1 - N_1) - bN_1N_2 = 0; cN_2(1 - N_2) -dN_1N_2 = 0$

implies, $a - aN_1 - bN_2 = 0; c - cN_2 - dN_1 = 0$

implies, $N_1 = \frac{c(a - b)}{ac - bd}$

$N_2 = \frac{a(c - d)}{ac - bd}$


Part 2: Predator-Prey Model
=============

We solve the Lotka-Volterra predator-prey model using `odeint` function from python. The parameters are `a=1, b=2, c=1, d=3`. We use maximum timesteps `n=10000` for `tmax=10`years. We show the population and phase plots below:

![Part2: Fig 1a](figs/Part2a_population.png){width=60%}
![Part2: Fig 1b](figs/Part2a_phase.png){width=60%}

We see that for these parameter choices, we get an oscillating population for both the species with periodic highs and lows. They never reach the steady-state, but keep on oscillating. We can see that the phase potrait is a closed curve, which represents an oscillating system.

For comparison, we look at the same solution with euler forward step with 10000 timesteps. There is no difference. 

![Part2: Fig 1a](figs/Part2b_population.png){width=60%}
![Part2: Fig 1b](figs/Part2b_phase.png){width=60%}


Part 3: Lorenz system: parameter study (Rayleigh number)
========================================================

In this part, we solve the lorenz system using `odeint` function from python. We use the following parameters and initial conditions:
```python
sigma = 10; b = 8/3

# Initial Conditions
x = 1; y = 1; z = 1
```

We vary the Rayleigh number `r` and look at the difference in trajectories. The plots are shown below:

![](figs/Part3a_trajectory.png){width=60%}
![](figs/Part3b_trajectory.png){width=60%}

![](figs/Part3c_trajectory.png){width=60%}
![](figs/Part3d_trajectory.png){width=60%}


![](figs/Part3a_phase.png){width=60%}
![](figs/Part3b_phase.png){width=60%}
![](figs/Part3c_phase.png){width=60%}
![](figs/Part3d_phase.png){width=60%}

The trajectories with `r < 25` look like damped oscillations. The phase potraits spiral into one point from some initial condition. The trajectories with `r > 25` look much more chaotic and unpredictable. The phase potraits resemble oscillations that follow the same shape but a different path every time. 

Part 4: Lorenz System
=====================


The parameters and initial conditions are:
```python
sigma = 10; b = 8/3; r = 23

# Initial Conditions
x = 1; y = 1; z = 1
```

Parameter r = 23
----------------

We get the following trajectories and phase diagrams:

![](figs/Part4a_trajectory.png){width=80%}

![](figs/Part4a_phase.png){width=80%}


We perturb the x and y axes by adding a small value $10^{-5}$ and show the plots below. They look same as the above plots for the given parameter sets. The values of x, y, z after 100 years of time converges to a constant value. If we look at the perturbation plot, we can see that the difference between the perturbed and the original values are nearly zero after 100 years of time.

![](figs/Part4b_trajectory.png){width=80%}

![](figs/Part4b_phase.png){width=80%}

The difference in trajectories is shown below:

![](figs/Part4c_diff.png){width=80%}


Parameter r = 25
----------------

Keeping other parameters constant, we change the value of `r` to `25`. The trajectories and the phase diagrams are shown below. The next plot shows the difference in the x and y trajectories. 

![](figs/Part4d_trajectory.png){width=80%}

![](figs/Part4d_phase.png){width=80%}

![](figs/Part4d_diff.png){width=80%}

We see that a small perturbation causes a large difference in the trajectories of `x` and `y`. Also, looking at the trajectories and the phase plot, we see that system is oscillatory over a very small space dimension but unpredictable over larger spatial extent. Thus, we can reasonably predict weather for a very short duration but it is impossible to make any long term predictions based on this models.
