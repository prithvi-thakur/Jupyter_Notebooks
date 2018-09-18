---
title: "Lab02: Lotka-Volterra Population Models"
output: 
    pdf_document:
        latex_engine: xelatex
        sansfont: roboto
author: Prithvi Thakur
date: "09-16-2018"
---

Testing
====================


The following conditions should be a sufficient test for the workflow.

* Every timestep ignites just the four neighboring cells.
* The initial fire is extinguished after igniting the neighbors.
* The boundaries are not lit on fire.
* Do not ignite the bare patches within the domain.


Part 1: Competition between species model
==============

For the parameter choice `a = 1, b = 2, c = 1, d = 3`, we see that the species `N2` become extinct, as shown in the figures below. 
![Part1: Fig 1a](figs/Part1a_population.png)
![Part1: Fig 1b](figs/Part1a_phase.png)


Experiment 2
=============
