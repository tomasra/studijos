#!/usr/bin/python

from functions import Functions
from constants import Constants
from algorithm import Algorithm
from plot import Plot

# testine animacija
Constants.n = 10
Constants.tau = 0.01
u_initial = Functions.u_exact_range(0)
func_points, time_points = Algorithm.run(u_initial)

p = Plot()
p.set_data(func_points, time_points)
p.animate(5.0)
