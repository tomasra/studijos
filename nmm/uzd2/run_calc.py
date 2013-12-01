#!/usr/bin/python

from src.algorithm import Algorithm
from src.constants import Constants
from src.functions import Functions

runs = 6

# skaiciavimai
Constants.n = 5
Constants.tau = 0.1

# penkis kartus mazinami zingsniai
for i in range(0, runs):
    u_initial = Functions.u_exact_range(0)
    func_points, time_points = Algorithm.run(u_initial)
    error_total = Functions.u_error_total(func_points, time_points)
    print "h = %.5f, tau = %.5f, netiktis: %.10f" % (Constants.h(), Constants.tau, error_total)
    Constants.n *= 2
    Constants.tau /= 2.0
