#!/usr/bin/python

from src.functions import Functions
from src.constants import Constants
from src.algorithm import Algorithm
from src.plot import Plot

# testine animacija
Constants.n = 10
Constants.tau = 0.01
u_initial = Functions.u_exact_range(0)
func_points, time_points = Algorithm.run(u_initial)

p = Plot()
p.set_data(func_points, time_points)
p.animate(5.0)
