---
title: "Lab01: Spread of Forest Fires and Infectious Disease"
output: 
    pdf_document:
        latex_engine: xelatex
        sansfont: roboto
author: Prithvi Thakur
date: "09-13-2018"
---

Testing
====================

For testing, we consider a small grid of 10x10 space dimensions. The boundaries are bare groundand the rest of the inner domain is all forest. The probability of starting fire is low enough to ignite just one cell. The probability of neighbours catching fire is 1. We look at first few timestep to see the propagation of fire. 

The following conditions should be a sufficient test for the workflow.

* Every timestep ignites just the four neighboring cells.
* The initial fire is extinguished after igniting the neighbors.
* The boundaries are not lit on fire.
* Do not ignite the bare patches within the domain.

We begin with the following set of parameters:
```python
Grid Dimensions: 10 x 10

# Probabilities
start_fire = 0.01 # Low enough such that very few cells are on fire
catch_fire = 1    # every neighboring cell catches fire
bare_patch = 0  # There is no bare patch 
```
The following figures show first few iterations for this simple setup.

![Test case 1: Initial fire and boundaries](figs/test0.png)
![Test case 1](figs/test1.png)
![Test case 1](figs/test2.png)
![Test case 1](figs/test3.png)

The next test has similar setup as above with some bare patches inside the domain. We test whether the fire spreading finds the neighboring trees correctly. Every parameter is same as above except the probability of bare patch `bare_patch = 0.02`. I have skipped the first few iterations so as to not display too many figures. 

![Test case 2: Initial fire and boundaries](figs/test_b3.png)
![Test case 2](figs/test_b4.png)
![Test case 2](figs/test_b5.png)
![Test case 2](figs/test_b6.png)

The above cases are sufficient to test the validity of the numerical procedure and code, assuming the probabilities for spreading fire work correctly, which can be seen from subsequent experiments.


Experiment 1
==============
Considering a dry forest with the following parameters:
```python
# Grid setup
Nx = 250    # Points in the x-direction
Ny = 250    # Points in the y-direction

# Probability that a cell is on fire
start_fire = 0.000025

# Probability a neighboring node catches fire
catch_fire = 1

# Probability that there is a bare patch in the inner grid
bare_patch = 0
```

Since the probability of cell catching fire initially is very low, only a few points are on fire initially (Experiment 1A). I have shown two figs, the initial grid with fire at one point, and grid after 50 iterations. Since the probability of neighbours catching fire is 1, we see a diamond shaped radiation pattern of the fire spread.

![Experiment 1: Initial fire and boundaries](figs/Experiment1a_0.png)
![Experiment 1: after 50 iterations](figs/Experiment1a_50.png)

We will look at a grid with 50% forest (Experiment 1B), and then with no forest. Since the fire spreads with a probability of 1, the presence of more bare patches would significantly inhibit the fire from spreading. With 100% forest, the entire forest burns inevitably. For 50% forest, a very small fraction of the forest burns before the fire dies out. The fire is more localized. I have shown the initial, middle, and final iteration for this case below.

![Experiment 1: 50 percent forest](figs/exp_1b0.png)
![Experiment 1: 50 percents forest](figs/exp_1b56.png)
![Experiment 1: 50 percents forest](figs/exp_1b112.png)


For a grid with no forest (Experiment 1C), there will never be any fire ignited, and the testing would be trivial. It will be a grey patch with no fire ever, therefore the computation will never progress to the time loop. The output is shown in figure below.

![Experiment 1: 0 percents forest](figs/exp_1c.png)


Experiment 2
=============
The parameters are as follows:
```python
bare_patch = 0.0 
start_fire = 0.000025
catch_fire = # varying between 0 and 1
```

I will show three test cases: 
```python 
Experiment 2A: catch_fire = 0.1
Experiment 2B: catch_fire = 0.5
Experiment 2C: catch_fire = 0.9
```

I am ignoring the trivial test case of `catch_fire = 0`. The results for `catch_fire = 1` are already shown in previous experiment. The results for this experiment are shown below for three iterations, the initial setting, the middle iteration, and the final iteration.

![Experiment 2: 10 percent probability to catch fire](figs/exp2a_0.png)
![Experiment 2: 10 percent probability to catch fire](figs/exp2a_1.png)
![Experiment 2: 10 percent probability to catch fire](figs/exp2a_2.png)

