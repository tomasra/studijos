from constants import Constants
from functions import Functions
from thomas import ThomasAlgorithm
from helpers import Helpers

class Algorithm:
    # maksimalus skirtumas tarp buvusiu ir patikslintu u reiksmiu - a.k.a progresas
    @staticmethod
    def _progress(u_old, u_new):
        return max([abs(u_new[i] - u_old[i]) for i in range(0, Constants.n)])

    # u reiksmiu radimas sekanciam laiko momentui
    # sprendziama TLS serija, tikslinant sprendinius iki tam tikro lygio (Constants.delta)
    # u - funkcijos reiksmes dabartiniu laiko momentu
    # t - dabartinis laikas
    @staticmethod
    def _iteration_block(u_now, t):
        u_next_old = u_now                              # pradinis grubus ivertis sekanciam laiko momentui
        u_next_new = []                                 # ieskomi sprendiniai
        f_now = Functions.f_range(t)                    # f(x,t) dabartiniu laiko momentu
        f_next = Functions.f_range(t + Constants.tau)   # f(x,t) sekanciu laiko momentu

        progress = Constants.delta * 2      # gali buti ir kitaip, svarbu kad butu daugiau uz delta
        while (progress >= Constants.delta):
            f_prime_values = Functions.f_prime_range(u_now, u_next_old, f_now, f_next)
            # patikslintas sprendinys
            u_next_new = ThomasAlgorithm.solve(Constants.u_const(), f_prime_values, Constants.kappa, Constants.gamma)
            progress = Algorithm._progress(u_next_old, u_next_new)
            u_next_old = u_next_new
        return u_next_new

    # viso algoritmo vykdymas
    # initial_conditions - pradines u reiksmes nustatytu diskretizacijos zingsniu Constants.h()
    # t - pradinis laiko momentas, paprastai nulis
    @staticmethod
    def run(u_initial, t = 0.0):
        u = u_initial
        results = [u_initial]
        time_points = [t]
        while (t < Constants.t_max):
            u = Algorithm._iteration_block(u, t)
            t += Constants.tau
            results.append(u)
            time_points.append(t)
        return results, time_points
