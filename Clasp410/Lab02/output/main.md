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

For testing, we consider a small grid of 10x10 space dimensions. The boundaries are bare groundand the rest of the inner domain is all forest. The probability of starting fire is low enough to ignite just one cell. The probability of neighbours catching fire is 1. We look at first few timestep to see the propagation of fire. 

The following conditions should be a sufficient test for the workflow.

* Every timestep ignites just the four neighboring cells.
* The initial fire is extinguished after igniting the neighbors.
* The boundaries are not lit on fire.
* Do not ignite the bare patches within the domain.


Part 1: Competition between species model
==============
<!-- ![Experiment 1: 0 percents forest](figs/exp_1c.png) -->


Experiment 2
=============