For the above case with 10% catch fire probability, the fire stops after 1-2 iterations almost every time. This would be very similar to a forest with 90 percent bare patch. Anything with less than 50% probability would spread fire to a vry small and localized region of the grid. For probabilitites greater than 50%, most of the forest would be demolished, similar to what would happen with less than 50% bare patches. The results are shown below.

![Experiment 2: 50 percent probability to catch fire](figs/exp2b_0.png)
![Experiment 2: 50 percent probability to catch fire](figs/exp2b_131.png)
![Experiment 2: 50 percent probability to catch fire](figs/exp2b_261.png)

![Experiment 2: 50 percent probability to catch fire](figs/exp2c_0.png)
![Experiment 2: 50 percent probability to catch fire](figs/exp2c_144.png)
![Experiment 2: 50 percent probability to catch fire](figs/exp2c_287.png)

We see that the fire-spreading radiation pattern for 90% probability is very similar to the diamond shape (just like experiment 1a) with some noise.


Experiment 3
==============
For a more realistic model, we use the following parameters:
```python
bare_patch = 0.225
start_fire = 0.000025
catch_fire = 0.7
```

We show the results at five different iterations below. The spreading pattern looks like a fractal. The fire spreads for a longer duration (number of iterations) but the total amount of trees burnt would be proportonal to the product of initial probabilities.

![Experiment 3: Mixed setting](figs/exp3_50.png)
![Experiment 3: Mixed setting](figs/exp3_100.png)
![Experiment 3: Mixed Setting](figs/exp3_200.png)
![Experiment 3: Mixed Setting](figs/exp3_300.png)
![Experiment 3: Mixed Setting](figs/exp3_400.png)


Experiment 4
=============
Ebola virus model: Immune people are grey. Dead people are blue. Healthy people are green. Infected people are red.

The following experiments are described:

* 4A: 70% disease spread rate, 22.5% immune to disease
* 4B: 90% disease spread rate, 40% imune to disease
* 4C: 50% disease spread rate, 0% immune to disease

We see that for 70% disease spread rate, around 20 to 30 % people vaccinated would arrest the spread of disease in most cases. 22.5% turns out to be very optimum percentage to be vaccinated. 

![Experiment 4: Ebola](figs/exp4a_10.png)
![Experiment 4: Ebola](figs/exp4a_50.png)
![Experiment 4: Ebola](figs/exp4a_100.png)


For 90% disease spread rate, about 40% of people being vaccinated is sufficient to localize the spread of disease. 

![Experiment 4: Ebola](figs/exp4b_10.png)
![Experiment 4: Ebola](figs/exp4b_50.png)
![Experiment 4: Ebola](figs/exp4b_100.png)

For anything below 50% disease spread rate, even 0% immunized is sufficient to localize the spread. At exactly 50% spread rate, anything above 0% immunization will work. And at exactly 0% immunization, the spread may or may not be contained. 

![Experiment 4: Ebola](figs/exp4c_10.png)
![Experiment 4: Ebola](figs/exp4c_50.png)
![Experiment 4: Ebola](figs/exp4c_100.png)


Questions
=========
Q1. Three things to make the model more realistic:

1. Instead of using probabilities, we can use a diffusion equation (or an equivalent partial differential equation) to model the spread of disease, and the model constraints would come from real observations. That would help us match the real observations, as well as predict the future spread of disease.
2. We can use a realistic spatial grid, like something from google maps where we know the population and location of people in a region.
3. In the case of forest fire, take seasonal and wind variations into account, and modify probabilities accordingly.


Q2. We can define drought as some extended period with low rainfall. During this period, the probability of fire catching and fire spreading would significantly increase.

Q3. If the fires can ignite their diagonal neighbour nodes, and the entire forest is trees the radiation pattern of fire spreading would change, and it wouldlook like a rectangular spreading front, as opposed to a diamond front. In other cases, the fire spread would be more than the current case even for a lower probability of spreading.  


Bonus
======

Bonus question 1 submitted as code.


Bonus question 2:
-----------------
Parameters used:
```python
start_disease = 0.000025 # Probability of initiating disease
catch_disease = 0.7      # Probability of spreading disease
immune = 0               # Probability that there is immunization
cure_prob = 0.5          # Probability that a person is cured and immune
                         # to further disease
```

I have used no people with immunization (grey patches) initially to show the effect of being cured. Dead people are represented with blue color, and the rest is same. Certain iterations are shown below:

![Bonus 2: Ebola](figs/bonus_10.png)
![Bonus 2: Ebola](figs/bonus_50.png)
![Bonus 2: Ebola](figs/bonus_100.png)
![Bonus 2: Ebola](figs/bonus_200.png)
